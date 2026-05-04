"""
English manuscript: Healthcare Expenditure as Economic Effect
— A Neutral Sustainability Framework Based on I-O Multipliers and Health-Capital Tempo

Generates:
  - output/docx/Healthcare_Economic_Effect_EN.docx
  - output/pptx/Healthcare_Economic_Effect_Figures_EN.pptx
"""
import os
import re
import json
import pandas as pd
from docx import Document
from docx.shared import Inches, Pt, Cm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from pptx import Presentation
from pptx.util import Inches as PptxInches, Pt as PptxPt
from pptx.enum.text import PP_ALIGN

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, ".."))
DATA = os.path.join(ROOT, "data")
FIG_EN = os.path.join(ROOT, "output", "figures_en")
FIG = os.path.join(ROOT, "output", "figures")  # fallback if EN figs not generated
DOCX_DIR = os.path.join(ROOT, "output", "docx")
PPTX_DIR = os.path.join(ROOT, "output", "pptx")
os.makedirs(DOCX_DIR, exist_ok=True)
os.makedirs(PPTX_DIR, exist_ok=True)


def get_fig(name):
    """Return EN figure path if it exists, otherwise fallback to default."""
    en_path = os.path.join(FIG_EN, name)
    if os.path.exists(en_path):
        return en_path
    return os.path.join(FIG, name)


# ---------------------------------------------------------------------------
# Helpers (same pattern as JA)
# ---------------------------------------------------------------------------
def add_text_with_refs(paragraph, text, bold=False):
    parts = re.split(r'(\{[^}]+\})', text)
    for part in parts:
        if part.startswith('{') and part.endswith('}'):
            run = paragraph.add_run(part[1:-1])
            run.font.superscript = True
            run.font.size = Pt(8)
        else:
            run = paragraph.add_run(part)
            if bold:
                run.bold = True


def add_heading(doc, text, level=1):
    return doc.add_heading(text, level=level)


def add_para(doc, text, bold=False):
    p = doc.add_paragraph()
    add_text_with_refs(p, text, bold=bold)
    return p


def add_figure(doc, img_path, caption):
    if os.path.exists(img_path):
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        run = p.add_run()
        run.add_picture(img_path, width=Inches(5.5))
    cap = doc.add_paragraph()
    cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
    cap.paragraph_format.space_before = Pt(6)
    cap.paragraph_format.space_after = Pt(12)
    run = cap.add_run(caption)
    run.font.size = Pt(9)
    run.italic = True


def add_table_from_df(doc, df, caption):
    cap = doc.add_paragraph()
    run = cap.add_run(caption)
    run.font.size = Pt(9)
    run.italic = True
    cap.paragraph_format.space_after = Pt(4)
    table = doc.add_table(rows=1, cols=len(df.columns), style='Table Grid')
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    for j, col in enumerate(df.columns):
        cell = table.rows[0].cells[j]
        cell.text = str(col)
        for p in cell.paragraphs:
            for r in p.runs:
                r.bold = True
                r.font.size = Pt(9)
    for _, row in df.iterrows():
        row_cells = table.add_row().cells
        for j, col in enumerate(df.columns):
            row_cells[j].text = str(row[col])
            for p in row_cells[j].paragraphs:
                for r in p.runs:
                    r.font.size = Pt(9)
    doc.add_paragraph()


def create_pptx_slide(prs, img_path, title, caption):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    txBox = slide.shapes.add_textbox(PptxInches(0.5), PptxInches(0.2),
                                      PptxInches(12.33), PptxInches(0.6))
    tf = txBox.text_frame
    tf.text = title
    tf.paragraphs[0].font.size = PptxPt(18)
    tf.paragraphs[0].font.bold = True
    tf.paragraphs[0].alignment = PP_ALIGN.CENTER
    if os.path.exists(img_path):
        slide.shapes.add_picture(img_path, PptxInches(1.5), PptxInches(1.0),
                                  PptxInches(10.33), PptxInches(5.0))
    txBox2 = slide.shapes.add_textbox(PptxInches(0.5), PptxInches(6.3),
                                       PptxInches(12.33), PptxInches(0.8))
    tf2 = txBox2.text_frame
    tf2.word_wrap = True
    tf2.text = caption
    tf2.paragraphs[0].font.size = PptxPt(10)
    tf2.paragraphs[0].font.italic = True
    tf2.paragraphs[0].alignment = PP_ALIGN.CENTER


REFERENCES = [
    "Yamada G, Imanaka Y. Input-output analysis on the economic impact of "
    "medical care in Japan. Environ Health Prev Med. 2015;20(5):379-387.",
    "Maeda Y. Economic ripple effects of healthcare and long-term care. "
    "JMARI Working Paper No. 172. 2008. [In Japanese]",
    "Dupor B, Guerrero R. The aggregate and local economic effects of "
    "government financed health care. Econ Inq. 2021;59(2):662-670.",
    "Ertuğrul HM, Baycan O, Atilgan E, Ulucan H. Health-led growth hypothesis "
    "and health financing systems: an econometric synthesis for OECD countries. "
    "Front Public Health. 2024;12:1437304.",
    "Amiri A, Ventelou B. Granger causality between total expenditure on "
    "health and GDP in OECD: Evidence from the Toda-Yamamoto approach. "
    "Econ Lett. 2012;116(3):541-544.",
    "Beylik U, Cetin M, Senol O, Cirakli U, Ecevit E. The relationship "
    "between health expenditure indicators and economic growth in OECD "
    "countries: A Driscoll-Kraay approach. Front Public Health. "
    "2022;10:1050550.",
    "Wang KM. Health care expenditure and economic growth: Quantile "
    "panel-type analysis. Econ Model. 2011;28(4):1536-1549.",
    "Mushkin SJ. Health as an investment. J Polit Econ. 1962;70(5):129-157.",
    "Grossman M. On the concept of health capital and the demand for "
    "health. J Polit Econ. 1972;80(2):223-255.",
    "OECD. Health at a Glance 2023: OECD Indicators. Paris: OECD Publishing; "
    "2023.",
    "Cabinet Office, Japan. Annual Report on the Japanese Economy 2025. "
    "Tokyo: Cabinet Office; 2025. [In Japanese]",
    "World Bank. World Development Indicators. Washington, DC: World Bank; "
    "2024. Available from: https://databank.worldbank.org/",
    "Henke KD, Ostwald DA. Health satellite account: the first step. "
    "In: Dged JM, ed. The Elgar Companion to Health Economics. 2nd ed. "
    "Cheltenham: Edward Elgar; 2012. p. 327-337.",
    "Piabuo SM, Tieguhong JC. Health expenditure and economic growth — "
    "a review of the literature and an analysis between the economic "
    "community for central African states (CEMAC) and selected African "
    "countries. Health Econ Rev. 2017;7(1):23.",
    "Barro RJ. Health and economic growth. Ann Econ Finance. "
    "2013;14(2):305-342.",
    "Bloom DE, Canning D, Sevilla J. The effect of health on economic "
    "growth: a production function approach. World Dev. "
    "2004;32(1):1-13.",
]


# ---------------------------------------------------------------------------
# Build English manuscript
# ---------------------------------------------------------------------------
def build_en_docx():
    doc = Document()

    # Title
    title = doc.add_paragraph()
    title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = title.add_run(
        "Healthcare Expenditure as Economic Effect:\n"
        "A Neutral Sustainability Framework Based on I-O Multipliers "
        "and Health-Capital Tempo"
    )
    run.font.size = Pt(16)
    run.bold = True

    # ---------- Abstract ----------
    add_heading(doc, "Abstract", level=1)
    add_para(doc,
        "Healthcare expenditure has traditionally been framed as a fiscal "
        "'cost' to be contained. However, input-output (I-O) analysis reveals "
        "that each unit of healthcare spending generates 2.78 times its value "
        "in economic output in Japan{1}, with multipliers ranging from 1.7 to "
        "2.9 across OECD countries{1,3,13}. Furthermore, the Health-Led Growth "
        "Hypothesis (HLGH) literature confirms bidirectional Granger causality "
        "between health expenditure and GDP growth{4-7}. This paper proposes "
        "a 'neutral sustainability criterion' that integrates (1) demand-side "
        "returns via I-O multipliers and (2) supply-side returns via health-capital "
        "stock accumulation with tempo effects. Using data from nine countries, "
        "we find that the demand-side fiscal return ratio (tau * m / pf) exceeds 1.0 "
        "in three of nine cases (Japan, France, Sweden), with the remaining six "
        "countries achieving ratios of 0.76-0.96 — recovering the majority of "
        "public expenditure through tax revenues from healthcare-induced economic "
        "activity alone. When supply-side health-capital accumulation returns are "
        "added, comprehensive sustainability likely holds for most countries. "
        "Reframing healthcare expenditure from 'cost' to 'investment with economic "
        "returns' can redirect the sustainability debate toward more productive "
        "policy discourse."
    )

    # ---------- 1. Introduction ----------
    add_heading(doc, "1. Introduction", level=1)
    add_para(doc,
        "Since the Cabinet's 'Basic Policies' decision in 2005, the Japanese "
        "government has pursued policies to moderate the growth of national "
        "medical care expenditure{1}. Japan's current health expenditure reached "
        "11.0% of GDP in 2019, ranking 5th among 38 OECD countries{10}. With "
        "rapid population aging, the 'sustainability' of healthcare spending "
        "has become a central policy concern{11}."
    )
    add_para(doc,
        "This discourse has almost uniformly treated healthcare expenditure as a "
        "'cost' — an expense to be minimized through efficiency gains and volume "
        "controls. Yet healthcare is also a major economic sector: it purchases "
        "inputs from pharmaceuticals, medical devices, and IT; it employs millions "
        "of workers; and these workers spend their incomes, generating further "
        "economic activity. Maeda (2008) estimated that Japan's healthcare sector "
        "supports 6.89 million jobs in total (2.95 million direct, approximately "
        "4 million indirect), with production-inducement effects exceeding those "
        "of any other service industry{2}. Yamada and Imanaka (2015) quantified "
        "the I-O multiplier at 2.78 (95% CI: 2.74-2.90){1}."
    )
    add_para(doc,
        "The aim of this paper is to re-evaluate healthcare expenditure from a "
        "neutral standpoint — as both a cost and an economic effect — and to "
        "formalize sustainability in terms of dual returns: demand-side (I-O "
        "multiplier) and supply-side (health-capital accumulation)."
    )

    # ---------- 2. Background ----------
    add_heading(doc, "2. Background: The Dual Nature of Healthcare Expenditure", level=1)

    add_heading(doc, "2.1 Demand Side: Input-Output Multipliers", level=2)
    add_para(doc,
        "Input-output analysis, pioneered by Leontief (1936), quantifies how "
        "final demand in one sector induces production across the entire economy "
        "through direct, indirect, and induced effects. For the healthcare sector, "
        "estimated multipliers across countries are shown in Figure 1 and Table 1."
    )

    add_figure(doc, get_fig("fig1_io_multipliers.png"),
               "Figure 1. Healthcare I-O Multipliers by Country")

    io_df = pd.read_csv(os.path.join(DATA, "io_multipliers.csv"))
    io_display = io_df[["country", "multiplier", "year", "source"]].copy()
    io_display.columns = ["Country", "Multiplier", "Reference Year", "Source"]
    add_table_from_df(doc, io_display, "Table 1. Healthcare Sector I-O Multipliers (Cross-Country)")

    add_para(doc,
        "Japan's multiplier of 2.78 is the highest among the comparator countries, "
        "comparable to or exceeding public works (2.1-2.5) and utilities "
        "(1.8-2.0){1,2}. The US Medicare multiplier of 1.7{3} is lower, "
        "likely reflecting leakage through high pharmaceutical prices and "
        "administrative costs to overseas firms."
    )

    add_heading(doc, "2.2 Supply Side: Health Capital and Human Capital", level=2)
    add_para(doc,
        "Since Mushkin (1962), health has been recognized as a component of human "
        "capital{8}. Grossman's (1972) health-capital model describes individual "
        "health stock as accumulated through investment (healthcare, prevention) "
        "and depreciated by aging and disease{9}. At the macro level, Bloom, "
        "Canning, and Sevilla (2004) demonstrated that improved health raises "
        "total factor productivity{16}, and Barro (2013) estimated that a one-year "
        "increase in life expectancy raises GDP growth by approximately 0.04 "
        "percentage points{15}."
    )
    add_para(doc,
        "Crucially, there is a temporal lag between health-capital accumulation "
        "and economic outcomes. Our healthcare_tempo_poc analysis (Candidate A-H) "
        "detected a mean lag drift of mu_H1 = +0.15 years/year, with the tempo "
        "model (M2) outperforming the constant-lag model (M1) in 95% of 39 "
        "countries. This implies that evaluating efficiency using only "
        "contemporaneous flow indicators (period spending vs. period outcomes) "
        "systematically underestimates the return on healthcare investment."
    )

    add_heading(doc, "2.3 Empirical Evidence for the HLGH", level=2)
    add_para(doc,
        "The Health-Led Growth Hypothesis (HLGH) posits that healthcare "
        "expenditure promotes economic growth. Table 2 summarizes the principal "
        "panel-data studies for OECD countries."
    )

    hlgh_df = pd.read_csv(os.path.join(DATA, "hlgh_evidence.csv"))
    hlgh_display = hlgh_df[["study", "n_countries", "period", "method", "direction"]].copy()
    hlgh_display.columns = ["Study", "Countries", "Period", "Method", "Causality Direction"]
    add_table_from_df(doc, hlgh_display,
                      "Table 2. Summary of HLGH Empirical Studies")

    add_para(doc,
        "All studies confirm a positive effect of health expenditure on GDP "
        "growth, and most detect bidirectional causality{4-7}. This supports "
        "the view that healthcare spending is not merely a cost but functions "
        "as an engine of economic growth."
    )

    # ---------- 3. Framework ----------
    add_heading(doc, "3. A Neutral Sustainability Framework", level=1)
    add_para(doc,
        "We propose evaluating healthcare sustainability through a dual-return "
        "structure encompassing demand-side and supply-side returns (Figure 4)."
    )

    add_figure(doc, get_fig("fig4_dual_return_schematic.png"),
               "Figure 4. Dual-Return Framework for Neutral Healthcare Sustainability")

    add_heading(doc, "3.1 Demand Side: Fiscal Return Ratio", level=2)
    add_para(doc,
        "Healthcare expenditure E(t), through the I-O multiplier m, induces "
        "total output of m * E(t) across the economy. With an effective tax "
        "rate tau on this output, and a public financing share pf of healthcare "
        "expenditure, the neutral fiscal sustainability criterion is:"
    )
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = p.add_run("Fiscal Return Ratio = (tau * m) / pf >= 1.0")
    run.bold = True
    run.font.size = Pt(11)

    add_para(doc,
        "When this ratio exceeds 1.0, the tax and social-insurance revenues "
        "generated by healthcare-induced economic activity exceed the public "
        "cost of healthcare. Table 3 and Figure 3 present the estimates for "
        "nine countries."
    )

    sust_df = pd.read_csv(os.path.join(DATA, "neutral_sustainability.csv"))
    sust_display = sust_df[["country", "io_multiplier", "eff_tax_rate",
                             "public_share_che", "fiscal_return_ratio", "sustainable"]].copy()
    sust_display.columns = ["Country", "I-O Multiplier", "Eff. Tax Rate",
                            "Public Share", "Fiscal Return Ratio", "Sustainable"]
    add_table_from_df(doc, sust_display,
                      "Table 3. Neutral Fiscal Sustainability Indicators (9 countries)")

    add_figure(doc, get_fig("fig3_fiscal_sustainability.png"),
               "Figure 3. Fiscal Return Ratio of Healthcare Spending by Country")

    add_para(doc,
        "Three of nine countries (Japan 1.09, France 1.18, Sweden 1.04) achieve a "
        "demand-side-only fiscal return ratio above 1.0. The remaining six countries "
        "range from 0.76 (Australia) to 0.96 (Germany), recovering the bulk of "
        "public expenditure through demand-side tax revenues alone. Germany (0.96) "
        "and the US (0.92) narrowly miss the threshold; Korea (0.86), Canada (0.82), "
        "the UK (0.78), and Australia (0.76) show progressively larger gaps. These "
        "gaps are expected to be closed by supply-side returns (health-capital "
        "accumulation) not captured in this demand-only metric. The finding that "
        "demand-side revenues alone recover 76-118% of public costs challenges the "
        "framing of healthcare as a pure fiscal drain."
    )

    add_heading(doc, "3.2 Supply Side: Tempo-Adjusted Health-Capital Returns", level=2)
    add_para(doc,
        "The fiscal return ratio captures only the contemporaneous flow effect. "
        "The full economic value of healthcare spending also includes supply-side "
        "returns through future productivity gains from health-capital "
        "accumulation. Our tempo analysis showed that the spending-to-outcome "
        "lag mu_H drifts at +0.15 years/year, meaning current spending accumulates "
        "into a health-capital stock whose returns manifest in future periods. "
        "Evaluating by period outcomes alone thus underestimates the true return."
    )
    add_para(doc, "The integrated sustainability criterion can be written as:")
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = p.add_run(
        "Total Return = Demand Return (tau * m * E) + Supply Return (dGDP/dH * delta_H)\n"
        ">= Public Cost (pf * E)"
    )
    run.bold = True
    run.font.size = Pt(10)

    # ---------- 4. Cross-country evidence ----------
    add_heading(doc, "4. Cross-Country Evidence", level=1)
    add_para(doc,
        "Figure 2 shows the relationship between healthcare expenditure "
        "(% of GDP) and life expectancy across OECD countries{10,12}. The "
        "quadratic fit reveals a diminishing relationship, where additional "
        "spending beyond a certain level yields smaller life-expectancy gains. "
        "However, this apparent diminishing return may reflect the tempo effect "
        "(lengthening lag) rather than genuine inefficiency."
    )

    add_figure(doc, get_fig("fig2_che_vs_lifeexp.png"),
               "Figure 2. Healthcare Spending (% GDP) vs Life Expectancy (OECD, 2019)")

    add_para(doc,
        "The US spends 17% of GDP on healthcare yet has below-OECD-average life "
        "expectancy — the textbook example of 'inefficiency.' From a neutral "
        "perspective, however: (1) the I-O multiplier of 1.7 generates approximately "
        "$1.0 trillion in additional output annually, and (2) the tempo drift "
        "suggests a portion of spending accumulates into future health capital. "
        "The issue is not the volume of spending but its composition — the shift "
        "from curative-heavy toward prevention and R&D is key{1,10}."
    )

    # ---------- 5. Discussion ----------
    add_heading(doc, "5. Discussion", level=1)

    add_heading(doc, "5.1 Paradigm Shift: From Cost to Investment", level=2)
    add_para(doc,
        "The conventional paradigm treating healthcare as a 'cost' ignores both "
        "its demand-side economic-multiplier effect and its supply-side "
        "health-capital accumulation effect. Under the neutral criterion proposed "
        "here, demand-side tax revenues alone recover 76-118% of public healthcare "
        "expenditure across nine countries, with three exceeding full recovery. "
        "When supply-side returns from health-capital accumulation are included, "
        "comprehensive sustainability likely holds for the majority. This implies "
        "that blanket cost-containment policies may inadvertently reduce economic "
        "output, employment, and tax revenue."
    )

    add_heading(doc, "5.2 Implications of the Japan-US Comparison", level=2)
    add_para(doc,
        "Japan's high multiplier (2.78) likely reflects universal health insurance "
        "ensuring broad access, and a domestic concentration of pharmaceutical and "
        "medical-device industries. The US's lower multiplier (1.7) reflects "
        "leakage through high drug prices and insurance administrative costs "
        "accruing to overseas firms and insurer profits{3}. The difference in "
        "multipliers points to institutional design improvements, not to healthcare "
        "spending itself being 'too high.'"
    )

    add_heading(doc, "5.3 Limitations and Future Directions", level=2)
    add_para(doc,
        "Several limitations apply. First, I-O multipliers are static models that "
        "do not account for price adjustments or supply constraints. Second, the "
        "fiscal return ratio depends on the effective tax rate parameter, requiring "
        "further refinement for robust international comparisons. Third, the tempo "
        "drift mu_H is a proxy for health-capital accumulation; direct causal "
        "inference requires additional identification strategies. Future work will "
        "use OECD SHA (System of Health Accounts) functional expenditure data to "
        "estimate bucket-specific multipliers (Candidate D-H) and determine which "
        "types of healthcare spending yield the highest returns."
    )

    # ---------- 6. Conclusion ----------
    add_heading(doc, "6. Conclusion", level=1)
    add_para(doc,
        "Healthcare expenditure is simultaneously a 'cost' and an 'economic effect.' "
        "I-O multipliers demonstrate that healthcare spending generates 1.7 to 2.9 "
        "times its value in economic output through direct, indirect, and induced "
        "effects. HLGH studies confirm bidirectional causality between health "
        "expenditure and GDP growth. Tempo analysis shows that contemporaneous "
        "flow indicators underestimate investment returns. Under the demand-side "
        "fiscal return ratio, three of nine countries exceed 1.0, and all nine "
        "recover at least 76% of public costs from demand-side tax revenues alone "
        "— before accounting for supply-side health-capital returns. "
        "The policy debate should shift from 'how to contain costs' to "
        "'how to maximize the economic return on healthcare investment.'"
    )

    # ---------- References ----------
    add_heading(doc, "References", level=1)
    for i, ref in enumerate(REFERENCES, 1):
        p = doc.add_paragraph()
        run = p.add_run(f"{i}. ")
        run.bold = True
        run.font.size = Pt(9)
        run2 = p.add_run(ref)
        run2.font.size = Pt(9)

    out_path = os.path.join(DOCX_DIR, "Healthcare_Economic_Effect_EN.docx")
    doc.save(out_path)
    print(f"Saved: {out_path}")
    return out_path


def build_en_pptx():
    prs = Presentation()
    prs.slide_width = PptxInches(13.333)
    prs.slide_height = PptxInches(7.5)

    figures = [
        ("fig1_io_multipliers.png",
         "Figure 1. Healthcare I-O Multipliers by Country",
         "Healthcare sector input-output multipliers. Japan leads at 2.78x. Sources: Yamada & Imanaka 2015, et al."),
        ("fig2_che_vs_lifeexp.png",
         "Figure 2. Healthcare Spending (% GDP) vs Life Expectancy (OECD, 2019)",
         "X-axis: CHE as % of GDP. Y-axis: Life expectancy at birth (years). Quadratic fit shows diminishing returns."),
        ("fig3_fiscal_sustainability.png",
         "Figure 3. Fiscal Return Ratio of Healthcare Spending",
         "Fiscal Return Ratio = (Effective tax rate x I-O multiplier) / Public share. Values >= 1.0 indicate fiscal self-sustainability."),
        ("fig4_dual_return_schematic.png",
         "Figure 4. Dual-Return Framework for Neutral Sustainability",
         "Healthcare spending generates returns through two channels: demand-side (I-O multiplier) and supply-side (health-capital tempo effect)."),
    ]

    for fname, title, caption in figures:
        path = get_fig(fname)
        create_pptx_slide(prs, path, title, caption)

    out_path = os.path.join(PPTX_DIR, "Healthcare_Economic_Effect_Figures_EN.pptx")
    prs.save(out_path)
    print(f"Saved: {out_path}")
    return out_path


if __name__ == "__main__":
    build_en_docx()
    build_en_pptx()
