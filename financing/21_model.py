"""
21_model.py

The amortisation and refinancing model. Imported by 22_compute.py; run directly
it executes a selftest.

Everything here follows THESIS.md, sealed 17 September 2026, and nothing here
decides anything the sealed file left open.

  Principal   S$400,000, identical on both routes (section 4).
  Tenure      25 years = 300 months base, 30 years sensitivity.
  HDB leg     2.6 per cent, constant for the life of the loan (section 2).
  Bank leg    compounded 3-month SORA plus a constant spread.
  R2          reprices every 36 months to the then-prevailing benchmark plus
              the same spread. No shopping around (section 5).
  R3          the best the bank route could have delivered under a simple,
              describable refinancing rule: refinance whenever the benchmark
              has fallen by at least a trigger of X percentage points AND the
              saving over the period the new package binds exceeds the
              switching cost. R3 reports the cheapest outcome over a grid of
              triggers, chosen with hindsight. Upper bound, not a real
              borrower (section 5).

              WHY IT IS DEFINED THIS WAY, and a departure from the sealed
              wording, recorded as AMENDMENT 1 in THESIS.md and written AFTER
              results were seen. THESIS.md says "move every time the saving
              over the remaining tenure exceeds the switching cost". Taken
              literally with a monthly re-evaluation, that assumes every rate
              cut persists to the end of the loan, so a 10 basis point tick
              clears a S$3,000 hurdle, the fee is paid again on the next
              twitch, and switching also displaces the repricing clock. Run
              that way on the real series a 2010 cohort refinances 17 times at
              S$3,000, pays S$51,000 in fees, and R3 costs MORE than R2 -- a
              direct contradiction of the sealed file's own description of R3
              as an upper bound on what the bank route could have delivered.
              The trigger grid below contains "never refinance opportunistically",
              which reproduces R2 exactly, so R3 <= R2 holds by construction
              and the upper bound is real rather than asserted.

  Realised    cumulative to the last data month, never to the end of tenure
              (section 3). That is the headline basis.

A note on what "total cost" means, because the two routes are not symmetric.
For the HDB leg and for R2 it is cumulative interest. For R3 it is cumulative
interest PLUS every switching cost actually paid, since a rule that refinances
for free is not the rule the sealed file describes. The break-even spread is
the spread at which the bank route's total cost equals the HDB route's
cumulative interest.

Usage:  python3 21_model.py --selftest
"""

import sys

PRINCIPAL = 400000.0
TENURE_MONTHS = 300
RESET_MONTHS = 36
SPREAD_GRID = [0.25, 0.50, 0.75, 1.00, 1.25, 1.50]
SWITCH_COSTS = [0.0, 3000.0, 6000.0]
# refinance triggers in percentage points; None = never refinance
# opportunistically, which reproduces R2 exactly
TRIGGERS = [None] + [x / 100.0 for x in range(0, 205, 10)]


def amortise(principal, annual_rate, months):
    """Level monthly payment. Lifted unchanged from 05_affordability.py."""
    if principal <= 0:
        return 0.0
    r = annual_rate / 12.0
    if r == 0:
        return principal / months
    return principal * r / (1.0 - (1.0 + r) ** (-months))


def run_fixed(principal, annual_rate_pct, tenure, horizon):
    """Constant-rate loan. Returns the cumulative interest path, month by month."""
    r = annual_rate_pct / 100.0
    pay = amortise(principal, r, tenure)
    bal, cum, path = principal, 0.0, []
    for _ in range(min(horizon, tenure)):
        interest = bal * r / 12.0
        bal = max(0.0, bal + interest - pay)
        cum += interest
        path.append(cum)
    return path


def run_floating(principal, spread_pct, rates, start, tenure, horizon,
                 switch_cost=None, trigger=None, reset_months=None):
    """
    Benchmark-plus-spread loan.

    rates      list of monthly benchmark values, per cent
    start      index into rates of the loan's first month
    switch_cost  None  -> R2, reprice only on the contractual schedule
                 float -> R3, also reprice opportunistically when it pays
    reset_months  the contractual repricing interval. None uses the module
                 default RESET_MONTHS (36, the base case). Overridden only by
                 the reset-interval sensitivity in 22b_reset_sensitivity.py.

    Returns (cumulative cost path, number of opportunistic switches). The path
    includes switching costs at the month they are paid, so it is total cost,
    not interest alone.
    """
    n = min(horizon, tenure, len(rates) - start)
    if n <= 0:
        return [], 0

    reset = RESET_MONTHS if reset_months is None else reset_months
    rate = (rates[start] + spread_pct) / 100.0
    pay = amortise(principal, rate, tenure)
    bal, cum, path, switches = principal, 0.0, [], 0
    next_reset = reset

    for k in range(n):
        remaining = tenure - k
        if k > 0 and k == next_reset:
            # contractual reset: both rules do this
            rate = (rates[start + k] + spread_pct) / 100.0
            pay = amortise(bal, rate, remaining)
            next_reset = k + reset
        elif k > 0 and switch_cost is not None and trigger is not None:
            market = (rates[start + k] + spread_pct) / 100.0
            if (rate - market) * 100.0 >= trigger:
                # The new package binds for one repricing cycle, and the saving
                # is measured against the benchmark path that actually followed
                # rather than against an assumption that today's rate persists.
                # R3 is declared an upper bound, "not a real person"
                # (THESIS.md section 5), so foresight is what it is for; the
                # naive version both assumed persistence AND lacked foresight,
                # which is how it managed to be worse than R2.
                binds = min(reset, remaining, len(rates) - (start + k))
                saving = 0.0
                for j in range(binds):
                    fut = (rates[start + k + j] + spread_pct) / 100.0
                    saving += (rate - fut) * bal / 12.0
                if saving > switch_cost:
                    rate = market
                    pay = amortise(bal, rate, remaining)
                    cum += switch_cost
                    switches += 1
                    next_reset = k + reset
        interest = bal * rate / 12.0
        bal = max(0.0, bal + interest - pay)
        cum += interest
        path.append(cum)

    return path, switches


def run_r3(principal, spread_pct, rates, start, tenure, horizon, switch_cost,
          reset_months=None):
    """
    R3: the cheapest outcome over the trigger grid, chosen with hindsight.

    TRIGGERS includes None, which never refinances opportunistically and so
    reproduces R2 exactly. R3 therefore can never cost more than R2, which is
    what makes it an upper bound rather than just another rule.

    Returns (path, switches, trigger) for the winning trigger.
    """
    best = None
    for th in TRIGGERS:
        path, n = run_floating(principal, spread_pct, rates, start, tenure,
                               horizon, switch_cost, th, reset_months)
        if not path:
            continue
        if best is None or path[-1] < best[0][-1] - 1e-9:
            best = (path, n, th)
    return best if best else ([], 0, None)


def breakeven_spread(principal, rates, start, tenure, horizon, hdb_rate_pct,
                     switch_cost=None, lo=-10.0, hi=20.0, tol=1e-7,
                     reset_months=None):
    """
    The spread at which the bank route's total cost equals the HDB route's
    cumulative interest over the same months.

    Bisection. Cost rises monotonically in the spread, so a sign change is
    bracketed unless the horizon is empty. Returns None if it does not
    converge, which is the only unreliability condition the sealed file allows
    (section 6, T1). No plausibility filter: a negative spread is a valid
    result and is returned as one.

    reset_months  passed through to run_floating/run_r3; None is the base
                 case, 36 months (section 5). Used by the reset-interval
                 sensitivity, AMENDMENT 3.
    """
    hdb = run_fixed(principal, hdb_rate_pct, tenure, horizon)
    if not hdb:
        return None
    target = hdb[-1]

    def excess(s):
        if switch_cost is None:
            path, _ = run_floating(principal, s, rates, start, tenure, horizon,
                                   reset_months=reset_months)
        else:
            path, _n, _t = run_r3(principal, s, rates, start, tenure, horizon,
                                  switch_cost, reset_months=reset_months)
        return (path[-1] - target) if path else None

    a, b = excess(lo), excess(hi)
    if a is None or b is None or a > 0 or b < 0:
        return None
    for _ in range(200):
        mid = (lo + hi) / 2.0
        e = excess(mid)
        if e is None:
            return None
        if abs(e) < tol or (hi - lo) < 1e-10:
            return mid
        if e < 0:
            lo = mid
        else:
            hi = mid
    return None


def crossover_month(principal, spread_pct, rates, start, tenure, horizon,
                    hdb_rate_pct, switch_cost=None, reset_months=None):
    """
    First month index where the bank route stops being ahead, i.e. cumulative
    bank cost first meets or exceeds cumulative HDB interest.

    Returns 0 if the bank route was never ahead (crossover recorded at the
    start month, per T2 prediction 2b), or None if no crossover occurs inside
    the observed window.
    """
    hdb = run_fixed(principal, hdb_rate_pct, tenure, horizon)
    if switch_cost is None:
        bank, _ = run_floating(principal, spread_pct, rates, start, tenure,
                               horizon, reset_months=reset_months)
    else:
        bank, _n, _t = run_r3(principal, spread_pct, rates, start, tenure,
                              horizon, switch_cost, reset_months=reset_months)
    n = min(len(hdb), len(bank))
    if n == 0:
        return None
    if bank[0] >= hdb[0]:
        return 0
    for k in range(n):
        if bank[k] >= hdb[k]:
            return k
    return None


def _selftest():
    ok = True

    def check(name, cond):
        nonlocal ok
        print("  %-58s %s" % (name, "ok" if cond else "FAIL"))
        ok = ok and cond

    print("21_model.py selftest")

    # amortisation against a hand-computable case
    pay = amortise(400000.0, 0.026, 300)
    check("S$400k at 2.6%% over 300 months pays ~1,814/month",
          1800 < pay < 1830)

    # a zero-rate loan repays principal only
    z = run_fixed(100000.0, 0.0, 100, 100)
    check("zero-rate loan accrues no interest", abs(z[-1]) < 1e-9)

    # interest over the full tenure must equal payments less principal
    full = run_fixed(400000.0, 2.6, 300, 300)
    check("full-tenure interest equals payments less principal",
          abs(full[-1] - (pay * 300 - 400000.0)) < 1.0)

    # a flat benchmark equal to the HDB rate less the spread must tie exactly
    flat = [2.6 - 0.5] * 400
    hdb = run_fixed(400000.0, 2.6, 300, 300)
    bank, _ = run_floating(400000.0, 0.5, flat, 0, 300, 300)
    check("flat benchmark plus spread equal to 2.6 ties with HDB",
          abs(bank[-1] - hdb[-1]) < 1e-6)

    # and the solver recovers that spread
    s = breakeven_spread(400000.0, flat, 0, 300, 300, 2.6)
    check("solver recovers the 0.50 break-even on the flat case",
          s is not None and abs(s - 0.5) < 1e-4)

    # monotonicity: a wider spread always costs more
    costs = []
    for sp in (0.0, 0.5, 1.0, 2.0):
        p, _ = run_floating(400000.0, sp, flat, 0, 300, 300)
        costs.append(p[-1])
    check("cost is monotonically increasing in the spread",
          all(x < y for x, y in zip(costs, costs[1:])))

    # a benchmark above the HDB rate forces a negative break-even
    dear = [4.0] * 400
    s = breakeven_spread(400000.0, dear, 0, 300, 300, 2.6)
    check("benchmark above 2.6 gives a NEGATIVE break-even spread",
          s is not None and s < 0)

    # R3 can never cost more than R2 at zero switching cost
    import random
    random.seed(7)
    noisy = [max(0.05, 2.0 + random.uniform(-1.5, 1.5)) for _ in range(400)]
    r2, _ = run_floating(400000.0, 0.5, noisy, 0, 300, 300)
    r3, n3, _th = run_r3(400000.0, 0.5, noisy, 0, 300, 300, 0.0)
    check("R3 at zero cost is never worse than R2", r3[-1] <= r2[-1] + 1e-6)
    check("R3 at zero cost actually switches", n3 > 0)

    # raising the switching cost cannot increase the number of switches
    counts = []
    for c in SWITCH_COSTS:
        _p, k, _th = run_r3(400000.0, 0.5, noisy, 0, 300, 300, c)
        counts.append(k)
    check("switch count is non-increasing in the switching cost",
          all(x >= y for x, y in zip(counts, counts[1:])))
    check("R3 tolerates a zero-length horizon", run_r3(400000.0, 0.5, noisy, 0, 300, 0, 0.0)[0] == [])

    # R3 must be an upper bound on R2 at every switching cost, on the real
    # series. This is the property the first implementation violated.
    import csv, os
    rp = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                      "out", "rates_monthly.csv")
    if os.path.exists(rp):
        sora = [float(r["sora3m"]) for r in csv.DictReader(open(rp, encoding="utf-8"))]
        worst = None
        for st in (0, 24, 60, 120):
            if st >= len(sora):
                continue
            hz = len(sora) - st
            r2, _ = run_floating(PRINCIPAL, 1.0, sora, st, TENURE_MONTHS, hz)
            for c in SWITCH_COSTS:
                r3, _n, _th = run_r3(PRINCIPAL, 1.0, sora, st, TENURE_MONTHS, hz, c)
                d = r3[-1] - r2[-1]
                worst = d if worst is None else max(worst, d)
        check("on the real series R3 never costs more than R2, any cost",
              worst is not None and worst <= 1e-6)

    print("selftest", "passed" if ok else "FAILED")
    return 0 if ok else 1


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        sys.exit(_selftest())
    print(__doc__)
