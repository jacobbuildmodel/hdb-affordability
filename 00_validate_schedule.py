"""
00_validate_schedule.py

Checks grant_schedule.csv against itself before anything reads it.

This exists because of a real error. Two rows dated 2023-02-14 were marked
VERIFIED-PRIMARY and carried income_band_high = 16000. The source they cited, MOF
Budget 2023 Annex E-1, says "$14,000". The 16,000 ceiling only took effect on
24 August 2026, after the window. Uncorrected, every household earning 14,001 to
16,000 would have been awarded an 80,000 grant it was not eligible for. That band
sits between the EHG cutoff and the 80th percentile, so it would have inflated the
upper group's grants and understated the T4 divergence, which is the headline
comparison.

The contradiction was visible in the file, because other rows already had the
ceiling path right. Nothing was checking. Now something is.

Four invariants, all fatal:

  V1  A row claiming primary verification must carry the quoted sentence.
      VERIFIED-PRIMARY and LEVEL-VERIFIED-PRIMARY both require a non-empty
      source_quote. You cannot mark a row as evidenced without pasting the
      evidence. This is the control that would have caught the original error at
      the moment of entry.

  V2  A CPF_HOUSING_GRANT row's income_band_high must equal the
      PURCHASE_AND_CPFHG_CEILING in force on that row's start date. The grant
      ceiling is not a separate parameter; it is the purchase ceiling. Two places
      in the file held the same fact and only one was right.

  V3  Date intervals within a (grant, scope) pair must not overlap and must not
      leave a gap between the first and last row of that pair.

  V4  Every dated row needs a start date, a numeric amount, and dates that parse.

Reads:  grant_schedule.csv
Writes: nothing. Exits 0 or 3.

Usage:  python 00_validate_schedule.py
        python 00_validate_schedule.py --selftest

--selftest reintroduces the exact original error into a temporary copy and fails
unless V2 catches it. A check nobody has seen fail is not a check.
"""

import csv
import os
import shutil
import subprocess
import sys
import tempfile
from datetime import date

HERE = os.path.dirname(os.path.abspath(__file__))
PATH = os.path.join(HERE, "grant_schedule.csv")

NEEDS_QUOTE = {"VERIFIED-PRIMARY", "LEVEL-VERIFIED-PRIMARY"}
VALID_STATUS = NEEDS_QUOTE | {"NEEDS-PRIMARY", "NOT-OBTAINED"}
FAR_FUTURE = date(9999, 12, 31)


def parse_date(txt, default=None):
    txt = (txt or "").strip()
    if not txt:
        return default
    y, m, d = txt.split("-")
    return date(int(y), int(m), int(d))


def selftest():
    """Reintroduce the original error and require V2 to catch it."""
    work = tempfile.mkdtemp(prefix="schedcheck_")
    try:
        script = os.path.join(work, "00_validate_schedule.py")
        target = os.path.join(work, "grant_schedule.csv")
        shutil.copy(os.path.abspath(__file__), script)

        with open(PATH, encoding="utf-8") as fh:
            text = fh.read()
        broken = text.replace(
            "2023-02-14,2026-08-23,CPF_HOUSING_GRANT,resale 2-4 room first-timer "
            "family,0,14000,80000",
            "2023-02-14,2026-08-23,CPF_HOUSING_GRANT,resale 2-4 room first-timer "
            "family,0,16000,80000")
        if broken == text:
            print("SELFTEST INCONCLUSIVE: the row the test mutates is no longer in "
                  "grant_schedule.csv in the expected form. Update the selftest.",
                  file=sys.stderr)
            return 3
        with open(target, "w", newline="\n", encoding="utf-8") as fh:
            fh.write(broken)

        proc = subprocess.run([sys.executable, script], cwd=work,
                              capture_output=True, text=True)
        combined = proc.stdout + proc.stderr
        if proc.returncode == 3 and "income_band_high 16000" in combined:
            print("selftest passed: V2 rejects the 16000 ceiling on a 2023 row")
            return 0
        print("SELFTEST FAILED: the validator did not reject the known-bad "
              "schedule. exit=%d\n%s" % (proc.returncode, combined), file=sys.stderr)
        return 3
    finally:
        shutil.rmtree(work, ignore_errors=True)


def main():
    if "--selftest" in sys.argv[1:]:
        sys.exit(selftest())

    with open(PATH, newline="", encoding="utf-8") as fh:
        rows = list(csv.DictReader(fh))

    problems = []
    ceilings = []

    for i, r in enumerate(rows, start=2):
        status = (r.get("status") or "").strip()
        grant = (r.get("grant") or "").strip()
        quote = (r.get("source_quote") or "").strip()

        if status not in VALID_STATUS:
            problems.append("line %d: status '%s' is not one of %s"
                            % (i, status, sorted(VALID_STATUS)))

        # V1
        if status in NEEDS_QUOTE and not quote:
            problems.append("line %d: %s is marked %s but source_quote is empty. "
                            "A row is not verified until the sentence is pasted in."
                            % (i, grant, status))
        if status == "NEEDS-PRIMARY" and quote:
            problems.append("line %d: %s carries a quote but is only NEEDS-PRIMARY. "
                            "Promote it or remove the quote." % (i, grant))

        if status == "NOT-OBTAINED":
            continue

        # V4
        start = parse_date(r.get("in_force_from"))
        if start is None:
            problems.append("line %d: %s has no in_force_from" % (i, grant))
            continue
        end = parse_date(r.get("in_force_to"), FAR_FUTURE)
        if end < start:
            problems.append("line %d: %s ends %s before it starts %s"
                            % (i, grant, end, start))
        amt = (r.get("amount") or "").strip()
        if not amt or not amt.replace(".", "", 1).isdigit():
            problems.append("line %d: %s has a non-numeric amount '%s'"
                            % (i, grant, amt))

        if grant == "PURCHASE_AND_CPFHG_CEILING":
            ceilings.append((start, end, float(amt), i))

    ceilings.sort()

    def ceiling_on(day):
        for s, e, v, _ln in ceilings:
            if s <= day <= e:
                return v
        return None

    # V2
    for i, r in enumerate(rows, start=2):
        if (r.get("grant") or "").strip() != "CPF_HOUSING_GRANT":
            continue
        if (r.get("status") or "").strip() == "NOT-OBTAINED":
            continue
        start = parse_date(r.get("in_force_from"))
        if start is None:
            continue
        band = (r.get("income_band_high") or "").strip()
        if not band:
            problems.append("line %d: CPF_HOUSING_GRANT has no income_band_high" % i)
            continue
        want = ceiling_on(start)
        if want is None:
            problems.append("line %d: no PURCHASE_AND_CPFHG_CEILING covers %s"
                            % (i, start))
        elif abs(float(band) - want) > 1e-9:
            problems.append(
                "line %d: CPF_HOUSING_GRANT from %s has income_band_high %s but the "
                "purchase ceiling in force that day is %.0f. The grant ceiling IS "
                "the purchase ceiling. This is the check that catches the 2023 "
                "error." % (i, start, band, want))

    # V3
    pairs = {}
    for i, r in enumerate(rows, start=2):
        if (r.get("status") or "").strip() == "NOT-OBTAINED":
            continue
        start = parse_date(r.get("in_force_from"))
        if start is None:
            continue
        key = ((r.get("grant") or "").strip(), (r.get("scope") or "").strip())
        pairs.setdefault(key, []).append(
            (start, parse_date(r.get("in_force_to"), FAR_FUTURE), i))

    for key, spans in sorted(pairs.items()):
        spans.sort()
        for (s1, e1, l1), (s2, _e2, l2) in zip(spans, spans[1:]):
            if s2 <= e1:
                problems.append("lines %d and %d: %s %s overlap, %s to %s then %s"
                                % (l1, l2, key[0], key[1], s1, e1, s2))
            elif (s2 - e1).days > 1:
                problems.append("lines %d and %d: %s %s leave a gap between %s and %s"
                                % (l1, l2, key[0], key[1], e1, s2))

    counts = {}
    for r in rows:
        counts[(r.get("status") or "").strip()] = \
            counts.get((r.get("status") or "").strip(), 0) + 1

    print("grant_schedule.csv: %d rows" % len(rows))
    for k in sorted(counts):
        print("  %-24s %d" % (k, counts[k]))
    print("")

    if problems:
        print("SCHEDULE VALIDATION FAILED, %d problem(s):" % len(problems),
              file=sys.stderr)
        for p in problems:
            print("  " + p, file=sys.stderr)
        sys.exit(3)

    print("all four invariants hold")
    print("")
    print("Reminder: rows still NOT-OBTAINED are not modelled anywhere. The "
          "grant-adjusted measure runs only over years whose schedule is "
          "documented, and the article says so.")


if __name__ == "__main__":
    main()
