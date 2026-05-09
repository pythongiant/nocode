# main.py
# Entry point for NOCODE agent
#
# FEATURES
# - Smooth streaming
# - Separate THINKING panel
# - Proper live token rendering
# - OpenAI/Hermes/Qwen tool calling
# - File tools
# - Terminal execution
# - Autonomous agent loop
# - Claude-Code style UX
#
# INSTALL:
# pip install openai rich
#
# RUN:
# python main.py

import os
from rich.prompt import Prompt
from config import console
from ui import header
from agent import run_agent, reset_messages






def main():
    """Main entry point"""
    os.system("clear")

    header()

    while True:

        try:

            user_input = Prompt.ask(
                "\n[bold cyan]>[/bold cyan]"
            )

            if user_input.lower() in ["exit", "quit"]:
                break

            run_agent(user_input)

        except KeyboardInterrupt:

            console.print(
                "\n[red]bye[/red]"
            )

            break

        except Exception as e:

            console.print(
                f"\n[red]ERROR:[/red] {str(e)}"
            )


if __name__ == "__main__":
    main()
