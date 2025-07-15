# AI Debate Crew

This project demonstrates a two-agent debate workflow using the CrewAI framework. Two “debater” agents argue **for** and **against** a given motion, and a “judge” agent decides which side is more convincing. All configurations, tasks, and agent definitions are stored in YAML files. The Python code wires everything together into a runnable CrewAI “crew.”

---

## How It Works

1. **Motion Input**  
   In `main.py`, you supply a motion (e.g. `"There needs to be strict laws to regulate LLMs"`). This value is interpolated into every agent/task description (via `{motion}` placeholders in the YAML).

2. **Crew Setup** (`crew.py`)  
   - The `@CrewBase`-decorated `Debate` class binds two configuration files:  
     - `agents.yaml` (defines agent roles, goals, and models)  
     - `tasks.yaml`  (defines task descriptions and expected outputs)  
   - `@agent` methods return `Agent` objects:  
     - **`debater`** (uses `openai/gpt-4o-mini`)  
     - **`judge`**   (uses `anthropic/claude-3-7-sonnet-latest`)  
   - `@task` methods return `Task` objects for:  
     1. **`propose`**: Generate a concise argument **in favor** of the motion.  
     2. **`oppose`**: Generate a concise argument **against** the motion.  
     3. **`decide`**: Judge which side is more convincing given both arguments.

3. **Sequential Processing**  
   The `Crew` is instantiated with `process=Process.sequential` so tasks run in order:  
   - **`propose`** → calls **debater** to write “for” argument → saves to `output/propose.md`  
   - **`oppose`**  → calls **debater** to write “against” argument → saves to `output/oppose.md`  
   - **`decide`**  → calls **judge** to pick a winner based on both arguments → saves to `output/decide.md`

4. **Outputs**  
   After running, you’ll find:  
   - `output/propose.md` → Persuasive argument in favor of the motion  
   - `output/oppose.md`  → Persuasive argument against the motion  
   - `output/decide.md`  → Judge’s reasoned decision on which side prevailed




