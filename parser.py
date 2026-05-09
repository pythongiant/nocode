# parser.py
# Stream token parsing logic

def parse_stream_token(
    token: str,
    state: dict,
    thinking_buffer: str,
    response_buffer: str
) -> tuple:
    """
    Parse streaming tokens and separate thinking from response.
    
    Returns:
        tuple: (thinking_buffer, response_buffer)
    """
    while token:

        if not state["thinking"]:

            start = token.find("<think>")

            if start == -1:

                response_buffer += token
                token = ""

            else:

                response_buffer += token[:start]

                token = token[start + len("<think>"):]

                state["thinking"] = True

        else:

            end = token.find("</think>")

            if end == -1:

                thinking_buffer += token
                token = ""

            else:

                thinking_buffer += token[:end]

                token = token[end + len("</think>"):]

                state["thinking"] = False

    return thinking_buffer, response_buffer
