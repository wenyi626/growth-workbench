# Decision Engine 决策引擎（v1.2.0）

> 本文档描述首页「AI CEO Dashboard（Today OS）」背后的**决策架构**。
> 核心原则：**所有建议都由 RuleEngine 统一决策**，LLM 只负责解释与细化，绝不参与决策。

---

## 1. 架构总览

决策层与展示层彻底解耦。首页 `TodayAgent` 不再自行"拍脑袋"生成建议，而是向 `RuleEngine` 要一份排好序的建议列表，再负责排版展示。

```
┌─────────────────────────────────────────────────────────────┐
│  数据层 S.data (localStorage: 学习/资产/运动/内容/复盘/体重…)   │
└───────────────┬──────────────┬──────────────┬───────────────┘
                │              │              │
        ┌───────▼──────┐ ┌─────▼──────┐ ┌────▼───────┐   （更多 Rule 可平行扩展）
        │  StudyRule   │ │ WealthRule │ │ FitnessRule │
        └───────┬──────┘ └─────┬──────┘ └────┬───────┘
                │              │              │
        ┌───────▼──────┐ ┌─────▼──────┐      │
        │  MediaRule   │ │ FutureRule │      │
        └───────┬──────┘ └─────┬──────┘      │
                │  每个 evaluate(d) 返回 Suggestion[]  │
                └──────────────┬─────────────┘
                               │  聚合 + 排序
                        ┌──────▼───────┐
                        │  RuleEngine  │  ← 唯一决策中心
                        │ getSuggestions() │
                        └──────┬───────┘
                               │  排序后 Suggestion[] (priority↓, estimatedTime↑)
                        ┌──────▼───────┐
                        │  TodayAgent  │  只消费、只排版展示
                        │ getDashboard() │  Top3 = action 优先
                        └──────┬───────┘
                               │
                        ┌──────▼───────┐
                        │  Pages.today │  9 段式 AI CEO Dashboard
                        └──────────────┘

        （未来）LLM 位置：在 RuleEngine 输出之后，仅做"解释/细化"装饰层，
         不参与排序与增删，决策权始终在 RuleEngine。
```

---

## 2. RuleEngine 如何工作

`RuleEngine` 是**唯一决策中心**，职责只有一个：把分散在各 `Rule` 里的判断，聚合成一份统一的、排好序的建议列表。

```js
window.RuleEngine = (function () {
  function aggregate() {
    var d = S.data;
    return []
      .concat(window.StudyRule.evaluate(d))
      .concat(window.WealthRule.evaluate(d))
      .concat(window.FitnessRule.evaluate(d))
      .concat(window.MediaRule.evaluate(d))
      .concat(window.FutureRule.evaluate(d));
  }
  function getSuggestions() {
    var list = aggregate();
    list.sort(function (a, b) {
      if (b.priority !== a.priority) return b.priority - a.priority;   // 优先级高者在前
      return (a.estimatedTime || 0) - (b.estimatedTime || 0);          // 同优先级：耗时短的优先
    });
    return list;
  }
  return { getSuggestions: getSuggestions };
})();
```

工作流程：

1. **聚合**：依次调用每个 Rule 的 `evaluate(S.data)`，把返回的 `Suggestion[]` 拼成一个大列表。
2. **排序**：先按 `priority` **降序**（数值越大越紧急），同级再按 `estimatedTime` **升序**（先做耗时短的）。
3. **输出**：返回排序后的完整列表；`TodayAgent` 取前 3 条 `action` 作为「今日三件」，不足则用 `opportunity` / `risk` 补齐。

> 扩展新维度时，只需新增一个 `XxxRule` 并在 `aggregate()` 里 `.concat(window.XxxRule.evaluate(d))` 一行即可，无需改动 `TodayAgent` 或页面。

---

## 3. Rule 的职责与契约

每个 `Rule` 是一个挂在 `window` 上的 IIFE，暴露唯一方法：

```js
window.StudyRule = (function () {
  function evaluate(d) {
    // d = S.data，读真实数据，产出 0..n 条 Suggestion
    return [ /* Suggestion, ... */ ];
  }
  return { evaluate: evaluate };
})();
```

- 输入：`d`（即 `S.data`，全量业务数据）。
- 输出：`Suggestion[]`（统一结构，见第 4 节）。
- 约束：**只读取、不写入**数据；不调用 UI；不做网络请求；不依赖 LLM。

### 各 Rule 职责明细

| Rule | 真实信号（来自 S.data） | 触发逻辑 | 产出 |
| --- | --- | --- | --- |
| `StudyRule` | `learning[].date` 最近学习日期 | 距今天数 `gap ≥ 2` | `action` p5「今天优先学习英语」(est 30min) |
| `WealthRule` | `assets[]` 现金/货基占比、`wealthSnapshots[].date` | 现金占比 > 目标+5 → `risk` p4；快照 `gap > 30` 天 → `action` p3；常驻 `opportunity` p3「市场回调时低位补仓」 | 1–3 条 |
| `FitnessRule` | `exercises[].date`、`weights[]` 体重趋势 | 运动 `gap ≥ 3` → `action` p5；体重连升 3 次 → `action` p4；常驻 `opportunity` p3「适合一次高质量有氧」 | 1–3 条 |
| `MediaRule` | `contents[].date`、`reviews[].date` | 发布 `gap ≥ 3` → `action` p4；复盘 `gap ≥ 7` → `risk` p4；常驻 `opportunity` p3「AI 做产品选题互动高」 | 1–3 条 |
| `FutureRule` | （预留）投资/职业等高级信号 | 当前为空桩 `return []` | 0 条（占位） |

> 阈值（如 `gap ≥ 2`、`> 目标+5`、`≥ 3`）与建议文案当前为**硬编码**，属于"Mock 风格"的配置，未来可抽成 `settings` 或交由 LLM 细化（见第 6 节）。

---

## 4. Suggestion 数据结构

所有 Rule 产出的都是同一个结构，保证 `RuleEngine` 可无差别聚合与排序：

```js
{
  id:            "study-gap",        // 规则内唯一标识（字符串）
  title:         "今天优先学习英语",  // 一句话建议标题（用于 Top3 / 卡片）
  description:   "已经连续 2 天未学习…", // 补充说明
  category:      "action",           // 枚举：action(行动) / risk(风险) / opportunity(机会)
  priority:      5,                  // 1–5，越大越紧急（排序主键）
  reason:        "已经连续 2 天未学习英语", // 触发原因（用于解释/可解释性）
  estimatedTime: 30,                 // 预计耗时（分钟），排序次键；0 表示无明确耗时
  source:        "StudyRule",        // 来源 Rule（用于 TodayAgent 按维度取 advice）
  status:        "open"              // 状态：open / done（预留）
}
```

字段语义：

- **category**：决定首页如何分组展示——`action` 进「今日三件」，`risk` 进「今日最大风险」，`opportunity` 进「今日最大机会」。
- **priority**：决策核心排序键。`TodayAgent` 的 Top3 以 `action` 优先，不足再用 `opportunity`/`risk` 补齐。
- **reason / source**：为"可解释决策"预留——未来 LLM 解释时可直接引用，也能按 `source` 反查是哪条规则触发。

---

## 5. 目前哪些规则是真实的，哪些是 Mock

| Rule | 数据来源 | 真实性 | 说明 |
| --- | --- | --- | --- |
| `StudyRule` | `S.data.learning`（真实） | **真实规则** | 间隔天数由真实学习记录计算；仅文案/阈值为硬编码 |
| `WealthRule` | `S.data.assets` / `wealthSnapshots`（真实） | **真实规则** | 占比、新鲜度由真实数据算；"市场回调补仓"机会文案为硬编码 |
| `FitnessRule` | `S.data.exercises` / `weights`（真实） | **真实规则** | 运动间隔、体重连升由真实数据算；机会文案为硬编码 |
| `MediaRule` | `S.data.contents` / `reviews`（真实） | **真实规则** | 发布/复盘间隔由真实数据算；机会文案为硬编码 |
| `FutureRule` | 无 | **纯占位 Mock** | `return []`，等待未来真实信号接入 |

结论：

- **决策逻辑是真的**——建议是否出现、优先级高低，全部由用户的真实数据缺口驱动，不是随机 Mock。
- **表达层是 Mock 风格**——具体的建议话术、阈值数字是写死的常量，尚未个性化，也未接 LLM。
- `TodayAgent` 中仅保留 `ONE_LINERS`（每日一句）与 `greeting`（问候语）为静态文案，它们**不是建议**，不参与 `RuleEngine` 决策；其余首页建议 100% 来自 `RuleEngine`。

---

## 6. 未来如何接入 OpenAI（重点：LLM 不决策）

未来引入大模型时，架构不变，LLM 只作为 `RuleEngine` 输出之后的**解释/细化装饰层**：

```
RuleEngine.getSuggestions()  ──▶  Suggestion[]  ──▶  [LLM 装饰层：解释 + 个性化细化]  ──▶  TodayAgent
        （决策：增/删/排序）              （事实）           （只改写文字，不动决策）        （消费展示）
```

集成要点（严格遵守）：

1. **决策权归 RuleEngine**：`RuleEngine` 继续负责是否给出建议、`priority` 排序、`Top3` 选取。LLM **不得**自行生成、新增、删除或重新排序建议。
2. **LLM 只做两件事**：
   - **解释（Explain）**：把 `reason` / `source` 翻译成更口语、更贴合用户背景（profile）的自然语言。
   - **细化（Refine）**：在 `title` / `description` 上做个性化润色（结合 `profile.longTermGoals`、`interests`），但不改变 `category` / `priority` / `estimatedTime` 等决策字段。
3. **前端禁硬编码 Key**：OpenAI 调用必须经**后端代理**（避免在前端暴露 API Key），调用边界与降级策略写入 `AI_RULES.md`。
4. **保留本地规则降级**：LLM 不可用时，`RuleEngine` 的原生 `Suggestion[]` 直接展示，体验不退化。
5. **Prompt 来源**：解释/细化用的 Prompt 统一放在 `docs/Prompt/`（如 `Home.md` / `Study.md`），不在 `index.html` 写死。

> 一句话：**OpenAI 不负责"该不该做、先做哪个"，只负责"用大白话把这事说清楚、说到用户心坎里"。** 决策引擎是唯一大脑，LLM 是它的嘴。

---

## 7. 自检清单（v1.2.0）

- [x] `TodayAgent` 不再自行生成 `Suggestion`，仅调用 `RuleEngine.getSuggestions()`。
- [x] `RuleEngine` 为唯一决策中心，聚合 5 个 Rule 并统一排序。
- [x] 每个 Rule 返回统一 `Suggestion[]` 结构。
- [x] 排序规则：priority 降序 → estimatedTime 升序；Top3 以 action 优先。
- [x] 前 4 个 Rule 由真实数据缺口驱动；`FutureRule` 为空桩。
- [x] 未接入任何 LLM；未来接入仅做解释/细化。
- [x] 其余 5 个页面、localStorage 数据契约、PWA、路由均未改动。
