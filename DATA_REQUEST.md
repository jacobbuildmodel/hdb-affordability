# Data request: one message, everything at once

data.gov.sg, singstat.gov.sg and hdb.gov.sg all refuse automated requests from this
sandbox. The egress proxy answers 403 to CONNECT before any request is sent, so an
API key does not help. Tested again 11 September 2026. Everything below has to come
from your machine.

Please do not send these one at a time. Send what you can in one go and tell me
what failed.

---

## A. The transaction file, and the size problem

**A1. Resale flat prices, January 2017 onwards**
https://data.gov.sg/datasets/d_8b84c4ee58e3cfc0ece0d773c8ca6abc/view
Dataset ID `d_8b84c4ee58e3cfc0ece0d773c8ca6abc`. Roughly 235,000 rows, about 22 MB.

**This may exceed the chat upload limit. Flagging it now rather than discovering it
in three days.** Three routes, in order of preference.

**Route 1, preferred: gzip it.** A 22 MB CSV of this shape compresses to roughly
4 MB and loses nothing. On Windows, with 7-Zip installed, right click the file and
choose 7-Zip then "Add to archive", format gzip. Or in PowerShell if you have
Python:

    python -c "import gzip,shutil; shutil.copyfileobj(open('ResaleFlatPrices.csv','rb'), gzip.open('ResaleFlatPrices.csv.gz','wb'))"

Then send me `ResaleFlatPrices.csv.gz` **and the MD5 of the uncompressed original**:

    certutil -hashfile ResaleFlatPrices.csv MD5

I record both MD5s in `raw/RETRIEVED.txt`, so the verifier can decompress and check
against the number data.gov.sg served you.

**Route 2, if gzip still will not upload: filter it.** Run this on the downloaded
file. It keeps every column and every four-room row, which is the pre-registered
subgroup, and prints both checksums.

    # save as reduce.py, run: python reduce.py ResaleFlatPrices.csv
    import csv, hashlib, sys
    src = sys.argv[1]
    dst = "resale_4room_2017on.csv"
    def md5(p):
        h = hashlib.md5()
        with open(p, "rb") as f:
            for c in iter(lambda: f.read(1 << 20), b""):
                h.update(c)
        return h.hexdigest()
    kept = total = 0
    with open(src, newline="", encoding="utf-8") as fi, \
         open(dst, "w", newline="", encoding="utf-8") as fo:
        r = csv.DictReader(fi)
        w = csv.DictWriter(fo, fieldnames=r.fieldnames)
        w.writeheader()
        for row in r:
            total += 1
            if row["flat_type"].strip().upper() == "4 ROOM":
                w.writerow(row); kept += 1
    print("source md5   ", md5(src))
    print("reduced md5  ", md5(dst))
    print("rows in      ", total)
    print("rows kept    ", kept)

Send `resale_4room_2017on.csv` plus that console output verbatim.

**What route 2 costs.** Test T5 compares the constant-quality index against the raw
median, and that still works within four-room. But I lose the ability to show how
the flat-type mix itself shifted, which is a supporting exhibit rather than a
headline. If you use route 2, the piece says so.

**Route 3, last resort:** put the file in a public GitHub repo yourself and give me
the raw URL. github.com is reachable from here. This is the cleanest of the three
for reproducibility and the most work for you.

**A1b. The two earlier transaction files. ADDED 11 September 2026 after review.**

The window now starts in 2013 rather than 2017, because a 2017 base sits near a
cyclical low and flatters the finding. Transactions are on a consistent
registration-date basis from March 2012, so these two files extend the window
without a basis break:

- Resale flat prices by registration date, March 2012 to December 2014
  https://data.gov.sg/datasets/d_2d5ff9ea31397b66239f245f57751537/view
- Resale flat prices by registration date, January 2015 to December 2016
  https://data.gov.sg/datasets/d_ea9ed51da2787afaf8e51f827c304208/view

Both are far smaller than the 2017 file and should upload directly. Do NOT send the
2000 to February 2012 file or the 1990 to 1999 file: those are on an approval-date
basis, which is a different construct, and mixing them would be a silent break in
the series.

One thing to expect: these two files have no `remaining_lease` column. That column
starts with the 2017 file. I reconstruct it from `lease_commence_date` and assert
the reconstruction reproduces the published column over the overlapping period.

**A2. HDB Resale Price Index, quarterly, 1Q2009 = 100**
https://data.gov.sg/datasets/d_14f63e595975691e7c24a27ae4c07c79/view
Small. Not an input to the finding. I use it to check my constant-quality index
against the official one; if my hedonic index and HDB's index disagree badly, that
is something the reader needs to know before anything else in the piece.

## B. Income

All three are a few kilobytes each. All from data.gov.sg.

**B1. Monthly household income from work EXCLUDING employer CPF, resident employed
households, at selected percentiles, annual**
https://data.gov.sg/datasets/d_ff1988785f3e36cfc4757cf604ae0acd/view
The main income input. The 20th, 50th and 80th percentiles are the three
pre-registered buyers. Excluding employer CPF because that is the basis HDB
assesses income on.

**B2. The same series INCLUDING employer CPF**
https://data.gov.sg/datasets/d_dff6b97b7c233917ac8294bd04051486/view
Sensitivity check only. The two differ by roughly the employer contribution rate,
which is not small, and a reader will ask which one I used.

**B3. Average and median household employment income, resident AND resident
employed households, annual**
https://data.gov.sg/datasets/d_ab4f7ecfc45e0a0eafe4ae4397e77059/view
Lets me state what share of households have no employment income at all, which
bounds how far the "resident employed" denominator can be pushed.

When you open each dataset page, note the **"Data Last Updated"** date shown on it
and paste that to me. SingStat revises these when the labour force survey is
reweighted and I need to record which vintage this is.

## C. Financing and grants, which the transaction file does not contain

These are the parts I cannot get, because hdb.gov.sg renders its tables in
JavaScript and this sandbox sees only the page shell.

**C1. The grant schedule, current.** Open each page in your browser and save as PDF
(Ctrl+P, then "Save as PDF"). I need the actual tables, not a summary.
- Enhanced CPF Housing Grant for families:
  https://www.hdb.gov.sg/buying-a-flat/flat-grant-and-loan-eligibility/couples-and-families/enhanced-cpf-housing-grant
- CPF Housing Grant for resale flats, families
- Proximity Housing Grant
Whatever the current income bands and amounts are, verbatim.

**C2. The grant schedule, historical.** This is the harder half and the piece
depends on it. I need what a first-timer family would have received in each year
from 2017 to 2025, which means the schedule before and after each change. Known
change points, to be confirmed from primary documents:
- September 2019, Enhanced CPF Housing Grant replaces the AHG and SHG
- 14 February 2023, Budget 2023, CPF Housing Grant for 2- to 4-room resale rises
  from 50,000 to 80,000. I already have this annex and it reads fine from here:
  https://isomer-user-content.by.gov.sg/153/5389b2b9-e526-4696-b138-9fcd49096960/annexe1.pdf
- August 2024, Enhanced CPF Housing Grant increase, announced with the loan-to-value
  cut. I could not open the HDB press release; the URL I tried 404s. If you can find
  the release on hdb.gov.sg, send it as PDF.

If any year's schedule cannot be sourced from a primary document, say so and I drop
the grant-adjusted measure rather than estimating it. That is condition 10 in
THESIS.md and I would rather trigger it honestly than guess.

**C2b. The income CEILINGS on the grants, and their history. ADDED after review,
and this is now the single most important item in section C.**

Test T7 turns entirely on one number: the Enhanced CPF Housing Grant household
income ceiling, which I have at 9,000 dollars a month, introduced at that level in
September 2019 and still 9,000 today. If that is right, the threshold has not moved
in seven years while incomes rose and while the maximum grant went from 80,000 to
120,000, and the median household may have crossed it inside the window. That would
be the headline.

It rests on two pages that both render their tables in JavaScript, so I could read
the prose and not the tables:
- CPF Board, "A guide to the Enhanced CPF Housing Grant and Proximity Grant",
  published 9 May 2025:
  https://www.cpf.gov.sg/member/infohub/educational-resources/a-guide-to-enhanced-cpf-housing-and-proximity-grant
- HDB MyNiceHome, "CPF Housing Grants for HDB Flat Buyers":
  https://www.mynicehome.gov.sg/get-started/hdb-grants-guide/

Save both as PDF. And if you can find anything showing the Enhanced CPF Housing
Grant ceiling at any point between 2019 and now, a press release, an annex, an
archived page, send it. **One documented year at a different ceiling withdraws the
seven-year-freeze claim**, so I would rather you find it than the verifier does.

For the record, the figures I am currently carrying, all to be confirmed against
your PDFs, and if a PDF disagrees the PDF wins:
- Enhanced CPF Housing Grant, families: up to 120,000, income ceiling 9,000
- CPF Housing Grant for resale, families: up to 80,000 for 2- to 4-room, up to
  50,000 for 5-room and larger, income ceiling 16,000, raised from 14,000 on
  24 August 2026
- Proximity Housing Grant: 30,000 living with, 20,000 within 4 km, no income test
- Maximum combined: 230,000

**C3. HDB concessionary loan rate.** Save this page as PDF:
https://www.hdb.gov.sg/managing-my-home/finances/loan-matters/interest-rate
I have it from secondary sources at 2.6 per cent, pegged at 0.1 points above the
CPF Ordinary Account rate, unchanged since 1999. That fact is load-bearing for the
whole argument and it needs HDB's own page behind it.

**C4. Loan-to-value limit history for HDB loans.** The limit changed at least twice
inside the window and it enters the repayment calculation directly. I believe the
path is 90 per cent, then 85 in December 2021, then 80 in September 2022, then 75
in August 2024, but I have not verified the middle two and will not write them
until I have. The HDB or MAS release for each change, as PDF.

## D. The bonus wedge. ADDED 12 September 2026, and it changes T7

Checking HDB's income basis from primary sources turned up something that moves the
expected answer, so this is now a real item rather than a nicety.

HDB assesses "total gross income earned including employee's CPF deductions and
**excluding employer's CPF contributions and bonuses**" (ask.gov.sg, HDB's own
channel). SingStat's household employment income "includes one-twelfth of the
annual bonus" (SingStat's Key Household Income Trends glossary). So even after the
employer-CPF question is settled in favour of the series I chose, SingStat still
sits **above** HDB's basis by roughly one month's bonus, which is on the order of
8 per cent, which at recent nominal growth rates is about two years of drift.

That is why T7 now reports a bound rather than a year. Details in
THESIS_ADDENDUM.md entry 2.

**D1. A primary figure for the average annual bonus as a share of wages.** MOM's
Report on Wage Practices, or the Occupational Wages tables, or an MOM summary
table. Whatever MOM publishes for the average variable bonus in months of basic
pay, for as many years of the window as it covers. If you can get a series rather
than one year, better.

With it I publish a lower bound alongside the upper bound and the article gives a
range. Without it I publish only the upper bound and say the true crossing is that
year or later. Either is fine. **Do not go hunting for a non-MOM estimate**, and I
will not apply a divisor of my own invention. This is the one place where an
invented number would quietly change the headline, so it is the one place I want a
document or nothing.

---

## What I do the moment A1, B1 and C3 land

Those three alone unlock the pipeline. The rest can follow.

1. `raw/RETRIEVED.txt` with title, publisher, dataset ID, URL, retrieval date,
   byte count and MD5 for every file.
2. `01_clean.py`, with the registration-date caveat encoded as an assertion.
3. `02_hedonic.py` and `03_basket.py`, the two independent composition corrections.
4. `04_affordability.py`, the three measures for the three buyers.
5. Then the tests in THESIS.md section 6, reported however they come out.

## What I will not do

Fill a gap with a plausible number. If the August 2024 grant change cannot be
sourced, the article says the grant path is unknown after August 2024 and stops the
grant-adjusted series there. "Not obtained" goes in the piece.
