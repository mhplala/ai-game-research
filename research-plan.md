# AI 小游戏与 Playable 体验赛道研究 — 完整研究方案

> 版本：v1.0 · 创建日期：2026-04-13
> 上游项目：`/Users/bytedance/research 牙刷/`（儿童口腔，方法论母本）
> 负责：Claude Opus 4.6 (1M context) + Gemini 3.1 Pro Preview（双路 fallback)

---

## 1. 研究主题

**"AI 如何重塑小游戏与 playable 体验赛道 — 2022-2026 的产品创新、商业机会与玩法前沿"**

赛道定义（三要素交集）：
- **小游戏**(Light Games):<50MB 即开即玩，微信/抖音/Meta/Steam/Poki 等轻量分发平台上的游戏
- **Playable 体验**：可互动广告 + 互动 H5 + 互动营销的广义 playable 内容
- **AI 游戏**:GenAI 作为核心机制（不是辅助工具）的新型游戏

**重点**：不做"AI 工具辅助开发"的研究（那是开发工具话题），只做 **"AI 作为玩法机制本身"** 或 **"AI 改变分发/变现/留存"** 的部分。

---

## 2. 研究目的 · 四视角"全都要"

与上一个项目（儿童口腔）的"品牌方策划新品线"单一视角不同，本项目**同时服务四种读者**:

| 视角 | 读者画像 | 研究重点 |
|------|------|------|
| **A. 产品经理 / 创业者** | 想立项一款 AI 小游戏 / playable 产品 | 具体产品机会、玩法原型、竞品空白、技术可行性 |
| **B. 投资人** | 一级市场 VC / 战投 | 赛道地图、玩家分层、融资历史、商业模式、退出路径 |
| **C. 行业从业者** | 游戏公司中层 / 市场营销人 / 媒体人 | 技术趋势、案例库、新概念、数据对比、竞争格局 |
| **D. 战略规划** | 大厂 / 平台新业务负责人 | 平台机会、生态位、进入路径、差异化、组织能力匹配 |

**四视角在每个模块的"洞察"章节都要分别回答**，不是单独一个模块。

---

## 3. 五大研究模块（+ 1 整合）

镜像口腔项目结构（工具链复用），但内容全部新写：

### 模块 00 · 方法论与术语
- methodology.md — 可信度分级 / 引用格式 / 安全网规则
- glossary.md — LLM / Diffusion / Playable / CPM / IAP / GaaS / NPC 等术语
- **不需要 sub-agent**，主 agent 直接写

### 模块 01 · 赛道现状与市场结构
- 1.1 赛道定义与边界（什么算 AI 小游戏？和传统小游戏/AI-native 游戏的分界）
- 1.2 市场规模与增速（2022-2025 全球/中国 /美/日韩数据）
- 1.3 平台格局（微信 / 抖音 / Meta Horizon / Poki / CrazyGames / Steam 等）
- 1.4 玩家全景图（100+ 公司/产品的结构化 Excel 表，15 字段）

### 模块 02 · 产品与玩法前沿
- 2.1 中国市场（微信/抖音小游戏 × AI 应用）
- 2.2 美国市场（AI-native 创业潮：Inworld / Hidden Door / Latitude / Altera)
- 2.3 日韩市场（Krafton / Nexon / NCSoft / CyberAgent / AI VN 实验）
- 2.4 跨区域趋势综合

### 模块 03 · 技术栈与可行性 GAP
- 不是"合规 GAP"，而是**技术能力 vs 市场期待的裂缝**
- 3.1 现有技术栈能做什么（LLM NPC / Diffusion 贴图 / RL 动态关卡 / WebGPU)
- 3.2 市场期待什么（用户访谈 / 需求假设）
- 3.3 真实 GAP（例：长时记忆 / 成本经济学 / 多人一致性）
- 3.4 解决方案路径与机会识别

### 模块 04 · 玩家行为与留存心理
- 不是儿童发展心理学，而是 **"为什么玩家为 AI 游戏付费 / 留存 / 退坑"**
- 4.1 付费心理与 Token 经济学（AI Dungeon/Character.AI subscription 模式）
- 4.2 留存曲线特征（AI 游戏的 D1/D7/D30 vs 传统小游戏）
- 4.3 情感依恋与 AI NPC(Replika/Character.AI 的启示）
- 4.4 退坑模式与长期留存难题

### 模块 05 · 跨品类启发
- 5.1 广告 × 游戏（Playable Ads 往游戏化）
- 5.2 社交 × 游戏（Discord/小红书社群游戏化）
- 5.3 教育 × 游戏（Duolingo 式游戏化 × AI 导师）
- 5.4 陪伴/工具 × 游戏（Notion/Character.AI 往游戏形态延展）
- 5.5 可迁移矩阵（15+ 条跨品类概念 × AI 游戏可迁移性）

### 模块 06 · 四视角机会地图整合（最终交付）
- 6.1 机会地图主文件（三维矩阵）
- 6.2 产品机会清单（A. PM/创业者视角，≥8 个）
- 6.3 投资标的与赛道地图（B. 投资视角）
- 6.4 行业趋势判断（C. 行业视角）
- 6.5 战略进入路径（D. 战略视角）
- 6.6 风险警示（不要做什么）

---

## 4. 地域 Tier 分层

与口腔项目（日本医学中心）不同，AI 游戏赛道是**双中心**:

| Tier | 区域 | 核心角色 |
|------|------|------|
| **Tier 1（深挖）** | **中国** | 小游戏最大单一市场 + AI 应用本土化最快 |
| **Tier 1（深挖）** | **美国** | AI-native 创业发源地 + VC 资金最密 |
| **Tier 2（中度）** | **日本 + 韩国** | 大厂 AI 游戏实验室 / AI VN 交叉 |
| **Tier 3（点缀）** | 欧洲 indie(Poki/King/Supercell)+ 东南亚 | WebGPU 技术前沿 + 小游戏本地化 |

---

## 5. 信息源策略

比口腔项目更重电商/融资/媒体数据（因为赛道缺学术基础）：

| 优先级 | 来源 | 可信度 |
|------|------|------|
| **高** | 官方公告、融资数据库（Crunchbase / Dealroom / 36Kr）、Steam SteamDB 数据、Data.ai / Sensor Tower / 点点数据 | 高 |
| **中** | 行业媒体（TechCrunch / Game Developer / Venturebeat / 游戏陀螺 / GameLook / 手游那点事）、X/Twitter 开发者自述、开发者 blog | 中 |
| **低** | YouTube gameplay / Reddit 讨论 / 小红书 / 知乎 | 低（仅作趋势佐证） |

---

## 6. 执行流水线 · 并行 + Gemini 兜底

与口腔项目不同，这次设计 **双路 fallback** 机制：

### 正常流程（Claude 为主）
1. 派 5-7 个 Claude sub-agents 并行做第一批模块
2. Monitor 每 30s 监听文件系统
3. 主 agent 并发等待

### 异常处理（Gemini 兜底）
4. **任一 sub-agent 卡 >10 分钟零输出**：立即派 **Gemini 3.1 Pro** 并行跑同一任务（写到 `.gemini.md` 后缀文件，不冲突）
5. 两者同时跑，先出的先用
6. 两者都出了就 diff 选好的，另一个进 `.backup/`

### 后续
7. 主 agent 做模块 2.4 / 1.4 全景图整合（用 Claude + Gemini 双写，取优）
8. 跑 `quality_audit.py`(Gemini 2.5 Flash 评审）
9. 跑 `optimize_parallel.py`(Gemini 3.1 Pro 改写，复用口腔项目脚本）
10. 跑 `regression_check.py` 分类 SAFE/DANGER
11. 建苹果风静态站点（复用 `build_site.py`)
12. 二次评审 + 对比前后
13. Push 到 GitHub（新 repo `ai-playable-research` 或类似）

---

## 7. 工具链（全部复用 + 新增 1 个）

### 从口腔项目完整复用
- `scripts/build_site.py` — 苹果风静态站点
- `scripts/normalize_punct.py` — 中文标点规范化
- `scripts/quality_audit.py` — Gemini 2.5 Flash 评审
- `scripts/optimize_parallel.py` — Gemini 3.1 Pro 批量优化
- `scripts/regression_check.py` — 关键事实保留度检查

### 新写
- `scripts/gemini_fallback.py` — **新！** 卡住时调 Gemini 3.1 Pro 兜底同一任务

---

## 8. 安全网设计

从口腔项目继承的原则（已证明有效）：

1. **每个关键节点 git commit**（快照可回滚）
2. **`optimize_parallel.py` 产出到 `optimized/` 镜像目录，不动原文**
3. **`regression_check.py` 字符数 < -20% 自动标 DANGER**
4. **关键数字/品牌/来源编号自动保留度检查**（基于本赛道的关键词库）

---

## 9. 关键字典（新建，用于 regression check)

本赛道的"关键数字/品牌"，用于检查优化后是否丢失：

**关键品牌**:Inworld / Hidden Door / Latitude / Altera / Suck Up! / AI Dungeon / Character.AI / Replika / Krafton / Nexon / NCSoft / rct AI / 量子绘梦 / Whispers from the Star / 1001 Nights / Kinetix / Sidekick / Luna Labs / Poki / CrazyGames / 微信小游戏 / 抖音小游戏 / 羊了个羊 / 咸鱼之王 / 寻道大千 / Supercell / King

**关键概念**:GenAI NPC / LLM agent / Diffusion 贴图 / WebGPU / Playable Ads / Token 经济学 / Agentic gameplay / Procedural generation / RL dynamic content / Character consistency

**关键平台**：微信小游戏 / 抖音小游戏 / 快手小游戏 / QQ 小游戏 / Meta Horizon / Facebook Instant Games / Steam / Poki / CrazyGames / itch.io

---

## 10. 交付物清单

完成后产出（和口腔项目结构完全同构）：
- `README.md` / `research-plan.md` / `PROGRESS.md` / `sources.md` / `校验点X-简报.md`
- `00-方法论与术语/` — methodology.md / glossary.md
- `01-赛道现状与市场结构/` — 4 个子文件 + Excel 全景图 + CSV 数据
- `02-产品与玩法前沿/` — 4 个子文件 + 产品案例库
- `03-技术栈与可行性GAP/` — 4 个子文件 + GAP 清单 + 机会映射
- `04-玩家行为与留存心理/` — 4 个子文件
- `05-跨品类启发/` — 5 个子文件 + 可迁移矩阵
- `06-机会地图整合/` — 6 个子文件 · 四视角机会输出
- `docs/` — 47+ HTML 苹果风静态站点
- `质量评审报告-优化前.md` / `质量评审报告.md` / `项目认知与市场认知.md`

预计总产出：**40-50 个 md 文件 + 1 个 Excel + 10+ CSV + 1 个网站**。

---

## 11. 成功标准

- 5 个核心模块五节结构齐全
- 全景图 ≥ 80 个公司/产品 × 15 字段
- 每个模块四视角洞察都有独立回答
- 机会地图识别 ≥ 8 个差异化产品机会 + ≥ 3 个投资主题 + ≥ 2 条战略路径
- 站点可访问，右栏 TOC 苹果风，数据可下载
- 最终 Gemini 评分均分 ≥ 8.0

---

**下一步**：立即写骨架文件 + 部署工具链 + 派第一批 Claude sub-agents。
