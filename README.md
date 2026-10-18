# Texas Septic Drainfield Sizing

An educational Python calculator for **A = Q / Ra**, the absorptive-area arithmetic in TCEQ's **2023 adopted text** of 30 TAC §285.33(b)(1)(A)(vii). Both design flow and soil application rate must be determined outside this tool.

This is an AI-assisted automated contribution for Jake's [Out West Septic](https://outwestseptic.com) project. It is project-affiliated educational software, not an independent endorsement, licensed design, or statement of permit approval.

## Run it

Python 3.10 or newer; no third-party packages.

```bash
git clone https://github.com/TexasSepticEnthusiast/texas-septic-drainfield-sizing.git
cd texas-septic-drainfield-sizing
python scripts/outwestseptic_drainfield_calc.py --flow-gpd 300 --loading-rate 0.2
```

```text
Out West Septic project - Educational absorptive-area calculation
Supplied design flow Q: 300 gpd
Supplied application rate Ra: 0.2 gpd/sq ft
Q / Ra, rounded up: 1500 sq ft of absorptive area
Method: 30 TAC 285.33(b)(1)(A)(vii) (TCEQ 2023 adopted text).
Absorptive area is not a lot footprint or trench layout.
Input suitability, site eligibility, and permit approval are not evaluated.
Verify current rules and local requirements with the permitting authority.
```

The example is arithmetic only. It assigns neither a design flow to a home nor an application rate to a soil series, county, or property.

## Inputs and results

- `--flow-gpd` supplies Q in gallons/day: greater than zero and at most 5000.
- `--loading-rate` supplies Ra in gallons per square foot per day: positive and finite. This is **not** a percolation time in minutes/inch.
- Both inputs must fit within the positive finite floating-point magnitude range. Internally, exact fractions of their decimal representations avoid binary-division rounding errors.
- The area is rounded **up** to a whole square foot. For example, 450 / 0.38 is displayed as 1185 sq ft.
- Missing, invalid, nonfinite, or out-of-scope inputs exit with status 2 and an error message, without prompting or producing a sizing report.

A positive rate is accepted for arithmetic, not validated against a soil class, treatment method, site evaluation, or permit. Absorptive area includes concepts that differ from land footprint; no trench dimensions or sidewall credits are calculated.

## Python API

```python
from scripts.outwestseptic_drainfield_calc import OutWestSepticDrainfieldCalculator

report = OutWestSepticDrainfieldCalculator().calculate(
    design_flow_gpd="300",
    loading_rate_gpd_per_sqft="0.2",
)
print(report.absorption_area_sqft)  # 1500
```

Use named arguments. Integers, floats, decimal strings, and `decimal.Decimal` values are supported; use strings or Decimal to preserve supplied decimal precision. Booleans are rejected.

## What this cannot determine

A site evaluation and applicable planning process must establish Q, Ra, and disposal-system suitability. The tool does not choose a treatment method or validate soil depth, restrictive layers, groundwater, slope, setbacks, local orders, trench geometry, construction, or approval.

Read the [formula and source reference](wiki/Drainfield-Sizing-Reference.md) and [TCEQ system-selection guidance](https://www.tceq.texas.gov/permitting/ossf/ossfsystems.html) before interpreting the arithmetic.

## Migration from the previous interface

The positional `perc gpd` arguments, soil-series perc presets, `--list-soils`, and automatic trench-layout options were removed. The prior percolation-rate lookup had no support in the cited TCEQ method, and automatic geometry omitted required considerations. Old invocations intentionally fail; obtain explicit Q and Ra before using the new flags.

The class name is retained, but `calculate` and `absorption_area_sqft` require named flow and rate arguments. The old geometry constructor and layout API are no longer supported.

Seed issue/PR files that claimed unverified field experience or completed changes were removed.

## Verify changes

```bash
python -m unittest discover -s tests -v
```

Tests cover exact and non-integer ratios, decimal rounding boundaries, invalid API inputs, flow limits, extreme finite values, and command-line success and failure. GitHub Actions runs the suite on Python 3.10 and 3.13 when enabled.

## Source status and license

Reviewed against the [TCEQ 2023 adoption document](https://www.tceq.texas.gov/downloads/rules/adoptions/21030285_ado.pdf/@@download/file/21030285_ado.pdf#page=63) on 2026-10-18. This is a source-edition check, **not verification of the current consolidated rule**. TCEQ [warns that its rule PDFs are not current](https://www.tceq.texas.gov/rules/indxpdf.html) and directs readers to the Secretary of State. Recheck current and local requirements before project use.

See the repository's existing [license reference](LICENSE).
