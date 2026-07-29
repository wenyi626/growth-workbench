# 架构：TrendSource / TrendLibrary（V1.5.0 Hot Trends Foundation）

> 内容中心（Content）升级的联网热点层。仿 `RemoteSource`，但目标对象是「热点」而非「学习内容」。

## 1. 位置与依赖
- 文件：`index.html` 内 `window.TrendSource`（含 `window.TrendLibrary` 查询门面）。
- 启动钩子：`App.load()` 中紧接 `LearningSource.loadRemote()` 之后，非阻塞调用 `TrendSource.loadRemote()`，完成后 `App.refresh()`。
- **不影响** `LearningSource` / `Library` / `ProjectLibrary`；**不写** `pgwb_data_v1`。

## 2. 数据流
```
App 启动（非阻塞）
  └─ TrendSource.loadRemote()
       ├─ fetch ./data/trends-daily.json
       │    ├─ 成功 → normalize（cat 路由，id 前缀 tr-<cat>-）→ TrendLibrary 注入 + 写缓存
       │    └─ 失败 → 读 pgwb_trends_cache_v1（上次成功缓存）
       │         └─ 仍失败 → 回退 LOCAL_FALLBACK（内置 6 条，标「离线·本地热点」）
  └─ 内容中心「热点」页渲染（读 TrendLibrary）
```

## 3. 模块接口
### TrendSource
- `load()`：同步返回 0（不阻塞启动，远程走 `loadRemote`）。
- `loadRemote()`：返回 Promise；成功返回条数，缓存命中返回 `-1`，本地兜底返回 `-2`，全失败返回 `0`。

### TrendLibrary（window.TrendLibrary）
- `all()` / `byCat(cat, limit)` / `today(limit=5)` / `weekly(limit=10)` / `search(q)`。
- `freshnessText()`：返回新鲜度文案（`已更新` / `缓存·N 天前` / `离线·本地热点`）。
- 排序一律按 `trendScore` 降序。

## 4. 归一化与 id 隔离
- `normalize` 强制 `id = 'tr-' + cat + '-' + (o.id || slug(hot))`，与本地 `en-/ai-/tpl-/ren-*` 命名空间互斥，杜绝后写覆盖。
- 合法 `cat`：`ai` / `tech` / `investment` / `xhs`；非法直接丢弃。

## 5. 缓存
- 键：`pgwb_trends_cache_v1`（与 `pgwb_data_v1` 完全独立）。
- 值：`{ generatedAt, cachedAt, trends }`。
- 新鲜度：≤24h 正常；1–7 天软提示；>7 天强提示（内容仍可看，不删）；无网保留旧缓存；无缓存无网回退本地兜底。

## 6. 数据来源（CI 生成，真实抓取）
- AI / 科技：Hacker News Algolia API、arXiv RSS、GitHub Search API、科技媒体 RSS。
- 投资：**财经 RSS（无实时行情拉取）**——实时行情留待未来版本。
- 小红书：**人工维护** `data/xhs-manual.json`（无公开 API，禁止直抓）。
- LLM（仅 CI Secrets）**只生成** `whyWorthWriting / fitAccount / angle / titles`，不虚构热点。

## 7. 降级表
| 情况 | 行为 |
|---|---|
| 远程 JSON 成功 | 注入 + 写缓存，提示「已更新」 |
| 远程失败 / 离线 | 用 `pgwb_trends_cache_v1`，提示「缓存·N 天前」 |
| 缓存也无 | 内置 LOCAL_FALLBACK，提示「离线·本地热点」 |
| 单条格式错误 | `validate` 失败跳过该条（仿 `RemoteSource.validate`） |

## 8. 主题去重（连续 7 天窗口，防霸榜）
目标：避免「OpenAI / OpenAI / Claude」连续多天霸榜，保障新鲜度与主题多样性。

### 去重依据（themeKey）
- `themeKey(hot)`：文本小写后，若命中已知品牌/实体词表（`openai/claude/github/小红书/比特币/…`，约 40 个，中英兼顾），返回该词；否则取前 6 个有效字符（去标点）作为主题键。
- 前端去重键为 `cat + '|' + themeKey(hot)`（不同分类的同名主题互不冲突，如 AI 的 OpenAI 与投资的 OpenAI 概念股）。

### 前端安全网（TrendSource.dedupeByTheme）
- `byCat / today / weekly` 查询时，对按 `trendScore` 降序的结果做 `dedupeByTheme`：同一 `cat|主题` 仅保留第一条（最高分），其余折叠。
- 作用：即便缓存/网络数据含同日重复，UI 也不重复展示。

### CI 跨天降权（scripts/gen_trends.py + data/trends-history.json）
- 维护滚动历史 `data/trends-history.json = { days: [ {date, themes[]} ] }`，每轮 CI 把**当日发布的主题**追加进去，并 `prune_history` 仅保留最近 7 天（严格 > 今天-7）。
- `cross_day_adjust(items, history, today)`：统计窗口内各主题出现次数——
  - 出现 **≥3 次** → 直接剔除（过度覆盖）；
  - 出现 **1–2 次** → `trendScore = max(45, 原分 - 8×次数)`（降权，仍可见但后排）；
  - 0 次 → 不动。
- `same_day_dedup(items)`：同一天同 `cat|主题` 仅保留 `trendScore` 最高的一条。
- 优先级：先跨天降权/剔除 → 再同日去重 → 再按分排序 → 取各分类规模上限。
- **7 天窗口实现**：完全落在 CI 端（前端无跨天记忆）；前端 `dedupeByTheme` 作为实时安全网兜底当日重复。

## 9. 半成品草稿提纲（模板化，不调用 LLM）
- 触发：内容中心热点卡「用这个选题创作」→ `createFromTrend()`。
- `buildOutline(trend)` 按固定模板拼接（纯字符串，无网络/无 LLM）：
  ```
  【开头】为什么最近很多人在讨论这个？
  最近「<hot>」频繁出现在各类讨论里。<summary/whyHot>
  【正文】
  1. 热点是什么？<hot>（<summary>）
  2. 为什么重要？<whyWorthWriting>
  3. 对普通人有什么影响？<angle>
  【结尾】我的观点是什么？
  <angle>
  ```
- 结果写入内容记录 `outline` 字段；打开 `addContent` 编辑弹窗时预填进「内容提纲」文本框，用户可继续编辑；详情弹窗同步展示。
- 价值：用户进入内容库即拥有一篇**可继续编辑的半成品草稿**，而非空白记录；零 API 成本、零延迟。

