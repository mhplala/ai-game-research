# 06C. 行业趋势判断 — 给行业从业者 / 观察者 / 媒体人的深度观察

> **视角**：游戏公司中层 / 市场营销人 / 媒体人 / 研究员 / 独立观察者
> **核心问题**:"这个赛道到底在发生什么？我怎么跟上？"
> **最后更新**:2026-04-13

---

## 0. TL;DR（给行业从业者的 30 秒版本）

**一句话判断**:

> **"2022-2024 是 AI 游戏的第一次泡沫 + 破灭，2024H2 资本集体从 C 端 AI-native 转向 B2B middleware 和 GPF 新物种。未来 24 个月的主线不是'更好的 AI 陪伴'，而是'Pipeline AI + UGC Feed' 破 Token 经济学真空带。"**

---

## 1. 赛道演变时间线（2022-2026)

```
2022 春   ChatGPT 3.5 发布 → AI 游戏 "首次觉醒"
          AI Dungeon (2019) 从 GPT-2 升级到 GPT-3.5

2022 秋   Character.AI 上线(Shazeer + De Freitas 从 Google 出走)
          AI 陪伴品类正式成立

2023 春   Inflection / Character.AI 大额融资
          a16z / Bitkraft 密集下注

2023 夏   Inworld AI $50M+ → 估值 $500M+,AAA 合作起来
          Hidden Door $20M Series A(a16z)
          Altera $11M(a16z + Eric Schmidt)

2023 秋   VC AI-native 游戏年累计融资 ~$450M(峰值)

2024 初   AI Dungeon 萎缩 / Suck Up! 独立爆款 / 1001 Nights / Infinite Craft
          独立开发者模式浮现,与 VC 模式分化

2024.03   ⭐ Inflection → Microsoft $650M(reverse acqui-hire 第一例)
          Suleyman 带队加入 MS

2024.08   ⭐ Character.AI → Google $2.7B 技术授权
          Shazeer + De Freitas 回流 Google
          a16z 实得远低 10x(赛道顶部退出信号)

2024 Q3-Q4  死亡潮:Fable / Faulty / Vibecheck / Artie / Dreamworld / Latitude 萎缩
          VC 全面转向 B2B middleware

2024 H2   Krafton MOGIA 成立(2024.06)
          NCSoft VARCO / Nexon Intelligence Labs 加码

2025.01   Steam AI 内容披露政策发布
          AI 披露游戏从 1000 款涨到 8000+

2025.03   ⭐ Krafton inZOI Smart Zoi EA 发布(东亚首个 AAA Runtime AI)

2025.08   ⭐ Anuttacon Whispers from the Star Steam 发布
          中国首个挂"游戏"名的 AI-native(团队注册美国)

2025 Q3-Q4  ⭐ Rezona(MWM.ai)/ LoopIt 发布 / YouTube Playables Builder
          GPF(Generative Playable Feed)新物种浮现

2025.11   Whispers from the Star iOS 上线

2026 ?     GPF 第一波洗牌?中国版 GPF 能否出现?
          Apple Intelligence SDK 进一步开放?
          YouTube Playables Builder 平台化?
```

---

## 2. 三大行业级趋势

### T1. 从 "自己淘金" 到 "卖铲子给淘金者"

**2022-2023**：大家都下场做 AI-native C 端游戏（AI Dungeon / Character.AI / Hidden Door / Fable / Altera / Latitude)

**2024 H2 拐点**:C 端陪伴天花板被 Character.AI $2.7B 定义（a16z 远低 10x 回报）+ C 端游戏死亡潮（Fable / Faulty / Vibecheck / Artie / Dreamworld)

**2025**：资本集体转向 **B2B middleware**(Inworld / Convai / Rho Series AI / Rosebud / Kinetix / Scenario)

**意义**：这是一个典型的 "**淘金热 → 卖铲子**" 周期。中国市场还没完成这个转向（Pipeline-Dev 象限除了 rct AI 几乎空白），**有 1-2 年窗口做中国版 Inworld**。

### T2. "游戏性定义权脱离"

**现象**:Character.AI / Replika / 猫箱 / 星野 / Duolingo Max / Midjourney Discord — 这些产品都**不把自己叫游戏**，但用户行为（日均时长 / 付费心理 / compulsion loop）与游戏完全同构。

**原因**:
- **绕苹果税**：非游戏类目分成 15% vs 游戏类目 30%
- **绕中国版号**：游戏需要版号，陪伴/工具不需要（虽然 AI 备案变严）
- **订阅制 ARPU 高**：订阅比 IAP 高 3-5 倍（Replika Pro Churn < 3%)
- **规避游戏监管风险**：欧盟 AI Act / 中国未成年人保护法等对游戏更严

**意义**:"**游戏性的定义权已经从游戏行业脱离**"（模块 5 的锋利判断）。未来 2-3 年，很多最赚钱的"准游戏"产品将正式拒绝"游戏" 标签。

### T3. Pipeline AI × UGC 浮现为 "真空带" 的正确答案

**现象**(2025 年）：
- **Rezona** / **LoopIt**(MWM.ai)/ **YouTube Playables Builder**(Google)/ **Upit** / **Jabali.ai** / **Rosebud AI** / **Websim** — 一整批产品**在同一个时间点**出现
- 它们都是 "**用户用 AI 生成 playable → TikTok 式 feed 消费 → 一键 remix**" 的同构模型

**精确命名**（来自模块 2.5):**Generative Playable Feed(GPF)**
- **Generative**（创作端 AI)
- **Playable**（可互动产物）
- **Feed**(TikTok 式消费端）

**经济学机制**:
- AI 只在创作时调用一次（~$0.1-0.5），静态化
- 玩家玩 100 次不用再调 AI(Runtime 成本 = 0)
- TikTok 式 feed 让 CAC 趋零（UGC 飞轮）
- **根本性绕过 Token 经济学真空带**

**意义**：这可能是 **"AI × 小游戏" 真空带的唯一正确答案**。

---

## 3. 行业"炒概念" vs "真趋势" 辨别清单

| 概念 | 判定 | 理由 |
|---|---|---|
| **"AI 驱动的 NPC 革命 AAA"** | 炒作 | 逆水寒 AI NPC 反面案例：10 万条对话后发现反刍设定；除 inZOI 外没有明星产品 |
| **"AI 女友会取代真人"** | 炒作 | Character.AI 天花板 $2.7B = a16z 远低 10x，纯 C 端陪伴已证伪 |
| **"AI 生成内容会让游戏开发白菜价"** | 半炒半真 | Pipeline-Dev 工具真实降成本，但还不足以颠覆 AAA 开发成本结构 |
| **"Token 成本明年会降 10 倍"** | **有据** | GPT-4o → GPT-4o mini 一年降了 10 倍，仍在继续 |
| **"端侧小模型会破真空带"** | **有据但早** | Apple Intelligence / Qwen 3B / Phi-4-mini 在路上，2026 H2 成熟 |
| **"UGC playable 是 AI 时代的 Roblox"** | **强判断** | 2025 年 Rezona/LoopIt/YouTube PB 同时冒出不是巧合 |
| **"Hidden Door 那种 AI 多人 RP 有大市场"** | 炒作 | Hidden Door 2025 Q1 传缩编，a16z $20M 烧完后方向不清 |
| **"Inworld middleware 稳赢"** | 半真 | 估值 $500M 但客户深度有限，Krafton 是唯一 AAA 成功案例 |
| **"Character.AI 被 Google 收购等于胜利"** | **错** | reverse acqui-hire 是失败的"成功退出"，老股东亏钱 |

---

## 4. 行业洗牌：谁在赢 / 谁在输 / 谁在观望

### 正在赢（2024-2025)

1. **Inworld AI** — middleware 领跑，Krafton 投资，AAA 客户
2. **Character.AI** — 28M MAU 峰值然后卖给 Google（表面赢，实质出局）
3. **星野**(MiniMax）— 中国 AI 陪伴跑通，2024 流水 > 3 亿
4. **猫箱**（字节）— DAU 百万，归属豆包家族
5. **Krafton MOGIA + inZOI Smart Zoi** — 东亚大厂唯一 Runtime AI 首次跑通
6. **Suck Up!**(Proxima Enterprises）— 独立爆款，< 5 人团队，Steam 买断 $9.99
7. **Infinite Craft**(Neal Agarwal）— solo 零融资 Poki 现象级
8. **Rezona / LoopIt**(MWM.ai）— GPF 新品类定义者之一
9. **YouTube Playables Builder**(Google）— 平台级降维打击的潜在赢家

### 正在输（2024-2025)

1. **AI Dungeon / Latitude** — 2021 NSFW 事件后萎缩，GenAI 游戏鼻祖掉队
2. **Hidden Door** — $20M 烧后 2025 Q1 传缩编
3. **Fable / Faulty / Vibecheck / Artie / Dreamworld** — 2024H2 死亡潮
4. **Inflection / Pi** — $1.3B 估值 → $650M 卖给 MS，不是胜利是失败
5. **逆水寒 AI NPC**（网易）— AI-washed 的反面案例，被玩家识破
6. **Glow**(MiniMax 前身）— 下架，中国 AI 陪伴鼻祖
7. **日本 Cotomo / Rinna** — 被 VTuber 挤占，半年下滑 DAU ~10 万
8. **字节 PICO 嘘嘘岛** — 停摆

### 正在观望 / 延后爆发

1. **NCSoft VARCO / Nexon Intelligence Labs / Smilegate FutureLab AI** — 4 大韩国 Lab 但 2026-2027 才爆
2. **Square Enix / Capcom / Bandai Namco** — 日本 AAA 内部工具化，不对外
3. **字节跳动（PICO / 抖音小游戏 AI)** — 大象缓慢转身
4. **腾讯 Hunyuan Game** — Lab 状态，没有明星产品
5. **Meta Horizon AI** — VR + AI 但 VR 本身不火
6. **米哈游 Anuttacon** — Whispers from the Star 2025.11 刚出，评估中
7. **Apple Intelligence 游戏应用** — 待 SDK 开放

### 新物种（最值得关注）

1. **Rezona**(MWM.ai）— "最离谱的 meme 游戏平台",iOS+Android
2. **LoopIt**(MWM.ai）— "触感互动玩具"
3. **YouTube Playables Builder**(Google）— 平台级
4. **Upit** — Build games with AI
5. **Rosebud AI** — no-code 游戏生成
6. **Jabali.ai** — Africa 团队的 AI 游戏创作工具
7. **Websim** — browser-native AI 生成

---

## 5. 行业内部的 4 个反直觉事实

### 反直觉 1：玩家心理瓶颈比技术瓶颈更严重

**数据**:Replika Pro Churn < 3%/月（接近 Netflix）但**退坑的最强触发器不是无聊**，是 "**人格漂移**" 导致的 **grief（哀伤）反应**（模块 4.4)

**意义**:A/B 测试 / filter 更新 / 上下文截断在 AI 游戏里是**有毒的** — 传统互联网实验文化需要被**抛弃**。大厂的产品文化必须改变才能做好 AI 游戏。

### 反直觉 2：纯陪伴 LTV 天花板只有 $20-40

**数据**:Character.AI $2.7B 谷歌授权，但 a16z 实得远低 10x,MAU 28M 但转化不够

**意义**:"AI 陪伴"作为独立商业模式**存在天花板**，除非转型为 B2B(middleware 路径）或进入情感 MMO 小众（5-10% 付费）模式。

### 反直觉 3:AI 游戏的留存曲线不是"三消曲线"

**数据**:AI 游戏 D1/D7 高（新奇感），但 D7-D30 断崖式下跌，D30 之后**反而高于传统小游戏**（筛选出的情感投入用户）

**意义**:**传统 D1/D7 KPI 会系统性误导 AI 游戏产品决策**。AI 游戏应该用 D30/D90 作为主 KPI。

### 反直觉 4：中国的"版号压力"意外成为 GPF 的催化剂

**数据**：量子绘梦 Anuttacon 团队注册美国 / 星野 / 猫箱 / 筑梦岛 全部不在游戏分类下

**意义**:**中国版号制度倒逼了"游戏性定义权脱离"** — 这是中国独有的"监管反向助推创新"模式。GPF 在中国的最终形态可能是"**一个不自称游戏的 AI 生成 playable 平台**"，反而因此绕开版号。

---

## 6. 给行业媒体 / 研究员的 5 条"追什么"建议

### 1. **Token 经济学** 是唯一真正重要的数字

别的指标都是干扰。盯紧 GPT-4o-mini / Gemini Flash / Claude Haiku 的 pricing 变化，每次下降都会打开一个子赛道。

### 2. **GPF 窗口期**(12-24 个月）

Rezona / LoopIt / YouTube Playables Builder / Upit 的月活 / 留存 / 商业化数据如果 2026 年底之前没出来，这个赛道就是泡沫。

### 3. **中国版号和 AI 备案** 的具体政策演变

2024 年 AI 备案制度开始严格执行，但 "AI 游戏" 的边界还没划清。任何 AI 游戏公司都受这个影响。

### 4. **Apple Intelligence SDK 对游戏开发者的开放**

这是"端侧小模型 × 小游戏"的关键时间节点。iOS 游戏 + Apple Intelligence 可能是 2026 的大事件。

### 5. **Krafton MOGIA + inZOI Smart Zoi 的商业验证**

它是东亚唯一跑通 Runtime AI AAA 的案例。2026 年 EA 阶段的用户反馈 / 数据 / 销量将决定这条路径是否可复制。

---

## 7. 本赛道的 3 个"假命题" 警示

### 假命题 1:"AI 会让游戏开发成本降 10 倍"

**真相**:AI 降的是**美术素材 / 对话脚本 / 买量创意**成本（Pipeline-Dev），但游戏开发的**设计 / 代码 / 运营** 成本没降。顶级游戏（原神 / GTA）的 AI 含量仍然极低。

### 假命题 2:"AI 陪伴会颠覆人类关系"

**真相**:Character.AI / Replika 的用户自述**都很清楚 AI 是 AI**，他们要的不是真人替代，而是"**无压力、低门槛、随时在线**"的互动对象。这和"人际替代论"完全不同。

### 假命题 3:"AI 游戏会把小游戏开发变成人人可做"

**真相**:GPF(Rezona/LoopIt) 做的是**简单 playable**，不是完整游戏。想做真游戏还是需要专业开发者。GPF 更接近"**AI 时代的表情包 meme**"，而不是"AI 时代的 Unity"。

---

## 8. 本赛道的 2 个"真命题" 判断

### 真命题 1:"未来 2 年，AI 游戏的主角不是 C 端游戏本身，是 B2B 工具 + GPF 新物种"

**证据**:
- 资本从 C 端转向 B2B（模块 1.2:2024 AI-native 融资回落 30%,middleware 崛起）
- GPF 新物种 2025 Q3-Q4 集中涌现（模块 2.5)
- Character.AI / Inflection 两个头部 C 端退出定义天花板

### 真命题 2:"中国的 AI 游戏创新会通过'不叫游戏'的产品实现"

**证据**:
- 星野 / 猫箱 / 筑梦岛 全部藏在陪伴品类
- Anuttacon 团队注册美国
- 版号制度 + 情感消费 + 女性三四线用户 = 独特的扭曲力
- 中国 GPF 版如果出现，一定不叫游戏，叫"AI 创作玩具"或"AI 互动 meme"或类似

---

## 9. 来源与引用

本文件综合 Phase 1-3 的全部模块，特别重引用：
- 模块 1.1 AI 可移除性刀 + AI 存在位置双刀分类
- 模块 1.2 市场规模 / 融资曲线
- 模块 1.4 玩家全景图 92 家 / 双刀象限统计
- 模块 2.1-2.3 中美日韩区域差异
- 模块 2.4 跨区域综合 5 条迁移路径
- 模块 2.5 GPF 新品类定义
- 模块 3 18 条 GAP 清单
- 模块 4 玩家心理学反直觉洞察
- 模块 5 游戏性定义权脱离
- PROGRESS.md 全局闭环叙事

---

## 10. Gaps（行业观察的盲区）

1. **中国大厂内部 AI 游戏 R&D 进展** — 字节 / 腾讯 / 米哈游的真实内部数据
2. **Apple Intelligence SDK 的游戏开放时间表**
3. **YouTube Playables Builder 的实际用户量**
4. **日本 Galgame 中型厂商的 AI 动作**(Marvelous / FuRyu / Key / Visual Arts)
5. **印度 / 东南亚 / 拉美** 市场的 AI 游戏动作（本研究只覆盖中美日韩欧）
6. **Character.AI → Google 授权** 后 a16z 实际回报倍数
7. **端侧小模型**的性能 benchmark（在真实游戏 session 中的表现）

---

**本文件与 A 产品机会 / B 投资机会 / D 战略进入路径 互补，共同构成模块 06 的四视角整合。**
