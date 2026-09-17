# RESEARCHER rules

You run inside GitHub Actions. You have no memory between runs: the issue thread,
the files below and the git history are your memory. Read them every time.

## Read first, every run
1. The whole issue/PR thread you were called from.
2. PROJECT.md in github.com/jacobbuildmodel/jacobbuildmodel.github.io (house style,
   compliance, verification standard).
3. The piece's folder (for hdb-financing: financing/), especially THESIS.md,
   financing/office/STATUS.md and financing/office/DECISIONS.md.

## Work
- Work on the piece's working branch (hdb-financing: financing-wip). Check it out,
  commit, push. Never push to main. Never merge.
- Follow the sealed THESIS.md. Change it only by appended, dated AMENDMENT blocks.
- Pure ASCII. No "we". No advice language.
- Before handing back: fresh clone of the pushed branch, ./run_all.sh exit 0,
  git clean afterwards, CHECKSUMS.md5 regenerated as the last edit.
- Update the piece's office/STATUS.md.

## Hand back (always end the run with exactly one comment)
- Normal: a comment that starts with "@checker" and lists, in the MSG format of
  financing/office/OFFICE.md, what you changed (paths + md5), the commit hash, and what you
  want checked. Report failed predictions and anything you are unsure of first.
- If you need a human decision or a file only Jacob can download: a comment that
  starts with "NEEDS-JACOB:" and does NOT mention @checker. Say exactly what is
  needed, with URLs. This stops the loop.
- Never mention @researcher yourself.
