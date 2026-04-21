# GDP tempo-effect PoC

This directory contains a proof-of-concept test of the hypothesis:

> *Just as adding a tempo effect (shifting mean age at birth) or a forgotten
> parameter (dispersion of the fertility schedule) improves the fit of period
> demographic indicators, the same logic might improve GDP models.*

The PoC operationalises the hypothesis as **time-varying time-to-build** in the
perpetual inventory method, and compares it against instant PIM and constant-lag
PIM on 39 countries (OECD + China + DR Congo) using Penn World Table 10.01.

See [`reports/poc_findings.md`](reports/poc_findings.md) for the main writeup.

## Reproduce

1. Download Penn World Table 10.01 (`.dta`) to `/home/ubuntu/gdp_tempo_data/pwt1001.dta`:
   ```bash
   mkdir -p /home/ubuntu/gdp_tempo_data
   curl -sL "https://dataverse.nl/api/access/datafile/354098" \
     -o /home/ubuntu/gdp_tempo_data/pwt1001.dta
   ```
2. Run:
   ```bash
   cd gdp_tempo_poc
   python scripts/run_poc.py
   python scripts/run_champion_plots.py
   ```

## Files

- `scripts/run_poc.py` — three PIM constructions × three evaluation tests across 39 countries.
- `scripts/run_champion_plots.py` — time-series overlay for the six countries with the largest M0→M2 gain.
- `data/poc_results.csv` — per-country results.
- `data/poc_summary.json` — aggregate statistics.
- `figures/fig1_growth_rmse.png` — RMSE bar chart by country (Test B).
- `figures/fig2_rmse_improvements_box.png` — pairwise RMSE improvement boxplot.
- `figures/fig3_K_direct_rmse.png` — direct K vs PWT's `rnna` comparison (Test C).
- `figures/fig4_mu1_scatter.png` — μ₁ drift vs RMSE reduction scatter.
- `figures/fig5_champions.png` — six "champion" countries' growth-rate fits.
- `reports/poc_findings.md` — writeup with conclusion and next steps.

## Headline result

- **M2 beats M0** on growth-rate RMSE for **74%** of the 39 countries.
- **Median improvement**: +0.028 pp on a baseline ~3.1 pp — directionally consistent
  but economically small. The tempo-effect channel in investment-to-output lag is
  about **1–2 orders of magnitude weaker** than the analogous fertility tempo effect.
- Largest gains are concentrated in transition economies (Baltic, Slovakia, Czech
  Republic) and small open economies (New Zealand, Luxembourg).
