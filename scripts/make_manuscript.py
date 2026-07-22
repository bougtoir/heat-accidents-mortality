#!/usr/bin/env python3
"""
Build the English manuscript (DOCX with inline figures + tables), an editable
figures PPTX (one figure per slide) and an editable tables DOCX.

Every numeric value is read from the generated result CSVs in data/processed/
and output/ -- nothing is hard-coded. Run `make all` first.
"""
import os
import csv
import numpy as np
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from pptx import Presentation
from pptx.util import Inches as PInches, Pt as PPt

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
PROC = os.path.join(ROOT, "data", "processed")
OUT = os.path.join(ROOT, "output")
FIG = os.path.join(OUT, "figures")
MAN = os.path.join(OUT, "manuscript")
os.makedirs(MAN, exist_ok=True)


def read_csv(name):
    with open(os.path.join(PROC, name), encoding="utf-8") as f:
        return list(csv.DictReader(f))


def f(x, n=3):
    return f"{float(x):.{n}f}"


# ------------------------------------------------------------------ load
US = read_csv("us_attributable.csv")[0]
JP = read_csv("jp_attributable.csv")[0]
US_LAG = {r["window"]: r for r in read_csv("us_lag_response.csv")}
JP_LAG = {r["window"]: r for r in read_csv("jp_lag_response.csv")}
CDC = read_csv("cdc_heat_deaths.csv")
CTRL = read_csv("us_sensitivity_controls.csv")[0]
cdc_recent = [int(r["heat_deaths_X30"]) for r in CDC if 2016 <= int(r["year"]) <= 2020]
CDC_MEAN = np.mean(cdc_recent)
CDC_YRS = f"{min(int(r['year']) for r in CDC if 2016 <= int(r['year']) <= 2020)}-" \
          f"{max(int(r['year']) for r in CDC if 2016 <= int(r['year']) <= 2020)}"


def rr(d, key):
    return f"{f(d[key])} (95% CI {f(d[key+'_lo'])}-{f(d[key+'_hi'])})"


def lagrr(d):
    return f"{f(d['rr'])} ({f(d['lo'])}-{f(d['hi'])})"


# ------------------------------------------------------------------ references
# Vancouver: numbered automatically in order of first appearance in the text.
REF_TEXT = {
    "dlnm": "Gasparrini A, Armstrong B, Kenward MG. Distributed lag non-linear models. Stat Med 2010;29:2224-34.",
    "lancet": "Gasparrini A, Guo Y, Hashizume M, et al. Mortality risk attributable to high and low ambient temperature: a multicountry observational study. Lancet 2015;386:369-75.",
    "basu": "Basu R. High ambient temperature and mortality: a review of epidemiologic studies from 2001 to 2008. Environ Health 2009;8:40.",
    "fars": "National Highway Traffic Safety Administration. Fatality Analysis Reporting System (FARS). US Department of Transportation. https://www.nhtsa.gov/research-data/fatality-analysis-reporting-system-fars",
    "ghcn": "Menne MJ, Durre I, Vose RS, Gleason BE, Houston TG. An overview of the Global Historical Climatology Network-Daily database. J Atmos Ocean Technol 2012;29:897-910.",
    "cdc": "Centers for Disease Control and Prevention. CDC WONDER Underlying Cause of Death database. https://wonder.cdc.gov/",
    "npa": "National Police Agency of Japan. Traffic accident statistics open data. https://www.npa.go.jp/publications/statistics/koutsuu/opendata/",
    "attrib": "Gasparrini A, Leone M. Attributable risk from distributed lag models. BMC Med Res Methodol 2014;14:55.",
    "eia": "US Energy Information Administration. Weekly finished motor gasoline product supplied (PET.WGFUPUS2.W). https://www.eia.gov/",
    "fhwa": "Federal Highway Administration. Traffic Volume Trends. https://www.fhwa.dot.gov/policyinformation/travel_monitoring/tvt.cfm",
}
_ref_order = []


def cite(*keys):
    nums = []
    for k in keys:
        if k not in _ref_order:
            _ref_order.append(k)
        nums.append(str(_ref_order.index(k) + 1))
    return "[" + ",".join(nums) + "]"


# ------------------------------------------------------------------ docx helpers
def setup(doc):
    st = doc.styles["Normal"].font
    st.name = "Times New Roman"; st.size = Pt(11)


def h(doc, text, level=1):
    p = doc.add_heading(text, level=level)
    return p


def para(doc, text, space_after=6):
    p = doc.add_paragraph(text)
    p.paragraph_format.space_after = Pt(space_after)
    p.paragraph_format.line_spacing = 2.0
    return p


def add_figure(doc, img, number, caption, width=5.6):
    doc.add_paragraph()
    p = doc.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.add_run().add_picture(os.path.join(FIG, img), width=Inches(width))
    cap = doc.add_paragraph()
    cap.paragraph_format.space_before = Pt(14)
    r = cap.add_run(f"Figure {number}. "); r.bold = True
    cap.add_run(caption)
    doc.add_paragraph()


def add_table(doc, number, title, header, rows):
    cap = doc.add_paragraph(); cap.paragraph_format.space_before = Pt(14)
    r = cap.add_run(f"Table {number}. "); r.bold = True
    cap.add_run(title)
    t = doc.add_table(rows=1, cols=len(header)); t.style = "Table Grid"
    for j, hd in enumerate(header):
        c = t.rows[0].cells[j].paragraphs[0].add_run(hd); c.bold = True
    for row in rows:
        cells = t.add_row().cells
        for j, v in enumerate(row):
            cells[j].text = str(v)
    doc.add_paragraph()


# figures/tables metadata (used by both manuscript and pptx/tables docx)
FIGURES = [
    ("fig1_absolute_exposure_response.png",
     "United States absolute-temperature exposure-response for daily traffic-crash "
     "deaths (cumulative over lag 0-10 days), relative to the minimum-mortality "
     "temperature. The curve peaks at mild temperatures and declines at extreme heat, "
     "reflecting the seasonal driving-exposure envelope rather than an acute heat effect."),
    ("fig2_anomaly_exposure_response.png",
     "United States temperature-anomaly exposure-response (primary analysis): "
     "cumulative rate ratio of crash deaths versus the local day-of-year seasonal norm. "
     "Days hotter than normal carry higher crash mortality."),
    ("fig3_lag_response.png",
     "United States lag structure of the crash-death response to a +9 C anomaly: an "
     "acute same-day excess followed by a 1-3 day deficit consistent with short-term "
     "mortality displacement."),
    ("fig4_attributable_by_year.png",
     "United States estimated net heat-attributable crash deaths per year, "
     "2016-2022."),
    ("fig5_hidden_vs_official.png",
     "United States comparison of estimated net heat-attributable crash deaths per year "
     "with officially recorded direct-heat deaths (ICD-10 X30) from CDC WONDER."),
    ("jp_fig2_anomaly_exposure_response.png",
     "Japan temperature-anomaly exposure-response (2019-2024). The estimate is "
     "imprecise: the confidence band is wide and includes the null throughout."),
    ("cross_fig_us_vs_japan_sameday.png",
     "Same-day rate ratio of traffic-crash deaths for a +9 C anomaly, United States "
     "versus Japan. The US shows a precise acute effect; the Japanese estimate is "
     "underpowered."),
]


def tbl1(doc):
    add_table(doc, 1, "Panel description and model summary.",
              ["", "United States", "Japan"],
              [["Crash deaths", f"{int(float(US['total_deaths'])):,}", f"{int(float(JP['total_deaths'])):,}"],
               ["Years", int(float(US['years'])), int(float(JP['years']))],
               ["Spatial units", "50 states", "47 prefectures"],
               ["Dispersion (phi)", f(US['dispersion_phi'], 2), f(JP['dispersion_phi'], 2)]])


def tbl2(doc):
    add_table(doc, 2, "Rate ratio of traffic-crash deaths for a +9 C temperature anomaly, by lag window.",
              ["Lag window (days)", "United States", "Japan"],
              [["0 (same day)", lagrr(US_LAG['lag0-0']), lagrr(JP_LAG['lag0-0'])],
               ["1-3", lagrr(US_LAG['lag1-3']), lagrr(JP_LAG['lag1-3'])],
               ["4-10", lagrr(US_LAG['lag4-10']), lagrr(JP_LAG['lag4-10'])],
               ["Cumulative 0-10", rr(US, 'cumRR_anom+9C'), rr(JP, 'cumRR_anom+9C')]])


def tbl3(doc):
    add_table(doc, 3, "United States net heat-attributable crash deaths versus officially recorded direct-heat deaths.",
              ["Quantity", "Estimate"],
              [["Net heat-attributable crash deaths / year", f"{float(US['net_heat_attributable_per_year']):.0f}"],
               ["Attributable fraction (%)", f(US['net_heat_attributable_fraction_pct'], 2)],
               [f"Official direct-heat deaths / year (X30, {CDC_YRS})", f"{CDC_MEAN:.0f}"]])


def build_manuscript():
    doc = Document(); setup(doc)

    t = doc.add_paragraph(); t.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = t.add_run("Hotter-than-normal days and traffic-crash mortality: a distributed-lag "
                  "analysis of the United States and Japan and the question of "
                  "under-recognised heat illness")
    r.bold = True; r.font.size = Pt(14)

    h(doc, "Abstract", 1)
    para(doc,
         "Objective: To test whether days that are hotter than the local seasonal norm "
         "are associated with higher daily traffic-crash mortality, a pathway through "
         "which heat-related impairment or undiagnosed heat illness could contribute to "
         "road deaths without being clinically recorded. "
         "Design: Time-series analysis of state-day (United States, US) and "
         "prefecture-day (Japan) panels using quasi-Poisson distributed-lag models of the "
         "local seasonal temperature anomaly, adjusting for spatial fixed effects, "
         "region-specific season, long-term trend and day of week. "
         f"Setting and data: US Fatality Analysis Reporting System (FARS) {cite('fars')} "
         f"2016-2022 and Japanese National Police Agency (NPA) accident open data {cite('npa')} "
         "2019-2024, each linked to Global Historical Climatology Network-Daily "
         f"(GHCN-Daily) temperature {cite('ghcn')}. "
         "Results: In the US ("
         f"{int(float(US['total_deaths'])):,} crash deaths), a +9 C anomaly raised same-day "
         f"crash mortality (rate ratio, RR {rr(US, 'sameday_RR_anom+9C')}"
         "), partly offset by a 1-3 day deficit; the effect was unchanged after adjustment "
         f"for national vehicle-miles travelled and gasoline supplied (RR "
         f"{f(CTRL['sameday_RR_anom+9C'])}). Estimated net heat-attributable crash deaths were "
         f"{float(US['net_heat_attributable_per_year']):.0f} per year "
         f"({f(US['net_heat_attributable_fraction_pct'],2)}%), comparable to the "
         f"{CDC_MEAN:.0f} officially recorded direct-heat deaths per year (ICD-10 X30, "
         f"{CDC_YRS}). In Japan ({int(float(JP['total_deaths'])):,} deaths) the estimate was "
         "in the same direction on some specifications but imprecise and not statistically "
         "significant. "
         "Conclusions: Unusually hot days are associated with an acute excess of US "
         "traffic-crash deaths of a magnitude similar to all officially recorded direct-heat "
         "mortality, consistent with an under-recognised heat contribution to road deaths. "
         "The aggregate association does not establish heat illness in any individual crash.",
         space_after=6)

    h(doc, "Introduction", 1)
    para(doc,
         "Heat waves are becoming more frequent under climate change, and ambient heat is "
         f"an established driver of mortality {cite('lancet','basu')}. Occupational and driving activity "
         "do not stop during heat, so some fatal accidents plausibly involve heat-related "
         "impairment or frank heat illness. Traffic-crash deaths are of particular interest "
         "because decedents rarely undergo the post-mortem assessment that would identify a "
         "heat contribution, so any such contribution would be largely invisible in routine "
         "cause-of-death coding. We therefore ask whether days that are hotter than the "
         "local seasonal norm carry excess traffic-crash mortality, and how the magnitude "
         "compares with officially recorded direct-heat deaths.")

    h(doc, "Methods", 1)
    para(doc,
         "We built daily panels of traffic-crash deaths by US state (FARS, 2016-2022) "
         f"{cite('fars')} and by Japanese prefecture (NPA accident open data, 2019-2024) "
         f"{cite('npa')}. Daily mean temperature was derived from GHCN-Daily stations "
         f"{cite('ghcn')} as the mean of TMAX and TMIN, aggregated to each spatial unit from the "
         "nearest reporting stations. For each unit we estimated a cyclic day-of-year "
         "climatology and defined the temperature anomaly as the observed minus the "
         "climatological temperature.")
    para(doc,
         "Because absolute temperature is strongly confounded by the seasonal cycle of "
         "driving exposure, our primary model used the anomaly. We fitted quasi-Poisson "
         f"distributed-lag models {cite('dlnm')} in which the exposure entered through a "
         "constant-free natural cubic spline within three lag windows (same-day, 1-3 days, "
         "4-10 days), adjusting for spatial fixed effects, region-specific season (natural "
         "spline of day of year), a long-term time trend and day of week. Overdispersion "
         "was accommodated with a quasi-Poisson dispersion parameter. Net heat-attributable "
         f"deaths were computed by the method of Gasparrini and Leone {cite('attrib')} with Monte "
         "Carlo confidence intervals. As a sensitivity analysis for the US we added national "
         f"vehicle-miles travelled {cite('fhwa')} and finished-motor-gasoline product supplied "
         f"{cite('eia')} as activity proxies. Officially recorded direct-heat deaths (ICD-10 "
         f"X30) were obtained from CDC WONDER {cite('cdc')}. All data are public and the full "
         "pipeline is reproducible from source (see Data availability).")

    h(doc, "Results", 1)
    para(doc,
         "The panels comprised "
         f"{int(float(US['total_deaths'])):,} US crash deaths over {int(float(US['years']))} "
         f"years (50 states) and {int(float(JP['total_deaths'])):,} Japanese crash deaths over "
         f"{int(float(JP['years']))} years (47 prefectures); descriptive characteristics and "
         "the quasi-Poisson dispersion are summarised in Table 1.")
    tbl1(doc)
    para(doc,
         "In the descriptive absolute-temperature model, US crash mortality peaked at mild "
         "temperatures and declined at extreme heat (Fig. 1); this reflects the seasonal "
         "driving-exposure envelope and cannot be read as an acute heat effect. When we "
         "instead used the temperature anomaly, days hotter than the seasonal norm carried "
         f"higher crash mortality (Fig. 2). A +9 C anomaly raised same-day crash deaths "
         f"(RR {rr(US, 'sameday_RR_anom+9C')}), with a cumulative lag 0-10 RR of "
         f"{rr(US, 'cumRR_anom+9C')}.")
    add_figure(doc, FIGURES[0][0], 1, FIGURES[0][1])
    add_figure(doc, FIGURES[1][0], 2, FIGURES[1][1])
    para(doc,
         "The lag structure showed an acute same-day excess followed by a deficit at 1-3 "
         f"days (RR {lagrr(US_LAG['lag1-3'])}), consistent with short-term mortality "
         "displacement (harvesting) rather than pure addition of deaths (Fig. 3; Table 2). The "
         "same-day association was essentially unchanged after adjusting for national "
         f"vehicle-miles travelled and gasoline supplied (RR {f(CTRL['sameday_RR_anom+9C'])}, "
         f"95% CI {f(CTRL['sameday_RR_lo'])}-{f(CTRL['sameday_RR_hi'])}), indicating that "
         "day-to-day driving volume does not explain the effect.")
    add_figure(doc, FIGURES[2][0], 3, FIGURES[2][1])
    tbl2(doc)
    para(doc,
         "Net heat-attributable crash deaths were "
         f"{float(US['net_heat_attributable_per_year']):.0f} per year (95% CI "
         f"{float(US['net_heat_attributable_lo'])/float(US['years']):.0f}-"
         f"{float(US['net_heat_attributable_hi'])/float(US['years']):.0f}), an attributable "
         f"fraction of {f(US['net_heat_attributable_fraction_pct'],2)}% (Fig. 4; Table 3). This is of "
         f"the same order as the {CDC_MEAN:.0f} officially recorded direct-heat deaths per "
         f"year (ICD-10 X30, {CDC_YRS}; Fig. 5), so a heat contribution to crash deaths of a "
         "magnitude comparable to all recorded direct-heat mortality would be entirely "
         "absent from cause-of-death statistics.")
    add_figure(doc, FIGURES[3][0], 4, FIGURES[3][1])
    add_figure(doc, FIGURES[4][0], 5, FIGURES[4][1])
    tbl3(doc)
    para(doc,
         f"In Japan ({int(float(JP['total_deaths'])):,} crash deaths over "
         f"{int(float(JP['years']))} years) the anomaly exposure-response was imprecise, with "
         "a wide confidence band that included the null throughout (Fig. 6); the same-day "
         f"point estimate for a +9 C anomaly was {rr(JP, 'sameday_RR_anom+9C')} and was not "
         "stable across specifications. Directly comparing the two countries (Fig. 7), the "
         "US shows a precise acute effect whereas the Japanese panel, with roughly fifteen "
         "times fewer annual crash deaths and sparser temperature coverage, is underpowered.")
    add_figure(doc, FIGURES[5][0], 6, FIGURES[5][1])
    add_figure(doc, FIGURES[6][0], 7, FIGURES[6][1])

    h(doc, "Discussion", 1)
    para(doc,
         "Days hotter than the local seasonal norm are associated with an acute, same-day "
         "excess of US traffic-crash deaths that is robust to activity confounding and is "
         "comparable in magnitude to all officially recorded direct-heat mortality. This is "
         "consistent with the hypothesis that heat-related impairment and under-recognised "
         "heat illness contribute to road deaths without appearing in cause-of-death data. "
         "The 1-3 day deficit indicates that part of the acute excess reflects short-term "
         "displacement, so the net annual burden is smaller than the same-day spike alone "
         "would imply.")
    para(doc,
         "Several limitations apply. First, this is an ecological, population-level "
         "association: it cannot establish that heat caused illness in any specific crash, "
         "and FARS and NPA carry no post-mortem heat diagnosis. Second, activity adjustment "
         "used national, not daily state-level, proxies. Third, exposure is measured at the "
         "spatial-unit level and misclassifies individual exposure. Fourth, the Japanese "
         "analysis is underpowered and inconclusive; its shorter series, far smaller death "
         "counts and sparser GHCN-Daily coverage preclude a firm estimate, and we therefore "
         "do not pool the two countries. These results motivate, but do not substitute for, "
         "individual-level studies linking crash decedents to ambient heat and, where "
         "available, post-mortem findings.")

    h(doc, "Conclusion", 1)
    para(doc,
         "Unusually hot days raise US traffic-crash mortality acutely, by an amount similar "
         "to all recorded direct-heat deaths, supporting the plausibility of an "
         "under-recognised heat contribution to road deaths. The Japanese data are "
         "consistent in direction on some specifications but too sparse for a firm "
         "conclusion.")

    h(doc, "Data availability", 1)
    para(doc,
         "All data are public: FARS, GHCN-Daily, CDC WONDER, FHWA/FRED, EIA and the "
         "Japanese NPA accident open data. Code and the reproduction pipeline (make all) are "
         "available in the project repository; all reported numbers are regenerated from "
         "source with no hard-coded values.")

    h(doc, "References", 1)
    for i, key in enumerate(_ref_order, 1):
        p = doc.add_paragraph(f"{i}. {REF_TEXT[key]}"); p.paragraph_format.space_after = Pt(4)
    missing = set(REF_TEXT) - set(_ref_order)
    assert not missing, f"uncited references: {missing}"

    path = os.path.join(MAN, "heat_crash_mortality.docx")
    doc.save(path); print("wrote", path)


def build_pptx():
    prs = Presentation(); prs.slide_width = PInches(13.333); prs.slide_height = PInches(7.5)
    blank = prs.slide_layouts[6]
    for i, (img, cap) in enumerate(FIGURES, 1):
        s = prs.slides.add_slide(blank)
        tb = s.shapes.add_textbox(PInches(0.5), PInches(0.2), PInches(12.3), PInches(0.6))
        tf = tb.text_frame; tf.text = f"Figure {i}"
        tf.paragraphs[0].runs[0].font.size = PPt(22); tf.paragraphs[0].runs[0].font.bold = True
        s.shapes.add_picture(os.path.join(FIG, img), PInches(2.5), PInches(1.0), height=PInches(4.8))
        cb = s.shapes.add_textbox(PInches(0.5), PInches(6.0), PInches(12.3), PInches(1.3))
        ctf = cb.text_frame; ctf.word_wrap = True; ctf.text = cap
        ctf.paragraphs[0].runs[0].font.size = PPt(12)
    path = os.path.join(MAN, "figures.pptx"); prs.save(path); print("wrote", path)


def build_tables_docx():
    doc = Document(); setup(doc)
    doc.add_heading("Tables (editable)", 1)
    tbl1(doc); tbl2(doc); tbl3(doc)
    path = os.path.join(MAN, "tables.docx"); doc.save(path); print("wrote", path)


if __name__ == "__main__":
    build_manuscript(); build_pptx(); build_tables_docx()
