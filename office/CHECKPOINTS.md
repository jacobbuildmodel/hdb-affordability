# CHECKPOINTS -- objective pass criteria

Purpose: nothing reaches Jacob as "ready" unless every box below is ticked with
evidence (a command output, an md5, a file path, or a page and line). A box that
cannot be ticked is a FAIL, not a judgement call. Each checkpoint is passed twice:
first by the bot checker (office/CHECKER.md), then independently by the Cowork
checker, who also compares its findings with the bot's.

## Checkpoint 1 -- analysis, charts and headline numbers
Goal: the numbers are right, reproducible, and scored honestly against the seal.
- [ ] THESIS.md was sealed in a commit that comes BEFORE the first commit reading F1.
- [ ] Fresh clone of the named commit: ./run_all.sh exit 0; git status clean after.
- [ ] Every md5 quoted in the hand-back matches.
- [ ] Each headline number reproduced by an independent script to the published precision.
- [ ] Every prediction scored PASS/FAIL in RESULTS.md against the sealed wording, verbatim.
- [ ] Failed predictions reported first in the hand-back.
- [ ] The T1b weak-evidence sentence is present next to the headline number.
- [ ] requirements.txt covers every import.
- [ ] Chart 1 and Chart 2 exist as SVG, each with a prefers-color-scheme block.
- [ ] Both charts rendered at 390px and 1280px, light and dark (4 images each),
      with no clipped text, no overlapping labels, and a legible zero line on Chart 2.
- [ ] The finding is under 60 characters and is supported by a number in RESULTS.md.
- [ ] Pure ASCII across financing/.

## Checkpoint 2 -- draft article
Goal: a non-specialist can follow it, and it says nothing the data does not support.
- [ ] All Checkpoint 1 boxes still pass on the new commit.
- [ ] Structure: hook blockquote, unheaded intro, storyline headings, what would
      prove this wrong, what this does not explain, what to take from this, sources.
- [ ] 1,200 to 1,800 words of linear prose (count reported).
- [ ] Headline is the finding, under 60 characters.
- [ ] Every number in the prose is in the number manifest with its script.
- [ ] Every source cited opens to a file in raw/ listed in RETRIEVED.txt.
- [ ] No "we"; no em dash, U+2212 or U+00D7.
- [ ] Banned-word grep clean: choose, should, recommend, better option, you should.
- [ ] Not-advice line present; findings in past tense and by cohort.
- [ ] Front matter: draft: true, date 2026-09-26 unless Jacob changed it, repo and dataset fields.
- [ ] Date not already used in content/economics/.

## Checkpoint 3 -- ready to merge and publish
Goal: what ships is exactly what was checked.
- [ ] All Checkpoint 1 and 2 boxes pass on the PR head commit.
- [ ] PR diff contains only the intended paths; top-level README lists financing/.
- [ ] run_all.sh at repo root rebuilds both the original analysis and financing/.
- [ ] Site build (Hugo) with the article passes; screenshots at 390px and desktop,
      light and dark, reviewed.
- [ ] Publish gate and prose linter pass as CI runs them.
- [ ] Jacob has seen the headline, the two charts and the three numbers.
