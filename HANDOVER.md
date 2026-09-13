# Brief for the website chat

You are placing finished files on jacobbuildmodel.github.io. You are not editing
them. Everything in this bundle has been verified against a reproducible pipeline;
a well-meant correction here silently breaks that chain.

## Where each file goes

| Source | Destination |
|---|---|
| `2026-09-12.md` | `content/economics/2026-09-12.md` |
| `figs/fig1_price_to_income.svg` | `static/figs/fig1_price_to_income.svg` |
| `figs/fig2_ehg_crossing.svg` | `static/figs/fig2_ehg_crossing.svg` |
| `figs/fig3_binding_constraint.svg` | `static/figs/fig3_binding_constraint.svg` |

The article references figures as `/figs/name.svg`. If your `static` layout differs,
change the destination, not the article, and tell Jacob which paths you used.

The analysis directory does not go in the Hugo site. It goes to
**github.com/jacobbuildmodel/hdb-affordability**, public, with `README.md` at the
top level of the repository. The article's front matter links to it, so the repo
must exist and be public before this piece is published.

## Rules

- **Copy the article file. Do not retype it, do not regenerate it, do not reflow
  it.** Every figure in it is listed in `number_manifest.csv` against the script that
  produced it. A retyping step breaks that silently and nothing downstream will
  catch it.
- **Do not rewrite prose that reads oddly.** It is far more likely deliberate than
  wrong. Flag it to Jacob and leave it.
- **Do not clear `draft: true`.** A human does that.
- **Do not "fix" the numbers.** Several look surprising on purpose. Prices rose 40
  per cent while the affordability ratio fell; that is the finding, not a typo.
- **Do not substitute a guess for any link.** If something will not resolve, say
  which one and stop.
- **Keep `.gitattributes`**, which contains exactly `* -text`. Without it Git
  rewrites line endings on a Windows checkout and every published checksum fails for
  reasons unrelated to the data.

## After placing, verify

- The two `{{< aside title="..." >}}` blocks render as collapsible blocks, not as
  literal text on the page. There are exactly two, one in "Everyone knows prices went
  up" and one in "The grant went up and stopped working".
- All three figures load at their new paths.
- All three are readable in dark mode. They carry their own CSS custom properties
  with literal fallbacks and should follow the site theme. Check the site is not
  overriding them.
- All three scale on a phone at 390px. They have a `viewBox` and no fixed width.
- The table of contents renders, since the front matter sets `showToc: true` and
  `TocOpen: true`.
- The linter passes. The article is pure ASCII, zero em dashes, zero U+2212, zero
  U+00D7, zero CRLF, and 1,787 words of linear read excluding the two asides and the
  Sources section.

## The repository, if you are pushing it

From inside the unpacked directory, with `README.md` at the top level:

    git init
    git add .
    git commit -m "HDB resale affordability: analysis and article"
    git branch -M main
    git remote add origin https://github.com/jacobbuildmodel/hdb-affordability.git
    git push -u origin main

Then confirm on the repo page that the README renders and that `raw/` is present
with the CSVs in it. A previous piece was pushed one directory too deep and its
README never appeared.

## If a verifier re-runs it

    rm -rf out figs && ./run_all.sh

Exit code 0, and `python3 08_manifest.py --check` reports all 59 checksums matching.
This was confirmed from a clean copy on 12 September 2026: all 14 generated files
came back byte-identical.

`CHECKSUMS.md5` is in two labelled sections. A changed INPUT means the source data or
a script moved. A changed OUTPUT with unchanged INPUTS means the pipeline is not
deterministic, which would be a real defect.

## Front matter, as shipped

    ---
    title: "A four-room flat costs less income than in 2013"
    date: 2026-09-12
    draft: true
    showToc: true
    TocOpen: true
    summary: "Everyone knows HDB resale prices have risen, and they have. Over 2013
    to 2025 median household income rose faster, so the same flat costs less income
    now than it did then, and a lot more than it did in 2019."
    tags: ["economics"]
    repo: "https://github.com/jacobbuildmodel/hdb-affordability"
    dataset: "https://data.gov.sg/datasets/d_8b84c4ee58e3cfc0ece0d773c8ca6abc/view"
    ---

Title is 47 characters.
