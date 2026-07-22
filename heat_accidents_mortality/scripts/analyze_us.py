#!/usr/bin/env python3
"""
US analysis: does ambient heat raise daily traffic-crash mortality (FARS)?

Time-series quasi-Poisson models on a state x day panel (2016-2022), adjusting
for state fixed effects, division-specific season (natural spline of day of
year), long-term trend and day of week:

  (A) Absolute-temperature model -> descriptive exposure-response (confounded by
      the seasonal driving-exposure envelope; peaks at mild temperatures).
  (B) Temperature-ANOMALY model (primary) -> effect of days hotter/colder than
      the local seasonal norm, decomposed over lag windows (same-day, 1-3 d,
      4-10 d). Isolates acute heat from the seasonal envelope.

All manuscript numbers derive from FARS + GHCN-Daily; nothing is hard-coded.
"""
import os
import numpy as np
import pandas as pd
from patsy import dmatrix
from model import (fit_model, cumulative_curve, bin_response, attributable, BINS, VAR_DF)

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
PROC = os.path.join(ROOT, "data", "processed")
OUT = os.path.join(ROOT, "output")
os.makedirs(OUT, exist_ok=True)

DIVISION = {
    9: 1, 23: 1, 25: 1, 33: 1, 44: 1, 50: 1,
    34: 2, 36: 2, 42: 2,
    17: 3, 18: 3, 26: 3, 39: 3, 55: 3,
    19: 4, 20: 4, 27: 4, 29: 4, 31: 4, 38: 4, 46: 4,
    10: 5, 11: 5, 12: 5, 13: 5, 24: 5, 37: 5, 45: 5, 51: 5, 54: 5,
    1: 6, 21: 6, 28: 6, 47: 6,
    5: 7, 22: 7, 40: 7, 48: 7,
    4: 8, 8: 8, 16: 8, 30: 8, 32: 8, 35: 8, 49: 8, 56: 8,
    2: 9, 6: 9, 15: 9, 41: 9, 53: 9,
}


def load_panel():
    fars = pd.read_csv(os.path.join(PROC, "fars_state_day.csv"), parse_dates=["date"])
    fars["state"] = fars.STATE.astype(int)
    temp = pd.read_csv(os.path.join(PROC, "state_day_temperature.csv"), parse_dates=["date"])
    temp["state"] = temp.state_fips.astype(int)
    states = sorted(set(fars.state) & set(temp.state))
    dates = pd.date_range(fars.date.min(), fars.date.max(), freq="D")
    grid = pd.MultiIndex.from_product([states, dates], names=["state", "date"]).to_frame(index=False)
    df = grid.merge(fars[["state", "date", "deaths"]], on=["state", "date"], how="left")
    df["deaths"] = df.deaths.fillna(0).astype(int)
    df = df.merge(temp[["state", "date", "tmean"]], on=["state", "date"], how="left")
    df = df.sort_values(["state", "date"]).reset_index(drop=True)
    df["unit"] = df.state
    df["dow"] = df.date.dt.dayofweek
    df["doy"] = df.date.dt.dayofyear
    df["division"] = df.state.map(DIVISION)
    df["t_index"] = (df.date - df.date.min()).dt.days
    n0 = len(df); df = df.dropna(subset=["tmean"]).reset_index(drop=True)
    parts = []
    for _, g in df.groupby("state"):
        g = g.sort_values("date").copy()
        B = np.asarray(dmatrix("cc(doy, df=6)", g, return_type="dataframe"))
        g["clim"] = B @ np.linalg.lstsq(B, g.tmean.values, rcond=None)[0]
        parts.append(g)
    df = pd.concat(parts).sort_values(["state", "date"]).reset_index(drop=True)
    df["anom"] = df.tmean - df.clim
    print(f"panel: {len(df):,} state-days ({n0-len(df):,} dropped for missing temp), "
          f"{df.state.nunique()} states, {int(df.deaths.sum()):,} deaths")
    return df


def confounders(df, season_df=8):
    nyears = df.date.dt.year.nunique()
    return dmatrix("C(state) + C(division):cr(doy, df=%d) + cr(t_index, df=%d) + C(dow)"
                   % (season_df, 3 * nyears), df, return_type="dataframe")


def main():
    df = load_panel()

    mabs = fit_model(df, "tmean", confounders, group="unit"); mabs["expname"] = "tmean"
    tgrid = np.linspace(*np.percentile(df.tmean, [0.5, 99.5]), 200)
    lo, hi = np.percentile(df.tmean, [1, 99])
    raw = np.array([mabs["cb"].cumulative_basis([t])[0] @ mabs["beta"] for t in tgrid])
    inr = (tgrid >= lo) & (tgrid <= hi)
    mmt = float(tgrid[np.where(inr)[0][np.argmin(raw[inr])]])
    cumulative_curve(mabs, tgrid, mmt).rename(columns={"x": "tmean"}).to_csv(
        os.path.join(PROC, "us_exposure_response_abs.csv"), index=False)

    m = fit_model(df, "anom", confounders, group="unit"); m["expname"] = "anom"
    agrid = np.linspace(*np.percentile(df.anom, [0.5, 99.5]), 200)
    cumulative_curve(m, agrid, 0.0).rename(columns={"x": "anom"}).to_csv(
        os.path.join(PROC, "us_anomaly_response.csv"), index=False)
    br = bin_response(m, 9.0, 0.0)
    br.to_csv(os.path.join(PROC, "us_lag_response.csv"), index=False)

    an_hot, sims_hot = attributable(m, "anom", ref=0.0, only="hot")
    y = m["d"].deaths.values; total = int(y.sum()); nyears = m["d"].date.dt.year.nunique()
    rr9 = cumulative_curve(m, [9.0], 0.0).iloc[0]; rr_same = br.iloc[0]

    res = {
        "total_deaths": total, "years": nyears,
        "mmt_abs_degC": round(mmt, 2), "dispersion_phi": round(float(m["phi"]), 3),
        "cumRR_anom+9C": round(float(rr9.rr), 3), "cumRR_anom+9C_lo": round(float(rr9.lo), 3),
        "cumRR_anom+9C_hi": round(float(rr9.hi), 3),
        "sameday_RR_anom+9C": round(float(rr_same.rr), 3),
        "sameday_RR_anom+9C_lo": round(float(rr_same.lo), 3),
        "sameday_RR_anom+9C_hi": round(float(rr_same.hi), 3),
        "net_heat_attributable_deaths": round(float(an_hot.sum()), 1),
        "net_heat_attributable_lo": round(float(np.percentile(sims_hot, 2.5)), 1),
        "net_heat_attributable_hi": round(float(np.percentile(sims_hot, 97.5)), 1),
        "net_heat_attributable_per_year": round(float(an_hot.sum() / nyears), 1),
        "net_heat_attributable_fraction_pct": round(float(100 * an_hot.sum() / total), 3),
    }
    for a in (3, 6, 9, 12):
        c = cumulative_curve(m, [float(a)], 0.0).iloc[0]
        res[f"net_cumRR_anom+{a}C"] = f"{c.rr:.3f} ({c.lo:.3f}-{c.hi:.3f})"

    ctrl_path = os.path.join(PROC, "driving_controls.csv")
    if os.path.exists(ctrl_path):
        c = pd.read_csv(ctrl_path, parse_dates=["date"])
        cc = df.merge(c, on="date", how="left")
        for col in ("vmt", "gasoline"):
            cc[col] = (cc[col] - cc[col].mean()) / cc[col].std()
        extra = cc[["vmt", "gasoline"]]; extra.index = df.index
        mc = fit_model(df, "anom", confounders, extra=extra, group="unit")
        s0 = bin_response(mc, 9.0, 0.0).iloc[0]; s9 = cumulative_curve(mc, [9.0], 0.0).iloc[0]
        pd.DataFrame([{"model": "with_VMT_gasoline_controls",
                       "sameday_RR_anom+9C": round(float(s0.rr), 3),
                       "sameday_RR_lo": round(float(s0.lo), 3),
                       "sameday_RR_hi": round(float(s0.hi), 3),
                       "cumRR_anom+9C": round(float(s9.rr), 3),
                       "cumRR_lo": round(float(s9.lo), 3),
                       "cumRR_hi": round(float(s9.hi), 3)}]).to_csv(
            os.path.join(PROC, "us_sensitivity_controls.csv"), index=False)
        res["sameday_RR_+9C_ctrl"] = round(float(s0.rr), 3)
        res["sameday_RR_+9C_ctrl_lo"] = round(float(s0.lo), 3)
        res["sameday_RR_+9C_ctrl_hi"] = round(float(s0.hi), 3)

    dfy = m["d"].assign(an=an_hot, year=m["d"].date.dt.year)
    per_year = dfy.groupby("year").agg(deaths=("deaths", "sum"), heat_an=("an", "sum")).reset_index()
    per_year["heat_af_pct"] = 100 * per_year.heat_an / per_year.deaths
    per_year.to_csv(os.path.join(PROC, "us_attributable_by_year.csv"), index=False)
    pd.DataFrame([res]).to_csv(os.path.join(PROC, "us_attributable.csv"), index=False)

    with open(os.path.join(OUT, "us_model_summary.txt"), "w") as f:
        f.write(f"US temperature-anomaly distributed-lag model, bins={BINS}, var_df={VAR_DF}\n")
        f.write(f"observations: {len(y):,}  deaths: {total:,}  states: {m['d'].state.nunique()}\n")
        f.write(f"quasi-Poisson dispersion phi = {m['phi']:.3f}\n\n")
        f.write("Lag-window RR for a +9C anomaly vs seasonal norm:\n")
        for _, r in br.iterrows():
            f.write(f"  {r.window:9s}: {r.rr:.3f} ({r.lo:.3f}-{r.hi:.3f})\n")
        f.write("\n")
        for k, v in res.items():
            f.write(f"{k}: {v}\n")
    print(open(os.path.join(OUT, "us_model_summary.txt")).read())


if __name__ == "__main__":
    main()
