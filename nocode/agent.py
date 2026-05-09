# agent.py
# Agent loop implementation

import json
from rich.live import Live

from .config import client, console, MODEL_NAME, SYSTEM_PROMPT
from .tools import TOOLS, TOOL_SCHEMAS, _consume_changes
from .parser import parse_stream_token
from .ui import (
    print_tool_call,
    print_tool_result,
    print_file_changes,
    render_thinking_response,
    get_thinking_spinner
)

# =========================================================
# MESSAGE HISTORY
# =========================================================

messages = [
    {
        "role": "system",
        "content": SYSTEM_PROMPT
    }
]


def reset_messages():
    """Reset message history"""
    global messages
    messages = [
        {
            "role": "system",
            "content": SYSTEM_PROMPT
        }
    ]


# =========================================================
# AGENT LOOP
# =========================================================

def run_agent(user_prompt: str):
    """
    Run the agent loop with the given user prompt.
    
    The agent will:
    1. Send prompt to model with available tools
    2. Stream response with thinking/response separation
    3. Execute any tool calls
    4. Continue until no more tool calls
    """
    global messages

    messages.append({
        "role": "user",
        "content": user_prompt
    })

    while True:

        console.print()

        thinking_buffer = ""
        response_buffer = ""

        state = {
            "thinking": False
        }

        tool_calls_accumulator = {}

        spinner = get_thinking_spinner()

        with Live(
            spinner,
            refresh_per_second=20,
            console=console,
            transient=False,
        ) as live:

            stream = client.chat.completions.create(
                model=MODEL_NAME,
                messages=messages,
                tools=TOOL_SCHEMAS,
                tool_choice="auto",
                temperature=0.7,
                max_tokens=4096,
                stream=True,
            )

            for chunk in stream:

                delta = chunk.choices[0].delta

                # ============================================
                # CONTENT STREAMING
                # ============================================

                if delta.content:

                    token = delta.content

                    thinking_buffer, response_buffer = parse_stream_token(
                        token,
                        state,
                        thinking_buffer,
                        response_buffer
                    )

                    live.update(
                        render_thinking_response(
                            thinking_buffer,
                            response_buffer
                        )
                    )

                # ============================================
                # TOOL CALL STREAMING
                # ============================================

                if delta.tool_calls:

                    for tc in delta.tool_calls:

                        idx = tc.index

                        if idx not in tool_calls_accumulator:

                            tool_calls_accumulator[idx] = {
                                "id": "",
                                "name": "",
                                "arguments": ""
                            }

                        if tc.id:
                            tool_calls_accumulator[idx]["id"] = tc.id

                        if tc.function:

                            if tc.function.name:
                                tool_calls_accumulator[idx]["name"] = (
                                    tc.function.name
                                )

                            if tc.function.arguments:
                                tool_calls_accumulator[idx]["arguments"] += (
                                    tc.function.arguments
                                )

        # =====================================================
        # FINAL TOOL CALL FORMAT
        # =====================================================

        final_tool_calls = []

        for tc in tool_calls_accumulator.values():

            final_tool_calls.append({
                "id": tc["id"],
                "function": {
                    "name": tc["name"],
                    "arguments": tc["arguments"]
                }
            })

        # =====================================================
        # SAVE ASSISTANT MESSAGE
        # =====================================================

        messages.append({
            "role": "assistant",
            "content": response_buffer,
            "tool_calls": (
                final_tool_calls
                if final_tool_calls
                else None
            )
        })

        # =====================================================
        # NO TOOL CALLS = DONE
        # =====================================================

        if not final_tool_calls:
            break

        # =====================================================
        # EXECUTE TOOLS
        # =====================================================

        for tool_call in final_tool_calls:

            tool_name = tool_call["function"]["name"]

            try:

                args = json.loads(
                    tool_call["function"]["arguments"]
                )

            except Exception:

                args = {}

            print_tool_call(
                tool_name,
                args
            )

            if tool_name not in TOOLS:

                result = (
                    f"ERROR: unknown tool {tool_name}"
                )

            else:

                try:

                    result = TOOLS[tool_name](**args)

                except Exception as e:

                    result = f"ERROR: {str(e)}"

            print_tool_result(result)
            print_file_changes(_consume_changes())

            messages.append({
                "role": "tool",
                "tool_call_id": tool_call["id"],
                "name": tool_name,
                "content": str(result)
            })
