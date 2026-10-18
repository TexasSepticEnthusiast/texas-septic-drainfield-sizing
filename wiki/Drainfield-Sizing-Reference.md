# Absorptive-area arithmetic and source reference

## Scope

The calculator implements A = Q / Ra using externally determined inputs. It does not determine whether a conventional system can be used on a site.

The method appears in **30 TAC §285.33(b)(1)(A)(vii)**, PDF page 63 of [TCEQ Rule Project 2021-030-285-CE, adopted in 2023](https://www.tceq.texas.gov/downloads/rules/adoptions/21030285_ado.pdf/@@download/file/21030285_ado.pdf#page=63). It references §285.91 Tables I and III. The source uses the most restrictive soil horizon along the media or within two feet below the excavation bottom when determining the application rate.

## Units and arithmetic

| Symbol | Supplied or calculated quantity | Units |
| --- | --- | --- |
| Q | Supplied design sewage flow | gallons/day |
| Ra | Supplied soil application rate | gallons/(square foot × day) |
| A | Calculated absorptive area, Q / Ra | square feet |

Example only: Q = 300 and Ra = 0.2 give A = 1500 sq ft. These numbers do not describe a particular home, soil series, or property.

The script rounds the exact decimal ratio upward to whole square feet. A result of 1500.0000000000001 therefore rounds to 1501, not 1500. The displayed area is not a complete design.

## Why no perc or soil-series defaults?

The cited method uses an application rate selected from the relevant site and rule information, not the previous script's minutes-per-inch lookup. A soil-series name does not establish the evaluated site's restrictive horizons, treatment compatibility, or application rate. The old presets were unsupported and have been removed.

The [TCEQ system-selection guidance](https://www.tceq.texas.gov/permitting/ossf/ossfsystems.html) distinguishes disposal methods and site constraints. Its table identifies septic-tank treatment followed by an absorptive drainfield as unsuitable in Class IV soil. Accepting a positive numeric Ra in this arithmetic tool does not override any such restriction.

## Why no trench layout?

The source's §285.33(b)(1)(A)(vii)(I), PDF page 64, addresses bottom area and sidewall credit. Other provisions address configuration and site conditions. Therefore, dividing A by a default trench width cannot establish a compliant length or footprint. The script does not compute excavation dimensions, usable lot area, spacing, reserve area, or construction quantities.

## Source review

- **Source reviewed:** TCEQ 2023 adopted text, PDF pages 63–64 and 103–105.
- **Review date:** 2026-10-18.
- **Current consolidated rule:** not verified. The [Secretary of State portal](https://texas-sos.appianportalsgov.com/rules-and-meetings?interface=VIEW_TAC&part=1&title=30) did not expose readable rule text to the review tools. TCEQ's [rules page](https://www.tceq.texas.gov/rules/indxpdf.html) warns that its PDFs are not current.
- **Local orders and site approval:** not evaluated. Recheck all inputs and applicable requirements with the permitting authority.

## Attribution

Prepared as an AI-assisted automated contribution for Jake's [Out West Septic](https://outwestseptic.com) project. This reference makes no claim of licensed authorship, field experience, or regulatory endorsement.
