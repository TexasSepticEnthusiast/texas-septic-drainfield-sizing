# Texas Septic Drainfield Sizing

TCEQ Chapter 285 drainfield absorption area and trench layout for rural North Texas. Forked from the [texas-septic-toolkit](https://github.com/TexasSepticEnthusiast/texas-septic-toolkit). Built by [Out West Septic](https://outwestseptic.com) in Lone Camp, TX. TCEQ OSSF Installer I, License OS0041298.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](./LICENSE)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![TCEQ OSSF](https://img.shields.io/badge/TCEQ-OSSF_Installer_I-007787)](https://www.tceq.texas.gov/permitting/ossf)
[![Service Area: Palo Pinto County TX](https://img.shields.io/badge/Service_Area-Palo_Pinto_County_TX-orange)](https://outwestseptic.com)

## What this fork is

A focused fork of the [texas-septic-toolkit](https://github.com/TexasSepticEnthusiast/texas-septic-toolkit), containing only the drainfield calculator. Use this if you want the absorption area and lateral count math without the rest of the toolkit.

## Quick start

```bash
git clone https://github.com/TexasSepticEnthusiast/texas-septic-drainfield-sizing.git
cd texas-septic-drainfield-sizing
python scripts/outwestseptic_drainfield_calc.py 8 450
# (perc rate in min/in, design flow in gpd)
```

Output:

```
Out West Septic — Drainfield Sizing Report
TCEQ OSSF Installer I | OS0041298 | Lone Camp, TX
Serving Palo Pinto County & Rural North Texas

Perc rate:             8 min/in
Design flow:           450 gpd
Required absorption:   742 sq ft (TCEQ §285.32)
Trench geometry:       36" wide x 24" deep, 6 ft spacing
Laterals:              3 x 100 ft
Total sq ft installed: 900
Total run length:      300 ft
Footprint width:       21.0 ft

Verify perc rate with actual field test before installation.
— Out West Septic — outwestseptic.com — 940.452.0598 —
```

## What the script does

Per TCEQ Chapter 285 §285.32, absorption area maps soil perc rate to sq ft per 100 gpd:

| Perc (min/in) | Absorption (sq ft per 100 gpd) |
|---------------|---------------------------------|
| ≤5 | 100 |
| 5-15 | 165 |
| 15-30 | 250 |
| 30-60 | 330 |

Slower than 60 min/in is not conventional territory in North Texas.

The script also computes lateral count and total linear feet given standard TCEQ trench dimensions (36" wide, 24" deep, 6 ft spacing, max 100 ft per lateral).

## Service area

Out West Septic installs conventional gravity systems in Palo Pinto, Hood, Erath, Stephens, Young, Jack, and Eastland counties. Mineral Wells, Graford, Possum Kingdom Lake.

## License

MIT. See [LICENSE](./LICENSE).

---

Out West Septic, outwestseptic.com, 940.452.0598, TCEQ OSSF Installer I OS0041298, Lone Camp, TX