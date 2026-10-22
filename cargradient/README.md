# cargradient

Does a dearer COE tilt HDB resale prices toward the city centre? This study
applies the method of Huang, Li and Ross (2018), who studied private homes, to
HDB resale flats. THESIS.md was sealed on 12 October 2026 (commit 7ee9b91,
registered at https://osf.io/rntsk) before any resale price was opened; the
results are in RESULTS.md. Run `bash cargradient/run_all.sh`.

**NOTE.md is the public form of this piece.** ARTICLE.md, the earlier
long-form draft, is superseded and kept only as a record.

| Path | What it is |
|---|---|
| NOTE.md | the public research note: finding, sealed bets, limits, method, links |
| ARTICLE.md | superseded long-form draft (Checkpoint 2), kept as a record |
| THESIS.md | the tests, windows, gates and verdict rule (sealed; never edited) |
| THESIS_ADDENDUM.md | dated records and rulings after the seal; none changes a test or a score |
| SEAL_MANIFEST.md | md5 of every file fixed at the seal |
| RESULTS.md, out/, figs/ | the real-data results, written by 10-15 |
| article/ | scripts for town distances and town prices used by ARTICLE.md (not sealed, not scored) |
| office/ | paper notes, Rule 0, feasibility, design sketch, titles |
| 00_coverage.py | labels and counts of the five resale files; the price column is never parsed -> out/coverage.txt |
| 00_addresses.py | block, street and month from the five resale datasets (no price field) -> out/addresses.csv |
| 01_coe_ranges.py | quarterly COE premium, categories A and B, as the paper builds it -> out/coe_ranges.txt |
| 04_coe_crossings.py | when the A and B premiums were at or above $100,000, bidding by bidding -> out/coe_crossings.txt |
| 01_geocode.py | OneMap Search for each block -> out/blocks_geocoded.csv (cache out/geocode_cache.jsonl is not committed) |
| 02_distance.py | great-circle km to Raffles Place and City Hall MRT -> out/block_distance.csv, out/station_points.csv |
| 03_unmatched.py | resale rows per pair (counts only) and the unmatched pairs -> out/address_rowcounts.csv, out/unmatched.csv |
| 05_street_points.py | OneMap street points for the streets of the unmatched pairs (sensitivity J) -> out/street_points.csv |
| cglib.py | shared windows, thresholds, the seal guard and the outcome rules |
| 10_load.py | the analysis panel; refuses raw/ until SEALED exists -> out/panel.csv.gz, coe_quarterly.csv, geocode_coverage.csv |
| 11_tests.py | T1-T3, both gates, the sensitivities, section 7A and the verdict -> out/tests.csv and others |
| 12_figures.py | two charts with finding titles -> figs/ |
| 13_results.py | RESULTS.md, failures first |
| 14_manifest.py | checksums, number check, and --seal for SEAL_MANIFEST.md |
| 15_reproduce.py | independent route (numpy only) to every scored number |
| tests/ | invented-data fixtures and the suite that forces every outcome branch and checks the guard |
| run_all.sh | the suite always; the real run only after the seal |
| raw/ | sources, with URL, date and md5 in raw/RETRIEVED.txt; raw/hansard/ holds the Parliament records |

Run from the repository root. 01_geocode.py needs ONEMAP_EMAIL and
ONEMAP_PASSWORD in the environment. The token is held in memory only, and
calls are limited to one per second.

## Attribution

Contains information from OneMap (Singapore Land Authority), accessed 5
October 2026, under the Singapore Open Data Licence version 1.0.

Resale, COE and MRT exit data: data.gov.sg and SingStat (data source LTA),
under the Singapore Open Data Licence version 1.0.
