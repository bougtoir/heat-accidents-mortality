#!/usr/bin/env python3
"""
Cover Letter for Water Alternatives — Research Article
British English, formal academic style
"""

from docx import Document
from docx.shared import Pt, Mm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH

OUTDIR = "/home/ubuntu/repos/wip/flood-prediction-review"

doc = Document()

# Page setup (A4)
section = doc.sections[0]
section.page_width = Mm(210)
section.page_height = Mm(297)
section.top_margin = Mm(25)
section.bottom_margin = Mm(25)
section.left_margin = Mm(25)
section.right_margin = Mm(25)

# Style
style = doc.styles["Normal"]
style.font.name = "Verdana"
style.font.size = Pt(10)
style.paragraph_format.line_spacing = Pt(18)
style.paragraph_format.space_after = Pt(6)


def add_para(text, bold=False, italic=False, alignment=None, space_before=0,
             space_after=6, font_size=10, color=None):
    p = doc.add_paragraph()
    if alignment:
        p.alignment = alignment
    p.paragraph_format.space_before = Pt(space_before)
    p.paragraph_format.space_after = Pt(space_after)
    run = p.add_run(text)
    run.font.name = "Verdana"
    run.font.size = Pt(font_size)
    run.bold = bold
    run.italic = italic
    if color:
        run.font.color.rgb = color
    return p


def add_placeholder(text):
    return add_para(text, color=RGBColor(255, 0, 0))


# ── Date ──
add_placeholder("[Date]")

# ── Recipient ──
add_para("")
add_para("Managing Editor")
add_para("Water Alternatives")
add_para("managing_editor@water-alternatives.org")

# ── Subject ──
add_para("")
add_para(
    "Re: Submission of Research Article — "
    "\"Unilateral flood control through subsurface storage management: "
    "A hydro-political analysis of planned-release hydropower and "
    "inter-watershed groundwater transfer\"",
    bold=True
)

# ── Salutation ──
add_para("")
add_para("Dear Managing Editor,")

# ── Body paragraph 1: Introduction ──
add_para("")
add_para(
    "We are pleased to submit the enclosed manuscript, entitled "
    "\"Unilateral flood control through subsurface storage management: "
    "A hydro-political analysis of planned-release hydropower and "
    "inter-watershed groundwater transfer\", for consideration as a "
    "Research Article in Water Alternatives."
)

# ── Body paragraph 2: Summary of the paper ──
add_para(
    "This paper proposes and analyses a novel flood control framework that "
    "integrates planned-release hydropower generation, inter-watershed "
    "groundwater pumping, and managed aquifer recharge into a single "
    "energy-positive system. The key contribution to the water governance "
    "literature is the concept of 'unilateral treatability' — the "
    "demonstration that downstream nations can implement effective flood "
    "control measures using subsurface storage within their own "
    "jurisdiction, without requiring upstream cooperation or transboundary "
    "agreements."
)

# ── Body paragraph 3: Relevance to Water Alternatives ──
add_para(
    "We believe this manuscript is well suited to Water Alternatives for "
    "several reasons. First, it engages directly with the hydro-hegemony "
    "framework (Zeitoun and Warner, 2006), challenging the assumption that "
    "downstream states are inherently disadvantaged in transboundary flood "
    "management. Second, it bridges the gap between technical feasibility "
    "analysis and water governance scholarship, demonstrating how "
    "engineering innovation can reshape political dynamics in contested "
    "river basins. Third, the paper discusses implications for multiple "
    "transboundary systems — including the Mekong, Nile, "
    "Ganges-Brahmaputra-Meghna, Indus, Tigris-Euphrates, and Jordan "
    "basins — as well as deltaic and arid-region applications, making it "
    "relevant to Water Alternatives' global readership."
)

# ── Body paragraph 4: Technical proof ──
add_para(
    "The paper provides quantitative feasibility analysis using two "
    "Japanese case studies: the Oda River–Takahashi River basin (site of "
    "the devastating 2018 Western Japan floods) and the Tokyo metropolitan "
    "area (Arakawa–Edogawa basin, 8.21 million people in projected "
    "inundation zones). These case studies demonstrate that the proposed "
    "framework is energy self-sufficient (generating 41.7 MW while "
    "consuming only 3.68 MW for pumping) and can provide significant flood "
    "volume reduction (12.0 × 10⁶ m³ of subsurface storage capacity)."
)

# ── Body paragraph 5: Novelty ──
add_para(
    "To the best of our knowledge, this is the first paper to analyse the "
    "hydro-political implications of subsurface flood storage as a tool "
    "for autonomous downstream adaptation in transboundary contexts. While "
    "managed aquifer recharge and pumped-storage hydropower are individually "
    "well-established technologies, their integration into a framework "
    "specifically designed to circumvent upstream-downstream power "
    "asymmetries has not previously been explored in the water governance "
    "literature."
)

# ── Body paragraph 6: Related submissions ──
add_para(
    "Disclosure of related submissions: A related manuscript focusing on "
    "quantitative engineering analysis (energy balance calculations, "
    "hydrograph simulation, and infrastructure design parameters) is being "
    "submitted to the Journal of JSCE (Special Issue: Hydroscience and "
    "Hydraulic Engineering, B1). The Journal of JSCE manuscript is a "
    "technical engineering paper with minimal overlap in governance content. "
    "The Water Alternatives manuscript presented here focuses on water "
    "governance, hydro-hegemony theory, and international policy "
    "implications, with technical details included only to support the "
    "governance argument."
)

# ── Body paragraph 7: Confirmations ──
add_para(
    "We confirm that this manuscript has not been published previously and "
    "is not under consideration for publication elsewhere in its current "
    "form. All authors have approved the manuscript and agree to its "
    "submission to Water Alternatives. We have no conflicts of interest to "
    "declare."
)

# ── Body paragraph 8: AI declaration ──
add_para(
    "AI use declaration: Generative AI tools were used to assist with "
    "literature search, data analysis, and manuscript drafting. All content "
    "has been verified, edited, and approved by the authors, who take full "
    "responsibility for the accuracy and integrity of the work."
)

# ── Closing ──
add_para("")
add_para(
    "We look forward to hearing from you regarding the suitability of this "
    "manuscript for Water Alternatives."
)

add_para("")
add_para("Yours sincerely,")

add_para("")
add_placeholder("[Corresponding Author Name]")
add_placeholder("[Position]")
add_placeholder("[Affiliation]")
add_placeholder("[City, Country]")
add_placeholder("[Email]")
add_placeholder("[ORCID (if available)]")

# ── Save ──
outpath = f"{OUTDIR}/waa_cover_letter.docx"
doc.save(outpath)
print(f"WaA cover letter saved: {outpath}")
