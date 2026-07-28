# Development.md — 开发类 Prompt（给未来 AI 协助开发用）

> 本文件定义「用 AI 协助开发本项目」时的统一 Prompt 框架。**任何 AI 在修改本仓库前，应先读 `AI_RULES.md` 与 `PROJECT.md`，并优先套用下列 Prompt。**

## 作用

让未来接手项目的 AI（或新会话）按统一规范、低风险地开发，避免破坏业务/UI/数据契约。

## 适用场景

- 新增功能、修改功能、修 Bug、UI 优化、重构等开发任务。
- 作为「开发子 agent / 新会话」的启动 Prompt 模板。

## 输入

- 任务描述（用户需求）
- 当前代码上下文（相关模块 `U/S/Charts/AI/Pages/App`）
- 约束来自 `AI_RULES.md`（禁止项、流程、Commit 规范）

## 输出

- 方案说明 + 改动清单 + 自测结论；必要时同步更新文档（PROJECT/CHANGELOG/TODO）。

## 规划中的 Prompt（待按 PromptGuide 模板补全）

### 新增功能 Prompt
- 简述：明确需求边界 → 确认是否触及 `AI_RULES.md` 禁止项 → 设计 → 实现 → 自测 → 同步文档 → 提交。

### 修改功能 Prompt
- 简述：定位现有逻辑 → 最小化改动 → 回归检查（不波及其他模块）。

### Bug 修复 Prompt
- 简述：复现 → 定位根因 → 修复 → 加防御 → 验证；禁止顺手重构。

### UI 优化 Prompt
- 简述：除非用户显式要求，禁止改配色/布局/动画；改动须遵循设计系统 CSS 变量。

### 重构 Prompt
- 简述：保持外部行为不变；先读 `PROJECT.md` 数据契约；分步提交。

## 后续待完善内容

- [ ] 补全 5 个开发 Prompt 的完整模板（含 Role/Goal/Constraints）。
- [ ] 把「禁止项清单」固化为开发 Prompt 的常驻 Constraints。
- [ ] 定义「何时必须停下来向用户确认」的触发条件。
