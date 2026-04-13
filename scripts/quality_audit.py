#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
研究质量批量审查脚本

对所有主要研究 md 做两类评估:
1. **客观指标**(本地计算):字数 / 句数 / 句长 / 引用密度 / 结构完整度 / 标点健康度
2. **主观评审**(Gemini 2.5 Flash):可读性 / 清晰度 / 证据强度 / 锋利度 / 改进建议

输出:
    质量评审报告.md — 一份综合 Markdown 报告,包含每个文件的评分 + 全局 Top 10 问题
    scripts/out/quality_raw.json — 原始数据(可后续分析)

用法:
    export GEMINI_API_KEY=xxx
    python3 scripts/quality_audit.py [--no-gemini] [--limit N]
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
OUT_DIR = ROOT / "scripts" / "out"
OUT_DIR.mkdir(parents=True, exist_ok=True)

# ============================================================
# 目标文件
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

# 排除:来源清单、产品案例库(表格)、README、附录等非"正文研究"
EXCLUDE_NAMES = {
    "sources.md",
    "methodology.md",
    "glossary.md",
    "README.md",
    "产品案例库.md",
    "GAP清单.md",
    "PROGRESS.md",
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
# 1. 客观指标
# ============================================================

def strip_md(text: str) -> str:
    """去掉代码块、URL、图片、链接,只留纯文字"""
    text = re.sub(r"```.*?```", " ", text, flags=re.S)
    text = re.sub(r"`[^`\n]*`", " ", text)
    text = re.sub(r"https?://[^\s\)]+", "", text)
    text = re.sub(r"!\[.*?\]\([^)]*\)", " ", text)
    text = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", text)
    text = re.sub(r"<!--.*?-->", " ", text, flags=re.S)
    return text


def objective_metrics(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")
    plain = strip_md(text)

    # 字数(中文字符 + 英文单词近似)
    cjk_chars = len(re.findall(r"[\u4e00-\u9fff]", plain))
    ascii_words = len(re.findall(r"[a-zA-Z]+", plain))
    word_count = cjk_chars + ascii_words

    # 句数(用全角句号 + 问号 + 叹号切分)
    sentences = re.split(r"[。!?\n]", plain)
    sentences = [s.strip() for s in sentences if len(s.strip()) > 3]
    sent_count = len(sentences) or 1
    avg_sent_len = sum(len(s) for s in sentences) / sent_count

    # 段落数(md 层面)
    paragraphs = [p for p in text.split("\n\n") if p.strip()]
    para_count = len(paragraphs)

    # 标题数
    h1 = len(re.findall(r"^# ", text, re.M))
    h2 = len(re.findall(r"^## ", text, re.M))
    h3 = len(re.findall(r"^### ", text, re.M))
    h4 = len(re.findall(r"^#### ", text, re.M))

    # 引用密度(每 1000 字的 [S-XX-XX] 来源编号数)
    citations = len(re.findall(r"\[S-[\d.\-]+\]", text))
    citation_density = (citations / word_count * 1000) if word_count else 0

    # 表格数量
    tables = len(re.findall(r"^\|.+\|$", text, re.M)) // 5  # 近似:一个表 5 行

    # 列表项
    list_items = len(re.findall(r"^[\*\-]\s", text, re.M))

    # 粗体强调(说明性文字密度)
    bold_count = len(re.findall(r"\*\*[^*]+\*\*", text))

    # 结构完整度(是否五节齐全)
    has_facts = bool(re.search(r"#+\s*.*?(信息|Facts|事实)", text))
    has_summary = bool(re.search(r"#+\s*.*?(总结|Summary)", text))
    has_insights = bool(re.search(r"#+\s*.*?(洞察|Insights)", text))
    has_sources = bool(re.search(r"#+\s*.*?(来源|Sources)", text)) or citations > 0
    has_gaps = bool(re.search(r"#+\s*.*?(Gaps?|待核实|gap|缺失)", text, re.I))
    five_sections = sum([has_facts, has_summary, has_insights, has_sources, has_gaps])

    # 半角标点残留(规范化后应该为 0)
    cjk_ctx = r"[\u4e00-\u9fff\u3000-\u303f\uff00-\uffef\u2018-\u201f]"
    half_comma = len(re.findall(cjk_ctx + r"," + cjk_ctx, text))
    half_lparen = len(re.findall(cjk_ctx + r"\(", text))
    half_rparen = len(re.findall(r"\)" + cjk_ctx, text))
    half_colon = len(re.findall(cjk_ctx + r":" + cjk_ctx, text))
    half_total = half_comma + half_lparen + half_rparen + half_colon

    return {
        "file": str(path.relative_to(ROOT)),
        "name": path.stem,
        "bytes": path.stat().st_size,
        "word_count": word_count,
        "cjk_chars": cjk_chars,
        "ascii_words": ascii_words,
        "sent_count": sent_count,
        "avg_sent_len": round(avg_sent_len, 1),
        "para_count": para_count,
        "h1": h1, "h2": h2, "h3": h3, "h4": h4,
        "citations": citations,
        "citation_density": round(citation_density, 2),
        "tables": tables,
        "list_items": list_items,
        "bold_count": bold_count,
        "five_sections": five_sections,
        "has_facts": has_facts,
        "has_summary": has_summary,
        "has_insights": has_insights,
        "has_sources": has_sources,
        "has_gaps": has_gaps,
        "half_punct_residue": half_total,
    }


# ============================================================
# 2. Gemini 主观评审
# ============================================================

GEMINI_ENDPOINT = (
    "https://generativelanguage.googleapis.com/v1beta/models/"
    "gemini-2.5-flash:generateContent"
)

PROMPT_TEMPLATE = """你是一位资深的中文非虚构编辑,专长是市场研究报告和商业策略报告。

请对以下 Markdown 研究文档做一次严格但建设性的质量评审。

---
文件路径:{path}
文件内容:

{content}

---

请用**严格 JSON** 格式回答(不要加 markdown 代码围栏,不要任何解释文字,只返回一个 JSON 对象),字段如下:

{{
  "overall": 整数 0-10,
  "readability": 整数 0-10(中文流畅度、句式节奏、段落节奏),
  "clarity": 整数 0-10(论点是否清晰、结构是否清晰),
  "evidence": 整数 0-10(事实密度、数字具体性、来源质量),
  "sharpness": 整数 0-10(洞察的原创性与锋利度,是否提出了"反共识"判断),
  "actionability": 整数 0-10(对品牌决策的可执行性),
  "top_strengths": [最多 3 条,每条 ≤ 30 字],
  "top_issues": [最多 3 条,每条 ≤ 40 字,必须可执行的改进建议],
  "missing_facts": [最多 3 条,文章显然缺失但应该有的具体事实/数据/案例],
  "one_line_verdict": "≤ 50 字的整体判断"
}}

评分参考:6 及格、7 良好、8 优秀、9 专业编辑水准、10 行业标杆。
请尽量严格,不要给所有文件打高分。"""


def call_gemini(path: Path, content: str, api_key: str, max_retries: int = 2) -> dict:
    # 截断过长内容(Gemini 2.5 Flash 上下文 1M,单文件不太可能超,但保留保险)
    if len(content) > 80000:
        content = content[:80000] + "\n\n[内容已截断,仅评审前 80000 字符]"

    prompt = PROMPT_TEMPLATE.format(
        path=str(path.relative_to(ROOT)),
        content=content,
    )

    body = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {
            "maxOutputTokens": 1500,
            "temperature": 0.3,
            "thinkingConfig": {"thinkingBudget": 0},
            "responseMimeType": "application/json",
        },
    }

    url = f"{GEMINI_ENDPOINT}?key={api_key}"
    data = json.dumps(body).encode("utf-8")

    for attempt in range(max_retries):
        try:
            req = urllib.request.Request(
                url,
                data=data,
                headers={"Content-Type": "application/json"},
            )
            with urllib.request.urlopen(req, timeout=90) as resp:
                raw = resp.read().decode("utf-8")
            result = json.loads(raw)

            if "candidates" not in result:
                return {"error": "no candidates", "raw": str(result)[:500]}

            text = result["candidates"][0]["content"]["parts"][0]["text"]
            # 清理 markdown 围栏(如果模型没听话)
            text = re.sub(r"^```(?:json)?\n", "", text)
            text = re.sub(r"\n```$", "", text)
            text = text.strip()

            try:
                review = json.loads(text)
                # 加上 usage
                if "usageMetadata" in result:
                    review["_usage"] = result["usageMetadata"]
                return review
            except json.JSONDecodeError as e:
                return {"error": f"json parse: {e}", "raw_text": text[:500]}

        except urllib.error.HTTPError as e:
            if e.code == 429 and attempt < max_retries - 1:
                time.sleep(5 * (attempt + 1))
                continue
            return {"error": f"HTTP {e.code}: {e.reason}"}
        except Exception as e:
            if attempt < max_retries - 1:
                time.sleep(2)
                continue
            return {"error": f"{type(e).__name__}: {e}"}

    return {"error": "max retries exceeded"}


# ============================================================
# 3. 汇总报告
# ============================================================

def render_report(records: list) -> str:
    """根据每个文件的 (objective, review) 合成 Markdown 报告"""

    # 全局统计
    total_files = len(records)
    total_words = sum(r["obj"]["word_count"] for r in records)
    total_citations = sum(r["obj"]["citations"] for r in records)
    total_residue = sum(r["obj"]["half_punct_residue"] for r in records)

    # Gemini 评分可用的文件
    scored = [r for r in records if "overall" in (r.get("review") or {})]
    if scored:
        avg_overall = sum(r["review"]["overall"] for r in scored) / len(scored)
        avg_read = sum(r["review"]["readability"] for r in scored) / len(scored)
        avg_clarity = sum(r["review"]["clarity"] for r in scored) / len(scored)
        avg_evidence = sum(r["review"]["evidence"] for r in scored) / len(scored)
        avg_sharpness = sum(r["review"]["sharpness"] for r in scored) / len(scored)
        avg_action = sum(r["review"]["actionability"] for r in scored) / len(scored)
    else:
        avg_overall = avg_read = avg_clarity = avg_evidence = avg_sharpness = avg_action = 0

    lines = []
    lines.append("# 研究质量评审报告")
    lines.append("")
    lines.append(f"> 生成时间:2026-04-13 · 工具:Gemini 2.5 Flash + 本地客观指标")
    lines.append(f"> 覆盖文件:**{total_files}** 个研究正文 md")
    lines.append("")
    lines.append("---")
    lines.append("")

    # ========== 全局概览 ==========
    lines.append("## 0. 全局概览")
    lines.append("")
    lines.append(f"- **总字数**:{total_words:,}")
    lines.append(f"- **总引用数**:{total_citations}(平均 {total_citations/total_files:.1f} 条/文件)")
    lines.append(f"- **半角标点残留**:{total_residue} 处(规范化后应为 0,实际值反映 edge case)")
    if scored:
        lines.append("")
        lines.append("### Gemini 评分(0-10)")
        lines.append("")
        lines.append(f"| 维度 | 平均分 |")
        lines.append(f"|------|------|")
        lines.append(f"| **综合 Overall** | **{avg_overall:.1f}** |")
        lines.append(f"| 可读性 Readability | {avg_read:.1f} |")
        lines.append(f"| 清晰度 Clarity | {avg_clarity:.1f} |")
        lines.append(f"| 证据强度 Evidence | {avg_evidence:.1f} |")
        lines.append(f"| 锋利度 Sharpness | {avg_sharpness:.1f} |")
        lines.append(f"| 可执行性 Actionability | {avg_action:.1f} |")
    lines.append("")
    lines.append("---")
    lines.append("")

    # ========== Top 5 / Bottom 5 ==========
    if scored:
        sorted_by_overall = sorted(scored, key=lambda r: -r["review"]["overall"])
        lines.append("## 1. Top 5 最高分文件")
        lines.append("")
        lines.append("| 排名 | 文件 | 综合 | 锋利度 | 一句话评价 |")
        lines.append("|------|------|------|------|------|")
        for i, r in enumerate(sorted_by_overall[:5], 1):
            name = r["obj"]["file"]
            o = r["review"]["overall"]
            s = r["review"]["sharpness"]
            v = r["review"].get("one_line_verdict", "")[:60]
            lines.append(f"| {i} | `{name}` | **{o}** | {s} | {v} |")
        lines.append("")

        lines.append("## 2. Bottom 5 最需改进")
        lines.append("")
        lines.append("| 排名 | 文件 | 综合 | 一句话评价 |")
        lines.append("|------|------|------|------|")
        for i, r in enumerate(sorted_by_overall[-5:], 1):
            name = r["obj"]["file"]
            o = r["review"]["overall"]
            v = r["review"].get("one_line_verdict", "")[:60]
            lines.append(f"| {i} | `{name}` | **{o}** | {v} |")
        lines.append("")
        lines.append("---")
        lines.append("")

    # ========== 逐文件详情 ==========
    lines.append("## 3. 逐文件详情")
    lines.append("")
    for r in sorted(records, key=lambda x: x["obj"]["file"]):
        o = r["obj"]
        rev = r.get("review") or {}
        lines.append(f"### `{o['file']}`")
        lines.append("")
        lines.append(f"**客观指标**:字数 {o['word_count']:,} · "
                     f"句数 {o['sent_count']} · 平均句长 {o['avg_sent_len']} · "
                     f"引用 {o['citations']} 条(密度 {o['citation_density']}/千字) · "
                     f"五节结构 {o['five_sections']}/5 · "
                     f"半角残留 {o['half_punct_residue']}")
        lines.append("")
        if "error" in rev:
            lines.append(f"**Gemini 评审**:❌ {rev['error']}")
        elif "overall" in rev:
            lines.append(
                f"**Gemini 评分**:综合 **{rev['overall']}** · "
                f"可读 {rev.get('readability','?')} · 清晰 {rev.get('clarity','?')} · "
                f"证据 {rev.get('evidence','?')} · 锋利 {rev.get('sharpness','?')} · "
                f"可执行 {rev.get('actionability','?')}"
            )
            if rev.get("one_line_verdict"):
                lines.append(f"> *{rev['one_line_verdict']}*")
            if rev.get("top_strengths"):
                lines.append("")
                lines.append("**优点**:")
                for s in rev["top_strengths"]:
                    lines.append(f"- ✅ {s}")
            if rev.get("top_issues"):
                lines.append("")
                lines.append("**改进**:")
                for s in rev["top_issues"]:
                    lines.append(f"- ⚠️ {s}")
            if rev.get("missing_facts"):
                lines.append("")
                lines.append("**缺失事实**:")
                for s in rev["missing_facts"]:
                    lines.append(f"- ❓ {s}")
        lines.append("")
        lines.append("---")
        lines.append("")

    return "\n".join(lines)


# ============================================================
# Main
# ============================================================

def main():
    args = sys.argv[1:]
    no_gemini = "--no-gemini" in args
    limit = None
    if "--limit" in args:
        i = args.index("--limit")
        limit = int(args[i + 1])

    api_key = os.environ.get("GEMINI_API_KEY")
    if not no_gemini and not api_key:
        print("ERROR: GEMINI_API_KEY 环境变量未设置。用 --no-gemini 跳过主观评审。")
        sys.exit(1)

    targets = collect_targets()
    if limit:
        targets = targets[:limit]

    print(f"{'='*60}")
    print(f"  研究质量批量评审")
    print(f"{'='*60}")
    print(f"  目标文件:{len(targets)}")
    print(f"  Gemini:  {'关闭' if no_gemini else 'gemini-2.5-flash'}")
    print()

    records = []
    for i, path in enumerate(targets, 1):
        print(f"[{i:2d}/{len(targets)}] {path.relative_to(ROOT)}")

        # 客观
        obj = objective_metrics(path)
        print(f"    客观:字 {obj['word_count']:,} / 句 {obj['sent_count']} / 引用 {obj['citations']} / 五节 {obj['five_sections']}/5")

        # 主观
        review = None
        if not no_gemini:
            content = path.read_text(encoding="utf-8")
            review = call_gemini(path, content, api_key)
            if "error" in review:
                print(f"    Gemini: ❌ {review['error']}")
            elif "overall" in review:
                print(f"    Gemini: 综合 {review['overall']}/10 · "
                      f"可读 {review.get('readability','?')} · "
                      f"证据 {review.get('evidence','?')} · "
                      f"锋利 {review.get('sharpness','?')}")
            time.sleep(1.2)  # rate limit friendly

        records.append({"obj": obj, "review": review})

    # 写原始 JSON
    raw_file = OUT_DIR / "quality_raw.json"
    raw_file.write_text(
        json.dumps(records, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    print(f"\n原始数据:{raw_file}")

    # 写报告
    report = render_report(records)
    report_file = ROOT / "质量评审报告.md"
    report_file.write_text(report, encoding="utf-8")
    print(f"评审报告:{report_file}")
    print()
    print("✅ 完成")


if __name__ == "__main__":
    main()
