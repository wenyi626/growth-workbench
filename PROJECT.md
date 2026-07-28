# PROJECT.md — 个人成长工作台（长期记忆）

> 本文件是项目的**唯一长期记忆**。任何重要修改完成后，都必须同步更新本文件以及对应的 README / VISION / TODO / CHANGELOG / AI_RULES。
> 新会话（或上下文被重置、出现「400 input length too long」）时，**先读这 6 份文档**，再开始任何工作。

---

## 1. 产品定位

**个人成长工作台（Growth Workbench）** 是一款**移动端优先的个人成长操作系统（Personal Growth OS）**：把「学习 / 财富 / 身体 / 自媒体」四大成长维度整合进一个 App，并用**本地规则型 AI** 做复盘、计划与建议，帮助用户获得更多人生选择权。

- 用户画像：非程序员的电商运营从业者，正在学习用 AI 解决实际问题、开发自己的产品。
- 形态：**纯前端单文件 PWA**，可安装到手机桌面、可离线使用，零后端依赖。
- 核心理念：数据归用户自己所有（localStorage 本地存储），AI 在端侧做轻量辅助，不依赖联网大模型。

---

## 2. 当前版本

| 项 | 值 |
| --- | --- |
| 当前版本号 | `1.0.0`（运行时版本源 `version.json`；v1.0.0 引入版本更新机制） |
| 最近一次提交 | `feat: version update detection and pwa update flow`（v1.0.0） |
| 发布状态 | 已部署 GitHub Pages，PWA 已可用 |
| 版本标签规范 | 正式发版使用 `v1.0`、`v1.1`、`v2.0` …（见第 13 节） |

---

## 3. 页面结构（6 个底部标签）

| 标签 | key | 主要负责模块 | 核心功能 |
| --- | --- | --- | --- |
| 🏠 今日 | `today` | `Pages.today` | 每日计划、AI 生成今日计划、复盘回顾、快捷入口 |
| 📚 学习 | `learn` | `Pages.learn` + `EnglishMod` | 学习记录（主题/分类/来源/理解度/产出）、英语模块（生成/测验/词库） |
| 💰 财富 | `wealth` | `Pages.wealth` | 资产、交易、财富快照、图表（环形/折线/柱状）、AI 财富复盘 |
| 🏃 身体 | `body` | `Pages.body` | 运动记录、体重/围度等身体指标、图表、AI 身体报告 |
| 📱 自媒体 | `content` | `Pages.content` | 内容数据（阅读/赞/藏/评/转/涨粉）、图表、AI 选题建议 |
| 👤 我的 | `profile` | `Pages.profile` | 个人资料、长期目标、兴趣、项目、自我分析、设置、数据导入导出 |

路由基于 `hash`（`#today` / `#learn` …），由 `App` 模块统一调度。

---

## 4. 技术栈

| 维度 | 方案 |
| --- | --- |
| 语言 | 原生 HTML + CSS + JavaScript（ES5/ES6 混用，兼容移动端 WebView） |
| 框架 | **无框架、无构建步骤、零运行时依赖** |
| 数据持久化 | `localStorage`（不可用时回退到内存） |
| 模块化 | 挂在 `window` 上的 IIFE 模块：`U` `S` `Charts` `AI` `EnglishMod` `Pages` `App` |
| 图表 | 手写 SVG：`Charts.donut` / `Charts.line` / `Charts.bar` |
| AI | **规则型本地「模拟 AI」**，非联网大模型（`AI.*` 为本地启发式函数） |
| PWA | `manifest.json` + `sw.js`（离线缓存外壳）、maskable 图标、iOS 启动图 |
| 托管 | GitHub Pages（main 分支根目录，HTTPS，push 自动部署） |

**重要约束**：AI 相关功能（见第 8 节）目前全部是**本地规则**，不调用任何外部大模型 API。

---

## 5. 文件结构

```
/workspace
├── index.html              # 整个应用（约 3100+ 行，内联全部 CSS/JS）
├── manifest.json           # PWA 清单（名称/图标/主题色/启动方式）
├── sw.js                   # Service Worker（离线缓存 + 导航网络优先回退）
├── version.json            # 版本号（当前为 "dev"，用于版本检测，本地）
├── icon-192.png            # PWA 图标 192
├── icon-512.png            # PWA 图标 512
├── icon-maskable-512.png   # 可遮罩图标（Android 安全区）
├── icon-1024.png           # 1024 高清明信片主图标（深蓝+白+绿）
├── apple-touch-icon.png    # iOS 主屏图标
├── splash-*.png            # 7 张 iOS 启动图（不同分辨率）
├── .gitignore
├── README.md               # 项目说明
├── PROJECT.md              # 本文件（长期记忆）
├── VISION.md               # 产品愿景
├── TODO.md                 # 需求池（P0/P1/P2）
├── CHANGELOG.md            # 版本记录
└── AI_RULES.md             # AI 开发规范
```

> 注意：`index.html` 是**单文件自包含**——所有 CSS、JS、数据种子都内联其中。`sw.js` 仅缓存静态外壳（其中 `index.html` 含全部逻辑），因此缓存它即可离线运行。

---

## 6. 数据结构（localStorage）

| 键 | 用途 |
| --- | --- |
| `pgwb_data_v1` | 全部业务数据（JSON） |
| `pgwb_settings_v1` | 设置项单独冗余存储（JSON，便于合并） |

`pgwb_data_v1` 的数据形状（`S.defaults()` 种子）：

- **profile**：`{ name, longTermGoals[], interests[], background, contentPositioning, availableTime }`
- **settings**：`{ theme: 'light'|'dark', baseCurrency: 'CNY', fx: {USD,HKD,JPY}, remindReview: bool }`
- **dailyPlans**：`{}`（按日期字符串为键）
- **learning[]**：`{ id, date, topic, category, source, summary, notes, understanding, output }`
- **projects[]**：`{ id, name, goal, stage, progress, nextAction, notes, versions[], aiChats[] }`
- **assets[]**：`{ id, name, symbol, category, currency, quantity, currentPrice, targetAllocation }`
- **transactions[]**：`{ id, date, asset, type, quantity, price, fee, exchangeRate, amount, reason, decisionType, risk }`
- **wealthSnapshots[]**：`{ id, date, totalAssets, investmentValue, cashValue, savingsContribution, investmentReturn, dividendIncome, fxImpact }`
- **exercises[]**：`{ id, date, type, duration, intensity, bodyParts[], feeling, notes }`
- **weights[]**：`{ id, date, weight, waist, hip, thigh, bodyFat, sleep, bodyState, notes }`
- **contents[]**：`{ id, date, title, topic, type, status, views, likes, saves, comments, shares, followersGained, notes }`
- **reviews[]**：`{ id, date, whatLearned, whatCompleted, whatProduced, whatToImprove, tomorrowPlan }`
- **selfAnalyses[]**：`[]`（AI 自我分析沉淀）
- **vocabBank[]**：`[]`（英语词库）

> **数据安全约束**：`pgwb_data_v1` 的顶层键集合与字段结构，属于稳定的**数据契约**。新增字段可向后兼容；**删除 / 重命名字段、改变嵌套结构** 属于破坏性变更，须经产品确认并在 CHANGELOG 记录、提供迁移逻辑（见 AI_RULES 第 4 条）。

---

## 7. 各模块公开能力（便于二次开发检索）

| 模块 | 公开方法 / 字段 |
| --- | --- |
| `U`（工具） | `todayStr` `addDays` `uid` `toast` …（日期、ID、提示等通用工具） |
| `S`（数据层） | `load` `save` `data` `setData` `add` `update` `find` `has` `length` `reset` `exportJSON` `importJSON` `restoreFromBackup` |
| `Charts` | `donut(cfg)` `line(cfg)` `bar(cfg)`（手写 SVG） |
| `AI`（本地规则） | `generateTodayPlan` `selfAnalysis` `wealthReview` `bodyReport` `parseExercise` `checkSentence` `genContentIdeas` `generateEnglish` |
| `EnglishMod` | `open` `openQuiz` `openBankQuiz` |
| `Pages` | `today` `learn` `wealth` `body` `content` `profile`（各页渲染器） |
| `App` | 路由器（hash 路由 + `refresh()` 刷新当前页） |

---

## 8. AI 能力说明（关键）

`AI` 模块是**本地规则引擎**，不联网、不调用大模型。当前能力：

- `AI.generateTodayPlan` — 根据资料/目标生成今日计划草稿
- `AI.selfAnalysis` — 基于 `selfAnalyses` 做自我分析
- `AI.wealthReview` — 财富复盘（资产/交易/快照）
- `AI.bodyReport` — 身体报告（运动/体重）
- `AI.parseExercise` — 解析自然语言运动输入
- `AI.checkSentence` — 英语句子检查
- `AI.genContentIdeas` — 生成自媒体选题
- `AI.generateEnglish` — 英语生成（配合 `EnglishMod`）

> 若未来要接入**真实大模型 API**，属于重大架构变更：需新增后端代理（避免在前端暴露密钥）、定义调用边界、保持离线降级，并在 AI_RULES 中记录规范。**当前严禁在前端硬编码任何 API Key。**

> **Prompt 管理**：所有 AI Prompt 已从代码中独立，统一维护在 `docs/Prompt/`（`PromptGuide.md` 定义规范，各模块一个文件）。未来接入真实模型时，Prompt 从此目录读取，不在 `index.html` 写死。

---

## 9. 已完成功能（截至 `d98691c`）

- [x] 单文件应用骨架 + 6 标签移动端布局（明/暗主题）
- [x] 数据层 `S`：localStorage 持久化 + 种子数据 + CRUD + 导入导出 + 重置
- [x] 今日：每日计划、AI 今日计划、复盘
- [x] 学习：学习记录（分类/理解度/产出）+ 英语模块（生成/测验/词库）
- [x] 财富：资产、交易、财富快照、环形/折线/柱状图、AI 财富复盘
- [x] 身体：运动记录、身体指标、图表、AI 身体报告
- [x] 自媒体：内容数据追踪、图表、AI 选题
- [x] 我的：资料、长期目标、项目、自我分析、设置（主题/币种/汇率）、数据导入导出
- [x] PWA：manifest + Service Worker 离线 + 图标（192/512/maskable/1024）+ iOS 启动图
- [x] GitHub Pages 部署（main 根目录，HTTPS）
- [x] 版本自动检测与「发现新版本」弹窗 + PWA `skipWaiting` 更新流（v1.0.0）
- [x] AI Prompt 管理体系（`docs/Prompt/`，9 个文件 + `PromptGuide.md` 规范）

---

## 10. 已知 Bug / 待确认

| 状态 | 说明 |
| --- | --- |
| ⚠️ | `/__backup`（云端备份）后端不存在，`S.backupToCloud` / `restoreFromBackup` 会静默失败，仅影响云端同步，不影响本地使用 |
| ⚠️ | 种子数据含示例资产/交易/内容，首次使用需用户自行清空或覆盖 |
| 🔍 | iOS 启动图在不同机型 safe area 适配待真机验证 |

---

## 11. UI 设计规范（不可擅自修改）

- 设计系统使用 CSS 变量（`:root` 与 `[data-theme="dark"]`）定义颜色/间距/圆角/阴影。
- 主色为**深蓝 + 少量绿色 + 白**；图标 `icon-1024.png` 为深蓝圆角矩形 + 白色上箭头 + 绿色点。
- 移动端优先：底部 6 标签导航，单列卡片流。
- 任何配色、间距、动画、交互的改动都属于「UI 变更」，须经确认（见 AI_RULES 第 3 条）。

---

## 12. 后续开发路线（Roadmap）

1. **v1.0（已达成）**：文档体系 + 版本自动检测与 PWA 更新流（见 v1.0.0）。下一步：数据契约冻结。
2. **v1.1**：真实选型/复盘增强、内容多平台、英语词库同步。
3. **v2.0（愿景）**：「AI Personal CEO」——端侧 AI 自动串联四大维度，给出每日优先级与行动建议。详见 VISION.md。

---

## 13. Commit / 版本规范（摘要，详见 AI_RULES.md）

- Commit 类型前缀：`feat` / `fix` / `refactor` / `docs` / `style` / `perf`。
- 正式发版打 tag：`v1.0`、`v1.1`、`v2.0` …；当前开发态 `version.json` 为 `dev`。
- 每次功能完成：改代码 → 自测 → **更新 PROJECT/CHANGELOG/TODO** → commit → push → 汇报。

---

## 14. 新会话恢复流程（必读）

当出现以下任一情况：**上下文被重置 / 模型提示「400 input length too long」/ 开启新聊天**，请按顺序执行：

1. 依次阅读：`PROJECT.md` → `VISION.md` → `TODO.md` → `CHANGELOG.md` → `AI_RULES.md` → `README.md`。
2. 运行 `git log --oneline -10` 与 `git status` 确认当前代码与未提交改动。
3. 确认本次任务范围（是否允许改 UI/数据契约）。
4. 按 AI_RULES 的「开发流程」执行，完成后同步更新文档再提交。

## 15. AI Prompt 管理体系（docs/Prompt/）

- 所有 AI Prompt 已从代码中独立，统一维护在 **`docs/Prompt/`** 目录（规范见 `docs/Prompt/PromptGuide.md`）。
- 规范：`PromptGuide.md` 定义统一模板（Role / Goal / Context / Input / Constraints / Output）与命名/新增规则；`AI.md` 为总体行为规范。
- 模块文件：`Home` / `Study` / `Wealth` / `Fitness` / `Media` / `Review`（对应六大业务模块），`Development.md` 为开发类 Prompt。
- 现状：当前 `AI.*` 为本地规则；未来接入真实模型时，Prompt 从此目录读取，不在 `index.html` 写死。
- 维护：新增/调整 Prompt 改 `docs/Prompt/` 文件并同步 `CHANGELOG.md`，**不修改业务代码**（见 `AI_RULES.md`）。
