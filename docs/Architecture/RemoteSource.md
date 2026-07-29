# 架构文档：RemoteSource（v1.4.1 英语联网 → v1.4.2 三类型内容源）

> 本文档描述 `RemoteSource` 的架构设计、加载策略、降级契约与扩展点。v1.4.1 打通英语联网；v1.4.2 扩展为支持 `english` / `ai` / `project` 三类远程内容，统一进学习库（英语/AI 走 `Library`，项目旁路进 `ProjectLibrary`）。
> 目标：在 **不改动各模块职责边界、不改动数据结构契约** 的前提下，让学习内容池可持续扩充。

---

## 1. 设计目标

1. **打通链路**：`RemoteSource` → `Library` → `EnglishMod` 整条链路可用。
2. **复用既有架构**：基于 `LearningSource` 扩展，保留 `LocalSource`；不推翻 `Library` / `LearningSource` / `EnglishMod`。
3. **本地数据结构零改动**：本地 8 篇英语对象保持 `{id, category:'en', title, source, excerpt, words, expressions, grammar}`。
4. **降级优先**：远程成功 → 远程 + 本地；远程失败 → 仅本地 8 篇。任何网络错误不得导致白屏 / 英语不可用 / 学习历史异常。
5. **范围克制（v1.4.1）**：仅英语联网；不动 AI 学习 / 自媒体 / 财富 / `ProjectEngine` / `RuleEngine` / `TodayAgent`；不接 LLM。
6. **三类型内容源（v1.4.2）**：`RemoteSource` 支持 `english` / `ai` / `project` 三类；英语/AI 进 `Library`，项目旁路 `ProjectLibrary`；职责边界不变，**不为「统一」而统一**。

---

## 2. 模块结构

```
window.LearningSource               数据源抽象（Data Source Abstraction）
  ├─ LocalSource(id,data)           本地静态数据源（.load() 返回内置数组）
  ├─ RemoteSource(id, endpoint, type) 联网数据源（v1.4.2 支持 english/ai/project）
  │     · fetchLessons()             fetch(endpoint) → 解析 JSON（网络/解析错误向上抛）
  │     · validate(o)               按 type 校验（英语需 words[]；AI/项目需 title 或 name）
  │     · normalize(o)              按 type 路由：_normEnglish / _normAi / _normProject
  │     · load()                     旧同步接口，恒返回 []（远程走异步 loadRemote）
  ├─ REMOTE_SOURCES[]               三路端点配置（en / ai / project 各一个 JSON）
  ├─ addSource(src)                  注册（同步）数据源
  ├─ registerBuiltin()               注册内置 LocalSource + 构建 remoteSources[]（三路）
  ├─ load()                          同步加载本地库（保证离线可用，不阻塞启动）
  └─ loadRemote()                   三路并行异步加载，按 type 路由；各路失败独立降级
```

加载时机：`App.load()` 启动时**同步**调用 `LearningSource.load()`（本地 8 英语 + 11 AI + 5 项目模板立即可用），随后**非阻塞**调用 `LearningSource.loadRemote()`（三路并行拉取远程内容，英语/AI 并入 `Library`、项目旁路 `ProjectLibrary`）。

---

## 3. 远程内容数据形状（按 type 分三类）

### 3.1 英语 english（兼容 EnglishMod，进 `Library` category 'en'）
用户给定：`{ id, type:'english', title, excerpt, words, expressions, grammar, quiz? }`
归一化后（与本地 8 篇一致）：`{ id:'ren-en-<id或slug>', category:'en', title, source, excerpt, words:[{w,def,ex}], expressions:[{ph,zh}], grammar:{point,ex}, quiz? }`
- `type:'english'` → 归一 `category:'en'`；`id` 加 `ren-en-` 前缀，避免覆盖本地 `en-*`。
- `quiz` 可选保留入库，`EnglishMod` 暂不渲染；本地 8 篇结构不变。

### 3.2 AI 课程 ai（复用 BUILTIN_AI，进 `Library` category 'ai'）
用户给定：`{ id, type:'ai', title, subtitle, source, intro, problem, forWhom, caps:[{name,desc}], cases:[{t,d}] }`
归一化后：`{ id:'ren-ai-<id或slug>', category:'ai', ...同字段 }`
- 进入 `Library` 后即被 `aiView()` 的 `Library.byCategory('ai')` 自动命中，**AI 中心 UI 无需改动**。
- 远程主题为本地 11 个工具之外的真实不同主题，禁止「入门/进阶/专家」式拆分灌水。

### 3.3 项目案例 project（复用 ProjectLibrary.TEMPLATES，旁路入 `ProjectLibrary`）
用户给定：`{ id, type:'project', name, keywords[], intro, goal, forWhom, estDuration, stages:[{name, steps:[{title,doneCriteria,estTime}]}], resources?[], pitfalls?[] }`
归一化后：`{ id:'prj-<id或slug>', name, keywords, intro, goal, forWhom, estDuration, stages, resources, pitfalls }`
- **不进 `Library`**，由 `loadRemote` 调用 `ProjectLibrary.addCases([norm])` 注入模板集合。
- `ProjectEngine` 消费 `TEMPLATES` 的方式不变（零改动）；`addCases` 按 `id` 去重。

---

## 4. 关键流转

### 4.1 同步启动（本地优先，防白屏）
`App.load()` → `LearningSource.load()`：
- `registerBuiltin()` 注册 LocalSource（en/ai/product），并设置 `remoteSource` 引用（**不拉取**）。
- 同步把本地 8 篇英语灌入 `Library` → 即使网络完全不可用，英语学习、生成课文、`EnglishMod.open` 全部正常。

### 4.2 异步远程加载（三路并行，按 type 路由）
`App.load()` → `LearningSource.loadRemote()`（不 await，非阻塞）：
- 遍历 `remoteSources`（en / ai / project 三路），各自 `fetchLessons()`：`fetch(endpoint, {cache:'no-cache'})` → `res.json()`；非 2xx 或解析失败 → 该路抛错。
- 成功：遍历数组，对每条 `validate` → `normalize`（按 type 选 `_normEnglish` / `_normAi` / `_normProject`）→ 路由注册：
  - `english` / `ai` → `Library.register`（并入 Library）。
  - `project` → `ProjectLibrary.addCases([norm])`（旁路注入模板集合）。
- 每路独立 `.catch`：失败仅该池降级（静默 `warn`），其余两路与本地不受影响；**App 不抛错、不白屏**。

### 4.3 流向 EnglishMod
`AI.generateEnglish(force)` 从 `Library.byCategory('en')` 取课文（本地 + 远程混合）→ 交给 `EnglishMod.open(lesson, opts)`。远程课文只要经 `normalize` 落入 `Library`（category:'en'），即可被既有取数逻辑命中，**无需改动 `EnglishMod` 取数逻辑**。

---

## 5. 远程内容 JSON 文件（三个静态文件，随 GitHub Pages 托管，无后端）

- `data/english-lessons.json`：英语远程课文（v1.4.2 扩至 **25 篇**：原 5 + 新增 20；含 `type:'english'`，部分带可选 `quiz`）。
- `data/ai-courses.json`：AI 课程远程内容（v1.4.2 新增 **13 篇**，均为本地 11 工具之外的真实不同主题；含 `type:'ai'`）。
- `data/project-cases.json`：项目案例远程内容（v1.4.2 新增 **20 个**真实案例，复用 `TEMPLATES` 形状；含 `type:'project'`）。
- 部署要求：均为同源静态文件，无需后端；相对路径 `./data/*.json` 在 GitHub Pages 与本地静态服务均可访问。
- 扩展：后续增删内容，只需修改对应 JSON；`RemoteSource` 代码无需改动。

**内容量（v1.4.2）**：英语 33（8 本地 + 25 远程）／ AI 24（11 本地 + 13 远程）／ 项目案例 20（0 本地 + 20 远程；本地另有 5 套项目模板独立存在）。

---

## 6. 降级契约（必须满足）

| 场景 | 结果 |
| --- | --- |
| 三路全成功 | 英语/AI 进 `Library`（本地 + 远程混合）；项目案例进 `ProjectLibrary`（远程案例）；`byCategory` 与 `ProjectLibrary.all` 均含远程内容 |
| 某一路失败 | 仅该池降级为本地，其余两路与本地不受影响；`console.warn('[RemoteSource] 远程内容加载失败（<type>），已降级为本地：', err)`；App 正常 |
| 三路全失败 | 等同 V1.4.1 现状：本地 8 英语 + 11 AI + 5 项目模板 |
| 远程 HTTP 非 2xx | 该路静默降级；App 正常 |
| 网络不可达 / fetch 抛错 | 该路静默降级；App 正常 |
| JSON 解析失败 / 空数组 | 该路静默降级；App 正常 |
| `file://` 直接打开（无 fetch 跨域） | `fetch` 失败 → 该路降级本地 |
| 学习历史 | 不受影响（`pgwb_data_v1` 不变，历史记录结构不变，旧记录可继续学习/重学） |

---

## 7. 约束遵守（v1.4.1 → v1.4.2）

- ✅ 本地英语 8 篇 / AI 11 个 / 项目模板 5 套数据结构不变；`Library.byCategory` / `aiView` / `EnglishMod.open` / `ProjectLibrary.match` 调用契约不变。
- ✅ 模块职责边界不变：`Library` / `LearningSource` / `ProjectLibrary` / `ProjectEngine` 各自职责与对外接口保持原样；英语/AI 走 `Library`，项目走 `ProjectLibrary`（Option A，不为「统一」而统一）。
- ✅ 未触碰 AI 学习联网、自媒体热点抓取、财富/身体模块；不接入 LLM / 任何 Key / 后端；全部内容为手写静态 JSON。
- ✅ 数据契约 `pgwb_data_v1` 不变（远程内容仅运行时进内存注册，不写入存储；学习进度 schema 不变，旧记录可继续学习/重学）。
- ✅ 运行时版本 `version.json` → `1.4.2`。

---

## 8. 扩展点（持续扩充内容，不改代码逻辑）

- **加内容不改 `index.html`**：新增/修改 `data/*.json` 即可扩充英语/AI/项目内容；`REMOTE_SOURCES` 已声明三路端点，`RemoteSource` 代码无需改动。
- **新增内容类型**：在 `REMOTE_SOURCES` 加一项、在 `RemoteSource.normalize` 加一个 `_normXxx` 分支即可；英语/AI 走 `Library`，需独立存储的内容走类似 `ProjectLibrary.addCases` 的旁路。
- **更多字段**：`normalize` / `validate` 可按类型扩展（如英语 audio、AI 难度等级），不影响本地数据结构。
