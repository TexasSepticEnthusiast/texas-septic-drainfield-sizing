"""Regression tests for exact area arithmetic and safe explicit-input CLI."""
import subprocess
import sys
import unittest
from decimal import Decimal
from fractions import Fraction
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from outwestseptic_drainfield_calc import OutWestSepticDrainfieldCalculator

SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "outwestseptic_drainfield_calc.py"


class DrainfieldTests(unittest.TestCase):
    def setUp(self):
        self.calculator = OutWestSepticDrainfieldCalculator()

    def area(self, flow, rate):
        return self.calculator.absorption_area_sqft(
            design_flow_gpd=flow, loading_rate_gpd_per_sqft=rate
        )

    def test_supplied_input_examples(self):
        self.assertEqual(self.area(300, "0.2"), 1500)
        self.assertEqual(self.area(450, "0.38"), 1185)
        self.assertEqual(self.area(300.25, "0.25"), 1201)
        self.assertEqual(self.area(5000, "0.2"), 25000)

    def test_decimal_rounding_at_whole_square_foot_boundary(self):
        self.assertEqual(self.area("0.07", "0.01"), 7)
        self.assertEqual(self.area("0.070000000000000001", "0.01"), 8)
        self.assertEqual(self.area("0.069999999999999999", "0.01"), 7)
        self.assertEqual(self.area("0.00001", "0.2"), 1)

    def test_area_covers_exact_ratio_with_less_than_one_sqft_rounding(self):
        for flow in ["0.001", "180", "300.25", "4999.99", "5000"]:
            for rate in ["0.1", "0.2", "0.25", "0.38"]:
                with self.subTest(flow=flow, rate=rate):
                    exact = Fraction(flow) / Fraction(rate)
                    actual = self.area(flow, rate)
                    self.assertGreaterEqual(actual, exact)
                    self.assertLess(actual - exact, 1)

    def test_area_increases_with_flow_and_decreases_with_rate(self):
        self.assertGreater(self.area(400, "0.2"), self.area(300, "0.2"))
        self.assertGreater(self.area(300, "0.2"), self.area(300, "0.38"))

    def test_invalid_input_rejected_for_both_quantities(self):
        values = [0, -1, True, False, None, [], "abc", "", "NaN", "sNaN",
                  "Infinity", "-Infinity", float("nan"), float("inf"),
                  Decimal("-Infinity"), "1e9999", "1e-9999", 10 ** 1000]
        for value in values:
            for field in ["design_flow_gpd", "loading_rate_gpd_per_sqft"]:
                with self.subTest(value=repr(value)[:40], field=field):
                    args = dict(design_flow_gpd=300, loading_rate_gpd_per_sqft="0.2")
                    args[field] = value
                    with self.assertRaises(ValueError):
                        self.calculator.calculate(**args)

    def test_flow_scope(self):
        with self.assertRaises(ValueError):
            self.area("5000.00001", "0.2")

    def test_small_finite_rate_does_not_overflow_float_division(self):
        self.assertEqual(self.area(1, "1e-308"), 10 ** 308)

    def test_old_perc_and_geometry_api_fails(self):
        with self.assertRaises(TypeError):
            self.calculator.calculate(8, 450)
        with self.assertRaises(TypeError):
            self.calculator.absorption_area_sqft(8, 450)
        with self.assertRaises(TypeError):
            OutWestSepticDrainfieldCalculator(trench_width_in=0)

    def test_report_preserves_supplied_decimal_precision_and_limits(self):
        report = self.calculator.calculate(
            design_flow_gpd="300.25", loading_rate_gpd_per_sqft="0.25"
        )
        self.assertEqual(report.design_flow_gpd, Decimal("300.25"))
        text = report.render()
        self.assertIn("1201 sq ft", text)
        self.assertIn("not a lot footprint or trench layout", text)
        self.assertIn("TCEQ 2023 adopted text", text)


class CommandLineTests(unittest.TestCase):
    def run_cli(self, *args):
        return subprocess.run(
            [sys.executable, str(SCRIPT), *args],
            input="", capture_output=True, text=True, timeout=10,
        )

    def test_valid_cli(self):
        result = self.run_cli("--flow-gpd", "300", "--loading-rate", "0.2")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("1500 sq ft", result.stdout)
        self.assertEqual(result.stderr, "")

    def test_invalid_cli_returns_usage_without_report_or_traceback(self):
        cases = [(), ("8", "450"), ("--list-soils",),
                 ("--flow-gpd", "300"),
                 ("--flow-gpd", "300", "--loading-rate", "0.2", "--trench-width-in", "0")]
        for value in ["0", "-1", "nan", "inf", "abc", "1e9999", "1e-9999"]:
            cases.append(("--flow-gpd", value, "--loading-rate", "0.2"))
            cases.append(("--flow-gpd", "300", "--loading-rate", value))
        cases.append(("--flow-gpd", "5001", "--loading-rate", "0.2"))
        for args in cases:
            with self.subTest(args=args):
                result = self.run_cli(*args)
                self.assertEqual(result.returncode, 2)
                self.assertEqual(result.stdout, "")
                self.assertIn("error:", result.stderr)
                self.assertNotIn("Traceback", result.stderr)

    def test_help_is_noninteractive(self):
        result = self.run_cli("--help")
        self.assertEqual(result.returncode, 0)
        self.assertIn("--loading-rate", result.stdout)


if __name__ == "__main__":
    unittest.main()
