# IJBM Initial Audit — heat-accidents-mortality

Date: 2026-09-28 (UTC). Branch: devin/1790635113-ijbm-submission (based on jsr-vitae tip 0bfcd29, the latest canonical tree containing all strata, DST-sensitivity and JSR work; origin/main is older).

## Canonical artifacts

- **Canonical manuscript source**: `scripts/make_manuscript.py` → `output/manuscript/heat_crash_mortality.docx` (inline figures) and `heat_crash_mortality_submission.docx` (legends only). All numbers are read from `data/processed/*.csv`; none are hard-coded. Style: Lancet-like (superscript Vancouver citations, "Research in context" panel, semi-structured Summary).
- **Canonical analysis outputs**: `data/processed/` (result CSVs, committed — no API keys needed to rebuild), `output/us_model_summary.txt`, `output/jp_model_summary.txt`, `output/figures/` (PNG + PDF).
- **Journal variant builders**: `scripts/make_aap_submission.py`, `make_ehp_submission.py`, `make_jsr_submission.py` — each re-runs `build_manuscript` then post-processes for the target journal (title, abstract, citation style, cover letter, package zip).
- **STROBE**: `strobe_checklist.docx` built by `build_strobe()` in make_manuscript.py.
- **Tables/figures**: `tables.docx`, `figures.pptx`, `submission_figures/` built by make_manuscript.py.

## Analysis baseline (frozen unless defect found)

US (FARS 2016–2022, 50 states, 272,586 deaths): same-day RR +9 °C anomaly 1.165 (1.135–1.196); cumulative lag0–10 RR 1.076 (1.017–1.139); net heat-attributable 528/yr (95% CI ~425–631; 1.36%); lag1–3 deficit 0.936 (0.904–0.968). VIF<10 screened full-controls same-day RR 1.170 (1.122–1.219). Open-air road users >> occupants (motorcyclist 2.14, pedestrian ~, cyclist ~, occupant 1.05).
Japan (NPA 2019–2024, 47 prefectures, 11,576 deaths): imprecise, cumulative RR 0.562 (0.207–1.525) — exploratory only.

## Outdated journal-specific text / stale artifacts

- `make_manuscript.py` cover letter: `[PLACEHOLDER date]`, `[Target journal]`, `[PLACEHOLDER competing interests]`, `[PLACEHOLDER confirm]`, `[PLACEHOLDER corresponding author]` — generic placeholder file, not journal-ready.
- ORCID `[iD to be added]` in manuscript correspondence and JSR title page.
- JSR cover letter hard-codes date "22 August 2026" (stale) and JSR framing.
- Title page: "Word count of main text: [to be confirmed]".
- Data availability section references "make ehp" — stale target wording.
- Prior packages (aap/ehp/jsr .docx/.zip) remain in output/manuscript — do not ship in IJBM package.

## Novelty claims that must be removed/softened (Phase 2)

- Title: "under-recognised risk factor".
- Summary/Interpretation: "under-recognised heat contribution".
- Research in context: "have received little attention as a possible reservoir of unrecognised heat mortality"; "We are not aware of national population-level studies..." — must be replaced by explicit acknowledgement of prior heat–crash/fatal-crash literature (incl. Wu et al. 2018 AAP FARS study).
- Introduction: "fatal crashes have rarely been examined as a heat-related safety outcome in their own right"; "under-recognised road-safety hazard".
- Discussion/Conclusion: "under-recognised heat contribution to road deaths".

## Mismatch/placeholder sweep to run at Phase 16

grep targets: "Journal of Safety Research", "Accident Analysis & Prevention", "Environmental Health Perspectives", "Lancet", "TBD/TODO/XXX/PLACEHOLDER/to be added/to be confirmed", old title, "22 August 2026".

## Feasibility notes for Phase 9 (+9 °C robustness)

Feasible: `scripts/analyze_us.py` refits the primary model from committed CSVs only; `bin_response`/`cumulative_curve` support arbitrary contrasts. Will add a small supplementary script computing same-day and cumulative RR at +5 °C, the empirical 95th-percentile anomaly, and +9 °C. Japan model likewise feasible if needed (not planned — US is primary).

## Japan disposition

Null/imprecise → retain as exploratory external transportability assessment; keep concise in main text, detail to supplement; not in title.
