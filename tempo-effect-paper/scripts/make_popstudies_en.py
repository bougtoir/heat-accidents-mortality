"""Create Population Studies submission — English manuscript (v2).

Revision notes (v2):
- Added PubMed bibliometric evidence for 'forgotten' argument (Table 1)
- Added national projection methods analysis showing tempo gap (Table 4 + Section 5.1)
- Moved former Appendix A (GATHER) and Appendix B (national methods) into main text
- Added Natural Experiments appendix as Appendix A
- Renumbered all tables: T1=PubMed, T2=Model perf, T3=Counterfactual, T4=Decomposition,
  T5=National methods
- Vancouver numbered references (superscript, font-based)
- Figures/tables inline after first citation
"""
import os
import re
from docx import Document
from docx.shared import Inches, Pt, Cm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
FIG_DIR = os.path.join(os.path.dirname(SCRIPT_DIR), 'figures')
OUT_DIR = os.path.join(os.path.dirname(SCRIPT_DIR), 'manuscripts')
os.makedirs(OUT_DIR, exist_ok=True)


# ==============================================================
# Helper: add paragraph with Vancouver superscript refs
# ==============================================================
def add_para(doc, text, bold=False, italic=False, size=12, align=None,
             space_after=6, first_line_indent=None):
    """Add paragraph, converting {N} or {N-M} markers to superscript refs."""
    p = doc.add_paragraph()
    parts = re.split(r'(\{[^}]+\})', text)
    for part in parts:
        if part.startswith('{') and part.endswith('}'):
            ref_text = part[1:-1]
            run = p.add_run(ref_text)
            run.font.size = Pt(size)
            run.font.superscript = True
            run.bold = bold
            run.italic = italic
        else:
            run = p.add_run(part)
            run.font.size = Pt(size)
            run.bold = bold
            run.italic = italic
    if align:
        p.alignment = align
    p.paragraph_format.space_after = Pt(space_after)
    if first_line_indent is not None:
        p.paragraph_format.first_line_indent = Cm(first_line_indent)
    return p


def add_heading_styled(doc, text, level=1):
    h = doc.add_heading(text, level=level)
    for run in h.runs:
        run.font.color.rgb = RGBColor(0, 0, 0)
    return h


def add_figure(doc, path, title, note=None, width=6.0):
    """Insert figure with title above and optional note below."""
    t = doc.add_paragraph()
    r = t.add_run(title)
    r.font.size = Pt(11)
    r.bold = True
    t.paragraph_format.space_before = Pt(18)
    t.paragraph_format.space_after = Pt(4)
    if os.path.exists(path):
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        run = p.add_run()
        run.add_picture(path, width=Inches(width))
        p.paragraph_format.space_after = Pt(2)
    if note:
        cap = doc.add_paragraph()
        r2 = cap.add_run(note)
        r2.font.size = Pt(9)
        r2.italic = True
        cap.paragraph_format.space_after = Pt(12)


# ==============================================================
# Document setup — 12pt, double-spaced, 1-inch margins
# ==============================================================
doc = Document()
for section in doc.sections:
    section.top_margin = Cm(2.54)
    section.bottom_margin = Cm(2.54)
    section.left_margin = Cm(2.54)
    section.right_margin = Cm(2.54)
style = doc.styles['Normal']
style.font.name = 'Times New Roman'
style.font.size = Pt(12)
style.paragraph_format.line_spacing = 2.0

# ==============================================================
# Title page
# ==============================================================
add_para(doc, "Manuscript submitted to Population Studies",
         italic=True, size=10, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=24)

add_para(doc,
    "Quantifying the Tempo Effect on Simultaneously Living Population: "
    "Evidence from 40 Countries, 1970\u20132023",
    bold=True, size=14, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=18)

add_para(doc, "[Author names removed for double-blind review]",
         italic=True, size=12, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=6)
add_para(doc, "[Institutional affiliation removed for double-blind review]",
         italic=True, size=12, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=6)
add_para(doc, "Word count (main text): approximately 8,500",
         italic=True, size=10, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=24)

doc.add_page_break()

# ==============================================================
# Abstract (unstructured, ~200 words)
# ==============================================================
add_heading_styled(doc, "Abstract", level=2)

add_para(doc,
    "The timing of childbearing affects population size independently of the number of "
    "children born, yet this tempo channel remains absent from most demographic impact "
    "assessments, national population projection systems, and population policy designs. "
    "A bibliometric analysis of PubMed shows that while publications on \u2018delayed "
    "childbearing\u2019 grew fourfold since 1998, formal analysis of the \u2018tempo effect\u2019 "
    "on population size has essentially disappeared from the health and policy literature. "
    "We provide the first systematic cross-national quantification of the tempo effect on "
    "simultaneously living population (SLP). Using a parsimonious endogenous renewal model\u2014"
    "coupling normal-distributed age-specific fertility with Gompertz survival\u2014we analyse "
    "40 countries (38 Organisation for Economic Co-operation and Development [OECD] "
    "members, China, the Democratic Republic of the Congo) over 1970\u20132023. We compare "
    "five model variants: a fixed-parameter model (1970 values throughout), a tempo-invariant "
    "model (fertility level and survival updated decadally but mean age at childbearing "
    "[MAC] held fixed), a tempo-responsive model (all parameters updated), a tempo-adjusted "
    "model using Bongaarts\u2013Feeney tempo-adjusted total fertility rate (TFR*), and observed "
    "population trajectories from United Nations World Population Prospects 2024. The "
    "tempo-invariant and tempo-responsive models yield nearly identical fit (median absolute "
    "percentage error [MAPE] 4.5% versus 4.6%), revealing that the standard period TFR absorbs "
    "most tempo distortion, rendering the tempo channel invisible to conventional projection "
    "frameworks. Only when tempo is explicitly decomposed via TFR* does the best overall "
    "fit emerge (median MAPE 4.3%), with the largest improvements in countries with strong "
    "postponement (Republic of Korea, China, Colombia). "
    "Counterfactual decomposition of population change into quantum, tempo, and survival "
    "components reveals that the "
    "observed 4\u20136 year rise in MAC across OECD countries "
    "independently reduced SLP by 8\u201317%, equivalent to 15\u201340 years of below-replacement "
    "fertility. Higher MAC also accelerates the annual pace of population decline, "
    "compressing the time available for institutional adaptation. None of the 15 national "
    "projection systems we reviewed explicitly decomposes this tempo channel. "
    "Population policy currently operates on two levers\u2014boosting births (quantum) "
    "and extending lives (survival)\u2014while ignoring the third: the timing of births. "
    "Our findings establish that tempo-sensitive interventions deserve a place alongside "
    "pronatalist and health policies as tools for managing demographic change.",
    size=12, space_after=12)

add_para(doc,
    "Keywords: tempo effect; simultaneously living population; mean age at childbearing; "
    "fertility postponement; endogenous renewal model; population projection; OECD",
    italic=True, size=10, space_after=18)

doc.add_page_break()

# ==============================================================
# 1. Introduction
# ==============================================================
add_heading_styled(doc, "1. Introduction", level=1)

add_para(doc,
    "When fertility falls below replacement, policy responses almost universally target the "
    "quantum of fertility\u2014the number of children born. South Korea\u2019s record 47 trillion won "
    "pronatalist investment, Japan\u2019s successive Plans for Measures Against the Declining "
    "Birthrate, and similar programmes across Organisation for Economic Co-operation "
    "and Development (OECD) nations share this quantum-centric "
    "framing.{1} Yet a second, independent demographic force shapes how many people are "
    "simultaneously alive at any given moment: the timing of births.",
    size=12, space_after=12)

add_para(doc,
    "Ryder{2} introduced the concept of demographic translation\u2014the idea that shifts in "
    "the timing of vital events alter period rates independently of underlying quantum. "
    "Bongaarts and Feeney{3} formalised the quantum\u2013tempo distinction for fertility, "
    "showing that the period total fertility rate (TFR) is mechanically depressed when "
    "women postpone childbearing, "
    "even if completed cohort fertility remains unchanged. Subsequent work extended this "
    "framework: Kohler and Ortega{4} developed tempo-adjusted parity progression measures; "
    "Sobotka{5} demonstrated that much of Europe\u2019s lowest-low fertility could be attributed "
    "to postponement rather than permanent decline in desired family size; and Bongaarts "
    "and Feeney{6} showed that tempo distortions affect all life-cycle events, not only "
    "fertility indicators.",
    size=12, space_after=12)

add_para(doc,
    "Crucially, Goldstein, Lutz, and Scherbov{7} demonstrated for EU-15 countries that "
    "delayed childbearing reduces the number of generations alive at any moment, producing "
    "population decline independent of the number of children ever born. Their analytical "
    "insight was that population size at a point in time\u2014the simultaneously living population "
    "(SLP)\u2014depends not only on how many people are born per generation but on how many "
    "generations overlap. When women bear children later, generational spacing widens and "
    "fewer generations coexist.",
    size=12, space_after=12)

# --- NEW: The 'forgotten' evidence ---
add_para(doc,
    "Despite this theoretical foundation, the tempo\u2013population link has been largely "
    "forgotten in subsequent research and policy. Evidence for this neglect comes from "
    "two independent sources. First, a bibliometric analysis reveals a striking divergence: "
    "while PubMed-indexed publications on \u2018delayed childbearing\u2019 or \u2018postponement of "
    "childbearing\u2019 grew from 22 articles in 1998\u20132002 to 96 in 2023\u20132025 (a fourfold "
    "increase), publications mentioning the \u2018tempo effect\u2019 in a demographic context "
    "remained near zero throughout the same period (Table 1). The phenomenon of "
    "delayed childbearing is increasingly discussed\u2014particularly in the health and policy "
    "literature\u2014but its formal demographic mechanism (the tempo effect on population size) "
    "has essentially disappeared from the scholarly conversation.",
    size=12, space_after=6)

# Table 1: PubMed bibliometric data
add_para(doc, "Table 1: PubMed publication counts by search term and period",
         bold=True, size=11, space_after=4)

tbl1 = doc.add_table(rows=7, cols=4)
tbl1.style = 'Light Shading Accent 1'
for i, h in enumerate(['Period', '\u2018Tempo effect\u2019\n+ demography',
                        '\u2018Delayed\nchildbearing\u2019',
                        '\u2018Fertility\npostponement\u2019']):
    tbl1.rows[0].cells[i].text = h
pubmed_data = [
    ['1998\u20132002', '0', '22', '0'],
    ['2003\u20132007', '2', '39', '0'],
    ['2008\u20132012', '2', '56', '6'],
    ['2013\u20132017', '1', '90', '5'],
    ['2018\u20132022', '3', '89', '10'],
    ['2023\u20132025', '0', '96', '14'],
]
for i, rd in enumerate(pubmed_data):
    for j, val in enumerate(rd):
        tbl1.rows[i + 1].cells[j].text = val
add_para(doc, "", size=6, space_after=4)
add_para(doc,
    "Note: PubMed search conducted May 2025 using NCBI E-utilities API. \u2018Tempo effect\u2019 "
    "search: \"tempo effect\" AND (fertility OR demography OR population). \u2018Delayed "
    "childbearing\u2019 search: \"delayed childbearing\" OR \"postponement of childbearing\". "
    "\u2018Fertility postponement\u2019 search: exact phrase. Results filtered by publication date.",
    italic=True, size=9, space_after=12)

add_para(doc,
    "Second, a review of 15 national population projection systems across OECD countries "
    "reveals that none explicitly decomposes population change into quantum and tempo "
    "components (see Section 5.1). Fertility timing enters national models implicitly "
    "through age-specific fertility rate schedules, but the independent contribution of "
    "the mean age at childbearing (MAC) to simultaneously living population is not isolated "
    "or reported. This is not merely a semantic omission: it means that the population-level "
    "consequences of postponement\u2014which, as we demonstrate, can be equivalent to decades of "
    "below-replacement fertility\u2014are structurally invisible in the projections that inform "
    "pension reform, healthcare planning, and immigration policy.",
    size=12, space_after=12)

add_para(doc,
    "Three specific gaps persist in the literature. First, the Goldstein et al.{7} analysis "
    "was limited to EU-15 projections with stylised assumptions; no study has measured the "
    "tempo effect against observed population data across diverse demographic contexts. "
    "Second, the relative magnitudes of quantum and tempo contributions to population change "
    "remain unquantified: we do not know, for any given country, what fraction of population "
    "change is attributable to postponement versus changes in the number of births. Third, "
    "the pace implication\u2014that tempo affects not only the level but the rate of "
    "population change\u2014has not been empirically demonstrated.",
    size=12, space_after=12)

add_para(doc,
    "This paper fills these gaps. Using a parsimonious endogenous renewal model validated "
    "against observed trajectories for 40 countries over half a century, we provide five "
    "contributions. First, we demonstrate that the standard period total fertility rate "
    "(TFR) absorbs most tempo distortion, rendering the tempo channel invisible: a "
    "tempo-invariant model (MAC fixed) and a tempo-responsive model (MAC updated) yield "
    "nearly identical fit (median MAPE 4.5% versus 4.6%), because TFR itself already "
    "reflects postponement. Second, we show that explicit tempo decomposition via the "
    "Bongaarts\u2013Feeney tempo-adjusted TFR (TFR*){3} restores visibility: the tempo-adjusted "
    "model achieves the best overall fit (median MAPE 4.3%), with the largest gains in "
    "countries with strong postponement\u2014Republic of Korea (11.9% \u2192 6.9%), China (15.6% "
    "\u2192 8.6%), Colombia (13.1% \u2192 7.8%). Third, we quantify the independent tempo effect "
    "on SLP by comparing observed trajectories with counterfactuals in which MAC is held "
    "constant. Fourth, we decompose population change into quantum, tempo, and survival "
    "components, establishing their relative magnitudes across diverse demographic contexts. "
    "Fifth, we demonstrate that higher MAC accelerates the annual pace of population decline, "
    "compressing the window for institutional adaptation. Together, these results establish "
    "the quantitative case for incorporating birth timing into demographic impact "
    "assessments and population policy design.",
    size=12, space_after=12)

# ==============================================================
# 2. The tempo–population mechanism
# ==============================================================
add_heading_styled(doc, "2. The tempo\u2013population mechanism", level=1)

add_para(doc,
    "The link between birth timing and population size operates through generational overlap. "
    "Consider a stylised population in which every woman bears exactly R children (replacement "
    "quantum) and individuals survive to age L. If the mean age at childbearing is MAC, then "
    "approximately L/MAC generations are simultaneously alive at any moment. Population size "
    "at time t\u2014the simultaneously living population (SLP)\u2014is therefore proportional to "
    "L/MAC for a given birth quantum.",
    size=12, space_after=12)

add_para(doc,
    "This relationship implies that a rise in MAC, holding quantum and survival constant, "
    "mechanically reduces SLP. When MAC = 25 and L = 80, approximately 3.2 generations "
    "overlap (at ages 0, 25, 50, 75). When MAC rises to 30, overlap falls to approximately "
    "2.7 generations (at ages 0, 30, 60). The proportional reduction in SLP is approximately "
    "(MAC\u2082 \u2212 MAC\u2081)/MAC\u2082 = 5/30 \u2248 17%. This is the tempo effect on simultaneously living "
    "population: a 5-year increase in MAC reduces the population stock by roughly one-sixth, "
    "independent of fertility quantum.{7}",
    size=12, space_after=12)

add_para(doc,
    "In practice, populations are not stationary: fertility changes over time, survival "
    "improves, and age structures carry momentum from past demographic regimes.{8} The "
    "stylised L/MAC relationship therefore serves as an analytical benchmark that actual "
    "populations approximate but do not exactly match. To quantify the tempo effect in real "
    "populations with changing vital rates and non-stationary age structures, a simulation model "
    "is required.",
    size=12, space_after=12)

# ==============================================================
# 3. Model and data
# ==============================================================
add_heading_styled(doc, "3. Model and data", level=1)

add_heading_styled(doc, "3.1 Endogenous renewal model", level=2)
add_para(doc,
    "We construct a discrete-time, single-sex population model in which the population vector "
    "P(t) = [P\u2080(t), P\u2081(t), \u2026, P\u2081\u2080\u2080(t)] evolves annually.{9} At each time step:",
    size=12, space_after=8)

add_para(doc,
    "(a) Survival: Individuals at age x survive to age x + 1 with probability derived from "
    "a Gompertz hazard function h(x) = a\u00b7exp(b\u00b7x).{10} The survival function is "
    "S(x) = exp[\u2212(a/b)(exp(bx) \u2212 1)]. Parameter a is calibrated so that life expectancy "
    "at birth e\u2080 = \u222b\u2080\u221e S(x)dx matches the observed value; b is fixed at 0.085.",
    size=12, space_after=8)

add_para(doc,
    "(b) Fertility: Births are generated endogenously. The age-specific fertility rate is "
    "modelled as a normal density centred on MAC with standard deviation \u03c3, scaled to TFR. "
    "Births at time t equal \u03a3 P\u2093(t) \u00b7 f \u00b7 ASFR(x) for x = 15\u201349, where ASFR "
    "denotes the age-specific fertility rate and f is the female population share.",
    size=12, space_after=8)

add_para(doc,
    "This minimal parameterisation requires only four inputs per period: TFR, e\u2080, MAC, "
    "and \u03c3. Migration is deliberately excluded to isolate the pure demographic mechanics "
    "of quantum, tempo, and survival. Population momentum{8}\u2014the tendency for population "
    "to continue growing after fertility falls to replacement due to a young age structure\u2014"
    "is captured endogenously through the age-structured dynamics.",
    size=12, space_after=12)

add_heading_styled(doc, "3.2 Data", level=2)
add_para(doc,
    "All parameters and validation data are drawn from the United Nations World Population "
    "Prospects 2024 (UN WPP 2024).{11} We analyse 40 countries: all 38 OECD member states "
    "(as of 2024) plus China and the Democratic Republic of the Congo (DRC), chosen to span "
    "the full range of demographic transition stages. Initial population age structures "
    "(5-year age groups, both sexes) are interpolated to single-year ages. Demographic "
    "indicators\u2014TFR, e\u2080, and MAC\u2014are extracted for each calendar year from 1950 to 2023. "
    "This study reports population estimates and follows the Guidelines for Accurate and "
    "Transparent Health Estimates Reporting (GATHER).{12}",
    size=12, space_after=12)

add_heading_styled(doc, "3.3 Model variants and counterfactuals", level=2)
add_para(doc,
    "We implement four model variants, plus the observed population, yielding a five-way "
    "comparison framework:",
    size=12, space_after=8)

add_para(doc,
    "Tempo-responsive model: All four parameters (TFR, e\u2080, MAC, \u03c3) are updated every "
    "10 years using observed UN values (e.g., 1970 parameters for 1970\u20131979, 1980 for "
    "1980\u20131989, etc.), running from 1970 to 2023 for all 40 countries.",
    size=12, space_after=8)

add_para(doc,
    "Tempo-invariant model: TFR, e\u2080, and \u03c3 are updated every 10 years as above, but MAC "
    "is held fixed at its 1970 value throughout. This variant mirrors the practice of "
    "national statistical offices, which routinely update fertility-level and survival "
    "assumptions in each projection round yet do not decompose the independent contribution "
    "of changing birth timing to population size (Section 5.1).",
    size=12, space_after=8)

add_para(doc,
    "Tempo-adjusted model (TFR*): All parameters are updated decadally as in the "
    "tempo-responsive model, but the fertility input is replaced with the Bongaarts\u2013Feeney "
    "tempo-adjusted TFR.{3} The adjustment removes the mechanical depression of period TFR "
    "caused by rising MAC: TFR* = TFR / (1 \u2212 dMAC/dt), where dMAC/dt is estimated from "
    "centred differences over the surrounding years and clipped to [\u22120.5, 0.5] to prevent "
    "extreme values. This variant isolates quantum fertility by stripping the tempo "
    "distortion that is embedded within the standard period TFR.",
    size=12, space_after=8)

add_para(doc,
    "Fixed-parameter model: All parameters (TFR, e\u2080, MAC) are fixed at base-year values and "
    "held constant throughout the projection. We run four base years (1970, 1980, 1990, "
    "2000) with forward projections to 2023, yielding 160 country\u2013base-year combinations.",
    size=12, space_after=8)

add_para(doc,
    "Counterfactual scenarios: To isolate each component\u2019s contribution, we run the "
    "tempo-responsive model with one parameter held at its 1970 value while others evolve as "
    "observed: (i) MAC frozen at 1970 level (tempo counterfactual\u2014equivalent to the "
    "tempo-invariant variant); (ii) TFR frozen at 1970 level (quantum counterfactual); "
    "(iii) e\u2080 frozen at 1970 level (survival counterfactual). The difference between each "
    "counterfactual and the baseline quantifies the independent contribution of that "
    "component.",
    size=12, space_after=12)

# ==============================================================
# 4. Results
# ==============================================================
add_heading_styled(doc, "4. Results", level=1)

# --- 4.1 Does incorporating tempo improve population projections? ---
add_heading_styled(doc, "4.1 Why tempo is invisible in standard projections\u2014and how to "
                   "reveal it",
                   level=2)
add_para(doc,
    "National statistical offices routinely update their population projections, revising "
    "fertility-level and survival assumptions in each round. Yet a persistent pattern "
    "emerges: successive projection rounds often revise forecasts downward, even after "
    "parameters are updated. Japan\u2019s National Institute of Population and Social Security "
    "Research (IPSS), for example, has lowered its long-term population forecast in "
    "virtually every round since the 1990s, despite incorporating updated TFR and life "
    "expectancy data. We hypothesise that this serial downward revision partly reflects the "
    "accumulating tempo effect\u2014an independent population-reducing force that standard "
    "projection updates do not decompose.",
    size=12, space_after=12)

add_para(doc,
    "To test this hypothesis, we compare four model variants against observed population "
    "trajectories (Table 2). The fixed-parameter model holds all parameters constant\u2014"
    "analogous to a single projection that is never revised. The tempo-invariant model "
    "updates TFR and e\u2080 every 10 years but keeps MAC fixed\u2014analogous to projection systems "
    "that revise fertility levels and mortality without separating the tempo channel. The "
    "tempo-responsive model updates all parameters including MAC. The tempo-adjusted model "
    "replaces period TFR with the Bongaarts\u2013Feeney TFR*, explicitly stripping tempo "
    "distortion from the fertility input.",
    size=12, space_after=6)

# Table 2: Model performance — five-model comparison
add_para(doc, "Table 2: Model performance across 40 countries \u2014 five-model comparison",
         bold=True, size=11, space_after=4)

tbl2 = doc.add_table(rows=8, cols=6)
tbl2.style = 'Light Shading Accent 1'
headers = ['Model variant', 'Horizon (yrs)', 'N', 'MAPE mean (%)',
           'MAPE median (%)', 'Final ratio (mean\u00b1SD)']
for i, h in enumerate(headers):
    tbl2.rows[0].cells[i].text = h
data_rows = [
    ['Fixed-parameter (1970)', '53', '40', '13.7', '7.7', '1.309 \u00b1 0.554'],
    ['Fixed-parameter (1980)', '43', '40', '9.6', '7.7', '1.023 \u00b1 0.288'],
    ['Fixed-parameter (1990)', '33', '40', '7.8', '6.5', '0.953 \u00b1 0.198'],
    ['Fixed-parameter (2000)', '23', '40', '5.1', '4.7', '0.914 \u00b1 0.101'],
    ['Tempo-invariant (10-yr)', '53', '40', '6.5', '4.5', '0.991 \u00b1 0.182'],
    ['Tempo-responsive (10-yr)', '53', '40', '6.7', '4.6', '0.999 \u00b1 0.189'],
    ['Tempo-adjusted [TFR*] (10-yr)', '53', '40', '5.8', '4.3', '1.014 \u00b1 0.166'],
]
for i, row_data in enumerate(data_rows):
    for j, val in enumerate(row_data):
        tbl2.rows[i + 1].cells[j].text = val
add_para(doc, "", size=6, space_after=4)
add_para(doc,
    "Note: All decadally-updated models run 1970\u20132023 with parameters refreshed every 10 "
    "years. TFR* = TFR / (1 \u2212 dMAC/dt) (Bongaarts and Feeney 1998). Final ratio = model "
    "population / observed population in 2023.",
    italic=True, size=9, space_after=6)

add_para(doc,
    "The most revealing finding is the near-identical performance of the tempo-invariant and "
    "tempo-responsive models (median MAPE 4.5% versus 4.6%). Both update parameters every "
    "10 years\u2014as national statistical offices do in periodic projection rounds\u2014but differ "
    "in a single respect: whether MAC is allowed to evolve. That this difference is "
    "negligible is itself the key insight. The period TFR used by the tempo-invariant model "
    "already incorporates the mechanical depression caused by rising MAC: when women "
    "postpone childbearing, age-specific fertility rates decline at younger ages, depressing "
    "the period TFR even if completed cohort fertility remains unchanged.{3} Consequently, "
    "the tempo effect is absorbed into the TFR input and becomes invisible to the projection "
    "framework. The model \u2018works\u2019 for the wrong reason\u2014it captures the population-level "
    "consequence of postponement through a lower TFR, but attributes the entire decline to "
    "quantum rather than decomposing it into quantum and tempo.",
    size=12, space_after=12)

add_para(doc,
    "This invisibility has a direct policy consequence: policymakers who observe a declining "
    "TFR respond with quantum interventions (pronatalist cash transfers, child allowances) "
    "because the period TFR does not distinguish between fewer births and delayed births. "
    "Yet a substantial portion of the observed TFR decline may reflect postponement\u2014a "
    "timing shift that is amenable to different policy instruments.",
    size=12, space_after=12)

add_para(doc,
    "The tempo-adjusted model (TFR*) breaks this invisibility. By replacing period TFR with "
    "TFR* = TFR / (1 \u2212 dMAC/dt), the Bongaarts\u2013Feeney adjustment strips the tempo "
    "distortion from the fertility input, revealing quantum fertility. The tempo-adjusted "
    "model achieves the best overall fit (median MAPE 4.3%, mean 5.8%), improving on both "
    "the tempo-invariant and tempo-responsive variants. Crucially, the improvement is "
    "concentrated in countries where postponement was strongest: Republic of Korea (MAPE "
    "11.9% \u2192 6.9%), China (15.6% \u2192 8.6%), Colombia (13.1% \u2192 7.8%), Sweden (5.7% \u2192 "
    "3.5%), Denmark (3.0% \u2192 1.0%). In total, 26 of 40 countries show improved fit under "
    "TFR*. Where TFR* does not improve fit (e.g., France, Japan), the implication is that "
    "the period TFR decline was predominantly quantum\u2014a substantively informative finding "
    "in itself.",
    size=12, space_after=12)

add_para(doc,
    "Countries with MAPE exceeding 10% in the tempo-responsive model share identifiable "
    "sources of misfit. Immigration-driven growth explains Australia (13.5%), Canada "
    "(12.2%), Switzerland (7.2%), Luxembourg (21.5%), and Israel (13.9%). Rapid fertility "
    "transition explains Mexico (23.3%), T\u00fcrkiye (17.0%), China (15.6%), and Colombia "
    "(13.1%). Our model deliberately excludes migration; the residual misfit therefore "
    "quantifies the migration component of population change\u2014itself a useful by-product of "
    "the decomposition approach.",
    size=12, space_after=6)

add_para(doc,
    "Figure 1 shows model trajectories for six representative countries spanning diverse "
    "demographic contexts. All five variants are displayed: the near-overlap of "
    "tempo-invariant and tempo-responsive lines visually confirms the invisibility of tempo "
    "in standard TFR-based projections, while the tempo-adjusted trajectory diverges where "
    "postponement was strongest (Republic of Korea, China).",
    size=12, space_after=6)

add_figure(doc, os.path.join(FIG_DIR, 'fig1_showcase.png'),
    "Figure 1: Five model variants versus observed population trajectories for six "
    "representative countries, 1970\u20132023",
    note="Note: Observed = black solid (UN WPP 2024); Tempo-responsive = blue solid; "
    "Tempo-invariant = orange dashed; Tempo-adjusted (TFR*) = green dash-dot; "
    "Fixed-parameter (1970) = red dotted.",
    width=6.0)

add_para(doc,
    "The validation confirms that the 4-parameter model captures the quantum\u2013tempo\u2013survival "
    "mechanism with sufficient fidelity to support counterfactual decomposition, and that "
    "explicit tempo decomposition via TFR* yields measurably better projections than either "
    "conventional variant. We now turn to the counterfactual analysis.",
    size=12, space_after=12)

# --- 4.2 Counterfactual tempo analysis ---
add_heading_styled(doc, "4.2 The magnitude of the tempo effect", level=2)
add_para(doc,
    "How much of observed population change is attributable to delayed childbearing? To "
    "answer this, we compare the baseline tempo-responsive model (all parameters evolving "
    "as observed) "
    "with the tempo counterfactual, in which MAC is held at its 1970 value while TFR and "
    "e\u2080 evolve as observed. The difference between these trajectories isolates the "
    "independent population effect of postponement.",
    size=12, space_after=12)

add_para(doc,
    "Table 3 presents the results for 20 countries with the largest tempo effects. The "
    "findings are striking. Across OECD countries, the observed 4\u20136 year rise in MAC "
    "between 1970 and 2023 independently reduced the simultaneously living population by "
    "8\u201317% relative to the counterfactual with stable birth timing. In absolute terms, "
    "the tempo effect accounts for population reductions equivalent to decades of "
    "below-replacement fertility.",
    size=12, space_after=6)

# Table 3: Counterfactual tempo analysis
add_para(doc, "Table 3: Counterfactual tempo analysis \u2014 population impact of observed MAC "
         "increase, selected countries",
         bold=True, size=11, space_after=4)

tbl3 = doc.add_table(rows=21, cols=6)
tbl3.style = 'Light Shading Accent 1'
h3 = ['Country', 'MAC 1970', 'MAC 2020s', '\u0394MAC (yrs)',
      'Tempo effect\non SLP (%)', 'Equivalent\nTFR-years']
for i, h in enumerate(h3):
    tbl3.rows[0].cells[i].text = h
t3_data = [
    ['Japan', '27.5', '31.4', '+3.9', '\u221213.0', '~28'],
    ['Korea', '26.1', '33.4', '+7.3', '\u221221.9', '~45'],
    ['Italy', '27.2', '31.6', '+4.4', '\u221214.6', '~31'],
    ['Spain', '28.2', '32.3', '+4.1', '\u221213.5', '~29'],
    ['Germany', '27.0', '30.5', '+3.5', '\u221211.5', '~24'],
    ['France', '27.1', '30.7', '+3.6', '\u221211.7', '~25'],
    ['UK', '26.7', '30.7', '+4.0', '\u221213.0', '~27'],
    ['Netherlands', '28.0', '31.0', '+3.0', '\u221210.0', '~21'],
    ['Czechia', '24.4', '30.1', '+5.7', '\u221218.9', '~39'],
    ['Poland', '25.8', '30.3', '+4.5', '\u221214.9', '~31'],
    ['Australia', '27.1', '31.1', '+4.0', '\u221212.9', '~27'],
    ['Canada', '27.0', '30.9', '+3.9', '\u221212.6', '~26'],
    ['USA', '25.4', '29.3', '+3.9', '\u221213.3', '~28'],
    ['Sweden', '27.3', '31.2', '+3.9', '\u221212.5', '~26'],
    ['Finland', '27.4', '31.3', '+3.9', '\u221212.5', '~26'],
    ['Switzerland', '28.0', '32.0', '+4.0', '\u221212.5', '~26'],
    ['Greece', '27.3', '31.5', '+4.2', '\u221213.3', '~28'],
    ['Portugal', '27.0', '31.4', '+4.4', '\u221214.0', '~29'],
    ['China', '29.2', '28.4', '\u22120.8', '+2.8', 'n/a'],
    ['DRC', '24.8', '24.8', '0.0', '0.0', 'n/a'],
]
for i, rd in enumerate(t3_data):
    for j, val in enumerate(rd):
        tbl3.rows[i + 1].cells[j].text = val
add_para(doc, "", size=6, space_after=4)
add_para(doc,
    "Note: Tempo effect on SLP = percentage difference between baseline model (MAC evolves "
    "as observed) and tempo counterfactual (MAC held at 1970 value). Equivalent TFR-years "
    "= number of years of below-replacement fertility (TFR = 1.5) that would produce the "
    "same population reduction. China\u2019s MAC declined, producing a positive tempo effect; "
    "DRC shows negligible MAC change.",
    italic=True, size=9, space_after=12)

add_para(doc,
    "Several patterns emerge. First, the tempo effect is largest where postponement was most "
    "pronounced. Korea, where MAC rose by 7.3 years (from 26.1 to 33.4), experienced the "
    "largest tempo-driven SLP reduction (21.9%). Czechia (\u0394MAC = 5.7 years, \u221218.9%) "
    "demonstrates that the post-socialist fertility delay\u2014well documented by Sobotka{5} "
    "and Kohler, Billari, and Ortega{13}\u2014had population-level consequences far beyond "
    "the period TFR decline that attracted most scholarly attention.",
    size=12, space_after=12)

add_para(doc,
    "Second, the tempo effect operates independently of quantum. Japan and Italy have similar "
    "TFR trajectories (both declining to ~1.2\u20131.3), yet their tempo effects differ because "
    "their MAC trajectories differ. Conversely, countries with different TFR trajectories "
    "but similar MAC changes show similar tempo effects. This independence confirms that the "
    "tempo channel is not merely a proxy for low fertility but a distinct demographic force.",
    size=12, space_after=12)

add_para(doc,
    "Third, the \u2018equivalent TFR-years\u2019 column provides a policy-relevant metric. Korea\u2019s "
    "tempo effect is equivalent to 45 years of fertility at TFR = 1.5; even for countries "
    "with moderate postponement (Germany, \u0394MAC = 3.5), the tempo effect equals ~24 years "
    "of below-replacement fertility. These magnitudes suggest that tempo is not a second-order "
    "correction but a first-order demographic force.",
    size=12, space_after=12)

# --- 4.3 Decomposition ---
add_heading_styled(doc, "4.3 Decomposing population change: quantum, tempo, and survival",
                   level=2)
add_para(doc,
    "The counterfactual framework allows systematic decomposition of total population change "
    "into three components. For each country, we compute the difference between the baseline "
    "trajectory and each single-parameter counterfactual. Table 4 shows the decomposition "
    "for 10 countries representing distinct demographic profiles.",
    size=12, space_after=6)

# Table 4: Decomposition
add_para(doc, "Table 4: Decomposition of modelled population change (1970\u20132023) into "
         "quantum, tempo, and survival components",
         bold=True, size=11, space_after=4)

tbl4 = doc.add_table(rows=11, cols=6)
tbl4.style = 'Light Shading Accent 1'
h4 = ['Country', 'Total pop.\nchange (%)', 'Quantum\neffect (%)',
      'Tempo\neffect (%)', 'Survival\neffect (%)', 'Interaction\n(%)']
for i, h in enumerate(h4):
    tbl4.rows[0].cells[i].text = h
t4_data = [
    ['Japan', '\u221212.8', '\u221232.1', '\u221213.0', '+28.4', '+3.9'],
    ['Korea', '+7.3', '\u221238.5', '\u221221.9', '+55.2', '+12.5'],
    ['Italy', '\u22124.2', '\u221228.7', '\u221214.6', '+34.8', '+4.3'],
    ['Germany', '+0.3', '\u221226.4', '\u221211.5', '+32.0', '+6.2'],
    ['France', '+23.8', '\u22128.3', '\u221211.7', '+38.2', '+5.6'],
    ['USA', '+46.3', '\u221212.4', '\u221213.3', '+58.7', '+13.3'],
    ['Czechia', '\u22124.1', '\u221222.0', '\u221218.9', '+30.6', '+6.2'],
    ['Sweden', '+17.5', '\u22125.1', '\u221212.5', '+28.4', '+6.7'],
    ['China', '+56.1', '\u221248.2', '+2.8', '+84.9', '+16.6'],
    ['DRC', '+296.4', '+156.2', '0.0', '+95.8', '+44.4'],
]
for i, rd in enumerate(t4_data):
    for j, val in enumerate(rd):
        tbl4.rows[i + 1].cells[j].text = val
add_para(doc, "", size=6, space_after=4)
add_para(doc,
    "Note: Quantum effect = difference between baseline and TFR-frozen counterfactual. "
    "Tempo effect = difference between baseline and MAC-frozen counterfactual. Survival "
    "effect = difference between baseline and e\u2080-frozen counterfactual. Interaction = "
    "residual from non-additive effects. Signs indicate direction: negative = reducing "
    "population relative to 1970 trajectory.",
    italic=True, size=9, space_after=12)

add_para(doc,
    "The decomposition reveals that tempo is the second-largest component of population change "
    "in most post-transitional countries, after survival gains. In Japan, the tempo effect "
    "(\u221213.0%) is roughly 40% the magnitude of the quantum effect (\u221232.1%) and would be "
    "even larger relative to quantum in the absence of Japan\u2019s substantial longevity gains "
    "(+28.4%). For Czechia, the tempo effect (\u221218.9%) approaches the quantum effect "
    "(\u221222.0%) in magnitude, highlighting that post-socialist postponement was nearly as "
    "consequential for population size as the decline in births themselves.",
    size=12, space_after=12)

add_para(doc,
    "France and Sweden illustrate an important point: even in countries where population "
    "grew over this period, the tempo effect was substantially negative (\u221211.7% and "
    "\u221212.5%, respectively). These countries\u2019 growth was driven by survival gains and, "
    "in France\u2019s case, relatively sustained quantum\u2014but would have grown more had "
    "childbearing not been postponed. The tempo channel thus operates as a drag on population "
    "growth even in demographically favourable contexts.",
    size=12, space_after=12)

add_para(doc,
    "China provides a revealing contrast. Its MAC actually declined slightly over this "
    "period (from 29.2 to 28.4), producing a small positive tempo effect (+2.8%). China\u2019s "
    "population dynamics were overwhelmingly driven by the quantum channel (the one-child "
    "policy) and survival gains. The DRC, still in early demographic transition, shows "
    "negligible tempo effect and massive growth driven by sustained high fertility and "
    "improving survival.",
    size=12, space_after=12)

add_para(doc,
    "Figure 2 shows model validation across all 40 countries, providing the empirical "
    "foundation for the decomposition results.",
    size=12, space_after=6)

add_figure(doc, os.path.join(FIG_DIR, 'fig2_all_countries.png'),
    "Figure 2: Five-model validation across all 40 countries",
    note="Note: Observed = black; Tempo-responsive = blue; Tempo-invariant = orange dashed; "
    "Tempo-adjusted (TFR*) = green dash-dot; Fixed-parameter = red dotted. "
    "Tempo-responsive MAPE shown in upper-right corner. Countries sorted alphabetically.",
    width=6.5)

# --- 4.4 Pace of adaptation ---
add_heading_styled(doc, "4.4 The pace of demographic change", level=2)
add_para(doc,
    "The tempo effect operates not only on the level of population but on the rate of change. "
    "This pace dimension has direct policy implications: it determines how quickly "
    "institutions must adapt to demographic shifts. We quantify this by comparing annual "
    "rates of population change under different MAC scenarios.",
    size=12, space_after=12)

add_para(doc,
    "Consider two countries with identical TFR = 1.5 and e\u2080 = 80 but MAC = 25 versus "
    "MAC = 33. In the low-MAC country, approximately 3.2 generations overlap, producing a "
    "generational replacement cycle of 25 years. In the high-MAC country, only 2.4 "
    "generations overlap with a 33-year cycle. The high-MAC country\u2019s population declines "
    "faster per calendar year because each generation\u2019s below-replacement contribution "
    "accumulates over fewer overlapping cohorts.",
    size=12, space_after=12)

add_para(doc,
    "This acceleration is not trivial. Our model shows that for a country with TFR = 1.5, "
    "the annual rate of population decline at MAC = 33 is approximately 0.7% per year, "
    "compared with 0.4% at MAC = 25\u2014a 75% acceleration. Over a 30-year planning horizon, "
    "this translates to a cumulative difference of approximately 9 percentage points of "
    "population (a decline of 19% versus 11%). For pension systems designed around 2\u20133% "
    "per-decade population adjustment, the higher MAC scenario requires twice the adaptation "
    "speed.",
    size=12, space_after=12)

add_para(doc,
    "This acceleration effect explains why countries with similar TFR but different MAC "
    "face qualitatively different policy challenges. Japan (TFR \u2248 1.2, MAC \u2248 31.4) and "
    "the USA (TFR \u2248 1.6, MAC \u2248 29.3) differ not only in their fertility levels but in "
    "the speed at which demographic change unfolds. Japan\u2019s higher MAC means its population "
    "decline is faster per calendar year than the USA\u2019s, compressing the time available for "
    "institutional reform\u2014pension adjustment, healthcare infrastructure expansion, labour "
    "market restructuring.",
    size=12, space_after=12)

add_para(doc,
    "Figure 3 illustrates how model fit varies across countries and base years, showing that "
    "the fixed-parameter model\u2019s degradation over longer horizons reflects accumulating demographic "
    "change\u2014the very phenomenon our decomposition quantifies.",
    size=12, space_after=6)

add_figure(doc, os.path.join(FIG_DIR, 'fig3_heatmap.png'),
    "Figure 3: Fixed-parameter model MAPE (%) by country and base year",
    note="Note: Greener cells indicate better fit; redder cells indicate poorer fit. "
    "Scale capped at 30%. Longer projection horizons show greater misfit, reflecting "
    "accumulating demographic change unaccounted for by fixed parameters.",
    width=5.0)

add_figure(doc, os.path.join(FIG_DIR, 'fig4_comparison.png'),
    "Figure 4: Four-model comparison\u2014MAPE and final population ratio by country",
    note="Note: Left panel: MAPE by country for fixed-parameter (red), tempo-invariant "
    "(orange), tempo-responsive (blue), and tempo-adjusted TFR* (green). Right panel: "
    "final population ratio (model/observed in 2023). The tempo-adjusted model (TFR*) "
    "achieves the best overall fit, particularly in countries with strong postponement.",
    width=6.0)

# ==============================================================
# 5. Discussion
# ==============================================================
add_heading_styled(doc, "5. Discussion", level=1)

add_para(doc,
    "Our results provide four main findings with implications for demographic research "
    "and policy.",
    size=12, space_after=12)

add_para(doc,
    "First, and most fundamentally, the tempo effect on population size is invisible within "
    "standard projection frameworks. The near-identical performance of the tempo-invariant "
    "and tempo-responsive models (median MAPE 4.5% versus 4.6%) demonstrates that period "
    "TFR\u2014the indicator on which virtually all national and international projections "
    "depend\u2014absorbs tempo distortion without decomposing it. When MAC rises, period TFR "
    "falls mechanically,{3} and projection systems treat this decline as if it were entirely "
    "quantum. The policy consequence is systematic: policymakers respond with quantum "
    "interventions (pronatalist cash transfers, child allowances) to a signal that is partly "
    "or largely a timing shift.",
    size=12, space_after=12)

add_para(doc,
    "Second, explicit tempo decomposition via the Bongaarts\u2013Feeney TFR* achieves the best "
    "overall fit (median MAPE 4.3%, mean 5.8%), outperforming both conventional variants. "
    "The improvement is concentrated in countries where postponement was strongest: the "
    "Republic of Korea (11.9% \u2192 6.9%), China (15.6% \u2192 8.6%), Colombia (13.1% \u2192 7.8%), "
    "Sweden (5.7% \u2192 3.5%), Denmark (3.0% \u2192 1.0%). This pattern reveals where the tempo "
    "distortion is largest\u2014and, by implication, where tempo-based policy interventions "
    "have the greatest potential demographic payoff. Conversely, countries where TFR* does "
    "not improve fit (e.g., France, Japan) are those where the period TFR decline was "
    "predominantly quantum\u2014itself a policy-relevant distinction. This finding extends "
    "Goldstein et al.\u2019s{7} theoretical insight from stylised EU-15 projections to observed "
    "population data across 40 countries spanning the full range of demographic transition "
    "stages.",
    size=12, space_after=12)

add_para(doc,
    "Third, the counterfactual decomposition reveals that tempo is typically the "
    "second-largest component of population change in post-transitional countries. "
    "The observed 4\u20136 year increase in MAC across OECD countries reduced SLP by 8\u201317%, "
    "magnitudes comparable to decades of below-replacement fertility. "
    "In Czechia, the tempo effect "
    "approaches the quantum effect in magnitude; in Japan, it accounts for 40% of the "
    "quantum effect. These proportions are large enough to alter the conclusions of "
    "demographic impact assessments that consider only quantum and survival. Lutz, Sanderson, "
    "and Scherbov{14} projected the end of world population growth; our analysis shows that "
    "the tempo channel is a substantial driver of how rapidly that endpoint is approached.",
    size=12, space_after=12)

add_para(doc,
    "Fourth, the pace dimension has direct policy implications. Higher MAC accelerates the "
    "annual rate of population decline, compressing the time available for institutional "
    "adaptation. This reframes the policy problem. Population policy currently operates "
    "on two levers: boosting births (quantum interventions such as child allowances, "
    "parental leave, and pronatalist incentives) and extending lives (survival interventions "
    "such as healthcare investment and disease prevention). Our results demonstrate that a "
    "third lever exists: interventions that influence the timing of births. Tempo-sensitive "
    "policies\u2014affordable housing that enables family formation at younger ages, universal "
    "childcare that reduces the opportunity cost of early parenthood, restructured "
    "educational and career pathways that do not penalise combining parenthood with "
    "professional development{15}\u2014could slow the pace of population decline and expand "
    "the window for institutional adjustment, even without raising TFR.",
    size=12, space_after=12)

add_para(doc,
    "The distinction between quantum and tempo interventions is not merely semantic. "
    "Quantum-focused policies (e.g., South Korea\u2019s 47 trillion won package, Japan\u2019s child "
    "allowance expansion) aim to increase the number of births. Tempo-focused policies aim "
    "to reduce the age at which existing births occur\u2014a fundamentally different target. "
    "Gauthier{26} showed that pronatalist cash transfers have modest and often transient "
    "effects on quantum; our analysis suggests that even if quantum remains unchanged, a "
    "2-year reduction in MAC from current levels would increase SLP by 5\u20137% in most OECD "
    "countries\u2014equivalent to roughly 10 years of moderate pronatalist success. This is a "
    "demographic dividend achievable without increasing the number of births per woman.",
    size=12, space_after=12)

add_para(doc,
    "Bongaarts and Sobotka{16} showed that some European countries had begun to reverse "
    "postponement trends, with period TFR recovering as tempo distortions subsided. "
    "Myrskyl\u00e4, Kohler, and Billari{17} demonstrated that advanced development can "
    "reverse fertility declines. Our results complement both findings by showing that "
    "even where quantum remains low, tempo adjustments independently alter the population "
    "trajectory. The policy implication is that the demographic response to population "
    "decline should not be framed as a binary choice between \u2018more births\u2019 and "
    "\u2018more immigration\u2019 but as a three-dimensional problem in which birth quantum, "
    "birth timing, and survival each constitute independent and actionable levers.",
    size=12, space_after=12)

add_para(doc,
    "The model\u2019s deliberate exclusion of migration is both a limitation and a feature. "
    "It limits direct applicability to high-immigration countries (Australia, Canada, "
    "Luxembourg), where MAPE exceeds 12%. However, the exclusion enables clean decomposition: "
    "the model\u2019s \u2018error\u2019 in these countries is itself informative, quantifying the "
    "migration component of population change. For example, Australia\u2019s 13.5% MAPE implies "
    "that net immigration added approximately 13\u201314% to the population beyond what natural "
    "increase would produce\u2014consistent with Australian Bureau of Statistics (ABS) "
    "estimates. Our natural experiments analysis "
    "(Appendix A) demonstrates that Germany\u2019s model misfit quantifies the demographic "
    "footprint of reunification as a migration shock.",
    size=12, space_after=12)

# --- 5.1 National projection systems: the tempo gap ---
add_heading_styled(doc, "5.1 National projection systems and the tempo gap", level=2)

add_para(doc,
    "To assess whether the tempo channel is accounted for in practice, we reviewed the "
    "official population projection methodologies of 15 national statistical offices and "
    "international organisations covering all 40 countries in our sample (Table 5). The "
    "review reveals a uniform finding: none explicitly decomposes population change into "
    "quantum and tempo components.",
    size=12, space_after=6)

# Table 5: National projection methods
add_para(doc, "Table 5: Summary of official population projection methods and tempo "
         "treatment by country/organisation",
         bold=True, size=11, space_after=4)

tbl5 = doc.add_table(rows=16, cols=5)
tbl5.style = 'Light Shading Accent 1'
hdr5 = ['Country /\nOrganisation', 'Method', 'Fertility\nassumption',
        'Mortality\nassumption', 'Tempo\ndecomposition?']
for i, h in enumerate(hdr5):
    tbl5.rows[0].cells[i].text = h

t5_data = [
    ['UN WPP 2024\n(All countries)', 'Cohort-component;\nprobabilistic (Bayesian)',
     'Bayesian hierarchical;\nTFR trajectories',
     'Lee\u2013Carter variant;\ncountry-specific drift', 'No'],
    ['Japan (IPSS)', 'Cohort-component;\n3\u00d73 variants',
     'Cohort fertility model;\nMAC = 32.8',
     'Lee\u2013Carter; e\u2080 = 85.9/91.8', 'No'],
    ['USA (Census)', 'Cohort-component;\nmain + 3 migration',
     'Race-specific ASFRs;\nTFR ~ 1.75 by 2060',
     'Cause-of-death model;\ne\u2080 ~ 83.9 by 2100', 'No'],
    ['Germany\n(Destatis)', 'Cohort-component;\n27 variants',
     'TFR 1.29\u20131.65;\nMAC ~ 31.7\u201332.1',
     'e\u2080 82.6\u201386.4 (M)\n85.9\u201389.3 (F)', 'No'],
    ['UK (ONS)', 'Cohort-component;\nprincipal + 9 variants',
     'ASFRs; TFR ~ 1.59\nlong-term',
     'Age-period-cohort;\ne\u2080 ~ 83.9/86.3', 'No'],
    ['France\n(INSEE)', 'Cohort-component;\ncentral + 3 variants',
     'TFR ~ 1.80 central',
     'Trend extrapolation;\ne\u2080 ~ 87.5/90.0', 'No'],
    ['Korea\n(KOSTAT)', 'Cohort-component;\n3 scenarios',
     'Cohort model;\nTFR 1.08 by 2040',
     'Lee\u2013Carter;\ne\u2080 = 88.0/91.4', 'No'],
    ['Italy (ISTAT)', 'Cohort-component;\nmedian + 4 scenarios',
     'TFR ~ 1.40 median',
     'Lee\u2013Carter;\ne\u2080 ~ 85.8/89.2', 'No'],
    ['Australia\n(ABS)', 'Cohort-component;\n3 series',
     'TFR 1.55\u20131.85',
     'Mortality improvement;\ne\u2080 ~ 87/89', 'No'],
    ['Canada\n(StatCan)', 'Cohort-component;\nmicrosimulation',
     'TFR 1.40\u20131.60',
     'Lee\u2013Carter variant;\ne\u2080 ~ 86/89', 'No'],
    ['Eurostat\n(EU members)', 'Cohort-component;\nconvergence model',
     'Partial convergence\nof TFR across EU',
     'Convergence of\nmortality improvement', 'No'],
    ['China (NBS)', 'Cohort-component\n(not regularly published)',
     'TFR 1.0\u20131.2;\nrecovery assumed',
     'Model life table;\ne\u2080 ~ 78.6', 'No'],
    ['DRC', 'Relies on UN WPP;\nno national projection',
     'TFR ~ 6.1; gradual\ndecline assumed',
     'Model life table;\ne\u2080 ~ 60.7', 'No'],
    ['Mexico\n(CONAPO)', 'Cohort-component;\n3 variants',
     'TFR ~ 1.7 by 2050',
     'Trend extrapolation;\ne\u2080 ~ 79/83', 'No'],
    ['T\u00fcrkiye\n(TurkStat)', 'Cohort-component;\n3 scenarios',
     'TFR declining to\n~1.60 long-term',
     'Improvement model;\ne\u2080 ~ 80/84', 'No'],
]
for i, rd in enumerate(t5_data):
    for j, val in enumerate(rd):
        tbl5.rows[i + 1].cells[j].text = val
add_para(doc, "", size=6, space_after=4)
add_para(doc,
    "Source: UN DESA (2024), IPSS Japan (2023), US Census Bureau (2023), Destatis (2025), "
    "ONS UK (2025), INSEE France (2021), KOSTAT Korea (2023), ISTAT Italy (2023), "
    "ABS Australia (2018), Statistics Canada (2024), Eurostat (2024), CONAPO Mexico (2018), "
    "TurkStat (2023). "
    "Abbreviations: IPSS = National Institute of Population and Social Security Research; "
    "Destatis = Federal Statistical Office of Germany; ONS = Office for National Statistics; "
    "INSEE = National Institute of Statistics and Economic Studies; "
    "KOSTAT = Statistics Korea; ISTAT = National Institute of Statistics (Italy); "
    "ABS = Australian Bureau of Statistics; CONAPO = National Population Council (Mexico); "
    "NBS = National Bureau of Statistics of China; TurkStat = Turkish Statistical Institute.",
    italic=True, size=9, space_after=12)

add_para(doc,
    "All 15 systems share the cohort-component method as their foundational structure. "
    "Fertility timing enters implicitly through age-specific fertility rate schedules, and "
    "some systems (Japan, Korea) use cohort fertility models that track timing shifts. "
    "However, the independent contribution of MAC to simultaneously living population is not "
    "isolated in any system. Our five-model comparison reveals why this gap matters. The "
    "tempo-invariant and tempo-responsive models produce nearly identical fit (median MAPE "
    "4.5% versus 4.6%), because the period TFR used by national systems already absorbs "
    "tempo distortion mechanically. Policymakers never see the tempo channel\u2014they see only "
    "a lower TFR and respond with quantum interventions. Only when tempo is explicitly "
    "decomposed via TFR* does the best fit emerge (median MAPE 4.3%), confirming that the "
    "standard approach conflates two distinct demographic forces. Japan\u2019s IPSS has revised "
    "its long-term projection downward in virtually every round since the 1990s\u2014not "
    "because its TFR or e\u2080 assumptions were wrong, but because the TFR signal conflated "
    "quantum and tempo, leading to systematically incorrect policy diagnosis. This is not a "
    "limitation of the cohort-component method itself\u2014it is a reporting and analytical gap. "
    "National projections could, in principle, run the same counterfactual decomposition we "
    "present here, using their more detailed models to separate the quantum and tempo "
    "channels. That none do so reinforces the \u2018forgotten\u2019 status of the tempo\u2013population "
    "link.",
    size=12, space_after=12)

add_para(doc,
    "Our 4-parameter model is not designed to replace these national projection systems but "
    "to complement them by making the tempo\u2013quantum\u2013survival decomposition explicit. The "
    "tempo-adjusted model (TFR*) achieves median MAPE of 4.3% against these same "
    "populations\u2014performance sufficient to establish the quantitative significance of the "
    "tempo channel, even though it cannot match the precision of full-parameterisation "
    "national models that include migration.{18,19}",
    size=12, space_after=12)

# --- 5.2 Limitations ---
add_heading_styled(doc, "5.2 Limitations", level=2)
add_para(doc,
    "Several limitations warrant acknowledgement. First, the normal fertility schedule is a "
    "simplification; actual ASFRs may be skewed or bimodal.{20} Second, our decadal update "
    "interval does not match the varying revision cycles of national statistical offices, "
    "which update their projections at intervals ranging from two years (Japan\u2019s IPSS) to "
    "five or more years (Eurostat, US Census Bureau). We adopt the 10-year interval as a "
    "deliberate analytical choice for two reasons: (a) it approximates the time scale over "
    "which major population policy interventions\u2014housing programmes, childcare systems, "
    "educational pathway reforms\u2014are designed, implemented, and begin to produce measurable "
    "demographic effects{15}; and (b) it provides a conservative test of the tempo channel, "
    "since more frequent updates would narrow any remaining gap between model variants. "
    "That the tempo-adjusted model (TFR*) still achieves measurably better fit (median MAPE "
    "4.3%) despite the conservative decadal interval strengthens the case for explicit "
    "tempo decomposition. Third, the Gompertz survival function fits "
    "adult mortality well but "
    "approximates infant and child mortality less precisely; national projections typically "
    "use more flexible models.{21} Fourth, the decomposition is necessarily model-dependent: "
    "the counterfactual \u2018MAC frozen at 1970\u2019 is a thought experiment, not a prediction "
    "of what would have occurred in the absence of postponement, since MAC changes are "
    "endogenous to broader social and economic shifts.{22} Despite these limitations, the "
    "model\u2019s parsimonious structure is a feature: it makes the tempo\u2013quantum\u2013survival "
    "decomposition transparent and allows the magnitudes of each component to be compared "
    "directly.",
    size=12, space_after=12)

add_para(doc,
    "Figure 5 provides model bias diagnostics, confirming that model performance is robust "
    "across demographic contexts with no systematic relationship between fit and TFR, life "
    "expectancy, or MAC.",
    size=12, space_after=6)

add_figure(doc, os.path.join(FIG_DIR, 'fig5_bias.png'),
    "Figure 5: Model bias analysis using base year 2000",
    note="Note: (a) Fit versus TFR; (b) fit versus life expectancy; (c) bias versus MAC. "
    "No systematic relationship is observed.",
    width=6.0)

# ==============================================================
# 6. Conclusion
# ==============================================================
add_heading_styled(doc, "6. Conclusion", level=1)

add_para(doc,
    "The tempo effect on simultaneously living population is well-established in demographic "
    "theory but has never been systematically quantified across countries. Meanwhile, "
    "bibliometric evidence shows that the concept has essentially disappeared from the health "
    "and policy literature, and no national projection system decomposes the tempo channel "
    "explicitly. We provide this quantification using a parsimonious model validated against "
    "observed trajectories for 40 countries over 1970\u20132023. Five findings emerge.",
    size=12, space_after=12)

add_para(doc,
    "First, the tempo effect is invisible within standard projection frameworks: "
    "tempo-invariant and tempo-responsive models yield nearly identical fit (median MAPE "
    "4.5% versus 4.6%), because period TFR absorbs tempo distortion without decomposing "
    "it. Policymakers who rely on period TFR cannot distinguish postponement from permanent "
    "quantum decline. Second, explicit tempo decomposition via the Bongaarts\u2013Feeney TFR* "
    "achieves the best overall fit (median MAPE 4.3%), with the largest improvements in "
    "countries experiencing strong postponement (Republic of Korea, China, Colombia). "
    "Third, the magnitude of the tempo effect is large: the observed rise in MAC across "
    "OECD countries independently reduced SLP by 8\u201317%, equivalent to 15\u201340 years of "
    "below-replacement fertility. "
    "Fourth, tempo is typically the second-largest component of population change in "
    "post-transitional countries, comparable in magnitude to quantum in several Central and "
    "Eastern European nations. Fifth, higher MAC accelerates the annual pace of population "
    "decline, compressing the time available for institutional adaptation.",
    size=12, space_after=12)

add_para(doc,
    "These findings have two practical implications. For demographic assessment, the tools "
    "to decompose quantum and tempo already exist within national cohort-component projection "
    "systems; what is needed is the analytical step of reporting their separate contributions\u2014"
    "a step that is straightforward in principle but absent in all 15 systems we reviewed. "
    "For population policy, the current framework operates on two levers\u2014boosting births "
    "and extending lives\u2014while ignoring the third. Our results demonstrate that birth "
    "timing constitutes an independent and quantitatively significant policy lever. "
    "Tempo-sensitive interventions\u2014housing, childcare, educational reform\u2014offer a "
    "complementary approach that operates not on the ultimate size of the population but on "
    "the speed at which demographic change unfolds. In an era where pronatalist policies "
    "have shown limited effectiveness in raising quantum,{26} the tempo channel deserves "
    "systematic attention as a means of managing the pace of demographic transition.",
    size=12, space_after=18)

# ==============================================================
# GATHER compliance statement
# ==============================================================
add_heading_styled(doc, "GATHER compliance statement", level=2)
add_para(doc,
    "This study reports population estimates and follows the Guidelines for Accurate and "
    "Transparent Health Estimates Reporting (GATHER).{12} All input data are from UN WPP "
    "2024, publicly available at https://population.un.org/wpp/. No primary data collection "
    "was undertaken. The Gompertz survival model, normal fertility schedule, and endogenous "
    "renewal model are described in Section 3. Four parameters per period (TFR, e\u2080, MAC, "
    "\u03c3) are used. MAPE and final ratio are reported as fit metrics. No formal uncertainty "
    "intervals; the model is deterministic. Analytical code is available from the authors "
    "upon request and will be deposited in a public repository upon acceptance.",
    size=12, space_after=18)

# ==============================================================
# Data availability statement
# ==============================================================
add_heading_styled(doc, "Data availability statement", level=2)
add_para(doc,
    "All input data are drawn from the United Nations World Population Prospects 2024, "
    "publicly available at https://population.un.org/wpp/. Analytical code is available "
    "from the authors upon request and will be deposited in a public repository upon "
    "acceptance.",
    size=12, space_after=18)

# ==============================================================
# References (Vancouver numbered, in order of first appearance)
# ==============================================================
add_heading_styled(doc, "References", level=1)

refs = [
    # 1
    'Th\u00e9venon O. Family policies in OECD countries: A comparative analysis. '
    'Population and Development Review 2011; 37(1): 57\u201387.',
    # 2
    'Ryder NB. The process of demographic translation. Demography 1964; 1(1): 74\u201382.',
    # 3
    'Bongaarts J, Feeney G. On the quantum and tempo of fertility. '
    'Population and Development Review 1998; 24(2): 271\u2013291.',
    # 4
    'Kohler H-P, Ortega JA. Tempo-adjusted period parity progression measures, fertility '
    'postponement and completed cohort fertility. Demographic Research 2002; 6(6): 91\u2013144.',
    # 5
    'Sobotka T. Is lowest-low fertility in Europe explained by the postponement of '
    'childbearing? Population and Development Review 2004; 30(2): 195\u2013220.',
    # 6
    'Bongaarts J, Feeney G. The quantum and tempo of life-cycle events. '
    'Vienna Yearbook of Population Research 2006; 4: 115\u2013151.',
    # 7
    'Goldstein JR, Lutz W, Scherbov S. Long-term population decline in Europe: The '
    'relative importance of tempo effects and generational length. Population and '
    'Development Review 2003; 29(4): 699\u2013707.',
    # 8
    'Keyfitz N. On the momentum of population growth. Demography 1971; 8(1): 71\u201380.',
    # 9
    'Preston SH, Heuveline P, Guillot M. Demography: Measuring and modeling population '
    'processes. Oxford: Blackwell; 2001.',
    # 10
    'Gompertz B. On the nature of the function expressive of the law of human mortality. '
    'Philosophical Transactions of the Royal Society of London 1825; 115: 513\u2013583.',
    # 11
    'United Nations, Department of Economic and Social Affairs, Population Division. '
    'World Population Prospects 2024. New York: United Nations; 2024.',
    # 12
    'Stevens GA, Alkema L, Black RE, et al. Guidelines for Accurate and Transparent '
    'Health Estimates Reporting: The GATHER statement. The Lancet 2016; 388(10062): '
    'e19\u2013e23.',
    # 13
    'Kohler H-P, Billari FC, Ortega JA. The emergence of lowest-low fertility in Europe '
    'during the 1990s. Population and Development Review 2002; 28(4): 641\u2013680.',
    # 14
    'Lutz W, Sanderson W, Scherbov S. The end of world population growth. '
    'Nature 2001; 412: 543\u2013545.',
    # 15
    'McDonald P. Gender equity in theories of fertility transition. Population and '
    'Development Review 2000; 26(3): 427\u2013439.',
    # 16
    'Bongaarts J, Sobotka T. A demographic explanation for the recent rise in European '
    'fertility. Population and Development Review 2012; 38(1): 83\u2013120.',
    # 17
    'Myrskyl\u00e4 M, Kohler H-P, Billari FC. Advances in development reverse fertility '
    'declines. Nature 2009; 460: 741\u2013743.',
    # 18
    'Gonand F. Assessing the robustness of demographic projections in OECD countries. '
    'OECD Economics Department Working Papers No. 464. Paris: OECD Publishing; 2005.',
    # 19
    'Lee RD, Carter LR. Modeling and forecasting U.S. mortality. Journal of the American '
    'Statistical Association 1992; 87(419): 659\u2013671.',
    # 20
    'Frejka T, Sobotka T. Fertility in Europe: Diverse, delayed and below replacement. '
    'Demographic Research 2008; 19(3): 15\u201346.',
    # 21
    'Wilmoth JR, Zureick S, Canudas-Romo V, Inoue M, Sawyer C. A flexible two-dimensional '
    'mortality model for use in indirect estimation. Population Studies 2012; 66(1): 1\u201328.',
    # 22
    'Lesthaeghe R. The unfolding story of the Second Demographic Transition. Population '
    'and Development Review 2010; 36(2): 211\u2013251.',
    # 23
    'Lutz W, Skirbekk V, Testa MR. The low-fertility trap hypothesis. Vienna Yearbook '
    'of Population Research 2006; 4: 167\u2013192.',
    # 24
    'Goldstein JR, Kreyenfeld M. Has East Germany overtaken West Germany? Recent trends '
    'in order-specific fertility. Population and Development Review 2011; 37(3): 453\u2013472.',
    # 25
    'Witte JC, Wagner GG. Declining fertility in East Germany after unification. '
    'Population and Development Review 1995; 21(2): 387\u2013397.',
    # 26
    'Gauthier AH. The impact of family policies on fertility in industrialized countries. '
    'Population Research and Policy Review 2007; 26(3): 323\u2013346.',
]
for i, r in enumerate(refs):
    add_para(doc, f'{i + 1}. {r}', size=11, space_after=4)

# ==============================================================
# Appendix A: Natural Experiments
# ==============================================================
doc.add_page_break()
add_heading_styled(doc, "Appendix A: Natural experiments \u2014 Political and border "
                   "changes as exogenous shocks", level=1)

add_para(doc,
    "Our model deliberately excludes migration. This design choice enables isolation of the "
    "pure quantum\u2013tempo\u2013survival mechanism, but raises an important question: how does the "
    "model perform when large-scale population redistribution occurs as a result of political "
    "events? Countries that experienced major border changes or state dissolution between 1970 "
    "and 2023 provide natural experiments in which exogenous migration shocks were effectively "
    "imposed on populations. We analyse five such cases.",
    size=12, space_after=12)

# --- A.1 Germany ---
add_heading_styled(doc, "A.1 Germany: Reunification as a migration shock (1990)", level=2)
add_para(doc,
    "German reunification on 3 October 1990 merged two populations that had evolved under "
    "sharply different demographic regimes for 41 years. East Germany had lower life "
    "expectancy (~74.5 versus ~76.0 in the West in 1990), earlier childbearing (MAC \u2248 25.1 "
    "vs. 28.3), and higher but declining TFR (1.52 vs. 1.45). The immediate aftermath saw "
    "massive East-to-West migration (~1.9 million between 1989 and 1992) and a dramatic "
    "fertility collapse in the East (TFR fell to 0.77 in 1994).{24,25}",
    size=12, space_after=6)

add_para(doc,
    "We model East and West Germany separately, run both forward from 1970, and construct "
    "a synthetic combined trajectory. This represents the counterfactual: what would "
    "Germany\u2019s population have looked like without reunification-related migration?",
    size=12, space_after=6)

# Table A1
add_para(doc, "Table A1: Germany reunification \u2014 synthetic East+West versus "
         "observed trajectory",
         bold=True, size=11, space_after=4)

tbl_a1 = doc.add_table(rows=6, cols=4)
tbl_a1.style = 'Light Shading Accent 1'
for i, h in enumerate(['Year', 'Synthetic E+W (M)', 'Observed (M)',
                        'Deviation (%)']):
    tbl_a1.rows[0].cells[i].text = h
a1_data = [
    ['1990', '76.5', '79.4', '\u22123.6'],
    ['2000', '75.3', '82.2', '\u22128.4'],
    ['2010', '73.7', '81.8', '\u22129.9'],
    ['2020', '71.0', '83.2', '\u221214.6'],
    ['2023', '70.1', '83.3', '\u221215.8'],
]
for i, rd in enumerate(a1_data):
    for j, val in enumerate(rd):
        tbl_a1.rows[i + 1].cells[j].text = val
add_para(doc, "", size=6, space_after=6)

add_para(doc,
    "The widening gap (3.6% to 15.8%) reflects three compounding processes absent from the "
    "closed model: (a) net immigration to unified Germany averaging ~300,000\u2013400,000 per "
    "year; (b) internal East-to-West migration; and (c) convergence of East German fertility "
    "toward Western patterns. The overall MAPE of 6.4% confirms that Germany\u2019s relatively "
    "poor fit in the main analysis is attributable to reunification\u2019s migration effects, "
    "not structural model failure.",
    size=12, space_after=6)

add_figure(doc, os.path.join(FIG_DIR, 'fig_germany_reunification.png'),
    "Figure A-1: Germany reunification analysis",
    note="Note: (a) Modelled East and West Germany with synthetic combined trajectory "
    "versus observed unified Germany. (b) Percentage deviation over time.",
    width=6.5)

# --- A.2 Other cases ---
add_heading_styled(doc, "A.2 Czechoslovakia: The Velvet Divorce (1993)", level=2)
add_para(doc,
    "The peaceful dissolution of Czechoslovakia on 1 January 1993 created Czechia and "
    "Slovakia with relatively limited cross-border migration. MAPE: Czechia 6.3%, Slovakia "
    "9.9%. Slovakia\u2019s higher error reflects emigration to Czechia and Western Europe "
    "following EU accession (2004).",
    size=12, space_after=12)

add_heading_styled(doc, "A.3 Yugoslavia: Dissolution and conflict (1991\u20132001)", level=2)
add_para(doc,
    "The breakup of Yugoslavia involved armed conflict and massive refugee flows. Model "
    "performance varies: Croatia (4.1%), North Macedonia (6.4%) show reasonable fit; "
    "Bosnia and Herzegovina (8.1%) and Slovenia (12.2%) show larger errors. The range "
    "illustrates how conflict-driven migration creates heterogeneous deviations from the "
    "endogenous renewal baseline.",
    size=12, space_after=12)

add_heading_styled(doc, "A.4 Baltic States: USSR dissolution (1991)", level=2)
add_para(doc,
    "Estonia, Latvia, and Lithuania gained independence in 1991. MAPE ranges from 4.8% "
    "(Estonia) to 7.1% (Lithuania), reflecting persistent emigration. Even moderate but "
    "sustained net emigration (~0.5\u20131.0% annually) accumulates substantially over "
    "three decades.",
    size=12, space_after=12)

add_heading_styled(doc, "A.5 Ethiopia and Eritrea: Separation (1993)", level=2)
add_para(doc,
    "Eritrean independence separated two populations in high-fertility transition. Ethiopia "
    "(MAPE 16.5%) shows overprojection from rapid fertility decline. Eritrea (37.8%) shows "
    "the largest error, driven by conflict and data uncertainty.",
    size=12, space_after=6)

add_figure(doc, os.path.join(FIG_DIR, 'fig_natural_experiments_summary.png'),
    "Figure A-2: Natural experiments summary",
    note="Note: Population trajectories for five cases of major political/border change. "
    "Red vertical lines mark the year of political change.",
    width=6.5)

# --- Synthesis table ---
add_heading_styled(doc, "A.6 Synthesis", level=2)
add_para(doc, "Table A2: Model performance across natural experiment cases",
         bold=True, size=11, space_after=4)

tbl_a2 = doc.add_table(rows=15, cols=4)
tbl_a2.style = 'Light Shading Accent 1'
for i, h in enumerate(['Country', 'Event (year)', 'MAPE (%)',
                        'Primary misfit source']):
    tbl_a2.rows[0].cells[i].text = h
a2_data = [
    ['Germany (synth. E+W)', 'Reunification (1990)', '6.4',
     'Immigration + internal migration'],
    ['Czechia', 'Velvet Divorce (1993)', '6.3', 'Post-EU emigration'],
    ['Slovakia', 'Velvet Divorce (1993)', '9.9', 'Emigration to EU/West'],
    ['Croatia', 'Yugoslav breakup (1991)', '4.1', 'Post-conflict stabilisation'],
    ['Slovenia', 'Yugoslav breakup (1991)', '12.2', 'Immigration (EU member)'],
    ['Bosnia & Herz.', 'Yugoslav breakup (1991)', '8.1', 'War displacement'],
    ['Serbia', 'Yugoslav breakup (1991)', '7.1', 'Refugee flows, emigration'],
    ['N. Macedonia', 'Yugoslav breakup (1991)', '6.4', 'Modest migration'],
    ['Montenegro', 'Yugoslav breakup (1991)', '8.1', 'Small state, volatile'],
    ['Estonia', 'USSR dissolution (1991)', '4.8', 'Ethnic Russian emigration'],
    ['Latvia', 'USSR dissolution (1991)', '6.6', 'Emigration (ethnic + EU)'],
    ['Lithuania', 'USSR dissolution (1991)', '7.1', 'Sustained emigration'],
    ['Ethiopia', 'Eritrean indep. (1993)', '16.5', 'Rapid fertility decline'],
    ['Eritrea', 'Eritrean indep. (1993)', '37.8', 'Conflict, data uncertainty'],
]
for i, rd in enumerate(a2_data):
    for j, val in enumerate(rd):
        tbl_a2.rows[i + 1].cells[j].text = val
add_para(doc, "", size=6, space_after=6)

add_para(doc,
    "These natural experiments yield three key insights. First, the model performs reasonably "
    "(MAPE < 8%) even for countries with major political upheaval, provided post-event "
    "migration was moderate. Second, the model\u2013observation divergence provides a direct "
    "estimate of the migration component: Germany\u2019s 15.8% gap implies ~13.5 million persons "
    "added by immigration. Third, the model\u2019s limitations are most acute in conflict-affected, "
    "data-sparse settings (Eritrea: 37.8%).",
    size=12, space_after=12)

# ==============================================================
# Save
# ==============================================================
outpath = os.path.join(OUT_DIR, 'PopStudies_Article_EN.docx')
doc.save(outpath)
print(f'OK: {outpath}')
