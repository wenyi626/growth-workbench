# 架构文档：项目引导基础设施 Project Foundation（v1.3.3）

> 本文档描述 v1.3.3「Project Learning Foundation」的架构设计、数据模型与扩展点。
> 目标：把「创造」模块从「手工记录工具」升级为「由本地项目知识库驱动、自动生成路线、进度自动计算」的项目引擎。

---

## 1. 设计原则

1. **本地优先**：`ProjectLibrary` 是纯本地内置数据，不联网、不调用大模型、不依赖 `RemoteSource`/`LearningSource`。
2. **模板非固定答案**：模板只用于「生成预览」，创建前用户可自由增删改步骤、调整顺序；确认后才落库。
3. **进度自动计算**：不再手工填写百分比；进度 = 已完成步骤 / 总步骤。下一步 = 第一个未完成步骤（跨阶段、按序）。
4. **向后兼容**：仅向 `pgwb_data_v1.projects[]` 新增可选字段，不改 / 不删已有字段；无 `stages` 的旧项目走 `openProjLegacy` 原手动编辑弹窗。
5. **不触碰其它模块**：英语学习、AI 学习、财富、身体、TodayAgent、RuleEngine、LearningSource、RemoteSource、PlannerEngine、Memory Engine、LLM/联网、Prompt 体系、Agent/Claude/Cursor/ChatGPT/MCP 等功能保持 v1.3.2 不变。

---

## 2. 模块结构

```
window.ProjectLibrary    本地项目知识库（模板注册中心 / Registry）
  · match(name)          按名称模糊匹配最合适的模板；无匹配返回通用兜底模板
  · get(id)              按 id 取模板
  · all()                全部模板

window.ProjectEngine     项目生成与计算引擎
  · buildDraft(name,tpl) 由模板生成「草稿」项目（仅内存，分配 id、步骤 done=false）
  · compute(p)           计算 { total, done, progress, nextAction, currentStage }
  · recompute(p)         把派生值（progress/nextAction/stage）写回项目对象
  · create(draft)        正式创建：补版本信息后 S.add('projects', p)
```

加载时机：`App.load()` 目前只加载 `LearningSource`；`ProjectLibrary`/`ProjectEngine` 为纯函数模块，无需预热，首次使用时直接调用。

---

## 3. 模板数据形状（ProjectLibrary）

每个模板统一字段：

```
{ id, name, keywords:[],
  intro, goal, forWhom, estDuration,
  stages:[ { name, steps:[ { title, doneCriteria, estTime } ] } ],
  resources:[], pitfalls:[] }
```

第一版内置 5 个模板（≤5，符合范围）：

| id | name | 覆盖场景 |
| --- | --- | --- |
| `tpl-ai-workbench` | 个人 AI 工作台 | AI / 工作台 / 效率 / 自动化 |
| `tpl-xhs` | 小红书账号 | 小红书 / 自媒体 / 笔记 |
| `tpl-taobao` | 淘宝自动化 | 淘宝 / 电商 / 店铺运营 |
| `tpl-website` | 个人网站 | 网站 / 产品 / 小程序 / 博客（含 Magic Kitchen 类自定义产品名） |
| `tpl-generic` | 通用项目 | 兜底模板，任何未匹配名称都生成通用路线 |

> 新增模板只需在 `TEMPLATES` 数组追加一个对象，无需改动任何调用方。

---

## 4. 项目数据形状（pgwb_data_v1.projects[]，新增字段）

原有字段（`id/name/goal/stage/progress/nextAction/notes/versions/aiChats`）**全部保留，未改动**。新增可选字段：

```
{ ...,                                                   // 原有字段不变
  sourceType: 'library' | 'generic',                    // 来源
  libraryId: 模板 id,                                    // 若为 library
  templateName: 模板名,
  intro, forWhom, estDuration,
  stages:[ { id, name, steps:[ { id, title, doneCriteria, estTime, done:false } ] } ],
  resources:[], pitfalls:[] }
```

向后兼容：旧项目无 `stages` → `buildView`/`openProj` 回退原 `progress`/`nextAction`，由 `openProjLegacy` 提供原手动编辑弹窗。

---

## 5. 关键流程

### 5.1 创建项目（预览 → 编辑 → 确认）
- `addProj()`：输入名称 → `ProjectLibrary.match(name)` 选模板 → `ProjectEngine.buildDraft` 生成草稿 → `renderPreview` 展示。
- `renderPreview(draft,tpl)`：展示项目元信息 + 阶段/步骤；支持编辑步骤标题/完成标准/耗时、增删步骤、步骤上下移、增删阶段、阶段上下移；文本字段 `oninput` 双向绑定到 `draft`。
- 结构性变更（增删/排序）直接改 `draft` 后重渲染预览；**确认前不落库**。
- 确认 → `ProjectEngine.create(draft)`（写回 progress/nextAction/stage）→ `S.add('projects', p)`。

### 5.2 进度与下一步自动计算
- `ProjectEngine.compute(p)`：遍历所有阶段的所有步骤，`progress = round(done/total*100)`；`nextAction` = 第一个 `done===false` 的步骤标题（全完成则「🎉 全部完成」，零步骤则「添加你的第一步」）；`currentStage` = 该步骤所在阶段。
- `openProj`（有 stages）：勾选步骤 → `st.done` 翻转 → `recompute(p)` → `S.save()` → 重渲染；进度条与下一步实时更新。
- `buildView`：有 stages 用 `compute`，否则回退原字段。

---

## 6. 约束遵守

- 未改动数据契约 `pgwb_data_v1` 的顶层键与已有字段；仅新增字段（向后兼容）。
- 未触碰英语学习 / AI 学习 / 财富 / 身体 / TodayAgent / RuleEngine / LearningSource / RemoteSource / PlannerEngine / Memory Engine / LLM / 联网 / Prompt。
- UI 沿用现有设计体系（card / field / btn / tool-row / tag / barr 等），未引入新视觉语言。
- PWA、版本检测（`version.json` → `1.3.3`）保持有效。
- 运行时版本 `version.json` → `1.3.3`。
