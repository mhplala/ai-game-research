# 研究进度跟踪 — PROGRESS.md

> 跨会话持久化进度文件
> 最近更新：2026-04-13

---

## 当前阶段

**Phase 0 · 启动期** — 目录建好，工具链部署中，即将派出第一批 Claude sub-agents

---

## 模块状态总览

| 模块 | 子任务 | 状态 | 负责 | 备注 |
|------|------|------|------|------|
| 00 方法论 | methodology.md | ⏳ 待建 | 主 | 主 agent 写 |
| 00 方法论 | glossary.md | ⏳ 待建 | 主 | 主 agent 写 |
| 01.1 赛道定义与边界 | — | ✅ 完成 | a8bf5 | 5.2 min · 18 来源 · AI 可移除性刀 |
| 01.2 市场规模与增速 | — | ✅ 完成 | a4b42 | 3.5 min · 41 来源 · 6 CSV |
| 01.3 平台格局 | — | ✅ 完成 | a4394 | 3.7 min · 27 来源 · 12 平台对比 + CSV |
| 01.4 玩家全景图 | — | ⏸️ 依赖 01.1-01.3 + 02 | 主 | Phase 3 |
| 02.1 中国市场产品 | — | ✅ 完成 | a397f | 3.4 min · 27 案例 · "版号强制偏离"洞察 |
| 02.2 美国市场 AI-native | — | ✅ 完成 | acd4c | 4.5 min · 50+ 来源 · 退出模式分析 |
| 02.3 日韩市场 | — | ✅ 完成 | adfb6 | 5.6 min · 27 案例 · "雷声大雨将落"判断 |
| 02.4 趋势综合 | — | ⏸️ 等 02.1-02.3 | 主 | Phase 3 |
| 03 技术 GAP | — | ✅ 完成 | acc89 | 5.9 min · 18 GAP(S1×7)+ 4 文件 |
| 04 玩家心理 | — | ✅ 完成（路径已修） | a5bf9 | 6.9 min · grief/人格金标洞察 |
| 05 跨品类启发 | — | ✅ 完成（路径已修） | a01493 | 5.9 min · "游戏性定义权脱离"洞察 |
| 06 机会地图 | — | ⏸️ 最终 | 主 | Phase 4 |

图例：⏳ 待启动 / 🟡 进行中 / ✅ 完成 / ❌ 阻塞

---

## 双路 fallback 状态

| Agent | Claude sub-agent | Gemini 3.1 Pro 兜底 | 采用 |
|------|------|------|------|
| *（未启动）* | — | — | — |

---

## 关键洞察日志

### 2026-04-13 · 模块 1.2 返回（市场规模）

- **微信小游戏 2024 流水 400 亿+**（腾讯 Q3 财报 + 微信公开课 2025)
- **微信小游戏 2023 流水 200 亿+**（微信公开课 2024 首次官宣）
- **全球移动游戏 2024 ~$98.7B**(Newzoo)
- **Character.AI 2023 Series A $150M / 估值 $1B**(a16z 官宣）
- **GPT-4o-mini 每小时 AI 对话成本 ~$0.014**(OpenAI 官方 pricing 2025.03)
- **AI-native 游戏 2022-2024 累计融资 ~$1B,2023 峰值 $450M,2024 回落 30%** — 重要"赛道温度"指标
- 抖音小游戏 **~150-200 亿**(DataEye/葡萄君反推，置信度 ±30%)
- 中国小游戏大盘 **~620-690 亿元**（估算）

### 2026-04-13 · 模块 1.3 返回（平台格局）

- **12 个平台全对比**（含 AI 友好度 1-5 评分）
- **AI 策略三分法**：封闭补贴（微信/抖音）/ 开放自由（Steam/Poki/itch)/ 中间（Meta/支付宝）
- **⭐ "AI 税"吞掉 15-40% 的 ARPDAU** — 这是平台方必须补贴自家模型的经济学底层
- **Steam 2024.01 AI 内容披露政策** = 赛道分水岭（AI 披露游戏 1000 → 8000+ 款）
- **6 个平台自研 AI 游戏 Lab**:Hunyuan Game / 字节嘘嘘岛 / Krafton MOGIA / Nexon Intelligence Labs / Poki Labs / Meta Horizon AI
- **最友好平台**:Steam + Poki 并列第一；国内是抖音（豆包免费 + 审核宽松）
- **itch.io 默认抽成 10%**，是所有平台里对独立开发者最友好的

### 2026-04-13 · 模块 1.1 返回（赛道定义）— ⭐ 最锋利的洞察

- **"AI 可移除性"刀**：移除 LLM 后 gameplay loop 是否仍成立 → 不成立即为 **AI-native**（赛道主战场）；成立即为 **AI-augmented**（存量升级）
- **💥 核心判断**:"**AI × 小游戏（IAA 变现，< $0.05/DAU）的交集区域基本为零 — 这正是本研究主命题的真空地带**"
- **经济学叙事**（和 1.3 的"AI 税 15-40% ARPDAU"呼应）：
  - 现有 AI 游戏都在 Steam/iOS 付费订阅（ARPU 够大，覆盖 token 成本）
  - 现有小游戏都在 IAA 广告变现（单 DAU < $0.05，吃不起 AI 税）
  - 两者之间是**真空带**，等待端侧小模型 / 运行时级 LLM 集成把推理成本压到 tCPM 之下
- **具体里程碑事实**:
  - **AI Dungeon 2019.11** 6 周破 100 万用户 / 600 万故事（Latitude 累计融资 $3.3M)
  - **Inworld 2023.08 估值 $500M+，累计 $100M+**(AAA 合作 NetEase Team Miaozi + Niantic 8th Wall)
  - **Character.AI 2024 峰值 28M MAU → 2025 末 20M MAU**,2024.08 Google $2.7B 非独家授权 + 返聘 Shazeer/De Freitas（子赛道天花板退出事件）
  - **蔡浩宇 Anuttacon · Whispers from the Star**:2025.08.15 Steam / 2025.11 iOS，中国首个 AI-native 原生工作室出货作品，**miHoYo 创始人选择分拆而非内部项目**（强信号）
  - **微信小游戏 2024 Q2 MAU 5-7.5 亿 / 240+ 款季度千万流水，但 TOP 榜单中零 AI-native 作品**
- **两大待补 gap**:
  1. Token 成本 vs 小游戏 ARPU 的**经济学测算**（决定赛道能否成立的核心数字） → **模块 3 必须补**
  2. 中国 AI 陪伴类（Glow/星野/筑梦岛/猫箱）的 MAU/ARPU/留存公开数据极度缺失

### 2026-04-13 · 模块 3 返回（技术栈 + GAP 清单）

- **18 条 GAP**(S1 × 7 阻塞级 / S2 × 9 体验级 / S3 × 2 效率级）
- **最严重 3 个 GAP**:
  - **G01 长时记忆工程墙**(S1/产品+技术）— LLM 上下文解不了，必须 RAG + vector + 遗忘策略 middleware,**是角色产品的生死线**
  - **G06 Token 成本 vs ARPDAU 倒挂**(S1/商业）— **GPT-4o-mini 堪堪打平，GPT-4o 倒亏，需再降 5-10 倍才能支撑"免费 AI 游戏 + 广告变现"**
  - **G10 LTV < $100 门槛**(S1/商业）— **Character.ai 被 $25 亿"技术授权收购"证明纯陪伴天花板只有 $20-40**,VC 集体学到教训
- **最佳创业机会 O-7**:**"AI 机制而非 AI 角色"** — 绕过 G01/G02/G06 三堵墙，用 AI 做关卡生成/对手/裁判（对标 Volley/Hidden Door/Series AI)
- **最佳投资主题 T-1**:**游戏 AI middleware** — 打包"人设+记忆+声音+立绘+评测"SDK，填 Inworld 价格空缺，Bitkraft/a16z 都在看，**18-24 个月时间窗**

### 2026-04-13 · 模块 4 返回（玩家心理）— 反直觉洞察爆炸

- **💥 Replika Pro Churn < 3%/月，接近 Netflix** — 因为情感依恋把订阅心智从**交易**转为**关系续费**，价格敏感度几乎消失
- **💥 AI 游戏留存曲线 = 高峰值 + D7-D30 断崖 + 超长尾** — 是"情感 MMO"，只服务能跨过"关系门槛"的 **5-10% 玩家**，其余是必然筛选流失。**用传统 D1/D7 做 KPI 会系统性误导产品决策**
- **💥 退坑最强触发器不是无聊，是 "人格漂移" 导致的 grief（哀伤）反应** — 玩家因 AI "不再是 TA" 产生类似丧亲情绪，情感强度远超卡关退坑
- **💥 A/B 测试在 AI 游戏里是有毒的** — 传统互联网实验文化需要被**抛弃**(filter 更新/上下文截断/prompt 改动都会引发人格漂移）
- **强建议**:
  1. **"记忆系统 + 人格一致性工程"列为 Day 1 工程优先级**
  2. 建立 "人格金标 eval" 流程持续监控漂移
  3. 年付定价做到月付的 60-70%，玩家提前锁进年付，抵御 D30 断崖和成本意识觉醒
  4. **永远不要把 token 成本可视化给玩家**
  5. **永远不要在账单日附近做运营触达**
- **⚠️ 最大的监管未知数**:**Garcia v. Character Technologies**(2024 年 14 岁少年自杀案）的后续判决将改写行业责任边界

### 2026-04-13 · 模块 5 返回（跨品类启发）— "游戏性定义权脱离"

- **18 条可迁移矩阵**
- **Top 5 高可迁移性概念**:
  1. **对话即游戏**(Character.AI / 猫箱模式）
  2. **生成即抽卡**(Midjourney / Suno 模式）
  3. **AI NPC 主持人/裁判/叙事者**(Hidden Door)
  4. **广告即游戏** — Playable as Product(Catizen / Telegram Mini App)
  5. **Streak + 损失厌恶**(Duolingo）— 空白蓝海，零成本高 ROI
- **⭐⭐ 最锋利的跨品类洞察**:
  - Character.AI **日均时长 2 小时**、Midjourney 11 人 **$300M ARR**、Duolingo **1 亿 MAU** — **它们都不把自己叫游戏，但行为循环、compulsion loop、付费心理与游戏完全同构**
  - **"游戏性"的定义权已经从游戏行业手里脱离**
  - **未来最优形态可能根本不应该在 App Store 归类到 Games** — 用陪伴/工具/教育的壳包装游戏内核
  - **同时吃到**：订阅制 ARPU(3-5 倍 IAP)+ 绕开苹果税 + 绕开中国版号 + 监管红利
  - **中国豆包/猫箱/星野已经无意识实践这条路径，但没人做成方法论**

### ⭐ 全局闭环叙事（Phase 1 五模块已形成完整逻辑链）

```
定义(1.1) → "AI × 小游戏交集当前真空,经济学卡在 Token vs ARPDAU"
市场(1.2) → "AI 游戏融资 2023 峰值 $450M,2024 回落 30%,资金转向 B2B middleware"
平台(1.3) → "AI 税吞掉 15-40% ARPDAU,6 个大厂 AI Lab 浮现"
技术 GAP(3) → "18 条 GAP,S1 × 7,G06 token 倒挂是真空带的经济学根因"
心理(4) → "AI 游戏是情感 MMO 不是三消,传统 KPI 误导,grief 退坑新模式"
跨品类(5) → "游戏性定义权脱离,最优形态是把游戏核藏进陪伴/工具/教育的壳"
```

这 5 个模块形成了一个**完整的经济-技术-心理闭环**:
- **为什么 AI × 小游戏现在不成立**(1.1 + 1.3 + 3)
- **什么情况下会成立**(3 → 端侧小模型 / middleware)
- **如果要赌，该怎么赌**(4 + 5 → 情感 MMO 思维 + 游戏壳下的非游戏定义）

这条叙事将直接成为模块 06 机会地图的核心骨架。

### 2026-04-13 · 模块 2.1 返回（中国市场产品）— 版号扭曲洞察

- **27 个中国 AI 游戏 / 小游戏案例**（远超目标 20)
- **💥 核心洞察："游戏性定义权脱离" 在中国被版号监管结构性强化**
  - 真正的 AI-native 游戏**必须伪装成陪伴/小说/剧场**才能活
  - 星野 / 猫箱 / 筑梦岛 **全部不在游戏分类下架**
  - **蔡浩宇把 Anuttacon 团队注册美国是同一逻辑的另一面**
  - 和美国"自发偏离"不同，这是**监管 + 情感消费 + 女性三四线用户** 共同制造的**结构性扭曲**
- **关键案例与数字**:
  - **星野 2024 流水 > 3 亿**(MiniMax),**付费率仅 3-5%**，头部用户 **月付 ¥1000+**
  - **猫箱 DAU 破百万**（字节），**已并入"豆包家族"而非游戏事业群**（战略信号）
  - **Whispers from the Star**(Anuttacon）— **团队注册美国规避版号**
  - **寻道大千**（三七互娱 2024 微信 Top 1）— **AI 仅用于买量素材**，验证了 1.2 "TOP 零 AI-native" 判断
  - **逆水寒 AI NPC**（网易）— **移除 AI 后仍是完整 MMO**，玩家 10 万条对话后发现 NPC 只会反刍设定，**反面印证 G01/G04**
- **这个中国版洞察补强了 Phase 1 的主命题**:AI × 小游戏交集真空不只是经济学原因，还有**监管/文化原因**
- 这 8-10 条洞察点将成为模块 06 "D. 战略视角" 中"中国市场特殊性" 板块的核心

### 2026-04-13 · 模块 2.2 返回（美国市场）— 退出模式浮现

- 32 行产品案例，50+ 来源，覆盖 AI-native 游戏 + AI 陪伴 + middleware + AAA 尝试
- **💥 2024-2025 两大退出事件**（赛道顶部准出口）：
  - **Character.AI → Google $2.7B 授权**(2024.08）— Shazeer + De Freitas 回流 Google,28M MAU 但 Token vs ARPDAU 跑不通，a16z 实得**远低 10x**，是一个**失败的"成功退出"**
  - **Inflection → Microsoft $650M**(2024.03）— 同构的 reverse acqui-hire,Suleyman 带队加入 MS,**C 端陪伴独立上市路径正式关闭**
- **2024H2 死亡潮**:Fable pivot SHOW-1 / Faulty 关停 / Vibecheck 关停 / Artie 关停 / Dreamworld 丑闻坐实 / Latitude 萎缩
- **资本全面转向 B2B middleware**:Inworld / Rho / Artificial Agency / Convai
- **💥 美国 vs 中国两大结构性差异**:
  1. **Middleware 存在性**：美国已跑出 Inworld(~$500M 估值）等 B2B 中间层；**中国几乎空白**（仅 rct AI 转型）— 美国资本有"退而求其次"路径，中国没有
  2. **退出模式**：美国有 reverse acqui-hire(Google/Microsoft 买技术+人）；**中国头部绑定巨头内生，没有独立退出**（星野/猫箱没人能独立 IPO)
- **关键融资**:Hidden Door $20M(a16z 2023.06)/ Altera Project Sid $11M(a16z + Schmidt 2024.09)/ Series AI Rho $28M(Bitkraft 2023.11)/ AI Dungeon Latitude $3.3M(2021 NSFW 事件后萎缩）
- **Suck Up!** 是**解题范式代表**:< 5 人小团队，2024.01 Steam 爆款，LLM 对话说服 NPC — 证明"小而美 + buy-out 付费"是现阶段能跑通的形态
- **Infinite Craft** 是**反例范式**:Neal Agarwal solo 零融资，Poki 现象级数千万玩家，证明 **"AI 在广告支持的小游戏里也能跑"但需要极简玩法 + 低频调用**

### 2026-04-13 · 模块 2.3 返回（日韩市场）— 日韩完全不同的画像

- 27 案例 / JP 14 + KR 17 条来源 / 严格按路径写入 ✅
- **💥 Krafton MOGIA + inZOI "Smart Zoi"**(2025.03 EA)= **东亚大厂第一个把 AI NPC 作为"用户可见卖点"商业化上线**
  - 底层**与 Inworld 深度绑定**(Krafton 是 Inworld 战略投资人）
  - 这是 Phase 2 唯一的"大厂 AI-native 成功案例"
- **日本 AAA 清一色"内部工具化"**:Square Enix AI Division / Capcom CEDEC / Bandai Namco 专利 / Konami 贴图 AI — 全部不对外营销，**Portopia AI Demo 翻车让业界对日式 LLM 游戏信心受挫**
- **💥 日韩 AI 陪伴分化**（非常有趣的对比）：
  - **日本**:Cotomo / Rinna 半年下滑 DAU ~10 万 → **被 VTuber + Galgame 挤占**（文化替代品效应）
  - **韩国**:ScatterLab Zeta(2024)MAU **数百万**,Character.AI 韩国 Top 5 流量国 → **被 K-drama IP + 语言封闭市场托举**
- **🎯 "雷声大雨点小" 的精准解释**:
  - **日本**：不是"雷声大"，是"**应该大却哑火**" — VN 土壤被作者性 + IP 法务锁死，VTuber 生态挤占 AI 陪伴位置，AAA 只做内部工具
  - **韩国**：是"**雷声大雨将落**" — 4 大 Lab(MOGIA / VARCO / Nexon Intelligence Labs / Smilegate AI)+ 底座 LLM 自研全到位，但 2026 前仅 inZOI + Zeta 两个商业验证，**2026-2027 才是爆款窗口期**
- **给模块 06 的直接输入**：日本是**反面案例**（文化结构阻止 AI-native 生成），韩国是**延后爆款**（窗口期可等），中美是**当前主战场**

---

## ⭐⭐ Phase 1+2 全部完成 — 全局叙事已完整（8 个模块，39 个子文件）

### 全球版图（四大市场画像）

| 市场 | 状态 | 关键特征 |
|---|---|---|
| **美国** | 主战场，退出模式已浮现 | middleware + acqui-hire 路径闭环 / C 端独立 IPO 关闭 |
| **中国** | 主战场，但"游戏性"被版号扭曲 | 星野/猫箱全部藏在陪伴品类，量子绘梦跑美国 |
| **日本** | 应该大却哑火 | VN 土壤被作者性 + VTuber + IP 法务锁死 |
| **韩国** | 雷声大雨将落 | 4 大 Lab + 底座 LLM 全到位，2026-2027 爆发窗口 |

### 三大命题支柱（将驱动模块 06)

1. **经济学真空带**:AI × 小游戏现在不成立，Token/session $0.014 vs ARPDAU < $0.05，需端侧模型或平台补贴破局
2. **游戏性定义权脱离**：最优形态不是游戏，而是把游戏核藏进陪伴/工具/教育的壳（全球趋势 + 中国版号强化）
3. **退出模式分化**：美国 reverse acqui-hire / 中国巨头绑定 / 韩国延后爆发 / 日本基本不退出

### 驱动模块 06 的基础已经齐全，现在进入 Phase 3 整合阶段

---

### 2026-04-13 · ⚠️ Scope 重大调整（研究中期发现新物种）

**触发**：用户提到 Rezona 和 LoopIt 两个产品名，WebSearch 后发现它们都是 **MWM.ai 2025 年的"AI UGC Playable Maker"新物种**，同时发现 **YouTube Playables Builder**(Google 官方 2024-2025 发布）也在同一赛道。

### 发现的新品类：**"Pipeline AI × UGC Feed" / "AI UGC Playable Maker"**

**核心特征**:
- 用户用 **AI 生成 playable**(text prompt → AI → mini-game)
- **AI 只在创作时被调用一次**(Pipeline AI)
- 玩家消费**静态生成结果**（无 Runtime AI 成本）
- **TikTok 式 feed 分发 + 一键 remix** 形成飞轮
- 玩家 = 创作者

**核心玩家**:
- **Rezona / LoopIt**(MWM.ai，法国）
- **YouTube Playables Builder**(Google 2024-2025)⭐ 最重要新发现
- **Upit / Ludo.ai / Jabali.ai / Rosebud / Websim / Replit**

**与原研究命题的关系**:

这个发现**修正了"AI × 小游戏真空带"的原命题**:

- **原命题**:"AI × 小游戏的交集是真空带"（因为 Runtime AI 成本 > IAA ARPDAU)
- **修订后**:"**Runtime AI × IAA 小游戏** 是真空带，但 **Pipeline AI × UGC Feed** 是正在兴起的破局路径"
- **Pipeline AI 路径**可能是未来 2-3 年最真实的 AI × 小游戏赛道
- 原来的 Scenario A/B/C/D 四条破局路径基础上，**新增 Scenario E (Pipeline AI × UGC Feed)**，是最彻底的解（Runtime 成本 = 0)

### 4 个调整动作已执行

1. **✅ 模块 2.4 追加 Scenario E** — 完整一节对比 A/B/C/D/E 五条路径，5x5 矩阵
2. **🟡 新派 sub-agent 做模块 2.5** — UGC AI Playable Maker 独立深度章节（agent `ac58a` 后台运行中，目标 15+ 产品案例）
3. **✅ 模块 1.1 追加"双刀分类"** — 在原"AI 可移除性"刀之上加第二把刀"AI 存在位置"，得到四象限：Runtime AI-native / Runtime AI-augmented / Pipeline AI Static / AI-free
4. **✅ PROGRESS.md 记录本次 scope 调整** — 本节

### 新的主命题（修订版）

> **AI × 小游戏赛道的核心张力是 "Runtime AI vs Pipeline AI" 的选择 — Runtime 路径被 Token 经济学卡死（真空带），而 Pipeline 路径（通过 Rezona / LoopIt / YouTube Playables Builder 等 2025 新物种）正在打开"AI 生成玩法 + UGC 飞轮分发"的新子赛道，可能是未来 2-3 年最真实的赛道入口。**

### 2026-04-13 · 模块 2.5 返回（Generative Playable Feed / GPF）— 最锋利的新品类定义

- **品类精确命名：Generative Playable Feed(GPF)** — 三词缺一不可：Generative（创作端 AI)+ Playable（可互动产物）+ Feed(TikTok 式消费端）
- **5200 字 + 19 个产品编号 + 五节结构完整**
- **Pipeline AI 经济学公式**:
  - AI 只在**创作时调用**，消费端零 AI 成本
  - 单次生成 **$0.1-0.5**
  - **creator:consumer ≥ 1:100 才成立**（新指标）
  - 消费端用广告/订阅支撑
- **MWM.ai 公司背景**:2021 C 轮 $50M(Blisce 领投）/ ~200 员工 / 音乐 SaaS 转型 AI 游戏
- **MWM 双品牌战略**(Rezona + LoopIt 不是 A/B test，是两个方向）：
  - **Rezona** = "有目标的 meme 游戏"
  - **LoopIt** = "无目标互动玩具"
- **YouTube Playables Builder 是平台级降维打击**:YouTube 2B+ MAU + Gemini 成本优势
- **Roblox 是品类最强潜在玩家**:~80M MAU + 2024 Roblox Assistant，正在自我 AI 化
- **⭐ 对主命题的意义（最重要）**:GPF 是**目前观察到唯一同时解决三大痛点的品类**:
  1. Token 经济学（Pipeline AI 摊薄）
  2. 内容枯竭（UGC feed 无限供给）
  3. 冷启动（remix 继承）
- **12-24 个月窗口期** → 之后可能被 YouTube/TikTok 平台化吃掉，**独立公司要快**
- **最大 gap**:MAU/DAU/留存/eCPM 全部黑箱，**经济学目前是假设不是结论**
- **中国市场 gap**：字节豆包 + 即梦 + 抖音小游戏合并、腾讯微信策略 无公开 confirmed 产品，只能从招聘/专利侧面验证

### ⭐ 全局命题更新（Scope 调整后的最终版本）

研究的主命题从"AI × 小游戏是真空带"修正为：

> **"Runtime AI × 小游戏是真空带（Token 经济学卡死），但 Generative Playable Feed(GPF）子品类正在用 Pipeline AI + UGC 飞轮打破它 — 窗口期 12-24 个月，之后被 YouTube/TikTok/Roblox 平台化吃掉。"**

这个命题和 Phase 1-2 的所有发现完全兼容，而且更完整：
- 模块 1.1 "AI 可移除性刀" + "AI 存在位置刀" = GPF 是 "AI-native + Pipeline" 象限
- 模块 1.2 "AI-native 融资 2023 峰值 $450M / 2024 回落 30%" → 资金正在从 Runtime 转向 Pipeline
- 模块 1.3 "AI 税 15-40% ARPDAU" → GPF 用 Pipeline 把 AI 税归零
- 模块 3 "G06 Token 倒挂" → GPF 是唯一不受 G06 影响的形态
- 模块 4 "情感 MMO 5-10% 玩家" → GPF 是"情感 MMO 的对立面"，服务 95% 轻度用户
- 模块 5 "游戏性定义权脱离" → GPF 是定义权脱离的终极形态 ("做 playable 但不叫游戏")

这个命题将是**模块 06 机会地图的第一主线**。

### 2026-04-13 · 模块 1.4 玩家全景图返回（92 家 × 15 列 Excel)

- **92 个玩家**(85 主扫描 + 2.5 占位 + 1 监管）
- **Excel 格式**：带双刀色块 / 冻结表头 / 自动筛选
- **国家分布**：中国 27 / 美国 32 / 日本 13 / 韩国 14 / 欧洲 3 / 政策 1
- **刀 1 分布**:AI-native 45 · AI-augmented 14 · AI-washed 13 · Enabler 17 · AI-free 3
- **刀 2 分布**:Runtime 42 · Pipeline-Dev 26 · Pipeline-Creator 7 · Pipeline-Embedded 3 · Hybrid 5 · None 8
- **状态分布**：跑通 6 / 增长 22 / 稳 24 / 早期 14 / 警告压力 10 / 死亡退出 11

### ⭐⭐⭐ 最关键 3 个发现（直接驱动模块 06)

1. **"跑通比例" 只有 6/85 ≈ 7%** — 星野 / Character.AI（准退出）/ Zeta / Inworld / 猫箱 / 寻道大千，整个赛道仍在**高度不确定期**
2. **赛道两端分化**:
   - **一端**:Krafton MOGIA / inZOI 这种 AAA Runtime AI **首次实测跑通**
   - **另一端**:Hidden Door / AI Dungeon / Character.AI **中型创业公司集体失血**
3. **💥💥💥 中国 Pipeline-Creator 象限零玩家** — 腾讯/字节只做底层 SDK,**没有终端 Creator 工具**,**12-24 个月内有被 MWM / Replit / YouTube Playables 先发占位的风险**

### 红海 vs 空白象限（四象限判断）

- **最红海**:
  - **AI-native × Runtime**(42 家，正在淘汰）
  - **Enabler × Pipeline-Dev middleware**(17 家但 B 端付费个位数）
- **最空白**:
  - **Enabler × Pipeline-Creator**（全球仅 7 家）— **与 1.1 §6 "Pipeline AI × UGC Feed 是真正破局路径"判断完全一致**

### 给模块 06 的三条黄金线索（驱动产品 / 投资 / 战略视角）

1. **产品视角 (A)**：做 **"中国版 Rezona / LoopIt"** — Pipeline-Creator 象限的中国机会，需要快（12-24 个月），需要结合抖音/小红书/微信生态
2. **投资视角 (B)**:**Enabler × Pipeline-Creator 是全球最空白的象限**(7 家），2025-2026 这 2 年窗口期 — 这是 T-1 投资主题（游戏 AI middleware）的升级版，从 "for Dev" 转向 "for Creator"
3. **战略视角 (D)**:**字节 / 腾讯必须立即入场 Pipeline-Creator**，否则会被 MWM / YouTube Playables Builder 抢中国市场 — 国内小游戏平台如果错过这个窗口，就是给全球平台送入场券

---

## 方案变更记录

- **2026-04-13**:brainstorming 完成。对齐 "交集" 方向 / "全都要" 四视角 / L2 深度 / 方案 B 五模块结构 / 并行 + Gemini 兜底 / 中美双中心 Tier 1。

---

## 下一步

1. 写 methodology.md + glossary.md（主 agent,2 分钟）
2. 写 gemini_fallback.py（主 agent,5 分钟）
3. 复用既有工具链（symlink 或复制 scripts/,2 分钟）
4. 派第一批 6 个 Claude sub-agents（模块 1.1/1.2/1.3/3/4/5)
5. Monitor 盯，卡住派 Gemini 兜底
