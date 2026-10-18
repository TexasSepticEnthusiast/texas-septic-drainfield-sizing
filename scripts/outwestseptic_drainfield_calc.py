"""Educational A = Q / Ra arithmetic using externally determined inputs.

Source: TCEQ 2023 adopted rule, 30 TAC 285.33(b)(1)(A)(vii).
See the repository documentation for source and scope limitations.
This automated contribution is for Jake's Out West Septic project.
"""

from __future__ import annotations

import argparse
import math
from dataclasses import dataclass
from decimal import Decimal, InvalidOperation
from fractions import Fraction


NumericInput = str | int | float | Decimal


def _positive_decimal(value: NumericInput, name: str) -> Decimal:
    """Preserve decimal inputs while rejecting booleans and nonfinite values.

    Bound input magnitude to the positive finite floating-point range so
    pathological exponents cannot create arbitrarily large integer ratios.
    Calculation below uses exact decimal fractions, not binary float division.
    """
    if isinstance(value, bool) or not isinstance(value, (str, int, float, Decimal)):
        raise ValueError(f"{name} must be a positive finite number.")
    try:
        number = Decimal(str(value))
        magnitude = float(number)
    except (InvalidOperation, ValueError, OverflowError):
        raise ValueError(f"{name} must be a positive finite number.") from None
    if not number.is_finite() or not math.isfinite(magnitude) or magnitude <= 0:
        raise ValueError(f"{name} must be positive and within the finite floating-point range.")
    return number


class OutWestSepticDrainfieldCalculator:
    """Calculate absorptive area; do not select a soil rate or trench layout."""

    def calculate(
        self, *, design_flow_gpd: NumericInput, loading_rate_gpd_per_sqft: NumericInput,
    ) -> "OutWestSepticDrainfieldReport":
        """Round exact decimal Q/Ra upward to a whole square foot.

        Named arguments prevent old positional perc-rate calls from being
        silently interpreted as application rates. Positive inputs do not imply
        that a rate or disposal method is suitable for a site.
        """
        flow = _positive_decimal(design_flow_gpd, "Design flow")
        rate = _positive_decimal(loading_rate_gpd_per_sqft, "Loading rate")
        if flow > 5000:
            raise ValueError("Design flow must not exceed this calculator's 5000 gpd scope.")
        area = Fraction(flow) / Fraction(rate)
        return OutWestSepticDrainfieldReport(
            design_flow_gpd=flow,
            loading_rate_gpd_per_sqft=rate,
            absorption_area_sqft=math.ceil(area),
        )

    def absorption_area_sqft(
        self, *, design_flow_gpd: NumericInput, loading_rate_gpd_per_sqft: NumericInput,
    ) -> int:
        """Return the rounded-up area without generating a rendered report."""
        return self.calculate(
            design_flow_gpd=design_flow_gpd,
            loading_rate_gpd_per_sqft=loading_rate_gpd_per_sqft,
        ).absorption_area_sqft


@dataclass(frozen=True)
class OutWestSepticDrainfieldReport:
    design_flow_gpd: Decimal
    loading_rate_gpd_per_sqft: Decimal
    absorption_area_sqft: int

    def render(self) -> str:
        return "\n".join([
            "Out West Septic project - Educational absorptive-area calculation",
            f"Supplied design flow Q: {self.design_flow_gpd} gpd",
            f"Supplied application rate Ra: {self.loading_rate_gpd_per_sqft} gpd/sq ft",
            f"Q / Ra, rounded up: {self.absorption_area_sqft} sq ft of absorptive area",
            "Method: 30 TAC 285.33(b)(1)(A)(vii) (TCEQ 2023 adopted text).",
            "Absorptive area is not a lot footprint or trench layout.",
            "Input suitability, site eligibility, and permit approval are not evaluated.",
            "Verify current rules and local requirements with the permitting authority.",
        ])


# Preserve the previous report type import for existing callers.
DrainfieldReport = OutWestSepticDrainfieldReport


def _build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="outwestseptic_drainfield_calc",
        description="Educational A = Q / Ra arithmetic using externally determined inputs.",
        epilog="A percolation time or soil-series name is not an application rate.",
        allow_abbrev=False,
    )
    parser.add_argument(
        "--flow-gpd", required=True,
        help="Externally determined design flow in gallons/day, greater than 0 and at most 5000.",
    )
    parser.add_argument(
        "--loading-rate", required=True,
        help="Externally determined Ra in gallons per square foot per day; positive and finite.",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = _build_arg_parser()
    args = parser.parse_args(argv)
    try:
        report = OutWestSepticDrainfieldCalculator().calculate(
            design_flow_gpd=args.flow_gpd,
            loading_rate_gpd_per_sqft=args.loading_rate,
        )
    except ValueError as error:
        parser.error(str(error))
    print(report.render())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
