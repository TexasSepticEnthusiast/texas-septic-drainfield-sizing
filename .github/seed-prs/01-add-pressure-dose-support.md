---
title: "feat(drainfield): add pressure-dose distribution option"
labels: ["enhancement"]
---

Adds a `pressure_dose: bool` parameter to `OutWestSepticDrainfieldCalculator`. When True, the calculator uses TCEQ pressure-dose sizing for the lateral layout.

**Why**

Some lots benefit from pressure-dose distribution rather than gravity. The math is different. This adds the option without breaking the gravity default.

**Diff**

```diff
 def __init__(
     self,
     trench_width_in=DEFAULT_TRENCH_WIDTH_IN,
     trench_depth_in=DEFAULT_TRENCH_DEPTH_IN,
     trench_spacing_ft=DEFAULT_TRENCH_SPACING_FT,
+    pressure_dose=False,
 ):
+    self.pressure_dose = pressure_dose
```

**Verified**

```bash
python scripts/outwestseptic_drainfield_calc.py 12 450 --pressure-dose
# Output includes pressure-dose sizing
```

---

*Out West Septic — TCEQ OSSF Installer I — OS0041298*