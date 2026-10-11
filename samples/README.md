# samples

本目录是虚构的样例数据，供课程练习使用，没有做完对应主线项目时可以先用这里的数据接着学。全部内容是编造的在线编程学习平台资料，不对应任何真实公司或产品。

## corpus/

约十份虚构语料和 `manifest.json`（记录每份文档的 `id`、`path`、`format`、`groups`、`version`、`status`、`needs_ocr`、`title`）。用于 Day12（文档解析与切片）、Day13～Day21（检索、权限、图谱）、Day22（阶段实战：带引用的知识问答）。

- `doc-plan-guide` 有新旧两版（`plan-guide-v1.md` 已被取代、`plan-guide-v2.md` 现行），练习版本过滤用这一组。
- `doc-course-handbook` 的 `groups` 只有 `staff`，练习权限过滤用这份文档。
- `doc-team-invoice-notice` 是一份 PDF 扫描件，`needs_ocr` 为 `true`；它的 OCR 结果见 `ocr-reference/`。

## ocr-reference/

扫描件人工核对过的 OCR 文本，文件名与 `corpus/` 里对应的扫描件同名（不同后缀）。入库时可以直接当作 OCR 步骤的参考答案，核对自己的解析结果，不代表某一种 OCR 工具的输出格式。

## golden-set.json

至少 20 条评估用例，字段按 [评估集格式示例](../模板/评估集格式示例.md)，覆盖 `answerable`、`should-abstain`、`relation`、`must-not-appear` 四类。用于 Day22、Day25 起步，以及 Day26、Day33 调用 `answer()` 验证评分器和评估平台的接入。每条用例的期望都能在 `corpus/` 里找到依据，`mustCiteSources` 引用的文档 ID 都在 `manifest.json` 里能找到。

## traces/runs.jsonl

30 条样例运行记录，一行一条 JSON，字段参考 Day09 的调用日志（`model`、`promptTokens`、`completionTokens`、`finishReason`、`latencySeconds`）并加上问答层面的字段（`question`、`user`、`topic`、`retrieved`、`citations`、`status`、`reason`、`answerExcerpt`、`steps`）。

- 用于 Day24（错误分析）：直接取这 30 条逐条标注通过/不通过，归类失败模式。其中 10 条是已知失败（`knownFailure: true`），`failureType` 标了具体原因：`retrieval_empty`（检索为空却仍作答）、`invalid_citation`（结论对但引用指向了错误文档）、`timeout`（模型调用超时）、`max_steps`（达到步数上限未完成）、`should_abstain_but_answered`（该弃答却给出了编造答案），各两条。
- 用于 Day86（阶段实战：主动提醒剧本）：`topic` 为 `team-invoice-overseas` 的三条记录（`run-0028`～`run-0030`）是同一主题下、不同提问人在几天内反复得到“资料不足”回答的样例，用来模拟触发知识缺口提议的事件，不用等真实流量。

## tickets/

4 张样例工单（Markdown），供 Day89（需求澄清 Agent）练习把模糊需求改写成带正例、反例、边界的验收标准。

| 文件 | 场景 | 模糊程度 |
| --- | --- | --- |
| `tk-01-order-export.md` | 订单导出按日期筛选 | 写得清楚，验收标准完整 |
| `tk-02-unsubscribe-flow.md` | 退订流程优化 | 缺验收标准，只有方向性的诉求 |
| `tk-03-enrollment-hold-seat.md` | 课程报名先占座后付款 | 缺验收标准，关键参数（占座时长）没定 |
| `tk-04-course-catalog-visibility.md` | 课程目录页展示逻辑 | 自相矛盾：要求同时默认展示全部课程和默认只展示已报名课程 |

## trajectories/

5 条样例 agent 轨迹（JSON），字段参考 Day29：`task`、`spec`（`mustCallTools`、`mustNotCallTools`、`maxToolCalls`、`milestones`）、`toolCalls`（每步的工具名、参数、结果）、`finalState`、`stopReason`（Day45 的停止原因枚举）。供 Day29（Agent 轨迹与工具调用评估）练习按最终状态和硬约束打分。

| 文件 | 问题 |
| --- | --- |
| `traj-01-clean-pass.json` | 无，全部里程碑完成，可作对照组 |
| `traj-02-forbidden-tool-call.json` | 调用了不得调用的工具 `merge_pr` |
| `traj-03-step-budget-exceeded.json` | 工具调用次数超过步数预算 |
| `traj-04-parameter-out-of-range.json` | `git_push` 的 `branch` 参数越界（推到了 `main` 而不是 `agent/` 分支） |
| `traj-05-partial-handoff.json` | 没有违反约束，但遇到工具失败后转人工，里程碑只完成了一部分，用于练习部分得分 |
