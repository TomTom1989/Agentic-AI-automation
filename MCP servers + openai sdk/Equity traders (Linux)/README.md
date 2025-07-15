PROJECT SPECIFICATION IMPORTANT REMARKS:  (Still some bugs to be fixed)
🛠 Setup Summary
To run this agentic AI project with tools like Playwright (via MCP), I had to use Linux (WSL with Ubuntu) for compatibility and security reasons — mainly due to how the Linux kernel handles sockets, subprocesses, and execution environments.

✅ What was done:
Installed the project in Ubuntu (via WSL)
Linux is required for running agent tools safely, especially when agents execute Python or browser code.

Opened Cursor IDE in Linux mode
Used Cursor's Remote-WSL mode to work directly inside the Ubuntu environment.

Installed Node.js inside the Ubuntu environment
This is needed for the @playwright/mcp tool to run via npx.

Installed and synced Python dependencies with uv

Configured the Python environment kernel
The .venv kernel was registered and selected inside Cursor (for Jupyter/Notebook compatibility).

Launched MCP tools inside the Linux project folder
Now tools like Playwright can run securely in subprocesses (via Docker, MCP, etc.)

🤔 Why Linux / WSL was needed
Although most of the code works on any OS, tools like MCP (used by CrewAI or OpenAI SDK) require features tied to the Linux kernel, such as:

✅ Unix-based sockets
Required for internal communication with MCP servers — not supported natively on Windows

✅ Safe subprocess handling and sandboxing
Linux supports tighter security controls, including Docker-based isolation for executing code safely

✅ Playwright tool compatibility
Playwright and other browser automation tools require a Linux-compatible runtime and system libraries

That’s why WSL + Ubuntu with a Linux kernel was used just for this project.

In production, this project should run on a Linux VM or in a Docker container with a Linux base image to support MCP tools, Unix sockets, and secure subprocess execution.

===================================================================================================

PROJECT DESCRIPTION:

This project is a simulated equity trading platform that leverages AI agents to manage, research, and trade stock portfolios. It combines automated trading logic, research tools, and a web-based dashboard to visualize and interact with multiple trader agents. The system is modular, using the Model Context Protocol (MCP) for agent communication and tool orchestration.


1. AI Agents
Trader Agent: Manages a portfolio, executes trades, and follows a strategy.
Researcher Agent: Gathers financial news and research to inform trading decisions.
Tools: Agents use tools (functions or remote services) for research, trading, and data retrieval.

2. MCP Servers
MCP servers (e.g., accounts_server.py, market_server.py) provide services like account management and market data. Agents communicate with these servers using the MCP protocol.

3. Account and Market Management
Account: Each trader has an account with balance, holdings, transaction history, and strategy.
Market: Market data (e.g., share prices) is fetched from external APIs (like Polygon.io) or simulated.

4. Web Dashboard (Gradio UI)
The main.py file builds a Gradio-based dashboard to visualize each trader’s portfolio, holdings, transactions, and logs in real time.


