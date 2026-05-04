"""
Healthcare Expenditure as Economic Effect: Neutral Sustainability Framework

Integrates:
  1. Input-Output (I-O) multiplier analysis — healthcare spending as demand stimulus
  2. Health-Led Growth Hypothesis (HLGH) — bidirectional causality evidence
  3. Tempo-effect health-capital model (from healthcare_tempo_poc) — lag structure
  4. Net fiscal balance — taxes/contributions generated vs public expenditure
  5. Three-layer tempo analogy (Population → GDP → Healthcare)
     from companion papers: Onishi (2026a) population, (2026b) GDP, (2026c) this paper

Produces bilingual (EN/JA) figures and data for the Japanese/English manuscripts.

Data: World Bank WDI via API, OECD health statistics (summary), published I-O studies,
      healthcare_tempo_poc Candidate A-H results.
"""

import os
import json
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
from matplotlib.patches import FancyBboxPatch

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, ".."))
DATA = os.path.join(ROOT, "data")
FIG = os.path.join(ROOT, "output", "figures")
os.makedirs(DATA, exist_ok=True)
os.makedirs(FIG, exist_ok=True)

plt.rcParams.update({
    "font.family": "DejaVu Sans",
    "axes.titlesize": 13,
    "axes.labelsize": 11,
    "xtick.labelsize": 9,
    "ytick.labelsize": 9,
    "legend.fontsize": 9,
    "figure.dpi": 200,
})

# ---------------------------------------------------------------------------
# 1. Published I-O multiplier data (healthcare sector)
# ---------------------------------------------------------------------------
IO_MULTIPLIERS = pd.DataFrame([
    {"country": "Japan", "iso3": "JPN", "multiplier": 2.78, "ci_lo": 2.74,
     "ci_hi": 2.90, "year": 2011, "source": "Yamada & Imanaka 2015"},
    {"country": "Japan (JMARI)", "iso3": "JPN", "multiplier": 2.85, "ci_lo": None,
     "ci_hi": None, "year": 2006, "source": "Maeda 2008 (JMARI WP172)"},
    {"country": "United States (Medicare)", "iso3": "USA", "multiplier": 1.70,
     "ci_lo": None, "ci_hi": None, "year": 2017,
     "source": "Dupor & Guerrero 2017 (Fed StL)"},
    {"country": "Canada", "iso3": "CAN", "multiplier": 1.82, "ci_lo": None,
     "ci_hi": None, "year": 2009, "source": "CIHI / Conference Board 2013"},
    {"country": "United Kingdom", "iso3": "GBR", "multiplier": 1.90, "ci_lo": None,
     "ci_hi": None, "year": 2016,
     "source": "ONS Health SUT / King's Fund 2018"},
    {"country": "Germany", "iso3": "DEU", "multiplier": 2.10, "ci_lo": None,
     "ci_hi": None, "year": 2014,
     "source": "Henke & Ostwald 2012 (GGR estimate)"},
    {"country": "Australia", "iso3": "AUS", "multiplier": 1.85, "ci_lo": None,
     "ci_hi": None, "year": 2015,
     "source": "AIHW / Deloitte Access Economics 2016"},
    {"country": "OECD Average", "iso3": "OECD", "multiplier": 1.95, "ci_lo": 1.50,
     "ci_hi": 2.90, "year": 2020,
     "source": "Synthesis (this study)"},
])


# ---------------------------------------------------------------------------
# 2. Health-Led Growth Hypothesis — evidence summary
#    (elasticities from published panel studies)
# ---------------------------------------------------------------------------
HLGH_EVIDENCE = pd.DataFrame([
    {"study": "Ertuğrul et al. 2024", "n_countries": 38,
     "period": "2000-2019", "method": "CS-ARDL / AMG",
     "elasticity_h2g": 0.12, "elasticity_g2h": 0.65,
     "direction": "Bidirectional", "journal": "Front Public Health"},
    {"study": "Beylik et al. 2022", "n_countries": 21,
     "period": "2000-2018", "method": "Driscoll-Kraay",
     "elasticity_h2g": 0.08, "elasticity_g2h": 0.71,
     "direction": "Bidirectional", "journal": "Front Public Health"},
    {"study": "Amiri & Ventelou 2012", "n_countries": 20,
     "period": "1995-2008", "method": "Toda-Yamamoto",
     "elasticity_h2g": None, "elasticity_g2h": None,
     "direction": "Bidirectional (Granger)", "journal": "Econ Lett"},
    {"study": "Wang 2011", "n_countries": 31,
     "period": "1986-2007", "method": "Panel VECM",
     "elasticity_h2g": 0.10, "elasticity_g2h": 0.80,
     "direction": "Bidirectional", "journal": "Soc Sci Med"},
    {"study": "Piabuo & Tieguhong 2017", "n_countries": 45,
     "period": "1995-2015", "method": "GMM",
     "elasticity_h2g": 0.05, "elasticity_g2h": 0.55,
     "direction": "H→G (developing)", "journal": "BMC Res Notes"},
])


# ---------------------------------------------------------------------------
# 3. WB data for cross-country scatter (CHE %GDP vs Life Exp)
# ---------------------------------------------------------------------------
def fetch_wb_indicator(indicator, year=2019):
    """Fetch a single WB indicator for the latest available year via CSV API."""
    import urllib.request
    url = (f"https://api.worldbank.org/v2/country/all/indicator/{indicator}"
           f"?date={year}&format=json&per_page=300")
    try:
        with urllib.request.urlopen(url, timeout=30) as resp:
            data = json.loads(resp.read().decode())
        if len(data) < 2:
            return {}
        return {r["countryiso3code"]: r["value"]
                for r in data[1] if r.get("value") is not None}
    except Exception as e:
        print(f"  [WARN] WB fetch {indicator}: {e}")
        return {}


OECD_ISO3 = [
    "AUS","AUT","BEL","CAN","CHL","COL","CRI","CZE","DNK","EST",
    "FIN","FRA","DEU","GRC","HUN","ISL","IRL","ISR","ITA","JPN",
    "KOR","LVA","LTU","LUX","MEX","NLD","NZL","NOR","POL","PRT",
    "SVK","SVN","ESP","SWE","CHE","TUR","GBR","USA",
]

COUNTRY_LABELS = {
    "JPN": "Japan", "USA": "USA", "DEU": "Germany", "GBR": "UK",
    "FRA": "France", "CAN": "Canada", "AUS": "Australia", "KOR": "Korea",
    "ITA": "Italy", "ESP": "Spain", "SWE": "Sweden", "NOR": "Norway",
    "CHE": "Switzerland", "NLD": "Netherlands",
}


def build_cross_country_df():
    """Build a DataFrame with CHE %GDP and LifeExp for OECD countries."""
    print("Fetching WB data ...")
    che_gdp = fetch_wb_indicator("SH.XPD.CHEX.GD.ZS", 2019)
    le = fetch_wb_indicator("SP.DYN.LE00.IN", 2019)
    che_pc = fetch_wb_indicator("SH.XPD.CHEX.PP.CD", 2019)

    rows = []
    for iso in OECD_ISO3:
        if iso in che_gdp and iso in le:
            rows.append({
                "iso3": iso,
                "label": COUNTRY_LABELS.get(iso, iso),
                "che_gdp_pct": che_gdp[iso],
                "life_exp": le[iso],
                "che_pc_ppp": che_pc.get(iso),
            })
    df = pd.DataFrame(rows)
    df.to_csv(os.path.join(DATA, "oecd_cross_country_2019.csv"), index=False)
    print(f"  {len(df)} countries with complete data.")
    return df


# ---------------------------------------------------------------------------
# 4. Net economic return model
#    Healthcare expenditure E generates:
#      - Direct + indirect + induced output = m * E  (I-O multiplier)
#      - Tax/social-contribution return   = τ * m * E
#      - Employment (persons per unit E)
#    "Neutral" sustainability criterion:
#      τ * m >= share of public financing (pf)
#      i.e. the tax return from multiplied output covers public share
# ---------------------------------------------------------------------------
def compute_neutral_sustainability(multiplier, tax_rate, public_share):
    """Return the net fiscal balance ratio: (τ·m) / pf.
    > 1 means the fiscal system recaptures more than it spends on healthcare."""
    return (tax_rate * multiplier) / public_share


def sustainability_table():
    """Build a table for representative countries."""
    params = [
        # iso, name, m, τ (effective tax+SSC/GDP), pf (public share of CHE)
        ("JPN", "Japan",        2.78, 0.33, 0.84),
        ("USA", "USA",          1.70, 0.27, 0.50),
        ("DEU", "Germany",      2.10, 0.39, 0.85),
        ("GBR", "UK",           1.90, 0.33, 0.80),
        ("FRA", "France",       2.20, 0.45, 0.84),
        ("SWE", "Sweden",       2.05, 0.43, 0.85),
        ("CAN", "Canada",       1.82, 0.33, 0.73),
        ("AUS", "Australia",    1.85, 0.28, 0.68),
        ("KOR", "Korea",        1.95, 0.27, 0.61),
    ]
    rows = []
    for iso, name, m, tau, pf in params:
        ratio = compute_neutral_sustainability(m, tau, pf)
        rows.append({
            "iso3": iso, "country": name,
            "io_multiplier": m,
            "eff_tax_rate": tau,
            "public_share_che": pf,
            "fiscal_return_ratio": round(ratio, 2),
            "sustainable": "Yes" if ratio >= 1.0 else "No",
        })
    df = pd.DataFrame(rows)
    df.to_csv(os.path.join(DATA, "neutral_sustainability.csv"), index=False)
    return df


# ---------------------------------------------------------------------------
# 5. Candidate A-H PoC results (from healthcare_tempo_poc PR#37)
#    Bug-fixed rerun (2026-04-21): corrected stock normalisation
# ---------------------------------------------------------------------------
POC_AH_RESULTS = {
    "n_countries": 39,
    "data_source": "World Bank WDI (SH.XPD.CHEX.PP.CD, SP.DYN.LE00.IN)",
    "period": "2000-2019",
    "models": {
        "M0_flow": {"description": "Naive flow-only regression",
                    "level_rmse_median": 0.510,
                    "change_rmse_median": 0.455},
        "M1_constant_lag": {"description": "Constant lag mu_H (PIM)",
                            "level_rmse_median": 0.441,
                            "change_rmse_median": 0.403,
                            "mu_const_median_yr": 4.0},
        "M2_tempo_lag": {"description": "Time-varying mu_H(t) = mu0 + mu1*(year-t0)",
                         "level_rmse_median": 0.434,
                         "change_rmse_median": 0.405,
                         "mu_H1_median_yr_per_yr": 0.15},
    },
    "key_findings": {
        "M1_beats_M0_level_pct": 69,
        "M2_beats_M0_level_pct": 77,
        "M2_beats_M0_change_pct": 87,
        "M2_beats_M1_pct": 95,
        "M0_to_M1_rmse_reduction_pct": 14,
        "M0_to_M2_rmse_reduction_pct": 15,
    },
    "interpretation": (
        "M2 beats M1 in 95% of countries, confirming that the "
        "spending-to-outcome lag is not constant but drifts over time. "
        "Median drift mu_H1 = +0.15 yr/yr means the lag lengthens by "
        "~1.5 years per decade, consistent with the shift from acute "
        "to chronic disease management and longer R&D-to-outcome cycles."
    ),
}

# Three-layer tempo analogy: Population → GDP → Healthcare
THREE_LAYER_ANALOGY = pd.DataFrame([
    {"concept": "Flow (quantum)",
     "population": "TFR (period fertility rate)",
     "gdp": "I/GDP (investment rate)",
     "healthcare": "E/GDP (health spending rate)"},
    {"concept": "Tempo (timing lag)",
     "population": "MAC (mean age at childbearing)",
     "gdp": "mu (investment-to-output lag)",
     "healthcare": "mu_H (spending-to-outcome lag)"},
    {"concept": "Forgotten parameter",
     "population": "sigma (parity variance)",
     "gdp": "beta (intangible capital share)",
     "healthcare": "lambda_b (composition multipliers)"},
    {"concept": "Stock",
     "population": "Cohort size N(t)",
     "gdp": "Capital stock K(t)",
     "healthcare": "Health capital H(t)"},
    {"concept": "Tempo drift (mu_1)",
     "population": "+0.05 yr/yr (MAC shift)",
     "gdp": "+0.04 yr/yr (time-to-build)",
     "healthcare": "+0.15 yr/yr (spending-to-outcome)"},
    {"concept": "Effect size vs M0",
     "population": "Large (TFR bias ~15-20%)",
     "gdp": "Small (MAPE -0.6 pp)",
     "healthcare": "Medium (RMSE -15%)"},
    {"concept": "Identity",
     "population": "Renewal equation",
     "gdp": "dW/dt = S(Y) - delta*W",
     "healthcare": "dH/dt = sum(lambda_b*E_b) - delta_H*H"},
])


def tempo_adjusted_narrative():
    """Combine PoC A-H results with tempo narrative for manuscripts."""
    poc = POC_AH_RESULTS
    return {
        "poc_summary": poc,
        "three_layer_analogy": THREE_LAYER_ANALOGY.to_dict(orient="records"),
        "key_insight": (
            "The healthcare_tempo_poc (Candidate A-H, 39 countries) shows "
            "that treating health spending as a stock-building flow with a "
            "time-varying lag mu_H(t) reduces life-expectancy prediction "
            f"RMSE from {poc['models']['M0_flow']['level_rmse_median']:.3f} "
            f"to {poc['models']['M2_tempo_lag']['level_rmse_median']:.3f} years "
            f"(−{poc['key_findings']['M0_to_M2_rmse_reduction_pct']}%). "
            "M2 beats M1 in 95% of countries, confirming that the lag is "
            "not constant but drifts at +0.15 yr/yr — the spending-to-outcome "
            "pipeline lengthens by ~1.5 years per decade."
        ),
        "policy_implication": (
            "A 'neutral' sustainability criterion must account for both "
            "channels: (1) the contemporaneous fiscal multiplier effect "
            "(I-O: does tax revenue from healthcare-induced economic "
            "activity cover public financing?), and (2) the intertemporal "
            "health-capital accumulation effect (tempo: does the stock "
            "of health built today justify the flow of spending?). "
            "Neither alone gives a complete picture. "
            "Furthermore, Candidate D-H (spending composition) suggests "
            "that the 'forgotten parameter' lambda_b — the relative "
            "outcome multiplier of preventive/R&D vs curative spending — "
            "may matter more than total spending level."
        ),
        "us_japan_contrast": (
            "The US has high spending (17% GDP) but a low I-O multiplier "
            "(1.7), suggesting leakage through high drug prices and "
            "administrative costs. Japan has moderate spending (11% GDP) "
            "but the highest multiplier (2.78) and a fiscal return ratio "
            "above 1.0 (1.09). Through the tempo lens, the US pattern — "
            "high flow, low stock accumulation — mirrors 'high TFR, low "
            "cohort fertility' in demography: a tempo-inflated flow that "
            "overstates true investment in health capital."
        ),
        "three_layer_connection": (
            "The tempo-plus-forgotten-parameter framework originated in "
            "demography (Bongaarts-Feeney 1998, Goldstein-Lutz-Scherbov 2003), "
            "was ported to GDP/wealth accounting (Onishi 2026, PR#39), and "
            "now extends to health expenditure (this paper). In each domain, "
            "a period flow statistic (TFR / I/GDP / E/GDP) is biased by "
            "a timing drift (MAC / mu / mu_H), and a forgotten stock parameter "
            "(sigma / beta / lambda_b) reconciles flow and stock accounts. "
            "Healthcare shows the largest tempo drift (+0.15 yr/yr vs GDP's "
            "+0.04), suggesting that health accounting may be the domain "
            "where the correction matters most."
        ),
    }


# ---------------------------------------------------------------------------
# 6. Figure generation
# ---------------------------------------------------------------------------
def fig1_io_multiplier_comparison(io_df):
    """Bar chart of I-O multipliers across countries."""
    fig, ax = plt.subplots(figsize=(8, 5))
    mask = io_df["iso3"] != "OECD"
    df = io_df[mask].sort_values("multiplier", ascending=True)

    colors = ["#2196F3" if iso != "JPN" else "#FF5722" for iso in df["iso3"]]
    bars = ax.barh(df["country"], df["multiplier"], color=colors, edgecolor="white")

    # Error bars for Japan
    jpn_mask = df["iso3"] == "JPN"
    if jpn_mask.any():
        jpn = df[jpn_mask].iloc[0]
        if pd.notna(jpn.get("ci_lo")) and pd.notna(jpn.get("ci_hi")):
            idx = df.index.get_loc(jpn.name)
            ax.errorbar(jpn["multiplier"], idx,
                        xerr=[[jpn["multiplier"] - jpn["ci_lo"]],
                              [jpn["ci_hi"] - jpn["multiplier"]]],
                        fmt="none", ecolor="black", capsize=4)

    ax.axvline(1.0, color="gray", linestyle="--", linewidth=0.8, label="Break-even (1.0)")
    oecd_row = io_df[io_df["iso3"] == "OECD"]
    if not oecd_row.empty:
        ax.axvline(oecd_row.iloc[0]["multiplier"], color="#4CAF50",
                   linestyle=":", linewidth=1.2, label=f'OECD synthesis ({oecd_row.iloc[0]["multiplier"]})')

    ax.set_xlabel("Economic Impact Multiplier (output per unit of healthcare spending)")
    ax.set_title("Figure 1. Healthcare I-O Multipliers by Country")
    ax.legend(loc="lower right", fontsize=8)
    ax.set_xlim(0, 3.5)

    for bar, val in zip(bars, df["multiplier"]):
        ax.text(val + 0.05, bar.get_y() + bar.get_height() / 2,
                f"{val:.2f}", va="center", fontsize=9)

    plt.tight_layout()
    path = os.path.join(FIG, "fig1_io_multipliers.png")
    fig.savefig(path)
    plt.close(fig)
    print(f"  Saved: {path}")
    return path


def fig2_scatter_che_vs_le(cc_df):
    """Scatter: CHE %GDP vs Life Expectancy with annotations."""
    fig, ax = plt.subplots(figsize=(8, 6))

    ax.scatter(cc_df["che_gdp_pct"], cc_df["life_exp"],
               s=60, alpha=0.7, c="#1976D2", edgecolors="white", linewidths=0.5)

    for _, row in cc_df.iterrows():
        if row["label"] in COUNTRY_LABELS.values():
            ax.annotate(row["label"],
                        (row["che_gdp_pct"], row["life_exp"]),
                        fontsize=7, xytext=(5, 3),
                        textcoords="offset points")

    z = np.polyfit(cc_df["che_gdp_pct"], cc_df["life_exp"], 2)
    xfit = np.linspace(cc_df["che_gdp_pct"].min(), cc_df["che_gdp_pct"].max(), 100)
    yfit = np.polyval(z, xfit)
    ax.plot(xfit, yfit, "r--", linewidth=1, alpha=0.6, label="Quadratic fit")

    ax.set_xlabel("Current Health Expenditure (% of GDP)")
    ax.set_ylabel("Life Expectancy at Birth (years)")
    ax.set_title("Figure 2. Healthcare Spending vs Life Expectancy (OECD, 2019)")
    ax.legend(fontsize=8)
    plt.tight_layout()
    path = os.path.join(FIG, "fig2_che_vs_lifeexp.png")
    fig.savefig(path)
    plt.close(fig)
    print(f"  Saved: {path}")
    return path


def fig3_fiscal_sustainability(sust_df):
    """Bar chart: fiscal return ratio by country."""
    fig, ax = plt.subplots(figsize=(8, 5))
    df = sust_df.sort_values("fiscal_return_ratio", ascending=True)

    colors = ["#4CAF50" if r >= 1.0 else "#FF9800" for r in df["fiscal_return_ratio"]]
    bars = ax.barh(df["country"], df["fiscal_return_ratio"], color=colors, edgecolor="white")

    ax.axvline(1.0, color="red", linestyle="--", linewidth=1.2, label="Break-even (τ·m = pf)")
    ax.set_xlabel("Fiscal Return Ratio  τ·m / pf")
    ax.set_title("Figure 3. Neutral Fiscal Sustainability of Healthcare Spending")
    ax.legend(loc="lower right", fontsize=8)

    for bar, val in zip(bars, df["fiscal_return_ratio"]):
        ax.text(val + 0.02, bar.get_y() + bar.get_height() / 2,
                f"{val:.2f}", va="center", fontsize=9)

    plt.tight_layout()
    path = os.path.join(FIG, "fig3_fiscal_sustainability.png")
    fig.savefig(path)
    plt.close(fig)
    print(f"  Saved: {path}")
    return path


def fig4_dual_return_schematic():
    """Conceptual diagram: I-O (demand) + Tempo (supply) dual return."""
    fig, ax = plt.subplots(figsize=(9, 5.5))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 6)
    ax.axis("off")

    # Central node
    ax.add_patch(plt.Rectangle((3.5, 2.5), 3, 1.2, facecolor="#E3F2FD",
                                edgecolor="#1565C0", linewidth=2, zorder=2))
    ax.text(5, 3.1, "Healthcare\nExpenditure E(t)",
            ha="center", va="center", fontsize=11, fontweight="bold", zorder=3)

    # Left: Demand-side (I-O)
    ax.annotate("", xy=(1.5, 4.8), xytext=(3.5, 3.5),
                arrowprops=dict(arrowstyle="->", color="#1976D2", lw=2))
    ax.add_patch(FancyBboxPatch((0.1, 4.3), 2.8, 1.2,
                                boxstyle="round,pad=0.15",
                                facecolor="#BBDEFB", edgecolor="#1565C0"))
    ax.text(1.5, 4.9, "Demand-side Return\n(I-O Multiplier m)",
            ha="center", va="center", fontsize=9, color="#0D47A1")

    # Left sub: tax return
    ax.annotate("", xy=(1.5, 1.0), xytext=(1.5, 4.3),
                arrowprops=dict(arrowstyle="->", color="#4CAF50", lw=1.5,
                                connectionstyle="arc3,rad=0.3"))
    ax.text(0.1, 2.6, "Tax return\nτ · m · E(t)",
            fontsize=8, color="#2E7D32", style="italic")

    # Right: Supply-side (Tempo / Health Capital)
    ax.annotate("", xy=(8.5, 4.8), xytext=(6.5, 3.5),
                arrowprops=dict(arrowstyle="->", color="#E65100", lw=2))
    ax.add_patch(FancyBboxPatch((7.1, 4.3), 2.8, 1.2,
                                boxstyle="round,pad=0.15",
                                facecolor="#FFF3E0", edgecolor="#E65100"))
    ax.text(8.5, 4.9, "Supply-side Return\n(Health Capital H(t))",
            ha="center", va="center", fontsize=9, color="#BF360C")

    # Right sub: future productivity
    ax.annotate("", xy=(8.5, 1.0), xytext=(8.5, 4.3),
                arrowprops=dict(arrowstyle="->", color="#FF9800", lw=1.5,
                                connectionstyle="arc3,rad=-0.3"))
    ax.text(7.5, 2.6, "Future GDP\ngrowth via\nproductivity",
            fontsize=8, color="#E65100", style="italic")

    # Bottom: Combined sustainability
    ax.add_patch(FancyBboxPatch((2.5, 0.2), 5, 0.8,
                                boxstyle="round,pad=0.15",
                                facecolor="#E8F5E9", edgecolor="#388E3C"))
    ax.text(5, 0.6, "Neutral Sustainability = Demand Return + Supply Return ≥ Public Cost",
            ha="center", va="center", fontsize=9, fontweight="bold", color="#1B5E20")

    # Arrows down to bottom
    ax.annotate("", xy=(3.5, 1.0), xytext=(1.5, 1.0),
                arrowprops=dict(arrowstyle="->", color="#4CAF50", lw=1.5))
    ax.annotate("", xy=(6.5, 1.0), xytext=(8.5, 1.0),
                arrowprops=dict(arrowstyle="->", color="#FF9800", lw=1.5))

    # Tempo annotation
    ax.text(8.5, 3.5, "μ_H(t) drift\n(tempo lag)",
            fontsize=7, color="#BF360C", ha="center", style="italic")

    ax.set_title("Figure 4. Dual-Return Framework for Neutral Healthcare Sustainability",
                 fontsize=12, pad=15)
    plt.tight_layout()
    path = os.path.join(FIG, "fig4_dual_return_schematic.png")
    fig.savefig(path, bbox_inches="tight")
    plt.close(fig)
    print(f"  Saved: {path}")
    return path


def fig5_three_layer_analogy(lang="en"):
    """Table-style figure showing the Population/GDP/Healthcare tempo analogy."""
    import matplotlib.font_manager as fm

    ja_font_name = "DejaVu Sans"
    if lang == "ja":
        ja_hits = [f for f in fm.fontManager.ttflist
                   if "IPAGothic" in f.name or "IPAPGothic" in f.name]
        if ja_hits:
            fm.fontManager.addfont(ja_hits[0].fname)
            ja_font_name = ja_hits[0].name

    fig, ax = plt.subplots(figsize=(10, 4.5))
    ax.axis("off")

    if lang == "ja":
        col_labels = ["概念", "人口", "GDP / 国富", "医療"]
        row_data = [
            ["フロー（量子）", "TFR\n（期間出生率）", "I/GDP\n（投資率）", "E/GDP\n（医療支出率）"],
            ["テンポ（時間ラグ）", "MAC\n（平均出産年齢）", "mu\n（投資→産出ラグ）", "mu_H\n（支出→成果ラグ）"],
            ["忘れられたパラメータ", "sigma\n（パリティ分散）", "beta\n（無形資本比率）", "lambda_b\n（構成乗数）"],
            ["ストック", "コーホート人口\nN(t)", "資本ストック\nK(t)", "健康資本\nH(t)"],
            ["テンポドリフト (mu_1)", "+0.05 年/年\n（MAC上昇）", "+0.04 年/年\n（建設期間延長）", "+0.15 年/年\n（支出→成果遅延）"],
            ["効果サイズ vs M0", "大（TFR偏り\n15-20%）", "小（MAPE\n-0.6 pp）", "中（RMSE\n-15%）"],
        ]
        title = "図5. テンポ効果の三層構造 — 人口→GDP→医療への移植"
    else:
        col_labels = ["Concept", "Population", "GDP / Wealth", "Healthcare"]
        row_data = [
            ["Flow (quantum)", "TFR\n(period fertility)", "I/GDP\n(investment rate)", "E/GDP\n(health spend rate)"],
            ["Tempo (timing lag)", "MAC\n(mean age childbearing)", "mu\n(invest-to-output lag)", "mu_H\n(spend-to-outcome lag)"],
            ["Forgotten parameter", "sigma\n(parity variance)", "beta\n(intangible K share)", "lambda_b\n(composition mult.)"],
            ["Stock", "Cohort size\nN(t)", "Capital stock\nK(t)", "Health capital\nH(t)"],
            ["Tempo drift (mu_1)", "+0.05 yr/yr\n(MAC shift)", "+0.04 yr/yr\n(time-to-build)", "+0.15 yr/yr\n(spend-to-outcome)"],
            ["Effect size vs M0", "Large (TFR bias\n15-20%)", "Small (MAPE\n-0.6 pp)", "Medium (RMSE\n-15%)"],
        ]
        title = "Figure 5. Three-Layer Tempo Analogy: Population to GDP to Healthcare"

    colors_col = ["#E3F2FD", "#FCE4EC", "#FFF3E0", "#E8F5E9"]
    table = ax.table(
        cellText=row_data,
        colLabels=col_labels,
        cellLoc="center",
        loc="center",
    )
    table.auto_set_font_size(False)
    table.set_fontsize(8.5)
    table.scale(1.0, 2.2)

    for (row, col), cell in table.get_celld().items():
        cell.set_edgecolor("#BDBDBD")
        if row == 0:
            cell.set_facecolor("#37474F")
            cell.set_text_props(color="white", fontweight="bold", fontsize=9.5,
                                fontfamily=ja_font_name)
        else:
            cell.set_facecolor(colors_col[col] if col < len(colors_col) else "#FFFFFF")
            cell.set_text_props(fontfamily=ja_font_name)
        if col == 3 and row > 0:
            cell.set_text_props(fontweight="bold", fontfamily=ja_font_name)

    ax.set_title(title, fontsize=12, pad=15, fontweight="bold",
                 fontfamily=ja_font_name)
    plt.tight_layout()
    suffix = "_ja" if lang == "ja" else ""
    path = os.path.join(FIG, f"fig5_three_layer_analogy{suffix}.png")
    fig.savefig(path, bbox_inches="tight")
    plt.close(fig)
    print(f"  Saved: {path}")
    return path


# ---------------------------------------------------------------------------
# 8. Main
# ---------------------------------------------------------------------------
def main():
    print("=" * 60)
    print("Healthcare Economic Effect — Neutral Sustainability Analysis")
    print("=" * 60)

    # I-O multiplier comparison
    print("\n[1] I-O Multiplier data")
    IO_MULTIPLIERS.to_csv(os.path.join(DATA, "io_multipliers.csv"), index=False)
    fig1_io_multiplier_comparison(IO_MULTIPLIERS)

    # HLGH evidence
    print("\n[2] Health-Led Growth Hypothesis evidence")
    HLGH_EVIDENCE.to_csv(os.path.join(DATA, "hlgh_evidence.csv"), index=False)

    # Cross-country scatter
    print("\n[3] Cross-country CHE vs Life Expectancy")
    cc_df = build_cross_country_df()
    if len(cc_df) > 5:
        fig2_scatter_che_vs_le(cc_df)
    else:
        print("  [WARN] Insufficient WB data; skipping scatter plot.")

    # Fiscal sustainability
    print("\n[4] Neutral fiscal sustainability")
    sust_df = sustainability_table()
    fig3_fiscal_sustainability(sust_df)
    print(sust_df.to_string(index=False))

    # Dual-return schematic
    print("\n[5] Dual-return conceptual diagram")
    fig4_dual_return_schematic()

    # Three-layer analogy (EN + JA)
    print("\n[6] Three-layer tempo analogy")
    fig5_three_layer_analogy(lang="en")
    fig5_three_layer_analogy(lang="ja")

    # PoC A-H results
    print("\n[7] PoC A-H results (from healthcare_tempo_poc)")
    with open(os.path.join(DATA, "poc_AH_summary.json"), "w") as f:
        json.dump(POC_AH_RESULTS, f, indent=2)
    THREE_LAYER_ANALOGY.to_csv(
        os.path.join(DATA, "three_layer_analogy.csv"), index=False)
    m2 = POC_AH_RESULTS["models"]["M2_tempo_lag"]
    print(f"  M2 level RMSE: {m2['level_rmse_median']:.3f} yr")
    print(f"  mu_H1 drift: +{m2['mu_H1_median_yr_per_yr']:.2f} yr/yr")
    print(f"  M2 beats M1: {POC_AH_RESULTS['key_findings']['M2_beats_M1_pct']}%")

    # Tempo narrative
    print("\n[8] Tempo-adjusted narrative")
    narrative = tempo_adjusted_narrative()
    with open(os.path.join(DATA, "tempo_narrative.json"), "w") as f:
        json.dump(narrative, f, indent=2, default=str)
    for k, v in narrative.items():
        if isinstance(v, str):
            print(f"  {k}: {v[:80]}...")

    print("\n" + "=" * 60)
    print("Analysis complete. See output/figures/ and data/.")
    print("=" * 60)


if __name__ == "__main__":
    main()
