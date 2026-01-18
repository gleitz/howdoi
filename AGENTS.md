# AGENTS.md

## Overview
- Personal note-taking CLI that indexes YAML knowledge base files for fast search.
- Primary command: `howdou <search terms>`.
- Local search uses SQLite FTS5 for indexing and retrieval.

## Key Files
- `howdou/howdou.py`: core CLI, YAML parsing, indexing, and search logic.
- `howdou/tests.py`: unit/integration tests (hit local index and remote search).
- `README.md`: usage and YAML knowledge base format.

## Data Model
- Knowledge base is a YAML list of entries with `questions` and `answers`.
- Answers can include `weight`, `date`, `source`, `formatter`, and `text`.
- Entries can include `include` keys to pull in additional YAML files.

## Runtime Paths and Env Vars
- `HOWDOU_KB`: YAML knowledge base file (default `~/.howdou.yml`).
- `HOWDOU_INDEX`: logical index name used to derive the SQLite filename (default `howdou`).
- `HOWDOU_DB`: override SQLite database path (optional).
- `HOWDOU_TIMESTAMP`: timestamp file used to detect changes.
- `HOWDOU_DIR`: app data directory for index hashes.
- `HOWDOU_LOCKFILE`: file lock path for reindexing.
- `HOWDOU_LOCALIZATION`: search localization (e.g., `en`, `pt-br`).
- `HOWDOU_DISABLE_SSL`: use HTTP for Google queries if SSL fails.

## How It Works
- `howdou --action=reindex` parses YAML, builds per-question/answer documents, and indexes them.
- `howdou <query>` searches the local SQLite index first; falls back to remote StackOverflow if no local result unless `--ignore-remote` is set.
- Indexing is incremental unless `--force` is supplied.

## Development Notes
- Tests require SQLite with FTS5 enabled and network access.
- `./test.sh` runs `pylint` and `tox`.
- Tests isolate data in `/tmp` and use the `howdou-test` index name.
- Keep search/index code backend-light; SQLite FTS5 is the current local store.

## Agent testing
When running local tests as an agent, prefer a per-agent venv at `.<agent_name>/.venv`.

The value <agent_name> is the simplified lowercase version of your name. e.g. Codex would be "codex", Claude would be "claude", Gemini would be "gemini", etc.

## Session Logging (IMPORTANT)

Always log each action you take to `.<agent_name>/log.txt` (lowercase) to maintain continuity between sessions. Format:
```
YYYY-MM-DD HH:MM:SS - Brief description of action taken or finding
```

Examples:
- `2025-12-18 17:45:01 - Ran: glob **/*zigbee* - Found notes/claude-ha-zigbee-audio-fix-addendum.md`
- `2025-12-18 17:45:50 - CONFIRMED: Zigbee coordinator is unresponsive to ZNP commands`

At session start, read `.<agent_name>/log.txt` to understand what was done previously. This file is gitignored.

Agent name rules:
- Must be lowercase
- Codex/OpenAI: `codex`
- Gemini: `gemini`
- Claude: `claude`

## Session Reload (IMPORTANT)
At session start, read these files to restore context:
```bash
cat STATE.txt
cat DECISIONS.txt
cat TODO.txt
cat CONTEXT.txt
```

.<agent_name>/
├── STATE.md        # current goals, constraints, known issues
├── DECISIONS.md    # why things were done a certain way
├── TODO.md         # pending tasks
└── CONTEXT.md      # compressed narrative summary
