# Study.md — 学习模块 AI Prompt

> 集中维护「学习」相关的 AI 能力。当前对应本地规则 `AI.checkSentence` / `AI.generateEnglish`（英语）与 `AI.selfAnalysis`（部分）。

## 作用

把「信息」转化为「能力」：辅助英语学习、理解 AI/阅读内容、规划学习路径、做每日推荐。

## 适用场景

- 学习页的英语练习、阅读理解、学习规划。
- 英语模块（`EnglishMod`）的测验与词库。

## 输入

- 学习记录：`{learning[]}`（topic/category/source/understanding/output）
- 长期目标中与学习相关的项：`{longTermGoals}`
- 英语词库：`{vocabBank[]}`

## 输出

- 按子能力分别返回（见下）。

## 规划中的 Prompt（待按 PromptGuide 模板补全）

### 英语
- 对应现状：`AI.generateEnglish` / `AI.checkSentence`
- 简述：生成可理解的可控难度英文材料；检查用户英文句子的语法/表达并给出改进。

### AI
- 简述：用通俗语言解释 AI 概念，并结合用户电商运营背景给落地场景。

### 阅读
- 简述：对一篇材料做摘要、提炼要点、生成追问，帮助深度理解。

### 学习规划
- 简述：基于已有学习记录与目标，排出周/月学习路径与里程碑。

### 每日推荐
- 简述：每天推荐 1 个值得投入的学习主题或练习。

## 后续待完善内容

- [ ] 补全上述 5 个子 Prompt 的完整模板。
- [ ] 英语模块与 `vocabBank` 打通，按记忆曲线出题。
- [ ] 明确「AI 概念解释」的领域边界（电商运营视角）。
