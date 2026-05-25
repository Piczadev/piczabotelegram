# Agent Instructions

## Identity & Mindset
- **Profile**: Yahir Rivera Flores (piczadev) - High-Performance Engineering, Blockchain & AI.
- **Tone**: Concise, technical, practical, skeptical, curious. No filler or pleasantries.
- **Cognitive Model**: Hyperfocus driven, systemic thinking (systems as debuggable architectures).
- **Preferences**: Deep work, out-of-the-box ideas, local/sovereign AI preference, automation over manual tasks.

## Current Project: Telegram SysBot
- **Tech Stack**: Python (asyncio), `python-telegram-bot` (v20+), `google-generativeai`, `aiofiles`.
- **Architecture**: Fully asynchronous. Modular handlers.
- **Core Rule**: Never use synchronous `open()`; always use `aiofiles` to prevent blocking the event loop.

## Package Manager & Environment
- **OS**: macOS (Apple Silicon).
- **Package Manager**: `pip` (active `venv`).

## File-Scoped Commands
| Task | Command |
|------|---------|
| Run Bot | `python bot/main.py` |
| Install Deps | `pip install <package>` |

## Code Conventions
- Use strict asynchronous patterns (`async`/`await`).
- Keep `main.py` limited to environment setup and orchestrating handlers.
- Secure all API keys (`TELEGRAM_TOKEN`, `GEMINI_API_KEY`) via `.env`.
- Ensure robust logging (INFO level minimum).

## Commit Attribution
AI commits MUST include:
```text
Co-Authored-By: Gemini Antigravity <noreply@google.com>
```
