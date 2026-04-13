# 06D. 战略进入路径 — 给大厂 / 平台 / 战投的路线图

> **视角**：大厂（腾讯 / 字节 / 阿里 / 米哈游 / 网易 / Krafton / Google / Meta / Microsoft）、平台方、战投部、新业务负责人
> **核心问题**:"我们公司 / 平台应该如何布局 AI 小游戏与 playable 体验赛道？"
> **最后更新**:2026-04-13

---

## 0. TL;DR（给 CEO 的 30 秒版本）

**一句话判断**:

> **"不要自己做 AI 游戏。做 GPF 创作工具 + 投资 middleware + 补贴 Token — 这三件事是未来 24 个月大厂在这个赛道应该做的全部事情。"**

**三条战略路径优先级**:

| 路径 | 推荐度 | 时间窗 | 成本 | 回报 |
|---|---|---|---|---|
| **S1. 做 Generative Playable Feed 创作工具** | ⭐⭐⭐⭐⭐ | 12-24 个月窗口 | 中（50-200 人团队） | 新子赛道所有权 |
| **S2. 补贴 Token 养生态** | ⭐⭐⭐⭐ | 已在发生 | 高（10 亿级年度补贴）| 生态占位 |
| **S3. 投资 / 收购 middleware** | ⭐⭐⭐⭐ | 2024-2026 窗口 | 中（战投级） | 技术 / 人才 / 退出通道 |
| **S4. AAA Runtime AI 合作 / 授权** | ⭐⭐⭐ | 长期 | 中高 | 品牌 + 技术护城河 |
| **S5. 自己做 AI-native C 端产品** | ⭐ | 随时 | 低 | **高风险低回报，不推荐** |

---

## 1. 核心战略判断（引用修订后主命题）

> **"Runtime AI × 小游戏是真空带（Token 经济学卡死），但 Generative Playable Feed(GPF）子品类正在用 Pipeline AI + UGC 飞轮打破它 — 窗口期 12-24 个月，之后被 YouTube / TikTok / Roblox 平台化吃掉。"**

### 这个判断对大厂意味着什么

1. **不要自己下场做 AI-native C 端产品** — Character.AI $2.7B "准退出" 已经证明了 C 端独立天花板
2. **GPF 窗口期极短**(12-24 个月）— 慢了就被 MWM / YouTube / Roblox 抢走中国市场
3. **Pipeline-Creator 象限全球仅 7 家**（模块 1.4 数据）— **中国零玩家**
4. **模块 1.1 双刀分类**给了清晰的战略坐标：不要做 "Runtime AI × IAA 小游戏"（真空），要做 "Pipeline AI × UGC"（蓝海）

---

## 2. 五条战略路径详细拆解

### S1. 做 Generative Playable Feed 创作工具 ⭐⭐⭐⭐⭐ 最强推荐

**逻辑**：中国 Pipeline-Creator 象限零玩家，这是**全球最空白的单一象限**。MWM.ai（法国）+ YouTube Playables Builder(Google)+ Upit / Jabali / Rosebud（美国）都在抢这个位置，中国必须在 12-24 个月内入场。

**核心产品形态**:
- **Text-to-playable 移动 App**（对标 Rezona / LoopIt)
- 用户输入"一个吃糖果的狐狸被捕"→ AI 生成可玩的 mini game → 一键发布 → TikTok 式 feed 消费
- 内置 remix 机制：看到别人的作品 → 点击 "remix" → 修改一行 prompt → 变成自己的

**谁最适合做**:

| 候选 | 优势 | 障碍 | 推荐度 |
|---|---|---|---|
| **字节跳动** | 抖音分发 + 豆包 Token 免费 + 即梦生成 + TikTok 海外协同 | 内部 BU 协同困难 | ⭐⭐⭐⭐⭐ 最优 |
| **腾讯** | 微信 / QQ / 视频号分发 + 混元模型 + 小游戏原生生态 | 内部创新抑制文化 | ⭐⭐⭐⭐ 强 |
| **快手** | 可灵模型领先 + 短视频二级平台 | 小游戏规模小 | ⭐⭐⭐ 中 |
| **小红书** | UGC 社区文化 + 女性用户密度 | 技术能力不足 | ⭐⭐⭐ 中 |
| **B 站** | 创作者生态 + Z 世代 | 无模型能力 | ⭐⭐ 弱 |
| **米哈游** | 美术 / 叙事品味 + 资金充裕 | 没有分发平台 | ⭐⭐ 弱 |

**推荐战略**:**字节跳动立即立项，用"豆包 + 即梦 + 抖音"三合一**做中国版 GPF，目标 2025 Q4 MVP 上线，2026 Q2 冲 500 万 MAU,2026 年内被抖音买量生态吸纳。

**与现有业务的关系**:
- **抖音小游戏**:GPF 不是小游戏的竞争者，是**小游戏的上游工具**（用 GPF 生成的作品，最好的那些可以孵化成正式小游戏）
- **豆包**:GPF 本身就是豆包的一个游戏化 vertical
- **即梦**：即梦负责视觉层，GPF 负责 playable 层
- **TikTok**:GPF 可以先在抖音冷启动，再用 TikTok 全球化

**ROI 估算（3 年）**:
- 成本：50-200 人团队 × 3 年 = **3-10 亿人民币**
- 回报：如果拿下 Pipeline-Creator 中国市场 80%+，就是 **"下一个 Roblox" 级别** 的战略资产

### S2. 补贴 Token 养生态 ⭐⭐⭐⭐ （已在发生，需持续）

**逻辑**:Token 经济学真空带的直接破法之一是平台方用**补贴**把 AI 税归零。豆包免费 Token 给抖音小游戏开发者 / 腾讯 Hunyuan 免费给微信小游戏开发者 / 快手可灵给视频化游戏开发者，**三家已在各自赛道执行**。

**战略价值**:
- 构建**开发者生态依赖**，未来哪怕模型能力被追上，生态锁定已形成
- 对标**抖音当年补贴短视频创作者**的路径
- 补贴让原本经济学不成立的"AI × 小游戏" 暂时可行，等端侧小模型成熟后顺势过渡

**建议**:
- **维持**目前的 Token 补贴策略，延长到 2027 年
- **透明化补贴规则**，吸引更多独立开发者
- **和 S1(GPF 创作工具）结合**，补贴作为 GPF 内置技术

**风险**:
- 如果补贴停（被财务砍），整个生态崩塌
- 财务上需要战略耐心

### S3. 投资 / 收购 middleware ⭐⭐⭐⭐

**逻辑**:2024H2 全球资本已经从 C 端 AI 游戏转向 B2B middleware(Inworld 估值 $500M / Rho $28M Series A / Convai / Rosebud）。中国大厂应该：

1. **投资美国 middleware**：腾讯投资部 / 字节跳动战投对 **Inworld / Convai / Kinetix** 下注，拿到技术 + 人才接触
2. **孵化中国 middleware**：中国 Pipeline-Dev 象限只有 rct AI 在转型，**可以孵化 2-3 家中国 Inworld 版**
3. **和 Krafton MOGIA 学习**:Krafton 把自己变成 Inworld 的"中国出口"，这个路径对腾讯 / 米哈游都开放

**最值得收购或投资的标的**:
- **Inworld AI**($500M，美国）— 技术 + AAA 客户 + 中国市场准入
- **Convai**（美国）— NPC API 简化版
- **rct AI / Chaos Box**（中国，转型中）— 中国稀缺的本土 middleware
- **Kinetix**（法国）— AI 动作生成

### S4. AAA Runtime AI 合作 / 授权 ⭐⭐⭐

**逻辑**:Krafton MOGIA 与 Inworld 的合作（inZOI Smart Zoi 2025.03 EA）证明了"**AAA × middleware**" 模式可行。中国 AAA 大厂（米哈游 / 腾讯 / 网易）可以：

1. **和 Inworld / Convai 合作**，为旗下 AAA 游戏（原神 / 逆水寒 / PUBG 等）加 AI NPC
2. **学习 Krafton**，投资 Inworld 拿到优先权
3. **自研小型 Runtime AI 能力**（米哈游可能已经在做）

**避免的坑**:
- **不要做"AI NPC"PR 式项目**（逆水寒反面案例：玩家 10 万条对话后发现 NPC 只会反刍设定）
- **要做就做到 inZOI 的水准**，真正让玩家"看得出 AI 的价值"

### S5. 自己做 AI-native C 端产品 ⭐(**不推荐**)

**为什么不推荐**:
- Character.AI $2.7B "准退出" 证明 C 端独立天花板 $20-40 LTV
- 纯 C 端 AI 陪伴 2024H2 死亡潮（Fable / Faulty / Vibecheck / Dreamworld)
- 大厂做 C 端 AI 游戏只会是"AI-washed"（逆水寒模式），浪费资源
- **情感 MMO 5-10% 付费玩家**的运营，大厂的组织不擅长（需要小团队 / 用户社区 / 内容运营文化）

**唯一的例外**:**米哈游 Anuttacon**（蔡浩宇分拆出去的独立工作室 / 注册美国规避版号）— 这种分拆模式可能是大厂的唯一做 AI-native 的正确方式。

---

## 3. 分公司战略建议

### 字节跳动

**推荐路径**:S1(GPF 创作工具） + S2（豆包补贴） 并行 + S3（投资 Inworld 或中国 middleware) + 维持猫箱现状

**具体动作**:
1. **立项"抖音版 Rezona"**（内部 codename GPF-CN),2025 Q4 MVP,2026 Q2 500 万 MAU
2. 豆包 Token 对游戏开发者**延长免费 tokens** 至 2027
3. 战投部评估 Inworld / Rosebud / Convai 投资机会
4. PICO "嘘嘘岛"停摆不再复活（模块 2.1 已标注死亡）
5. **猫箱保持陪伴品类定位**，不转游戏事业群（目前做法正确）

### 腾讯

**推荐路径**:S1(GPF × 微信/视频号） + S4(Hunyuan Game 和 AAA 合作） + S3（投资 middleware)

**具体动作**:
1. **微信小游戏 Team 立项 GPF**，基于混元 + 微信社交图谱 + 视频号分发
2. Hunyuan Game 从"自研游戏" 转向"给腾讯游戏 AAA 做 NPC 能力"（参考 Inworld 模式）
3. 腾讯投资 / IEG 战投关注 Inworld / Rho / Convai
4. **天美 / 光子**不应自己做 AI 游戏，而是和 Hunyuan Game 内部合作

### 米哈游

**推荐路径**：维持 Anuttacon 分拆 + S4（和 Inworld 合作 for 原神）

**具体动作**:
1. **Anuttacon 继续独立运营**（注册美国策略正确）
2. **原神 / 星穹铁道内的 AI NPC** 应与 Inworld 合作，不自研
3. **不要做 C 端 AI 陪伴独立品牌**（米哈游没有社区运营基因）
4. **Whispers from the Star 2025.11 iOS 上线是关键里程碑**，决定 Anuttacon 继续投入还是转型

### 网易

**推荐路径**:S4(AAA 合作 / 授权）+ 小心做 S5

**具体动作**:
1. **承认逆水寒 AI NPC 是失败案例**，停止作为 PR 亮点
2. 和 Inworld / Convai 深度合作做下一代 AI NPC
3. 评估 NetEase Team Miaozi 的 Inworld 合作是否可以扩展
4. **不要再做"AI-washed" AAA** 了

### Krafton（韩国）

**推荐路径**：延续 MOGIA + 授权出海 + 孵化 2-3 个 AI game studio

**具体动作**:
1. MOGIA 继续深化，2026 推第二款 Runtime AI 游戏
2. 基于 inZOI Smart Zoi 的经验做**"AI NPC 技术授权"** 给其他大厂
3. 孵化 2-3 个**"MOGIA × 美国中间层"** 的跨国合作产品

### Google

**推荐路径**:YouTube Playables Builder 继续深化 + Character.AI 整合 + Gemini 成本优势

**具体动作**:
1. **YouTube Playables Builder 是现阶段最重要的战略产品** — Google 在 Phase 2 研究中被低估，它可能是全球 GPF 赛道的最强玩家
2. **整合 Shazeer + De Freitas 团队** 做 Gemini Game（可能已在进行）
3. 用 Gemini 成本优势把 Token 打到 OpenAI / Anthropic 之下

---

## 4. 三大行动优先级（给战投部 / CEO)

### P0(2025 Q4 必须做）

1. **立项 GPF 创作工具**(S1）— 字节 / 腾讯 / 快手至少一家必须做，否则被 YouTube Playables Builder 抢走中国市场
2. **维持 Token 补贴生态**(S2）— 延长 2 年，作为 GPF 的底层基础设施
3. **战投部立即开始跟 Inworld / Convai / Rosebud / Kinetix 谈**(S3)

### P1(2026 H1 应该做）

4. **AAA 合作试点**(S4）— 腾讯 / 米哈游 / 网易 的下一代 AAA 至少选 1 款做 Runtime AI 合作
5. **孵化 2-3 家中国 middleware**(S3 扩展）— 字节 / 腾讯投资部拨出 5000 万人民币基金
6. **现有 AI 陪伴产品保持陪伴定位**（猫箱 / 星野）— 不要转"游戏"

### P2(2026 H2 - 2027)

7. **GPF 从中国到全球** — 通过 TikTok 海外扩张
8. **自研 middleware**（字节 / 腾讯）— 如果 S3 投资无法完成
9. **端侧小模型游戏化**（跟 Apple / Google / Qualcomm 合作）— Apple Intelligence 到位后

---

## 5. 组织能力匹配

### 做 GPF(S1）需要什么样的组织

| 能力 | 必须 | 对标 |
|---|---|---|
| **产品 / 创作者社区运营** | 必须 | 字节 TikTok / Roblox |
| **LLM / 生成式 AI 工程** | 必须 | 需要 20+ 工程师 |
| **移动端高性能游戏引擎** | 必须 | WebGPU / Unity / Godot |
| **TikTok 式 feed 算法** | 必须 | 字节 / 快手已有 |
| **Remix / UGC 工具链** | 新能力 | Roblox Studio / Figma 模板 |
| **创作者激励 / 分成体系** | 必须 | Roblox / YouTube |

**结论**:**只有字节跳动完整具备所有能力**，其他家缺 1-2 项但可以补。

### 做 middleware(S3/S4）需要什么样的组织

- **B2B 销售能力**（中国大厂普遍弱）
- **与国际 AAA 建立客户关系**
- **开源社区运营**(Inworld 部分开源）
- **SDK 文档 / 开发者布道**

**结论**:**中国大厂都缺 B2B 销售文化**，自建 middleware 很难。**投资美国 middleware 反而是更好的路径**。

---

## 6. 风险与规避

| 风险 | 规避 |
|---|---|
| **GPF 窗口期关闭**（被 MWM/YouTube 抢走）| S1 必须 2025 Q4 前立项 |
| **Token 补贴不可持续**（财务压力）| 每年滚动评估 + 结合 S1 内生造血 |
| **middleware 投资泡沫**(2024H2 已过峰值）| 投资窗口关闭前完成 |
| **AAA 合作失败**（逆水寒教训）| 只做 inZOI 级的深度合作 |
| **自己做 C 端 AI 陪伴**(Character.AI 警示）| 除 Anuttacon 式分拆外不推荐 |
| **监管 / 版号风险** | GPF 定位在"创作工具" 而非"游戏" |
| **内部 BU 协同**（字节豆包 × 抖音小游戏） | CEO 直接汇报的新 BU |

---

## 7. 来源与引用

本文件主要引用自：
- 修订后主命题（PROGRESS.md 全局命题更新）
- 模块 1.4 玩家全景图（92 家，Pipeline-Creator 象限零中国玩家）
- 模块 2.4 五条迁移路径（Scenario A-E)
- 模块 2.5 GPF 品类定义
- 模块 3 18 条 GAP 清单（特别是 G06 Token 倒挂）
- 模块 4 玩家心理（情感 MMO 5-10% 付费）
- 模块 2.2 美国市场退出模式（Character.AI / Inflection)
- 模块 2.3 日韩市场（Krafton MOGIA 案例）

---

## 8. Gaps

1. **字节 / 腾讯 / 快手在 GPF 方向的内部动作**未公开确认，只能从招聘 / 专利 / 代码仓库侧面推测
2. **Inworld 估值和收购价**的真实区间未公开
3. **端侧小模型 + WebGPU** 的具体成熟时点（Apple Intelligence SDK 开放时间）未明
4. **YouTube Playables Builder 对中国市场是否开放**未明

---

**本文件是给大厂 / 平台 / 战投的战略路线图，与 A 产品机会 / B 投资机会 / C 行业趋势 互补，共同构成模块 06 的四视角整合。**
