# OFFICE.md -- how the sessions work together

Pilot: HDB financing piece, from 16 September 2026.

## Roles

| Name | Where it runs | Does | Never does |
|---|---|---|---|
| `claude-2a` (checker) | Cowork, cloud | reviews, runs checks, decides what is ready, writes push instructions | writes research |
| `hdb` (researcher) | Claude Code cloud session, repo `hdb-affordability`, branch `financing-wip` | THESIS, scripts, figures, drafts, all inside `financing/`; commits and pushes to `financing-wip` only | touches `main`, merges, edits outside `financing/` (except files the checker names) |
| Jacob | anywhere | decisions, downloads the checker cannot reach, approves pushes | relays routine messages |

## Channels, in order of preference

Direct session-to-session messaging was tested on 16 Sep 2026 and did not connect. So:
1. **Checker to researcher:** Jacob pastes the checker's short MSG into the researcher session.
2. **Researcher to checker:** the researcher appends its reply to `financing/office/OUTBOX.md`, commits and pushes `financing-wip`, and tells Jacob "pushed MSG nnn". The checker reads the branch directly from GitHub. Jacob carries no files.
3. Jacob, for decisions.

## Message format (every message, both directions)

```
MSG <nnn> | from <name> | <date>
PIECE: hdb-financing
NEED: <one line: what you want from the recipient>
FILES: <path> md5 <hash>   (one per line; never paste file contents)
BLOCKER: <none | what stops you>
---
<body: as short as it can be; numbered points; no recap of earlier messages>
```

## Shared state (in `financing/office/`)

- `STATUS.md` -- one table: stage, blocker, who acts next. Update it on every handover.
- `DECISIONS.md` -- date | decision | decided by. Only Jacob's decisions and checker rulings go here.

## Rules

1. Point to files by path and md5. Do not paste them.
2. The researcher pushes only to `financing-wip`. The checker verifies the branch from a fresh GitHub download; only then does Jacob merge to `main`.
3. Decisions that belong to Jacob (design, dates, scope, compliance) are escalated, never settled between sessions.
4. House style, compliance and verification rules are in PROJECT.md and the brief. They apply unchanged.
