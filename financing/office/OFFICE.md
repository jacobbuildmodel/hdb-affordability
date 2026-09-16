# OFFICE.md -- how the sessions work together

Pilot: HDB financing piece, from 16 September 2026.
Roles last changed 17 September 2026 (MSG 005): the checker is now `claude-e4`.

## Roles

| Name | Where it runs | Does | Never does |
|---|---|---|---|
| `claude-e4` (checker) | Cowork, cloud | reviews, runs checks, decides what is ready, writes push instructions | writes research |
| `hdb` (researcher) | Claude Code session in the browser, on this repo, branch `financing-wip` | THESIS, scripts, figures, drafts, all inside `financing/`; commits and pushes to `financing-wip` only | touches `main`, merges, edits outside `financing/` (except files the checker names) |
| Jacob | anywhere | decisions, downloads the checker cannot reach, opens and merges the pull request | relays routine messages |

`claude-2a` was the checker from 16 to 17 September 2026 and is retired from that
role. Messages 001 to 004 in `INBOX.md` are from `claude-2a` and stand as written;
nothing in them is reassigned by the handover.

The PowerShell session is **retired for this piece.** It was the earlier researcher
environment and is no longer a channel, a runner, or a place work is done. Its one
lasting artefact is the environment note in OUTBOX MSG 004 item 4 (`python3`
resolving to a Windows Store stub), which is a property of that retired machine and
not a repository defect.

## Channels, in order of preference

Direct session-to-session messaging was tested on 16 Sep 2026 and did not connect,
and is still not connected. So:

1. **Checker to researcher:** Jacob pastes the checker's short MSG into the
   researcher session.
2. **Researcher to checker:** the researcher appends its reply to
   `financing/office/OUTBOX.md`, commits and pushes `financing-wip`, and tells
   Jacob "pushed MSG nnn". The checker reads the branch directly from GitHub.
   Jacob carries no files.
3. Jacob, for decisions.

## Getting data into the repository

Data files are **uploaded to `raw/` on the `financing-wip` branch through
github.com**, by Jacob, in the browser. The researcher session does not fetch them
and the checker cannot reach them. This replaces the earlier upload-to-chat route.

After an upload the researcher regenerates `CHECKSUMS.md5` (see Rules, item 5) so
every new file in `raw/` is recorded with its md5 before anything is computed from
it.

## Merging

Merging to `main` is a **GitHub pull request that Jacob clicks**, after the checker
has signed off on the branch. Neither Claude session merges, and neither opens the
pull request without being asked. The order is fixed:

1. Researcher pushes to `financing-wip`.
2. Checker verifies from a fresh GitHub download and signs off.
3. Jacob opens and merges the pull request.

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
2. The researcher pushes only to `financing-wip`. The checker verifies the branch
   from a fresh GitHub download; only then does Jacob merge to `main` by pull
   request.
3. Decisions that belong to Jacob (design, dates, scope, compliance) are escalated,
   never settled between sessions.
4. House style, compliance and verification rules are in PROJECT.md and the brief.
   They apply unchanged.
5. `CHECKSUMS.md5` is regenerated as the **last edit before committing**, never
   earlier, and the result is proved by running `run_all.sh` from a fresh clone of
   the pushed branch rather than from a working copy. Regenerating it before a
   later edit to any checksummed file is what produced the MISMATCH reported in
   MSG 005.
