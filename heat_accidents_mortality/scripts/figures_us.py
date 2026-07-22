#!/usr/bin/env python3
"""Generate US figures (English) from processed result CSVs. One figure per file."""
import os
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
PROC = os.path.join(ROOT, "data", "processed")
FIG = os.path.join(ROOT, "output", "figures")
os.makedirs(FIG, exist_ok=True)
plt.rcParams.update({"figure.dpi": 130, "font.size": 11, "axes.grid": True,
                     "grid.alpha": 0.3, "savefig.bbox": "tight"})


def save(fig, name):
    for ext in ("png", "pdf"):
        fig.savefig(os.path.join(FIG, f"{name}.{ext}"))
    plt.close(fig)


def fig_abs():
    d = pd.read_csv(os.path.join(PROC, "us_exposure_response_abs.csv"))
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.fill_between(d.tmean, d.lo, d.hi, alpha=0.2, color="tab:red")
    ax.plot(d.tmean, d.rr, color="tab:red")
    ax.axhline(1, ls="--", color="k", lw=0.8)
    ax.set_xlabel("Daily mean temperature (\u00b0C)")
    ax.set_ylabel("Rate ratio of crash deaths (vs MMT)")
    ax.set_title("A. Absolute-temperature exposure-response\n(confounded by seasonal driving envelope)")
    save(fig, "fig1_absolute_exposure_response")


def fig_anom():
    d = pd.read_csv(os.path.join(PROC, "us_anomaly_response.csv"))
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.fill_between(d.anom, d.lo, d.hi, alpha=0.2, color="tab:orange")
    ax.plot(d.anom, d.rr, color="tab:orange")
    ax.axhline(1, ls="--", color="k", lw=0.8)
    ax.axvline(0, ls=":", color="grey", lw=0.8)
    ax.set_xlabel("Temperature anomaly vs local seasonal norm (\u00b0C)")
    ax.set_ylabel("Cumulative rate ratio (lag 0-10)")
    ax.set_title("B. Anomaly exposure-response (primary model)")
    save(fig, "fig2_anomaly_exposure_response")


def fig_lag():
    d = pd.read_csv(os.path.join(PROC, "us_lag_response.csv"))
    fig, ax = plt.subplots(figsize=(6, 4))
    x = np.arange(len(d))
    ax.errorbar(x, d.rr, yerr=[d.rr - d.lo, d.hi - d.rr], fmt="o", capsize=4,
                color="tab:blue")
    ax.axhline(1, ls="--", color="k", lw=0.8)
    ax.set_xticks(x); ax.set_xticklabels(d.window)
    ax.set_xlabel("Lag window (days)")
    ax.set_ylabel("Rate ratio for +9\u00b0C anomaly")
    ax.set_title("C. Lag structure: acute spike then displacement")
    save(fig, "fig3_lag_response")


def fig_year():
    d = pd.read_csv(os.path.join(PROC, "us_attributable_by_year.csv"))
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.bar(d.year, d.heat_an, color="tab:red", alpha=0.8)
    ax.set_xlabel("Year")
    ax.set_ylabel("Heat-attributable crash deaths")
    ax.set_title("D. Net crash deaths attributable to\nhotter-than-normal days, by year")
    save(fig, "fig4_attributable_by_year")


def fig_compare():
    att = pd.read_csv(os.path.join(PROC, "us_attributable.csv")).iloc[0]
    cdc = pd.read_csv(os.path.join(PROC, "cdc_heat_deaths.csv"))
    off = cdc[cdc.year.between(2016, 2020)].heat_deaths_X30.mean()
    fig, ax = plt.subplots(figsize=(6, 4))
    vals = [off, att.net_heat_attributable_per_year]
    labs = ["Official direct-heat\ndeaths (ICD-10 X30)", "Est. heat-attributable\ncrash deaths (this study)"]
    ax.bar(labs, vals, color=["tab:grey", "tab:red"], alpha=0.85)
    for i, v in enumerate(vals):
        ax.text(i, v, f"{v:.0f}/yr", ha="center", va="bottom")
    ax.set_ylabel("Deaths per year (US)")
    ax.set_title("E. Hidden heat burden in crashes vs\nofficially recognised heat deaths")
    save(fig, "fig5_hidden_vs_official")


def main():
    fig_abs(); fig_anom(); fig_lag(); fig_year(); fig_compare()
    print("figures written to", FIG)


if __name__ == "__main__":
    main()
