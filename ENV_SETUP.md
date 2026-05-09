# Environment Configuration Guide

This project now uses environment files for flexible configuration management.

## Files Overview

### `.env` - API Configuration
Contains hard-coded variables for the LLM integration:
```
MODEL_NAME=qwen-coder
BASE_URL=http://192.168.1.4:9005/v1
API_KEY=dummy
WORKSPACE_PATH=./workspace
```

**Customize these values to:**
- Switch to different LLM providers (OpenAI, local services, etc.)
- Update API endpoints and authentication
- Change workspace location

### `.env.colors` - UI Color Configuration
Contains all Rich color styling for the terminal UI:
```
HEADER_BORDER_COLOR=bright_cyan
HEADER_TEXT_COLOR=bold cyan
TOOL_CALL_BORDER_COLOR=yellow
...
```

**Color options include:**
- Border colors for all panels
- Text colors for specific elements
- Spinner and prompt colors
- Panel titles and messages

**Common Rich colors:**
- `bright_cyan`, `cyan`, `bright_yellow`, `yellow`
- `bright_green`, `green`, `bright_red`, `red`
- `white`, `bright_black`, `dim white`
- `bold cyan`, `bold white`, etc.

## How It Works

1. **Loading Configuration:**
   - `config.py` uses `python-dotenv` to load `.env` and `.env.colors`
   - Environment variables are accessed via `os.getenv()` with defaults

2. **Using in Code:**
   - All UI modules import color settings from `config.py`
   - API settings are centralized in one place
   - Easy to override values without modifying code

3. **Example: Changing Colors**
   ```
   # Before: hardcoded in code
   border_style="bright_cyan"
   
   # After: configurable
   border_style=HEADER_BORDER_COLOR  # from .env.colors
   ```

## Security

- `.env` files are listed in `.gitignore`
- Never commit sensitive keys to version control
- Use different `.env` files per environment (dev, staging, prod)

## Common Customizations

### Change LLM Provider
```bash
# Use OpenAI
MODEL_NAME=gpt-4
BASE_URL=https://api.openai.com/v1
API_KEY=sk-...

# Use local Ollama
MODEL_NAME=llama2
BASE_URL=http://localhost:11434
```

### Theme the UI
```bash
# Dark theme
HEADER_BORDER_COLOR=white
HEADER_TEXT_COLOR=bold white

# Calm theme
HEADER_BORDER_COLOR=green
TOOL_CALL_BORDER_COLOR=green
RESPONSE_BORDER_COLOR=green
```

## Requirements

- `python-dotenv` (already installed)
- Python 3.7+

To ensure it's installed:
```bash
pip install python-dotenv
```
