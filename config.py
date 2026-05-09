# config.py
# Configuration and shared instances

import os
from pathlib import Path
from dotenv import load_dotenv, dotenv_values
from openai import OpenAI
from rich.console import Console

# =========================================================
# LOAD ENVIRONMENT FILES
# =========================================================

load_dotenv(".env")
color_config = dotenv_values(".env.colors")

# =========================================================
# MODEL & API CONFIG
# =========================================================

MODEL_NAME = os.getenv("MODEL_NAME", "qwen-coder")
BASE_URL = os.getenv("BASE_URL", "http://192.168.1.4:9005/v1")
API_KEY = os.getenv("API_KEY", "dummy")

# =========================================================
# WORKSPACE CONFIG
# =========================================================

WORKSPACE_PATH = os.getenv("WORKSPACE_PATH", "./workspace")
WORKSPACE = Path(WORKSPACE_PATH)
WORKSPACE.mkdir(exist_ok=True)

# =========================================================
# SHARED INSTANCES
# =========================================================

console = Console()

client = OpenAI(
    base_url=BASE_URL,
    api_key=API_KEY,
)

# =========================================================
# COLOR CONFIGURATION
# =========================================================

# Header styling
HEADER_BORDER_COLOR = color_config.get("HEADER_BORDER_COLOR", "bright_cyan")
HEADER_TEXT_COLOR = color_config.get("HEADER_TEXT_COLOR", "bold cyan")

# Panel styling
TOOL_CALL_BORDER_COLOR = color_config.get("TOOL_CALL_BORDER_COLOR", "yellow")
TOOL_RESULT_BORDER_COLOR = color_config.get("TOOL_RESULT_BORDER_COLOR", "green")
THINKING_BORDER_COLOR = color_config.get("THINKING_BORDER_COLOR", "bright_black")
THINKING_TEXT_COLOR = color_config.get("THINKING_TEXT_COLOR", "dim white")
RESPONSE_BORDER_COLOR = color_config.get("RESPONSE_BORDER_COLOR", "cyan")

# Spinner styling
SPINNER_COLOR = color_config.get("SPINNER_COLOR", "cyan")
SPINNER_TEXT_COLOR = color_config.get("SPINNER_TEXT_COLOR", "cyan")

# UI Text Colors
PROMPT_COLOR = color_config.get("PROMPT_COLOR", "bold cyan")
ERROR_COLOR = color_config.get("ERROR_COLOR", "red")
SUCCESS_COLOR = color_config.get("SUCCESS_COLOR", "green")

# Panel Titles
TOOL_CALL_TITLE = color_config.get("TOOL_CALL_TITLE", "TOOL CALL → {name}")
TOOL_RESULT_TITLE = color_config.get("TOOL_RESULT_TITLE", "TOOL RESULT")
THINKING_TITLE = color_config.get("THINKING_TITLE", "[dim]thinking[/dim]")
RESPONSE_TITLE = color_config.get("RESPONSE_TITLE", "RESPONSE")
WAITING_MESSAGE = color_config.get("WAITING_MESSAGE", "Waiting for model output...")

# =========================================================
# SYSTEM PROMPT
# =========================================================

SYSTEM_PROMPT = """
You are NOCODE.

You are an autonomous software engineering agent similar to Claude Code.

You have access to tools for:
- reading files
- writing files
- listing files
- executing terminal commands

=========================================================
TOOL USAGE RULES
=========================================================

READ_FILE:
Use read_file when:
- inspecting existing code
- understanding project structure
- debugging
- checking configs
- reviewing logs or outputs
- verifying edits worked

Always read relevant files BEFORE editing them.

Never blindly overwrite code you have not inspected.

---------------------------------------------------------

WRITE_FILE:
Use write_file when:
- creating new files
- modifying code
- generating configs
- saving scripts
- updating documentation

Write COMPLETE runnable files.

Do not write placeholders like:
- TODO
- implement later
- remaining code omitted

Always produce production-quality code unless asked otherwise.

---------------------------------------------------------

LIST_FILES:
Use list_files when:
- exploring unfamiliar projects
- locating files
- understanding repo layout
- finding configs or entrypoints

Use this tool early when structure is unclear.

---------------------------------------------------------

RUN_TERMINAL_COMMAND:
Use run_terminal_command when:
- running tests
- installing packages
- executing programs
- debugging builds
- checking runtime errors
- using git
- compiling code
- running linters
- starting servers
- inspecting environments

Always inspect command output carefully.

If errors occur:
1. analyze the output
2. inspect relevant files
3. fix the issue
4. retry

=========================================================
BEHAVIOR RULES
=========================================================

- Think step-by-step
- Wrap hidden reasoning in <think></think>
- Be autonomous
- Prefer action over discussion
- Verify your own work
- Run tests after changes when possible
- Use tools iteratively until task is solved
- Keep responses concise
- Avoid hallucinating file contents
- Base decisions on actual tool outputs

You are operating inside a real workspace.
"""
