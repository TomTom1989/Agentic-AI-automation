## Deep Research AI Agent

This project performs deep research on a user-provided topic using a multi-agent system powered by OpenAI's Agents SDK, presented via a Gradio interface. It plans web searches, summarizes results, generates a detailed report, and sends it by email using SendGrid.

---

## Project Flow

### 🔹 Entry Point: `deep_research.py`
- Launches a **Gradio UI** with a textbox and "Run" button.
- When triggered, it calls the `run()` async generator.
- This generator instantiates `ResearchManager()` and streams back progress updates and the final report.

### 🔹 Core Orchestrator: `research_manager.py`
- Manages the full research pipeline using async functions:
  1. **`plan_searches()`** → calls `planner_agent` to generate 5 relevant search queries.
  2. **`perform_searches()`** → calls `search_agent` concurrently for each search term.
  3. **`write_report()`** → calls `writer_agent` to create a long Markdown report from the summarized results.
  4. **`send_email()`** → calls `email_agent` to convert the report to HTML and email it via SendGrid.
- Each step is traced using the custom `trace()` context manager and `gen_trace_id()`.

---

## Agent Mechanism: `agents.py`
- Centralized utility module for agent logic and tool registration.
- Provides:
  - `Agent`: core class for managing LLM calls and tool execution.
  - `Runner`: async interface to trigger agents.
  - `trace` / `gen_trace_id`: lightweight tracing utility for step tracking.
  - `function_tool`: decorator to register async function tools.
  - `WebSearchTool` / `ModelSettings`: optional tool configuration and model tuning.
  - `AgentResponse`: wraps and transforms raw or structured output from LLM.
- Supports structured outputs via Pydantic models and mock fallbacks when `OPENAI_API_KEY` is not set.

---

## Agent Modules

### `planner_agent.py`
- Uses an LLM to generate 5 search terms and reasons.
- Output structured using `WebSearchPlan` and `WebSearchItem` models.

### `search_agent.py`
- Summarizes search results using `WebSearchTool`.
- Returns 2–3 paragraph summaries per query.

### `writer_agent.py`
- Generates a cohesive Markdown research report (1000+ words) and a short summary.
- Output typed using `ReportData`.

### `email_agent.py`
- Registers `send_email()` as a callable function tool.
- Sends the final report via SendGrid using HTML formatting.

---

## Technologies Used

- [OpenAI Agents SDK](https://openai.github.io/openai-agents-python/)
- OpenAI GPT-4 / GPT-4o
- Gradio (interactive UI)
- Python asyncio
- SendGrid API (email delivery)
- dotenv for config
- Pydantic for data models

---

## How to Run

1. **Install dependencies**:
   ```bash
   pip install openai-agents openai gradio python-dotenv sendgrid pydantic



PS: IMPORTANT==> > **Note:** I initially created a custom `agents` module to define core components like `Agent`, `Runner`, and `WebSearchTool`. However, this can be simplified by using the official OpenAI Agents SDK instead. (Dont need any additional agents module, just import the right package for each agent)
You can install it with:

```bash
pip install openai-agents
