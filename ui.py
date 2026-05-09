# ui.py
# UI rendering functions

import json
from rich.console import Console, Group
from rich.markdown import Markdown
from rich.panel import Panel
from rich.text import Text
from rich.spinner import Spinner
from config import (
    MODEL_NAME,
    BASE_URL,
    WORKSPACE,
    console,
    HEADER_BORDER_COLOR,
    HEADER_TEXT_COLOR,
    TOOL_CALL_BORDER_COLOR,
    TOOL_RESULT_BORDER_COLOR,
    THINKING_BORDER_COLOR,
    THINKING_TEXT_COLOR,
    RESPONSE_BORDER_COLOR,
    SPINNER_COLOR,
    SPINNER_TEXT_COLOR,
    TOOL_CALL_TITLE,
    TOOL_RESULT_TITLE,
    THINKING_TITLE,
    RESPONSE_TITLE,
    WAITING_MESSAGE,
)

# =========================================================
# HEADER
# =========================================================

def header():
    """Print the welcome header"""
    logo = r"""
███╗   ██╗ ██████╗  ██████╗ ██████╗ ██████╗ ███████╗
████╗  ██║██╔═══██╗██╔════╝██╔═══██╗██╔══██╗██╔════╝
██╔██╗ ██║██║   ██║██║     ██║   ██║██║  ██║█████╗
██║╚██╗██║██║   ██║██║     ██║   ██║██║  ██║██╔══╝
██║ ╚████║╚██████╔╝╚██████╗╚██████╔╝██████╔╝███████╗
╚═╝  ╚═══╝ ╚═════╝  ╚═════╝ ╚═════╝ ╚═════╝ ╚══════╝
"""

    body = f"""
[{HEADER_TEXT_COLOR}]{logo}[/{HEADER_TEXT_COLOR}]

[bold white]model:[/bold white] {MODEL_NAME}
[bold white]base url:[/bold white] {BASE_URL}
[bold white]workspace:[/bold white] {WORKSPACE.resolve()}
"""

    console.print(
        Panel.fit(
            body,
            border_style=HEADER_BORDER_COLOR
        )
    )


# =========================================================
# TOOL OUTPUT PANELS
# =========================================================

def print_tool_call(name: str, args: dict):
    """Print tool call information"""
    pretty = json.dumps(args, indent=2)

    console.print()

    console.print(
        Panel.fit(
            pretty,
            title=f"TOOL CALL → {name}",
            border_style="yellow"
        )
    )


def print_tool_result(result: str):
    """Print tool execution result"""
    console.print(
        Panel.fit(
            str(result),
            title="TOOL RESULT",
            border_style="green"
        )
    )


# =========================================================
# THINKING & RESPONSE PANELS
# =========================================================

def render_thinking_response(thinking_buffer: str, response_buffer: str) -> Group:
    """Render thinking and response panels"""
    panels = []

    if thinking_buffer.strip():
        panels.append(
            Panel(
                Text(
                    thinking_buffer,
                    style="dim white"
                ),
                title="[dim]thinking[/dim]",
                border_style="bright_black",
            )
        )

    if response_buffer.strip():
        panels.append(
            Panel(
                Markdown(response_buffer),
                title="RESPONSE",
                border_style="cyan",
            )
        )

    if not panels:
        panels.append(
            Panel(
                "Waiting for model output...",
                border_style="dim"
            )
        )

    return Group(*panels)


# =========================================================
# SPINNER
# =========================================================

def get_thinking_spinner() -> Spinner:
    """Get a spinner for thinking state"""
    return Spinner(
        "dots",
        text=Text(
            " thinking...",
            style="cyan"
        )
    )
