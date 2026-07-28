# PROJECT.md — 个人成长工作台（长期记忆）

> 本文件是项目的**唯一长期记忆**。任何重要修改完成后，都必须同步更新本文件以及对应的 README / VISION / TODO / CHANGELOG / AI_RULES。
> 新会话（或上下文被重置、出现「400 input length too long」）时，**先读这 6 份文档**，再开始任何工作。
> 🤖 **AI 接管入口**：任何新 AI 接手本项目前，必须先读 **`PROJECT_BOOTSTRAP.md`**（唯一入口，禁止依赖聊天记录）。

---

## 1. 产品定位

**个人成长工作台（Growth Workbench）** 是一款**移动端优先的个人成长操作系统（Personal Growth OS）**：把「学习 / 财富 / 身体 / 自媒体」四大成长维度整合进一个 App，并用**本地规则型 AI** 做复盘、计划与建议，帮助用户获得更多人生选择权。

- 用户画像：非程序员的电商运营从业者，正在学习用 AI 解决实际问题、开发自己的产品。
- 形态：**纯前端单文件 PWA**，可安装到手机桌面、可离线使用，零后端依赖。
- 核心理念：数据归用户自己所有（localStorage 本地存储），AI 在端侧做轻量辅助，不依赖联网大模型。

---

## 2. 当前版本

| 项 | 值 |
| --- | --- |
| 当前版本号 | `1.3.3`（运行时版本源 `version.json`；v1.2.0 Decision Engine；v1.2.1 财富 SSOT/英语换一篇/交易编辑删除；v1.2.2 学习历史点击回看；v1.3.1 学习引擎基础 Learning Foundation（Library + LearningSource + 学习历史升级 + 英语读 Library + AI 工具学习中心 AIToolMod）；**v1.3.2 AI 工具课程模板标准化（统一 6 段行动化模板，11 个真实工具去百科化）**；**v1.3.3 Project 学习引擎基础（ProjectLibrary + ProjectEngine，进度/下一步自动计算，创建前可预览调整）**） |
| 最近一次提交 | `feat: v1.3.3 Project Learning Foundation (ProjectLibrary + ProjectEngine)` |
| 发布状态 | 已部署 GitHub Pages，PWA 已可用 |
| 版本标签规范 | 正式发版使用 `v1.0`、`v1.1`、`v2.0` …（见第 13 节） |

---

## 3. 页面结构（6 个底部标签）

| 标签 | key | 主要负责模块 | 核心功能 |
| --- | --- | --- | --- |
| 🏠 今日 | `today` | `Pages.today` + `TodayAgent` | **AI CEO Dashboard（Today OS）**：欢迎区、今日三件、财富/学习/身体/自媒体摘要、今日最大风险与机会、复盘提醒 |
| 📚 学习 | `learn` | `Pages.learn` + `EnglishMod` | 学习记录（主题/分类/来源/理解度/产出）、英语模块（生成/测验/词库） |
| 💰 财富 | `wealth` | `Pages.wealth` | 资产、交易、财富快照、图表（环形/折线/柱状）、AI 财富复盘 |
| 🏃 身体 | `body` | `Pages.body` | 运动记录、体重/围度等身体指标、图表、AI 身体报告 |
| 📱 自媒体 | `content` | `Pages.content` | 内容数据（阅读/赞/藏/评/转/涨粉）、图表、AI 选题建议 |
| 👤 我的 | `profile` | `Pages.profile` | 个人资料、长期目标、兴趣、项目、自我分析、设置、数据导入导出 |

路由基于 `hash`（`#today` / `#learn` …），由 `App` 模块统一调度。

---

## 4. 技术栈

| 维度 | 方案 |
| --- | --- |
| 语言 | 原生 HTML + CSS + JavaScript（ES5/ES6 混用，兼容移动端 WebView） |
| 框架 | **无框架、无构建步骤、零运行时依赖** |
| 数据持久化 | `localStorage`（不可用时回退到内存） |
| 模块化 | 挂在 `window` 上的 IIFE 模块：`U` `S` `Charts` `AI` `EnglishMod` `Library` `LearningSource` `Pages` `App` `ProjectLibrary` `ProjectEngine` |
| 图表 | 手写 SVG：`Charts.donut` / `Charts.line` / `Charts.bar` |
| AI | **规则型本地「模拟 AI」**，非联网大模型（`AI.*` 为本地启发式函数） |
| PWA | `manifest.json` + `sw.js`（离线缓存外壳）、maskable 图标、iOS 启动图 |
| 托管 | GitHub Pages（main 分支根目录，HTTPS，push 自动部署） |

**重要约束**：AI 相关功能（见第 8 节）目前全部是**本地规则**，不调用任何外部大模型 API。

---

## 5. 文件结构

```
/workspace
├── index.html              # 整个应用（约 3500+ 行，内联全部 CSS/JS）
├── manifest.json           # PWA 清单（名称/图标/主题色/启动方式）
├── sw.js                   # Service Worker（离线缓存 + 导航网络优先回退）
├── version.json            # 版本号（当前 1.3.1，运行时版本检测源）
├── icon-192.png            # PWA 图标 192
├── icon-512.png            # PWA 图标 512
├── icon-maskable-512.png   # 可遮罩图标（Android 安全区）
├── icon-1024.png           # 1024 高清明信片主图标（深蓝+白+绿）
├── apple-touch-icon.png    # iOS 主屏图标
├── splash-*.png            # 7 张 iOS 启动图（不同分辨率）
├── .gitignore
├── README.md               # 项目说明
├── PROJECT.md              # 本文件（长期记忆）
├── VISION.md               # 产品愿景
├── TODO.md                 # 需求池（P0/P1/P2）
├── CHANGELOG.md            # 版本记录
└── AI_RULES.md             # AI 开发规范
```

> 注意：`index.html` 是**单文件自包含**——所有 CSS、JS、数据种子都内联其中。`sw.js` 仅缓存静态外壳（其中 `index.html` 含全部逻辑），因此缓存它即可离线运行。

---

## 6. 数据结构（localStorage）

| 键 | 用途 |
| --- | --- |
| `pgwb_data_v1` | 全部业务数据（JSON） |
| `pgwb_settings_v1` | 设置项单独冗余存储（JSON，便于合并） |

`pgwb_data_v1` 的数据形状（`S.defaults()` 种子）：

- **profile**：`{ name, longTermGoals[], interests[], background, contentPositioning, availableTime }`
- **settings**：`{ theme: 'light'|'dark', baseCurrency: 'CNY', fx: {USD,HKD,JPY}, remindReview: bool }`
- **dailyPlans**：`{}`（按日期字符串为键）
- **learning[]**：`{ id, date, topic, category, source, summary, notes, understanding, output }`
- **projects[]**：`{ id, name, goal, stage, progress, nextAction, notes, versions[], aiChats[], stages[]:{id,name,steps[]:{id,title,doneCriteria,estTime,done}}, sourceType, libraryId, templateName, resources[], pitfalls[], currentStage }`（v1.3.3 起 `stages` 存在时进度/下一步自动计算，旧项目无 `stages` 沿用原手工字段）
- **assets[]**：`{ id, name, symbol, category, currency, quantity, currentPrice, targetAllocation }`
- **transactions[]**：`{ id, date, asset, type, quantity, price, fee, exchangeRate, amount, reason, decisionType, risk }`
- **wealthSnapshots[]**：`{ id, date, totalAssets, investmentValue, cashValue, savingsContribution, investmentReturn, dividendIncome, fxImpact }`
- **exercises[]**：`{ id, date, type, duration, intensity, bodyParts[], feeling, notes }`
- **weights[]**：`{ id, date, weight, waist, hip, thigh, bodyFat, sleep, bodyState, notes }`
- **contents[]**：`{ id, date, title, topic, type, status, views, likes, saves, comments, shares, followersGained, notes }`
- **reviews[]**：`{ id, date, whatLearned, whatCompleted, whatProduced, whatToImprove, tomorrowPlan }`
- **selfAnalyses[]**：`[]`（AI 自我分析沉淀）
- **vocabBank[]**：`[]`（英语词库）

> **数据安全约束**：`pgwb_data_v1` 的顶层键集合与字段结构，属于稳定的**数据契约**。新增字段可向后兼容；**删除 / 重命名字段、改变嵌套结构** 属于破坏性变更，须经产品确认并在 CHANGELOG 记录、提供迁移逻辑（见 AI_RULES 第 4 条）。

---

## 7. 各模块公开能力（便于二次开发检索）

| 模块 | 公开方法 / 字段 |
| --- | --- |
| `U`（工具） | `todayStr` `addDays` `uid` `toast` …（日期、ID、提示等通用工具） |
| `S`（数据层） | `load` `save` `data` `setData` `add` `update` `find` `has` `length` `reset` `exportJSON` `importJSON` `restoreFromBackup` |
| `Charts` | `donut(cfg)` `line(cfg)` `bar(cfg)`（手写 SVG） |
| `AI`（本地规则） | `generateTodayPlan` `selfAnalysis` `wealthReview` `bodyReport` `parseExercise` `checkSentence` `genContentIdeas` `generateEnglish` |
| `EnglishMod` | `open(lesson, opts)` `openQuiz` `openBankQuiz`（v1.3.1：`open` 支持 `opts.prefill` 回填复述、`opts.updateId` 继续学习更新原记录） |
| `Library` | `register` `registerAll` `get` `all` `byCategory` `findByTitle` `search` `categories`（v1.3.1 学习对象统一注册中心：英语 8 篇 / AI 工具 11 个 / 产品 2 篇） |
| `LearningSource` | `addSource` `load` `LocalSource` `RemoteSource`（v1.3.1 数据源抽象：内置 LocalSource 聚合进 Library；`RemoteSource` 为 V1.3.2 联网预留，当前返回空） |
| `AIToolMod` | `open(tool, opts)` `scoreQuiz(tool)`（v1.3.2 统一课程模板渲染器：`open` 用固定 6 段模板（是什么/核心能力/实战案例/实际操作/今日任务/小测验）渲染任意工具课，支持 `opts.prefill`/`opts.updateId` 回填与续学；`scoreQuiz` 批改单选测验） |
| `ProjectLibrary` | `match(name)` `get(id)` `all()`（v1.3.3 本地项目知识库：内置 5 套模板，按关键词/子串模糊匹配，未命中回退通用模板；无联网/无 AI/无 LLM） |
| `ProjectEngine` | `buildDraft(name,tpl)` `compute(p)` `recompute(p)` `create(draft)`（v1.3.3 项目路线自动生成器：深拷贝模板生成草稿，自动计算进度/下一步/当前阶段并落库） |
| `Pages` | `today` `learn` `wealth` `body` `content` `profile`（各页渲染器） |
| `TodayAgent` | `getDashboard` / `regen`（首页聚合入口；**不再自行生成建议**，改为调用 `RuleEngine.getSuggestions()` 取 Top3；各维度汇总文案仍由 Study/Wealth/Fitness/Media Agent 提供） |
| `RuleEngine` | `getSuggestions()`（**唯一决策中心**：聚合 5 个 Rule 的 `Suggestion[]`，按 priority 降序、estimatedTime 升序排序后输出） |
| `StudyRule` | `evaluate(d)` → `Suggestion[]`（学习间隔 ≥2 天未学习 → action p5） |
| `WealthRule` | `evaluate(d)` → `Suggestion[]`（现金/货基占比超配 → risk p4；资产快照 >30 天未更新 → action p3；常驻机会 p3） |
| `FitnessRule` | `evaluate(d)` → `Suggestion[]`（运动间隔 ≥3 天 → action p5；体重连升 3 次 → action p4；常驻机会 p3） |
| `MediaRule` | `evaluate(d)` → `Suggestion[]`（发布间隔 ≥3 天 → action p4；复盘间隔 ≥7 天 → risk p4；常驻机会 p3） |
| `FutureRule` | `evaluate(d)` → `Suggestion[]`（占位空桩，预留未来真实投资/职业等高级规则） |
| `App` | 路由器（hash 路由 + `refresh()` 刷新当前页） |

---

## 8. AI 能力说明（关键）

`AI` 模块是**本地规则引擎**，不联网、不调用大模型。当前能力：

- `AI.generateTodayPlan` — 根据资料/目标生成今日计划草稿
- `AI.selfAnalysis` — 基于 `selfAnalyses` 做自我分析
- `AI.wealthReview` — 财富复盘（资产/交易/快照）
- `AI.bodyReport` — 身体报告（运动/体重）
- `AI.parseExercise` — 解析自然语言运动输入
- `AI.checkSentence` — 英语句子检查
- `AI.genContentIdeas` — 生成自媒体选题
- `AI.generateEnglish` — 英语生成（从 `Library` 的 `en` 类别取课文，配合 `EnglishMod`；不再直接依赖 EN_LIB）
- `AIToolMod`（v1.3.1 新增，AI 工具学习中心查看器）：渲染真实 AI 工具的完整课程（教程/案例/练习/测验）并记录学习，属于内容/UI 模块，不调用大模型。

> 若未来要接入**真实大模型 API**，属于重大架构变更：需新增后端代理（避免在前端暴露密钥）、定义调用边界、保持离线降级，并在 AI_RULES 中记录规范。**当前严禁在前端硬编码任何 API Key。**

> **Prompt 管理**：所有 AI Prompt 已从代码中独立，统一维护在 `docs/Prompt/`（`PromptGuide.md` 定义规范，各模块一个文件）。未来接入真实模型时，Prompt 从此目录读取，不在 `index.html` 写死。

---

## 9. 已完成功能（截至 `d98691c`）

- [x] 单文件应用骨架 + 6 标签移动端布局（明/暗主题）
- [x] 数据层 `S`：localStorage 持久化 + 种子数据 + CRUD + 导入导出 + 重置
- [x] 今日：每日计划、AI 今日计划、复盘
- [x] 学习：学习记录（分类/理解度/产出）+ 英语模块（生成/测验/词库）
- [x] 财富：资产、交易、财富快照、环形/折线/柱状图、AI 财富复盘
- [x] 身体：运动记录、身体指标、图表、AI 身体报告
- [x] 自媒体：内容数据追踪、图表、AI 选题
- [x] 我的：资料、长期目标、项目、自我分析、设置（主题/币种/汇率）、数据导入导出
- [x] PWA：manifest + Service Worker 离线 + 图标（192/512/maskable/1024）+ iOS 启动图
- [x] GitHub Pages 部署（main 根目录，HTTPS）
- [x] 版本自动检测与「发现新版本」弹窗 + PWA `skipWaiting` 更新流（v1.0.0）
- [x] AI Prompt 管理体系（`docs/Prompt/`，9 个文件 + `PromptGuide.md` 规范）
- [x] Today OS 首页架构（v1.1.0）：`TodayAgent` 汇总 + `StudyAgent`/`WealthAgent`/`FitnessAgent`/`MediaAgent` 桩，9 段式 AI CEO Dashboard（Mock/真实摘要混合）
- [x] Decision Engine 决策引擎（v1.2.0）：`RuleEngine` 成为**唯一决策中心**，`TodayAgent` 改为只调用 `RuleEngine.getSuggestions()`；`StudyRule`/`WealthRule`/`FitnessRule`/`MediaRule` 基于真实数据缺口产出 `Suggestion[]`，`FutureRule` 为占位空桩；详见 `docs/Architecture/DecisionEngine.md`
- [x] 财富数据单一数据源 SSOT（v1.2.1 / BUG-001）：`S.wealthTotal()` 统一首页 / TodayAgent / 财富页 / RuleEngine / WealthAgent 的当前总资产读数
- [x] 英语「换一篇」真正切换（v1.2.1 / BUG-002）
- [x] 交易记录编辑与删除（v1.2.1 / IMP-001，复用现有 UI 与数据契约）
- [x] 学习历史点击回看（v1.2.2）：历史记录可点击恢复完整内容；英语匹配 EN_LIB 复原文章/单词/语法/测验，其它类别恢复已存摘要/笔记/产出
- [x] 学习引擎基础 Learning Foundation（v1.3.1）：新增 `Library` 学习对象统一注册中心 + `LearningSource` 数据源抽象（内置 LocalSource 含 英语8篇 / AI工具11个真实工具 / 产品2篇，**不再写死 4 篇**；`RemoteSource` 为 V1.3.2 联网预留）；英语模块改为读取 `Library`（不再直接依赖 EN_LIB）；学习历史升级「查看历史笔记 / 继续学习 / 重新学习」，记录可完整恢复；保留数据契约 `pgwb_data_v1` 不变
- [x] AI 工具学习中心（v1.3.1）：AI 页从抽象的「生成今日 AI 学习任务」表单重构为真实工具学习中心，内置 11 个真实 AI 工具（Claude Code / Cursor / WorkBuddy / ChatGPT / Gemini CLI / Codex / Windsurf / MCP / A2A / n8n / Dify）的完整课程（是什么/适合解决什么问题/核心能力/常见使用场景/基础教程/实际案例/今日练习/小测验），点击工具卡片或「今日推荐」即可学→做→测并标记已学；删除旧的 `genAiTask`/`aiPrefillFromLib` 抽象表单
- [x] AI 工具课程模板标准化（v1.3.2）：所有 AI 工具统一 6 段固定模板（是什么/核心能力/实战案例/实际操作/今日任务/小测验），由 `AIToolMod.open` 固定渲染；11 个真实工具课程行动化重写（去百科化），实战案例与分步操作可照做，今日任务为当天可完成的小任务。

---

- [x] Project 学习引擎基础（v1.3.3）：新增 `ProjectLibrary`（本地项目知识库，5 套模板：个人 AI 工作台 / 小红书账号 / 淘宝自动化 / 个人网站 / 通用兜底，含阶段与步骤的完成标准与预计耗时、推荐资料、踩坑提示）+ `ProjectEngine`（基于模板自动生成完整项目路线）；项目进度与下一步改为自动计算（已完成步骤数/总步骤数），取消手工填写百分比；创建前可预览并自由新增/删除/修改/重排阶段与步骤；旧项目（无 `stages`）沿用原手工编辑与进度字段，数据契约完全向后兼容；新增架构文档 `docs/Architecture/ProjectFoundation.md`。

## 10. 已知 Bug / 待确认

| 状态 | 说明 |
| --- | --- |
| ⚠️ | `/__backup`（云端备份）后端不存在，`S.backupToCloud` / `restoreFromBackup` 会静默失败，仅影响云端同步，不影响本地使用 |
| ⚠️ | 种子数据含示例资产/交易/内容，首次使用需用户自行清空或覆盖 |
| 🔍 | iOS 启动图在不同机型 safe area 适配待真机验证 |

---

## 11. UI 设计规范（不可擅自修改）

- 设计系统使用 CSS 变量（`:root` 与 `[data-theme="dark"]`）定义颜色/间距/圆角/阴影。
- 主色为**深蓝 + 少量绿色 + 白**；图标 `icon-1024.png` 为深蓝圆角矩形 + 白色上箭头 + 绿色点。
- 移动端优先：底部 6 标签导航，单列卡片流。
- 任何配色、间距、动画、交互的改动都属于「UI 变更」，须经确认（见 AI_RULES 第 3 条）。

---

## 12. 后续开发路线（Roadmap）

1. **v1.0（已达成）**：文档体系 + 版本自动检测与 PWA 更新流（见 v1.0.0）。下一步：数据契约冻结。
2. **v1.1（已达成）**：Today OS 首页架构（v1.1.0）+ Decision Engine 决策引擎（v1.2.0）、财富 SSOT / 英语换一篇 / 交易编辑（v1.2.1）、学习历史点击回看（v1.2.2）。
3. **v1.3（收尾）**：学习引擎基础 Learning Foundation（v1.3.1 已落地：LearningLibrary + LearningSource + 学习历史升级 + 英语读 Library + AI 工具学习中心 AIToolMod）；**v1.3.2 已落地：AI 工具课程模板标准化**——所有 AI 工具统一 6 段固定模板、行动化重写（去百科化），新增工具只填同一组字段即可复用模板；**联网 AI 学习（`RemoteSource` 真实课文源）顺延至后续版本**，不在本版本实现联网、不改动数据契约；**v1.3.3 已落地：Project 学习引擎基础（ProjectLibrary + ProjectEngine，进度/下一步自动计算，创建前预览可调）**。
4. **v2.0（愿景）**：「AI Personal CEO」——端侧 AI 自动串联四大维度，给出每日优先级与行动建议。详见 VISION.md。

---

## 13. Commit / 版本规范（摘要，详见 AI_RULES.md）

- Commit 类型前缀：`feat` / `fix` / `refactor` / `docs` / `style` / `perf`。
- 正式发版打 tag：`v1.0`、`v1.1`、`v2.0` …；当前开发态 `version.json` 为 `dev`。
- 每次功能完成：改代码 → 自测 → **更新 PROJECT/CHANGELOG/TODO** → commit → push → 汇报。

---

## 14. 新会话恢复流程（必读）

当出现以下任一情况：**上下文被重置 / 模型提示「400 input length too long」/ 开启新聊天**，请按顺序执行：

1. 首先阅读项目唯一入口 **`PROJECT_BOOTSTRAP.md`**，按其规定的「AI 接管流程」完成接管（其内已包含完整文档清单与代码扫描步骤）。
2. 运行 `git log --oneline -10` 与 `git status` 确认当前代码与未提交改动。
3. 确认本次任务范围（是否允许改 UI/数据契约）。
4. 按 AI_RULES 的「开发流程」执行，完成后同步更新文档再提交。

## 15. AI Prompt 管理体系（docs/Prompt/）

- 所有 AI Prompt 已从代码中独立，统一维护在 **`docs/Prompt/`** 目录（规范见 `docs/Prompt/PromptGuide.md`）。
- 规范：`PromptGuide.md` 定义统一模板（Role / Goal / Context / Input / Constraints / Output）与命名/新增规则；`AI.md` 为总体行为规范。
- 模块文件：`Home` / `Study` / `Wealth` / `Fitness` / `Media` / `Review`（对应六大业务模块），`Development.md` 为开发类 Prompt。
- 现状：当前 `AI.*` 为本地规则；未来接入真实模型时，Prompt 从此目录读取，不在 `index.html` 写死。
- 维护：新增/调整 Prompt 改 `docs/Prompt/` 文件并同步 `CHANGELOG.md`，**不修改业务代码**（见 `AI_RULES.md`）。

## 16. AI 接管入口（PROJECT_BOOTSTRAP.md）

- **唯一入口**：`PROJECT_BOOTSTRAP.md` 是整个项目面向 AI 的单一接管入口。任何新 AI（WorkBuddy / Claude / GPT / Gemini / Cursor / Codex 等）开始工作前必须先读它，禁止依赖聊天记录。
- 它统管：接管流程、开发原则、文档维护、Git 工作流、AI 行为规范、输出规范、新聊天规范、长期维护原则（共 9 节）。
- 本文（`PROJECT.md`）是「长期记忆」，负责沉淀细节；`PROJECT_BOOTSTRAP.md` 是「入口与流程」，负责引导接管。两者配合。
- 若新增文档 / 修改规范 / 调整 Git 或 Prompt 管理，必须同步更新 `PROJECT_BOOTSTRAP.md`（见其第 9 节）。
