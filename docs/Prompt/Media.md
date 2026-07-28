# Media.md — 自媒体模块 AI Prompt

> 集中维护「自媒体」相关的 AI 能力。当前对应本地规则 `AI.genContentIdeas`。

## 作用

把内容数据转化为选题、创作与复盘建议，帮用户用数据放大个人影响力。

## 适用场景

- 自媒体页的选题、爆文拆解、内容生成、数据复盘。
- 结合账号定位 `{profile.contentPositioning}` 产出贴合人设的内容。

## 输入

- 内容记录：`{contents[]}`（title/topic/type/status/views/likes/saves/comments/shares/followersGained）
- 账号定位：`{profile.contentPositioning}`、`{profile.interests}`
- 长期目标中自媒体相关项：`{longTermGoals}`

## 输出

- 按子能力分别返回（见下），均须贴合用户人设与数据反馈。

## 规划中的 Prompt（待按 PromptGuide 模板补全）

### 小红书选题
- 对应现状：`AI.genContentIdeas`
- 简述：基于人设与历史高互动话题，生成可落地的选题清单。

### 热点分析
- 简述：判断当前热点是否与用户定位相关、值不值得追。

### 发布时间
- 简述：基于历史互动时段，推荐最佳发布时间窗口。

### 爆文拆解
- 简述：对一篇爆款做结构拆解（标题/开头/钩子/结尾），可复用方法论。

### 内容生成
- 简述：按选题与人设生成图文/短文草稿。

### 数据复盘
- 简述：对一段时间内内容做表现归因（什么类型涨粉/收藏高）。

## 后续待完善内容

- [ ] 补全 6 个子 Prompt 的完整模板。
- [ ] 多平台字段扩展（当前以小红书为主）。
- [ ] 选题需避免「标题党」，与 `AI.md` 行为准则一致。
