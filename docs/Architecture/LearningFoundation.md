# 架构文档：学习引擎基础 Learning Foundation（v1.3.1）

> 本文档描述 v1.3.1「学习引擎基础」的架构设计、数据契约与扩展点。
> 目标：把 Learning 模块从「静态展示」升级为「可扩展的学习基础设施」，但**不接入真实联网 AI**、不实现 Planner/Project/Memory Engine，不改动 `pgwb_data_v1` 数据契约。

---

## 1. 设计目标

1. **统一学习对象管理**：英语、AI 工具、产品等学习对象由同一个注册中心 `window.Library` 管理，不再散落在各模块的硬编码数组（`EN_LIB` / `AI_TOPICS`）。
2. **可扩展数据源**：引入 `window.LearningSource` 抽象，当前用内置 `LocalSource` 提供内容（英语 8 篇 / AI 工具 3 篇 / 产品 2 篇），**不再写死仅 4 篇英语**；为 V1.3.2 联网预留 `RemoteSource` 接口。
3. **学习历史可续学**：历史记录支持「查看历史笔记 / 继续学习 / 重新学习」，英语/AI 记录可完整恢复交互式内容，其它类别恢复已存摘要/笔记/产出。
4. **英语模块去耦**：英语模块读取 `Library`（按 `category:'en'`），不再直接依赖 `EN_LIB`。

---

## 2. 模块结构

```
window.Library         学习对象统一注册中心（Registry）
  ├─ register(obj)        注册单个对象（自动补 id / category）
  ├─ registerAll(arr)     批量注册
  ├─ get(id) / all()      查询
  ├─ byCategory(cat)      按类别取（en / ai / product ...）
  ├─ findByTitle(title)   按标题精确查找（学习历史回看用它定位课文）
  ├─ search(q)            全文检索（V1.3.2 搜索/推荐预留）
  └─ categories()         各类别计数

window.LearningSource   数据源抽象（Data Source Abstraction）
  ├─ LocalSource(id,data) 本地静态数据源（.load() 返回内容数组）
  ├─ RemoteSource(id,ep)  联网数据源【占位】(.load() 当前返回 []，V1.3.2 实现)
  ├─ addSource(src)       注册数据源
  ├─ load()               聚合所有数据源 → 灌入 Library（幂等）
  └─ registerBuiltin()     注册内置 LocalSource（en/ai/product）
```

加载时机：`App.load()` 启动时调用 `window.LearningSource.load()`，把内置内容灌入 `Library`，之后各模块统一从 `Library` 读取。

---

## 3. 学习对象数据形状

所有对象统一字段：`{ id, category, title, source, ... }`（`register` 自动补 `id`/`category`）。

**英语（category:'en'）** —— 兼容 `EnglishMod.open(lesson)`：
```
{ id, category:'en', title, source, excerpt,
  words:[{w,def,ex}], expressions:[{ph,zh}], grammar:{point,ex} }
```

**AI 工具（category:'ai'）** —— 兼容 `genAiTask` 表单：
```
{ id, category:'ai', title, source, core, question, relation, practice, output }
```

**产品（category:'product'）** —— 统一注册占位（当前无独立 UI，为未来产品学习视图预留）：
```
{ id, category:'product', title, source, summary, points:[...] }
```

> 新增类别只需在 `LearningSource` 内置库追加 `LocalSource` 数据，并约定该类别的对象形状；`Library` 与 `byCategory` 无需改动。

---

## 4. 关键流转

### 4.1 英语模块读取 Library
- `AI.generateEnglish(force)`：从 `Library.byCategory('en')` 取课文；按今日主线 `plan.cat` 优先匹配对应课文（`PLAN_EN_MAP`），否则按日期在未学课文中确定性取一篇；`force` 时在未学课文中随机切换且保证与当前展示不同。
- `AI.findEnglish(topic)`：委托 `Library.byCategory('en').find(o=>o.title===topic)`。
- 学习历史「继续学习/重新学习」英语：从 `Library.findByTitle(r.topic)` 取到课文对象，交给 `EnglishMod.open(lesson, opts)`。

### 4.2 学习历史升级
`openLearnRecord(id)` 弹出记录详情：
- **查看历史笔记**（默认）：恢复该记录已保存的 摘要 / 笔记 / 产出 / 理解度。
- **继续学习**：回填历史笔记到交互式学习，`EnglishMod.open(libObj,{prefill, updateId})` / `genAiTask({prefill, updateId})`，保存时**更新原记录、保留原始日期**。
- **重新学习**：全新状态 `EnglishMod.open(libObj,{})` / `genAiTask({})`，保存时**新增一条今日记录**。

英语/AI 记录若能在 `Library` 找到对应对象（`interactive=true`），才展示续学按钮；产品等当前仅支持查看笔记。

---

## 5. 为 V1.3.2（联网 AI 学习）预留的扩展点

1. **`LearningSource.RemoteSource(id, endpoint)`**：已实现空壳，`load()` 当前返回 `[]`。V1.3.2 可在此实现 `fetch(endpoint)` 拉取真实课文源与个性化练习，**不改动调用方**。
2. **`Library.search(q)` / `categories()`**：检索与聚合能力已具备，供未来推荐/筛选使用。
3. **`EnglishMod.open(lesson, opts)` 的 `opts`**：续学/回填接口已抽象，未来可传入从远端拉取的个性化内容。
4. **数据契约不变**：`pgwb_data_v1` 的 `learning[]` 形状未改，新增字段向后兼容；联网方案不得破坏本地存储与离线能力。

---

## 6. 约束遵守（v1.3.1 范围）

- ✅ 未改动数据契约 `pgwb_data_v1`。
- ✅ 未触碰 Planner / Project / Memory Engine、TodayAgent、RuleEngine、财富/身体/自媒体模块。
- ✅ 保持 UI 风格与 localStorage 兼容，PWA 正常。
- ✅ 未实现任何联网逻辑（`RemoteSource` 仅占位）。
- ⛔ 未实现：真实联网课文源、复习曲线、联网 AI 批改 —— 属 V1.3.2+。
