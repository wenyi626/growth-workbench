# PromptGuide.md — AI Prompt 管理规范

> 本目录统一保管「个人成长工作台」所有 AI Prompt。**以后所有 AI 能力应尽量使用本目录维护的 Prompt，而不是直接写死在代码里。**

## 1. 为什么要统一管理

- **调整 AI 行为**：改一个 md 文件即可，不必动 `index.html` 业务代码。
- **更换 AI 模型**：Prompt 与模型解耦；切换模型/供应商时只改调用层。
- **维护 Prompt**：版本可读、可 diff、可评审，Prompt 演进有迹可循。
- **新 AI 快速接手**：新会话/新同学先读本目录即知每个 AI 能力的设计意图。

> 现状说明：当前 App 的 `AI.*`（`generateTodayPlan` / `wealthReview` / `bodyReport` / `genContentIdeas` / `checkSentence` / `selfAnalysis` / `parseExercise` / `generateEnglish`）均为**本地规则引擎**，未调用真实大模型。本目录是**未来接入真实模型时的统一 Prompt 来源**，也是规则逻辑的「设计契约」。

## 2. 目录结构

```
docs/Prompt/
├── PromptGuide.md   # 本规范（必读）
├── AI.md            # App 内 AI 总体行为规范
├── Home.md          # 首页 / 今日
├── Study.md         # 学习模块（英语 / AI / 阅读 / 规划 / 推荐）
├── Wealth.md        # 财富模块
├── Fitness.md       # 身体模块
├── Media.md         # 自媒体模块
├── Review.md        # 每日复盘
└── Development.md   # 开发类 Prompt（给未来 AI 协助开发用）
```

## 3. 每个 Prompt 的用途

- 每个文件对应一个**业务模块**或一类**场景**。
- 每个 `### 子标题` 是一个**独立的 Prompt 单元**（一个具体 AI 能力）。
- Prompt 只描述「角色 / 目标 / 上下文 / 输入 / 约束 / 输出」，不绑定具体代码实现。

## 4. 命名规范

- **文件名**：模块英文名，首字母大写，如 `Wealth.md`、`Media.md`。
- **Prompt 单元**：用 `###` 二级标题，语义化命名（如 `### 仓位分析`、`### 小红书选题`）。
- **状态标注**（可选，写在单元内）：`状态: 规划中 | 草稿 | 在用 | 已废弃`。
- **版本**（可选）：`版本: v0.1`。
- 不在代码里硬编码 Prompt 文本；代码只引用「模块 + Prompt 单元名」。

## 5. 以后新增 Prompt 的规则

1. 先判断属于哪个模块，写入对应文件；跨模块或通用规范放进 `AI.md`。
2. **必须**使用下方统一模板（Role / Goal / Context / Input / Constraints / Output）。
3. 单元内标注状态与适用场景，便于评审。
4. 新增后同步更新 `CHANGELOG.md` 与 `PROJECT.md` 的 Prompt 清单。
5. 调整 AI 行为时改本目录，**不要**顺手改 `index.html` 业务代码（见 `AI_RULES.md` 禁止项）。

## 6. Prompt 统一模板

每个 Prompt 单元按下表填写：

| 字段 | 含义 | 写法要点 |
| --- | --- | --- |
| **Role（角色）** | AI 扮演谁 | 一句话定位，如「你是一位严谨的个人财富教练」 |
| **Goal（目标）** | 这次要达成什么 | 可量化、可验证的结果 |
| **Context（上下文）** | 需要知道的背景 | 用户长期目标、历史数据、当前页面状态（用占位符 `{...}`） |
| **Input（输入）** | 用户/系统提供什么 | 明确字段与格式，如「资产列表 `{assets}`、交易 `{transactions}`」 |
| **Constraints（约束）** | 不能做什么 | 不编造数据、不越权、结合长期目标、给出依据 |
| **Output（输出格式）** | 返回什么结构 | 指定 JSON / 列表 / 固定字段，便于前端解析 |

**最小示例：**

```markdown
### 仓位分析
- 状态: 规划中
- 角色: 你是一位严谨的个人财富教练。
- 目标: 判断当前持仓是否偏离目标配置，并给出再平衡建议。
- 上下文: 用户长期目标={longTermGoals}；当前日期={date}。
- 输入: 资产列表={assets}；目标配置={targetAllocation}。
- 约束: 不编造价格；建议必须说明原因；结合用户风险偏好。
- 输出: JSON：{ deviation:[...], suggestions:[...], rationale:string }
```
