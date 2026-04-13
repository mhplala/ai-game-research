#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Gemini 3.1 Pro Preview 兜底 agent 脚本

用途:当某个 Claude sub-agent 卡住超过 10 分钟零输出时,
立即派 Gemini 3.1 Pro 并行跑同一任务,让两者赛跑,先出的用先出的。

用法:
    export GEMINI_API_KEY=xxx
    python3 scripts/gemini_fallback.py \
        --task 1.1 \
        --brief-file /tmp/task_1.1.txt \
        --output-file "01-赛道现状与市场结构/1.1-赛道定义与边界.md"

或者直接命令行传 brief:
    python3 scripts/gemini_fallback.py \
        --task 1.1 \
        --brief "给一个 AI 小游戏..." \
        --output-file "..."

脚本会:
1. 调 Gemini 3.1 Pro Preview
2. 把产出写到 --output-file.gemini.md (加后缀避免冲突)
3. 主 agent 稍后对比两份产出,选好的覆盖到原文件
"""

import os
import sys
import json
import time
import argparse
import urllib.request
import urllib.error
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

MODEL = "gemini-3.1-pro-preview"
ENDPOINT = f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL}:generateContent"


PROMPT_WRAPPER = """你是一位专业的市场研究员,正在为一个大型跨模块研究项目负责一个具体的子任务。

上游研究方案的关键约定:
- 本项目主题:**AI 如何重塑小游戏与 playable 体验赛道 — 2022-2026 的产品创新、商业机会与玩法前沿**
- 四视角交付:PM/创业者(A)· 投资人(B)· 行业观察(C)· 战略规划(D)
- 地域 Tier 1:中国 + 美国(双中心)· Tier 2:日本 + 韩国 · Tier 3:欧洲 + 东南亚
- 语言:全中文,品牌名 / 专业术语保留原文,中文标点全角
- 五节结构:Facts / Summary / Insights / Sources / Gaps
- 引用格式:`[S-模块编号-序号]`,如 `[S-01.2-05]`
- 禁止事项:禁止编造融资数字 / 公司名 / 游戏名;禁止引用不可访问的 URL

## 你的具体任务

{brief}

---

## 输出要求

1. 直接输出完整的 Markdown 文档,从第一个 `#` 标题开始
2. 严格五节结构:Facts / Summary / Insights / Sources / Gaps
3. Insights 章节必须分 A/B/C/D 四个视角小节
4. Facts 里的每条事实必须带来源编号 `[S-XX-XX]`
5. 中文全角标点(, 。 : ; ? ! ( ))
6. 不要有任何元评论 / 前言,直接进入正文
"""


def call_gemini(prompt: str, api_key: str, max_retries: int = 3) -> dict:
    body = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {
            "maxOutputTokens": 40000,
            "temperature": 0.4,
        },
    }
    url = f"{ENDPOINT}?key={api_key}"
    data = json.dumps(body).encode("utf-8")

    for attempt in range(max_retries):
        try:
            req = urllib.request.Request(
                url, data=data,
                headers={"Content-Type": "application/json"},
            )
            with urllib.request.urlopen(req, timeout=600) as resp:
                raw = resp.read().decode("utf-8")
            result = json.loads(raw)
            if "error" in result:
                return {"ok": False, "error": result["error"].get("message", "?")}
            if "candidates" not in result:
                return {"ok": False, "error": "no candidates"}
            cand = result["candidates"][0]
            text = ""
            if "content" in cand and "parts" in cand["content"]:
                for p in cand["content"]["parts"]:
                    if "text" in p:
                        text += p["text"]
            if not text:
                return {"ok": False, "error": f"empty (finishReason={cand.get('finishReason')})"}
            return {
                "ok": True,
                "text": text,
                "finishReason": cand.get("finishReason"),
                "usage": result.get("usageMetadata", {}),
            }
        except urllib.error.HTTPError as e:
            msg = f"HTTP {e.code} {e.reason}"
            if e.code in (429, 503) and attempt < max_retries - 1:
                time.sleep(10 * (attempt + 1))
                continue
            return {"ok": False, "error": msg}
        except Exception as e:
            if attempt < max_retries - 1:
                time.sleep(5)
                continue
            return {"ok": False, "error": f"{type(e).__name__}: {e}"}

    return {"ok": False, "error": "max retries"}


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--task", required=True, help="任务 ID(如 '1.1')")
    p.add_argument("--brief", help="任务 brief 文本")
    p.add_argument("--brief-file", help="任务 brief 文件路径")
    p.add_argument("--output-file", required=True, help="输出目标 md 文件(会加 .gemini.md 后缀)")
    args = p.parse_args()

    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("ERROR: GEMINI_API_KEY not set", file=sys.stderr)
        sys.exit(1)

    if args.brief_file:
        brief = Path(args.brief_file).read_text(encoding="utf-8")
    elif args.brief:
        brief = args.brief
    else:
        print("ERROR: need --brief or --brief-file", file=sys.stderr)
        sys.exit(1)

    prompt = PROMPT_WRAPPER.format(brief=brief)

    # 输出到 .gemini.md 后缀的文件(避免覆盖 Claude sub-agent 的版本)
    out_base = Path(args.output_file)
    if not out_base.is_absolute():
        out_base = ROOT / out_base
    out_path = out_base.with_suffix(".gemini.md")

    print(f"[gemini-fallback] 任务 {args.task} · 模型 {MODEL}", flush=True)
    print(f"[gemini-fallback] 输出到: {out_path}", flush=True)
    print(f"[gemini-fallback] brief 长度: {len(brief)} 字符", flush=True)

    t0 = time.time()
    result = call_gemini(prompt, api_key)
    dt = time.time() - t0

    if not result["ok"]:
        print(f"[gemini-fallback] ❌ 失败 {dt:.1f}s: {result['error']}", flush=True)
        sys.exit(2)

    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(result["text"], encoding="utf-8")

    usage = result.get("usage", {})
    print(f"[gemini-fallback] ✅ 完成 {dt:.1f}s · finishReason={result.get('finishReason')}", flush=True)
    print(f"[gemini-fallback] tokens: in {usage.get('promptTokenCount',0):,} / out {usage.get('candidatesTokenCount',0):,} / thk {usage.get('thoughtsTokenCount',0):,}", flush=True)
    print(f"[gemini-fallback] 产出: {len(result['text']):,} 字符", flush=True)


if __name__ == "__main__":
    main()
