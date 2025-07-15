# 🧠 Sidekick AI – LangGraph Agentic Assistant

This project is an **agentic AI assistant** built using **LangGraph**, **LangChain**, and **Gradio**.  
It supports tool usage, dynamic decision-making, and iterative refinement based on feedback and success criteria.

---

## 🚀 Overview

**Sidekick** is an intelligent AI assistant that:

- Takes a user request and success criteria.
- Uses tools (search, Python REPL, file management, Playwright browser, etc.).
- Evaluates its own output against the success criteria.
- Asks the user for clarification if it gets stuck.
- Sends push notifications when needed.
- Continues working until either:
  - ✅ The task is successfully completed, or
  - ❓ User clarification is required.

---

## ⚙️ Core Components

- **`app.py`** – The Gradio UI interface.
- **`sidekick.py`** – Core agent logic, memory, and LangGraph state machine.
- **`sidekick_tools.py`** – Defines external tools like:
  - 🌐 Web browser (Playwright)
  - 🔍 Google search (Serper)
  - 📚 Wikipedia queries
  - 🧮 Python REPL
  - 📁 File writing
  - 🔔 Push notification (Pushover)

---

## 🧭 Flow of Interactions

### 1. User Input via Gradio
- User enters:
  - A message (task or request)
  - Optional success criteria

### 2. Agent Setup
- Sidekick initializes tools (`playwright_tools`, `other_tools`)
- Two LLMs are prepared:
  - **Worker LLM**: Handles task execution and tool usage
  - **Evaluator LLM**: Judges task completion

### 3. Graph Execution with LangGraph
- The LangGraph state machine is built with nodes:
  - `worker`: Uses LLM with tools
  - `tools`: Executes tool calls
  - `evaluator`: Validates progress
- Conditional edges decide next steps

### 4. Task Loop
- The worker processes the task
- If tools are needed → `tools` node runs
- Otherwise, result is evaluated:
  - ✅ If criteria met → success
  - 🔁 If not met → loop continues or asks user for input

### 5. Gradio UI Updates
- Response, feedback, and state updates are shown in the chatbot
- Buttons: **Go** to run the task, **Reset** to start fresh

### 6. Resource Cleanup
- Browser and Playwright processes are gracefully closed after session ends

---

## 🛠️ Example Use Case

- **Input**: "Summarize the latest research about quantum computing"  
- **Success Criteria**: "Include at least 3 sources, be under 300 words"

### 🧩 Flow:
- Assistant searches the web using Serper
- Uses Python REPL to clean or process text
- Generates a summary
- Evaluator checks if success criteria are met
- If not, feedback is looped into the worker

---

## 📦 Tools Available

- ✅ Playwright (web browsing)
- ✅ Serper (Google Search API)
- ✅ Wikipedia queries
- ✅ Python REPL
- ✅ File writing to `sandbox/`
- ✅ Push notifications (Pushover)

---

## 🧠 Memory

- Uses `MemorySaver` from LangGraph to checkpoint each step
- `thread_id` is session-specific for isolating task memory
