# Final Handoff — IJBM revision

## A. Final manuscript title
"Traffic-crash mortality during unusually hot days in the United States: distributed-lag and road-user-specific analyses"

## B. Target journal
International Journal of Biometeorology (Springer) — Original Research Paper.

## C. Files generated
- `output/manuscript/ijbm_main_inline.docx` (embedded figs/tables, author review)
- `output/manuscript/ijbm_main_submission.docx` (legends-only, journal-ready)
- `output/manuscript/ijbm_title_page.docx`
- `output/manuscript/ijbm_cover_letter.docx` (dated 28 Sep 2026)
- `output/manuscript/ijbm_strobe_checklist.docx`
- `output/manuscript/ijbm_supplement.docx` (Figs. S1–S6, Tables S1–S4)
- `IJBM_submission_FINAL/` + `IJBM_submission_FINAL.zip` (docs, figures/, tables/, code/, data_processed/, audit files)
- `scripts/make_ijbm_submission.py` (+ `make ijbm` Makefile target)
- `scripts/sensitivity_contrast.py` → `data/processed/us_contrast_sensitivity.csv`
- `IJBM_INITIAL_AUDIT.md`, `REFERENCE_AND_NOVELTY_AUDIT.md`, `IJBM_FORMAT_AUDIT.md`, `IJBM_HOSTILE_REVIEW.md`, `AUTHOR_QUERIES.md`, this file.
- Highlights not produced: IJBM does not require them (see IJBM_FORMAT_AUDIT.md).

## D. Major scientific reframing
Manuscript now explicitly acknowledges prior heat–crash and heat–fatal-crash evidence and is positioned as refinement/extension: seasonal temperature-anomaly exposure, distributed-lag decomposition (acute excess vs displacement), nationwide fatal-crash mortality, road-user heterogeneity, attributable burden, exploratory transportability. "Research in context"/"under-recognised" framing removed; citation style converted to IJBM author–year with alphabetical Springer-style list; structure switched to Abstract/Keywords/Introduction/Methods/Results/Discussion/Conclusion/Declarations.

## E. New references added (all verified)
Wu CYH et al. 2018 Accid Anal Prev 119:195–201 (10.1016/j.aap.2018.07.025); Basagaña X et al. 2015 Environ Health Perspect 123:1309–1316 (10.1289/ehp.1409223); Pan R et al. 2024 Environ Res Commun 6:085011 (10.1088/2515-7620/ad6b03); Hsu C-K et al. 2025 Nat Cities 2:897–906 (10.1038/s44284-025-00279-x); Hsu C-K et al. 2026 Discov Cities (10.1007/s44327-026-00248-6).

## F. +9 °C sensitivity analysis
Performed (`scripts/sensitivity_contrast.py`). Same-day/cumulative RR: +5 °C 1.079/1.031; empirical p95 anomaly (6.25 °C) 1.104/1.043; +9 °C 1.165/1.076. Conclusions are contrast-robust → Table S1 (supplement), continuous curve remains primary.

## G. Numerical results changed
None — all reported values come from the committed result CSVs unchanged. Note: refitting the primary US model on the current committed inputs reproduces the +9 °C RRs exactly, but the re-derived panel is slightly larger (130,407 state-days / 273,427 deaths vs committed 129,897 / 272,586), a minor upstream data-build difference flagged for transparency.

## H. Analyses rerun
Only the contrast-robustness refit (F). Frozen otherwise; no new pipeline.

## I. Japan disposition
Retained, concise main-text subsection "External transportability: Japan" + detail in supplement (Figs. S5–S6, Table S4). Characterised as exploratory external comparison; not replication, not in title.

## J. Warming scenarios
Moved to supplement (Fig. S4, Table S3), one sentence in Results; labelled "illustrative scenario translation", never forecast.

## K. Direct-heat-death comparison
Retained in Results/Discussion + Table 5 and Fig. S3, reframed as magnitude context with explicit different-constructs caveat; out of title/abstract headline.

## L. Unresolved author metadata
ORCID iD; suggested reviewers; preprint/prior-submission confirmation; funding confirmation; name form. See AUTHOR_QUERIES.md.

## M. Unresolved submission-form items
Reviewer suggestions and any declarations collected via Springer submission interface must be entered by the author.

## N. Stale artifacts / placeholders
All IJBM deliverables scanned: no "TBD/TODO/XXX/PLACEHOLDER/to be added/to be confirmed", no stale journal names (AAP/EHP/JSR/Lancet appear only as legitimate references), no stale dates, no old title. Prior-journal files in output/manuscript were not shipped in the FINAL package.

## O. Consistency confirmation
All manuscript numbers are generated from the committed CSVs (no hard-coding); table/figure numbering sequential (Tables 1–5, Figs. 1–6, S1–S4/S1–S6); abstract 190 words; main-text budget ≈7,050 word-equivalents ≤ 7,500; OMML equations present; `make test` 6/6 pass; docx files verified to open.

## P. Readiness
**Ready for submission pending AUTHOR_QUERIES items** (ORCID, reviewer suggestions, preprint/funding confirmations). Scientifically conservative, literature-aware, IJBM-formatted package.
