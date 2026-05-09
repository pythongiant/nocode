# tools.py
# Tool implementations and schemas

import subprocess

from .config import PROJECT_ROOT
from .diff import compute_changes, format_changes_text, snapshot
from .permissions import confirm_command

# =========================================================
# SIDE CHANNEL
# =========================================================
# After each tool invocation the UI peeks at this list to render
# a colored "files changed" panel. Cleared at the start of every call.

last_changes: list[dict] = []


def _consume_changes() -> list[dict]:
    out = list(last_changes)
    last_changes.clear()
    return out


# =========================================================
# TOOL IMPLEMENTATIONS
# =========================================================

def run_terminal_command(command: str):
    """Execute a shell command from the project root, with user confirmation
    and a per-file diff summary attached to the result."""
    last_changes.clear()

    if not confirm_command(command):
        return (
            "USER DENIED COMMAND. The command was not executed.\n"
            "Do not retry the same command. Ask the user how to proceed "
            "or try a different approach."
        )

    before = snapshot(PROJECT_ROOT)

    try:
        result = subprocess.run(
            command,
            shell=True,
            cwd=PROJECT_ROOT,
            capture_output=True,
            text=True,
            timeout=120,
        )
    except subprocess.TimeoutExpired:
        return "ERROR: command timed out"
    except Exception as e:
        return f"ERROR: {str(e)}"

    after = snapshot(PROJECT_ROOT)
    changes = compute_changes(before, after)
    last_changes.extend(changes)

    output = ""
    if result.stdout:
        output += f"STDOUT:\n{result.stdout}\n"
    if result.stderr:
        output += f"STDERR:\n{result.stderr}\n"
    output += f"\nEXIT CODE: {result.returncode}"
    if changes:
        output += "\n\n" + format_changes_text(changes)
    return output


# =========================================================
# TOOLS REGISTRY
# =========================================================

TOOLS = {
    "run_terminal_command": run_terminal_command,
}

# =========================================================
# TOOL SCHEMAS
# =========================================================

TOOL_SCHEMAS = [
    {
        "type": "function",
        "function": {
            "name": "run_terminal_command",
            "description": "Execute terminal commands from the project root directory. Use this for running, reading, writing, and verifying anything.",
            "parameters": {
                "type": "object",
                "properties": {
                    "command": {
                        "type": "string",
                        "description": "The shell command to execute (bash/sh syntax)"
                    }
                },
                "required": ["command"]
            }
        }
    }
]
