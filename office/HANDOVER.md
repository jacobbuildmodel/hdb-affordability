# HANDOVER -- hdb-affordability (researcher role)

Written 11 October 2026 for a new chat with no history. Read this, then the
files it points to. The root HANDOVER.md is the old September brief for the
website chat and is stale.

## 1. What this repo holds

Public analysis repo behind jacobbuildmodel.github.io. Each piece has a
THESIS.md sealed before its data is opened, a one-command pipeline, and
checksums. The site repo (jacobbuildmodel/jacobbuildmodel.github.io) holds
the pages, PROJECT.md (house style) and office/ (REPLY_FORMAT, CHECKPOINTS,
EDITOR, QUESTION_RULES, STORY_CRAFT).

| Piece | Where | Status |
|---|---|---|
| HDB affordability | repo root (00-08_*.py, THESIS.md, 2026-09-12.md) | sealed 12 Sep 2026; data opened; published as content/economics/2026-09-19.md |
| Financing (HDB loan vs SORA) | financing/ | sealed 17 Sep 2026 (0ed509e); data opened; published as content/economics/2026-10-03.md |
| cargradient (COE x distance, HDB resale) | cargradient/ on branch cargradient-wip ONLY | NOT sealed; no resale price opened; pre-seal |

cargradient is a conceptual replication of Huang, Li and Ross (2018, RSUE
68:160-171) on HDB resale data: T1 (2002-2015), T2 (2016-2026), T3 (did the
COE tilt weaken after quota growth went to zero in Feb 2018). Everything is
in cargradient/THESIS.md; the office notes are in cargradient/office/.

## 2. Branches and PRs, next step on each

- cargradient-wip (HEAD bf30a7b): the open piece. No PR; never merged by a
  chat. Next steps, in order:
  1. Jacob rules on the drift guard (out/coverage_guard.txt, from
     `06_coverage_check.py --guard`, 11 Oct). No tested design fixed a
     persistent drift (S0 50-56% false links) without breaking the null
     (Driscoll-Kraay 10.7-21.6%) or the instrument (trend controls: T2 F
     0.8 and 0.0). The proposal was to keep S0 and seal the limit into the
     verdict wording. Then update THESIS section 6 and
     office/DESIGN_SKETCH.md; if a guard design is adopted, change 11_tests.py
     AND 15_reproduce.py the same way and rerun the fixture suite.
  2. The seal prompt: Jacob's three confidences (and T1/T2 Why lines) go into
     THESIS "Confidence at seal" lines, verbatim. Then
     `python3 cargradient/14_manifest.py --seal` writes SEAL_MANIFEST.md, then
     `touch cargradient/SEALED`, one seal commit. Only in that prompt.
  3. After the seal: `bash cargradient/run_all.sh` runs the real data.
- #2 readme-revision-note-wording (open since September): stale README
  wording fix. Leave it for Jacob; do not merge.
- handover-2026-10: this file.
- Everything else on origin is merged history.
- Site repo: never touch site PRs #17 or #22.

## 3. Rules, and where they live

- Hand-backs: site office/REPLY_FORMAT.md (STATUS / PR+HEAD / CHANGED /
  CHECKS / NEEDS JACOB; line limit as the prompt sets).
- Checkpoints: office/CHECKPOINTS.md here and in the site repo.
- Researcher and checker bots: office/RESEARCHER.md, office/CHECKER.md.
- Style: site PROJECT.md; STANDARDS v2 machine half is ./check.sh.
- cargradient question rules: cargradient/office/RULE0.md.
- Public text: pure ASCII, no em dash; no "we/us/our"; banned words should,
  recommend, choose, better option, you should. Quotes (Jacob, Hansard) are
  verbatim; wrap a flagged quote in a scoped
  `<!-- vale Site.Directives = NO -->` ... `= YES -->` pair.
- PAPER_NOTES' OLS-vs-IV catch is never described in public as an error in
  the paper.
- Commits as Jacob:
  `git -c user.name=Jacob -c user.email=jacobong999@gmail.com commit`,
  with the attribution trailers the session gives. No model names in files.
- Push only the branch named in the prompt. Never merge. Force-push only
  when asked, always `--force-with-lease=<branch>:<sha>`.
- Do not watch PRs; if a subscription appears, unsubscribe and say so.

## 4. Commands

    ./check.sh                      # STANDARDS v2: ASCII, banned words, headline, charts, pins
    ./check.sh --full               # also rebuilds the September piece and tests its guard
    ./run_all.sh                    # September piece; ends with 08_manifest.py --check
    bash cargradient/run_all.sh     # fixture suite always; real run only if SEALED exists
    python3 -W ignore -m unittest discover -s cargradient/tests -p "test_*.py" -v   # 48 tests
    python3 cargradient/14_manifest.py --check
    PYTHONPATH=cargradient python3 cargradient/06_coverage_check.py            # placebo
    PYTHONPATH=cargradient python3 cargradient/06_coverage_check.py --guard    # drift guards

Vale as CI runs it (site lint.yml): Vale 3.24.0, `vale --no-wrap <files>`
from a site checkout so .vale.ini and styles/Site/ apply. Copy the page into
the site checkout's content/ to lint it; restore any site file you touched
(`git checkout HEAD -- .vale.ini styles`). Site CI also runs
`python scripts/aitell.py <files> --strict --published-only` and
`python scripts/check_open_pages.py --base <sha>`.

Python: pandas 3.0.6, numpy 2.4.6, scipy 1.17.1, pyfixest 0.60.0
(cargradient/requirements.txt); a venv is the easy route.

## 5. Gotchas and fixes

- Long runs die at the 2-hour background limit. Launch with
  `setsid nohup ... > log 2>&1 < /dev/null &` and log progress. The placebo
  uses an exact fixed-effects projector (Projector in 06), seconds per run,
  instead of re-demeaning with MAP (minutes per run).
- `A && B & echo` backgrounds the whole chain; put `&` on its own command.
- `pgrep -f name` in a wait loop matches the loop itself; match on the
  interpreter path instead.
- MAP demeaning failed to converge on large-scale columns: columns are
  scaled to unit sd first and a finite check runs (11_tests.demeaned).
- A block-clustered first-stage F could never fire (instrument varies only
  by quarter): the F gate is two-way.
- numpy bools wrote as "0"/"1": cast gate flags with bool().
- Manifest check compared reformatted strings: compare fmt() on both sides.
- per10k sign: (5 - 20) x beta x 10000.
- The paper PDF must never be committed (copyright; it was removed from
  history once). raw_files() skips .pdf.
- Hosts: news sites are blocked (name it and stop). TfL needs bot
  verification: ask Jacob to upload the page. Chromium distrusted some
  certs: save HTML with curl instead. /usr/bin/time is missing: use $SECONDS.
- Keep `.gitattributes` (`* -text`) or checksums fail on Windows checkouts.
- panel.csv.gz is written with gzip mtime 0 so it is byte-stable.

## 6. Credentials (names only)

- ONEMAP_EMAIL, ONEMAP_PASSWORD (environment). The OneMap token is fetched
  from these, held in memory, never printed or committed. The token last
  fetched EXPIRED on 8 Oct 2026; 01_geocode.py fetches a new one. Geocoding
  is finished, so only a re-geocode needs them. If either is missing, stop
  and say so.
- GitHub: through the session's GitHub app; nothing to set by hand.

## 7. Do NOT

- Create cargradient/SEALED or SEAL_MANIFEST.md outside the seal prompt.
- Read any resale price before SEALED exists (10_load.py refuses anyway;
  00_coverage and 06 read the files with the price column excluded).
- Fit anything on real prices before the seal.
- Write or suggest a confidence. Confidences are Jacob's, at the seal.
- Edit a sealed THESIS.md (root, financing/) or any file in a
  SEAL_MANIFEST/CHECKSUMS INPUTS list. Changes go in an addendum.
- Merge any PR, or push to main.
- Edit Jacob's verbatim quotes.
