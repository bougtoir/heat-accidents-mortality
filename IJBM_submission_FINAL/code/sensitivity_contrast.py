#!/usr/bin/env python3
"""
Supplementary contrast-robustness check (IJBM revision).

Refits the primary US anomaly model from the committed processed CSVs and
reports the same-day and cumulative (lag 0-10) rate ratios at three anomaly
contrasts: +5 degC, the empirical 95th percentile of the anomaly distribution,
and +9 degC (the manuscript's reference contrast).  Tests whether the
interpretation depends uniquely on the +9 degC choice.  Writes
data/processed/us_contrast_sensitivity.csv.
"""
import os
import sys
import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
PROC = os.path.join(ROOT, "data", "processed")
sys.path.insert(0, HERE)

from analyze_us import load_panel, confounders  # noqa: E402
from model import fit_model, cumulative_curve, bin_response  # noqa: E402


def main():
    df = load_panel()
    m = fit_model(df, "anom", confounders, group="unit")
    m["expname"] = "anom"

    p95 = float(np.percentile(df.anom, 95))
    rows = []
    for label, a in (("+5C", 5.0), ("p95", p95), ("+9C", 9.0)):
        s = bin_response(m, a, 0.0).iloc[0]
        c = cumulative_curve(m, [a], 0.0).iloc[0]
        rows.append({
            "contrast": label,
            "anomaly_degC": round(a, 2),
            "sameday_RR": round(float(s.rr), 3),
            "sameday_lo": round(float(s.lo), 3),
            "sameday_hi": round(float(s.hi), 3),
            "cumRR_0_10": round(float(c.rr), 3),
            "cum_lo": round(float(c.lo), 3),
            "cum_hi": round(float(c.hi), 3),
        })
        print(rows[-1])
    out = pd.DataFrame(rows)
    path = os.path.join(PROC, "us_contrast_sensitivity.csv")
    out.to_csv(path, index=False)
    print("wrote", path, f"(empirical 95th percentile anomaly = {p95:.2f} degC)")


if __name__ == "__main__":
    main()
