#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
用 Gemini 3.1 Pro Preview 批量优化研究报告

策略:
- 全量扫描 27 个研究 md 文件
- 每个文件交给 Gemini 3.1 Pro 做"可读性优化 + 解决评审问题"
- 优化版写入 optimized/ 镜像目录,不动原文
- 每个文件的"改动说明"写入 optimized/_audit.md
- 全局总结写入 optimized/_summary.md

用法:
    export GEMINI_API_KEY=xxx
    python3 scripts/optimize_with_gemini.py [--dry-run] [--only 文件名关键词]

依赖:
    质量评审报告.md 和 scripts/out/quality_raw.json 作为"改什么"的输入
"""

import os
import re
import json
import sys
import time
from pathlib import Path
import urllib.request
import urllib.error

ROOT = Path(__file__).resolve().parent.parent
OUT_DIR = ROOT / "optimized"
RAW_REVIEW = ROOT / "scripts" / "out" / "quality_raw.json"

MODEL = "gemini-3.1-pro-preview"
ENDPOINT = f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL}:generateContent"

# ============================================================
# 目标文件(和 quality_audit.py 保持一致)
# ============================================================
TARGET_DIRS = [
    "01-赛道现状与市场结构",
    "02-产品与玩法前沿",
    "03-技术栈与可行性GAP",
    "04-玩家行为与留存心理",
    "05-跨品类启发",
    "06-机会地图整合",
]
ROOT_FILES = [
    "校验点3-中期简报.md",
    "research-plan.md",
]
EXCLUDE_NAMES = {
    "sources.md", "methodology.md", "glossary.md", "README.md",
    "产品案例库.md", "GAP清单.md", "PROGRESS.md",
}


def collect_targets():
    targets = []
    for fn in ROOT_FILES:
        p = ROOT / fn
        if p.exists():
            targets.append(p)
    for d in TARGET_DIRS:
        dp = ROOT / d
        if not dp.exists():
            continue
        for f in sorted(dp.rglob("*.md")):
            if f.name in EXCLUDE_NAMES:
                continue
            targets.append(f)
    return targets


# ============================================================
# 加载评审结果,按文件查索
# ============================================================
def load_review_map() -> dict:
    if not RAW_REVIEW.exists():
        return {}
    data = json.loads(RAW_REVIEW.read_text(encoding="utf-8"))
    return {r["obj"]["file"]: r for r in data}


# ============================================================
# Prompt 模板 — 这是优化质量的关键
# ============================================================
PROMPT_TEMPLATE = """你是一位顶级中文非虚构编辑,专长是市场研究报告。你的任务是**优化改写**下面这份研究 Markdown 文档,让它:

1. **可读性显著提升** — 句子短、节奏好、主语清晰、避免长定语堆砌、善用小标题和断点
2. **解决评审指出的具体问题**(见下方评审意见)
3. **保留所有事实、数据、品牌名、来源编号、具体案例** — 不允许删除事实性内容
4. **结构更清晰** — 如果缺少五节结构(Facts / Summary / Insights / Sources / Gaps)就补上,如果有就优化
5. **为估算数据加 `[估算]` 标记**,和权威数据明显区分
6. **加强锋利度** — insight 要提出"反共识"判断、明确"强判断 vs 推测"

**原则**(极其重要):
- **宁可不动也不要改错** — 如果不确定某句话的原意,保留原句
- **不要引入新的事实** — 你不能编造任何 Gemini 自己"以为"的数据或品牌
- **保留所有 Markdown 结构**:标题层级、表格、代码块、引用块、图片、链接
- **保留所有来源编号**:`[S-XX-XX]` 等格式
- **中文标点全用全角**:,。:;?!()
- **不要加入你自己的 meta 评论**,只返回优化后的 md 正文

---

**文件路径**:{path}

**评审意见**(来自 Gemini 2.5 Flash 的前一轮评审):
- 综合评分:{overall}/10 · 可读性 {readability}/10 · 证据强度 {evidence}/10 · 锋利度 {sharpness}/10
- 评审一句话:{verdict}
- 主要改进建议:
{issues}
- 缺失事实(不要编造,只是提醒你 insight 要避开这些空缺):
{missing}

---

**原文**:

```markdown
{content}
```

---

现在请输出**完整的优化后 Markdown 正文**。不要有任何前言、不要用代码围栏包裹、不要加"以下是优化版本"之类的元文字。**直接从第一个 `#` 标题开始输出完整的优化版 md**。

在输出完整 md 后,**加一行分隔符**:

```
<!--OPTIMIZATION_NOTES-->
```

然后用 ≤ 200 字中文说明你做了什么改动(可读性提升点 / 结构调整 / 加了什么标记 / 如何解决评审问题),给主 agent 参考。"""


def build_prompt(path: Path, content: str, review: dict) -> str:
    rv = (review or {}).get("review") or {}
    overall = rv.get("overall", "?")
    readability = rv.get("readability", "?")
    evidence = rv.get("evidence", "?")
    sharpness = rv.get("sharpness", "?")
    verdict = rv.get("one_line_verdict", "无")
    issues = "\n".join(f"  - {x}" for x in rv.get("top_issues", [])) or "  - (无)"
    missing = "\n".join(f"  - {x}" for x in rv.get("missing_facts", [])) or "  - (无)"

    return PROMPT_TEMPLATE.format(
        path=str(path.relative_to(ROOT)),
        overall=overall,
        readability=readability,
        evidence=evidence,
        sharpness=sharpness,
        verdict=verdict,
        issues=issues,
        missing=missing,
        content=content,
    )


# ============================================================
# Gemini 调用
# ============================================================
def call_gemini(prompt: str, api_key: str, max_retries: int = 3) -> dict:
    body = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {
            "maxOutputTokens": 32000,
            "temperature": 0.4,
        },
    }

    url = f"{ENDPOINT}?key={api_key}"
    data = json.dumps(body).encode("utf-8")

    last_err = None
    for attempt in range(max_retries):
        try:
            req = urllib.request.Request(
                url, data=data,
                headers={"Content-Type": "application/json"},
            )
            with urllib.request.urlopen(req, timeout=300) as resp:
                raw = resp.read().decode("utf-8")
            result = json.loads(raw)

            if "error" in result:
                return {"ok": False, "error": result["error"].get("message", "unknown")}

            if "candidates" not in result or not result["candidates"]:
                return {"ok": False, "error": "no candidates"}

            cand = result["candidates"][0]
            finish = cand.get("finishReason", "?")

            # 3.1 Pro 可能返回 content.parts,也可能 thinking 之后只有 content 没有 parts
            text = ""
            if "content" in cand and "parts" in cand["content"]:
                for p in cand["content"]["parts"]:
                    if "text" in p:
                        text += p["text"]

            if not text:
                return {
                    "ok": False,
                    "error": f"empty text (finishReason={finish})",
                    "usage": result.get("usageMetadata", {}),
                }

            return {
                "ok": True,
                "text": text,
                "finishReason": finish,
                "usage": result.get("usageMetadata", {}),
            }

        except urllib.error.HTTPError as e:
            body_txt = e.read().decode("utf-8", errors="ignore")[:500] if hasattr(e, 'read') else ''
            last_err = f"HTTP {e.code}: {e.reason} | {body_txt[:200]}"
            if e.code in (429, 503) and attempt < max_retries - 1:
                time.sleep(10 * (attempt + 1))
                continue
            return {"ok": False, "error": last_err}
        except Exception as e:
            last_err = f"{type(e).__name__}: {e}"
            if attempt < max_retries - 1:
                time.sleep(3)
                continue
            return {"ok": False, "error": last_err}

    return {"ok": False, "error": last_err or "max retries"}


# ============================================================
# 拆分 md 和 notes
# ============================================================
def split_md_and_notes(text: str) -> tuple[str, str]:
    marker = "<!--OPTIMIZATION_NOTES-->"
    if marker in text:
        md, notes = text.split(marker, 1)
        return md.strip(), notes.strip()
    return text.strip(), ""


# ============================================================
# Main
# ============================================================
def main():
    args = sys.argv[1:]
    dry_run = "--dry-run" in args
    only = None
    if "--only" in args:
        i = args.index("--only")
        only = args[i + 1]

    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("ERROR: GEMINI_API_KEY 环境变量未设置")
        sys.exit(1)

    review_map = load_review_map()
    if not review_map:
        print("WARNING: scripts/out/quality_raw.json 不存在,优化将不带评审意见")

    targets = collect_targets()
    if only:
        targets = [t for t in targets if only in str(t)]

    OUT_DIR.mkdir(parents=True, exist_ok=True)

    print("=" * 60)
    print(f"  Gemini 3.1 Pro Preview 批量优化")
    print("=" * 60)
    print(f"  目标文件:{len(targets)}")
    print(f"  输出目录:{OUT_DIR}")
    print(f"  模型:    {MODEL}")
    if dry_run:
        print(f"  模式:    DRY RUN(不写盘)")
    print()

    audit_records = []
    total_in_tokens = 0
    total_out_tokens = 0
    total_thinking = 0
    success = 0
    failed = 0

    for i, path in enumerate(targets, 1):
        rel = path.relative_to(ROOT)
        out_path = OUT_DIR / rel
        out_path.parent.mkdir(parents=True, exist_ok=True)

        content = path.read_text(encoding="utf-8")
        review = review_map.get(str(rel))

        orig_len = len(content)
        print(f"[{i:2d}/{len(targets)}] {rel}")
        print(f"       原文 {orig_len:,} 字符")

        if dry_run:
            print("       (dry-run 跳过)")
            continue

        prompt = build_prompt(path, content, review)
        t0 = time.time()
        result = call_gemini(prompt, api_key)
        dt = time.time() - t0

        if not result.get("ok"):
            print(f"       ❌ 失败 {dt:.1f}s: {result.get('error')}")
            failed += 1
            audit_records.append({
                "file": str(rel),
                "status": "failed",
                "error": result.get("error"),
            })
            time.sleep(3)
            continue

        text = result["text"]
        finish = result.get("finishReason")
        usage = result.get("usage", {})
        in_t = usage.get("promptTokenCount", 0)
        out_t = usage.get("candidatesTokenCount", 0)
        think_t = usage.get("thoughtsTokenCount", 0)
        total_in_tokens += in_t
        total_out_tokens += out_t
        total_thinking += think_t

        md_body, notes = split_md_and_notes(text)

        # 写优化版
        out_path.write_text(md_body + "\n", encoding="utf-8")

        opt_len = len(md_body)
        delta = opt_len - orig_len
        delta_pct = (delta / orig_len * 100) if orig_len else 0

        status = "✅" if finish == "STOP" else f"⚠️ {finish}"
        print(f"       {status} {dt:.1f}s · 原 {orig_len:,} → 新 {opt_len:,} ({delta:+,}, {delta_pct:+.0f}%)")
        print(f"       tokens: in {in_t:,} / out {out_t:,} / thinking {think_t:,}")
        if notes:
            short_notes = notes[:80].replace("\n", " ")
            print(f"       notes: {short_notes}…")

        success += 1
        audit_records.append({
            "file": str(rel),
            "status": "ok",
            "orig_len": orig_len,
            "opt_len": opt_len,
            "delta_pct": round(delta_pct, 1),
            "finish": finish,
            "in_tokens": in_t,
            "out_tokens": out_t,
            "thinking_tokens": think_t,
            "notes": notes,
            "review_overall": (review or {}).get("review", {}).get("overall") if review else None,
        })

        # Rate limit 友好
        time.sleep(2.5)

    # ========== 写 _audit.md ==========
    audit_md = ["# 优化审计报告", "",
                f"> 模型:{MODEL}",
                f"> 生成时间:2026-04-13",
                f"> 成功:{success} · 失败:{failed} · 总计:{len(targets)}",
                f"> Token 消耗:输入 {total_in_tokens:,} · 输出 {total_out_tokens:,} · 思考 {total_thinking:,}",
                "", "---", ""]

    for rec in audit_records:
        audit_md.append(f"## `{rec['file']}`")
        audit_md.append("")
        if rec["status"] == "failed":
            audit_md.append(f"❌ **失败**:{rec.get('error', '')}")
            audit_md.append("")
            audit_md.append("---")
            audit_md.append("")
            continue

        audit_md.append(f"- **状态**:{rec['finish']}")
        audit_md.append(f"- **字符数**:{rec['orig_len']:,} → {rec['opt_len']:,} ({rec['delta_pct']:+.1f}%)")
        audit_md.append(f"- **Token**:in {rec['in_tokens']:,} / out {rec['out_tokens']:,} / thinking {rec['thinking_tokens']:,}")
        if rec.get("review_overall") is not None:
            audit_md.append(f"- **优化前评分**:{rec['review_overall']}/10")
        audit_md.append("")
        if rec.get("notes"):
            audit_md.append("**Gemini 改动说明**:")
            audit_md.append("")
            audit_md.append(rec["notes"])
            audit_md.append("")
        audit_md.append("---")
        audit_md.append("")

    (OUT_DIR / "_audit.md").write_text("\n".join(audit_md), encoding="utf-8")

    # ========== 写 _summary.md ==========
    ok_records = [r for r in audit_records if r["status"] == "ok"]
    summary = [
        "# 优化总结", "",
        f"> 模型:{MODEL}",
        f"> 完成:{success}/{len(targets)}",
        f"> 失败:{failed}",
        "",
        "## Token 消耗",
        "",
        f"- 输入:{total_in_tokens:,}",
        f"- 输出:{total_out_tokens:,}",
        f"- 思考:{total_thinking:,}",
        f"- **总计**:{total_in_tokens + total_out_tokens + total_thinking:,}",
        "",
        "## 字符数变化统计", "",
    ]
    if ok_records:
        deltas = [r["delta_pct"] for r in ok_records]
        summary.append(f"- 平均变化:**{sum(deltas)/len(deltas):+.1f}%**")
        summary.append(f"- 最大增长:{max(deltas):+.1f}%")
        summary.append(f"- 最大缩减:{min(deltas):+.1f}%")
    summary.append("")
    summary.append("## 每个文件的优化幅度")
    summary.append("")
    summary.append("| 文件 | 原字符 | 新字符 | 变化 | 优化前评分 |")
    summary.append("|------|------|------|------|------|")
    for r in sorted(ok_records, key=lambda x: x["file"]):
        score = r.get("review_overall", "-")
        summary.append(f"| `{r['file']}` | {r['orig_len']:,} | {r['opt_len']:,} | {r['delta_pct']:+.1f}% | {score} |")
    summary.append("")

    (OUT_DIR / "_summary.md").write_text("\n".join(summary), encoding="utf-8")

    print()
    print("=" * 60)
    print(f"  完成")
    print(f"=" * 60)
    print(f"  成功:{success}")
    print(f"  失败:{failed}")
    print(f"  Token 总计:输入 {total_in_tokens:,} + 输出 {total_out_tokens:,} + 思考 {total_thinking:,}")
    print(f"  审计报告:{OUT_DIR / '_audit.md'}")
    print(f"  总结:  {OUT_DIR / '_summary.md'}")


if __name__ == "__main__":
    main()
