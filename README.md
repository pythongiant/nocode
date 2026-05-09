# NOCODE

An autonomous, terminal-native coding agent — Claude Code-style UX, but pointed at any OpenAI-compatible model (local or hosted).

NOCODE installs as a single CLI command, `nocode`, that you can run from **any directory on your system**. It treats the directory you launch it in as the workspace and drives a live REPL with streaming responses, separated thinking panels, and shell tool execution.

---

## Install

From the repo root:

```bash
pip install .
```

Or, if you're hacking on it:

```bash
pip install -e .
```

That registers a `nocode` console script on your `$PATH`.

---

## Usage

```bash
nocode              # run the agent in the current directory
nocode .            # same thing, explicit
nocode ~/projects/foo   # cd into that path first, then run
python -m nocode    # equivalent module entry point
```

Inside the REPL:

- Type a prompt, hit enter — the agent streams its response and may call tools.
- `exit` or `quit` to leave. `Ctrl+C` also works.

The agent runs shell commands relative to whichever directory you launched it in, so it sees *your* project, not the install location.

---

## Configuration

NOCODE reads two config files, layered from lowest to highest precedence:

1. **Bundled defaults** — shipped inside the package (`nocode/defaults/`). Always available, never edited by you.
2. **User config** — `~/.config/nocode/.env` and `~/.config/nocode/.env.colors`. The right place for your personal model/endpoint setup.
3. **Per-project override** — a `.env` or `.env.colors` in whichever directory you launch `nocode` from.
4. **Process environment** — anything exported in your shell wins over file values.

You can also set `NOCODE_CONFIG_DIR` to point at a different user config directory.

### `.env` — model & API

```bash
MODEL_NAME=qwen-coder
BASE_URL=http://localhost:11434/v1
API_KEY=dummy
```

Any OpenAI-compatible endpoint works — local llama.cpp, Ollama, vLLM, OpenAI itself, etc.

### `.env.colors` — UI theming

Override any of the Rich panel colors / titles. See [`nocode/defaults/default_env_colors`](nocode/defaults/default_env_colors) for the full list of keys.

### First-time setup

```bash
mkdir -p ~/.config/nocode
cp nocode/defaults/default_env        ~/.config/nocode/.env
cp nocode/defaults/default_env_colors ~/.config/nocode/.env.colors
# edit ~/.config/nocode/.env to point at your model
```

---

## How it works

The agent has one tool: `run_terminal_command`. Every action — reading, writing, listing, testing, building — happens via shell commands executed in your working directory. Output streams back to the model, which decides the next step. The loop continues until the model emits no more tool calls.

Streaming output is split into two panels:
- **thinking** (dimmed) — anything the model wraps in `<think>...</think>`
- **response** (rendered as Markdown) — everything else

---

## Project layout

```
nocode/                       # the installable package
├── __init__.py
├── __main__.py               # `python -m nocode`
├── main.py                   # CLI entry point + arg parsing
├── config.py                 # layered .env loading, OpenAI client
├── agent.py                  # streaming loop, tool dispatch, history
├── tools.py                  # run_terminal_command + schemas
├── parser.py                 # <think> tag stream parser
├── ui.py                     # Rich panels, header, spinner
└── defaults/
    ├── default_env           # bundled fallback model config
    └── default_env_colors    # bundled fallback theme
pyproject.toml                # build + console_scripts
```

---

## Requirements

- Python 3.9+
- An OpenAI-compatible chat completions endpoint with tool-calling support

Dependencies (`openai`, `python-dotenv`, `rich`) are pulled in automatically by pip.
# nocode
