"""
mcp_params.py  – “ultra-minimal” edition
Launches *just one* helper: accounts_server.py
"""

from __future__ import annotations
import sys
from pathlib import Path

BASE_DIR = Path(
    "/mnt/c/Users/twalciszewski/Agentic AI projects/MCP servers + openai sdk/Equity traders"
)

PY = sys.executable                     # the venv’s python
COMMON = {"startup_timeout": 20, "env": {"PYTHONUNBUFFERED": "1"}}

# Trader-side servers (only accounts)
trader_mcp_server_params: list[dict] = [
    {
        "command": PY,
        "args": ["-u", str(BASE_DIR / "accounts_server.py")],
        "cwd":  str(BASE_DIR),
        **COMMON,
    }
]

# Researcher-side servers — empty for now
researcher_mcp_server_params: list[dict] = []
