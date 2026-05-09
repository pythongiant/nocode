# main.py
# Entry point for NOCODE agent

import argparse
import os
import sys
from pathlib import Path


def main():
    """Main entry point.

    Usage:
        nocode              # run in current directory
        nocode <path>       # cd into <path> first, then run
    """
    parser = argparse.ArgumentParser(
        prog="nocode",
        description="NOCODE — autonomous coding agent.",
    )
    parser.add_argument(
        "path",
        nargs="?",
        default=".",
        help="Working directory the agent should operate in (default: current).",
    )
    parser.add_argument(
        "-y", "--yes",
        action="store_true",
        help="Auto-approve every shell command (skip the y/n/a prompt).",
    )
    args = parser.parse_args()

    target = Path(args.path).expanduser().resolve()
    if not target.is_dir():
        print(f"nocode: not a directory: {target}", file=sys.stderr)
        sys.exit(1)
    os.chdir(target)

    # Imports happen AFTER chdir so config.py snapshots the right CWD.
    from rich.prompt import Prompt
    from .config import console, PROMPT_COLOR, ERROR_COLOR
    from .ui import header
    from .agent import run_agent
    from .permissions import set_auto_approve

    set_auto_approve(args.yes)

    os.system("clear")
    header()

    while True:
        try:
            user_input = Prompt.ask(
                f"\n[{PROMPT_COLOR}]>[/{PROMPT_COLOR}]"
            )

            if user_input.lower() in ["exit", "quit"]:
                break

            run_agent(user_input)

        except KeyboardInterrupt:
            console.print(f"\n[{ERROR_COLOR}]bye[/{ERROR_COLOR}]")
            break

        except Exception as e:
            console.print(
                f"\n[{ERROR_COLOR}]ERROR:[/{ERROR_COLOR}] {str(e)}"
            )


if __name__ == "__main__":
    main()
