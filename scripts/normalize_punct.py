#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
中文 Markdown 标点规范化脚本 v2

核心策略:
- 先保护代码块 / 行内代码 / URL / HTML 注释
- 然后把所有 "不跟英文字母/数字相邻的半角标点" 替换成全角
  这样能正确处理中文+全角引号+半角逗号等混合情况
- 保留 "e.g." / "3.14" / "Dr." / "co-op" 等英文语境

用法:
    python3 scripts/normalize_punct.py [--dry-run] [path...]
"""

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# 半角 → 全角 映射(用 Unicode escape 避免字体/编辑器 normalize 陷阱)
PUNCT_MAP = {
    ',': '\uFF0C',   # ,
    '.': '\u3002',   # 。
    ':': '\uFF1A',   # :
    ';': '\uFF1B',   # ;
    '?': '\uFF1F',   # ?
    '!': '\uFF01',   # !
    '(': '\uFF08',   # (
    ')': '\uFF09',   # )
}

# 解包方便后面用
FW_COMMA = '\uFF0C'
FW_PERIOD = '\u3002'
FW_COLON = '\uFF1A'
FW_SEMI = '\uFF1B'
FW_QUEST = '\uFF1F'
FW_EXCL = '\uFF01'
FW_LPAREN = '\uFF08'
FW_RPAREN = '\uFF09'

# 要规范化的目录(研究正文)
TARGET_DIRS = [
    '00-方法论与术语',
    '01-赛道现状与市场结构',
    '02-产品与玩法前沿',
    '03-技术栈与可行性GAP',
    '04-玩家行为与留存心理',
    '05-跨品类启发',
    '06-机会地图整合',
]

TARGET_ROOT_FILES = [
    'research-plan.md',
    '校验点3-中期简报.md',
    'PROGRESS.md',
    'README.md',
]

# 不改的文件(英文 URL / 技术骨架)
SKIP_FILES = {
    'sources.md',
    'methodology.md',
}


def protect(text: str) -> tuple[str, list[str]]:
    """保护代码块 / 行内代码 / URL / HTML 注释,返回占位后文本和片段列表"""
    stash = []

    def store(m):
        stash.append(m.group(0))
        return f'\x00P{len(stash)-1}\x00'

    # 顺序很重要:先大块后小块
    text = re.sub(r'```.*?```', store, text, flags=re.S)
    text = re.sub(r'<!--.*?-->', store, text, flags=re.S)
    text = re.sub(r'`[^`\n]+`', store, text)
    text = re.sub(r'https?://[^\s\)\]\}]+', store, text)
    # 文件路径(不含中文)如 data/1.3.csv
    text = re.sub(r'[a-zA-Z0-9_\-/\.]+\.(csv|xlsx|md|py|sh|html|tsv|json|png|jpg|jpeg|pdf)\b',
                  store, text)
    return text, stash


def restore(text: str, stash: list[str]) -> str:
    return re.sub(r'\x00P(\d+)\x00', lambda m: stash[int(m.group(1))], text)


def normalize_text(text: str) -> tuple[str, int]:
    """核心:把"非英文字母数字相邻的半角标点"替换为全角"""
    text, stash = protect(text)
    count = 0

    # 对每个半角标点:
    # 规则:前或后其中一个"不是 ASCII 字母/数字",就替换
    # 这样能捕获 "中文," "「," "),"  "」,中文" "引文,中文" 等所有场景
    # 但保留 "e.g.," "Dr.Smith" "3.14" "co-op" 这类英文内部

    # 特殊:句号要更严格,避免破坏 "3.14" "v1.0" "Dr."
    # 规则:句号只替换"CJK + . + (CJK|行尾|换行)"的明确中文场景

    CJK = r'[\u4e00-\u9fff\u3000-\u303f\uff00-\uffef]'  # 含中日韩 + 中文标点 + 全角
    # 更宽:凡"中文字/中文标点/全角字符"都算"中文语境"
    CJK_CONTEXT = r'[\u4e00-\u9fff\u3000-\u303f\uff00-\uffef\u2018-\u201f\u2014\u2026]'

    # 1. 中文字符 + 逗号/分号/冒号/问号/叹号 + 非英文数字
    for half, full in [(',', FW_COMMA), (';', FW_SEMI), (':', FW_COLON),
                        ('?', FW_QUEST), ('!', FW_EXCL)]:
        # "中文语境 + 半角" → "中文语境 + 全角"
        pat = f'({CJK_CONTEXT}){re.escape(half)}'
        new_text, n = re.subn(pat, lambda m, f=full: m.group(1) + f, text)
        count += n
        text = new_text
        # 反向:"半角 + 中文语境" → "全角 + 中文语境"
        pat = f'{re.escape(half)}({CJK_CONTEXT})'
        new_text, n = re.subn(pat, lambda m, f=full: f + m.group(1), text)
        count += n
        text = new_text

    # 2. 括号
    # "中文语境 + (" → "中文语境 + ("
    pat = f'({CJK_CONTEXT})\\('
    new_text, n = re.subn(pat, lambda m: m.group(1) + FW_LPAREN, text)
    count += n
    text = new_text
    # "( + 中文语境" → "( + 中文语境"
    pat = f'\\(({CJK_CONTEXT})'
    new_text, n = re.subn(pat, lambda m: FW_LPAREN + m.group(1), text)
    count += n
    text = new_text
    # ") + 中文语境" → ") + 中文语境"
    pat = f'\\)({CJK_CONTEXT})'
    new_text, n = re.subn(pat, lambda m: FW_RPAREN + m.group(1), text)
    count += n
    text = new_text
    # "中文语境 + )" → "中文语境 + )"
    pat = f'({CJK_CONTEXT})\\)'
    new_text, n = re.subn(pat, lambda m: m.group(1) + FW_RPAREN, text)
    count += n
    text = new_text

    # 3. 句号:只替换明确的中文句末
    pat = f'({CJK_CONTEXT})\\.(?=\\s*\\n|\\s*$|{CJK_CONTEXT})'
    new_text, n = re.subn(pat, lambda m: m.group(1) + FW_PERIOD, text, flags=re.M)
    count += n
    text = new_text

    text = restore(text, stash)
    return text, count


def normalize_file(path: Path, dry_run: bool = False) -> int:
    if not path.exists() or path.name in SKIP_FILES:
        return 0
    original = path.read_text(encoding='utf-8')
    text = original
    total = 0
    # 多轮直到稳定
    for _ in range(20):
        new_text, count = normalize_text(text)
        if count == 0 or new_text == text:
            break
        text = new_text
        total += count
    if total == 0:
        return 0
    if not dry_run:
        path.write_text(text, encoding='utf-8')
    return total


def collect_targets():
    targets = []
    for fn in TARGET_ROOT_FILES:
        p = ROOT / fn
        if p.exists():
            targets.append(p)
    for d in TARGET_DIRS:
        dp = ROOT / d
        if not dp.exists():
            continue
        for f in dp.rglob('*.md'):
            if f.name in SKIP_FILES:
                continue
            targets.append(f)
    return targets


def main():
    args = sys.argv[1:]
    dry_run = '--dry-run' in args
    args = [a for a in args if a != '--dry-run']

    if args:
        targets = [Path(a) for a in args]
    else:
        targets = collect_targets()

    print(f"{'[DRY RUN] ' if dry_run else ''}规范化 {len(targets)} 个 md 文件...")
    print()

    total_replacements = 0
    changed_files = 0
    for t in targets:
        n = normalize_file(t, dry_run=dry_run)
        if n > 0:
            rel = t.relative_to(ROOT) if t.is_relative_to(ROOT) else t
            print(f"  [{n:6d}]  {rel}")
            total_replacements += n
            changed_files += 1

    print()
    print(f"共替换 {total_replacements} 处,影响 {changed_files} 个文件。")
    if dry_run:
        print("(dry-run 模式,未写盘)")


if __name__ == '__main__':
    main()
