# permissions.py
# User-confirmation gate for shell commands.

from rich.panel import Panel
from rich.prompt import Prompt

from .config import (
    console,
    TOOL_CALL_BORDER_COLOR,
    PROMPT_COLOR,
    ERROR_COLOR,
)


class _State:
    auto_approve: bool = False


state = _State()


def set_auto_approve(value: bool) -> None:
    state.auto_approve = bool(value)


def confirm_command(command: str) -> bool:
    """Ask the user whether to run *command*. Returns True iff approved.

    Choices:
      y  — run this command
      n  — deny this command (model gets a "denied" result and can react)
      a  — always allow for the rest of this session
    """
    if state.auto_approve:
        return True

    console.print(
        Panel.fit(
            command,
            title="RUN COMMAND?",
            border_style=TOOL_CALL_BORDER_COLOR,
        )
    )

    while True:
        choice = Prompt.ask(
            f"[{PROMPT_COLOR}]yes / no / always[/{PROMPT_COLOR}]",
            default="y",
            show_default=True,
        ).strip().lower()

        if choice in ("y", "yes", ""):
            return True
        if choice in ("n", "no"):
            return False
        if choice in ("a", "always"):
            state.auto_approve = True
            return True

        console.print(
            f"[{ERROR_COLOR}]please answer y, n, or a[/{ERROR_COLOR}]"
        )
