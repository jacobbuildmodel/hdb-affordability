# Everything I still need from you, in one list

Written 12 September 2026. Work top down. Item 1 is the only one that blocks the
headline; everything below it firms up claims I can otherwise only hedge.

For each file, tell me the **"Last updated"** date if the page shows one. Download
date is today unless you say otherwise.

---

## 1. The EHG amount-by-income-band table. THE BLOCKER.

Without this the grant-adjusted lead measure cannot run and tests T3 and T4 stay
unevaluated. The direct file URLs I gave you are dead, so do not chase them. Go via
the page instead, which is where HDB keeps the live link.

**Step by step:**

1. Open https://www.hdb.gov.sg/buying-a-flat/flat-grant-and-loan-eligibility/couples-and-families/enhanced-cpf-housing-grant
2. Scroll to the row labelled **Amount** in the big criteria table.
3. In that cell there is a link reading **"average monthly household income and
   corresponding EHG amount"** with **(PDF, 198KB)** after it. Click it.
4. Save whatever opens. If it opens in a viewer, Ctrl+S. If it opens as a page,
   Ctrl+P then "Save as PDF".
5. Send me that file.

**While you are on that page**, there is a second thing the first print missed.
Under the heading **"Examples on how the EHG is calculated"** there are two
collapsed accordions, "First-timer families" and "First-timer and second-timer
families". **Click both to expand them**, then Ctrl+P, Save as PDF, and send that
too. Collapsed accordions do not print, which is why they came through blank.

**What I need out of it:** every income band and its grant amount. That is all.

---

## 2. Provenance, nearly closed

I have recorded the dates you gave. Three small gaps:

**2a.** The one dataset you did not give a date for:
https://data.gov.sg/datasets/d_ea9ed51da2787afaf8e51f827c304208/view
(Resale flat prices, Jan 2015 to Dec 2016.) Just the "Last updated" date.

**2b.** The Resale Price Index page
https://data.gov.sg/datasets/d_14f63e595975691e7c24a27ae4c07c79/view
You gave 28 Aug 2024, but the file you sent contains data through 2026-Q2. A 2024
vintage cannot contain 2026 data. Please re-check what that page says, and whether
the date is against the dataset or against the metadata. I have recorded the
contradiction in `raw/RETRIEVED.txt` rather than picking one.

**2c.** One command, on the machine you downloaded to, in the folder with the
downloaded files:

    certutil -hashfile ResaleflatpricesbasedonregistrationdatefromJan2017onwards.csv MD5

Send me the hash. If it reads `a9e696ef2d4d10e9765eada65fbd50b2`, the transfer was
clean and the provenance chain closes. It takes ten seconds and it is the single
thing a verifier is most likely to poke at.

---

## 3. The August 2024 loan-to-value change

I sourced the other two changes myself from primary documents, with quotes: 90 to
85 per cent on 16 December 2021 from MOF, and 85 to 80 per cent on 30 September
2022 from MAS. Only the last one is missing.

**Step by step:**

1. Open https://www.hdb.gov.sg/about-us/news-and-publications/press-releases
2. Filter or scroll to **August 2024**.
3. Find the release titled **"Measures to Cool the HDB Resale Market and Provide
   More Support for First-Time Home Buyers"**, dated 19 or 20 August 2024.
4. Ctrl+P, Save as PDF, send it.

If HDB's listing will not go back that far, the same release is on MND:
https://www.mnd.gov.sg/newsroom/press-releases

**What I need out of it:** the LTV going from 80 to 75 per cent, its effective
date, and the EHG maximum going from 80,000 to 120,000. That one document settles
two rows in `ltv_schedule.csv` and one in `grant_schedule.csv`.

---

## 4. CPF Ordinary Account rate history -- CLOSED, 17 September 2026

`cpf2.pdf` (Q1 2016) and `cpf3_q3_2026.pdf` (Q3 2026), both already supplied and in
`raw/`, are the two anchor points asked for below. `06_tests.py` was revised on 16
September 2026 to cite them; T2 is now PASS. Nothing further needed here.

Left below for the record.

This is what turns test T2 from PARTIAL to PASS. HDB's own page proves the rate is
pegged at 0.1 points above the OA rate and is 2.60 per cent now. It does not show
history, so "2.6 per cent across the whole window" is currently unsourced.

**Step by step:**

1. Open https://www.cpf.gov.sg/member/growing-your-savings/earning-higher-returns/earning-attractive-interest
2. Ctrl+P, Save as PDF, send it.
3. Then open https://www.cpf.gov.sg/member/infohub/news/news-releases and search
   for "CPF interest rates". Send me **any two** of the quarterly announcements
   from different years, ideally one from around 2013 to 2015 and one recent.

Two announcements years apart, both showing the OA at 2.5 per cent, plus the page
stating the legislated floor, is enough to support the claim honestly. I do not
need all fifty quarters.

---

## 5. The GitHub repository

The article's front matter links to it, so it has to exist and be public before the
piece ships. You said instructions were optional; here they are anyway.

1. Go to https://github.com/new
2. Repository name: **`hdb-affordability`** (exactly this, it is in the front
   matter).
3. Owner: your `jacobbuildmodel` account. Visibility: **Public**.
4. Do **not** tick "Add a README", "Add .gitignore" or "Choose a license". I am
   shipping all three and an initialised repo creates merge conflicts.
5. Click "Create repository". Leave the page open; it shows the push commands.
6. When I send you the finished zip, unpack it so that `README.md` sits at the
   **top level** of the repo, not inside a subfolder. A previous piece was pushed
   one directory too deep and its README never rendered.
7. From inside that folder:

        git init
        git add .
        git commit -m "HDB resale affordability: analysis and article"
        git branch -M main
        git remote add origin https://github.com/jacobbuildmodel/hdb-affordability.git
        git push -u origin main

8. Then open the repo page and check: does the README render, and is `raw/` there
   with the CSVs in it.

The `.gitattributes` I ship contains exactly `* -text`. Keep it. Without it Git
rewrites line endings on a Windows checkout and every published checksum fails for
reasons unrelated to the data.

---

## 6. Optional, and genuinely optional

**6a. MOM Report on Wage Practices 2025.**
https://stats.mom.gov.sg/iMAS_PdfLibrary/mrsd-report-on-wage-practices-2025.pdf

This converts T7 from a one-sided bound into a range. HDB excludes bonuses from
assessed income and SingStat includes one-twelfth of the annual bonus, so the
crossing year I can currently publish is "2022.1 or later". The report gives
variable wages as a share of total wages and the annual variable component in
months of basic pay, which lets me put a floor under it as well.

I can read that PDF from here, so I have previewed it, but a figure that reaches
the article has to come out of a file in `raw/` with a checksum. If you send it, I
use it. If not, the article says "2022 or later" and stops, which is honest and
slightly weaker.

**6b. Pre-2019 grant schedule**, the Additional and Special CPF Housing Grants that
the EHG replaced, and the Proximity Housing Grant history. Only needed if you want
the grant-adjusted measure to run from 2013 rather than from 2019. If it is hard to
find, say so and the grant series simply starts in 2019 with the text explaining
why.

---

## What I am doing meanwhile

Figures, sources file, number manifest, checksums, the handover brief, and the
article spine. None of it waits on you. When item 1 lands I run two more scripts,
T3 and T4 resolve, and the piece is complete.
