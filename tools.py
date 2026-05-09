# tools.py
# Tool implementations and schemas

import json
import os
import subprocess
from config import WORKSPACE

# =========================================================
# TOOL IMPLEMENTATIONS
# =========================================================

def read_file(path: str):
    """Read a file from workspace"""
    full_path = WORKSPACE / path

    if not full_path.exists():
        return f"ERROR: file does not exist: {path}"

    try:
        with open(full_path, "r", encoding="utf-8") as f:
            return f.read()

    except Exception as e:
        return f"ERROR: {str(e)}"


def write_file(path: str, content: str):
    """Write content to a file"""
    full_path = WORKSPACE / path

    try:
        full_path.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        with open(full_path, "w", encoding="utf-8") as f:
            f.write(content)

        return f"SUCCESS: wrote file -> {path}"

    except Exception as e:
        return f"ERROR: {str(e)}"


def list_files(path: str = "."):
    """List files in workspace"""
    full_path = WORKSPACE / path

    if not full_path.exists():
        return f"ERROR: path does not exist: {path}"

    results = []

    for root, dirs, files in os.walk(full_path):
        for file in files:
            rel = os.path.relpath(
                os.path.join(root, file),
                WORKSPACE
            )
            results.append(rel)

    if not results:
        return "No files found."

    return "\n".join(results)


def run_terminal_command(command: str):
    """Execute terminal commands inside workspace"""
    try:
        result = subprocess.run(
            command,
            shell=True,
            cwd=WORKSPACE,
            capture_output=True,
            text=True,
            timeout=120
        )

        output = ""

        if result.stdout:
            output += f"STDOUT:\n{result.stdout}\n"

        if result.stderr:
            output += f"STDERR:\n{result.stderr}\n"

        output += f"\nEXIT CODE: {result.returncode}"

        return output

    except subprocess.TimeoutExpired:
        return "ERROR: command timed out"

    except Exception as e:
        return f"ERROR: {str(e)}"


# =========================================================
# TOOLS REGISTRY
# =========================================================

TOOLS = {
    "read_file": read_file,
    "write_file": write_file,
    "list_files": list_files,
    "run_terminal_command": run_terminal_command,
}

# =========================================================
# TOOL SCHEMAS
# =========================================================

TOOL_SCHEMAS = [
    {
        "type": "function",
        "function": {
            "name": "read_file",
            "description": "Read a file from workspace",
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {
                        "type": "string"
                    }
                },
                "required": ["path"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "write_file",
            "description": "Write content to a file",
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {
                        "type": "string"
                    },
                    "content": {
                        "type": "string"
                    }
                },
                "required": [
                    "path",
                    "content"
                ]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "list_files",
            "description": "List files in workspace",
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {
                        "type": "string"
                    }
                }
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "run_terminal_command",
            "description": "Execute terminal commands inside workspace",
            "parameters": {
                "type": "object",
                "properties": {
                    "command": {
                        "type": "string"
                    }
                },
                "required": ["command"]
            }
        }
    }
]
