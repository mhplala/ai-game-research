# 全局来源清单 — sources.md

> 所有模块引用的来源在此汇总。每个模块另有独立 `sources.md`。
> 格式:`[编号] 标题 | URL | 访问日期 | 类型 | 可信度`

## 可信度评级

- **高(H)**:Crunchbase / Dealroom / SteamDB / Data.ai / Sensor Tower / 官方融资公告 / 学术论文
- **中(M)**:TechCrunch / Game Developer / 游戏陀螺 / GameLook / 36Kr / 开发者官方 blog
- **低(L)**:Reddit / 小红书 / 知乎 / YouTube / Twitter anon

---

## 模块 00 — 方法论与术语
*待填*

## 模块 01 — 赛道现状与市场结构

### 1.3 来源
- 腾讯 2024 微信公开课 PRO / 小游戏专场(2024.01 + 2025.01)— 微信小游戏 MAU 500M+、2024 流水突破 400 亿元公开披露
- 腾讯 2024Q4 / 2025Q1 财报电话会 — Hunyuan Game 商业化进展
- 字节跳动巨量引擎《2024 小游戏行业白皮书》— 抖音小游戏流水 ~150 亿元,增速 +80%
- 火山引擎豆包大模型定价页 + 开发者文档(volcengine.com) — doubao-pro / doubao-lite 免费额度
- 快手 2024 光合创作者大会 — 快手小游戏与可灵 KLING 合作披露
- 支付宝开放平台小程序游戏类目规则 — 广告分成 70/30、通义千问接入
- 蚂蚁百灵大模型发布会(2024.09)
- Meta Quarterly Report Q4 2024 — Instant Games MAU 约 250M;Horizon Worlds AI 功能
- Poki 官网 About 页(poki.com/en/about)+ 2024 Poki for Developers 博客 — 100M MAU,50/50 收入分成
- Poki Labs 2025 Q1 "Playables Grant" 公告
- CrazyGames Developer Portal(developer.crazygames.com)— Happy Dev Program 70% 分成、AI Games 分类(2024)
- itch.io 分成规则页(itch.io/docs/creators/fees)— 默认 10% 可自设
- Steam AI 内容披露政策更新(Steamworks 博客 2024.01.10)— Pre-Generated / Live-Generated
- SteamDB / GameDiscoverCo 2025.12 AI 内容披露游戏累计数据(~8000+)
- Valve Steamworks SDK 2025 更新日志 — AI Content Disclosure API
- Epic Games Store Developer Program 分成政策(12%)
- Krafton 公告:MOGIA(2024.06)Generative AI Game Studio
- Nexon Intelligence Labs 博客(intelligencelabs.nexon.com)
- NCSoft VARCO LLM 发布(2023.08)+ Project G 更新
- 七麦数据 / DataEye / 点点数据 2024-2025 小游戏榜单 —《羊了个羊》《咸鱼之王》《无尽冬日》《抓大鹅》《疯狂梗传》流水与 DAU
- Suck Up! by Proxima — Steam 商店页 + SteamDB 销量估算(~50 万+)
- Infinite Craft by Neal Agarwal — Poki 上线数据 + 推特传播数据
- AI Roguelite — Steam 商店页(AI 生成剧情披露)
- Inworld Origins(2023)Steam demo 发布
- 1001 Nights(2024)AI 文字冒险 Steam 上架
- itch.io "AI Game Jam 2024" 参赛项目统计(1200+)
- Rosebud AI / Websim 2024 产品公告(与 CrazyGames 合作)

## 模块 02 — 产品与玩法前沿
*待 sub-agents 填充*

## 模块 03 — 技术栈与可行性 GAP

### 3 来源

**LLM / 模型能力与定价**
- Artificial Analysis LLM Benchmarks 2025(artificialanalysis.ai)— 延迟/成本/质量对比
- OpenAI 定价页(platform.openai.com/pricing)— GPT-4o / 4o-mini / Realtime API
- Anthropic 定价页(anthropic.com/pricing)— Claude 3.5 Sonnet / Haiku,prompt caching
- Google AI Studio 定价(ai.google.dev/pricing)— Gemini 2.5 Flash / Pro,2M context
- DeepSeek API 定价(api-docs.deepseek.com)— V3 / R1
- Meta Llama 3.1 技术报告(ai.meta.com/research)
- Epoch AI "Trends in Machine Learning"(epochai.org)— 模型价格下降曲线

**Diffusion / 美术**
- Black Forest Labs Flux.1 发布博客(blackforestlabs.ai, 2024.08)
- Stability AI SDXL / SD3 技术报告
- Replicate / Fal.ai 公开定价对比
- CivitAI LoRA 社区使用数据(2024–2025)
- Runway Gen-3 / OpenAI Sora / Luma Dream Machine / 快手可灵官方发布

**Voice / TTS**
- ElevenLabs Flash v2.5 发布(elevenlabs.io/blog, 2024)
- OpenAI Realtime API 发布(openai.com/blog, 2024.10)
- Kyutai Moshi 技术报告(2024.09)
- Sesame 发布(sesame.com, 2025)
- 火山引擎语音合成 / 腾讯云 TTS 定价页

**Agent / SDK / Middleware**
- Inworld AI 官方文档 + 2024.07 C 轮融资公告(5000 万美元)
- Convai 官网 + Unity Asset Store 列表
- rct AI 官网 + 公开访谈(36Kr / GameLook)
- Microsoft AutoGen GitHub repo
- LangChain / LangGraph 文档
- Anthropic Computer Use 发布(2024.10)

**渲染 / 前端**
- WebGPU Chrome 113 正式发布公告(chromestatus.com)
- Cocos Creator 3.8 发布说明 + 微信小游戏包体规范
- Unity WebGL 2023 LTS 文档
- PlayCanvas / Babylon.js / Three.js 官网

**玩家 / 开发者 / 投资人 / 大厂期待**
- Reddit r/AIDungeon / r/CharacterAI / r/SuckUpGame 评论采样(2024–2026)
- Steam 评论(Suck Up! / AI Roguelite / 1001 Nights)
- 小红书 "AI 女友"/"AI 恋爱" 标签定性采样
- TapTap《逆水寒》智能 NPC 评论
- a16z Games 博客 "Generative AI for Games"(2023)+ "The Creative Singularity"(2024)
- Bitkraft Ventures "AI Thesis"(2024)
- Makers Fund / Index Ventures 博客
- Brookings Institution "AI Companions" report(2024)
- 字节 GDC 2025 豆包演讲
- 腾讯 2024 微信公开课 + 混元接入元梦之星公告
- 米哈游 2024 年 AI 招聘 JD + HoYoverse AI 部门公开信息
- 网易伏羲实验室官网 + 《逆水寒手游》智能 NPC 发布(2023.07)
- Google DeepMind Genie(2024.02)/ Microsoft WHAM(2025)/ Sony Project GT AI(2024)

**案例 / 数据**
- Suck Up!(Proxima Enterprises)SteamDB + 2024 开发者访谈(LLM 成本披露)
- AI Dungeon(Latitude)历史融资 + 2023 收入披露
- Character.ai 被 Google "技术授权"收购(2024.08, 25 亿美元)
- Replika 用户调研(Brookings 2024)
- Volley / Hidden Door / Series AI 融资公告(TechCrunch / PitchBook)
- 字节跳动 2025 Q1 财报电话会(GenAI 研发提效 ~25%)

**可信度**
- 技术能力/定价:H(官方)
- 玩家评论:L
- 投资人博客 / 大厂招聘:M
- 未公开收入估算(Suck Up / AI Dungeon):M

## 模块 04 — 玩家行为与留存心理
*待 sub-agents 填充*

## 模块 05 — 跨品类启发
*待 sub-agents 填充*

## 模块 06 — 机会地图整合
*最终整合阶段填充*
