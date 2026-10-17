---
title: "[feature] Add support for mounded drainfield systems"
labels: ["enhancement"]
---

Some lots in Palo Pinto County have shallow soil over bedrock and need a **mounded drainfield** rather than a standard subsurface one. The current `outwestseptic_drainfield_calc.py` assumes standard trenches.

**What I'd want**

- A `--mound` flag that adjusts the math for sand mound systems
- TCEQ §285.32 has separate sizing for mounds

**Why**

We do a few mound systems per year on Bonti-Exray lots. Having the script handle it would save manual math.

**Affected file**

`scripts/outwestseptic_drainfield_calc.py`

---

*Out West Septic — TCEQ OSSF Installer I — OS0041298*