# CHANGELOG.md — 版本记录

> 格式参考 [Keep a Changelog](https://keepachangelog.com/)。版本号规范：`v1.0` / `v1.1` / `v2.0` …；开发态 `version.json` 为 `dev`。
> 每次发版必须在此追加条目，并更新 PROJECT.md 第 2 节「当前版本」。

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
