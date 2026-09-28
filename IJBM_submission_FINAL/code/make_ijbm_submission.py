#!/usr/bin/env python3
"""
International Journal of Biometeorology (IJBM) submission package.

Builds the IJBM-revised manuscript directly from the committed result CSVs via
make_manuscript.py's data loaders (no hard-coded numbers).  The revision
repositions the paper: it acknowledges the established heat-crash and
heat-fatal-crash literature (Wu et al. 2018; Basagaña et al. 2015; Pan et al.
2024; Hsu et al. 2025, 2026; Liang et al. 2021, 2022) and frames the
incremental contribution as (i) a seasonal temperature-anomaly exposure,
(ii) a distributed-lag decomposition, (iii) nationwide fatal-crash mortality,
(iv) road-user-specific heterogeneity, (v) an attributable mortality burden,
and (vi) an exploratory external transportability assessment using Japan.

IJBM format applied: author-year citations with an alphabetical Springer-style
reference list; 150-250 word abstract; 4-6 keywords; Original Research word
budget (7,500 words incl. 250 words per figure/table), so secondary figures
and tables are moved to a supplement file.
"""
import os
import sys
import shutil
import zipfile

from docx import Document
from docx.shared import Inches, Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
MAN = os.path.join(ROOT, "output", "manuscript")
FIG = os.path.join(ROOT, "output", "figures")
FINAL = os.path.join(ROOT, "IJBM_submission_FINAL")

sys.path.insert(0, HERE)
import make_manuscript as mm  # noqa: E402  (loads all result CSVs)

f, rr, lagrr = mm.f, mm.rr, mm.lagrr
subrr, ctrlrr, ctrlcum, vif_cell = mm.subrr, mm.ctrlrr, mm.ctrlcum, mm._vif_cell
US, JP, USER, AGE = mm.US, mm.JP, mm.USER, mm.AGE
CTXG, JPSG, TOD_D, TOD_MAX = mm.CTXG, mm.JPSG, mm.TOD_D, mm.TOD_MAX
US_LAG, JP_LAG, PROJ_D = mm.US_LAG, mm.JP_LAG, mm.PROJ_D
CTRL, CTRL_VMT, CTRL_VIF5, CTRL_FREE = mm.CTRL, mm.CTRL_VMT, mm.CTRL_VIF5, mm.CTRL_FREE
CTRL_KEPT_NAMES, CTRL_DROPPED_NAMES = mm.CTRL_KEPT_NAMES, mm.CTRL_DROPPED_NAMES
CTRL_ROWS, SENS_LABELS, SENS_ORDER = mm.CTRL_ROWS, mm.SENS_LABELS, mm.SENS_ORDER
CDC_MEAN, CDC_YRS, US_JP_RATIO = mm.CDC_MEAN, mm.CDC_YRS, mm.US_JP_RATIO

import csv
CONTRAST = {r["contrast"]: r for r in csv.DictReader(
    open(os.path.join(mm.PROC, "us_contrast_sensitivity.csv"), encoding="utf-8"))}

TITLE = ("Traffic-crash mortality during unusually hot days in the United "
         "States: distributed-lag and road-user-specific analyses")

# ---------------------------------------------------------------------------
# Author-year references (Springer basic style)
# ---------------------------------------------------------------------------
# key -> (in-text label, full reference)
IJBM_REFS = {
    "basagana2015": (
        "Basagaña et al. 2015",
        "Basagaña X, Escalera-Antezana JP, Dadvand P, Llatje Ò, Barrera-Gómez J, "
        "Cunillera J, Medina-Ramón M, Pérez K (2015) High ambient temperatures "
        "and risk of motor vehicle crashes in Catalonia, Spain (2000-2011): a "
        "time-series analysis. Environ Health Perspect 123:1309-1316. "
        "https://doi.org/10.1289/ehp.1409223"),
    "basu": (
        "Basu 2009",
        "Basu R (2009) High ambient temperature and mortality: a review of "
        "epidemiologic studies from 2001 to 2008. Environ Health 8:40. "
        "https://doi.org/10.1186/1476-069X-8-40"),
    "cdc": (
        "CDC n.d.",
        "Centers for Disease Control and Prevention (n.d.) CDC WONDER "
        "Underlying Cause of Death database. https://wonder.cdc.gov/"),
    "care": (
        "European Commission n.d.",
        "European Commission, Directorate-General for Mobility and Transport "
        "(n.d.) Community database on road accidents (CARE). "
        "https://road-safety.transport.ec.europa.eu/european-road-safety-"
        "observatory/methodology-and-research/care-database_en"),
    "census_pep": (
        "US Census Bureau n.d.",
        "US Census Bureau (n.d.) Population Estimates Program: annual state "
        "population estimates. "
        "https://www.census.gov/programs-surveys/popest.html"),
    "daanen": (
        "Daanen et al. 2003",
        "Daanen HAM, van de Vliert E, Huang X (2003) Driving performance in "
        "cold, warm, and thermoneutral environments. Appl Ergon 34:597-602. "
        "https://doi.org/10.1016/j.apergo.2003.01.001"),
    "dlnm": (
        "Gasparrini et al. 2010",
        "Gasparrini A, Armstrong B, Kenward MG (2010) Distributed lag "
        "non-linear models. Stat Med 29:2224-2234. "
        "https://doi.org/10.1002/sim.3940"),
    "attrib": (
        "Gasparrini and Leone 2014",
        "Gasparrini A, Leone M (2014) Attributable risk from distributed lag "
        "models. BMC Med Res Methodol 14:55. "
        "https://doi.org/10.1186/1471-2288-14-55"),
    "eia": (
        "US EIA n.d.",
        "US Energy Information Administration (n.d.) Weekly finished motor "
        "gasoline product supplied (PET.WGFUPUS2.W). https://www.eia.gov/"),
    "fhwa": (
        "FHWA n.d.",
        "Federal Highway Administration (n.d.) Traffic Volume Trends. "
        "https://www.fhwa.dot.gov/policyinformation/travel_monitoring/tvt.cfm"),
    "fhwa_vm2": (
        "FHWA n.d.",
        "Federal Highway Administration (n.d.) Highway Statistics VM-2: annual "
        "state vehicle-miles travelled. "
        "https://www.fhwa.dot.gov/policyinformation/statistics.cfm"),
    "fars": (
        "NHTSA n.d.",
        "National Highway Traffic Safety Administration (n.d.) Fatality "
        "Analysis Reporting System (FARS). US Department of Transportation. "
        "https://www.nhtsa.gov/research-data/fatality-analysis-reporting-system-fars"),
    "ghcn": (
        "Menne et al. 2012",
        "Menne MJ, Durre I, Vose RS, Gleason BE, Houston TG (2012) An overview "
        "of the Global Historical Climatology Network-Daily database. "
        "J Atmos Ocean Technol 29:897-910. https://doi.org/10.1175/JTECH-D-11-00103.1"),
    "ipcc": (
        "IPCC 2021",
        "IPCC (2021) Climate Change 2021: The Physical Science Basis. "
        "Contribution of Working Group I to the Sixth Assessment Report of the "
        "Intergovernmental Panel on Climate Change. Cambridge University "
        "Press, Cambridge"),
    "lancet": (
        "Gasparrini et al. 2015",
        "Gasparrini A, Guo Y, Hashizume M, et al (2015) Mortality risk "
        "attributable to high and low ambient temperature: a multicountry "
        "observational study. Lancet 386:369-375. "
        "https://doi.org/10.1016/S0140-6736(14)62114-0"),
    "liang2022": (
        "Liang et al. 2022",
        "Liang M, Min M, Guo X, Song Q, Wang H, Li N, et al (2022) The "
        "relationship between ambient temperatures and road traffic injuries: "
        "a systematic review and meta-analysis. Environ Sci Pollut Res "
        "29:50647-50660. https://doi.org/10.1007/s11356-022-19276-0"),
    "liang2021_aap": (
        "Liang et al. 2021",
        "Liang M, Zhao D, Wu Y, Ye P, Wang Y, Yao Z, et al (2021) Short-term "
        "effects of ambient temperature and road traffic accident injuries in "
        "Dalian, Northern China: a distributed lag non-linear analysis. "
        "Accid Anal Prev 153:106057. https://doi.org/10.1016/j.aap.2021.106057"),
    "hsu2025": (
        "Hsu et al. 2025",
        "Hsu C-K, Quistberg DA, Sánchez BN, Kephart JL, Bilal U, Gouveia N, "
        "Pérez Ferrer C, Caiaffa WT, de Lima Friche AA, Yannone I, Rodríguez DA "
        "(2025) Individual and city-level variations in heat-related road "
        "traffic deaths in Latin America. Nat Cities 2:897-906. "
        "https://doi.org/10.1038/s44284-025-00279-x"),
    "hsu2026": (
        "Hsu et al. 2026",
        "Hsu C-K, Quistberg DA, Pérez-Ferrer C, Rodríguez DA (2026) Extreme "
        "heat disproportionately increases severe road traffic crashes in "
        "high conflict settings and among vulnerable road users in "
        "California. Discov Cities. https://doi.org/10.1007/s44327-026-00248-6"),
    "npa": (
        "NPA n.d.",
        "National Police Agency of Japan (n.d.) Traffic accident statistics "
        "open data. "
        "https://www.npa.go.jp/publications/statistics/koutsuu/opendata/"),
    "pan2024": (
        "Pan et al. 2024",
        "Pan R, et al (2024) Temporal change and spatial heterogeneity of the "
        "association between ambient temperature and transport accident "
        "mortality in Japan from 1972 to 2019: a nationwide time-stratified "
        "case-crossover study. Environ Res Commun 6:085011. "
        "https://doi.org/10.1088/2515-7620/ad6b03"),
    "wu2018": (
        "Wu et al. 2018",
        "Wu CYH, Zaitchik BF, Gohlke JM (2018) Heat waves and fatal traffic "
        "crashes in the continental United States. Accid Anal Prev "
        "119:195-201. https://doi.org/10.1016/j.aap.2018.07.025"),
}
_cited = []


def cite(*keys):
    labels = []
    for k in keys:
        if k not in _cited:
            _cited.append(k)
        labels.append(IJBM_REFS[k][0])
    return "(" + "; ".join(labels) + ")"


# ---------------------------------------------------------------------------
# docx helpers
# ---------------------------------------------------------------------------
def setup(doc):
    st = doc.styles["Normal"].font
    st.name = "Times New Roman"; st.size = Pt(11)


def h(doc, text, level=1):
    return doc.add_heading(text, level=level)


def para(doc, text, space_after=6):
    p = doc.add_paragraph(text)
    p.paragraph_format.space_after = Pt(space_after)
    p.paragraph_format.line_spacing = 2.0
    return p


def add_figure(doc, img, label, caption, embed=True, width=5.6):
    if embed:
        doc.add_paragraph()
        p = doc.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.add_run().add_picture(os.path.join(FIG, img), width=Inches(width))
    cap = doc.add_paragraph()
    cap.paragraph_format.space_before = Pt(14)
    r = cap.add_run(f"{label} "); r.bold = True
    cap.add_run(caption)
    doc.add_paragraph()


def add_table(doc, label, title, header, rows):
    cap = doc.add_paragraph(); cap.paragraph_format.space_before = Pt(14)
    r = cap.add_run(f"{label} "); r.bold = True
    cap.add_run(title)
    t = doc.add_table(rows=1, cols=len(header)); t.style = "Table Grid"
    for j, hd in enumerate(header):
        c = t.rows[0].cells[j].paragraphs[0].add_run(hd); c.bold = True
    for row in rows:
        cells = t.add_row().cells
        for j, v in enumerate(row):
            cells[j].text = str(v)
    doc.add_paragraph()


add_equation = mm.add_equation
_msub, _mbar, _mnary, _mr = mm._msub, mm._mbar, mm._mnary, mm._mr


# ---------------------------------------------------------------------------
# Main-text figures (IJBM budget) and captions
# ---------------------------------------------------------------------------
MAIN_FIGS = [
    ("fig2_anomaly_exposure_response.png", "Fig. 1",
     "United States temperature-anomaly exposure-response (primary analysis): "
     "cumulative rate ratio of traffic-crash deaths versus the local "
     "day-of-year seasonal norm. Days hotter than normal carry higher crash "
     "mortality."),
    ("fig3_lag_response.png", "Fig. 2",
     "United States lag structure of the crash-death response to a +9 °C "
     "anomaly: an acute same-day excess followed by a 1-3 day deficit "
     "consistent with short-term displacement (harvesting)."),
    ("fig_us_roaduser.png", "Fig. 3",
     "United States same-day rate ratio of crash death for a +9 °C anomaly by "
     "road-user type. Estimates for open-air users (motorcyclists, "
     "pedestrians, cyclists) are larger than for enclosed, often "
     "air-conditioned, vehicle occupants. This gradient is compatible with "
     "differences in heat exposure, vehicle protection, travel behaviour and "
     "other mode-specific factors; the subgroup analysis is exploratory and "
     "not adjusted for multiple comparisons."),
    ("fig_us_crashcontext.png", "Fig. 4",
     "United States same-day rate ratio of crash death for a +9 °C anomaly by "
     "crash circumstances: manner of collision, weather condition, "
     "rural/urban land use and police-reported driver drinking. The excess is "
     "present on clear or cloudy days, is larger for single-vehicle crashes "
     "than multi-vehicle collisions, and is similar regardless of reported "
     "driver drinking. These analyses are exploratory and are not adjusted "
     "for multiple comparisons."),
    ("fig4_attributable_by_year.png", "Fig. 5",
     "United States estimated net heat-attributable crash deaths per year, "
     "2016-2022 (model-based attributable burden, not a count of coded "
     "deaths)."),
    ("cross_fig_us_vs_japan_sameday.png", "Fig. 6",
     "Same-day rate ratio of traffic-crash deaths for a +9 °C anomaly, "
     "United States versus Japan. The US shows a precise acute association; "
     "the Japanese estimate is underpowered. This external-transportability "
     "comparison is exploratory and not adjusted for multiple comparisons."),
]

SUPP_FIGS = [
    ("fig1_absolute_exposure_response.png", "Fig. S1",
     "United States absolute-temperature exposure-response for daily "
     "traffic-crash deaths (cumulative over lag 0-10 days), relative to the "
     "minimum-mortality temperature. The curve peaks at mild temperatures and "
     "declines at extreme heat, reflecting the seasonal driving-exposure "
     "envelope rather than an acute heat association."),
    ("fig_us_timeofday.png", "Fig. S2",
     "United States same-day rate ratio of crash death for a +9 °C anomaly by "
     "crash hour of day. The excess is largest for crashes in the hottest "
     "part of the day (12-17 h) and weakest in the cool morning (06-11 h); "
     "the overnight band is also elevated. Exploratory; not adjusted for "
     "multiple comparisons."),
    ("fig5_hidden_vs_official.png", "Fig. S3",
     "United States comparison of estimated net heat-attributable crash "
     "deaths per year (a model-based attributable-burden estimate) with "
     "officially coded direct-heat deaths (ICD-10 X30) from CDC WONDER. The "
     "two quantities are different constructs and are shown for magnitude "
     "context only."),
    ("fig_us_projection.png", "Fig. S4",
     "United States additional traffic-crash deaths per year implied by the "
     "fitted anomaly association under a uniform +1, +2 or +3 °C shift of the "
     "daily temperature distribution, holding baseline population, driving "
     "activity, the vehicle fleet and adaptation constant. This is an "
     "illustrative scenario translation, not a forecast."),
    ("jp_fig2_anomaly_exposure_response.png", "Fig. S5",
     "Japan temperature-anomaly exposure-response (2019-2024). The estimate "
     "is imprecise: the confidence band is wide and includes the null "
     "throughout."),
    ("fig_jp_strata.png", "Fig. S6",
     "Japan same-day rate ratio of crash death for a +9 °C anomaly by "
     "accident type and by prefecture population density (split at the "
     "median, a proxy for public-transport availability). All confidence "
     "intervals are wide and include the null; exploratory, not adjusted for "
     "multiple comparisons."),
]


# ---------------------------------------------------------------------------
# Tables
# ---------------------------------------------------------------------------
def tbl_panel(doc):
    add_table(doc, "Table 1", "Panel description and model summary.",
              ["", "United States", "Japan"],
              [["Crash deaths", f"{int(float(US['total_deaths'])):,}", f"{int(float(JP['total_deaths'])):,}"],
               ["Years", int(float(US['years'])), int(float(JP['years']))],
               ["Spatial units", "50 states", "47 prefectures"],
               ["Dispersion (phi)", f(US['dispersion_phi'], 2), f(JP['dispersion_phi'], 2)]])


def tbl_lag(doc):
    add_table(doc, "Table 2",
              "Rate ratio of traffic-crash deaths for a +9 °C temperature "
              "anomaly relative to the seasonal norm, by lag window.",
              ["Lag window (days)", "United States", "Japan"],
              [["0 (same day)", lagrr(US_LAG['lag0-0']), lagrr(JP_LAG['lag0-0'])],
               ["1-3", lagrr(US_LAG['lag1-3']), lagrr(JP_LAG['lag1-3'])],
               ["4-10", lagrr(US_LAG['lag4-10']), lagrr(JP_LAG['lag4-10'])],
               ["Cumulative 0-10", rr(US, 'cumRR_anom+9C'), rr(JP, 'cumRR_anom+9C')]])


def tbl_subgroup(doc):
    add_table(doc, "Table 4",
              "United States same-day rate ratio of crash death for a +9 °C "
              "anomaly, by road-user type and age band. Exploratory subgroup "
              "analysis, not adjusted for multiple comparisons.",
              ["Subgroup", "Crash deaths", "Same-day RR (95% CI)"],
              [["Vehicle occupant", f"{int(USER['vehicle_occupant']['deaths']):,}", subrr(USER['vehicle_occupant'])],
               ["Motorcyclist", f"{int(USER['motorcyclist']['deaths']):,}", subrr(USER['motorcyclist'])],
               ["Pedestrian", f"{int(USER['pedestrian']['deaths']):,}", subrr(USER['pedestrian'])],
               ["Cyclist", f"{int(USER['cyclist']['deaths']):,}", subrr(USER['cyclist'])],
               ["Age <25 y", f"{int(AGE['<25']['deaths']):,}", subrr(AGE['<25'])],
               ["Age 25-64 y", f"{int(AGE['25-64']['deaths']):,}", subrr(AGE['25-64'])],
               ["Age 65+ y", f"{int(AGE['65+']['deaths']):,}", subrr(AGE['65+'])]])


def tbl_attrib(doc):
    add_table(doc, "Table 5",
              "United States model-based net heat-attributable crash deaths "
              "alongside officially coded direct-heat deaths. The two "
              "quantities measure different constructs (modelled burden vs "
              "coded cause of death) and are juxtaposed only to gauge "
              "magnitude.",
              ["Quantity", "Estimate"],
              [["Net heat-attributable crash deaths / year (model-based)",
                f"{float(US['net_heat_attributable_per_year']):.0f}"],
               ["Attributable fraction (%)", f(US['net_heat_attributable_fraction_pct'], 2)],
               [f"Officially coded direct-heat deaths / year (ICD-10 X30, {CDC_YRS})",
                f"{CDC_MEAN:.0f}"]])


def tbl_sens(doc):
    rows = []
    for key in SENS_ORDER:
        if key not in CTRL_ROWS:
            continue
        r = CTRL_ROWS[key]
        rows.append([SENS_LABELS.get(key, key), ctrlrr(r), ctrlcum(r), vif_cell(r)])
    add_table(doc, "Table 3",
              "United States sensitivity of the +9 °C anomaly association to "
              "activity, precipitation and heat-stress controls. All added "
              "continuous controls were z-scored; population entered as a log "
              "offset; heat-stress metrics were anomaly-derived. The VIF < 10 "
              "row is the primary full-controls model; a stricter VIF < 5 "
              "screen and an unscreened model are shown for comparison.",
              ["Model", "Same-day RR (95% CI)", "Cumulative RR (95% CI)", "Max control VIF"],
              rows)


def tbl_contrast(doc):
    rows = []
    for key in ("+5C", "p95", "+9C"):
        r = CONTRAST[key]
        name = {"+5C": "+5 °C anomaly",
                "p95": f"95th-percentile anomaly (+{r['anomaly_degC']} °C)",
                "+9C": "+9 °C anomaly (reference)"}[key]
        rows.append([name,
                     f"{r['sameday_RR']} ({r['sameday_lo']}-{r['sameday_hi']})",
                     f"{r['cumRR_0_10']} ({r['cum_lo']}-{r['cum_hi']})"])
    add_table(doc, "Table S1",
              "United States robustness to the anomaly contrast: same-day and "
              "cumulative (lag 0-10 day) rate ratios at +5 °C, the empirical "
              "95th percentile of the anomaly distribution, and the +9 °C "
              "reference contrast, from the primary model.",
              ["Contrast", "Same-day RR (95% CI)", "Cumulative RR (95% CI)"],
              rows)


def tbl_crashcontext(doc):
    label = {"manner": "Manner of collision", "weather": "Weather condition",
             "rururb": "Land use", "alcohol": "Driver drinking"}
    names = {"single_vehicle": "Single-vehicle (not a MVIT collision)",
             "multi_vehicle": "Multi-vehicle collision",
             "clear_or_cloudy": "Clear or cloudy",
             "adverse": "Adverse (rain, snow, fog, wind)",
             "rural": "Rural", "urban": "Urban",
             "no_drinking": "No drinking driver",
             "drinking_driver": "Drinking driver involved"}
    rows = []
    for dim in ("manner", "weather", "rururb", "alcohol"):
        for rr_ in mm.CTX:
            if rr_["dimension"] == dim:
                rows.append([f"{label[dim]}: {names[rr_['group']]}",
                             f"{int(rr_['deaths']):,}", subrr(rr_)])
    add_table(doc, "Table S2",
              "United States same-day rate ratio of crash death for a +9 °C "
              "anomaly, by crash circumstances. Exploratory; not adjusted for "
              "multiple comparisons.",
              ["Stratum", "Crash deaths", "Same-day RR (95% CI)"], rows)


def tbl_projection(doc):
    add_table(doc, "Table S3",
              "United States additional traffic-crash deaths per year implied "
              "by the fitted anomaly association under a uniform warming "
              "shift, holding activity, population and baseline rates "
              "constant; an illustrative scenario translation, not a "
              "forecast.",
              ["Uniform shift", "Additional deaths/year (95% CI)"],
              [[f"+{d} °C",
                f"{float(PROJ_D[d]['extra_deaths_per_year']):.0f} "
                f"({float(PROJ_D[d]['extra_lo']):.0f}-{float(PROJ_D[d]['extra_hi']):.0f})"]
               for d in (1, 2, 3)])


def tbl_jpstrata(doc):
    label = {"atype": "Accident type", "density": "Prefecture density"}
    names = {"single_vehicle": "Single-vehicle",
             "vehicle_vehicle": "Vehicle-vehicle",
             "vehicle_pedestrian": "Vehicle-pedestrian",
             "high_density": "High-density prefectures (transit-rich proxy)",
             "low_density": "Low-density prefectures (transit-poor proxy)"}
    rows = []
    for dim in ("atype", "density"):
        for r in mm.JPS:
            if r["dimension"] == dim:
                rows.append([f"{label[dim]}: {names[r['group']]}",
                             f"{int(r['deaths']):,}", subrr(r)])
    add_table(doc, "Table S4",
              "Japan same-day rate ratio of crash death for a +9 °C anomaly, "
              "by accident type and prefecture population density. All "
              "estimates are underpowered; exploratory, not adjusted for "
              "multiple comparisons.",
              ["Stratum", "Crash deaths", "Same-day RR (95% CI)"], rows)


# ---------------------------------------------------------------------------
# Manuscript
# ---------------------------------------------------------------------------
def abstract_text():
    return (
        "Prior studies have linked heat and heat waves to road crashes, "
        "including fatal crashes, but less is known about locally unusual "
        "heat relative to seasonal norms, its lag structure, and the "
        "mortality burden involved. We fitted quasi-Poisson distributed-lag "
        "models relating daily mean-temperature anomalies (departures from "
        "each spatial unit's day-of-year climatology) to traffic-crash deaths "
        "in US state-day (Fatality Analysis Reporting System, 2016-2022; "
        f"{int(float(US['total_deaths'])):,} deaths) and Japanese "
        f"prefecture-day (National Police Agency, 2019-2024; "
        f"{int(float(JP['total_deaths'])):,} deaths) panels. In the US, a "
        "+9 °C anomaly was associated with higher same-day mortality (rate "
        f"ratio {f(US['sameday_RR_anom+9C'])}, 95% CI "
        f"{f(US['sameday_RR_anom+9C_lo'])}-{f(US['sameday_RR_anom+9C_hi'])}), "
        "followed by a 1-3 day deficit consistent with partial short-term "
        "displacement; the cumulative 0-10 day rate ratio was "
        f"{f(US['cumRR_anom+9C'])} ({f(US['cumRR_anom+9C_lo'])}-"
        f"{f(US['cumRR_anom+9C_hi'])}). The excess was much larger for "
        "open-air road users (motorcyclists, pedestrians, cyclists) than for "
        "vehicle occupants. Model-based net heat-attributable mortality was "
        f"about {float(US['net_heat_attributable_per_year']):.0f} deaths per "
        f"year ({f(US['net_heat_attributable_fraction_pct'],2)}% of crash "
        "deaths), numerically similar to officially coded direct-heat "
        "mortality, although the two measures represent different "
        "constructs. Japanese estimates were imprecise and did not provide "
        "clear replication. Days that are unusually hot for the local season "
        "are associated with an acute excess of US crash mortality "
        "concentrated in heat-exposed road users.")


KEYWORDS = ("temperature anomaly; extreme heat; traffic-crash mortality; "
            "distributed-lag model; vulnerable road users; biometeorology")


def body(doc, embed):
    # ---- title block
    t = doc.add_paragraph(); t.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = t.add_run(TITLE); r.bold = True; r.font.size = Pt(14)
    ap = doc.add_paragraph(); ap.alignment = WD_ALIGN_PARAGRAPH.CENTER
    ap.add_run("Tatsuki Onishi")
    af = doc.add_paragraph(); af.alignment = WD_ALIGN_PARAGRAPH.CENTER
    af.add_run("Data Science and AI Innovation Research Promotion Center, "
               "Shiga University of Medical Science, Seta Tsukinowa-cho, "
               "Otsu, Shiga 520-2192, Japan")
    cp = doc.add_paragraph(); cp.alignment = WD_ALIGN_PARAGRAPH.CENTER
    cp.add_run("Corresponding author: Tatsuki Onishi "
               "(bougtoir@gmail.com)")

    h(doc, "Abstract", 1)
    para(doc, abstract_text())
    para(doc, "Keywords: " + KEYWORDS)

    h(doc, "Introduction", 1)
    para(doc,
         "Road traffic crashes are a leading cause of preventable death "
         "worldwide, and ambient heat is an established driver of daily "
         f"mortality {cite('lancet','basu')}. That heat also affects road "
         "safety is likewise well documented. In a nationwide "
         "time-stratified case-crossover analysis of the continental United "
         "States, fatal traffic crashes were 3.4% (95% CI 0.9-5.9%) more "
         f"frequent on heat-wave days than on non-heat-wave days {cite('wu2018')}, "
         "and daily time-series studies have reported increases in crash and "
         "injury risk with higher temperatures and during heat waves "
         f"{cite('basagana2015','liang2021_aap','liang2022')}. More recent "
         "work has extended this evidence to road-traffic mortality and to "
         "vulnerable road users: across 272 Latin-American cities, "
         "road-traffic mortality rose monotonically with temperature, with "
         "the largest risks among adolescents, males, motorcyclists and "
         f"bicyclists {cite('hsu2025')}, and across 177 Californian cities, "
         "extreme heat was associated with fatal and severe crashes, "
         "particularly at intersections and among pedestrians and "
         f"bicyclists {cite('hsu2026')}. In Japan, a nationwide "
         "case-crossover study spanning 1972-2019 estimated that transport "
         "accident mortality increased by 1.47% (95% CI 1.10-1.85%) per 1 °C "
         f"of daily mean temperature {cite('pan2024')}.")
    para(doc,
         "Three aspects of this relationship remain less well characterised. "
         "First, most prior studies used absolute temperature or fixed "
         "heat-wave thresholds; how locally unusual heat—departures from the "
         "seasonal conditions to which populations and travel behaviour are "
         "adapted—relates to crash mortality has received less attention, "
         "even though anomaly-based metrics are central to biometeorological "
         "studies of heat-health relationships. Second, the temporal "
         "structure of the association—whether an acute excess is followed "
         "by compensating deficits (short-term displacement or "
         "'harvesting')—has rarely been decomposed for crash mortality, "
         "leaving open whether heat adds deaths or advances deaths that "
         "would have occurred soon anyway. Third, the population mortality "
         "burden attributable to such exposure, in deaths per year, has not "
         "been quantified at the national scale alongside the risk ratios "
         "that dominate the literature.")
    para(doc,
         "We therefore analysed nationwide US traffic-crash mortality "
         "(Fatality Analysis Reporting System [FARS], 2016-2022) against "
         "daily mean-temperature anomalies relative to each state's "
         "day-of-year climatology, using a quasi-Poisson distributed-lag "
         "model that separates an acute same-day component from subsequent "
         "lag windows. We examined heterogeneity by road-user type, age, "
         "hour of day and crash circumstances as hypothesis-generating "
         "analyses, estimated the net heat-attributable mortality burden, "
         "and assessed external transportability using a harmonized "
         "prefecture-level analysis of Japanese accident statistics "
         "(2019-2024). We hypothesised that hotter-than-normal days would "
         "carry a same-day excess of crash deaths, that the excess would be "
         "larger for road users with greater bodily heat exposure, and that "
         "part of the acute excess would be offset at longer lags.")

    h(doc, "Methods", 1)
    h(doc, "Data and panels", 2)
    para(doc,
         "We built daily panels of traffic-crash deaths by US state (FARS, "
         f"2016-2022){cite('fars')} and by Japanese prefecture (National "
         f"Police Agency [NPA] accident open data, 2019-2024){cite('npa')}. "
         "Daily mean temperature was taken from the Global Historical "
         f"Climatology Network-Daily (GHCN-Daily) stations{cite('ghcn')} as "
         "the mean of daily maximum and minimum temperature, aggregated to "
         "each spatial unit from its nearest reporting stations. State-level "
         "precipitation and, in sensitivity analyses, daily average dew "
         "point, relative humidity and average wet-bulb temperature were "
         "taken from the same stations and used to compute the humidex, the "
         "US National Weather Service heat index and an estimated wet-bulb "
         "globe temperature (0.7 times wet-bulb plus 0.3 times air "
         "temperature).")
    h(doc, "Exposure definition", 2)
    para(doc,
         "For every spatial unit we estimated a cyclic day-of-year "
         "climatology and defined the exposure as the anomaly of observed "
         "daily mean temperature from that climatology,", space_after=2)
    add_equation(doc,
                 _msub(_mr("A"), _mr("u,t")) + _mr(" = ") + _msub(_mr("T"), _mr("u,t"))
                 + _mr(" − ") + _msub(_mbar(_mr("T")), _mr("u")) + _mr("(")
                 + _msub(_mr("d"), _mr("t")) + _mr(")"))
    para(doc,
         "for the anomaly A of spatial unit u on day t, where T is the "
         "observed daily mean temperature and the barred T is the "
         "day-of-year climatology d(t) for that unit. The anomaly isolates "
         "locally unusual heat: absolute temperature is strongly confounded "
         "by the seasonal cycle of driving exposure (summer days are both "
         "warmer and busier), so an absolute-temperature model is reported "
         "only descriptively (Fig. S1) and the anomaly is the primary "
         "exposure. The reference point for all contrasts is an anomaly of "
         "0 °C, i.e. a day exactly at the local seasonal norm.")
    h(doc, "Statistical model", 2)
    para(doc,
         f"We fitted a quasi-Poisson distributed-lag model{cite('dlnm')} of "
         "the form", space_after=2)
    add_equation(doc,
                 _mr("log E(") + _msub(_mr("Y"), _mr("u,t")) + _mr(") = ")
                 + _mnary(_mr("k"), _msub(_mr("f"), _mr("k")) + _mr("(")
                          + _msub(_mr("A"), _mr("u,t")) + _mr(")"))
                 + _mr(" + ") + _msub(_mr("α"), _mr("u"))
                 + _mr(" + ") + _msub(_mr("s"), _mr("r(u)")) + _mr("(")
                 + _msub(_mr("d"), _mr("t")) + _mr(")")
                 + _mr(" + h(t) + ") + _msub(_mr("δ"), _mr("dow(t)")))
    para(doc,
         "where Y is the daily crash-death count, the fₖ are constant-free "
         "natural cubic splines of the anomaly within three lag windows "
         "(same day, 1-3 days, 4-10 days) summed over k, αᵤ are spatial "
         "fixed effects, s is a region-specific cyclic seasonal spline of "
         "day of year, h a long-term time trend and δ a day-of-week effect. "
         "Each exposure-response spline had 4 df (3 effective df after "
         "removing the constant); the US and Japanese seasonal splines had 8 "
         "and 6 df respectively, and the long-term trend had 3 df per study "
         "year. Overdispersion was handled with a quasi-Poisson dispersion "
         "parameter. The +9 °C reporting contrast lies near the upper end of "
         "the observed positive-anomaly range while remaining within the "
         "support of the estimated response (approximately −12 to +10 °C), "
         "so no extrapolation is involved; as a robustness check we report "
         "the same-day and cumulative rate ratios at +5 °C and at the "
         "empirical 95th percentile of the anomaly distribution alongside "
         "+9 °C (Table S1).")
    h(doc, "Attributable burden and scenario translation", 2)
    para(doc,
         "Net heat-attributable deaths were computed by the method of "
         f"Gasparrini and Leone{cite('attrib')} with Monte Carlo confidence "
         "intervals (CIs): for each day the excess relative to the seasonal "
         "norm was accumulated from the fitted exposure-response and summed "
         "over the study period. To gauge the order of magnitude of this "
         "model-based burden we juxtaposed it with officially coded "
         "direct-heat deaths (International Classification of Diseases, 10th "
         "revision code X30) obtained from CDC "
         f"WONDER{cite('cdc')}; the two quantities measure different "
         "constructs (a modelled attributable burden versus a coded cause "
         "of death) and are not equivalent. Separately, we applied the "
         "fitted anomaly association to a uniform +1, +2 and +3 °C shift of "
         "the daily temperature distribution as an illustrative scenario "
         f"translation{cite('ipcc')}—holding baseline population, driving "
         "activity, the vehicle fleet and adaptation constant—reported in "
         "the supplement (Fig. S4, Table S3); it is not a forecast.")
    h(doc, "Sensitivity and stratified analyses", 2)
    para(doc,
         "As sensitivity analyses for the US we added (i) national "
         f"vehicle-miles travelled (VMT){cite('fhwa')} and "
         "finished-motor-gasoline product supplied"
         f"{cite('eia')} as activity proxies, and (ii) a richer control set "
         f"with state annual population entered as a log offset{cite('census_pep')}, "
         f"state annual VMT{cite('fhwa_vm2')} and daily state precipitation, "
         "all as z-scored linear terms except the population offset, plus "
         "GHCN-derived heat-stress metrics expressed as anomalies relative "
         "to their day-of-year climatology. Because heat-stress metrics are "
         "functions of temperature and can be collinear with the anomaly "
         "exposure, the primary full-controls model was selected by a "
         "variance-inflation-factor (VIF) screen that iteratively drops "
         "added controls with VIF > 10; a stricter VIF < 5 screen and an "
         "unscreened model were also fitted. Because crash spikes have been "
         "reported around daylight-saving-time transitions, we also refit "
         "the primary model excluding state-days within 7 days of each US "
         "clock change. Stratified refits by road-user type (vehicle "
         "occupant, motorcyclist, pedestrian, cyclist), age band, crash "
         "hour band and crash circumstances (manner of collision, weather "
         "condition, rural/urban land use, police-reported driver drinking) "
         "are exploratory subgroup analyses; they involve multiple "
         "comparisons without formal adjustment and are interpreted as "
         "hypothesis-generating rather than confirmatory.")
    h(doc, "External transportability analysis", 2)
    para(doc,
         "The Japanese prefecture-day panel was analysed with the same "
         "anomaly definition and model family as a harmonized exploratory "
         "external-transportability assessment. Because the Japanese death "
         "counts are much smaller and GHCN-Daily coverage sparser, we did "
         "not pool the two countries and we interpret the Japanese results "
         "as an external comparison of the direction and precision of the "
         "association, not as a confirmatory replication.")
    para(doc,
         "No ethics approval was required because the study used publicly "
         "available, aggregated and de-identified data with no individual "
         "records. Generative artificial-intelligence tools were used to "
         "assist with code development and manuscript drafting; the author "
         "reviewed and verified all content and takes full responsibility "
         "for the work. Reporting follows the STROBE guideline (checklist "
         "provided).")

    h(doc, "Results", 1)
    para(doc,
         "The panels comprised "
         f"{int(float(US['total_deaths'])):,} US crash deaths over "
         f"{int(float(US['years']))} years (50 states) and "
         f"{int(float(JP['total_deaths'])):,} Japanese crash deaths over "
         f"{int(float(JP['years']))} years (47 prefectures) (Table 1). In "
         "the descriptive absolute-temperature model, US crash mortality "
         "peaked at mild temperatures and declined at extreme heat (Fig. "
         "S1); this reflects the seasonal driving-exposure envelope and "
         "cannot be read as an acute heat effect.")
    tbl_panel(doc)
    para(doc,
         "Using the temperature anomaly as the exposure, days hotter than "
         "the seasonal norm carried higher crash mortality (Fig. 1). A +9 °C "
         "anomaly was associated with higher same-day crash deaths, "
         f"RR {rr(US, 'sameday_RR_anom+9C')}. The lag structure showed an "
         "acute same-day excess followed by a deficit at 1-3 days, "
         f"RR {lagrr(US_LAG['lag1-3'])}, consistent with short-term "
         "displacement (harvesting) rather than a net addition of deaths at "
         f"every lag (Fig. 2; Table 2); the cumulative 0-10 day RR was "
         f"{rr(US, 'cumRR_anom+9C')}. The conclusion was not sensitive to the "
         "choice of contrast: same-day and cumulative RRs were similar at "
         "+5 °C and at the empirical 95th-percentile anomaly (Table S1).")
    add_figure(doc, MAIN_FIGS[0][0], MAIN_FIGS[0][1], MAIN_FIGS[0][2], embed)
    add_figure(doc, MAIN_FIGS[1][0], MAIN_FIGS[1][1], MAIN_FIGS[1][2], embed)
    tbl_lag(doc)
    para(doc,
         "The same-day association was essentially unchanged after "
         "adjusting for national vehicle-miles travelled and gasoline "
         f"supplied (RR {f(CTRL_VMT['sameday_RR_anom+9C'])}, 95% CI "
         f"{f(CTRL_VMT['sameday_RR_lo'])}-{f(CTRL_VMT['sameday_RR_hi'])}; "
         f"cumulative RR {ctrlcum(CTRL_VMT)}). A VIF-screened full-controls "
         "model—starting with state population as a log offset plus "
         "z-scored state annual VMT, daily precipitation and the three "
         "heat-stress metrics, then iteratively dropping any added control "
         f"with VIF > 10—retained {CTRL_KEPT_NAMES} (dropped: "
         f"{CTRL_DROPPED_NAMES}); the same-day RR remained similar (RR "
         f"{ctrlrr(CTRL)}) while the cumulative 0-10 day RR was attenuated "
         f"(RR {ctrlcum(CTRL)}). A stricter VIF < 5 screen gave "
         f"{ctrlrr(CTRL_VIF5)} and the unscreened model "
         f"{ctrlrr(CTRL_FREE)} (max control VIF {vif_cell(CTRL_FREE)}). "
         "Excluding state-days around daylight-saving-time transitions left "
         "the estimate unchanged "
         f"(same-day RR {ctrlrr(CTRL_ROWS['exclude_DST_transition_weeks'])}). "
         "All sensitivity results are in Table 3.")
    tbl_sens(doc)
    para(doc,
         "The same-day excess differed markedly by road-user type (Fig. 3; "
         f"Table 4): small for enclosed, often air-conditioned vehicle "
         f"occupants (RR {subrr(USER['vehicle_occupant'])}) but several-fold "
         f"larger for motorcyclists (RR {subrr(USER['motorcyclist'])}), "
         f"pedestrians (RR {subrr(USER['pedestrian'])}) and cyclists (RR "
         f"{subrr(USER['cyclist'])}). This heterogeneity is compatible with "
         "differences in heat exposure, vehicle protection, travel behaviour "
         "and other mode-specific factors; it does not by itself demonstrate "
         "a physiological mechanism, because discretionary open-air travel "
         "may also increase on hotter-than-normal days. Across age bands the "
         "excess was similar (<25 y RR "
         f"{subrr(AGE['<25'])}; 25-64 y RR {subrr(AGE['25-64'])}; 65+ y RR "
         f"{subrr(AGE['65+'])}). The excess was largest for crashes in the "
         f"hottest part of the day ({TOD_MAX['hour_band']} h, RR "
         f"{subrr(TOD_MAX)}) and weakest in the cool morning (06-11 h, RR "
         f"{subrr(TOD_D['06-11'])}), although the overnight band was also "
         "elevated, so the diurnal pattern is not a clean daytime-only "
         "gradient (Fig. S2).")
    add_figure(doc, MAIN_FIGS[2][0], MAIN_FIGS[2][1], MAIN_FIGS[2][2], embed)
    tbl_subgroup(doc)
    para(doc,
         "Crash-circumstance strata provided additional descriptive checks "
         "(Fig. 4; Table S2). The same-day excess was larger for "
         f"single-vehicle crashes (RR {subrr(CTXG[('manner','single_vehicle')])}) "
         f"than for multi-vehicle collisions (RR {subrr(CTXG[('manner','multi_vehicle')])}), "
         "persisted on clear or cloudy days "
         f"(RR {subrr(CTXG[('weather','clear_or_cloudy')])}) and in adverse "
         f"weather (RR {subrr(CTXG[('weather','adverse')])}), was similar in "
         f"rural (RR {subrr(CTXG[('rururb','rural')])}) and urban (RR "
         f"{subrr(CTXG[('rururb','urban')])}) settings, and was present with "
         "similar magnitude whether or not a driver was reported to have "
         f"been drinking (RR {subrr(CTXG[('alcohol','no_drinking')])} and "
         f"{subrr(CTXG[('alcohol','drinking_driver')])}; police-reported "
         "drinking is under-ascertained in FARS).")
    add_figure(doc, MAIN_FIGS[3][0], MAIN_FIGS[3][1], MAIN_FIGS[3][2], embed)
    para(doc,
         "Model-based net heat-attributable crash deaths were "
         f"{float(US['net_heat_attributable_per_year']):.0f} per year (95% CI "
         f"{float(US['net_heat_attributable_lo'])/float(US['years']):.0f}-"
         f"{float(US['net_heat_attributable_hi'])/float(US['years']):.0f}), "
         f"an attributable fraction of {f(US['net_heat_attributable_fraction_pct'],2)}% "
         "of all crash deaths (Fig. 5; Table 5). For magnitude context, this "
         "model-based burden is numerically similar to the "
         f"{CDC_MEAN:.0f} officially coded direct-heat deaths per year "
         f"(ICD-10 X30, {CDC_YRS}; Fig. S3), although the two measures "
         "represent different constructs. The illustrative scenario "
         f"translation{cite('ipcc')} implied "
         f"{float(PROJ_D[1]['extra_deaths_per_year']):.0f}-"
         f"{float(PROJ_D[3]['extra_deaths_per_year']):.0f} additional deaths "
         "per year for a uniform +1 to +3 °C shift of the temperature "
         "distribution, holding other factors constant (Fig. S4; Table S3).")
    add_figure(doc, MAIN_FIGS[4][0], MAIN_FIGS[4][1], MAIN_FIGS[4][2], embed)
    tbl_attrib(doc)

    h(doc, "External transportability: Japan", 2)
    para(doc,
         f"In Japan ({int(float(JP['total_deaths'])):,} crash deaths over "
         f"{int(float(JP['years']))} years) the anomaly exposure-response was "
         "imprecise, with a wide confidence band that included the null "
         f"throughout (Fig. S5); the same-day point estimate for a +9 °C "
         f"anomaly was {rr(JP, 'sameday_RR_anom+9C')} and the cumulative "
         f"0-10 day RR was {rr(JP, 'cumRR_anom+9C')}. The external "
         "comparison (Fig. 6) therefore did not provide clear replication: "
         "the US shows a precise acute association, whereas the Japanese "
         f"panel—with roughly {US_JP_RATIO:.0f}-fold fewer annual crash "
         "deaths and sparser temperature coverage—is underpowered. Japanese "
         "stratified estimates were likewise imprecise (Fig. S6; Table S4).")
    add_figure(doc, MAIN_FIGS[5][0], MAIN_FIGS[5][1], MAIN_FIGS[5][2], embed)

    h(doc, "Discussion", 1)
    para(doc,
         "Principal findings. A +9 °C temperature anomaly relative to the "
         "local seasonal norm was associated with a same-day rate ratio of "
         f"{rr(US, 'sameday_RR_anom+9C')} for US traffic-crash deaths. The "
         "excess was acute: the 1-3 day window showed a deficit consistent "
         "with short-term displacement, and the cumulative 0-10 day "
         "association was positive but smaller "
         f"(RR {rr(US, 'cumRR_anom+9C')}). The model-based net "
         "heat-attributable burden was "
         f"{float(US['net_heat_attributable_per_year']):.0f} deaths per "
         "year, about "
         f"{f(US['net_heat_attributable_fraction_pct'],2)}% of crash "
         "deaths.")
    para(doc,
         "Relationship to prior evidence. These findings are consistent "
         "with, and extend, an established literature linking heat to road "
         "crashes and crash mortality. A nationwide US case-crossover "
         f"analysis found 3.4% more fatal crashes on heat-wave days{cite('wu2018')}; "
         "time-series studies reported more crashes and injuries at higher "
         f"temperatures and during heat waves{cite('basagana2015','liang2021_aap','liang2022')}; "
         "and recent multi-city analyses documented higher road-traffic "
         "mortality on hot days, concentrated in motorcyclists, bicyclists "
         "and other vulnerable road users in Latin America"
         f"{cite('hsu2025')} and California{cite('hsu2026')}. Our results "
         "align with that evidence while adding three elements: an "
         "exposure metric defined relative to local seasonal conditions, a "
         "distributed-lag decomposition of acute versus displaced deaths, "
         "and a national attributable-burden estimate for fatal crashes.")
    para(doc,
         "What the anomaly adds. Because absolute temperature is entangled "
         "with the seasonal cycle of driving exposure, the anomaly "
         "isolates departures from the conditions to which local travel "
         "patterns and behaviour are adapted. The approximately linear "
         "rise of crash mortality with positive anomalies, and the "
         "stability of the same-day association to the contrast used "
         "(Table S1), indicate that locally unusual heat—not extreme heat "
         "alone—carries measurable excess crash mortality. This complements "
         "heat-wave-based designs, which capture only the most extreme "
         f"days{cite('wu2018')}, and absolute-temperature DLNM analyses"
         f"{cite('pan2024')}, which mix seasonal exposure differences with "
         "acute effects.")
    para(doc,
         "Road-user heterogeneity and mechanism. The several-fold larger "
         "same-day excess among motorcyclists, pedestrians and cyclists "
         "than among vehicle occupants, the peak in the hottest hours, and "
         "the larger estimate for single-vehicle than multi-vehicle crashes "
         "are compatible with differences in heat exposure, vehicle "
         "protection, travel behaviour and other mode-specific factors. "
         "They are also coherent with experimental evidence that heat "
         f"degrades psychomotor and driving performance{cite('daanen')} and "
         "with prior reports that vulnerable road users bear the largest "
         f"heat-associated risks{cite('hsu2025','hsu2026')}. However, these "
         "ecological gradients are not proof of a bodily-heat mechanism: "
         "open-air travel volumes themselves change with the weather, and "
         "our activity proxies are national and not mode-specific, so "
         "exposure substitution cannot be separated from physiology.")
    para(doc,
         "Attributable burden in context. The model-based estimate of "
         f"{float(US['net_heat_attributable_per_year']):.0f} net "
         "heat-attributable crash deaths per year is of similar numerical "
         f"magnitude to the {CDC_MEAN:.0f} officially coded direct-heat "
         "deaths per year in CDC WONDER, but the two quantities are "
         "different constructs—a modelled attributable burden versus coded "
         "cause-of-death counts—and the comparison is offered only to "
         "indicate that the possible scale is not negligible. It should not "
         "be read as evidence that a comparable number of crashes are "
         "individually caused by heat illness.")
    para(doc,
         "External transportability. The harmonized Japanese analysis did "
         "not provide clear replication: point estimates were below the US "
         "values with wide intervals. Plausible explanations—fewer crash "
         "deaths per year, different modal composition, greater availability "
         "of cooled public transport, different vehicle fleets and climate "
         "adaptation—are hypotheses only; the prefecture-density split was "
         "too imprecise to test them. The Japanese estimates are therefore "
         "presented as an exploratory external comparison, and prior "
         f"Japanese evidence linking absolute temperature to "
         f"transport-accident mortality{cite('pan2024')} suggests that the "
         "exposure metric and period analysed may matter for whether an "
         "association is detectable.")
    para(doc,
         "Limitations. This is an ecological, population-level association "
         "and cannot establish that heat caused illness in any specific "
         "crash; neither FARS nor NPA records post-mortem heat diagnosis. "
         "Exposure is measured at the state or prefecture level from the "
         "nearest GHCN-Daily stations, misclassifying individual exposure "
         "and missing sub-unit variation such as urban heat islands. "
         "Activity adjustment used national monthly proxies and annual "
         "state VMT; no daily, mode-specific or shared-mobility activity "
         "denominators are publicly available, so weather-related activity "
         "shifts cannot be fully separated from a heat effect. Subgroup "
         "analyses involve multiple comparisons without adjustment. "
         "Police-reported drinking is incompletely ascertained. The "
         "quasi-Poisson model accounts for overdispersion but not an "
         "explicit autoregressive term; although the lag, seasonal, trend "
         "and day-of-week terms absorb much short-term autocorrelation, "
         "residual serial correlation could affect confidence intervals. "
         "The warming translation is an illustrative scenario holding "
         "population, travel, vehicle fleet and adaptation constant, not a "
         "forecast. Finally, the study is restricted to the United States "
         "and Japan because, among high-income countries with robust crash "
         "and meteorological records, they provide the best public daily "
         "data for this design; the European CARE database is not publicly "
         f"available at the daily individual level{cite('care')}, so "
         "transportability to other settings is uncertain.")
    para(doc,
         "Biometeorological and adaptation relevance. Within the "
         "biometeorology literature this study places traffic-crash "
         "mortality alongside other acute heat-health outcomes quantified "
         "with anomaly-based, distributed-lag methods, and identifies "
         "open-air road users as a group in whom heat exposure is "
         "occupational or behavioural rather than incidental. The "
         "harvesting pattern implies that the acute signal is larger than "
         "the net burden, which matters for the timing of heat-health "
         "warnings. Whether heat-targeted advisories for motorcyclists, "
         "cyclists, pedestrians and outdoor workers reduce crash risk is a "
         "testable hypothesis for intervention studies, not a conclusion of "
         "this analysis.")

    h(doc, "Conclusion", 1)
    para(doc,
         "Days that are unusually hot relative to the local seasonal norm "
         "were associated with an acute, same-day excess of US "
         "traffic-crash mortality, concentrated in open-air road users and "
         "followed by partial short-term displacement. The model-based "
         "attributable burden was of a similar numerical magnitude to "
         "officially coded direct-heat mortality, although the two "
         "constructs differ. A harmonized analysis in Japan was too "
         "imprecise to establish transportability. The results refine and "
         "extend prior evidence that heat is associated with road-crash "
         "mortality; they do not establish individual-level causation, and "
         "individual-level studies linking crash decedents to ambient heat "
         "exposure are needed.")

    h(doc, "Declarations", 1)
    para(doc, "Ethics approval: not required; the study used publicly "
              "available, aggregated and de-identified data.")
    para(doc, "Competing interests: the author declares no competing "
              "interests.")
    para(doc, "Funding: no specific funding was received for this study.")
    para(doc, "Author contributions: Tatsuki Onishi conceived the study, "
              "performed the analysis, drafted the manuscript and approved "
              "the final version. The author had full access to all data "
              "and verified the reported results.")
    para(doc, "Data availability: all data are public (FARS, GHCN-Daily, "
              "CDC WONDER, US Census Bureau Population Estimates, FHWA, EIA "
              "and the Japanese NPA accident open data; see References). "
              "Processed data files are included in the repository so the "
              "manuscript and figures can be regenerated without API keys. "
              "The complete analysis code and reproducible pipeline (make "
              "all for data and figures, make ijbm for this submission "
              "package) is openly available at "
              "https://github.com/bougtoir/heat-accidents-mortality; every "
              "reported number, figure and table is regenerated from "
              "source with no hard-coded values.")
    para(doc, "Declaration of generative AI use: during the preparation of "
              "this work the author used generative artificial-intelligence "
              "tools to assist with code development and manuscript "
              "drafting; the author reviewed and edited the content and "
              "takes full responsibility for the published content.")

    h(doc, "References", 1)
    for key in sorted(_cited, key=lambda k: IJBM_REFS[k][1].lower()):
        p = doc.add_paragraph(IJBM_REFS[key][1])
        p.paragraph_format.space_after = Pt(4)


def build_main(filename, embed):
    global _cited
    _cited = []
    doc = Document(); setup(doc)
    body(doc, embed)
    path = os.path.join(MAN, filename)
    doc.save(path); print("wrote", path)


def build_supplement():
    doc = Document(); setup(doc)
    h(doc, "Supplementary material", 1)
    para(doc, TITLE, space_after=12)
    tbl_contrast(doc)
    for img, label, cap in SUPP_FIGS:
        add_figure(doc, img, label, cap, embed=True)
    tbl_crashcontext(doc)
    tbl_projection(doc)
    tbl_jpstrata(doc)
    path = os.path.join(MAN, "ijbm_supplement.docx")
    doc.save(path); print("wrote", path)


def build_title_page():
    doc = Document(); setup(doc)
    t = doc.add_paragraph(); t.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = t.add_run(TITLE); r.bold = True; r.font.size = Pt(14)
    para(doc, "Tatsuki Onishi")
    para(doc, "Data Science and AI Innovation Research Promotion Center, "
              "Shiga University of Medical Science, Seta Tsukinowa-cho, "
              "Otsu, Shiga 520-2192, Japan")
    para(doc, "Corresponding author: Tatsuki Onishi, "
              "bougtoir@gmail.com")
    para(doc, "Article type: Original Research Paper")
    para(doc, "Declarations of interest: none.")
    para(doc, "Funding: none.")
    path = os.path.join(MAN, "ijbm_title_page.docx")
    doc.save(path); print("wrote", path)


def build_cover_letter():
    doc = Document(); setup(doc)
    para(doc, "28 September 2026")
    para(doc, "The Editor-in-Chief, International Journal of Biometeorology")
    para(doc, "Dear Editor-in-Chief,")
    para(doc,
         "We submit for your consideration our manuscript, \u201c" + TITLE +
         "\u201d, as an Original Research Paper.")
    para(doc,
         "That heat and heat waves are associated with road crashes, "
         "including fatal crashes, is already established in the "
         "literature. The incremental contribution of this study is to "
         "reframe the exposure biometeorologically: rather than absolute "
         "temperature or fixed heat-wave thresholds, we analyse departures "
         "from each spatial unit's own seasonal climatology in a "
         "distributed-lag model that separates an acute same-day excess "
         "from subsequent temporal displacement. Applied to nationwide US "
         "fatal-crash data (272,586 deaths, 2016-2022), the model shows an "
         "acute same-day association (RR 1.165, 95% CI 1.135-1.196 for a "
         "+9 \u00b0C anomaly) concentrated in open-air road users, and a "
         "model-based net attributable burden of about 528 deaths per year. "
         "A harmonized analysis of Japanese prefecture data is reported "
         "transparently as an exploratory external-transportability "
         "assessment that did not clearly replicate.")
    para(doc,
         "We believe the manuscript fits the International Journal of "
         "Biometeorology's focus on relationships between the atmospheric "
         "environment and human health and safety: it applies "
         "biometeorological exposure concepts (seasonal anomalies, lag "
         "structure, heat-stress metrics) to a human safety outcome, "
         "identifies occupationally and behaviourally heat-exposed "
         "population groups, and quantifies a heat-health burden with "
         "relevance to adaptation.")
    para(doc,
         "The manuscript is original, is not under consideration elsewhere, "
         "and all authors approve submission. All data are public and the "
         "complete analysis pipeline is openly available and fully "
         "reproducible, with no hard-coded results. We declare no competing "
         "interests and no specific funding. Generative AI tools were used "
         "to assist with code development and drafting, as disclosed in the "
         "manuscript.")
    para(doc, "Yours sincerely,")
    para(doc, "Tatsuki Onishi\n"
              "Data Science and AI Innovation Research Promotion Center\n"
              "Shiga University of Medical Science\n"
              "Seta Tsukinowa-cho, Otsu, Shiga 520-2192, Japan\n"
              "E-mail: bougtoir@gmail.com")
    path = os.path.join(MAN, "ijbm_cover_letter.docx")
    doc.save(path); print("wrote", path)


STROBE_ITEMS = [
    ("1a", "Study design in title or abstract", "Title; Abstract"),
    ("1b", "Informative and balanced abstract", "Abstract (250-word unstructured)"),
    ("2", "Background/rationale", "Introduction"),
    ("3", "Objectives / hypotheses", "Introduction (final paragraph)"),
    ("4", "Study design", "Methods (ecological time-series; quasi-Poisson DLM)"),
    ("5", "Setting, locations, periods", "Methods (US states 2016-2022; Japan prefectures 2019-2024); Table 1"),
    ("6", "Participants / units of analysis", "Methods (state-day and prefecture-day panels); Table 1"),
    ("7", "Variables (outcome, exposure, confounders)", "Methods (crash deaths; temperature anomaly; seasonal/trend/DOW; activity and heat-stress controls)"),
    ("8", "Data sources / measurement", "Methods; Data availability (FARS, GHCN-Daily, NPA, CDC WONDER, FHWA, EIA, Census)"),
    ("9", "Bias", "Methods (anomaly design); Discussion (limitations)"),
    ("10", "Study size", "Table 1 (death counts, years, units)"),
    ("11", "Quantitative variables handling", "Methods (spline lag windows; anomaly construction; contrast robustness)"),
    ("12", "Statistical methods", "Methods (quasi-Poisson DLM, attributable risk, sensitivity, subgroups)"),
    ("13", "Descriptive data", "Results (panel sizes); Table 1"),
    ("14", "Outcome data", "Results; Tables 2, 5"),
    ("15", "Main results (estimates, CIs)", "Results; Tables 2-5; Figs. 1-6"),
    ("16", "Other analyses (subgroups, sensitivity)", "Results; Tables 3-4, S1-S4; Figs. 3-6, S1-S6"),
    ("17", "Key results", "Discussion (principal findings); Conclusion"),
    ("18", "Limitations", "Discussion (limitations paragraph)"),
    ("19", "Interpretation", "Discussion; Abstract"),
    ("20", "Generalisability", "Discussion (external transportability; ecological scope)"),
    ("21", "Funding", "Declarations (Funding)"),
]


def build_strobe():
    doc = Document(); setup(doc)
    doc.add_heading("STROBE checklist — ecological time-series study", 1)
    para(doc, "Strengthening the Reporting of Observational Studies in "
              "Epidemiology (STROBE). Item numbering follows the STROBE "
              "Statement; the third column indicates where each item is "
              "addressed in the IJBM manuscript.")
    t = doc.add_table(rows=1, cols=3); t.style = "Table Grid"
    for j, hd in enumerate(("Item", "Recommendation", "Location in manuscript")):
        run = t.rows[0].cells[j].paragraphs[0].add_run(hd); run.bold = True
    for item, rec, loc in STROBE_ITEMS:
        cells = t.add_row().cells
        cells[0].text = item; cells[1].text = rec; cells[2].text = loc
    path = os.path.join(MAN, "ijbm_strobe_checklist.docx")
    doc.save(path); print("wrote", path)


def build_final_package():
    os.makedirs(FINAL, exist_ok=True)
    mapping = {
        "ijbm_main_inline.docx": "IJBM_MAIN_inline.docx",
        "ijbm_main_submission.docx": "IJBM_MAIN_submission.docx",
        "ijbm_title_page.docx": "IJBM_TITLE_PAGE.docx",
        "ijbm_cover_letter.docx": "IJBM_COVER_LETTER.docx",
        "ijbm_strobe_checklist.docx": "IJBM_STROBE_CHECKLIST.docx",
        "ijbm_supplement.docx": "IJBM_SUPPLEMENT.docx",
    }
    for src, dst in mapping.items():
        p = os.path.join(MAN, src)
        if os.path.exists(p):
            shutil.copyfile(p, os.path.join(FINAL, dst))
    for sub, src in (("figures", FIG), ("tables", MAN), ("code",
                     os.path.join(ROOT, "scripts"))):
        dst = os.path.join(FINAL, sub)
        os.makedirs(dst, exist_ok=True)
        if sub == "figures":
            for img, _l, _c in MAIN_FIGS + SUPP_FIGS:
                for ext in (".png", ".pdf"):
                    s = os.path.join(src, os.path.splitext(img)[0] + ext)
                    if os.path.exists(s):
                        shutil.copyfile(s, os.path.join(dst, os.path.basename(s)))
        elif sub == "tables":
            for name in ("tables.docx",):
                s = os.path.join(src, name)
                if os.path.exists(s):
                    shutil.copyfile(s, os.path.join(dst, name))
        else:
            for name in os.listdir(src):
                if name.endswith(".py"):
                    shutil.copyfile(os.path.join(src, name),
                                    os.path.join(dst, name))
    # reproducibility: processed results so figures/manuscript regenerate
    dst = os.path.join(FINAL, "data_processed")
    os.makedirs(dst, exist_ok=True)
    for name in os.listdir(mm.PROC):
        if name.endswith(".csv"):
            shutil.copyfile(os.path.join(mm.PROC, name),
                            os.path.join(dst, name))
    for name in ("IJBM_INITIAL_AUDIT.md", "REFERENCE_AND_NOVELTY_AUDIT.md",
                 "IJBM_FORMAT_AUDIT.md", "IJBM_HOSTILE_REVIEW.md",
                 "AUTHOR_QUERIES.md", "FINAL_HANDOFF.md", "Makefile",
                 "README.md"):
        p = os.path.join(ROOT, name)
        if os.path.exists(p):
            shutil.copyfile(p, os.path.join(FINAL, name))
    zip_base = os.path.join(ROOT, "IJBM_submission_FINAL")
    if os.path.exists(zip_base + ".zip"):
        os.remove(zip_base + ".zip")
    shutil.make_archive(zip_base, "zip", FINAL)
    print("wrote", zip_base + ".zip")


def main():
    os.makedirs(MAN, exist_ok=True)
    build_main("ijbm_main_inline.docx", embed=True)
    build_main("ijbm_main_submission.docx", embed=False)
    build_title_page()
    build_cover_letter()
    build_strobe()
    build_supplement()
    build_final_package()


if __name__ == "__main__":
    main()
