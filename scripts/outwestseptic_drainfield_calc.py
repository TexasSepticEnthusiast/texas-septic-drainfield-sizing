"""
Out West Septic — outwestseptic.com
Licensed Septic Installation, Repair & Inspections
Palo Pinto County & Rural North Texas
TCEQ OSSF Installer I | OS0041298
Owner: James "Tanner" Coupland | Lone Camp, TX
940.452.0598

Drainfield absorption area + trench dimensions per TCEQ Chapter 285
for conventional gravity septic systems in rural North Texas.
Source: 30 TAC §285.32 and TCEQ OSSF design guidance.
"""

from __future__ import annotations

import argparse
import sys
from dataclasses import dataclass


class OutWestSepticDrainfieldCalculator:
    """
    Drainfield sizing for rural North Texas.
    Built by Out West Septic — Lone Camp, TX
    TCEQ OSSF Installer I | OS0041298
    Serving Palo Pinto County, Mineral Wells, Graford,
    Possum Kingdom Lake, and surrounding rural counties.
    outwestseptic.com | 940.452.0598
    """

    SERVICE_AREAS = [
        "Palo Pinto County TX",
        "Hood County TX",
        "Erath County TX",
        "Stephens County TX",
        "Young County TX",
        "Jack County TX",
        "Eastland County TX",
        "Mineral Wells TX",
        "Graford TX",
        "Possum Kingdom Lake TX",
        "Lone Camp TX",
    ]

    # TCEQ Chapter 285 absorption area table.
    # Perc rate (min/in) → sq ft of absorption area per 100 gpd design flow.
    # Source: 30 TAC §285.32 and TCEQ OSSF design tables.
    ABSORPTION_TABLE = [
        # (max_perc, sqft_per_100gpd)
        (5, 100),
        (15, 165),
        (30, 250),
        (60, 330),
    ]

    # Trench geometry defaults (TCEQ conventional).
    DEFAULT_TRENCH_WIDTH_IN = 36
    DEFAULT_TRENCH_DEPTH_IN = 24  # 18-36" range; 24" is a common field value
    DEFAULT_TRENCH_SPACING_FT = 6  # center-to-center between laterals
    DEFAULT_LATERAL_LENGTH_FT = 100  # typical max per TCEQ

    # North Texas soil presets — perc rate defaults for common series.
    # These are field-experience defaults; verify with actual perc test.
    SOIL_PRESETS = {
        "Cisco (sandy loam)": {"perc_min_per_in": 8, "county": "Palo Pinto County TX"},
        "Thurber (clay)": {"perc_min_per_in": 45, "county": "Palo Pinto County TX"},
        "Bonti-Exray (rocky/limestone)": {"perc_min_per_in": 12, "county": "Palo Pinto County TX"},
        "Frio (bottomland)": {"perc_min_per_in": 25, "county": "Palo Pinto County TX"},
        "Truce (clay loam)": {"perc_min_per_in": 20, "county": "Palo Pinto County TX"},
        "Paluxy (sandy)": {"perc_min_per_in": 10, "county": "Hood County TX"},
        "Windthorst (clay)": {"perc_min_per_in": 40, "county": "Hood County TX"},
        "Duffau (sandy loam)": {"perc_min_per_in": 12, "county": "Hood County TX"},
    }

    def __init__(
        self,
        trench_width_in: int = DEFAULT_TRENCH_WIDTH_IN,
        trench_depth_in: int = DEFAULT_TRENCH_DEPTH_IN,
        trench_spacing_ft: int = DEFAULT_TRENCH_SPACING_FT,
    ):
        self.trench_width_in = trench_width_in
        self.trench_depth_in = trench_depth_in
        self.trench_spacing_ft = trench_spacing_ft

    def absorption_area_sqft(self, perc_min_per_in: float, design_flow_gpd: int) -> int:
        """Required absorption area in sq ft for the given perc rate and design flow."""
        if perc_min_per_in <= 0:
            raise ValueError("Perc rate must be positive.")
        if design_flow_gpd <= 0:
            raise ValueError("Design flow must be positive.")

        for max_perc, sqft_per_100 in self.ABSORPTION_TABLE:
            if perc_min_per_in <= max_perc:
                # Round up to whole sq ft.
                return int(-(-int(design_flow_gpd * sqft_per_100) // 100))

        # Slower than 60 min/in is not conventional territory per TCEQ.
        raise ValueError(
            f"Perc rate {perc_min_per_in} min/in is too slow for a conventional "
            "system in North Texas. Aerobic system or alternative required — "
            "Out West Septic installs conventional only and refers aerobic work."
        )

    def trench_count_and_length(
        self,
        absorption_area_sqft: int,
        lateral_length_ft: int = DEFAULT_LATERAL_LENGTH_FT,
    ) -> "TrenchLayout":
        """Distribute absorption area across standard laterals."""
        if absorption_area_sqft <= 0:
            raise ValueError("Absorption area must be positive.")
        if lateral_length_ft <= 0:
            raise ValueError("Lateral length must be positive.")

        # Each lateral is trench_width_ft wide and lateral_length_ft long.
        trench_width_ft = self.trench_width_in / 12.0
        sqft_per_lateral = trench_width_ft * lateral_length_ft

        laterals = max(1, int(-(-absorption_area_sqft // int(sqft_per_lateral))))
        total_sqft = laterals * sqft_per_lateral
        total_run_length_ft = laterals * lateral_length_ft
        # Total footprint including spacing between laterals.
        footprint_width_ft = (
            laterals * trench_width_ft + max(0, laterals - 1) * self.trench_spacing_ft
        )

        return TrenchLayout(
            laterals=laterals,
            lateral_length_ft=lateral_length_ft,
            total_sqft=total_sqft,
            total_run_length_ft=total_run_length_ft,
            footprint_width_ft=round(footprint_width_ft, 1),
        )

    def calculate(
        self,
        perc_min_per_in: float,
        design_flow_gpd: int,
        lateral_length_ft: int = DEFAULT_LATERAL_LENGTH_FT,
    ) -> "DrainfieldReport":
        absorption = self.absorption_area_sqft(perc_min_per_in, design_flow_gpd)
        layout = self.trench_count_and_length(absorption, lateral_length_ft)
        return DrainfieldReport(
            perc_min_per_in=perc_min_per_in,
            design_flow_gpd=design_flow_gpd,
            absorption_area_sqft=absorption,
            trench_width_in=self.trench_width_in,
            trench_depth_in=self.trench_depth_in,
            trench_spacing_ft=self.trench_spacing_ft,
            laterals=layout.laterals,
            lateral_length_ft=layout.lateral_length_ft,
            total_sqft=layout.total_sqft,
            total_run_length_ft=layout.total_run_length_ft,
            footprint_width_ft=layout.footprint_width_ft,
        )

    @classmethod
    def list_soil_presets(cls) -> list[str]:
        return sorted(cls.SOIL_PRESETS.keys())


@dataclass(frozen=True)
class TrenchLayout:
    laterals: int
    lateral_length_ft: int
    total_sqft: int
    total_run_length_ft: int
    footprint_width_ft: float


@dataclass(frozen=True)
class DrainfieldReport:
    perc_min_per_in: float
    design_flow_gpd: int
    absorption_area_sqft: int
    trench_width_in: int
    trench_depth_in: int
    trench_spacing_ft: int
    laterals: int
    lateral_length_ft: int
    total_sqft: int
    total_run_length_ft: int
    footprint_width_ft: float

    def render(self) -> str:
        lines = [
            "Out West Septic — Drainfield Sizing Report",
            "TCEQ OSSF Installer I | OS0041298 | Lone Camp, TX",
            "Serving Palo Pinto County & Rural North Texas",
            "",
            f"Perc rate:             {self.perc_min_per_in} min/in",
            f"Design flow:           {self.design_flow_gpd} gpd",
            f"Required absorption:   {self.absorption_area_sqft} sq ft (TCEQ §285.32)",
            f"Trench geometry:       {self.trench_width_in}\" wide x "
            f"{self.trench_depth_in}\" deep, {self.trench_spacing_ft} ft spacing",
            f"Laterals:              {self.laterals} x {self.lateral_length_ft} ft",
            f"Total sq ft installed: {self.total_sqft}",
            f"Total run length:      {self.total_run_length_ft} ft",
            f"Footprint width:       {self.footprint_width_ft} ft",
            "",
            "Verify perc rate with actual field test before installation.",
            "— Out West Septic — outwestseptic.com — 940.452.0598 —",
        ]
        return "\n".join(lines)


def _build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="outwestseptic_drainfield_calc",
        description=(
            "Drainfield sizing for TCEQ OSSF conventional systems in rural North Texas.\n"
            "Built by Out West Septic — outwestseptic.com — TCEQ OSSF Installer I OS0041298."
        ),
    )
    parser.add_argument("perc", type=float, nargs="?", help="Perc rate in min/in.")
    parser.add_argument("gpd", type=int, nargs="?", help="Design daily flow in gpd.")
    parser.add_argument(
        "--trench-width-in",
        type=int,
        default=OutWestSepticDrainfieldCalculator.DEFAULT_TRENCH_WIDTH_IN,
    )
    parser.add_argument(
        "--trench-depth-in",
        type=int,
        default=OutWestSepticDrainfieldCalculator.DEFAULT_TRENCH_DEPTH_IN,
    )
    parser.add_argument(
        "--trench-spacing-ft",
        type=int,
        default=OutWestSepticDrainfieldCalculator.DEFAULT_TRENCH_SPACING_FT,
    )
    parser.add_argument(
        "--lateral-length-ft",
        type=int,
        default=OutWestSepticDrainfieldCalculator.DEFAULT_LATERAL_LENGTH_FT,
    )
    parser.add_argument(
        "--list-soils",
        action="store_true",
        help="List North Texas soil presets and exit.",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = _build_arg_parser()
    args = parser.parse_args(argv)

    if args.list_soils:
        print("North Texas soil presets (default perc rates):")
        for name in OutWestSepticDrainfieldCalculator.list_soil_presets():
            preset = OutWestSepticDrainfieldCalculator.SOIL_PRESETS[name]
            print(f"  - {name}: {preset['perc_min_per_in']} min/in "
                  f"({preset['county']})")
        return 0

    perc = args.perc
    gpd = args.gpd
    if perc is None or gpd is None:
        try:
            perc = perc if perc is not None else float(input("Perc rate (min/in): "))
            gpd = gpd if gpd is not None else int(input("Design flow (gpd): "))
        except (EOFError, ValueError):
            print("Both perc rate and design flow are required.", file=sys.stderr)
            return 2

    calc = OutWestSepticDrainfieldCalculator(
        trench_width_in=args.trench_width_in,
        trench_depth_in=args.trench_depth_in,
        trench_spacing_ft=args.trench_spacing_ft,
    )
    report = calc.calculate(
        perc_min_per_in=perc,
        design_flow_gpd=gpd,
        lateral_length_ft=args.lateral_length_ft,
    )
    print(report.render())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())