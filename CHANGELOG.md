# CHANGELOG.md — 版本记录

> 格式参考 [Keep a Changelog](https://keepachangelog.com/)。版本号规范：`v1.0` / `v1.1` / `v2.0` …；开发态 `version.json` 为 `dev`。
> 每次发版必须在此追加条目，并更新 PROJECT.md 第 2 节「当前版本」。

## [v1.3.2] - AI 工具课程模板标准化（行动化重构）

> 本版本目标重新定义为：不是增加更多 AI 工具，而是把「一个 AI 工具应该怎么学」这件事做好。所有 AI 工具统一采用同一套 6 段课程模板，后续扩展几十个工具都不会乱。

### Added
- **统一 AI 工具课程模板（6 段固定结构）**：所有 AI 工具（Claude Code / Cursor / WorkBuddy / ChatGPT / Gemini CLI / Codex / Windsurf / MCP / A2A / n8n / Dify）一律用同一套结构渲染——① 是什么（约 5%）② 核心能力（约 15%）③ 实战案例（约 30%）④ 实际操作（约 30%）⑤ 今日任务（约 10%）⑥ 小测验（约 10%）。模板由 `AIToolMod.open` 固定渲染，新增任何工具只需填同一组字段，结构不可能漂移。
- **`AIToolMod` 重写为固定模板渲染器**：课程 HTML 严格按 6 段生成（标注占比），`scoreQuiz` 批改单选测验、提交写入 `category:'ai'` 学习记录的逻辑保持不变；`open` 支持 `opts.prefill` / `opts.updateId` 回填与续学。
- **11 个工具课程全部行动化重写（去百科化）**：从「知道是什么」转向「会用」——实战案例改为真实可做的案例（如「用 Cursor 写网页 / 改 Bug / 重构 / 调试 / 接 MCP」），实际操作改为可照做的分步指引，今日任务改为一个当天就能完成的小任务（如「用 Cursor 创建一个 Hello World 页面」）。

### Changed
- **数据模型**：`BUILTIN_AI` 课程对象字段从百科式（what/capabilities/scenarios/tutorial/caseStudy/exercise）改为模板式（intro/problem/forWhom/caps[]/cases[]/steps[]/task/quiz[]）；与 `Library` 注册中心、`pgwb_data_v1` 数据契约无关，不影响用户已有学习记录。

### 约束遵守
- 未改动数据契约 `pgwb_data_v1`；未触碰 Planner / Project / Memory Engine、TodayAgent、RuleEngine、财富/身体/自媒体模块与 UI 风格；保持 localStorage 兼容、PWA 正常。
- 运行时版本 `version.json` → `1.3.2`。
- 提交：`feat: v1.3.2 AI tool course template standardized (action-oriented, fixed 6-part)`

## [v1.3.1] - 学习引擎基础 Learning Foundation

### Added（学习基础设施）
- **LearningLibrary（学习对象统一注册中心 `window.Library`）**：统一管理英语 / AI工具 / 产品 等学习对象，提供 `register` / `byCategory` / `findByTitle` / `search` / `categories` 等接口，为 V1.3.2（联网 AI 学习）预留统一扩展点。
- **LearningSource（数据源抽象 `window.LearningSource`）**：内置 `LocalSource` 聚合可扩展的本地内容（**英语 8 篇 / AI 工具 11 个真实工具（Claude Code / Cursor / WorkBuddy / ChatGPT / Gemini CLI / Codex / Windsurf / MCP / A2A / n8n / Dify）/ 产品 2 篇**，不再写死仅 4 篇英语）；`RemoteSource` 为 V1.3.2 联网预留（`load()` 当前返回空，不实现联网逻辑）。`App.load()` 启动时调用 `LearningSource.load()` 把内容灌入 `Library`。
- **英语模块重构读取 `Library`**：`AI.generateEnglish` / `AI.findEnglish` 改为从 `Library` 取课文（`category:'en'`），不再直接依赖 `EN_LIB`；英语课文统一迁移至 `LearningSource` 内置库。

- **AI 工具学习中心 `AIToolMod`（把 AI 模块做成真实工具课）**：AI 页从抽象的「生成今日 AI 学习任务」表单重构为真实工具学习中心——工具库网格展示 11 个真实 AI 工具（Claude Code / Cursor / WorkBuddy / ChatGPT / Gemini CLI / Codex / Windsurf / MCP / A2A / n8n / Dify），每个工具含完整课程（是什么 / 适合解决什么问题 / 核心能力 / 常见使用场景 / 基础教程 / 实际案例 / 今日练习 / 小测验）；点击工具卡片或「今日推荐」（按日期确定性选取）打开完整课程，做完练习、测完验即可一键「标记已学」并写入学习记录（`category:'ai'`）；学习历史的 AI 记录支持「继续学习 / 重新学习」回填到 `AIToolMod.open`。删除旧的 `genAiTask` / `aiPrefillFromLib` 表单逻辑。

### Changed
- **学习历史升级（查看历史笔记 / 继续学习 / 重新学习）**：`openLearnRecord` 弹出记录详情，可「继续学习」（回填历史笔记并 **更新原记录、保留原始日期**）或「重新学习」（全新状态、新增一条今日记录）；英语/AI 记录可完整恢复文章/单词/语法/测验与已存摘要/笔记/产出/理解度。`EnglishMod.open` 新增 `opts.prefill` / `opts.updateId` 支持回填与续学。

### 约束遵守
- 未改动数据契约 `pgwb_data_v1`；未触碰 Planner / Project / Memory Engine、TodayAgent、RuleEngine、财富/身体/自媒体模块与 UI 风格；保持 localStorage 兼容、PWA 正常。
- 运行时版本 `version.json` → `1.3.1`。
- 提交：`feat: v1.3.1 learning foundation (Library + LearningSource + history upgrade + AI tool learning center)`

## [v1.2.2] - 学习历史点击回看（当前版本）

### Fixed
- **学习历史点击无反应（实现遗漏）**：`historyView()` 历史卡片与「英语学习历史」列表新增 `data-learn`，点击调用 `openLearnRecord(id)`。
  - 英语记录：按 `topic` 匹配 `EN_LIB` 课文 → `EnglishMod.open()` 完整复原 **文章 / 重点单词 / 重要表达 / 语法 / 测验**；
  - 其它类别或英语未匹配到课文：弹出模态恢复该记录已保存的**摘要 / 笔记 / 产出 / 理解度**。
  - 复用现有 UI 与数据契约，未改动 `pgwb_data_v1`。

### Known Limitation（保留至 V1.3）
- **英语 `EN_LIB` 仍为静态库（4 篇）**：「换一篇」仅在库内随机切换，并非「更新学习内容」。新增真实课文源与 `Learning Engine` 属 V1.3 范围；按约定本版本不做联网或任何半成品方案。

### 其他
- 运行时版本 `version.json` → `1.2.2`。
- 提交：`fix: v1.2.2 learning history click-to-review`

## [v1.2.1] - 财富单一数据源 / 英语换一篇 / 交易编辑删除（当前版本）

### Fixed
- **BUG-001 财富模块单一数据源（SSOT）**：新增 `S.wealthTotal()` 作为「当前总资产」唯一来源；首页 `wealthSummary()`、`WealthAgent`、`WealthRule`、财富页 `totals()` 全部改为读取同一实时值。编辑资产后首页立即同步，不再依赖手动更新 `wealthSnapshots`。
- **BUG-002 英语「换一篇」无效**：`generateEnglish(force)` 现在真正响应 `force` 参数，在未学过的课文中随机切换且保证与当前展示不同；「换一篇」按钮改为直接打开新文章，不再被 `App.refresh()` 的缓存覆盖。

### Added
- **IMP-001 交易记录编辑 / 删除**：交易列表每条新增 ✎ 编辑与 🗑 删除入口；`txEditModal` 支持修改操作类型、日期、金额（人民币）、备注；`txDelete` 提供删除确认。沿用现有 UI 风格与数据契约，未改动 `pgwb_data_v1`。

### 其他
- 运行时版本 `version.json` → `1.2.1`（已打开页面将收到「发现新版本」提示）。
- 提交：`fix: v1.2.1 wealth SSOT, english regen, tx edit/delete`

## [v1.2.0] - Decision Engine 决策引擎（当前部署）

### Added
- **Decision Engine 决策引擎**：新增 `RuleEngine` 作为**唯一决策中心**，`TodayAgent` 不再自行生成建议，改为调用 `RuleEngine.getSuggestions()` 取排序后建议。
- **规则体系**：新增 `StudyRule` / ` WealthRule` / `FitnessRule` / `MediaRule` / `FutureRule`，每个 `evaluate(d)` 返回统一结构的 `Suggestion[]`；`RuleEngine` 聚合并按 `priority` 降序、`estimatedTime` 升序排序，输出 Top3。
- **真实数据缺口驱动**：学习/运动/发布/复盘间隔、资产快照新鲜度、现金占比、体重趋势等均由真实 `S.data` 计算（非随机 Mock）；建议文案与阈值仍为硬编码（Mock 风格），`FutureRule` 为占位空桩。
- **LLM 定位明确**：当前未接入任何大模型；未来 OpenAI 仅负责**解释 / 细化** `RuleEngine` 产出的 `Suggestion[]`，**绝不参与决策**。
- 运行时版本 `version.json` → `1.2.0`（已打开页面将收到「发现新版本」提示）。
- 架构文档：`docs/Architecture/DecisionEngine.md`。
- 提交：`feat: build decision engine architecture`

## [v1.1.0] - Today OS 首页 AI 决策中心（当前部署）

### Added
- **Today OS 首页架构**：首页重构为「AI CEO Dashboard」，9 段式结构（欢迎区 / 今日三件 / 财富·学习·身体·自媒体摘要 / 今日最大风险 / 今日最大机会 / 复盘提醒）。
- **Agent 架构**：新增 `TodayAgent`（首页唯一入口，负责汇总）+ `StudyAgent` / `WealthAgent` / `FitnessAgent` / `MediaAgent` 桩；当前为 Mock/真实摘要混合，未接入真实 AI。
- 新增仪表盘所需 CSS（沿用既有设计变量）；其余 5 个页面与数据契约不变。
- 运行时版本 `version.json` → `1.1.0`（已打开页面将收到「发现新版本」提示）。
- 提交：`feat: build Today AI dashboard architecture`

## [未发布] AI 接管入口（docs 提交）

### Added
- 新增 `PROJECT_BOOTSTRAP.md`：整个项目**唯一的 AI 接管入口**（9 节：文件作用 / 接管流程 / 开发原则 / 文档维护 / Git 工作流 / 行为规范 / 输出规范 / 新聊天规范 / 长期维护）。
- 任何新 AI 接手前必读，禁止依赖聊天记录；唯一可信来源为 GitHub 最新代码 + 6 份根文档 + `docs/`。
- 提交：`docs: add PROJECT_BOOTSTRAP for AI onboarding`

## [未发布] AI Prompt 管理体系（docs 提交）

### Added
- 新增 `docs/Prompt/` 目录与 9 个文件：`PromptGuide.md`（管理规范）、`AI.md`（总体行为规范）、`Home/Study/Wealth/Fitness/Media/Review.md`（模块 Prompt 框架）、`Development.md`（开发类 Prompt）。
- 将所有 AI Prompt 从代码中独立，统一在此管理；未来接入真实模型时从本目录读取，不在 `index.html` 写死。
- 提交：`docs: initialize AI prompt management system`

## [v1.0.0] - 版本更新机制（当前部署）

### Added
- **版本自动检测 + 「发现新版本」弹窗**：`version.json` 作为运行时版本源；`index.html` 内联检测脚本（每分钟 + 回到前台时轮询，对比已加载版本与 `version.json`，不一致即弹窗）。
- **PWA 更新流**：`sw.js` 新增 `skipWaiting` 消息处理；点击「立即更新」→ `postMessage('skip')` → 新 SW 激活并 `clients.claim()` 立即接管 → 自动刷新到最新版；「稍后更新」关闭弹窗、下次再提示。
- 配套资源：`manifest.json` 主题色深蓝 `#16335c`、背景 `#f4f7fb`；新增 `icon-1024.png` 并登记进 manifest；刷新 7 张 iOS 启动图。
- 提交：`feat: version update detection and pwa update flow`

## [未发布] dev（本地）

- 文档体系已在 `eb51f87 docs:` 提交并推送；后续功能迭代请按 AI_RULES 维护本文件。

## [v0.9] PWA 阶段（已部署，未打 tag）

### Added
- `d98691c` **升级为完整 PWA**：`manifest.json` + `sw.js`（离线缓存外壳）+ 图标（192/512/maskable/apple-touch）+ 7 张 iOS 启动图。

### Added
- `e64590f` **部署到 GitHub Pages**：`standalone.html` → `index.html`，main 分支根目录静态托管，HTTPS。

### Added
- `8e13376` **init**：上传单文件 `standalone.html`（个人成长工作台单文件版），含 6 标签、数据层、本地规则 AI、手写图表。

---

## 约定

- 提交信息前缀：`feat` / `fix` / `refactor` / `docs` / `style` / `perf`（详见 AI_RULES.md）。
- 正式版本：在 main 打 `vX.Y` 轻量 tag；`version.json` 的 `version` 字段随之更新。
- 破坏性数据变更（删除/重命名字段）必须在「Changed」中显式说明并提供迁移。
