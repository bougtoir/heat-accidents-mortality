#!/usr/bin/env python3
"""
Convert the base manuscript into a Journal of Safety Research (JSR) submission
package.

Re-uses make_manuscript.py so every reported number is read from the generated
result CSVs (no hard-coded results).  The post-processing steps enforce JSR
formatting:

  - double-anonymized review: the main manuscript contains no author
    information; author details go to a separate title-page file
  - structured abstract (<= 300 words) with JSR subheadings:
    Introduction / Method / Results / Conclusions / Practical Applications
  - keywords
  - numbered main sections, ending with a "Practical Applications" section
  - APA-style in-text citations (author-date) and an alphabetical APA
    reference list (all authors listed)
  - JSR declaration headings (Declaration of competing interests, generative
    AI declaration, data statement)
  - anonymized GitHub repository reference for double-anonymized review
"""
import os
import re
import shutil
import sys
import tempfile
import zipfile  # noqa: F401  (kept for parity with other submission scripts)

from docx import Document
from docx.shared import Pt

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
MAN = os.path.join(ROOT, "output", "manuscript")
FIG = os.path.join(ROOT, "output", "figures")

sys.path.insert(0, HERE)
import make_manuscript as mm  # noqa: E402


# ---------------------------------------------------------------------------
# JSR formatting constants
# ---------------------------------------------------------------------------
JSR_KEYWORDS = ("heat; traffic crash; mortality; climate change; road safety; "
                "distributed-lag model")

JSR_COVER = """22 August 2026

The Editors, Journal of Safety Research

Dear Editors,

We submit for your consideration our manuscript, "Ambient heat as an under-recognised risk factor for US traffic-crash mortality: a distributed-lag analysis with road-safety implications", as a Research Article.

Road traffic crashes remain a leading cause of preventable death, and climate change is adding a heat-related layer of risk that road-safety statistics do not capture: fatal crashes on unusually hot days may involve heat-related impairment or unrecorded heat illness, yet decedents are almost never assessed for a heat contribution. Using only public data, this ecological time-series study shows that days hotter than the local seasonal norm carry an acute, same-day excess of US traffic-crash deaths. The excess survives adjustment for driving activity, is concentrated in heat-exposed open-air road users (motorcyclists, pedestrians and cyclists) and in the hottest hours of the day, and is comparable in magnitude to all officially recorded direct-heat deaths. Scenario projections suggest the burden would grow under uniform warming.

We believe this work fits the Journal of Safety Research's interdisciplinary scope on traffic safety and accident countermeasures: it quantifies an environmental risk factor that is invisible to both heat-mortality surveillance and crash statistics, and it translates the findings into practical applications for heat-aware road-safety messaging, targeted warnings for open-air road users, and shared-mobility heat-adaptation measures.

The manuscript is original, is not under consideration elsewhere, and all authors approve submission. All data are public and the complete analysis pipeline is openly available and fully reproducible (make all for data and figures, then make jsr for the manuscript and submission package), with no hard-coded results. We declare no competing interests. The manuscript has not been posted to a preprint server. The main manuscript is anonymized for double-anonymized review; author details appear in the separate title-page file.

We look forward to your assessment.

Yours sincerely,

Tatsuki Onishi, on behalf of all authors
Data Science and AI Innovation Research Promotion Center
Shiga University of Medical Science
Seta Tsukinowa-cho, Otsu, Shiga 520-2192, Japan
E-mail: bougtoir@gmail.com
"""

TITLE_PAGE_LINES = [
    ("Ambient heat as an under-recognised risk factor for US traffic-crash "
     "mortality: a distributed-lag analysis with road-safety implications", "title"),
    ("Tatsuki Onishi", "author"),
    ("Data Science and AI Innovation Research Promotion Center, Shiga "
     "University of Medical Science, Seta Tsukinowa-cho, Otsu, Shiga "
     "520-2192, Japan", "affil"),
    ("Corresponding author: Tatsuki Onishi, Data Science and AI Innovation "
     "Research Promotion Center, Shiga University of Medical Science, Seta "
     "Tsukinowa-cho, Otsu, Shiga 520-2192, Japan. E-mail: bougtoir@gmail.com. "
     "ORCID: [iD to be added]", "corr"),
    ("Word count of main text: [to be confirmed]. Number of tables: 6. "
     "Number of figures: 10.", "meta"),
    ("Declarations of interest: none.", "decl"),
    ("Author contributions: Tatsuki Onishi conceived the study, performed "
     "the analysis, drafted the manuscript, and approved the final version. "
     "The author had full access to all data and verified the reported "
     "results.", "contrib"),
    ("Funding: There was no specific funding for this study.", "funding"),
]

# ---------------------------------------------------------------------------
# APA references (alphabetical; in-text citation metadata per key)
# (intext, year, apa_reference)
# ---------------------------------------------------------------------------
JSR_REFS = {
    "basu": (
        "Basu",
        "2009",
        "Basu, R. (2009). High ambient temperature and mortality: a review of "
        "epidemiologic studies from 2001 to 2008. Environmental Health, 8, 40. "
        "https://doi.org/10.1186/1476-069X-8-40"),
    "care": (
        "European Commission, Directorate-General for Mobility and Transport",
        "n.d.",
        "European Commission, Directorate-General for Mobility and Transport. "
        "(n.d.). Community database on road accidents (CARE). "
        "https://road-safety.transport.ec.europa.eu/european-road-safety-observatory/"
        "methodology-and-research/care-database_en"),
    "cdc": (
        "Centers for Disease Control and Prevention",
        "n.d.",
        "Centers for Disease Control and Prevention. (n.d.). CDC WONDER "
        "Underlying Cause of Death database. https://wonder.cdc.gov/"),
    "census_pep": (
        "US Census Bureau",
        "n.d.",
        "US Census Bureau. (n.d.). Population Estimates Program: annual state "
        "population estimates. https://www.census.gov/programs-surveys/popest.html"),
    "daanen": (
        "Daanen et al.",
        "2003",
        "Daanen, H. A. M., van de Vliert, E., & Huang, X. (2003). Driving "
        "performance in cold, warm, and thermoneutral environments. Applied "
        "Ergonomics, 34(6), 597-602. "
        "https://doi.org/10.1016/S0003-6870(03)00055-3"),
    "dlnm": (
        "Gasparrini et al.",
        "2010",
        "Gasparrini, A., Armstrong, B., & Kenward, M. G. (2010). Distributed "
        "lag non-linear models. Statistics in Medicine, 29(21), 2224-2234. "
        "https://doi.org/10.1002/sim.3940"),
    "eia": (
        "US Energy Information Administration",
        "n.d.",
        "US Energy Information Administration. (n.d.). Weekly finished motor "
        "gasoline product supplied (PET.WGFUPUS2.W). https://www.eia.gov/"),
    "fhwa": (
        "Federal Highway Administration",
        "n.d.-a",
        "Federal Highway Administration. (n.d.-a). Traffic Volume Trends. "
        "https://www.fhwa.dot.gov/policyinformation/travel_monitoring/tvt.cfm"),
    "fhwa_vm2": (
        "Federal Highway Administration",
        "n.d.-b",
        "Federal Highway Administration. (n.d.-b). Highway Statistics VM-2: "
        "annual state vehicle-miles travelled. "
        "https://www.fhwa.dot.gov/policyinformation/statistics.cfm"),
    "fars": (
        "National Highway Traffic Safety Administration",
        "n.d.",
        "National Highway Traffic Safety Administration. (n.d.). Fatality "
        "Analysis Reporting System (FARS). US Department of Transportation. "
        "https://www.nhtsa.gov/research-data/fatality-analysis-reporting-system-fars"),
    "ghcn": (
        "Menne et al.",
        "2012",
        "Menne, M. J., Durre, I., Vose, R. S., Gleason, B. E., & Houston, T. G. "
        "(2012). An overview of the Global Historical Climatology Network-Daily "
        "database. Journal of Atmospheric and Oceanic Technology, 29(7), "
        "897-910. https://doi.org/10.1175/JTECH-D-11-00103.1"),
    "attrib": (
        "Gasparrini & Leone",
        "2014",
        "Gasparrini, A., & Leone, M. (2014). Attributable risk from "
        "distributed lag models. BMC Medical Research Methodology, 14, 55. "
        "https://doi.org/10.1186/1471-2288-14-55"),
    "ipcc": (
        "IPCC",
        "2021",
        "IPCC. (2021). Climate change 2021: The physical science basis. "
        "Contribution of Working Group I to the Sixth Assessment Report of the "
        "Intergovernmental Panel on Climate Change. Cambridge University Press."),
    "lancet": (
        "Gasparrini et al.",
        "2015",
        "Gasparrini, A., Guo, Y., Hashizume, M., Lavigne, E., Zanobetti, A., "
        "Schwartz, J., Tobias, A., Tong, S., Rocklov, J., Forsberg, B., Leone, "
        "M., De Sario, M., Bell, M. L., Guo, Y.-L. L., Wu, C., Kan, H., Yi, "
        "S.-M., Coelho, M. S. Z. S., Saldiva, P. H. N., Honda, Y., Kim, H., "
        "& Armstrong, B. (2015). Mortality risk attributable to high and low "
        "ambient temperature: a multicountry observational study. The Lancet, "
        "386(9991), 369-375. https://doi.org/10.1016/S0140-6736(14)62114-0"),
    "liang2021_aap": (
        "Liang et al.",
        "2021",
        "Liang, M., Zhao, D., Wu, Y., Ye, P., Wang, Y., Yao, Z., Bi, P., Duan, "
        "L., & Sun, Y. (2021). Short-term effects of ambient "
        "temperature and road traffic accident injuries in Dalian, Northern "
        "China: a distributed lag non-linear analysis. Accident Analysis & "
        "Prevention, 153, 106057. https://doi.org/10.1016/j.aap.2021.106057"),
    "liang2022": (
        "Liang et al.",
        "2022",
        "Liang, M., Min, M., Guo, X., Song, Q., Wang, H., Li, N., Su, W., "
        "Liang, Q., Ding, X., Ye, P., Duan, L., & Sun, Y. (2022). The "
        "relationship between ambient "
        "temperatures and road traffic injuries: a systematic review and "
        "meta-analysis. Environmental Science and Pollution Research, 29(33), "
        "50647-50660. https://doi.org/10.1007/s11356-022-19437-y"),
    "npa": (
        "National Police Agency of Japan",
        "n.d.",
        "National Police Agency of Japan. (n.d.). Traffic accident statistics "
        "open data. https://www.npa.go.jp/publications/statistics/koutsuu/opendata/"),
}


def _apa_intext(key):
    authors, year, _ = JSR_REFS[key]
    if " and " in authors or " & " in authors:
        surnames = authors
    else:
        surnames = authors
    return surnames, year


def _first_surname(key):
    """First author surname / organisation name for narrative-cite matching."""
    intext = JSR_REFS[key][0]
    base = re.sub(r"\s+et al\.$", "", intext)
    base = base.split(" and ")[0].split(" & ")[0]
    return base


# ---------------------------------------------------------------------------
# docx helpers (adapted from make_aap_submission.py / make_ehp_submission.py)
# ---------------------------------------------------------------------------
def _heading_text(p):
    return (p.text or "").strip()


def _set_heading_text(p, text):
    p.text = text


def _remove_paragraph(p):
    p._element.getparent().remove(p._element)


def _insert_paragraph_after(paragraph, text="", style=None):
    from docx.oxml.ns import qn
    from docx.text.paragraph import Paragraph
    new_el = paragraph._p.makeelement(qn("w:p"), {})
    paragraph._p.addnext(new_el)
    p = Paragraph(new_el, paragraph._parent)
    if text:
        p.add_run(text)
    if style:
        p.style = style
    return p


def _repurpose_as_keywords(p, keywords):
    p.text = ""
    r1 = p.add_run("Keywords: ")
    r1.bold = True
    p.add_run(keywords)
    p.paragraph_format.line_spacing = 2.0
    p.paragraph_format.space_after = Pt(6)


def _find_heading(doc, text):
    for p in doc.paragraphs:
        if p.style and p.style.name.startswith("Heading") and _heading_text(p) == text:
            return p
    return None


# ---------------------------------------------------------------------------
# Citation conversion: numbered superscripts -> APA author-date
# ---------------------------------------------------------------------------
def _build_num_to_key(doc):
    """Reproduce the citation order: keys were assigned numbers in order of
    first appearance.  We recover the mapping by scanning the reference list
    paragraphs ('N. <REF_TEXT>') at the end of the document."""
    mapping = {}
    for p in doc.paragraphs:
        m = re.match(r"^(\d+)\.\s+(.*)$", p.text or "")
        if not m:
            continue
        n, ref = int(m.group(1)), m.group(2)
        for key, rtext in mm.REF_TEXT.items():
            if ref.strip() == rtext:
                mapping[n] = key
                break
    return mapping


def _apa_for_keys(keys):
    parts = [f"{_apa_intext(k)[0]}, {_apa_intext(k)[1]}" for k in keys]
    return "; ".join(parts)


def _convert_citations_to_apa(doc, num_to_key):
    """Replace each superscript run '1,2' with a normal APA parenthetical.

    'text.{1,2}' -> 'text (Author, Year; Author2, Year).'
    Narrative citations whose preceding text already names the author(s)
    (e.g. 'the method of Gasparrini and Leone{1}') become '(Year)' only.
    """
    punct = set(".,;:!?")
    for p in doc.paragraphs:
        runs = p.runs
        i = 0
        while i < len(runs):
            r = runs[i]
            if r.font.superscript and r.text and re.fullmatch(r"[\d,]+", r.text):
                nums = [int(x) for x in r.text.split(",") if x.strip()]
                keys = [num_to_key.get(n) for n in nums]
                if any(k is None for k in keys):
                    i += 1
                    continue
                prev = runs[i - 1].text if i > 0 else ""
                # narrative citation: preceding text ends with the author name
                narrative = False
                if len(keys) == 1:
                    surname = _first_surname(keys[0])
                    tail = prev.strip().split()[-4:] if prev.strip() else []
                    tail_txt = " ".join(tail)
                    if surname in tail_txt:
                        narrative = True
                if narrative:
                    repl = f" ({JSR_REFS[keys[0]][1]})"
                else:
                    repl = f" ({_apa_for_keys(keys)})"
                trailing = ""
                if prev and prev[-1] in punct:
                    trailing = prev[-1]
                    runs[i - 1].text = prev[:-1]
                    repl = repl + trailing
                elif prev and prev[-1].isspace():
                    repl = repl.lstrip()
                r.text = repl
                r.font.superscript = None
            i += 1


def _replace_reference_list(doc):
    """Replace the numbered Vancouver reference list with an alphabetical APA
    list of only the references actually cited (those present as 'N. ...')."""
    ref_heading = _find_heading(doc, "References")
    if ref_heading is None:
        return
    cited_keys = []
    paragraphs = doc.paragraphs
    start = next(i for i, p in enumerate(paragraphs)
                 if p._p is ref_heading._p) + 1
    ref_ps = []
    for p in paragraphs[start:]:
        m = re.match(r"^(\d+)\.\s+(.*)$", p.text or "")
        if not m:
            break
        for key, rtext in mm.REF_TEXT.items():
            if m.group(2).strip() == rtext:
                cited_keys.append(key)
                break
        ref_ps.append(p)

    # Insert APA entries (alphabetical by formatted string) after the heading,
    # then delete the old numbered paragraphs.
    anchor = ref_heading
    apa_entries = sorted((JSR_REFS[k][2] for k in cited_keys), key=str.lower)
    for entry in apa_entries:
        np = _insert_paragraph_after(anchor)
        np.add_run(entry)
        np.paragraph_format.space_after = Pt(6)
        np.paragraph_format.line_spacing = 2.0
        anchor = np
    for p in ref_ps:
        _remove_paragraph(p)


# ---------------------------------------------------------------------------
# Front matter
# ---------------------------------------------------------------------------
def _anonymize_front_matter(doc):
    """Remove the three centred author/affiliation/correspondence paragraphs
    that follow the title (they move to the title-page file)."""
    removed = 0
    for p in list(doc.paragraphs):
        if p.alignment is not None and p.text and removed < 3:
            t = p.text
            if (t.startswith("Tatsuki Onishi")
                    or t.startswith("Data Science and AI Innovation")
                    or t.startswith("Correspondence to:")):
                _remove_paragraph(p)
                removed += 1
    return removed


def _make_jsr_abstract(doc, abstract_heading, body_ps):
    """Rebuild Summary as a JSR structured abstract + keywords."""
    sections = {}
    funding_p = None
    for p in body_ps:
        txt = p.text or ""
        for lab in ("Background", "Methods", "Findings", "Interpretation", "Funding"):
            if txt.startswith(lab):
                sections[lab] = re.sub(rf"^{lab}\s*", "", txt)
                if lab == "Funding":
                    funding_p = p
                break

    jsr_blocks = [
        ("Introduction", sections.get("Background", "")),
        ("Method", sections.get("Methods", "")),
        ("Results", sections.get("Findings", "")),
        ("Conclusions", sections.get("Interpretation", "")),
        ("Practical Applications",
         "Heat warnings and travel advice during unusually hot periods could "
         "be targeted at motorcyclists, cyclists, pedestrians and outdoor "
         "delivery riders, and crash-prevention messaging could incorporate "
         "temperature forecasts. Road-safety agencies and heat-health plans "
         "should treat hot days as a crash-risk condition."),
    ]

    # Rewrite abstract body paragraphs in place / insert as needed.
    body = list(body_ps)
    for p in body[1:]:
        if p is not funding_p:
            _remove_paragraph(p)
    body = [body_ps[0]]
    first = body_ps[0]
    first.text = ""
    anchor = first
    for j, (label, text) in enumerate(jsr_blocks):
        if j == 0:
            p = first
        else:
            p = _insert_paragraph_after(anchor)
            anchor = p
        r = p.add_run(label + ". ")
        r.bold = True
        p.add_run(text)
        p.paragraph_format.line_spacing = 2.0
        p.paragraph_format.space_after = Pt(6)

    if funding_p is not None:
        _repurpose_as_keywords(funding_p, JSR_KEYWORDS)

    _set_heading_text(abstract_heading, "Abstract")

    words = sum(len(t.split()) for _, t in jsr_blocks)
    print(f"JSR abstract word count: {words} (limit 300)")
    if words > 300:
        print("WARNING: JSR abstract exceeds 300 words")


def _remove_research_in_context(doc, heading, body_ps):
    _remove_paragraph(heading)
    for p in body_ps:
        _remove_paragraph(p)


def _renumber_headings(doc):
    renames = {
        "Introduction": "1. Introduction",
        "Methods": "2. Materials and methods",
        "Results": "3. Results",
        "Discussion": "4. Discussion",
        "Conclusion": "5. Conclusion",
        "Exploratory external validation: Japan comparison":
            "3.1. Exploratory external validation: Japan comparison",
        "Implications for road safety": "4.1. Implications for road safety",
        "Contributors": "Author contributions",
        "Declaration of competing interests": "Declaration of competing interest",
        "Declaration of generative AI use":
            "Declaration of generative AI and AI-assisted technologies in the "
            "manuscript preparation process",
        "Data availability": "Data statement",
    }
    for p in doc.paragraphs:
        if p.style and p.style.name.startswith("Heading"):
            txt = _heading_text(p)
            if txt in renames:
                _set_heading_text(p, renames[txt])


def _anonymize_text(doc):
    """Anonymize self-identifying content for double-anonymized review."""
    for p in doc.paragraphs:
        txt = p.text or ""
        new = None
        if txt.startswith("Tatsuki Onishi conceived the study"):
            new = ("The author conceived the study, performed the analysis, "
                   "drafted the manuscript, and approved the final version. "
                   "The author had full access to all data and verified the "
                   "reported results.")
        elif "github.com/bougtoir/heat-accidents-mortality" in txt:
            new = txt.replace(
                "https://github.com/bougtoir/heat-accidents-mortality",
                "[repository URL anonymized for double-anonymized review]")
            new = new.replace("make ehp for the EHP submission package",
                              "make jsr for the JSR submission package")
        if new is not None:
            p.text = new
            p.paragraph_format.line_spacing = 2.0
            p.paragraph_format.space_after = Pt(6)


def _insert_practical_applications(doc):
    """Append a 'Practical Applications' section before the back-matter
    declarations (JSR requires a closing practical-applications section)."""
    concl = _find_heading(doc, "5. Conclusion")
    if concl is None:
        return
    # find the paragraph following the conclusion heading (conclusion body)
    paragraphs = doc.paragraphs
    idx = next(i for i, p in enumerate(paragraphs) if p._p is concl._p)
    body = paragraphs[idx + 1]
    anchor = body
    hp = _insert_paragraph_after(anchor)
    try:
        hp.style = doc.styles["Heading 1"]
    except Exception:
        pass
    hp.add_run("6. Practical Applications")
    tp = _insert_paragraph_after(hp)
    tp.add_run(
        "Unusually hot days are associated with an acute excess of US "
        "traffic-crash deaths that routine crash and heat-mortality "
        "surveillance do not capture. Road-safety agencies could treat "
        "forecast heat as a crash-risk condition: integrate temperature "
        "warnings into crash-prevention messaging, target alerts at "
        "motorcyclists, cyclists, pedestrians and outdoor delivery riders, "
        "and coordinate with heat-health plans so that warnings reach "
        "outdoor workers and commuters. Shared e-scooter, e-bike and bikeshare "
        "operators could temporarily reduce or suspend rentals above "
        "high-temperature thresholds, shade or relocate docking and charging "
        "infrastructure, and add heat warnings to app-based routing. These "
        "measures are consistent with a Safe System approach to environmental "
        "risk; intervention studies are needed to test whether they reduce "
        "crash risk.")
    tp.paragraph_format.line_spacing = 2.0
    tp.paragraph_format.space_after = Pt(6)


# ---------------------------------------------------------------------------
# Builders
# ---------------------------------------------------------------------------
def _postprocess(src_path, dst_path):
    doc = Document(src_path)

    # 1. Numbered citation -> APA (needs the Vancouver reference list present).
    num_to_key = _build_num_to_key(doc)
    _convert_citations_to_apa(doc, num_to_key)
    _replace_reference_list(doc)

    # 2. Front matter: drop author block; rebuild abstract; add keywords.
    _anonymize_front_matter(doc)

    abstract_heading = None
    abstract_body = []
    research_heading = None
    research_body = []
    collect = None
    for p in doc.paragraphs:
        if p.style and p.style.name.startswith("Heading"):
            txt = _heading_text(p)
            if txt == "Summary":
                abstract_heading = p
                collect = "abstract"
                continue
            if txt == "Research in context":
                research_heading = p
                collect = "research"
                continue
            collect = None
            continue
        if collect == "abstract":
            abstract_body.append(p)
        elif collect == "research":
            research_body.append(p)

    if abstract_heading and abstract_body:
        _make_jsr_abstract(doc, abstract_heading, abstract_body)
    if research_heading:
        _remove_research_in_context(doc, research_heading, research_body)

    # 3. Headings, anonymization, practical-applications section.
    _renumber_headings(doc)
    _anonymize_text(doc)
    _insert_practical_applications(doc)

    doc.save(dst_path)
    print("wrote", dst_path)


def _build_title_page(path):
    doc = Document()
    mm.setup(doc)
    doc.add_heading("Title page", 1)
    for text, kind in TITLE_PAGE_LINES:
        p = doc.add_paragraph(text)
        if kind == "title":
            p.runs[0].bold = True
        p.paragraph_format.line_spacing = 1.5
        p.paragraph_format.space_after = Pt(6)
    doc.save(path)
    print("wrote", path)


def _build_highlights(path):
    doc = Document()
    mm.setup(doc)
    t = doc.add_paragraph()
    t.alignment = mm.WD_ALIGN_PARAGRAPH.CENTER
    r = t.add_run("Highlights")
    r.bold = True
    r.font.size = Pt(14)
    highlights = [
        "Hotter-than-normal days are linked to same-day US traffic-crash deaths.",
        "The excess is comparable to all officially recorded direct-heat deaths.",
        "Motorcyclists, pedestrians and cyclists face the largest heat risk.",
        "Uniform +1 to +3 C warming would add hundreds of deaths per year.",
        "Heat-aware road safety could target an uncounted climate-sensitive burden.",
    ]
    for bullet in highlights:
        p = doc.add_paragraph(bullet)
        p.paragraph_format.line_spacing = 1.5
        p.paragraph_format.space_after = Pt(6)
        try:
            p.style = doc.styles["List Bullet"]
        except Exception:
            pass
        if len(bullet) > 85:
            print(f"WARNING: highlight exceeds 85 characters ({len(bullet)})")
    doc.save(path)
    print("wrote", path)


def _build_cover_letter(path):
    doc = Document()
    mm.setup(doc)
    for block in JSR_COVER.strip().split("\n\n"):
        text = " ".join(block.splitlines())
        if text:
            p = doc.add_paragraph(text)
            p.paragraph_format.line_spacing = 1.15
            p.paragraph_format.space_after = Pt(6)
    doc.save(path)
    print("wrote", path)


def _build_submission_zip():
    zip_base = os.path.join(MAN, "jsr_submission_package")
    stage = zip_base + "_stage"
    if os.path.exists(stage):
        shutil.rmtree(stage)
    os.makedirs(stage)
    files = [
        "heat_crash_mortality_jsr.docx",      # anonymized main manuscript
        "jsr_title_page.docx",                # author details (separate)
        "jsr_highlights.docx",
        "jsr_cover_letter.docx",
        "strobe_checklist.docx",
    ]
    for name in files:
        src = os.path.join(MAN, name)
        if os.path.exists(src):
            shutil.copyfile(src, os.path.join(stage, name))
        else:
            print(f"WARNING: missing {name}")
    if os.path.exists(zip_base + ".zip"):
        os.remove(zip_base + ".zip")
    shutil.make_archive(zip_base, "zip", stage)
    shutil.rmtree(stage)
    print("wrote", zip_base + ".zip")


def main():
    os.makedirs(MAN, exist_ok=True)

    # Build a fresh inline base manuscript in a temp dir so tracked outputs
    # are not overwritten.
    tmpdir = tempfile.mkdtemp(prefix="jsr_build_", dir=MAN)
    original_man = mm.MAN
    mm.MAN = tmpdir
    try:
        mm.build_manuscript("tmp_inline.docx", embed=True)
    finally:
        mm.MAN = original_man

    _postprocess(os.path.join(tmpdir, "tmp_inline.docx"),
                 os.path.join(MAN, "heat_crash_mortality_jsr.docx"))
    shutil.rmtree(tmpdir)

    _build_title_page(os.path.join(MAN, "jsr_title_page.docx"))
    _build_highlights(os.path.join(MAN, "jsr_highlights.docx"))
    _build_cover_letter(os.path.join(MAN, "jsr_cover_letter.docx"))
    _build_submission_zip()


if __name__ == "__main__":
    main()
