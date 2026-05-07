"""Create Population Studies cover letter — English (.docx)."""
import os
from docx import Document
from docx.shared import Pt, Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
OUT_DIR = os.path.join(os.path.dirname(SCRIPT_DIR), 'manuscripts')
os.makedirs(OUT_DIR, exist_ok=True)


def add_para(doc, text, bold=False, italic=False, size=12, align=None,
             space_after=6):
    p = doc.add_paragraph()
    run = p.add_run(text)
    run.font.size = Pt(size)
    run.bold = bold
    run.italic = italic
    if align:
        p.alignment = align
    p.paragraph_format.space_after = Pt(space_after)
    return p


doc = Document()
for section in doc.sections:
    section.top_margin = Cm(2.54)
    section.bottom_margin = Cm(2.54)
    section.left_margin = Cm(2.54)
    section.right_margin = Cm(2.54)
style = doc.styles['Normal']
style.font.name = 'Times New Roman'
style.font.size = Pt(12)
style.paragraph_format.line_spacing = 1.5

# Date
add_para(doc, "[Date]", size=12, space_after=12)

# Addressee
add_para(doc, "The Editors", bold=True, size=12, space_after=2)
add_para(doc, "Population Studies", italic=True, size=12, space_after=2)
add_para(doc, "Population Investigation Committee", size=12, space_after=2)
add_para(doc, "London School of Economics and Political Science",
         size=12, space_after=18)

add_para(doc, "Dear Editors,", size=12, space_after=12)

add_para(doc,
    "We are pleased to submit our manuscript entitled \u201cQuantifying the Tempo Effect on "
    "Simultaneously Living Population: Evidence from 40 Countries, 1970\u20132023\u201d for "
    "consideration as a research article in Population Studies.",
    size=12, space_after=12)

# What the paper does
add_para(doc,
    "This paper provides the first systematic cross-national quantification of the tempo "
    "effect on simultaneously living population (SLP). While the theoretical link between "
    "birth timing and population size has been established\u2014notably by Goldstein, Lutz, "
    "and Scherbov (2003) in this journal\u2019s intellectual tradition\u2014no study has "
    "measured this effect against observed population data across diverse demographic "
    "contexts. Using a parsimonious endogenous renewal model validated against UN WPP 2024 "
    "data for 40 countries over half a century, we make three contributions:",
    size=12, space_after=8)

add_para(doc,
    "(1) We quantify the independent tempo effect on SLP through counterfactual analysis, "
    "finding that the observed 4\u20136 year rise in mean age at childbearing across OECD "
    "countries independently reduced SLP by 8\u201317%\u2014equivalent to 15\u201340 years of "
    "below-replacement fertility.\n\n"
    "(2) We decompose population change into quantum, tempo, and survival components, "
    "showing that tempo is typically the second-largest contributor to population change "
    "in post-transitional countries.\n\n"
    "(3) We demonstrate that higher MAC accelerates the annual pace of population decline, "
    "compressing the time available for institutional adaptation.",
    size=12, space_after=12)

# Why Population Studies
add_para(doc,
    "We believe Population Studies is the ideal venue for this work. The journal\u2019s "
    "long tradition of publishing foundational contributions on fertility tempo and "
    "formal demography\u2014including the Bongaarts\u2013Feeney framework and related work on "
    "demographic translation\u2014means that the readership is uniquely positioned to "
    "evaluate and build upon our findings.",
    size=12, space_after=12)

# Disclosure of prior submissions
add_para(doc, "Prior submissions", bold=True, size=12, space_after=6)
add_para(doc,
    "In the interest of transparency, we disclose that earlier versions of this manuscript "
    "were submitted to and declined by three journals:",
    size=12, space_after=6)
add_para(doc,
    "\u2022 The Lancet: Declined at pre-review (outside scope for a clinical journal).\n"
    "\u2022 Population and Development Review: Declined at pre-review.\n"
    "\u2022 Demographic Research: Declined at pre-review. The editor noted that while "
    "the manuscript was readable, the structure did not yet support the central claims, "
    "results were focused mainly on model fit, and the contribution appeared too limited "
    "for a full research article given that the core mechanism is already established.",
    size=12, space_after=12)

add_para(doc,
    "We have substantially revised the manuscript in response to the Demographic Research "
    "feedback. The key changes are: (a) restructured from a model-validation paper to "
    "a substantive findings paper, with counterfactual tempo analysis and component "
    "decomposition as the main results; (b) added systematic quantification of the "
    "tempo effect through country-level counterfactuals; (c) added decomposition of "
    "population change into quantum, tempo, and survival components; (d) empirically "
    "grounded the pace-of-adaptation argument; and (e) repositioned the model validation "
    "as supporting evidence rather than the primary result.",
    size=12, space_after=12)

# Formalities
add_para(doc,
    "The manuscript has not been published elsewhere and is not under consideration by "
    "any other journal. All authors have approved the manuscript and agree to its "
    "submission. The authors declare no conflicts of interest.",
    size=12, space_after=12)

add_para(doc,
    "We look forward to your consideration.",
    size=12, space_after=18)

add_para(doc, "Yours sincerely,", size=12, space_after=6)
add_para(doc, "[Author name(s)]", size=12, space_after=2)
add_para(doc, "[Institutional affiliation]", size=12, space_after=2)
add_para(doc, "[Email address]", size=12, space_after=2)

outpath = os.path.join(OUT_DIR, 'CoverLetter_PopStudies_EN.docx')
doc.save(outpath)
print(f'OK: {outpath}')
