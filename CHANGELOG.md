# CHANGELOG.md — 版本记录

> 格式参考 [Keep a Changelog](https://keepachangelog.com/)。版本号规范：`v1.0` / `v1.1` / `v2.0` …；开发态 `version.json` 为 `dev`。
> 每次发版必须在此追加条目，并更新 PROJECT.md 第 2 节「当前版本」。

## [v1.5.0] - Hot Trends Foundation（热点中心）

> 本版本目标：让自媒体（Content）模块**真正联网并每日更新**——从纯本地 `TRENDS` 数组升级为可每日刷新的热点中心（Content Center）。这是 Content Center 升级，**不是** AI/英语/Project 扩展，不动 `LearningSource`/`Library`/`ProjectLibrary`，不破坏 `pgwb_data_v1`。

### Added
- **`TrendSource` + `TrendLibrary` 新模块**（仿 `RemoteSource` 范式，独立内存 + 独立缓存键 `pgwb_trends_cache_v1`）：`TrendSource.loadRemote()` 异步拉取 `data/trends-daily.json` → `normalize`（按 `cat` 路由，`id` 前缀 `tr-<cat>-`）→ 注入 `TrendLibrary`；远程失败按 `缓存 → 本地兜底` 逐级降级，绝不白屏。
- **内容中心「热点」页**：新增 `热点` 一级子页（与 `选题`/`我的内容`/`分析` 并列），分段切换 `今天 / 本周 / AI / 投资 / 小红书`；每条热点突出 `为什么值得写` / `适合账号` / `推荐角度` / `推荐标题` + `trendScore` 排序，而非新闻摘要。
- **选题闭环（热点 → 半成品草稿 → 内容库）**：热点卡「用这个选题创作」按钮 → 直接 `S.add('contents', …)` 创建草稿（预填 `标题 / 平台 / 灵感来源 / 推荐角度 / 内容提纲`）并打开编辑弹窗继续编辑；内容记录新增 `platform` / `inspiration` / `angle` / `outline` 字段，详情弹窗同步展示。用户进入内容库即拥有一篇可继续编辑的**半成品草稿**，而非空白记录。
- **热点数据结构（v2）**：每条含 `hot / whyHot / source / url / date / summary / valueTag / whyWorthWriting / fitAccount / angle / titles / trendScore`；`trendScore`（1–100）用于排序，由来源热度/讨论量/时效性/创作价值综合。
- **热点种子 `data/trends-daily.json`**：手工策展 **30 条**（AI 10 / 科技 5 / 投资 10 / 小红书 5 人工维护），满足今日 10 / 本周 10 / AI 10 / 投资 10 / 小红书 5 规模上限。
- **CI 每日生成流水线**：`.github/workflows/trends.yml`（每日 UTC 00:00）+ `scripts/gen_trends.py`（仅标准库）：真实抓取 HN Algolia / arXiv RSS / GitHub API / 科技·财经 RSS；小红书走人工维护 `data/xhs-manual.json`；投资热点**仅来自财经 RSS，不含实时行情拉取**（实时行情留待未来版本）；LLM（仅存 CI Secrets）**只生成** `whyWorthWriting / fitAccount / angle / titles` 四类衍生字段，不虚构热点；质量门（价值标签 + 反套路黑名单）+ 规模上限。
- **缓存策略**：启动非阻塞刷新；`pgwb_trends_cache_v1` 存 `{generatedAt, cachedAt, trends}`；新鲜度分级提示（≤24h 正常 / 1–7 天软提示 / >7 天强提示 / 离线回退本地兜底），旧热点跨次保留。
- **半成品草稿提纲（模板化，不调用 LLM）**：`buildOutline(trend)` 按固定模板生成「开头（为什么最近很多人在讨论这个？）→ 正文（1.热点是什么 / 2.为什么重要 / 3.对普通人有什么影响）→ 结尾（我的观点是什么？）」，用热点真实字段（`hot/summary/whyWorthWriting/angle`）填充，得到可继续编辑的草稿；纯前端、零 API 成本、零延迟。
- **主题去重（连续 7 天窗口，防霸榜）**：前端 `TrendSource.dedupeByTheme()` 以 `cat|themeKey(hot)` 折叠同主题（仅留 `trendScore` 最高一条）；CI 端 `scripts/gen_trends.py` 额外维护滚动历史 `data/trends-history.json`（最近 7 天发布的主题），次日对重复主题**降权**（`trendScore - 8×出现次数`，下限 45）或**剔除**（≥3 次）；同一天同主题仅保留一条。保障热点新鲜度与主题多样性。

### Changed
- 运行时版本 `version.json` → `1.5.0`。

### 约束遵守
- 无后端常驻服务；前端不暴露任何 Key（Key 仅存 CI Secrets / GitHub Actions）。
- 不影响 `LearningSource` / `Library` / `ProjectLibrary`；不写 `pgwb_data_v1`（用户内容仍在 `S.data.contents`）。

## [v1.4.2] - Learning Content Expansion（学习内容扩展）

> 本版本目标：扩充学习内容供给，把内容池从「英语 / AI 工具 / 项目模板」三路并进，未来可持续新增而**不改动 `index.html` 内容逻辑**。仅做内容扩展，不重构架构、不统一存储。

### Added
- **`RemoteSource` 支持三类内容（english / ai / project）**：`RemoteSource(id, endpoint, type)` 新增 `type` 参数；`REMOTE_SOURCES` 配置三个静态 JSON 端点（`english-lessons.json` / `ai-courses.json` / `project-cases.json`）；`normalize` 按 `type` 路由到对应形状并强制 id 前缀（`ren-en-` / `ren-ai-` / `prj-`），与本地 `en-` / `ai-` / `tpl-` 命名空间互斥，杜绝后写覆盖。
- **英语内容扩充**：`data/english-lessons.json` 由 5 篇扩至 **25 篇远程**（保留原 5 篇 + 新增 20 篇不同主题，含 words/expressions/grammar）；加本地 8 篇，**英语总量 33 篇**。
- **AI 课程新内容池**：新增 `data/ai-courses.json`（**13 篇**远程，覆盖 ComfyUI / Flowise / RAG / Agent / 向量数据库 / Prompt Engineering / AI 自动化 / AI 产品设计 / AI 创业案例 / Perplexity / Midjourney / Whisper / 模型微调——均为本地 11 个工具之外**真实不同主题**，无「入门/进阶/专家」式拆分灌水）；加本地 11 个，**AI 总量 24 个**。
- **项目案例新内容池**：新增 `data/project-cases.json`（**20 个真实项目案例**，复用 `ProjectLibrary.TEMPLATES` 形状：魔法厨房 / 小红书运营系统 / 个人博客 / 自动化周报 / 电商看板 / 英语学习系统 / 个人 AI 助手 / 习惯 App / 知识库 / 短视频脚本 / 客服机器人 / 简历优化 / 会议纪要 / 竞品监控 / 读书卡片 / 家庭记账 / 内容日历 / 代码评审 / 旅行规划 / 简历初筛）；**项目案例总量 20 个**。
- **`ProjectLibrary.addCases(list)`**：新增远程案例注入接口（按 `id` 去重 push 进 `TEMPLATES`）；`match/get/all` 不变，`ProjectEngine` / `RuleEngine` / `TodayAgent` 零改动。

### Changed
- **加载策略（三路并行、各自降级）**：`LearningSource.loadRemote()` 遍历三个远程源，按 `type` 路由——英语/AI 进 `Library`，项目旁路进 `ProjectLibrary`；任一路失败仅该池降级（静默 `warn`），其余两池与本地不受影响，绝不抛错、绝不白屏。
- 运行时版本 `version.json` → `1.4.2`。

### 约束遵守
- 职责边界不变：`Library` / `LearningSource` / `ProjectLibrary` / `ProjectEngine` 各自职责与对外接口保持原样；英语/AI 走 `Library`，项目走 `ProjectLibrary`（Option A，不为「统一」而统一）。
- 未修改 `pgwb_data_v1`（远程内容仅运行时进内存注册，学习进度 schema 不变，旧记录可继续学习/重学）。
- 未触碰 AI 学习联网、自媒体热点抓取、财富/身体模块；不接入 LLM / 任何 Key / 后端；全部内容为手写静态 JSON。
- 本地英语 8 篇、本地 AI 11 个、本地项目模板 5 个均保留不变。

### 降级能力（必须满足）
- App 可正常打开；英语/AI/项目三模块均可用；学习历史与旧记录不受影响。
- 某路远程失败（网络/HTTP/解析/`file://`）→ 仅该池回退本地，无白屏、无异常中断；三路全失败等同 V1.4.1 现状。

## [v1.4.1] - RemoteSource English（英语联网课文）

> 本版本目标：让英语学习模块支持联网获取课文。仅做英语联网，不触碰 AI 学习 / 自媒体 / 财富 / ProjectEngine / RuleEngine / TodayAgent；不接入 LLM。

### Added
- **`RemoteSource` 真正联网（原为 V1.3.1 占位空壳）**：`fetchLessons()` 通过 `fetch(endpoint)` 拉取同源静态 JSON 课文；`validate(lesson)` 校验（title + category/type + words 数组，quiz 可选）；`normalize(lesson)` 将 `type:'english'` 归一为 `category:'en'`，补齐 words/expressions/grammar 默认形状，保证最终进入 `Library` 的对象与本地 8 篇完全一致。
- **远程课文 JSON 文件**：新增 `data/english-lessons.json`（同源静态托管，GitHub Pages 可访问，无后端），首版含 5 篇远程课文（含 `type:'english'`；其中 2 篇带可选 `quiz` 字段以验证 quiz 容错）。
- **`LearningSource.loadRemote()` 异步加载**：在 `App.load()` 中**非阻塞**调用；成功则把远程课文并入 `Library`（远程 + 本地），失败（网络/解析错误）静默降级为仅本地 8 篇，**绝不抛错、不阻塞启动**。
- **`docs/Architecture/RemoteSource.md`**：新增架构文档，记录加载策略与降级契约。

### Changed
- **加载策略（RemoteSource 优先、LocalSource 兜底）**：`LearningSource.load()` 仍仅同步加载本地内置库（保证离线/无网络时英语立即可用、永不白屏）；远程课文通过异步 `loadRemote()` 在启动后并入，最终效果为「远程成功 → 远程+本地；远程失败 → 仅本地 8 篇」。

### 约束遵守
- 未修改本地英语课文数据结构（`{id,category:'en',title,source,excerpt,words,expressions,grammar}` 保持不变）；未改动 `Library.byCategory('en')` / `AI.generateEnglish()` / `EnglishMod.open()` 的调用契约。
- 未触碰 AI 学习模块、自媒体热点、财富模块、`ProjectEngine`、`RuleEngine`、`TodayAgent`；不接入 LLM / OpenAI / Claude Key；不做聊天机器人。
- 数据契约 `pgwb_data_v1` 不变（远程课文仅作为学习对象流入 `Library`，不写入存储；用户产生的学习记录仍走既有 `S.add('learning',...)` 结构）。
- 运行时版本 `version.json` → `1.4.1`。

### 降级能力（必须满足）
- App 可正常打开；英语学习可正常使用；学习历史不受影响；`pgwb_data_v1` 不变。
- 任何网络错误 → 静默降级本地 8 篇，无白屏、无异常中断。

## [v1.3.3] - Project Learning Foundation（项目学习引擎）

> 本版本目标：把「学习」里的 Project（创造）模块从「手工记录工具」升级为「基于本地项目知识库的项目学习引擎」。新增 `ProjectLibrary`（本地项目知识库）+ `ProjectEngine`（项目路线生成器），进度与下一步改为自动计算，创建前可预览并自由调整阶段与步骤。

### Added
- **`ProjectLibrary`（本地项目知识库，无联网 / 无 AI / 无 LLM）**：纯本地内置数据，挂在 `window.ProjectLibrary`，提供 `match(name)`（按关键词/子串模糊匹配，未命中回退通用项目模板）、`get(id)`、`all()`。首版内置 5 套完整项目模板：
  - `tpl-ai-workbench` 个人 AI 工作台
  - `tpl-xhs` 小红书账号
  - `tpl-taobao` 淘宝自动化
  - `tpl-website` 个人网站
  - `tpl-generic` 通用项目（兜底模板）
  每套模板含：项目介绍、项目目标、适合人群、预计周期、阶段列表（每个阶段含若干步骤，每步含 标题 / 完成标准 / 预计耗时）、推荐学习资料、容易踩坑的问题。
- **`ProjectEngine`（项目路线自动生成器）**：`buildDraft(name, tpl)` 基于模板深拷贝生成项目草稿（阶段/步骤分配 `U.uid`、`done:false`、记录 `sourceType/libraryId/templateName/resources/pitfalls`、初始版本 `versions:[{v:'0.1'}]`）；`compute(p)` 自动计算总步数/已完成数/进度百分比/下一步（首个未完成步骤标题，全完成则 `🎉 全部完成`，零步骤则 `添加你的第一步`）/当前阶段；`recompute(p)` 回写 `progress/nextAction/currentStage`；`create(draft)` 经 `recompute` 后 `S.add('projects', p)`。
- **进度自动计算（取消手工填写百分比）**：项目进度不再是用户手填的数字，而是由「已完成步骤数 / 总步骤数」实时计算（`round(done/total*100)`），20 步完成 4 步即 20%、全部完成即 100%。
- **下一步自动计算（取消手工填写）**：「下一步」自动取第一个未完成的步骤标题，无需用户手工维护。
- **创建前预览与可调**：输入项目名 → 匹配模板 → 生成完整项目路线预览 → 用户可在创建前任意新增/删除/修改步骤与阶段、调整顺序 → 确认后才 `ProjectEngine.create` 落库。模板是「模板」而非标准答案，允许创建前调整。
- **创造能力模块重写（向后兼容）**：`buildView` / `openProj` / `addProj` 重构；新增 `projProgress/projNext/projStage` 帮助函数（有 `stages` 用 `ProjectEngine.compute`，无 `stages` 的旧项目回退原 `progress`/`nextAction` 与原手工编辑表单 `openProjLegacy`）；项目详情页渲染阶段勾选框（勾选即 `done` + `recompute` + `S.save` + 重渲染）、进度条、介绍/目标/适合人群/预计周期/推荐资料/踩坑提示。

### Changed
- **数据模型（仅增量，不破坏契约）**：`projects[]` 在原有字段基础上新增 `stages[]`（每阶段含 `id/name/steps[]`，每步含 `id/title/doneCriteria/estTime/done`）、`sourceType`、`libraryId`、`templateName`、`resources[]`、`pitfalls[]`、`currentStage`。通过 `stages` 是否存在区分新旧项目，旧项目（无 `stages`）沿用原进度/下一步/手工编辑，数据契约完全向后兼容。
- **数据契约 `pgwb_data_v1` 保持 add-only**：未修改/删除任何既有顶层键或字段（含 learn/wealth/body/content/TodayAgent/RuleEngine/AI 学习/英语学习/PWA/版本检测），完全向后兼容。

### 约束遵守
- 未改动英语学习、AI 学习、财富、身体、自媒体模块；未触碰 TodayAgent、RuleEngine、LearningSource、RemoteSource、PlannerEngine、Memory Engine、任何 LLM、联网能力、Prompt 体系与 Agent/Claude/Cursor/ChatGPT/MCP 等功能；保持既有 UI 风格，无新设计系统。
- 运行时版本 `version.json` → `1.3.3`。
- 新增架构文档：`docs/Architecture/ProjectFoundation.md`。
- 提交：`feat: v1.3.3 Project Learning Foundation (ProjectLibrary + ProjectEngine)`

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
