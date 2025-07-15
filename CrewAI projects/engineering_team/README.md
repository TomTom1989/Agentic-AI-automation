# 🧠 CrewAI Automation Flow: From Design to Demo

This project uses CrewAI to generate a backend module, unit tests, and a Gradio UI from high-level requirements using a multi-agent workflow. Each agent plays a specific role in a full development cycle from idea to working prototype.

---

## 🔄 Workflow Overview

1. **👨‍💼 `engineering_lead`**  
   - **Input**: High-level requirements (`{requirements}`)  
   - **Task**: Produces a detailed design document in Markdown format, describing the Python module’s classes and methods.  
   - **Output**: `output/{module_name}_design.md`

2. **👨‍💻 `backend_engineer`**  
   - **Input**: The design from `engineering_lead`  
   - **Task**: Implements a complete Python module based on the design.  
   - **Output**: `output/{module_name}` (e.g., `accounts.py`)

3. **🧪 `test_engineer`**  
   - **Input**: The backend module  
   - **Task**: Writes unit tests to validate the module's functionality.  
   - **Output**: `output/test_{module_name}` (e.g., `test_accounts.py`)

4. **🎨 `frontend_engineer`**  
   - **Input**: The backend module  
   - **Task**: Creates a Gradio UI to demonstrate the backend's capabilities.  
   - **Output**: `output/app.py`

---

## 📁 Output Folder Structure

After running the crew, the following files are generated in the `output/` directory:

output/
├── accounts.py # Backend logic
├── app.py # Gradio UI
├── test_accounts.py # Unit tests
├── accounts_design.md # Design document

yaml
Copy
Edit

> The name `accounts` is based on the `{module_name}` used during generation.

---

## ▶️ How to Run the Gradio UI

Once all modules are created, you can launch the app with:

```bash
python output/app.py


PS: We could improve this system by adding vector storage and SQL-based memory implementation for the AI agents.
