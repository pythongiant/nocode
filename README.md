# NOCODE Agent - Refactored Structure

This project has been refactored into multiple focused modules for better code organization and maintainability.

## Project Structure

### `main.py` (Entry Point)
- The application's entry point
- Handles the main REPL loop
- Minimal logic - delegates to other modules

### `config.py` (Configuration & Shared Instances)
- API configuration (model, base URL, API key)
- Workspace configuration
- Shared instances (OpenAI client, Rich console)
- System prompt for the agent

### `tools.py` (Tool Implementations)
- All tool functions (read_file, write_file, list_files, run_terminal_command)
- Tools registry (`TOOLS` dict)
- Tool schemas for the API (`TOOL_SCHEMAS`)

### `ui.py` (User Interface)
- All Rich UI rendering functions
- Header display
- Tool call/result panels
- Thinking and response rendering
- Spinner creation

### `parser.py` (Stream Parsing)
- Token parsing logic for thinking/response separation
- `parse_stream_token()` function that handles `<think>` tags

### `agent.py` (Agent Logic)
- Message history management
- Main `run_agent()` function
- Agent loop implementation
- Tool execution and response handling

## Module Dependencies

```
main.py
├── config (for console, header setup)
├── ui (for header, UI display)
└── agent (for run_agent function)

agent.py
├── config (for client, SYSTEM_PROMPT)
├── tools (for TOOLS, TOOL_SCHEMAS)
├── parser (for parse_stream_token)
└── ui (for UI rendering functions)

ui.py
└── config (for console, MODEL_NAME, BASE_URL, WORKSPACE)

tools.py
└── config (for WORKSPACE)

parser.py
└── (no external dependencies)

config.py
└── (only standard library + openai, rich)
```

## Running the Application

```bash
python main.py
```

## Benefits of This Refactoring

1. **Clear Separation of Concerns** - Each module has a single responsibility
2. **Easier Testing** - Individual modules can be tested in isolation
3. **Better Maintainability** - Changes to one concern don't affect others
4. **Reusability** - Modules can be imported and used independently
5. **Scalability** - Easy to add new features or modify existing ones
6. **Collaborative Development** - Multiple developers can work on different modules
