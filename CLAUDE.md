# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

# Important Note on Your Context Window
Your context window will be automatically compacted as it approaches its limit, allowing you to continue working indefinitely from where you left off. Therefore, do not stop tasks early due to token budget concerns. As you approach your token budget limit, save your current progress and state to memory before the context window refreshes. Always be as persistent and autonomous as possible and complete tasks fully, even if the end of your budget is approaching. Never artificially stop any task early regardless of the context remaining.

## Communication Style

**CRITICAL**: When working with this codebase:
- **NEVER use emojis** in any communication, code, comments, or documentation
- **Always maintain a concise, professional tone** in all interactions
- Provide direct, clear technical communication without unnecessary elaboration
- Focus on facts and technical accuracy over conversational language

## Testing and Development Files

**CRITICAL**: All testing artifacts, temporary files, and development scripts must be placed in the `/tmp` folder to maintain repository cleanliness:

- Development scripts and experiments
- Temporary output files
- Test artifacts and logs
- Mock data generators

This prevents clutter in the working directory and ensures consistent cleanup across development environments.

## Package Management

Uses **uv** for Python package and environment management. Python 3.13+ is required.