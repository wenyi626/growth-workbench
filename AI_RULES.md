# AI_RULES.md — AI 开发规范

> 本文件约束**所有 AI 助手（包括未来的新会话）**在修改本项目时的行为边界与流程。
> 任何 AI 在动手前，必须先读完 PROJECT.md 与本文档。

## 1. 绝对禁止的改动（未经用户明确授权）

以下改动属于「破坏性 / 体验回归」，**默认禁止**，必须用户显式要求才可执行：

1. **业务逻辑**：任何 `S`（数据层）、`AI`、`Pages`、`App` 的计算 / CRUD / 路由逻辑。
2. **UI / 页面布局**：6 标签结构、卡片流、导航、弹层结构。
3. **配色 / 主题**：CSS 变量、深浅色主题、主色（深蓝+绿+白）体系。
4. **动画 / 过渡**：任何 `transition` / `animation` / 交互反馈。
5. **交互行为**：点击、手势、表单提交、提示（toast）的既有行为。
6. **数据契约**：`pgwb_data_v1` / `pgwb_settings_v1` 的顶层键与字段（增字段可向后兼容；**删除/重命名字段、改嵌套结构** 须用户确认 + CHANGELOG 记录 + 迁移逻辑）。
7. **影响 GitHub Pages / PWA**：不得让部署失效、`sw.js` 缓存策略退化、manifest 失效。

> 简单说：**「只做被要求做的事」**。文档任务就只写文档；部署任务就只部署；不要顺手「优化」UI 或数据结构。

## 2. 标准开发流程（每次任务都执行）

```
1. 分析（Analyze）   → 读 PROJECT/AI_RULES/TODO/CHANGELOG，确认范围与约束
2. 确认（Confirm）   → 若范围模糊或触及第 1 节禁止项，先问用户，不要猜
3. 修改（Modify）     → 仅在授权范围内改动，保持单文件自包含
4. 自测（Self-check） → 静态检查、确认 PWA/Pages 不受影响、确认无破坏
5. 更新文档（Docs）   → 同步 PROJECT/VISION/TODO/CHANGELOG/README（如涉及）
6. 提交（Commit）     → 按第 4 节规范写 commit message
7. 推送（Push）       → 推到 origin/main（需有效 GitHub Token）
8. 汇报（Report）     → 列出改动文件、每个文件作用、后续事项
```

## 3. 文档同步规则（强制）

- **每次功能完成**：必须更新 `PROJECT.md`（长期记忆）与 `CHANGELOG.md`（版本记录）。
- 涉及需求变动：更新 `TODO.md`（移动优先级 / 标记完成）。
- 涉及愿景/定位：更新 `VISION.md`。
- 文档改动本身用 `docs:` 前缀提交。

## 4. Commit 规范

| 前缀 | 含义 |
| --- | --- |
| `feat` | 新功能 |
| `fix` | 修复 Bug |
| `refactor` | 重构（不改外部行为） |
| `docs` | 仅文档 |
| `style` | 仅格式/空格（**非配色/非 UI 视觉**） |
| `perf` | 性能优化 |

示例：
- `feat: 版本自动检测与更新提示`
- `fix: 财富图表在暗色下文字不可见`
- `docs: initialize project documentation system`
- `refactor: 抽离图表配色到 CSS 变量（不改变外观）`

## 5. 版本标签规范

- 正式发版在 `main` 打轻量 tag：`v1.0` / `v1.1` / `v2.0` …（语义化：次版本=功能增量，主版本=重大架构/愿景跃迁）。
- 开发态 `version.json` 的 `version` 字段保持 `dev`，发版时改为对应 `vX.Y`。
- 每次发版在 CHANGELOG.md 追加条目，并更新 PROJECT.md 第 2 节。

## 6. 新会话 / 上下文恢复流程

出现以下任一情况：**「400 input length too long」/ 上下文被重置 / 开启新聊天**，立即执行：

1. 依次阅读：`PROJECT.md` → `VISION.md` → `TODO.md` → `CHANGELOG.md` → `AI_RULES.md` → `README.md`。
2. `git log --oneline -10` 与 `git status`，核对当前代码与未提交改动（注意本地可能有未提交的实验性改动）。
3. 确认本次任务是否允许触及第 1 节禁止项。
4. 按第 2 节流程执行，完成后同步文档再提交。

## 7. 安全红线

- **严禁在前端硬编码任何 API Key / Token / 密码。**
- 若要接入联网大模型，必须经后端代理；密钥只存在于服务端。
- 不修改任何会泄露用户数据的逻辑。
- 涉及 Git 推送的 Token 属用户私密，用完即弃，不写入仓库、不写入文档、不回显到对话。

## 8. 技术约定速记

- 单文件 `index.html` 自包含；所有 CSS/JS 内联。
- 模块挂在 `window`：`U` `S` `Charts` `AI` `EnglishMod` `Pages` `App`。
- 图表用手写 SVG（`Charts.donut/line/bar`），不引入图表库。
- 持久化用 `localStorage`，失败时回退内存。
- AI 当前为本地规则（`AI.*`），非联网模型。
