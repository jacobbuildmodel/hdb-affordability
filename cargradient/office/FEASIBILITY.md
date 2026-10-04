# FEASIBILITY -- labels and coverage only

Checked 4 October 2026, about 10:10 to 10:40 UTC, from the research session.
No price value was printed, plotted, summarised or saved to the repo. Coverage
came from dataset metadata and from queries that asked for the `month` field
alone (first, last, row total). The COE table was read by its metadata
(series labels, first and last period), not its values.

Licence for everything on data.gov.sg: Singapore Open Data Licence version
1.0 (https://data.gov.sg/open-data-licence). SingStat's terms of use say
datasets on its services are under the same licence.

## Hosts

| Host | Reachable | Used for |
|---|---|---|
| data.gov.sg, api-production.data.gov.sg, api-open.data.gov.sg | yes | HDB resale, COE, MRT exits, HDB buildings |
| tablebuilder.singstat.gov.sg, www.singstat.gov.sg | yes | COE from 2002 |
| liberalarts.tulane.edu | NO, 403 | the paper (see PAPER_NOTES.md); stopped |
| www.onemap.gov.sg | NO, 403 | geocoding; stopped |
| datamall.lta.gov.sg, www.lta.gov.sg | NO, 403 | LTA data and the 2018 growth-rate notice; stopped |
| www.hdb.gov.sg | NO, 403 | not needed for these series |
| tfl.gov.uk | NO, 403 | world-view source; stopped |

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
label across the whole series. Which category and which averaging the paper
used is unknown until the paper is read.

## 3. OneMap geocoding

www.onemap.gov.sg is refused (403). Terms of use, rate limits and whether
bulk geocoding is allowed: NOT CHECKED, stopped for that host.

Reachable alternatives, labels only, for Jacob to weigh:
- "HDB Existing Building", d_16b157c52ed637edd6ba1232e026258d, GeoJSON,
  57 MB, fields OBJECTID, BLK_NO, ST_COD, ENTITYID, POSTAL_COD, INC_CRC,
  FMEL_UPD_D, SHAPE.AREA, SHAPE.LEN. It keys on a street CODE, not the street
  name the resale files carry, so a join needs a code-to-name table not found
  yet. Current buildings only (coverage start 2025-11-04).
- "HDB Property Information", d_17f5382f26140b1fdae0ba2ef6239d2f, CSV,
  13,357 rows, blk_no and street (names) and year_completed among 24 columns,
  no coordinates.

## 4. The CBD point the paper uses

Unknown: it is in the paper, which is blocked. Not substituted.

## 5. MRT station locations (only if the paper's controls need them)

"LTA MRT Station Exit (GEOJSON)", d_b39d3a0871985372d7e1637193335da5:
613 exit points, 190 station names, fields OBJECTID, STATION_NA, EXIT_CODE,
INC_CRC, FMEL_UPD_D. A current snapshot (coverage start 2025-08-18) with no
opening dates, so a station that opened in 2013 or 2020 cannot be dated from
it. LTA DataMall is refused (403).

## 6. The February 2018 zero-growth change

The date and the rate need a primary source (LTA). www.lta.gov.sg is refused
(403); not sourced yet.

## Exposure, disclosed

- No resale price, COE premium or derived figure was seen in this session.
- This repo already holds resale files (raw/, registration-date basis,
  2012 onward) and the affordability piece's RESULTS.md, built on them. They
  were not opened for this piece. The checker decides whether that earlier
  piece's town-level findings bear on these tests.
