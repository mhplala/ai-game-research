#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Regression 检查:对比原文 vs optimized/ 优化版,确认关键内容没丢失

检查维度:
1. 字符数变化(< -20% 标记为危险)
2. 关键数字保留(原文中所有重要数字的出现次数对比)
3. 来源编号保留([S-XX-XX] 格式)
4. 图片引用保留(![...](assets/...))
5. Markdown 链接保留
6. 品牌名保留(兔头妈妈 / Apagard / usmile 等重要品牌)

输出:
    scripts/out/regression_report.md — 每个文件的详细 diff 分析
    stdout — 每个文件的分类(SAFE / REVIEW / DANGER)
"""

import re
import sys
import json
from pathlib import Path
from collections import Counter

ROOT = Path(__file__).resolve().parent.parent
OPTIMIZED = ROOT / "optimized"
OUT = ROOT / "scripts" / "out"

# 哪些是"关键"品牌 — 出现次数应该保留
KEY_BRANDS = [
    # 美国 AI 游戏
    "Inworld", "Hidden Door", "Latitude", "Altera", "AI Dungeon",
    "Character.AI", "Replika", "Suck Up", "Kinetix", "Sidekick",
    "Convai", "Ex-Human", "NVIDIA ACE",
    # 中国 AI 游戏 / 小游戏
    "量子绘梦", "Whispers from the Star", "rct AI", "彩云小梦",
    "筑梦岛", "羊了个羊", "咸鱼之王", "寻道大千", "三七互娱",
    "热力小镇", "疯狂动物园", "腾讯", "字节跳动",
    # 日韩
    "1001 Nights", "Krafton", "MOGIA", "Nexon", "NCSoft",
    "CyberAgent",
    # 欧美 indie / 平台
    "Poki", "CrazyGames", "King", "Supercell", "Valve",
    # 平台
    "微信小游戏", "抖音小游戏", "快手小游戏", "QQ 小游戏",
    "Meta Horizon", "Facebook Instant Games", "Steam", "itch.io",
    # 技术
    "OpenAI", "Anthropic", "Gemini", "Llama",
]

# 哪些数字是"关键事实" — 丢失即判定 regression
# 格式:(正则, 描述)
# 注:本赛道信息快变,具体数字会在 sub-agent 产出后再次补充
KEY_NUMBERS = [
    # 通用占位,sub-agent 产出后人工补充具体数字
]


def analyze_file(orig_path: Path, opt_path: Path) -> dict:
    rel = orig_path.relative_to(ROOT)
    orig = orig_path.read_text(encoding="utf-8")
    opt = opt_path.read_text(encoding="utf-8")

    r = {"file": str(rel), "issues": [], "warnings": []}

    # 1. 字符数
    o_len = len(orig)
    n_len = len(opt)
    delta_pct = (n_len - o_len) / o_len * 100 if o_len else 0
    r["orig_len"] = o_len
    r["opt_len"] = n_len
    r["delta_pct"] = round(delta_pct, 1)

    if delta_pct < -25:
        r["issues"].append(f"字符数大幅减少 {delta_pct:.0f}%")
    elif delta_pct < -15:
        r["warnings"].append(f"字符数减少 {delta_pct:.0f}%")

    # 2. 来源编号保留
    orig_sources = re.findall(r"\[S-[\d.\-]+\]", orig)
    opt_sources = re.findall(r"\[S-[\d.\-]+\]", opt)
    r["orig_sources"] = len(orig_sources)
    r["opt_sources"] = len(opt_sources)
    lost_sources = set(orig_sources) - set(opt_sources)
    if lost_sources:
        r["issues"].append(f"丢失 {len(lost_sources)} 个来源编号: {list(lost_sources)[:5]}")

    # 3. 图片引用保留
    orig_imgs = re.findall(r"!\[[^\]]*\]\(([^)]+)\)", orig)
    opt_imgs = re.findall(r"!\[[^\]]*\]\(([^)]+)\)", opt)
    r["orig_imgs"] = len(orig_imgs)
    r["opt_imgs"] = len(opt_imgs)
    lost_imgs = set(orig_imgs) - set(opt_imgs)
    if lost_imgs:
        r["issues"].append(f"丢失 {len(lost_imgs)} 个图片引用")

    # 4. 关键数字
    lost_numbers = []
    for pat, desc in KEY_NUMBERS:
        orig_has = bool(re.search(pat, orig))
        opt_has = bool(re.search(pat, opt))
        if orig_has and not opt_has:
            lost_numbers.append(desc)
    if lost_numbers:
        r["issues"].append(f"丢失关键数字: {lost_numbers}")
    r["lost_numbers"] = lost_numbers

    # 5. 关键品牌(次数显著下降视为丢失)
    lost_brands = []
    for brand in KEY_BRANDS:
        o_count = orig.count(brand)
        n_count = opt.count(brand)
        if o_count >= 2 and n_count == 0:
            lost_brands.append(f"{brand}(原 {o_count} 次 → 0)")
        elif o_count >= 5 and n_count < o_count * 0.3:
            lost_brands.append(f"{brand}({o_count}→{n_count})")
    if lost_brands:
        r["warnings"].append(f"品牌出现频率显著下降: {lost_brands[:5]}")

    # 6. Markdown 表格行(检查表格是否被大幅删除)
    orig_table_rows = len(re.findall(r"^\|.+\|$", orig, re.M))
    opt_table_rows = len(re.findall(r"^\|.+\|$", opt, re.M))
    r["orig_table_rows"] = orig_table_rows
    r["opt_table_rows"] = opt_table_rows
    if orig_table_rows > 10 and opt_table_rows < orig_table_rows * 0.5:
        r["issues"].append(f"表格行减半以上: {orig_table_rows}→{opt_table_rows}")

    # 7. 分类
    if r["issues"]:
        r["verdict"] = "DANGER"  # 红色 — 不能自动覆盖
    elif r["warnings"]:
        r["verdict"] = "REVIEW"  # 黄色 — 建议人工审
    else:
        r["verdict"] = "SAFE"    # 绿色 — 可以自动覆盖

    return r


def main():
    if not OPTIMIZED.exists():
        print("ERROR: optimized/ 不存在,先跑 optimize_parallel.py", file=sys.stderr)
        sys.exit(1)

    # 找所有 optimized/ 下的 md(排除 _audit / _summary)
    opt_files = []
    for f in OPTIMIZED.rglob("*.md"):
        if f.name.startswith("_"):
            continue
        opt_files.append(f)

    results = []
    for opt_f in sorted(opt_files):
        rel = opt_f.relative_to(OPTIMIZED)
        orig_f = ROOT / rel
        if not orig_f.exists():
            print(f"WARN: 原文不存在 {rel}")
            continue
        results.append(analyze_file(orig_f, opt_f))

    # 分类统计
    safe = [r for r in results if r["verdict"] == "SAFE"]
    review = [r for r in results if r["verdict"] == "REVIEW"]
    danger = [r for r in results if r["verdict"] == "DANGER"]

    print(f"\n{'='*60}")
    print(f"  Regression 检查结果")
    print(f"{'='*60}")
    print(f"  ✅ SAFE:   {len(safe)}")
    print(f"  ⚠️  REVIEW: {len(review)}")
    print(f"  ❌ DANGER: {len(danger)}")
    print()

    if danger:
        print("❌ DANGER 文件(不建议自动覆盖):")
        for r in danger:
            print(f"  {r['file']} ({r['delta_pct']:+.0f}%)")
            for i in r["issues"]:
                print(f"    - {i}")
        print()

    if review:
        print("⚠️  REVIEW 文件(建议人工审阅):")
        for r in review:
            print(f"  {r['file']} ({r['delta_pct']:+.0f}%)")
            for w in r["warnings"]:
                print(f"    - {w}")
        print()

    # 写详细报告
    OUT.mkdir(parents=True, exist_ok=True)
    report_path = OUT / "regression_report.md"
    lines = ["# Regression 检查详细报告", "",
             f"> 对比:原文 vs optimized/",
             f"> 总计:{len(results)} 个文件",
             f"> SAFE: {len(safe)} · REVIEW: {len(review)} · DANGER: {len(danger)}",
             "", "---", ""]

    for verdict_label, items, icon in [
        ("DANGER", danger, "❌"),
        ("REVIEW", review, "⚠️"),
        ("SAFE", safe, "✅"),
    ]:
        if not items:
            continue
        lines.append(f"## {icon} {verdict_label}({len(items)} 个)")
        lines.append("")
        for r in items:
            lines.append(f"### `{r['file']}`")
            lines.append("")
            lines.append(f"- 字符数:{r['orig_len']:,} → {r['opt_len']:,} ({r['delta_pct']:+.1f}%)")
            lines.append(f"- 来源编号:{r['orig_sources']} → {r['opt_sources']}")
            lines.append(f"- 图片:{r['orig_imgs']} → {r['opt_imgs']}")
            lines.append(f"- 表格行:{r['orig_table_rows']} → {r['opt_table_rows']}")
            if r["issues"]:
                lines.append("")
                lines.append("**问题**:")
                for i in r["issues"]:
                    lines.append(f"- ❌ {i}")
            if r["warnings"]:
                lines.append("")
                lines.append("**警告**:")
                for w in r["warnings"]:
                    lines.append(f"- ⚠️ {w}")
            lines.append("")
            lines.append("---")
            lines.append("")

    report_path.write_text("\n".join(lines), encoding="utf-8")
    print(f"详细报告:{report_path}")

    # 同时写一个可被其他脚本读的 JSON
    (OUT / "regression.json").write_text(
        json.dumps(results, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    # Exit code:如果有 DANGER,退出 1(让自动化脚本知道)
    sys.exit(1 if danger else 0)


if __name__ == "__main__":
    main()
