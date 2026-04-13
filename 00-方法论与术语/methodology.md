# 研究方法论 — methodology.md

> 本文件定义所有模块必须遵守的研究规则。

---

## 1. 信息源可信度(三级)

| 级别 | 含义 | 典型来源 |
|------|------|------|
| **高(H)** | 可直接引用 | 官方融资公告、Crunchbase / Dealroom、SteamDB 公开数据、Data.ai / Sensor Tower 公开报告、Newzoo、App Annie、Steam 页面直接数据 |
| **中(M)** | 可引用需说明 | TechCrunch / Game Developer / Venturebeat / 游戏陀螺 / GameLook / 手游那点事 / 36Kr / 品玩 · 开发者 X/Twitter 公开发言 · 品牌官方 blog |
| **低(L)** | 仅作趋势佐证 | YouTube gameplay / Reddit 讨论 / 小红书笔记 / 知乎回答 / Twitter anon |

---

## 2. 事实引用格式

**行内**:`某数据/事实 [S-模块-序号]`,如 `[S-01.2-05]`

**sources.md 条目**:
```
[S-01.2-05] 标题 | URL | 访问日期(2026-04-13) | 类型(OFF/VC/MEDIA/STEAM/INSIGHT) | 可信度(高/中/低)
```

类型缩写:
- **OFF** = 品牌官网 / 官方公告
- **VC** = 融资数据库 / VC 报告
- **MEDIA** = 行业媒体
- **STEAM** = Steam / App Store / Google Play 公开页面
- **INSIGHT** = 咨询公司报告(Newzoo / Data.ai)
- **DEV** = 开发者 blog / Twitter
- **ACAD** = 学术论文(本赛道稀缺,但有也算高可信)

---

## 3. 数字类事实的交叉验证规则

**必须交叉验证**(≥ 2 个独立高可信源):
- 市场规模(¥亿 / $亿)
- 融资金额与估值
- 日活 / 月活 / 留存率
- Token 成本(OpenAI / Anthropic / Google 公开 pricing)
- 下载量 / 收入(Data.ai / Sensor Tower)

**可单源引用**:
- 品牌的产品描述(官网为准)
- 游戏的玩法机制(Steam 页面 + 官方 trailer)

**冲突处理**:
- 两个高可信源冲突 → 全部列出、标注差异原因(口径 / 时间窗 / 样本源)
- 估算或推算数据 → 加 `[估算]` 标记
- 自说自话(品牌 PR 的数据) → 标"品牌披露,未独立核实"

---

## 4. 时效性

- **优先**:**2024-2026** 数据(本赛道最热两年)
- **允许**:2022-2023 作为"赛道起点"或历史对比
- **警惕**:2022 年前的 AI 游戏数据基本无意义(GenAI 时代之前)
- **特别规则**:**超过 6 个月未更新的融资/估值** 加 "截至 YYYY-MM" 标注

---

## 5. 四视角输出原则

每个模块的 "Insights" 章节必须分四个小节:

### A. 产品视角(PM / 创业者)
- "这说明我应该做什么产品?"
- 具体到 SKU / 玩法 / 目标用户

### B. 投资视角
- "这说明哪些公司值得关注?"
- 哪些赛道估值高 / 低 / 刚起来

### C. 行业视角
- "这说明行业在发生什么?"
- 趋势判断 + 为什么

### D. 战略视角
- "这说明大厂 / 平台应该怎么布局?"
- 组织能力匹配 / 进入路径 / 防御策略

---

## 6. 关键词库(用于 regression check)

本赛道的"关键概念/品牌",优化版丢失即视为风险:

**关键品牌**:
- 美国:Inworld / Hidden Door / Latitude / Altera / AI Dungeon / Character.AI / Replika / Suck Up! / Kinetix / Sidekick.io / Couchbase / Convai
- 中国:量子绘梦 / Whispers from the Star / rct AI / 彩云小梦 / 筑梦岛 / 羊了个羊 / 咸鱼之王 / 寻道大千 / 热力小镇 / 疯狂动物园
- 日韩:1001 Nights / Krafton MOGIA / Nexon AI Lab / CyberAgent
- 欧洲:Poki / CrazyGames / King / Supercell / Suck Up!
- 平台:微信小游戏 / 抖音小游戏 / Meta Horizon / Steam / Poki / Facebook Instant Games

**关键概念**:
- GenAI NPC / LLM Agent / Agentic gameplay / Procedural Content Generation / Character Consistency / RAG / Fine-tuning / Token Economics / WebGPU / Canvas 2D / Unity / Godot / PWA / Instant Games / Playable Ads / IAP / Gacha / Live Ops / D1 / D7 / D30 / CAC / LTV / ARPPU / ARPDAU

---

## 7. 禁止事项

- 禁止编造融资数字 / 公司名 / 游戏名
- 禁止引用不可访问的 URL
- 禁止不标年份的数据(尤其市场规模)
- 禁止用"近期"、"大幅"、"显著"替代具体数字
- 禁止把 "AI 辅助开发的游戏" 归为 "AI 游戏"(界限必须明确)

---

## 8. 中文标点规范

- 正文中文 + 品牌名 / 术语保留原文(Inworld / AI Dungeon / Character.AI)
- 中文之间使用全角标点(,。:;?!())
- 英文术语之间和数字之间使用半角
- **最终由 `normalize_punct.py` 脚本统一规范化**
