"""Produce:
- Fig 3: six-panel W_PIM vs CWON PCA trajectories (selected countries).
- Fig 5: conceptual diagram of the population <-> GDP tempo correspondence.
- Table 1: M0-M4 parameter distributions and test metrics (CSV + tex).
- Table 2: population <-> GDP correspondence table (CSV + tex).

Writes to ../figures/ and ../tables/.
"""
from __future__ import annotations

import json
import os
import shutil

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import matplotlib.patches as patches
from matplotlib import font_manager

# Register a Japanese font so that JA figures render correctly.
for path in ("/usr/share/fonts/opentype/ipafont-gothic/ipag.ttf",
             "/usr/share/fonts/truetype/fonts-japanese-gothic.ttf"):
    if os.path.exists(path):
        font_manager.fontManager.addfont(path)
        plt.rcParams["font.sans-serif"] = ["IPAGothic", "DejaVu Sans"]
        break

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, ".."))
FIG = os.path.join(ROOT, "figures")
TAB = os.path.join(ROOT, "tables")
DATA = os.path.join(ROOT, "data")
os.makedirs(FIG, exist_ok=True)
os.makedirs(TAB, exist_ok=True)

CWON_TS = "/home/ubuntu/repos/wip_cwon/gdp_cwon_integration/data/cwon_integration_ts.json"


def make_fig3(lang: str = "en"):
    with open(CWON_TS) as fh:
        ts = json.load(fh)
    highlight = [
        "United States", "Japan", "Germany", "Republic of Korea",
        "Netherlands", "Israel",
    ]
    labels = {
        "en": {
            "title": "Fig. 3. Reconstructed PIM stock vs. CWON produced capital",
            "pim": "PIM $K_{tang}+\\beta K_{intan}$ (demeaned log)",
            "cwon": "CWON PCA (demeaned log)",
            "year": "Year",
            "y": "log stock (within-country demeaned)",
        },
        "ja": {
            "title": "図3. PIM資本ストックとCWON生産資本の軌跡比較",
            "pim": r"PIM $K_{tang}+\beta K_{intan}$（国内平均を除去した対数）",
            "cwon": "CWON PCA（国内平均を除去した対数）",
            "year": "年",
            "y": "対数ストック（国ごとに平均を除去）",
        },
    }[lang]
    fig, axes = plt.subplots(2, 3, figsize=(12, 7), sharex=True)
    for ax, country in zip(axes.flat, highlight):
        if country not in ts:
            ax.set_visible(False)
            continue
        d = ts[country]
        years = np.array(d["years"])
        pim = np.array(d["pim_produced_plus_intan"], dtype=float)
        pca = np.array(d["cwon_pca"], dtype=float)
        mask = np.isfinite(pim) & np.isfinite(pca) & (pim > 0) & (pca > 0)
        if mask.sum() < 3:
            ax.set_visible(False)
            continue
        lp = np.log(pim[mask]); lc = np.log(pca[mask])
        lp_d = lp - lp.mean(); lc_d = lc - lc.mean()
        ax.plot(years[mask], lp_d, "o-", color="#c44e52", ms=3,
                label=labels["pim"])
        ax.plot(years[mask], lc_d, "s-", color="#4c72b0", ms=3,
                label=labels["cwon"])
        ax.set_title(country, fontsize=10)
        ax.grid(alpha=0.3)
    for ax in axes[-1]:
        ax.set_xlabel(labels["year"])
    for ax in axes[:, 0]:
        ax.set_ylabel(labels["y"], fontsize=8)
    handles, lbls = axes[0, 0].get_legend_handles_labels()
    fig.legend(handles, lbls, loc="lower center", ncol=2,
               bbox_to_anchor=(0.5, -0.02))
    fig.suptitle(labels["title"], y=0.99)
    plt.tight_layout(rect=[0, 0.03, 1, 0.97])
    out = os.path.join(FIG, f"fig3_trajectories_{lang}.png")
    plt.savefig(out, dpi=180, bbox_inches="tight")
    plt.close()
    print("wrote", out)


def make_fig5(lang: str = "en"):
    labels = {
        "en": {
            "title": "Fig. 5. Population–GDP tempo correspondence",
            "pop_flow": "Fertility flow\n$B(t)$",
            "pop_stock": "Population stock\n$N(t)$",
            "gdp_flow": "Investment flow\n$I(t)$",
            "gdp_stock": "Capital stock\n$W(t)$",
            "mac": "Quantum: $TFR$\nTempo: $MAC(t)$",
            "mu": "Quantum: $I(t)$\nTempo: $\\mu(t)$",
            "sigma": "Forgotten $\\sigma$",
            "beta": "Forgotten $\\beta$",
            "arrow_demog": "demography",
            "arrow_capital": "capital",
            "balance": "$dN/dt = B - dN$",
            "balance_c": "$dW/dt = I - \\delta W$",
        },
        "ja": {
            "title": "図5. 人口・GDPテンポ対応関係",
            "pop_flow": "出生フロー\n$B(t)$",
            "pop_stock": "人口ストック\n$N(t)$",
            "gdp_flow": "投資フロー\n$I(t)$",
            "gdp_stock": "資本ストック\n$W(t)$",
            "mac": "量: $TFR$\nテンポ: $MAC(t)$",
            "mu": "量: $I(t)$\nテンポ: $\\mu(t)$",
            "sigma": "忘却 $\\sigma$",
            "beta": "忘却 $\\beta$",
            "arrow_demog": "人口",
            "arrow_capital": "資本",
            "balance": "$dN/dt = B - dN$",
            "balance_c": "$dW/dt = I - \\delta W$",
        },
    }[lang]

    fig, ax = plt.subplots(figsize=(10, 5.5))
    ax.set_xlim(0, 10); ax.set_ylim(0, 6)
    ax.set_axis_off()

    def box(x, y, w, h, text, facecolor, fontsize=10):
        r = patches.FancyBboxPatch(
            (x - w / 2, y - h / 2), w, h,
            boxstyle="round,pad=0.08",
            facecolor=facecolor, edgecolor="black", lw=1.2)
        ax.add_patch(r)
        ax.text(x, y, text, ha="center", va="center", fontsize=fontsize)

    # Demography row (top)
    box(2, 4.7, 1.8, 0.9, labels["pop_flow"], "#e0ecff")
    box(5, 4.7, 1.8, 0.9, labels["mac"], "#d6ebd8")
    box(8, 4.7, 1.8, 0.9, labels["pop_stock"], "#e0ecff")
    ax.annotate("", xy=(4.1, 4.7), xytext=(2.9, 4.7),
                arrowprops=dict(arrowstyle="->", lw=1.5))
    ax.annotate("", xy=(7.1, 4.7), xytext=(5.9, 4.7),
                arrowprops=dict(arrowstyle="->", lw=1.5))
    ax.text(8, 4.1, labels["balance"], ha="center", fontsize=9,
            style="italic")
    ax.text(0.6, 4.7, labels["arrow_demog"], ha="center", va="center",
            fontsize=11, fontweight="bold")

    # Capital row (bottom)
    box(2, 1.7, 1.8, 0.9, labels["gdp_flow"], "#ffe6d6")
    box(5, 1.7, 1.8, 0.9, labels["mu"], "#d6ebd8")
    box(8, 1.7, 1.8, 0.9, labels["gdp_stock"], "#ffe6d6")
    ax.annotate("", xy=(4.1, 1.7), xytext=(2.9, 1.7),
                arrowprops=dict(arrowstyle="->", lw=1.5))
    ax.annotate("", xy=(7.1, 1.7), xytext=(5.9, 1.7),
                arrowprops=dict(arrowstyle="->", lw=1.5))
    ax.text(8, 1.1, labels["balance_c"], ha="center", fontsize=9,
            style="italic")
    ax.text(0.6, 1.7, labels["arrow_capital"], ha="center", va="center",
            fontsize=11, fontweight="bold")

    # Forgotten parameters (small boxes to the side)
    box(9.3, 3.8, 1.1, 0.45, labels["sigma"], "#fbe7a2", fontsize=9)
    box(9.3, 2.6, 1.1, 0.45, labels["beta"], "#fbe7a2", fontsize=9)
    ax.annotate("", xy=(8.6, 4.5), xytext=(9.0, 4.0),
                arrowprops=dict(arrowstyle="->", lw=1.0, ls=":"))
    ax.annotate("", xy=(8.6, 1.9), xytext=(9.0, 2.4),
                arrowprops=dict(arrowstyle="->", lw=1.0, ls=":"))

    ax.set_title(labels["title"], fontsize=12)
    out = os.path.join(FIG, f"fig5_concept_{lang}.png")
    plt.tight_layout()
    plt.savefig(out, dpi=180, bbox_inches="tight")
    plt.close()
    print("wrote", out)


def make_tables():
    fair = pd.read_csv(os.path.join(DATA, "fair_eval.csv"))
    oos = pd.read_csv(os.path.join(DATA, "oos.csv"))
    boot = pd.read_csv(os.path.join(DATA, "bootstrap_ci.csv"))

    # Table 1: per-model metrics.
    def q(s, qv): return float(np.nanquantile(s, qv))
    rows = []
    for name in ("M0", "M1", "M2", "M3", "M4"):
        brmse = fair[f"{name}_B_rmse"]
        amape = fair[f"{name}_A_mape"]
        oo = oos[f"{name}_oos_mape"] if f"{name}_oos_mape" in oos.columns \
            else pd.Series([np.nan])
        rows.append({
            "Model": name,
            "Description": {
                "M0": "Instant PIM (Solow baseline)",
                "M1": "Constant lag $\\mu^\\star$",
                "M2": "Time-varying lag $\\mu(t)=\\mu_0+\\mu_1(t-t_0)$",
                "M3": "Instant PIM + intangible $K_I$",
                "M4": "Joint tempo+intangible (GDP \\& CWON)",
            }[name],
            "Growth RMSE median (pp)": round(np.nanmedian(brmse), 3),
            "Growth RMSE IQR (pp)": (
                f"[{q(brmse, 0.25):.2f}, {q(brmse, 0.75):.2f}]"),
            "Level MAPE median (\\%)": round(np.nanmedian(amape), 3),
            "OOS MAPE median (\\%)": round(np.nanmedian(oo), 3),
        })
    t1 = pd.DataFrame(rows)
    t1.to_csv(os.path.join(TAB, "table1_model_metrics.csv"), index=False)
    print("wrote table1")

    # Table 2: population <-> GDP correspondence.
    t2_rows = [
        {"Concept": "Flow",
         "Population (Bongaarts-Feeney, 1998)": "Births $B(t)$",
         "Capital (this paper)": "Investment $I(t)$"},
        {"Concept": "Stock",
         "Population (Bongaarts-Feeney, 1998)": "Population $N(t)$",
         "Capital (this paper)": "Reproducible capital $W(t)$"},
        {"Concept": "Quantum",
         "Population (Bongaarts-Feeney, 1998)": "Total Fertility Rate $TFR$",
         "Capital (this paper)": "Investment rate $I/Y$"},
        {"Concept": "Tempo",
         "Population (Bongaarts-Feeney, 1998)": "Mean age at childbearing $MAC(t)$",
         "Capital (this paper)": "Time-to-build $\\mu(t)$"},
        {"Concept": "Bongaarts-Feeney adjustment",
         "Population (Bongaarts-Feeney, 1998)": "$TFR^\\ast=TFR/(1-r(t))$",
         "Capital (this paper)": "$K^\\ast(t)$ via $\\mu(t)$-weighted PIM"},
        {"Concept": "Forgotten parameter",
         "Population (Bongaarts-Feeney, 1998)": "Parity-specific $\\sigma$ (Goldstein-Lutz-Scherbov, 2003)",
         "Capital (this paper)": "Intangible share $\\beta$ (Corrado-Hulten-Sichel, 2009)"},
        {"Concept": "Book-keeping identity",
         "Population (Bongaarts-Feeney, 1998)": "$dN/dt = B - d\\cdot N$",
         "Capital (this paper)": "$dW/dt = I - \\delta W$"},
        {"Concept": "Joint identification",
         "Population (Bongaarts-Feeney, 1998)": "TFR* vs. life-table consistency",
         "Capital (this paper)": "PIM vs. CWON consistency"},
    ]
    t2 = pd.DataFrame(t2_rows)
    t2.to_csv(os.path.join(TAB, "table2_correspondence.csv"), index=False)
    print("wrote table2")

    # Additionally export a bootstrap CI summary for manuscript.
    with open(os.path.join(TAB, "bootstrap_summary.json"), "w") as fh:
        json.dump({
            "n_countries": int(len(boot)),
            "mu_central_median": float(np.nanmedian(boot["mu_central"])),
            "mu_ci_width_median": float(np.nanmedian(
                boot["mu_hi"] - boot["mu_lo"])),
            "beta_central_median": float(np.nanmedian(boot["beta_central"])),
            "beta_ci_width_median": float(np.nanmedian(
                boot["beta_hi"] - boot["beta_lo"])),
        }, fh, indent=2)


def make_fig1_bilingual(lang: str = "en"):
    """Re-render M0-M4 growth RMSE ranking (Fig. 1) in given language."""
    fair = pd.read_csv(os.path.join(DATA, "fair_eval.csv"))
    s = fair.sort_values("M0_B_rmse")
    y = np.arange(len(s))
    bw = 0.18
    fig, ax = plt.subplots(figsize=(11, 9))
    labels = {
        "en": {"xlab": "Test B: 1-year GDP growth fit RMSE (pp)",
               "title": "Fig. 1. In-sample growth-rate fit across five K-constructions"},
        "ja": {"xlab": "検定B：単年度GDP成長率の当てはめRMSE（pp）",
               "title": "図1. 5つの資本ストック構成下での標本内成長率当てはめ"},
    }[lang]
    colors = ["#888888", "#4c72b0", "#dd8452", "#55a868", "#c44e52"]
    names = ["M0", "M1", "M2", "M3", "M4"]
    for i, (name, color) in enumerate(zip(names, colors)):
        ax.barh(y + (i - 2) * bw, s[f"{name}_B_rmse"].values, bw,
                label=name, color=color)
    ax.set_yticks(y); ax.set_yticklabels(s["country"].values, fontsize=8)
    ax.set_xlabel(labels["xlab"])
    ax.set_title(labels["title"])
    ax.legend(loc="lower right")
    plt.tight_layout()
    out = os.path.join(FIG, f"fig1_m_ranking_{lang}.png")
    plt.savefig(out, dpi=180)
    plt.close()
    print("wrote", out)


def make_fig2_bilingual(lang: str = "en"):
    oos = pd.read_csv(os.path.join(DATA, "oos.csv"))
    cols = ["M0_oos_mape", "M1_oos_mape", "M2_oos_mape",
            "M3_oos_mape", "M4_oos_mape"]
    fig, ax = plt.subplots(figsize=(8, 5))
    data = [oos[col].dropna().values for col in cols]
    ax.boxplot(data, tick_labels=["M0", "M1", "M2", "M3", "M4"],
               showmeans=True)
    if lang == "en":
        ax.set_ylabel("Out-of-sample MAPE 2015-19 (%)")
        ax.set_title("Fig. 2. Out-of-sample forecast accuracy, 39 countries")
    else:
        ax.set_ylabel("標本外MAPE 2015-19年（%）")
        ax.set_title("図2. 標本外予測精度（39カ国）")
    ax.grid(axis="y", alpha=0.3)
    plt.tight_layout()
    out = os.path.join(FIG, f"fig2_oos_{lang}.png")
    plt.savefig(out, dpi=180)
    plt.close()
    print("wrote", out)


def make_fig4_bilingual(lang: str = "en"):
    gamma = pd.read_csv(os.path.join(DATA, "gamma_price.csv"))
    gammas = [-0.04, -0.02, 0.0, 0.02, 0.04]
    highlight = ["Japan", "United States", "Germany",
                 "Republic of Korea", "Netherlands"]
    highlight_ja = {
        "Japan": "日本", "United States": "米国", "Germany": "ドイツ",
        "Republic of Korea": "韓国", "Netherlands": "オランダ",
    }
    fig, ax = plt.subplots(figsize=(8, 5))
    for country in highlight:
        row = gamma[gamma["country"] == country]
        if row.empty:
            continue
        vals = [float(row[f"logratio_g{g:+.2f}"].iloc[0]) for g in gammas]
        label = country if lang == "en" else highlight_ja[country]
        ax.plot(gammas, vals, "o-", label=label)
    ax.axhline(0, c="k", lw=0.5)
    if lang == "en":
        ax.set_xlabel(r"$\gamma_{price}$ (annual price re-evaluation rate)")
        ax.set_ylabel(r"$\log(W_{PIM}/\mathrm{CWON\ PCA}_{adj})$")
        ax.set_title("Fig. 4. γ_price sensitivity of the PIM-CWON gap")
    else:
        ax.set_xlabel(r"$\gamma_{price}$（年率価格再評価）")
        ax.set_ylabel(r"$\log(W_{PIM}/\mathrm{CWON\ PCA}_{adj})$")
        ax.set_title("図4. PIM-CWONギャップのγ_price感度")
    ax.legend()
    ax.grid(alpha=0.3)
    plt.tight_layout()
    out = os.path.join(FIG, f"fig4_gamma_price_{lang}.png")
    plt.savefig(out, dpi=180)
    plt.close()
    print("wrote", out)


def main():
    for lang in ("en", "ja"):
        make_fig1_bilingual(lang)
        make_fig2_bilingual(lang)
        make_fig3(lang)
        make_fig4_bilingual(lang)
        make_fig5(lang)
    make_tables()
    # Also make a second-language copy of figs 1/2/4 for JA
    # (axis labels regenerated later if needed -- for now English plots
    # are acceptable in JA manuscript with JA captions; but generate JA
    # versions for pptx consistency)
    print("done")


if __name__ == "__main__":
    main()
