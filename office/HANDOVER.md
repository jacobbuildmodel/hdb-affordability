# HANDOVER -- hdb-affordability (researcher role)

Written 11 October 2026 for a new chat with no history. The root
HANDOVER.md is the stale September brief for the website chat.

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
  1. Drift guard (THESIS section 6 stress case). Round 1, bf30a7b,
     out/coverage_guard.txt: no design fixed a persistent drift without
     breaking the null or T2's instrument (T2 F 0.8 and 0.0 with trend
     controls: its quota variation is mostly trend). Round 2,
     out/coverage_guard2.*: time-block clusters, a two-step quarterly
     gradient (levels, first differences), drift dose-response. Jacob rules;
     then THESIS section 6 and DESIGN_SKETCH, and any adopted design goes
     into 11_tests.py AND 15_reproduce.py with the fixture suite rerun.
  2. Seal (site office/CHECKPOINTS.md, Checkpoint S; the SGD and PWM pieces
     did it this way):
     a. One commit: Jacob's three confidences (and T1/T2 Why lines) in the
        THESIS "Confidence at seal" lines, verbatim.
     b. The next commit, on its own, is the seal: SEAL_MANIFEST.md ONLY,
        written by `python3 cargradient/14_manifest.py --seal`. Record the
        hash. Never run `--seal` again after this.
     c. The same day: the open question page PR goes to the site
        (office/OPEN_QUESTION_DRAFT.md, seal link filled in); Jacob merges
        it; the checker confirms it is live; Jacob registers the thesis on
        OSF that day.
     d. Only then, in its own commit: `touch cargradient/SEALED` (the data
        key). The loader refuses raw/ until the key exists.
  3. After the data key: `bash cargradient/run_all.sh` runs the real data.
     The branch reaches main by a MERGE commit (never squash or rebase), so
     the seal and key commits stay ancestors of main.
- #2 readme-revision-note-wording (open since September): stale README
  wording fix. Leave it for Jacob; do not merge.
- handover-2026-10 is this file; every other origin branch is merged history.
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

Python: cargradient/requirements.txt (pandas 3.0.6, numpy 2.4.6, scipy
1.17.1, pyfixest 0.60.0), in a venv.

## 5. Gotchas and fixes

- Long runs die at the 2-hour background limit. Launch with
  `setsid nohup ... > log 2>&1 < /dev/null &` and log progress. The placebo
  uses an exact fixed-effects projector (Projector in 06), seconds per run,
  instead of re-demeaning with MAP (minutes per run).
- `A && B & echo` backgrounds the whole chain; `pgrep -f name` in a wait
  loop matches the loop itself (match the interpreter path).
- MAP demeaning: columns scaled to unit sd plus a finite check. The F gate
  is two-way (block-clustered, it could never fire).
- Cast gate flags with bool(); compare fmt() on both sides of the manifest
  check; per10k is (5 - 20) x beta x 10000.
- The paper PDF must never be committed (copyright; it was removed from
  history once). raw_files() skips .pdf.
- Hosts: news sites are blocked (name it and stop). TfL needs bot
  verification: ask Jacob to upload the page. Chromium distrusted some
  certs: save HTML with curl instead. /usr/bin/time is missing: use $SECONDS.
- Keep `.gitattributes` (`* -text`); panel.csv.gz uses gzip mtime 0.

## 6. Credentials (names only)

- ONEMAP_EMAIL, ONEMAP_PASSWORD (environment): the OneMap token is fetched
  from them, held in memory, never printed. The last token EXPIRED 8 Oct
  2026. Geocoding is finished; only a re-geocode needs them. Missing: stop.
- GitHub: through the session's GitHub app; nothing to set by hand.

## 7. Do NOT

- Create SEAL_MANIFEST.md outside the seal commit, or cargradient/SEALED
  before the open page is live. Never re-run `14_manifest.py --seal`.
- Read a resale price or fit on real data before SEALED exists (10_load.py
  refuses; 00_coverage and 06 never read the price column).
- Write or suggest a confidence. Confidences are Jacob's, at the seal.
- Edit a sealed THESIS.md (root, financing/) or any file in a
  SEAL_MANIFEST/CHECKSUMS INPUTS list. Changes go in an addendum.
- Merge any PR, push to main, or edit Jacob's verbatim quotes.

## 8. Starter prompt for a new chat in this role

    You are the researcher for github.com/jacobbuildmodel/hdb-affordability.
    Read office/HANDOVER.md first, then cargradient/THESIS.md and
    cargradient/office/RULE0.md. Hand-backs: office/REPLY_FORMAT.md in
    jacobbuildmodel.github.io. Work only on cargradient-wip; never merge;
    commit as Jacob (HANDOVER section 3). Read no resale price and fit
    nothing on real data until cargradient/SEALED exists. The seal follows
    HANDOVER section 2 step 2 exactly: confidences commit, then a commit
    with SEAL_MANIFEST.md only, then the open page live and OSF the same
    day, then the SEALED key in its own commit; never re-run --seal.
    Confidences are Jacob's; never write or suggest one. Current state:
    HANDOVER section 2. First run the fixture suite and check.sh and report.
