#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Gemini 3.1 Pro Preview 并行批量优化(8 路并发)

复用 optimize_with_gemini.py 的 collect_targets / build_prompt / call_gemini / split_md_and_notes。
加上 ThreadPoolExecutor 并发调度 + 进度写入 stdout(每完成一个文件打一行)。
"""

import os
import sys
import json
import time
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed

# 把脚本目录加到 sys.path 以便导入
sys.path.insert(0, str(Path(__file__).resolve().parent))

from optimize_with_gemini import (
    collect_targets,
    load_review_map,
    build_prompt,
    call_gemini,
    split_md_and_notes,
    ROOT,
    OUT_DIR,
)

CONCURRENCY = int(os.environ.get("OPT_CONCURRENCY", "8"))


def process_one(path, review_map, api_key):
    """单文件处理,返回 record dict"""
    rel = path.relative_to(ROOT)
    out_path = OUT_DIR / rel
    out_path.parent.mkdir(parents=True, exist_ok=True)

    content = path.read_text(encoding="utf-8")
    review = review_map.get(str(rel))
    orig_len = len(content)

    prompt = build_prompt(path, content, review)
    t0 = time.time()
    result = call_gemini(prompt, api_key)
    dt = time.time() - t0

    base = {
        "file": str(rel),
        "elapsed": round(dt, 1),
        "orig_len": orig_len,
    }

    if not result.get("ok"):
        base.update({"status": "failed", "error": result.get("error", "unknown")})
        return base

    text = result["text"]
    usage = result.get("usage", {})
    md_body, notes = split_md_and_notes(text)
    out_path.write_text(md_body + "\n", encoding="utf-8")

    opt_len = len(md_body)
    delta_pct = (opt_len - orig_len) / orig_len * 100 if orig_len else 0

    base.update({
        "status": "ok",
        "opt_len": opt_len,
        "delta_pct": round(delta_pct, 1),
        "finish": result.get("finishReason"),
        "in_tokens": usage.get("promptTokenCount", 0),
        "out_tokens": usage.get("candidatesTokenCount", 0),
        "thinking_tokens": usage.get("thoughtsTokenCount", 0),
        "notes": notes,
        "review_overall": (review or {}).get("review", {}).get("overall") if review else None,
    })
    return base


def main():
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("ERROR: GEMINI_API_KEY not set")
        sys.exit(1)

    review_map = load_review_map()
    targets = collect_targets()
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    # stdout 即时 flush(让 Monitor 看得到每行)
    sys.stdout.reconfigure(line_buffering=True)

    print(f"=== 并行优化 ({CONCURRENCY} 路) · {len(targets)} 文件 ===", flush=True)

    records = []
    t_start = time.time()
    success = failed = 0
    total_in = total_out = total_think = 0

    with ThreadPoolExecutor(max_workers=CONCURRENCY) as ex:
        futs = {ex.submit(process_one, p, review_map, api_key): p for p in targets}
        for i, fut in enumerate(as_completed(futs), 1):
            try:
                rec = fut.result()
            except Exception as e:
                p = futs[fut]
                rec = {
                    "file": str(p.relative_to(ROOT)),
                    "status": "failed",
                    "error": f"{type(e).__name__}: {e}",
                    "elapsed": 0,
                    "orig_len": 0,
                }
            records.append(rec)

            if rec["status"] == "ok":
                success += 1
                total_in += rec.get("in_tokens", 0)
                total_out += rec.get("out_tokens", 0)
                total_think += rec.get("thinking_tokens", 0)
                print(
                    f"[{i:2d}/{len(targets)}] ✅ {rec['file']}  "
                    f"{rec['elapsed']}s  {rec['orig_len']:,}→{rec['opt_len']:,} "
                    f"({rec['delta_pct']:+.0f}%)  "
                    f"tok in {rec['in_tokens']:,}/out {rec['out_tokens']:,}/thk {rec['thinking_tokens']:,}",
                    flush=True,
                )
            else:
                failed += 1
                print(
                    f"[{i:2d}/{len(targets)}] ❌ {rec['file']}  "
                    f"{rec['elapsed']}s  ERROR: {rec.get('error','')[:80]}",
                    flush=True,
                )

    t_total = time.time() - t_start

    # 写 _audit.md
    audit = [
        "# 优化审计报告(并行版)",
        "",
        f"> 模型:gemini-3.1-pro-preview",
        f"> 并发度:{CONCURRENCY}",
        f"> 总耗时:{t_total:.1f}s",
        f"> 成功:{success} · 失败:{failed} · 总计:{len(targets)}",
        f"> Token:输入 {total_in:,} · 输出 {total_out:,} · 思考 {total_think:,} · 合计 {total_in+total_out+total_think:,}",
        "",
        "---",
        "",
    ]
    for rec in sorted(records, key=lambda r: r["file"]):
        audit.append(f"## `{rec['file']}`")
        audit.append("")
        if rec["status"] == "failed":
            audit.append(f"❌ **失败**:{rec.get('error', '')}")
        else:
            audit.append(f"- **耗时**:{rec['elapsed']}s · **状态**:{rec['finish']}")
            audit.append(f"- **字符数**:{rec['orig_len']:,} → {rec['opt_len']:,} ({rec['delta_pct']:+.1f}%)")
            audit.append(f"- **Token**:in {rec['in_tokens']:,} / out {rec['out_tokens']:,} / thinking {rec['thinking_tokens']:,}")
            if rec.get("review_overall") is not None:
                audit.append(f"- **优化前评分**:{rec['review_overall']}/10")
            if rec.get("notes"):
                audit.append("")
                audit.append("**Gemini 改动说明**:")
                audit.append("")
                audit.append(rec["notes"])
        audit.append("")
        audit.append("---")
        audit.append("")

    (OUT_DIR / "_audit.md").write_text("\n".join(audit), encoding="utf-8")

    # 写 _summary.md
    ok_recs = [r for r in records if r["status"] == "ok"]
    summary = [
        "# 优化总结(并行版)",
        "",
        f"> 模型:gemini-3.1-pro-preview",
        f"> 并发:{CONCURRENCY} 路 · 总耗时 **{t_total:.1f}s**",
        f"> 成功 {success} / 失败 {failed} / 总 {len(targets)}",
        "",
        "## Token 总消耗",
        "",
        f"- 输入 prompt:{total_in:,}",
        f"- 输出 completion:{total_out:,}",
        f"- 思考 thinking:{total_think:,}",
        f"- **合计**:{total_in + total_out + total_think:,}",
        "",
    ]
    if ok_recs:
        deltas = [r["delta_pct"] for r in ok_recs]
        summary.append("## 字符数变化")
        summary.append("")
        summary.append(f"- 平均变化:**{sum(deltas)/len(deltas):+.1f}%**")
        summary.append(f"- 最大增长:{max(deltas):+.1f}%")
        summary.append(f"- 最大缩减:{min(deltas):+.1f}%")
        summary.append("")
        summary.append("## 每个文件的优化幅度")
        summary.append("")
        summary.append("| 文件 | 原 | 新 | 变化 | 耗时 | 前评分 |")
        summary.append("|---|---|---|---|---|---|")
        for r in sorted(ok_recs, key=lambda x: x["file"]):
            score = r.get("review_overall", "-")
            summary.append(
                f"| `{r['file']}` | {r['orig_len']:,} | {r['opt_len']:,} | "
                f"{r['delta_pct']:+.1f}% | {r['elapsed']}s | {score} |"
            )

    (OUT_DIR / "_summary.md").write_text("\n".join(summary), encoding="utf-8")

    print(f"\n=== 完成 {success}/{len(targets)} · 总耗时 {t_total:.1f}s ===", flush=True)
    print(f"audit:   {OUT_DIR / '_audit.md'}", flush=True)
    print(f"summary: {OUT_DIR / '_summary.md'}", flush=True)


if __name__ == "__main__":
    main()
