"""
Generate the manuscript as .docx (English) following academic formatting.
Inline figures, Vancouver-style citations.

Onishi T. 2026.
"""

import os
import sys
import json
import re
import numpy as np
import pandas as pd
from docx import Document
from docx.shared import Inches, Pt, Cm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml.ns import qn

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FIGURES_DIR = os.path.join(BASE_DIR, 'figures')
RESULTS_DIR = os.path.join(BASE_DIR, 'results')


def load_results():
    with open(os.path.join(RESULTS_DIR, 'full_results.json'), 'r') as f:
        return json.load(f)


def add_superscript_refs(paragraph, text):
    """Parse text with {N} markers and add superscript references."""
    parts = re.split(r'(\{[^}]+\})', text)
    for part in parts:
        if part.startswith('{') and part.endswith('}'):
            run = paragraph.add_run(part[1:-1])
            run.font.superscript = True
            run.font.size = Pt(8)
        else:
            run = paragraph.add_run(part)
            run.font.size = Pt(11)


def create_manuscript():
    doc = Document()

    # Set default font
    style = doc.styles['Normal']
    font = style.font
    font.name = 'Times New Roman'
    font.size = Pt(11)

    # Margins
    sections = doc.sections
    for section in sections:
        section.top_margin = Cm(2.54)
        section.bottom_margin = Cm(2.54)
        section.left_margin = Cm(2.54)
        section.right_margin = Cm(2.54)

    # ======== TITLE PAGE ========
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = p.add_run('Modern Re-examination of 52 Canonical Curves:\n'
                    'Outlier Dependence, Sample Size Artifacts, and '
                    'the Fragility of Established Nonlinear Relationships')
    run.bold = True
    run.font.size = Pt(14)

    doc.add_paragraph()

    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = p.add_run('Tatsuki Onishi')
    run.font.size = Pt(12)

    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = p.add_run('2026')
    run.font.size = Pt(11)

    doc.add_page_break()

    # ======== ABSTRACT ========
    p = doc.add_paragraph()
    run = p.add_run('Abstract')
    run.bold = True
    run.font.size = Pt(12)

    results = load_results()
    verdicts = [r['verdict']['verdict'] for r in results]
    n_ns = verdicts.count('NOT_SIGNIFICANT')
    n_outlier = verdicts.count('OUTLIER_DEPENDENT')
    n_robust = verdicts.count('ROBUST_NONLINEAR')
    n_overfit = verdicts.count('OVERFITTING')

    abstract_text = (
        f"Background: Many curvilinear relationships are cited as established facts across diverse "
        f"academic disciplines, yet few have been systematically re-evaluated using modern model "
        f"selection techniques. "
        f"Methods: We re-examined 52 canonical curves spanning eight disciplines (economics, "
        f"public health, demography, environmental science, psychology, physics, political science, "
        f"and agriculture) using nested F-tests (linear vs. quadratic), Akaike and Bayesian "
        f"Information Criteria (AIC/BIC), leave-one-out cross-validation (LOOCV) RMSE, and "
        f"Cook's distance sensitivity analysis with removal of the top 3 influential observations. "
        f"Results: Of 52 curves, {n_ns} ({100*n_ns/52:.0f}%) showed no statistically significant "
        f"nonlinearity (p > 0.05), {n_outlier} ({100*n_outlier/52:.0f}%) were outlier-dependent "
        f"(significance lost after removing 1-3 influential points), {n_overfit} ({100*n_overfit/52:.0f}%) "
        f"showed overfitting on cross-validation, and only {n_robust} ({100*n_robust/52:.0f}%) "
        f"demonstrated robust nonlinearity surviving all tests. The outlier-dependent category "
        f"includes several high-profile relationships: the Kuznets Curve, Environmental Kuznets Curve, "
        f"Great Gatsby Curve, Lipset Hypothesis, and Species-Area relationship in log-log space. "
        f"Conclusions: A substantial fraction of textbook curvilinear relationships fail modern "
        f"re-examination, with implications for policy recommendations based on these curves."
    )
    p = doc.add_paragraph(abstract_text)
    p.paragraph_format.first_line_indent = Pt(0)

    p = doc.add_paragraph()
    run = p.add_run('Keywords: ')
    run.bold = True
    p.add_run('model selection; nonlinearity; outlier dependence; F-test; AIC; BIC; '
              'cross-validation; Cook\'s distance; canonical relationships')

    doc.add_page_break()

    # ======== 1. INTRODUCTION ========
    h = doc.add_heading('1. Introduction', level=1)

    intro_paras = [
        ("Curvilinear relationships occupy a privileged position in the social and natural sciences. "
         "From the Phillips Curve in macroeconomics to the Preston Curve in public health, "
         "these nonlinear functional forms are widely taught, frequently cited in policy documents, "
         "and often treated as established empirical regularities.{1-3} Yet many of these "
         "relationships were originally established with limited data, rudimentary statistical "
         "methods, and in eras when model selection criteria such as the Akaike Information "
         "Criterion (AIC) and Bayesian Information Criterion (BIC) were not yet standard practice.{4,5}"),

        ("Recent work has demonstrated that some celebrated curves may be artifacts of small "
         "samples, outlier dependence, or inappropriate model specification. For example, "
         "the Preston Curve's apparent concavity has been shown to depend heavily on the "
         "position of the United States as an outlier.{6} The Environmental Kuznets Curve "
         "for CO2 emissions has been repeatedly challenged.{7,8} The Dunning-Kruger effect "
         "has been argued to be a statistical artifact of regression to the mean.{9}"),

        ("Despite these individual re-examinations, no systematic cross-disciplinary audit "
         "has been conducted. The present study fills this gap by applying a uniform "
         "methodological framework to 52 canonical curves across eight academic disciplines. "
         "Our approach combines four complementary techniques: (1) nested F-tests for the "
         "significance of quadratic terms, (2) information criteria (AIC/BIC) for model "
         "selection, (3) leave-one-out cross-validation (LOOCV) for predictive accuracy, "
         "and (4) Cook's distance sensitivity analysis to assess outlier dependence."),
    ]
    for text in intro_paras:
        p = doc.add_paragraph()
        add_superscript_refs(p, text)

    # ======== 2. METHODS ========
    h = doc.add_heading('2. Methods', level=1)

    doc.add_heading('2.1 Curve Selection', level=2)
    p = doc.add_paragraph(
        "We selected 52 curves meeting the following criteria: (a) described by a named "
        "relationship (eponymous or otherwise) in the academic literature; (b) claimed to "
        "exhibit nonlinearity (concavity, convexity, U-shape, J-shape, or power law); "
        "(c) amenable to bivariate analysis (single predictor, single outcome); and "
        "(d) testable with publicly available cross-sectional or time-series data. "
        "The curves span economics (12), public health/epidemiology (10), demography (6), "
        "environmental science (6), psychology (5), physics (4), political science (5), "
        "and agriculture/nutrition (4)."
    )

    doc.add_heading('2.2 Data Sources', level=2)
    p = doc.add_paragraph(
        "Data were drawn from the World Bank World Development Indicators, OECD statistics, "
        "Penn World Tables, UN Population Division, published meta-analyses, and original "
        "study data where available. For each curve, we used the most recent available "
        "cross-sectional data (typically 2019-2023) or the longest available time series. "
        "Sample sizes ranged from N=11 (Fries Compression of Morbidity) to N=74 "
        "(Lee-Carter Mortality Model)."
    )

    doc.add_heading('2.3 Statistical Framework', level=2)

    p = doc.add_paragraph()
    run = p.add_run('Nested F-test. ')
    run.bold = True
    p.add_run("For each curve, we fitted a restricted (linear: y = a + bx) and unrestricted "
              "(quadratic: y = a + bx + cx\u00b2) model via ordinary least squares. The F-statistic "
              "for the additional quadratic parameter was computed as F = [(RSS_r - RSS_u)/p] / "
              "[RSS_u/df_u], where p = 1 is the number of additional parameters.")

    p = doc.add_paragraph()
    run = p.add_run('Information Criteria. ')
    run.bold = True
    p.add_run("AIC and BIC were computed for linear, quadratic, and logarithmic (where x > 0) "
              "models. The model with the lowest AIC (or BIC) was selected as the preferred "
              "functional form.")

    p = doc.add_paragraph()
    run = p.add_run('Leave-One-Out Cross-Validation. ')
    run.bold = True
    p.add_run("LOOCV root mean squared error (RMSE) was computed for both linear and quadratic "
              "models to assess out-of-sample predictive accuracy.")

    p = doc.add_paragraph()
    run = p.add_run("Cook's Distance Sensitivity Analysis. ")
    run.bold = True
    p.add_run("Cook's distance was computed for the linear model, and the top 3 most influential "
              "observations were removed. The F-test was then repeated on the reduced dataset. "
              "A curve was classified as 'outlier-dependent' if the nonlinear term was significant "
              "(p < 0.05) with full data but not significant (p > 0.05) after removing the top "
              "3 influential observations.")

    doc.add_heading('2.4 Verdict Classification', level=2)
    p = doc.add_paragraph("Each curve was assigned one of five verdicts:")
    verdicts_list = [
        "ROBUST_NONLINEAR: F-test significant (p < 0.05) with full data AND after outlier removal, quadratic LOOCV RMSE lower than linear.",
        "OUTLIER_DEPENDENT: F-test significant with full data but NOT after removing top 3 influential points.",
        "NOT_SIGNIFICANT: F-test not significant even with full data (p \u2265 0.05).",
        "OVERFITTING: F-test significant but LOOCV RMSE is worse for the quadratic model.",
        "BIC_PREFERS_LINEAR: F-test significant but BIC selects the linear model."
    ]
    for v in verdicts_list:
        p = doc.add_paragraph(v, style='List Bullet')

    # ======== 3. RESULTS ========
    h = doc.add_heading('3. Results', level=1)

    doc.add_heading('3.1 Overall Distribution of Verdicts', level=2)
    p = doc.add_paragraph()
    add_superscript_refs(p,
        f"Of the 52 canonical curves examined, {n_robust} ({100*n_robust/52:.0f}%) demonstrated "
        f"robust nonlinearity, {n_outlier} ({100*n_outlier/52:.0f}%) were outlier-dependent, "
        f"{n_ns} ({100*n_ns/52:.0f}%) showed no significant nonlinearity, and "
        f"{n_overfit} ({100*n_overfit/52:.0f}%) exhibited overfitting (Fig. 1). "
        f"This distribution suggests that nearly two-thirds of textbook nonlinear relationships "
        f"either fail to reach significance or are driven by a small number of influential observations."
    )

    # Insert Figure 1
    doc.add_paragraph()
    doc.add_picture(os.path.join(FIGURES_DIR, 'fig1_verdict_distribution.png'), width=Inches(6.0))
    p = doc.add_paragraph()
    run = p.add_run('Figure 1. ')
    run.bold = True
    p.add_run('Distribution of verdicts across 52 canonical curves. (A) Overall pie chart. '
              '(B) Verdicts stratified by academic domain.')
    p.paragraph_format.space_before = Pt(6)

    # Results by domain
    doc.add_heading('3.2 Economics', level=2)
    econ_text = (
        "Of the 12 economics curves examined, 7 showed no significant nonlinearity, "
        "4 were outlier-dependent, and only 1 (J-Curve for trade) demonstrated robust "
        "nonlinearity. Notable findings include: (a) the Phillips Curve shows no significant "
        "nonlinearity in US data 1960-2023 (F=0.05, p=0.82); (b) the Kuznets Curve's "
        "inverted-U is not statistically significant with 60 countries (p=0.25); "
        "(c) the Environmental Kuznets Curve for CO2 is significant (p=0.003) but becomes "
        "non-significant after removing 3 high-income high-emission countries (p=0.11); "
        "(d) the Laffer Curve and Great Gatsby Curve are similarly outlier-dependent."
    )
    doc.add_paragraph(econ_text)

    doc.add_heading('3.3 Public Health and Epidemiology', level=2)
    health_text = (
        "Public health curves showed the highest rate of robust nonlinearity (8 of 10). "
        "The BMI-Mortality J-curve, Alcohol-Mortality J-curve, Barker Hypothesis U-shape, "
        "and LNT dose-response all survived rigorous testing. The Preston Curve maintained "
        "significance after outlier removal (p=0.003), though the log model is strongly "
        "preferred over quadratic by BIC. The Wilkinson Curve (inequality vs. health) "
        "showed no significant relationship (p=0.75), and the Fries Compression of "
        "Morbidity was outlier-dependent."
    )
    doc.add_paragraph(health_text)

    doc.add_heading('3.4 Demography', level=2)
    demo_text = (
        "The demographic domain showed mixed results. The Lee-Carter mortality decline "
        "and Coale-Trussell fertility schedule demonstrated robust nonlinearity, while "
        "the Bongaarts-Feeney tempo effect and Second Demographic Transition showed no "
        "significant nonlinearity. The Demographic Transition model was classified as "
        "overfitting: the quadratic term is significant but LOOCV favors the linear model, "
        "suggesting that the apparent curvature does not improve out-of-sample prediction."
    )
    doc.add_paragraph(demo_text)

    doc.add_heading('3.5 Environmental Science', level=2)
    env_text = (
        "Environmental curves showed the most heterogeneous results. The Keeling Curve's "
        "acceleration is robustly nonlinear (p < 10\u207b\u00b9\u2075), as expected for an "
        "exponentially increasing trend. However, the Species-Area Curve in log-log space "
        "is outlier-dependent (p=0.009 full, p=0.38 after removal), suggesting that the "
        "power-law exponent z \u2248 0.25 may be driven by a few extreme island sizes. "
        "The Hubbert Peak Oil curve for the US shows no significant quadratic trend (p=0.90) "
        "due to the shale revolution creating a second peak."
    )
    doc.add_paragraph(env_text)

    doc.add_heading('3.6 Psychology', level=2)
    psych_text = (
        "Four of five psychology curves showed robust nonlinearity: Yerkes-Dodson, "
        "Ebbinghaus forgetting, Dunning-Kruger, and the Happiness U-Curve. However, "
        "the Weber-Fechner Law (in log-transformed space) did not show significant "
        "departure from linearity (p=0.07), consistent with Stevens' Power Law being "
        "a better descriptor. The Dunning-Kruger result is notable: despite criticisms "
        "of the effect as a statistical artifact, the quadratic relationship between "
        "actual and self-assessed performance remains highly significant (p < 10\u207b\u00b9\u2074) "
        "and survives outlier removal."
    )
    doc.add_paragraph(psych_text)

    doc.add_heading('3.7 Physics and Natural Sciences', level=2)
    phys_text = (
        "Physics curves showed surprising fragility. Hubble's Law, while linear by "
        "theoretical expectation, shows marginal nonlinearity (p=0.035) that becomes "
        "non-significant after outlier removal (p=0.085), consistent with the known "
        "influence of peculiar velocities for nearby galaxies. Kleiber's Law in log-log "
        "space shows no significant departure from linearity (p=0.36), confirming the "
        "power-law relationship. The Gutenberg-Richter law is outlier-dependent in "
        "log-linear space (p=0.004 full, p=0.056 clean), driven by the rarest "
        "mega-earthquakes. Moore's Law shows no significant quadratic deceleration "
        "in log space (p=0.71)."
    )
    doc.add_paragraph(phys_text)

    doc.add_heading('3.8 Political Science', level=2)
    pol_text = (
        "The Lipset Hypothesis (income vs. democracy) is the most dramatic outlier-dependent "
        "case: highly significant with full data (p=0.0001) but completely non-significant "
        "after removing Gulf oil states (p=0.37). Duverger's Law shows no significant "
        "nonlinearity (p=0.45), nor does Zipf's Law for US cities (p=0.15). The "
        "Crime-Temperature curve is outlier-dependent, with the apparent downturn at "
        "extreme temperatures driven by a few data points."
    )
    doc.add_paragraph(pol_text)

    doc.add_heading('3.9 Agriculture', level=2)
    agr_text = (
        "The Mitscherlich yield response curve shows robust nonlinearity (p < 10\u207b\u2079), "
        "confirming the well-established diminishing returns to fertilizer application. "
        "The Micronutrient U-shape for Vitamin D is also robust. However, the Green "
        "Revolution yield curve does not show significant nonlinear deceleration (p=0.28) "
        "in global data, and the Body Weight Set-Point shows predominantly linear "
        "calorie-weight relationship (p=0.74)."
    )
    doc.add_paragraph(agr_text)

    # Insert Figure 2
    doc.add_heading('3.10 Sensitivity Analysis', level=2)
    p = doc.add_paragraph(
        "Figure 2 displays the relationship between p-values from the full dataset and "
        "after outlier removal. Points in the upper-left quadrant (significant with full "
        "data, non-significant after removal) represent outlier-dependent curves. The "
        "concentration of points in this region, particularly from economics and political "
        "science, highlights the vulnerability of cross-country nonlinear relationships "
        "to influential observations (Fig. 2)."
    )

    doc.add_paragraph()
    doc.add_picture(os.path.join(FIGURES_DIR, 'fig2_sensitivity_analysis.png'), width=Inches(5.5))
    p = doc.add_paragraph()
    run = p.add_run('Figure 2. ')
    run.bold = True
    p.add_run('Sensitivity of F-test p-values to outlier removal. Each point represents one '
              'curve. Points above the horizontal dashed line (p=0.05) lost significance '
              'after removing top 3 influential observations.')
    p.paragraph_format.space_before = Pt(6)

    # ======== Table 1: Summary ========
    doc.add_heading('3.11 Summary Table', level=2)
    p = doc.add_paragraph(
        "Table 1 presents the complete results for all 52 curves, organized by discipline."
    )

    # Create summary table
    df = pd.read_csv(os.path.join(RESULTS_DIR, 'summary_table.csv'))

    table = doc.add_table(rows=1, cols=7)
    table.style = 'Table Grid'
    table.alignment = WD_TABLE_ALIGNMENT.CENTER

    headers = ['#', 'Curve', 'N', 'p (full)', 'p (clean)', 'Best BIC', 'Verdict']
    for i, h_text in enumerate(headers):
        cell = table.rows[0].cells[i]
        cell.text = h_text
        cell.paragraphs[0].runs[0].bold = True
        cell.paragraphs[0].runs[0].font.size = Pt(8)

    for idx, row in df.iterrows():
        row_cells = table.add_row().cells
        row_cells[0].text = str(idx + 1)
        row_cells[1].text = str(row['Curve'])[:30]
        row_cells[2].text = str(row['N'])
        p_full = row['p (full)']
        row_cells[3].text = f"{p_full:.4f}" if p_full > 0.0001 else f"{p_full:.2e}"
        p_clean = row['p (clean)']
        row_cells[4].text = f"{p_clean:.4f}" if p_clean > 0.0001 else f"{p_clean:.2e}"
        row_cells[5].text = str(row['BIC best'])
        row_cells[6].text = str(row['Verdict']).replace('_', ' ')

        for cell in row_cells:
            for para in cell.paragraphs:
                for run in para.runs:
                    run.font.size = Pt(7)

    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(12)
    run = p.add_run('Table 1. ')
    run.bold = True
    p.add_run('Summary of re-examination results for 52 canonical curves. '
              'p (full) = F-test p-value with all data; p (clean) = after removing '
              'top 3 Cook\'s distance points; Best BIC = model preferred by Bayesian '
              'Information Criterion.')

    # Insert Figure 3
    doc.add_paragraph()
    doc.add_picture(os.path.join(FIGURES_DIR, 'fig3_model_comparison.png'), width=Inches(5.5))
    p = doc.add_paragraph()
    run = p.add_run('Figure 3. ')
    run.bold = True
    p.add_run('Model preference by AIC (left) and BIC (right). BIC more strongly '
              'penalizes complexity and thus favors parsimony.')
    p.paragraph_format.space_before = Pt(6)

    # ======== 4. DISCUSSION ========
    h = doc.add_heading('4. Discussion', level=1)

    doc.add_heading('4.1 Cross-Cutting Patterns', level=2)
    p = doc.add_paragraph()
    add_superscript_refs(p,
        "Our analysis reveals five cross-cutting patterns in the fragility of canonical curves:"
    )

    patterns = [
        ("Outlier-driven nonlinearity (23% of curves): The most common failure mode involves "
         "1-3 observations that drive the curvature. In cross-country analyses, these are often "
         "geopolitically distinctive nations (oil states for Lipset, the US for Great Gatsby and "
         "Preston, Nigeria for Engel)."),
        ("Domain asymmetry: Public health and psychology curves are substantially more robust "
         "(80% and 80% passing) than economics curves (8% passing). This likely reflects the "
         "mechanistic basis of dose-response and psychophysical relationships versus the "
         "contingent nature of macroeconomic regularities."),
        ("Time-series vs. cross-section: Time-series curves (Lee-Carter, Keeling, Ebbinghaus) "
         "are more robust than cross-sectional ones (Kuznets, Lipset, Wilkinson), likely because "
         "time-series data are less vulnerable to compositional effects and unmeasured confounders."),
        ("Log transformation resolves apparent nonlinearity: In many cases (Preston, Engel, "
         "Balassa-Samuelson), a simple log transformation of the predictor produces a linear "
         "relationship, suggesting that the 'canonical curve' is merely a linear relationship "
         "on the wrong scale."),
        ("BIC is more conservative: BIC selects the linear model in several cases where AIC "
         "prefers the quadratic, reflecting BIC's stronger penalty for complexity. When BIC "
         "and AIC disagree, the curve is typically in the borderline zone and should be "
         "interpreted cautiously."),
    ]
    for pat in patterns:
        p = doc.add_paragraph(pat, style='List Number')

    doc.add_heading('4.2 Implications for Policy', level=2)
    policy_text = (
        "Several outlier-dependent curves have direct policy implications. The Laffer Curve "
        "is used to justify tax rate reductions; our analysis shows its empirical basis is "
        "fragile across OECD nations. The Environmental Kuznets Curve for CO2 is frequently "
        "cited to argue that economic growth will eventually resolve emissions problems; this "
        "relationship is not robust after removing high-income oil producers. The Lipset "
        "Hypothesis underpins modernization theory in political science; its nonlinearity "
        "depends almost entirely on Gulf state outliers."
    )
    doc.add_paragraph(policy_text)

    doc.add_heading('4.3 Limitations', level=2)
    limitations = (
        "Several limitations should be noted. First, our analysis is restricted to bivariate "
        "relationships; many canonical curves may be better specified in multivariate settings. "
        "Second, we use a uniform quadratic alternative, whereas some curves posit specific "
        "functional forms (e.g., power laws, logistic functions). Third, our data are "
        "representative but not exhaustive; larger datasets might reveal patterns not visible "
        "here. Fourth, we test only concavity/convexity, not the existence of any relationship. "
        "A curve classified as 'not significantly nonlinear' may still have a significant "
        "linear component. Finally, for some curves (especially in psychology and demography), "
        "we rely on representative or meta-analytic data rather than individual-level microdata."
    )
    doc.add_paragraph(limitations)

    doc.add_heading('4.4 Recommendations for Researchers', level=2)
    recs = [
        "Always test whether a log-transformation linearizes the relationship before reporting nonlinearity.",
        "Report Cook's distance analysis and sensitivity to influential observations.",
        "Distinguish between statistical significance and practical significance of curvature.",
        "Use BIC rather than AIC when the goal is model identification rather than prediction.",
        "Report LOOCV alongside in-sample fit to guard against overfitting.",
    ]
    for r in recs:
        doc.add_paragraph(r, style='List Number')

    # ======== 5. CONCLUSION ========
    h = doc.add_heading('5. Conclusion', level=1)
    conclusion = (
        f"This systematic re-examination of 52 canonical curves reveals that "
        f"{100*(n_ns + n_outlier + n_overfit)/52:.0f}% of established nonlinear relationships "
        f"fail at least one modern robustness test. The most common failure mode is outlier "
        f"dependence ({100*n_outlier/52:.0f}%), followed by non-significance ({100*n_ns/52:.0f}%). "
        f"Only {100*n_robust/52:.0f}% of curves demonstrate nonlinearity that is statistically "
        f"significant, survives outlier removal, and shows superior out-of-sample prediction. "
        f"These findings urge caution in citing canonical curves as empirical support for "
        f"nonlinear theories, particularly in policy-relevant contexts where the shape of "
        f"the relationship (not merely its existence) determines optimal interventions."
    )
    doc.add_paragraph(conclusion)

    # ======== REFERENCES ========
    doc.add_page_break()
    h = doc.add_heading('References', level=1)

    references = [
        "Phillips AW. The relation between unemployment and the rate of change of money wage rates in the United Kingdom, 1861-1957. Economica. 1958;25(100):283-299.",
        "Kuznets S. Economic growth and income inequality. Am Econ Rev. 1955;45(1):1-28.",
        "Preston SH. The changing relation between mortality and level of economic development. Popul Stud. 1975;29(2):231-248.",
        "Akaike H. A new look at the statistical model identification. IEEE Trans Automat Contr. 1974;19(6):716-723.",
        "Schwarz G. Estimating the dimension of a model. Ann Stat. 1978;6(2):461-464.",
        "Onishi T. Re-examination of the Preston Curve: outlier dependence of quadratic fit. Working paper. 2026.",
        "Grossman GM, Krueger AB. Environmental impacts of a North American free trade agreement. NBER Working Paper 3914. 1991.",
        "Stern DI. The rise and fall of the environmental Kuznets curve. World Dev. 2004;32(8):1419-1439.",
        "Krueger J, Mueller RA. Unskilled, unaware, or both? The better-than-average heuristic and statistical regression predict errors in estimates of own performance. J Pers Soc Psychol. 2002;82(2):180-188.",
    ]

    for i, ref in enumerate(references, 1):
        p = doc.add_paragraph()
        run = p.add_run(f"{i}. ")
        run.bold = True
        p.add_run(ref)
        p.paragraph_format.first_line_indent = Pt(0)
        p.paragraph_format.left_indent = Cm(1)

    # Save
    output_path = os.path.join(BASE_DIR, 'manuscript_canonical_curves_en.docx')
    doc.save(output_path)
    print(f"Manuscript saved to: {output_path}")
    return output_path


if __name__ == "__main__":
    create_manuscript()
