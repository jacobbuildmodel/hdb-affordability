# FEASIBILITY -- labels and coverage only

Checked 4 October 2026 from the research session.
No price value was printed, plotted, summarised or saved to the repo. Coverage
came from dataset metadata and from queries that asked for the `month` field
alone (first, last, row total). The COE table was read by its metadata
(series labels, first and last period), not its values.

Licence for everything on data.gov.sg: Singapore Open Data Licence version
1.0 (https://data.gov.sg/open-data-licence). SingStat's terms of use say
datasets on its services are under the same licence.

## Needs Jacob (updated round 3, 5 October 2026)

Done in round 3:
- T3's direction (weaker).
- The March 2012 options ((a) plus (d), with (c) as a sensitivity).
- The TfL page (saved by Jacob).
- The PDF (removed from the repo).

Still open:
1. OneMap: done 5 October 2026 (office/GEOCODE_REPORT.md). Fallback C
   decided 6 October 2026.
2. T3 before-window and first-stage gate: approved 5 October 2026.
3. Updated 6 October 2026: the growth-rate steps, including 0.25% before
   February 2018, are sourced from Parliament (raw/hansard/; THESIS section
   4). LTA's October 2017 release is still not found. www.mot.gov.sg and
   www.gov.sg are now allowed.

## Hosts

First check 4 October 2026 from about 10:10 UTC. Re-checked after Jacob
widened the network allowance, from about 10:29 UTC.

| Host | First check | After allowance | Used for |
|---|---|---|---|
| data.gov.sg, api-production.data.gov.sg, api-open.data.gov.sg | yes | yes | HDB resale, COE, MRT exits, HDB buildings |
| tablebuilder.singstat.gov.sg, www.singstat.gov.sg | yes | yes | COE from 2002 |
| liberalarts.tulane.edu | NO, 403 | yes | the paper (working-paper copy) |
| www.onemap.gov.sg | NO, 403 | yes | geocoding, section 3 |
| www.lta.gov.sg | NO, 403 | yes | vehicle growth rate, TEL stage dates |
| datamall.lta.gov.sg | NO, 403 | allowed, not needed yet | -- |
| www.hdb.gov.sg | NO, 403 | allowed, not needed yet | -- |
| doi.org, ideas.repec.org | NO, 403 | yes | the published version's citation |
| www.sciencedirect.com | NO, 403 | connects, answers 403 | published text not read |
| tfl.gov.uk | NO, 403 | connects, answers 403 "Verification required" | world view; stopped, not bypassed |

## 1. HDB resale flat prices (collection 189, publisher HDB)

URL pattern: https://data.gov.sg/datasets/<id>/view

| Dataset id | Name | Basis | First | Last | Rows |
|---|---|---|---|---|---|
| d_ebc5ab87086db484f88045b47411ebc5 | 1990 - 1999 | approval date | 1990-01 | 1999-12 | 287,196 |
| d_43f493c6c50d54243cc1eab0df142d6a | 2000 - Feb 2012 | approval date | 2000-01 | 2012-02 | 369,651 |
| d_2d5ff9ea31397b66239f245f57751537 | Mar 2012 to Dec 2014 | registration date | 2012-03 | 2014-12 | 52,203 |
| d_ea9ed51da2787afaf8e51f827c304208 | Jan 2015 to Dec 2016 | registration date | 2015-01 | 2016-12 | 37,153 |
| d_8b84c4ee58e3cfc0ece0d773c8ca6abc | Jan 2017 onwards | registration date | 2017-01 | 2026-10 | 241,920 |

Columns, all five: month, town, flat_type, block, street_name, storey_range,
floor_area_sqm, flat_model, lease_commence_date, resale_price. The 2015-2016
and 2017-onwards files add remaining_lease. 2026-10 is a part month (checked
on 4 October). Every column the brief names is present (lease start is
lease_commence_date).

Watch: the basis changes from approval date to registration date in March
2012, inside the paper's 2002-2015 window. SOURCES.md for the affordability
piece excluded the approval-date files for that reason; this piece cannot,
because test 1 needs 2002-2011.

## 2. COE bidding results

| Source | Id | First | Last | Size | Columns or series |
|---|---|---|---|---|---|
| data.gov.sg, "COE Bidding Results / Prices" | d_69b3380ad7e51aff3a7dcc84eba52b8a | 2010-01 | 2026-09 | 1,980 rows | month, bidding_no, vehicle_class, quota, bids_success, bids_received, premium |
| SingStat Table Builder, "Motor Vehicle Quota, Quota Premium And Prevailing Quota Premium, Monthly" (data source LTA) | M651121 | 2002 Feb | 2026 Sep | 50 series | quota, successful bids, bids received, quota premium, per bidding, for cars up to 1600cc and 97kW (A), above (B), goods vehicles and buses, motorcycles, open; prevailing quota premium |

The data.gov.sg file starts in 2010, so test 1 (from 2002) needs SingStat
M651121. SingStat footnote, in short: February and March 2002 first bidding
was closed bidding; open bidding from April 2002; no bidding in April, May
and June 2020. Category definitions changed (the data.gov.sg description
dates one change to the May 2022 first exercise); SingStat labels use one
label across the whole series. The paper used categories A and B, with each
bidding weighted by successful bids and averaged within the quarter (PAPER_NOTES
section 4). M651121 carries all three inputs per bidding, so it can be rebuilt
exactly.

## 3. OneMap geocoding

Search API: GET https://www.onemap.gov.sg/api/common/elastic/search
(?searchVal=...&returnGeom=Y&getAddrDetails=Y&pageNum=1). Read 4 October 2026
from the API docs (https://www.onemap.gov.sg/apidocs/, served as a script
bundle), the API Terms of Service
(https://www.onemap.gov.sg/legal/apitermsofservice.html) and the site Terms of
Use (https://www.onemap.gov.sg/legal/termsofuse.html).

**Token.** The docs list no header parameter for Search, unlike Reverse
Geocode, which lists "API token provided by the Authentication Service". In
the live test below, each Search call returned HTTP 200 WITH results, AND an
error field: "Authentication token missing. Please create an account and
generate or renew your API Token." So it works without a token today but asks
for one. A full run uses a registered account and token
(POST /api/auth/post/getToken). Jacob registers; the token never goes in the
repo.

**Rate limit.** No number is published on the Search page. The API terms
say limits are "found on the individual pages of each API". The docs warn
against "overloading OneMap API which might result in rate limited ban", and
list "429 - Quota exceeded" on other endpoints. The estimates below are
therefore assumptions, not a sourced limit.

**Bulk use for a public research site.** Quoted:
- API Terms of Service: "Use of the datasets is governed by the Singapore
  Open Data Licence." "You can use, access, call, command, query or request
  the API, whether commercially or non-commercially". "You shall not
  interfere with or disrupt the API or the servers".
- Site Terms of Use: "SLA grants to you a non-transferable, non-exclusive,
  royalty-free, revocable licence to access, view, download, print or
  otherwise use the SLA Data and the SLA Material for any usage, subject to
  the terms". Anyone building on the API "will need to complete the online
  registration process and ... accept the terms of the Developer Agreement."
  (The Developer Agreement itself was not read; it is shown at registration.)
- Reading: nothing quoted forbids a one-off, rate-limited batch of address
  look-ups for research. Results are datasets under the Open Data Licence, so
  derived distances can be published with attribution. Whether the
  coordinates themselves may be committed to a public repo is for Jacob to
  confirm against the Developer Agreement at registration.

**Unique addresses.** cargradient/00_addresses.py reads only block,
street_name and month from the five resale datasets (no price field
requested; the script asserts it). Result: cargradient/out/addresses.csv,
md5 1b9d1be0fba0ecff2b5d2e1458885885.
- Rows read: 988,123, all five files.
- Unique block + street pairs: 10,016, on 597 street names.
- Pairs with any sale in T1's window (2002-04 to 2015-12): 8,516.
- Pairs with any sale in T2's window (2016-01 to 2026-10): 9,770.

**Run time for 10,016 calls, one call each (assumed rates):**
- 1 per second: about 2.8 hours.
- 4 per second: about 42 minutes.
- Add retries for non-matches by hand-expanding abbreviations (NTH, ST,
  AVE, DR, C'WEALTH).

**Live test, 5 addresses only** (4 October 2026, no token; raw responses not
kept):

| Block, street (resale file) | Found | Top result | Block and road match |
|---|---|---|---|
| 525 BEDOK NTH ST 3 | 2 | 525 BEDOK NORTH STREET 3, 460525 | yes |
| 213 TAMPINES ST 23 | 1 | 213 TAMPINES STREET 23, 520213 | yes |
| 688F WOODLANDS DR 75 | 1 | 688F WOODLANDS DRIVE 75, 736688 | yes |
| 514 BEDOK NTH AVE 2 | 1 | 514 BEDOK NORTH AVENUE 2, 460514 | yes |
| 181A BOON LAY DR | 1 | 181A BOON LAY DRIVE, 641181 | yes |

5 of 5 matched on block and road, with the abbreviations expanded by
OneMap itself. Five easy cases prove little: blocks demolished under SERS
since 1990 may no longer geocode at all. Count those in the full run before
sealing.

Fallbacks, labels only: "HDB Existing Building" (d_16b157c52ed637edd6ba1232e026258d,
GeoJSON, BLK_NO, ST_COD, POSTAL_COD; keys on a street code, not a street name)
and "HDB Property Information" (d_17f5382f26140b1fdae0ba2ef6239d2f, 13,357
rows, blk_no and street, no coordinates). Both are current buildings only.

## 4. The CBD point the paper uses

Raffles Place MRT station (paper p. 11, note 19), with City Hall MRT station as
a robustness check (Table 5). Both are in the data.gov.sg MRT exit layer below,
with 10 exits for Raffles Place and 4 for City Hall (exits, not station
centres). How an exit set becomes one point (mean of
exits, or one named exit) is a choice to seal. The paper used MapInfo station
points (p. 15), which are not public.

## 5. MRT station locations

The paper needs them only for one robustness check: projects more than 1,000 m
from the nearest of "all 2015 proposed and existing stations" (p. 15).

"LTA MRT Station Exit (GEOJSON)", d_b39d3a0871985372d7e1637193335da5:
- 613 exit points under 190 station names; fields OBJECTID, STATION_NA,
  EXIT_CODE, INC_CRC, FMEL_UPD_D.
- A current snapshot (coverage start 2025-08-18) with no opening dates.
- Opening dates for the newer lines are on LTA's line pages, for example the
  TEL stages in raw/lta_tel_project_page.html. They are not in one table.

## 6. The February 2018 zero-growth change

- Start date and rate: LTA, 13 Aug 2020, saved as
  raw/lta_20200813_vehicle_growth_rate.html: "0% per annum for Categories A, B
  and D since February 2018".
- Announcement date (23 October 2017): news reports only. LTA's newsroom on
  lta.gov.sg lists releases from 2020 onward, so the October 2017 release is
  not there. www.mot.gov.sg and www.gov.sg refuse the session (CONNECT 403,
  5 October 2026); the search stopped for those hosts. NEEDS-PRIMARY. T3
  drops 2017Q4 to 2018Q1, which covers any announcement day in that quarter.
- The rate before February 2018 (0.25%, Jacob's figure): not confirmed by a
  primary source. LTA's 2020 release says only that Category C "was
  maintained at 0.25% per annum". NEEDS-PRIMARY.

## Exposure, disclosed

- No HDB resale price was requested, printed or saved. The address pull asked
  for block, street_name and month only, and asserts that no other field came
  back.
- Reading the paper showed its COE premium summary for 2002Q2-2015Q4 and its
  Figure 3 (PAPER_NOTES.md, Exposure). Those are COE values, not HDB prices.
  No COE value was requested from SingStat or data.gov.sg.
- This repo already holds resale files (raw/, registration-date basis, 2012
  onward) and the affordability piece's RESULTS.md, which is built on them.
  Neither was opened for this piece. The checker decides whether that earlier
  piece's town-level findings bear on these tests.
