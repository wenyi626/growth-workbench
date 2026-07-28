# 个人成长工作台（Growth Workbench）

> 移动端优先的个人成长操作系统：把 **学习 / 财富 / 身体 / 自媒体** 整合进一个可安装、可离线的 PWA，并用**端侧 AI** 做复盘与计划。

[![GitHub](https://img.shields.io/badge/GitHub-wenyi626/growth--workbench-blue)](https://github.com/wenyi626/growth-workbench)
[![License: 自用项目](https://img.shields.io/badge/license-个人自用-brightgreen)](#)

- 🌐 **在线访问**：https://wenyi626.github.io/growth-workbench/
- 📱 **安装到桌面**：用手机浏览器打开 → 添加到主屏幕 → 以独立 App 运行（支持离线）。

---

## ✨ 功能一览

| 模块 | 功能 |
| --- | --- |
| 🏠 今日 | 每日计划、AI 生成今日计划、复盘回顾 |
| 📚 学习 | 学习记录（主题/分类/理解度/产出）+ 英语模块（生成/测验/词库） |
| 💰 财富 | 资产、交易、财富快照、图表、AI 财富复盘 |
| 🏃 身体 | 运动记录、身体指标、图表、AI 身体报告 |
| 📱 自媒体 | 内容数据追踪、图表、AI 选题建议 |
| 👤 我的 | 资料、长期目标、项目、自我分析、设置、数据导入导出 |

图表均为**手写 SVG**（环形 / 折线 / 柱状），AI 为**本地规则引擎**（不联网、不调用大模型）。

---

## 🛠 技术栈

- 原生 **HTML + CSS + JavaScript**，**无框架、无构建步骤、零运行时依赖**。
- 数据持久化：`localStorage`（不可用时回退内存）。
- PWA：`manifest.json` + `sw.js` 离线缓存 + maskable 图标 + iOS 启动图。
- 托管：**GitHub Pages**（main 分支根目录，HTTPS，push 自动部署）。

---

## 🚀 本地运行

无需安装任何依赖，两种任选：

```bash
# 方式一：直接用浏览器打开
open index.html        # macOS
# 或把 index.html 拖进浏览器

# 方式二：起一个静态服务器（推荐，Service Worker 需在 http(s) 下生效）
python3 -m http.server 8080
# 然后访问 http://localhost:8080
```

> 注意：PWA / Service Worker / 离线 能力需在 `http(s)` 下才生效，直接 `file://` 打开只能看界面。

---

## 📁 项目结构

```
index.html             # 整个应用（单文件自包含，内联全部 CSS/JS）
manifest.json          # PWA 清单
sw.js                  # Service Worker（离线缓存）
version.json           # 版本号（开发态为 dev）
icon-*.png             # 各尺寸 PWA 图标（深蓝+白+绿）
splash-*.png           # iOS 启动图
PROJECT.md             # 项目长期记忆（核心）
VISION.md              # 产品愿景（AI Personal CEO）
TODO.md                # 需求池（P0/P1/P2）
CHANGELOG.md           # 版本记录
AI_RULES.md            # AI 开发规范（边界与流程）
```

---

## 📚 文档体系

| 文件 | 作用 |
| --- | --- |
| `PROJECT.md` | **唯一长期记忆**：定位、版本、页面、技术栈、文件结构、数据结构、AI 能力、已完成/已知问题/路线 |
| `VISION.md` | 产品愿景：「AI Personal CEO」与四维度模型 |
| `TODO.md` | 需求池，按 P0/P1/P2 优先级维护 |
| `CHANGELOG.md` | 版本记录，发版必更 |
| `AI_RULES.md` | **AI 开发规范**：禁止项、开发流程、Commit/版本规范、新会话恢复流程 |

---

## 🔒 数据与隐私

- 所有数据保存在**你自己的浏览器** `localStorage` 中（`pgwb_data_v1` / `pgwb_settings_v1`）。
- 支持在「我的」页**导出 / 导入 JSON**，以及重置。
- 未配置任何外部后端；云端备份（`/__backup`）当前为占位，不影响本地使用。

---

## 🗺 路线图

- **v1.0**：文档体系 + 版本自动检测 + 数据契约冻结。
- **v1.1**：财富/英语/自媒体/身体增强。
- **v2.0（愿景）**：AI Personal CEO —— 端侧 AI 自动串联四维度，给出每日优先级与行动建议。

详见 [VISION.md](./VISION.md) 与 [TODO.md](./TODO.md)。
