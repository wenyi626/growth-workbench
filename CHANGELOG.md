# CHANGELOG.md — 版本记录

> 格式参考 [Keep a Changelog](https://keepachangelog.com/)。版本号规范：`v1.0` / `v1.1` / `v2.0` …；开发态 `version.json` 为 `dev`。
> 每次发版必须在此追加条目，并更新 PROJECT.md 第 2 节「当前版本」。

## [未发布] dev（本地）

### 进行中 / 本地已实现未提交
- **版本自动检测与更新弹窗**：新增 `version.json`、`index.html` 内联检测脚本（发现新版本 → 立即更新 / 稍后更新）、`icon-1024.png`；`manifest.json` 主题色改为深蓝 `#16335c`、背景色 `#f4f7fb`。
  - 状态：**本地改动在 working tree，尚未单独提交**（按文档任务约定未纳入本次 `docs` 提交）。待补全 `sw.js` 的 `skipWaiting` 消息处理后，以 `feat:` 单独提交。

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
