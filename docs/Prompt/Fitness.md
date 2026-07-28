# Fitness.md — 身体模块 AI Prompt

> 集中维护「身体」相关的 AI 能力。当前对应本地规则 `AI.bodyReport` / `AI.parseExercise`。

## 作用

把运动与身体指标数据转化为可执行的健康建议，帮用户用数据管理身体。

## 适用场景

- 身体页的报告、运动/恢复建议、指标分析。
- 用自然语言记录运动后自动解析（当前 `AI.parseExercise`）。

## 输入

- 运动：`{exercises[]}`（type/duration/intensity/bodyParts/feeling）
- 身体指标：`{weights[]}`（weight/waist/hip/thigh/bodyFat/sleep/bodyState）
- 长期目标中身体相关项：`{longTermGoals}`

## 输出

- 按子能力分别返回建议（见下），均须结合趋势而非单次数据。

## 规划中的 Prompt（待按 PromptGuide 模板补全）

### 运动建议
- 对应现状：`AI.bodyReport`
- 简述：基于近期运动频率与强度，给出下一阶段训练重点。

### 恢复建议
- 简述：根据强度/睡眠/疲劳状态，提示是否需要休息或低强度活动。

### 体重分析
- 简述：分析体重/围度/体脂趋势，区分水分/脂肪波动，避免误读。

### 身体数据分析
- 简述：综合睡眠、体脂、围度给出整体身体状态评分与预警。

## 后续待完善内容

- [ ] 补全 4 个子 Prompt 的完整模板。
- [ ] 明确「疲劳/正常」判定的输入依据（当前 `bodyState` 为人工标记）。
- [ ] 健康建议需标注「非医疗建议」免责声明（见 `AI.md`）。
