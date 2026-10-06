"""
test_pipeline.py -- the cargradient pipeline on invented data only.

  python3 -m unittest discover -s cargradient/tests -p "test_*.py" -v

Each scenario builds fixtures with make_fixtures.make(), runs steps 10-15 end
to end with --root on a temporary copy, and checks the sealed outcome of
every test. Together the scenarios force every branch of THESIS section 6:

  T1, T2: SURVIVE, FAIL_NO_LINK, FAIL_OPPOSITE, NOT_SCORED (first-stage F
          gate; geocoding gate)
  T3:     SURVIVE, FAIL_NO_CHANGE, FAIL_STRONGER, NOT_SCORED_NO_TILT (the
          premise: no tilt before 2018), NOT_SCORED (F gate; geocoding gate)
  7A:     share readable, and not readable
  Brier and expected held from confidences, when set.

THESIS has no INCONCLUSIVE outcome: an interval that includes zero is a FAIL
(FAIL_NO_LINK, FAIL_NO_CHANGE), by the bets as written.

The guard test runs 10_load.py and 15_reproduce.py against the real
cargradient/raw/ and requires the refusal (exit 3) while cargradient/SEALED
does not exist.
"""
import csv
import os
import shutil
import subprocess
import sys
import tempfile
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
CG = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import make_fixtures as M  # noqa: E402

PY = sys.executable
ENV = dict(os.environ, CG_BOOT_N="9", PYTHONPATH=CG)
STEPS = ["10_load.py", "11_tests.py", "12_figures.py", "15_reproduce.py", "13_results.py"]


def run(root):
    for s in STEPS:
        p = subprocess.run([PY, os.path.join(CG, s), "--root", root], env=ENV, capture_output=True, text=True)
        if p.returncode != 0:
            raise AssertionError(f"{s} failed ({p.returncode}):\n{p.stdout[-2000:]}\n{p.stderr[-3000:]}")
    for args in (["--root", root], ["--root", root, "--check"]):
        p = subprocess.run([PY, os.path.join(CG, "14_manifest.py")] + args, env=ENV, capture_output=True, text=True)
        if p.returncode != 0:
            raise AssertionError(f"14_manifest {args} failed:\n{p.stdout}\n{p.stderr}")
    T = {r["key"]: r["value"] for r in csv.DictReader(open(os.path.join(root, "out", "tests.csv")))}
    C = {r["key"]: r["value"] for r in csv.DictReader(open(os.path.join(root, "out", "calc_7a.csv")))}
    return T, C


class Scenario(unittest.TestCase):
    params = {}
    expect = {}
    readable = None

    @classmethod
    def setUpClass(cls):
        if cls is Scenario:
            raise unittest.SkipTest("base class")
        cls.root = tempfile.mkdtemp(prefix="cg_fx_")
        M.make(cls.root, **cls.params)
        cls.T, cls.C = run(cls.root)

    @classmethod
    def tearDownClass(cls):
        if cls is not Scenario:
            shutil.rmtree(cls.root, ignore_errors=True)

    def test_outcomes(self):
        for t, oc in self.expect.items():
            self.assertEqual(self.T[f"{t}_outcome"], oc, t)

    def test_reproduced(self):
        self.assertTrue(open(os.path.join(self.root, "out", "reproduce.txt")).read().startswith(
            "compared 27 numbers and outcomes; differences 0"))

    def test_results_failures_first(self):
        text = open(os.path.join(self.root, "RESULTS.md")).read()
        heads = [ln for ln in text.splitlines() if ln.startswith("### T")]
        rank = [0 if ": FAIL" in h else 1 if ": NOT_SCORED" in h else 2 for h in heads]
        self.assertEqual(rank, sorted(rank))

    def test_figures(self):
        for f in ("cargradient_chart1_tests.svg", "cargradient_chart2_years.svg"):
            s = open(os.path.join(self.root, "figs", f)).read()
            self.assertIn("prefers-color-scheme: dark", s)
            self.assertIn("How to read", s)

    def test_calc_7a(self):
        if self.readable is not None:
            self.assertEqual(self.C["share_readable"], str(self.readable))


class A_AllSurvive(Scenario):
    params = dict(confidences={"T1": 70, "T2": 60, "T3": 40}, actual_gap_shift=-0.6)
    expect = {"T1": "SURVIVE", "T2": "SURVIVE", "T3": "SURVIVE"}
    readable = True

    def test_brier(self):
        self.assertAlmostEqual(float(self.T["brier"]), ((0.7 - 1) ** 2 + (0.6 - 1) ** 2 + (0.4 - 1) ** 2) / 3, 6)
        self.assertAlmostEqual(float(self.T["expected_held"]), 1.7, 6)

    def test_verdict(self):
        v = open(os.path.join(self.root, "out", "verdict.txt")).read()
        self.assertTrue(v.startswith("Not only a coincidence"))


class B_NoLinkOppositeNoTilt(Scenario):
    params = dict(beta_pre=0.0, beta_before=0.0, beta_after=0.003)
    expect = {"T1": "FAIL_NO_LINK", "T2": "FAIL_OPPOSITE", "T3": "NOT_SCORED_NO_TILT"}

    def test_verdict(self):
        v = open(os.path.join(self.root, "out", "verdict.txt")).read()
        self.assertIn("If anything the opposite", v)
        self.assertIn("There was no link before 2018 to weaken", v)


class C_OppositeNoChange(Scenario):
    params = dict(beta_pre=0.003, beta_before=-0.003, beta_after=-0.003)
    expect = {"T1": "FAIL_OPPOSITE", "T2": "SURVIVE", "T3": "FAIL_NO_CHANGE"}


class D_Stronger(Scenario):
    params = dict(beta_after=-0.007)
    expect = {"T1": "SURVIVE", "T3": "FAIL_STRONGER"}


class E_WeakBeforeFGate(Scenario):
    params = dict(strong_before=False)
    expect = {"T3": "NOT_SCORED"}

    def test_gate(self):
        self.assertLess(float(self.T["T3_F_before"]), 10.0)
        self.assertEqual(self.T["T3_F_ok"], "False")


class F_WeakT1FGate(Scenario):
    params = dict(strong_pre=False, strong_before=False)
    expect = {"T1": "NOT_SCORED", "T3": "NOT_SCORED"}

    def test_gate(self):
        self.assertLess(float(self.T["T1_F"]), 10.0)


class G_GeocodeGate(Scenario):
    params = dict(unmatched_t2_share=0.10)
    expect = {"T1": "SURVIVE", "T2": "NOT_SCORED", "T3": "NOT_SCORED"}

    def test_gate(self):
        self.assertLess(float(self.T["T2_geo_share"]), 0.95)
        self.assertEqual(self.T["T2_geo_ok"], "False")


class H_NoAfterTiltNotReadable(Scenario):
    params = dict(beta_after=0.0)
    expect = {"T3": "SURVIVE"}
    readable = False


class Guard(unittest.TestCase):
    def test_refuses_real_raw_before_seal(self):
        self.assertFalse(os.path.exists(os.path.join(CG, "SEALED")), "SEALED exists: the guard test needs it absent")
        for s in ("10_load.py", "15_reproduce.py"):
            p = subprocess.run([PY, os.path.join(CG, s)], env=ENV, capture_output=True, text=True)
            self.assertEqual(p.returncode, 3, s)
            self.assertIn("REFUSED", p.stderr)
        self.assertFalse(os.path.exists(os.path.join(CG, "out", "panel.csv.gz")))

    def test_fixture_root_is_allowed(self):
        sys.path.insert(0, CG)
        import cglib as L
        root = tempfile.mkdtemp(prefix="cg_guard_")
        try:
            self.assertEqual(L.guard(os.path.join(root, "raw")), os.path.join(root, "raw"))
        finally:
            shutil.rmtree(root)


if __name__ == "__main__":
    unittest.main()
