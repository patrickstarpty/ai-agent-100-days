# Writing brief for lessons in `ai-agent-100-days`

You are writing lesson files (Simplified Chinese) for this public GitHub course repo (paths below are relative to the repo root), modelled on Python-100-Days: one Markdown lesson per day, grouped in stage folders. 42 of 100 lessons already exist. You write ONLY the days assigned to you, into the folder named in your assignment. Do not edit any existing file, do not create a README, do not run git commands.

## Read these first (match their style, density and structure exactly)
- `Day35-46/39.反思模式.md` (the canonical example of a normal lesson, including the final 参考说明)
- `Day57-66/57.Agent的威胁模型.md`
- `Day23-34/23.评估全景.md`
- For 阶段实战 lessons: `Day01-10/10.阶段实战-命令行问答助手.md`
- For 复盘 lessons: `Day35-46/46.阶段复盘-编排规格.md`
- The full syllabus: the 100-day outline in `README.md` (entries marked “待更新” are not written yet). The same data lives in `scripts/gen_readme.py`.
Also skim any already-written lesson in your own stage so your lessons connect to it and do not repeat it.

## The owner's style requirement
简单易懂、提纲挈领、高屋建瓴. Every lesson states its essence in one plain sentence first, then says where it sits in the whole system, then explains the idea with one everyday analogy, and only then goes into detail. A reader who reads only the two blockquote lines and the analogy should already understand what the lesson is about and why it matters.

## Required structure of every lesson (exact headings)
```
## DayNN - 标题

> <阶段名> ｜ 建议用时 1 小时

> **一句话**：(one plain sentence: the essence of this lesson)
>
> **放在全局看**：(one or two sentences: where this sits in the whole system, which other days it connects to)

### 学习目标
(2–3 bullets)

### 核心概念

**打个比方**：(one everyday analogy, 1–3 sentences. Omit only for 阶段实战 and 复盘 lessons.)

(the teaching content: short sub-sections with **bold lead-ins**; tables where content is tabular; short code only where code teaches something)

### 阅读材料
(optional — see link rules; omit the section entirely if you have no verified link)

### 动手练习
(concrete tasks for ~20 minutes, tied to 主线项目 / 案例 A / 案例 B where natural)

### 自检
(exactly 2 numbered questions, no answers)

### 参考说明
(what this lesson drew on: one bullet per source: `- [title](url)：<which idea/fact was taken from it>`, then a last bullet `- 其余的讲解、比方、示例和练习为本课程自己编写。` If the lesson used no external source, write the single line: `本课没有新增的外部参考，内容为本课程自己整理，用到的方法来自前面各课。`)
```
- The H2 is exactly `## DayNN - 标题` with a two-digit day number and the title given in your assignment.
- The stage name in the first blockquote line is given in your assignment.
- Length: about 700–1300 Chinese characters of prose per lesson (tables and exercises included), plus code. 实战 lessons may be longer.
- 复盘 lessons (stage wrap-ups) replace 动手练习/自检 with 产出 sections and a final `### 阶段验收` checklist of `- [ ]` items, as in `Day35-46/46.阶段复盘-编排规格.md`. They still end with 参考说明.

## Recurring objects (use these names)
- **主线项目**: the learner's own agent application. The course's running example is “一个基于企业知识做问答和测试设计的平台”.
- **案例 A：企业知识库** — system docs, business docs and code organised as knowledge for people and agents to retrieve; access follows each user's permissions in the source systems.
- **案例 B：AI 原生研发流程** — a requirement is described in a ticket system (e.g. Jira); an agent refines it; after approval an agent codes, commits, builds and releases.
- Example technology stack when a concrete product is needed: LangGraph (orchestration), Langfuse (tracing/evaluation), Azure Foundry (model platform). Concepts must not depend on these products.
- Day01–10 built a thin wrapper `from llm import chat` (litellm, OpenAI chat-completions format; `chat(messages, **kwargs)` returns the response; text at `resp.choices[0].message.content`). You may use it in plain-Python sketches.

## Content rules
- Simplified Chinese; code, identifiers and established English terms (agent, token, prompt, trace, span, tool call) stay in English.
- No company, employer, internal project or person from the owner's workplace. Generic examples only (套餐、订单、退订、工单、课程、图书馆). Do NOT use insurance or banking examples.
- Do not use “不是……而是……” as a rhetorical device. No rhetorical questions, no slogans, no emoji, no closing paragraph that repeats the lesson.
- Do not invent statistics, benchmarks, prices, version numbers or product limits. If you did not verify a number in this session, describe the relationship qualitatively.
- Refer to other lessons as `DayNN` using the syllabus. You may reference days that are not written yet.
- Prefer designs where: the model proposes and deterministic code or a human decides; every loop has limits; write actions run under a user's identity; retrieval filters by permission at query time. These are the course's standing positions.

## Code rules
- Python 3.11+. Short, correct, and only where it teaches.
- Any framework or SDK API (LangGraph, Langfuse, MCP SDK, OpenTelemetry, Azure SDKs, etc.) may appear in code ONLY if you opened the official documentation with WebFetch in this session and the code follows what you read. If you cannot verify it, explain the mechanism in prose or plain-Python pseudo-code instead and say nothing about exact API names.
- Never hardcode a vendor model name or a key.

## Link rules
- Under 阅读材料 and 参考说明, include a link only if (a) you fetched it with WebFetch in this session and it says what you claim, or (b) it is in the pre-verified list below and you use it only for the claims listed there.
- Do not copy or closely paraphrase passages. Write explanations yourself; quote at most a short phrase.
- It is fine for a lesson to have no external link.

## Pre-verified sources (opened and checked on 2026-10-10)
- https://www.anthropic.com/engineering/building-effective-agents — workflows vs agents; five workflow patterns (prompt chaining, routing, parallelization, orchestrator-workers, evaluator-optimizer).
- https://anthropic.com/engineering/demystifying-evals-for-ai-agents — code/model/human graders; capability vs regression evals; start with 20–50 tasks from real failures; grade outcomes not paths; read transcripts.
- https://hamel.dev/blog/posts/evals-faq/ — error analysis first; binary pass/fail; one domain expert decides; validate LLM judges against human labels; prefer code checks.
- https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents — compaction, structured note-taking, sub-agents with clean context returning summaries, just-in-time retrieval.
- https://www.anthropic.com/engineering/writing-tools-for-agents — few well-targeted tools, namespacing, meaningful returns, token-efficient responses with actionable errors, careful tool descriptions.
- https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents — initializer session, feature list file with status, one feature per session leaving clean state, end-to-end testing as a user.
- https://www.anthropic.com/engineering/contextual-retrieval — contextual embeddings + contextual BM25 + reranking.
- https://simonwillison.net/2025/Jun/16/the-lethal-trifecta/ — private data + untrusted content + external communication.
- https://genai.owasp.org/resource/owasp-top-10-for-agentic-applications-for-2026 — the OWASP page (published Dec 2025). The page itself does NOT list the ten items; do not list them unless you verify them from OWASP's own document.
- https://github.com/humanlayer/12-factor-agents — the twelve factors (own your prompts, own your context window, own your control flow, small focused agents, stateless reducer, launch/pause/resume, contact humans with tool calls, compact errors into context, etc.).
- https://modelcontextprotocol.io/docs/learn/architecture — host/client/server; tools/resources/prompts; stdio and Streamable HTTP; protocol version 2026-07-28 is stateless; OAuth recommended for HTTP.
- https://docs.langchain.com/oss/python/langgraph/persistence — checkpointers (thread-scoped) vs stores (cross-thread).
- https://docs.langchain.com/oss/python/langgraph/interrupts — `interrupt()` pauses, `Command(resume=...)` resumes, node restarts from its beginning.
- https://langfuse.com/docs/evaluation/overview , https://langfuse.com/docs/evaluation/experiments/datasets , https://langfuse.com/docs/evaluation/evaluation-methods/llm-as-a-judge , https://langfuse.com/docs/evaluation/experiments/experiments-ci-cd , https://langfuse.com/integrations/frameworks/langgraph — Langfuse evaluation concepts (datasets, experiments, scores, LLM-as-a-judge, annotation queues, online vs offline), CI experiments, LangGraph tracing via `CallbackHandler` from `langfuse.langchain`.
- https://learn.microsoft.com/en-us/azure/search/search-document-level-access-overview — security filters (GA) vs preserving source ACLs (preview; ADLS Gen2, Blob, SharePoint); user token in `x-ms-query-source-authorization`; permission changes apply after sync.
- https://learn.microsoft.com/azure/ai-foundry/agents/how-to/tools/knowledge-retrieval — agents connect to a knowledge base over MCP; without the user token permission-enabled sources return unfiltered results.
- https://learn.microsoft.com/en-us/azure/architecture/ai-ml/guide/ai-agent-design-patterns — sequential, concurrent, group chat, handoff, magentic patterns; use the lowest level of complexity that works.
- https://learn.microsoft.com/en-us/azure/foundry/how-to/develop/langchain-traces — tracing LangChain/LangGraph with OpenTelemetry GenAI semantic conventions (`gen_ai.operation.name` values such as `invoke_agent`, `chat`, `execute_tool`).
- https://www.deeplearning.ai/courses/agentic-ai/ — Andrew Ng's Agentic AI course: modules on reflection, tool use (incl. code execution, MCP), practical tips (evals, error analysis, component-level evaluation, latency and cost), planning and multi-agent workflows. Only its public outline was consulted; cite it only for topic framing or as a video supplement.
- https://github.blog/changelog/2026-03-05-github-copilot-coding-agent-for-jira-is-now-in-public-preview/ and https://docs.github.com/en/copilot/concepts/agents/coding-agent/about-coding-agent — an off-the-shelf coding agent: assign a ticket, it opens a draft PR, follows existing review rules; one repo and one PR per task; fixed session time limit.
- https://aider.chat/docs/repomap.html — repository map of symbols ranked by a dependency graph within a token budget.

## When done
Re-read each file once. Check: headings exact, two 自检 questions, 参考说明 present, every `DayNN` you mention matches the syllabus, no forbidden content. Then reply with: files written; every external URL you included and whether it was fetched this session or taken from the pre-verified list; anything you were unsure about.
