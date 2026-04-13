#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AI 小游戏与 Playable 体验研究 — 苹果风静态站点构建脚本

用法:
    cd "/Users/bytedance/research 牙刷"
    python3 scripts/build_site.py

输出:
    docs/ 下的完整静态站点,可直接部署到 GitHub Pages
"""

import os
import re
import json
import shutil
from pathlib import Path
from html import escape as html_escape

import markdown
from markdown.extensions import fenced_code, tables, toc, codehilite

# ============================================================
# 路径配置
# ============================================================
ROOT = Path(__file__).resolve().parent.parent
DOCS = ROOT / "docs"
ASSETS = DOCS / "assets"
DATA_OUT = DOCS / "data"

# 源文件模块顺序(决定导航顺序)
MODULES_ORDER = [
    ("00-方法论与术语", "方法论与术语", "研究规则 / 可信度 / 术语表"),
    ("01-赛道现状与市场结构", "赛道现状与市场结构", "赛道定义 / 市场规模 / 平台格局 / 玩家全景"),
    ("02-产品与玩法前沿", "产品与玩法前沿", "中国 / 美国 / 日韩 / 趋势综合"),
    ("03-技术栈与可行性GAP", "技术栈与可行性 GAP", "技术能力 / 市场期待 / 真实 GAP / 机会"),
    ("04-玩家行为与留存心理", "玩家行为与留存心理", "付费心理 / 留存曲线 / 情感依恋 / 退坑模式"),
    ("05-跨品类启发", "跨品类启发", "广告 / 社交 / 教育 / 陪伴工具 / 迁移矩阵"),
    ("06-机会地图整合", "机会地图整合", "机会地图 / 产品 / 投资 / 行业 / 战略"),
]

# 根级文件(顶栏显示)
ROOT_FILES = [
    ("README.md", "总览"),
    ("research-plan.md", "研究方案"),
    ("校验点5-最终简报.md", "最终简报"),
    ("PROGRESS.md", "进度跟踪"),
    ("sources.md", "全局来源"),
]


# ============================================================
# 工具
# ============================================================
def slugify(s: str) -> str:
    """把路径转为安全的 URL slug(保留中文)"""
    s = s.replace(" ", "-").replace("/", "-")
    s = re.sub(r"[^\w\u4e00-\u9fff\-.]", "", s)
    return s


def strip_md(text: str) -> str:
    """去掉 markdown 标记,用于搜索索引 / snippet / 描述"""
    text = re.sub(r"```.*?```", " ", text, flags=re.S)
    text = re.sub(r"`[^`]*`", " ", text)
    text = re.sub(r"!\[.*?\]\([^)]*\)", " ", text)
    text = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", text)
    text = re.sub(r"^#+\s*", "", text, flags=re.M)
    text = re.sub(r"[*_>|#\-=]", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def first_para(md_text: str, max_len=180) -> str:
    """提取第一段非空文本(去 frontmatter / 标题)作为描述"""
    lines = md_text.split("\n")
    buf = []
    for line in lines:
        s = line.strip()
        if not s:
            if buf:
                break
            continue
        if s.startswith("#"):
            continue
        if s.startswith(">") or s.startswith("---"):
            continue
        buf.append(s)
        if sum(len(x) for x in buf) > max_len:
            break
    text = strip_md(" ".join(buf))
    if len(text) > max_len:
        text = text[:max_len].rstrip() + "…"
    return text


# ============================================================
# 扫描源文件
# ============================================================
def scan_sources():
    """扫描所有要渲染的 md 文件,返回结构化清单"""
    docs = []  # [{src, rel_url, title, module_dir, module_label, kind}]

    # 根级文件
    for fname, label in ROOT_FILES:
        p = ROOT / fname
        if p.exists():
            docs.append({
                "src": p,
                "rel_url": p.stem + ".html",
                "title": label,
                "module_dir": None,
                "module_label": "总览",
                "kind": "root",
                "raw_name": fname,
            })

    # 模块文件
    for mdir, mlabel, mdesc in MODULES_ORDER:
        mpath = ROOT / mdir
        if not mpath.exists():
            continue
        files = sorted([f for f in mpath.iterdir() if f.suffix == ".md"])
        for f in files:
            # README 用"模块首页"处理
            if f.name == "README.md":
                rel = f"modules/{slugify(mdir)}/index.html"
                title = mlabel
                kind = "module_index"
            else:
                rel = f"modules/{slugify(mdir)}/{slugify(f.stem)}.html"
                title = f.stem
                kind = "module_page"
            docs.append({
                "src": f,
                "rel_url": rel,
                "title": title,
                "module_dir": mdir,
                "module_label": mlabel,
                "module_desc": mdesc,
                "kind": kind,
                "raw_name": f.name,
            })

    return docs


def scan_data_files():
    """扫描所有 csv/xlsx/tsv,复制到 docs/data/ 并记录下载清单"""
    DATA_OUT.mkdir(parents=True, exist_ok=True)
    data_files = []
    patterns = [".csv", ".xlsx", ".tsv"]

    for root, dirs, files in os.walk(ROOT):
        rel_root = Path(root).relative_to(ROOT)
        if rel_root.parts and rel_root.parts[0] in ("docs", "scripts", ".git"):
            continue
        for f in files:
            if any(f.endswith(p) for p in patterns):
                src = Path(root) / f
                dest_name = f"{slugify(str(rel_root)).replace('-', '_')}__{f}" if str(rel_root) != "." else f
                dest = DATA_OUT / dest_name
                shutil.copy2(src, dest)
                data_files.append({
                    "name": f,
                    "module": str(rel_root) if str(rel_root) != "." else "(根)",
                    "size": src.stat().st_size,
                    "url": f"data/{dest_name}",
                })
    return sorted(data_files, key=lambda x: (x["module"], x["name"]))


def scan_images():
    """扫描图片并复制到 docs/assets/img/ """
    img_out = ASSETS / "img"
    img_out.mkdir(parents=True, exist_ok=True)
    image_map = {}  # src_abs -> web_rel_url

    for root, dirs, files in os.walk(ROOT):
        rel_root = Path(root).relative_to(ROOT)
        if rel_root.parts and rel_root.parts[0] in ("docs", "scripts", ".git"):
            continue
        for f in files:
            if f.lower().endswith((".jpg", ".jpeg", ".png", ".gif", ".webp", ".svg")):
                src = Path(root) / f
                # 用模块前缀避免重名
                prefix = str(rel_root).replace("/", "__").replace(" ", "_")
                dest_name = f"{prefix}__{f}" if prefix and prefix != "." else f
                dest = img_out / dest_name
                try:
                    shutil.copy2(src, dest)
                    image_map[src.resolve()] = f"assets/img/{dest_name}"
                except Exception as e:
                    print(f"  ⚠️ 图片复制失败 {src}: {e}")
    return image_map


# ============================================================
# Markdown 渲染(自定义)
# ============================================================
MD_EXT = [
    "extra",         # 表格、fenced code 等
    "tables",
    "fenced_code",
    "toc",
    "codehilite",
    "sane_lists",
    "smarty",
    "attr_list",
]
MD_CFG = {
    "toc": {"permalink": "#", "toc_depth": "2-4"},
    "codehilite": {"css_class": "codehilite", "guess_lang": False},
}


def render_markdown(src_path: Path, image_map: dict, doc_info: dict, docs_depth: int) -> tuple[str, str]:
    """渲染单个 md 文件,返回 (html_body, toc_html)"""
    text = src_path.read_text(encoding="utf-8")

    # 1. 修正图片路径 — md 里通常是 assets/xxx.jpg 相对路径
    #    要把它们指向站点的 assets/img/<prefix>__xxx.jpg
    src_dir = src_path.parent
    def img_replacer(m):
        alt, path = m.group(1), m.group(2)
        # 试解析为绝对路径
        abs_path = (src_dir / path).resolve()
        if abs_path in image_map:
            # 转成从当前 html 页面出发的相对路径
            rel = "../" * docs_depth + image_map[abs_path]
            return f"![{alt}]({rel})"
        return m.group(0)
    text = re.sub(r"!\[([^\]]*)\]\(([^)]+)\)", img_replacer, text)

    # 2. 修正 md 之间的相互链接
    def link_replacer(m):
        label, path = m.group(1), m.group(2)
        if path.startswith(("http:", "https:", "#", "mailto:")):
            return m.group(0)
        # .md → .html
        if path.endswith(".md"):
            new = path[:-3] + ".html"
            return f"[{label}]({new})"
        return m.group(0)
    text = re.sub(r"\[([^\]]*)\]\(([^)]+)\)", link_replacer, text)

    # 3. 渲染
    md = markdown.Markdown(extensions=MD_EXT, extension_configs=MD_CFG)
    body = md.convert(text)
    toc_html = getattr(md, "toc", "")
    return body, toc_html


# ============================================================
# HTML 模板
# ============================================================
BASE_TPL = """<!DOCTYPE html>
<html lang="zh-CN" data-theme="light">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<meta name="description" content="{description}">
<title>{title} · AI 小游戏与 Playable 体验研究</title>
<link rel="stylesheet" href="{base_prefix}assets/style.css">
<link rel="icon" href="data:image/svg+xml,<svg xmlns=%22http://www.w3.org/2000/svg%22 viewBox=%220 0 100 100%22><text y=%22.9em%22 font-size=%2290%22>🎮</text></svg>">
</head>
<body>

<nav class="topnav">
  <div class="topnav-inner">
    <button class="menu-toggle" aria-label="菜单">☰</button>
    <a class="topnav-logo" href="{base_prefix}index.html">🎮 AI 游戏研究</a>
    <div class="topnav-links">
      <a href="{base_prefix}index.html">总览</a>
      <a href="{base_prefix}校验点5-最终简报.html">最终简报</a>
      <a href="{base_prefix}research-plan.html">研究方案</a>
      <a href="{base_prefix}downloads.html">下载</a>
      <a href="https://github.com" target="_blank" rel="noopener">GitHub</a>
      <button class="theme-toggle" aria-label="切换主题">☾</button>
    </div>
  </div>
</nav>
<div class="scroll-progress"></div>

<div class="layout {layout_class}">
  {sidebar}
  <main class="main">
    {content}
  </main>
  {toc_right}
</div>

<footer class="footer">
  AI 小游戏与 Playable 体验赛道研究 · 2026-04 · 由 Claude 研究团队生成 · <a href="{base_prefix}sources.html">来源索引</a>
</footer>

<script src="{base_prefix}assets/script.js" defer></script>
</body>
</html>
"""


def build_sidebar(docs, current_url, base_prefix: str) -> str:
    """生成左侧栏 HTML。current_url 用于标记 active。"""
    parts = ['<aside class="sidebar">']

    # 搜索框
    parts.append('<div class="sidebar-section">')
    parts.append('<div class="sidebar-section-title">搜索</div>')
    parts.append('<input type="text" class="search-box" id="search-input" placeholder="搜索全文…">')
    parts.append('<div id="search-results"></div>')
    parts.append('</div>')

    # 总览
    root_docs = [d for d in docs if d["kind"] == "root"]
    if root_docs:
        parts.append('<div class="sidebar-section">')
        parts.append('<div class="sidebar-section-title">总览</div>')
        parts.append('<ul class="sidebar-files">')
        for d in root_docs:
            active = " active" if d["rel_url"] == current_url else ""
            parts.append(f'<li><a class="{active}" href="{base_prefix}{d["rel_url"]}">{html_escape(d["title"])}</a></li>')
        parts.append('</ul>')
        parts.append('</div>')

    # 按模块分组
    for mdir, mlabel, mdesc in MODULES_ORDER:
        mdocs = [d for d in docs if d.get("module_dir") == mdir]
        if not mdocs:
            continue
        parts.append('<div class="sidebar-section">')
        parts.append('<div class="sidebar-section-title">' + html_escape(mlabel) + '</div>')

        # 模块 README 作为首页
        idx = next((d for d in mdocs if d["kind"] == "module_index"), None)
        if idx:
            active = " active" if idx["rel_url"] == current_url else ""
            parts.append(f'<a class="sidebar-module-title{active}" href="{base_prefix}{idx["rel_url"]}">{html_escape(mlabel)} 索引</a>')

        # 子文件(除 README)
        subs = [d for d in mdocs if d["kind"] == "module_page"]
        if subs:
            parts.append('<ul class="sidebar-files">')
            for d in subs:
                active = " active" if d["rel_url"] == current_url else ""
                parts.append(f'<li><a class="{active}" href="{base_prefix}{d["rel_url"]}">{html_escape(d["title"])}</a></li>')
            parts.append('</ul>')
        parts.append('</div>')

    parts.append('</aside>')
    return "\n".join(parts)


def build_toc_right(body_html: str) -> str:
    """从已渲染的 body HTML 里抽取 H2/H3/H4 标题,生成右侧 TOC 栏 HTML。

    markdown 的 toc 扩展会自动给每个标题加 id,形如 <h2 id="xxx">xxx</h2>,
    这里用正则解析即可。
    """
    # 匹配 <hN id="xxx">...</hN>,N ∈ {2,3,4}
    pat = re.compile(
        r'<h([234])\s+id="([^"]+)"[^>]*>(.*?)</h\1>',
        re.DOTALL,
    )
    items = []
    for m in pat.finditer(body_html):
        level = int(m.group(1))
        hid = m.group(2)
        inner = m.group(3)
        # 去掉 inner 里的 HTML 标签(permalink 的 # 锚)
        text = re.sub(r"<[^>]+>", "", inner).strip()
        # markdown toc 扩展的 permalink 会在去标签后留下尾部 "#"
        text = text.rstrip(" #").strip()
        if not text:
            continue
        items.append((level, hid, text))

    if len(items) < 2:
        return ""

    parts = ['<aside class="toc-right">',
             '<div class="toc-right-title">本文目录</div>',
             '<ul>']
    for level, hid, text in items:
        cls = f"toc-h{level}" if level > 2 else ""
        parts.append(
            f'<li class="{cls}"><a href="#{hid}">{html_escape(text)}</a></li>'
        )
    parts.append('</ul>')
    parts.append('</aside>')
    return "\n".join(parts)


def render_page(doc, docs, body_html, image_map) -> str:
    """渲染单个文档页面"""
    current_url = doc["rel_url"]
    # 计算 base_prefix(相对于当前页面到 docs/ 根的距离)
    depth = current_url.count("/")
    base_prefix = "../" * depth

    sidebar = build_sidebar(docs, current_url, base_prefix)

    # 面包屑
    breadcrumb = []
    breadcrumb.append(f'<a href="{base_prefix}index.html">总览</a>')
    if doc.get("module_dir"):
        breadcrumb.append(f'<a href="{base_prefix}modules/{slugify(doc["module_dir"])}/index.html">{html_escape(doc["module_label"])}</a>')
    breadcrumb.append(html_escape(doc["title"]))
    breadcrumb_html = '<div class="article-breadcrumb">' + " · ".join(breadcrumb) + '</div>'

    content = f'<article class="article">{breadcrumb_html}{body_html}</article>'

    # 右侧 TOC 栏
    toc_right = build_toc_right(body_html)
    layout_class = "layout-with-toc" if toc_right else ""

    desc = first_para(doc["src"].read_text(encoding="utf-8"))
    return BASE_TPL.format(
        title=html_escape(doc["title"]),
        description=html_escape(desc),
        base_prefix=base_prefix,
        sidebar=sidebar,
        content=content,
        toc_right=toc_right,
        layout_class=layout_class,
    )


def render_index(docs, data_files) -> str:
    """渲染首页"""
    current_url = "index.html"
    sidebar = build_sidebar(docs, current_url, "")

    # 收集模块索引卡片
    cards = []
    for mdir, mlabel, mdesc in MODULES_ORDER:
        mdocs = [d for d in docs if d.get("module_dir") == mdir]
        if not mdocs:
            continue
        idx = next((d for d in mdocs if d["kind"] == "module_index"), None)
        target = idx["rel_url"] if idx else (mdocs[0]["rel_url"] if mdocs else "#")
        num = mdir.split("-")[0]
        cards.append(f"""
        <a class="module-card" href="{target}">
          <div class="module-card-number">模块 {num}</div>
          <div class="module-card-title">{html_escape(mlabel)}</div>
          <div class="module-card-desc">{html_escape(mdesc)}</div>
          <div class="module-card-arrow">→</div>
        </a>""")

    cards_html = '<div class="modules-grid">' + "".join(cards) + '</div>'

    # 关键数字 cards
    insight_nums = [
        ("6+1", "研究模块"),
        ("92", "全球玩家全景图"),
        ("18", "技术 GAP(S1 × 7)"),
        ("29", "子文件总数"),
        ("8.03", "Gemini 评分均值"),
        ("12-24", "GPF 窗口期(月)"),
    ]
    insights_html = '<div class="insights-grid">'
    for n, l in insight_nums:
        insights_html += f'<div class="insight-card"><div class="insight-number">{n}</div><div class="insight-label">{l}</div></div>'
    insights_html += '</div>'

    content = f"""
    <section class="hero">
      <div class="hero-eyebrow">2026 年 · 赛道研究</div>
      <h1>AI 小游戏与<br>Playable 体验</h1>
      <p class="hero-subtitle">从赛道边界、产品玩法、技术可行性、玩家心理、跨品类启发五大维度,
      回答"AI 如何重塑小游戏赛道",并为产品经理、投资人、行业观察者、战略规划者四类读者同时输出机会地图。</p>
      <div class="hero-cta">
        <a class="btn btn-primary" href="校验点5-最终简报.html">查看最终简报 →</a>
        <a class="btn btn-secondary" href="modules/06-机会地图整合/index.html">机会地图</a>
      </div>
    </section>

    <h2 style="font-size:40px;font-weight:600;letter-spacing:-0.022em;margin-bottom:12px;">关键数字</h2>
    <p style="color:var(--text-secondary);margin-bottom:24px;">研究产出的全局规模概览。</p>
    {insights_html}

    <h2 style="font-size:40px;font-weight:600;letter-spacing:-0.022em;margin:80px 0 12px;">研究模块</h2>
    <p style="color:var(--text-secondary);margin-bottom:32px;">六个核心模块 + 一个最终整合,点击进入。</p>
    {cards_html}

    <h2 style="font-size:40px;font-weight:600;letter-spacing:-0.022em;margin:80px 0 12px;">三个核心洞察</h2>
    <div class="insights-grid" style="grid-template-columns:1fr;gap:20px;">
      <div class="insight-card" style="padding:32px;">
        <div style="font-size:14px;color:var(--accent);font-weight:600;margin-bottom:8px;">洞察 ①</div>
        <div style="font-size:22px;font-weight:600;margin-bottom:8px;">"AI × 小游戏"现在是真空带,经济学卡死</div>
        <div style="color:var(--text-secondary);font-size:15px;">Token/session $0.014 vs IAA ARPDAU &lt; $0.05,毛利空间吃不起 AI 税。微信小游戏 Top 200 零 AI-native 作品 — 这个"真空带"现在仍未被正面攻破。</div>
      </div>
      <div class="insight-card" style="padding:32px;">
        <div style="font-size:14px;color:var(--accent);font-weight:600;margin-bottom:8px;">洞察 ②</div>
        <div style="font-size:22px;font-weight:600;margin-bottom:8px;">Generative Playable Feed(GPF)是真正破局的新物种</div>
        <div style="color:var(--text-secondary);font-size:15px;">Rezona / LoopIt / YouTube Playables Builder 用 Pipeline AI + UGC 飞轮绕过 Token 真空带 — AI 只在创作时调用一次,消费端静态化。中国 Pipeline-Creator 象限零玩家,12-24 个月窗口期。</div>
      </div>
      <div class="insight-card" style="padding:32px;">
        <div style="font-size:14px;color:var(--accent);font-weight:600;margin-bottom:8px;">洞察 ③</div>
        <div style="font-size:22px;font-weight:600;margin-bottom:8px;">游戏性的定义权已从游戏行业脱离</div>
        <div style="color:var(--text-secondary);font-size:15px;">Character.AI / 星野 / 猫箱 / Duolingo Max 都不叫自己游戏,但用户行为、付费心理与游戏完全同构。未来最赚钱的"准游戏"产品都会拒绝游戏标签 — 中国版号制度反向助推了这一趋势。</div>
      </div>
    </div>

    <h2 style="font-size:40px;font-weight:600;letter-spacing:-0.022em;margin:80px 0 12px;">数据下载</h2>
    <p style="color:var(--text-secondary);margin-bottom:24px;">所有结构化数据文件(CSV / Excel),可直接下载用于分析。</p>
    <p><a class="btn btn-secondary" href="downloads.html">查看全部 {len(data_files)} 个数据文件 →</a></p>
    """

    return BASE_TPL.format(
        title="总览",
        description="AI 小游戏与 Playable 体验赛道研究 · 2026",
        base_prefix="",
        sidebar=sidebar,
        content=content,
        toc_right="",
        layout_class="",
    )


def render_downloads(docs, data_files) -> str:
    current_url = "downloads.html"
    sidebar = build_sidebar(docs, current_url, "")

    rows = []
    for d in data_files:
        size_kb = d["size"] / 1024
        size_str = f"{size_kb:.1f} KB" if size_kb < 1024 else f"{size_kb/1024:.1f} MB"
        rows.append(
            f'<tr><td>{html_escape(d["name"])}</td><td>{html_escape(d["module"])}</td>'
            f'<td>{size_str}</td><td><a href="{d["url"]}" download>下载</a></td></tr>'
        )

    content = f"""
    <article class="article">
      <div class="article-breadcrumb"><a href="index.html">总览</a> · 数据下载</div>
      <h1>数据下载</h1>
      <p>研究过程中生成的全部结构化数据文件({len(data_files)} 个),可直接下载。</p>
      <div class="table-wrapper">
      <table>
        <thead><tr><th>文件名</th><th>所属模块</th><th>大小</th><th>操作</th></tr></thead>
        <tbody>{"".join(rows)}</tbody>
      </table>
      </div>
    </article>
    """

    return BASE_TPL.format(
        title="数据下载",
        description="研究产出的全部结构化数据文件",
        base_prefix="",
        sidebar=sidebar,
        content=content,
        toc_right="",
        layout_class="",
    )


# ============================================================
# 主流程
# ============================================================
def main():
    print("=" * 60)
    print("  AI 小游戏与 Playable 体验研究 — 苹果风站点构建")
    print("=" * 60)

    # 清理旧产出(保留 assets 目录因为有 style/script)
    print("\n[1/6] 清理旧产出...")
    if DOCS.exists():
        for item in DOCS.iterdir():
            if item.name == "assets":
                # 保留 style.css / script.js,清理其他
                for sub in item.iterdir():
                    if sub.name not in ("style.css", "script.js"):
                        if sub.is_dir():
                            shutil.rmtree(sub)
                        else:
                            sub.unlink()
                continue
            if item.is_dir():
                shutil.rmtree(item)
            else:
                item.unlink()
    else:
        DOCS.mkdir(parents=True, exist_ok=True)
        ASSETS.mkdir(exist_ok=True)

    # 扫描图片并复制
    print("\n[2/6] 扫描图片资产...")
    image_map = scan_images()
    print(f"  → 复制了 {len(image_map)} 张图片到 docs/assets/img/")

    # 扫描数据文件
    print("\n[3/6] 扫描数据文件...")
    data_files = scan_data_files()
    print(f"  → 复制了 {len(data_files)} 个数据文件到 docs/data/")

    # 扫描 md 源文件
    print("\n[4/6] 扫描 Markdown 源文件...")
    docs = scan_sources()
    print(f"  → 发现 {len(docs)} 个 md 文件")

    # 渲染所有页面
    print("\n[5/6] 渲染 HTML 页面...")
    search_index = []
    for doc in docs:
        out_path = DOCS / doc["rel_url"]
        out_path.parent.mkdir(parents=True, exist_ok=True)
        depth = doc["rel_url"].count("/")
        body, toc_html = render_markdown(doc["src"], image_map, doc, depth)
        html = render_page(doc, docs, body, image_map)
        out_path.write_text(html, encoding="utf-8")

        # 加入搜索索引
        raw_text = doc["src"].read_text(encoding="utf-8")
        search_index.append({
            "title": doc["title"],
            "path": f"{doc['module_label']} · {doc['raw_name']}" if doc.get("module_label") else doc["raw_name"],
            "url": doc["rel_url"],
            "content": strip_md(raw_text)[:4000],
        })

    # 渲染首页
    (DOCS / "index.html").write_text(render_index(docs, data_files), encoding="utf-8")
    (DOCS / "downloads.html").write_text(render_downloads(docs, data_files), encoding="utf-8")

    # 写搜索索引
    (ASSETS / "search-index.json").write_text(
        json.dumps(search_index, ensure_ascii=False),
        encoding="utf-8"
    )

    # .nojekyll(GitHub Pages 友好,防止 _ 开头目录被忽略)
    (DOCS / ".nojekyll").write_text("", encoding="utf-8")

    # 统计
    total_html = sum(1 for _ in DOCS.rglob("*.html"))
    print(f"  → 生成 {total_html} 个 HTML 页面")

    print("\n[6/6] 构建完成!")
    print(f"  → 输出目录: {DOCS}")
    print(f"  → 打开: open '{DOCS}/index.html'")
    print(f"  → GitHub Pages: 把 {DOCS.name}/ 目录设为 Pages source")
    print("=" * 60)


if __name__ == "__main__":
    main()
