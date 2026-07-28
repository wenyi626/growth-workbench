# TODO.md — 需求池

> 维护规范：每次完成一个需求，将其从对应优先级移到「已完成」区，并在 CHANGELOG.md 记录。
> 优先级：**P0 必须做 / 近期**，**P1 重要 / 下一迭代**，**P2 可选 / 远期**。

## P0 — 必须做 / 近期

- [ ] **（已合并到 v1.0.0）版本自动检测与「发现新版本」弹窗**
  - 见 CHANGELOG `[v1.0.0]`：已补全 `sw.js` 的 `skipWaiting` 消息处理并随 `feat: version update detection and pwa update flow` 提交。
- [ ] **数据契约冻结确认**：确认 `pgwb_data_v1` 字段结构，作为 v1.0 稳定基线。
- [ ] **首次启动引导**：帮助用户清空示例种子数据或一键导入自己的数据。
- [ ] **文档体系补全**：本项目 PROJECT/VISION/TODO/CHANGELOG/AI_RULES/README 已初始化（本次任务）。
- [ ] **Projects / Planner 重构（IMP-004，下一版本）**：引入 `PlannerEngine`，Projects 进度从手工百分比改为计划 / 排期驱动。

## P1 — 重要 / 下一迭代
- [ ] **RuleEngine 接入 OpenAI（仅解释/细化，不决策）**：用 `docs/Prompt/` 中的 Prompt 让 LLM 对 `RuleEngine.getSuggestions()` 返回的 `Suggestion[]` 做自然语言解释与个性化细化；**决策权仍归 RuleEngine**，LLM 不得自行生成或增删建议（参考 `Home.md`/`Study.md` 等）。
- [ ] **规则增强**：Study/Wealth/Fitness/Media Rule 接入更多真实信号（如目标配置偏离、汇率影响、睡眠趋势），并补充 `FutureRule` 真实投资/职业类高级规则。
- [x] **学习历史升级（IMP-002 / v1.3.1 基础已落地）**：学习历史支持「查看历史笔记 / 继续学习 / 重新学习」，记录可完整恢复（英语/AI 交互式续学，其它类别恢复已存摘要/笔记/产出）。**复习曲线与产出追踪**留作 P2。
- [x] **AI 学习模块重构（IMP-003 / v1.3.1 已落地 AI 工具学习中心）**：建立 `Library` + `LearningSource` 统一学习引擎，英语模块改读 `Library`；AI 模块从抽象主题重构为真实「AI 工具学习中心」——内置 11 个真实工具（Claude Code / Cursor / WorkBuddy / ChatGPT / Gemini CLI / Codex / Windsurf / MCP / A2A / n8n / Dify）完整课程（教程/案例/练习/测验），点击即学→做→测并标记已学；联网 AI 学习留待 V1.3.2。
- [x] **英语课文源扩展（V1.3.1 基础已落地）**：`EN_LIB` 静态 4 篇已迁至 `LearningSource` 内置库（英语 8 篇 / AI 11 篇 / 产品 2 篇，且可继续扩充），「换一篇」在库内确定性/随机切换；**真实联网课文源属 V1.3.2（`RemoteSource` 占位）**，不在此版本实现联网

- [ ] **财富增强**：资产再平衡提示、目标配置偏离告警、分红/汇率影响可视化。
- [ ] **英语词库同步**：`vocabBank` 与 `EnglishMod` 测验打通，支持手动添加/复习曲线。
- [ ] **自媒体多平台**：不止小红书，支持多平台字段与对比。
- [ ] **身体指标趋势**：体重/围度/体脂/睡眠的多指标联合视图与预警。
- [ ] **云端备份后端**：实现 `/__backup` 或替换方案（如 GitHub Gist / 用户自托管），消除当前静默失败。
- [ ] **V1.3.2 联网 AI 学习（顺延）**：原规划的「联网真实课文源」顺延至后续版本；本版本（v1.3.2）目标已重新定义为「AI 工具课程模板标准化」——统一 6 段固定模板、11 个工具行动化重写（去百科化）。`RemoteSource` 仍仅占位，不实现联网、不改动数据契约。
- [ ] **内容/数据导出增强**：可导出 CSV、可生成分享图。

## P2 — 可选 / 远期

- [ ] **真实大模型接入**：在后端代理下接入 LLM（前端禁硬编码 Key），保留本地规则降级。
- [ ] **AI Personal CEO 主动编排**：跨维度每日优先级与行动建议（对应 VISION 阶段三）。
- [ ] **多设备同步**：基于用户自托管后端的跨端数据一致性。
- [ ] **日历/提醒集成**：与系统日历联动，落实 `remindReview`。
- [ ] **可访问性（a11y）优化**：对比度、字体缩放、屏幕阅读器支持。
- [ ] **国际化**：界面支持中英切换（与英语学习场景呼应）。

## 已完成

- [x] 单文件应用骨架 + 6 标签移动端布局（明/暗主题）
- [x] 数据层 `S`：持久化 + 种子 + CRUD + 导入导出 + 重置
- [x] 今日 / 学习 / 财富 / 身体 / 自媒体 / 我的 六大模块
- [x] 手写 SVG 图表（donut / line / bar）
- [x] 本地规则型 AI（8 个能力）
- [x] PWA：manifest + Service Worker 离线 + 图标 + iOS 启动图
- [x] GitHub Pages 部署
- [x] 文档体系初始化（PROJECT / VISION / TODO / CHANGELOG / AI_RULES / README）
- [x] 版本自动检测与 PWA 更新流（v1.0.0）：`version.json` 版本源 + 「发现新版本」弹窗 + `sw.js` skipWaiting 更新流
- [x] Today OS 首页架构（v1.1.0）：`TodayAgent` + 四 Agent 桩，9 段式 AI CEO Dashboard（Mock 数据）
- [x] Decision Engine 决策引擎（v1.2.0）：`RuleEngine` 唯一决策中心 + 5 个 Rule（`StudyRule`/`WealthRule`/`FitnessRule`/`MediaRule`/`FutureRule`）；`TodayAgent` 改为只消费 `RuleEngine.getSuggestions()`，未接入 LLM
- [x] 财富数据单一数据源 SSOT（v1.2.1 / BUG-001）
- [x] 英语「换一篇」真正切换（v1.2.1 / BUG-002）
- [x] 交易记录编辑与删除（v1.2.1 / IMP-001）
- [x] 学习历史点击回看（v1.2.2）：历史记录点击恢复完整内容（英语匹配 EN_LIB 复原文章/单词/语法/测验）
- [x] 学习引擎基础 Learning Foundation（v1.3.1）：LearningLibrary + LearningSource 数据源抽象（英语8/AI11/产品2，不再写死4篇；RemoteSource 为 V1.3.2 联网预留）；英语模块改读 Library；学习历史升级「查看历史笔记 / 继续学习 / 重新学习」
- [x] AI 工具学习中心（v1.3.1）+ 课程模板标准化（v1.3.2）：AI 页从抽象表单重构为 11 个真实 AI 工具的课程中心（由 `AIToolMod` 驱动）；v1.3.2 进一步把所有工具统一为 6 段固定模板（是什么/核心能力/实战案例/实际操作/今日任务/小测验）并行动化重写（去百科化），新增工具只填同一组字段即可复用模板。
