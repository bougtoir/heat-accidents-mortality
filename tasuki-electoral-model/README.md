# TASUKI: Trust-Adjusted Scoring with Unified Knowledge Integration (襷)

A novel electoral accountability mechanism that institutionalizes retrospective evaluation by linking candidate trust coefficients to measured policy fulfillment.

**Target Journal:** JASSS (Journal of Artificial Societies and Social Simulation)

## Overview

TASUKI introduces a continuous accountability loop into representative democracy. The name derives from the Japanese 襷 (tasuki), the relay sash passed between runners in ekiden races — symbolizing the passing of accountability across electoral cycles.

### Core Mechanism
1. **Pledge Declaration** — Candidates declare weighted policy pledges before elections
2. **Election** — Citizens vote; effective votes are modulated by candidate trust coefficients
3. **Term in Office** — Elected officials implement policies
4. **Fulfillment Evaluation** — Independent body assesses pledge fulfillment
5. **Accountability Score** — Weighted sum of fulfillment scores: S = Σ wⱼ·fⱼ
6. **Trust Coefficient Update** — Score mapped to trust via influence function: τ = ω(S)

### Key Innovation
The trust coefficient attaches to **candidates**, not voters, preserving the one-person-one-vote principle while creating performance-based electoral incentives.

## Repository Structure

```
tasuki-electoral-model/
├── README.md                          # This file
├── DRD-CT_先行文献比較レポート.md       # Literature comparison report (Japanese)
├── src/
│   ├── create_figures.py              # Generate 6 PNG figures (matplotlib)
│   ├── create_pptx.py                 # Generate English & Japanese PPTX slides
│   ├── create_paper_en.py             # Generate English DOCX paper
│   └── create_paper_ja.py             # Generate Japanese DOCX paper
└── output/
    ├── figures/                        # Generated PNG figures (6 files)
    │   ├── fig1_conceptual_overview.png
    │   ├── fig2_influence_functions.png
    │   ├── fig3_simulation_results.png
    │   ├── fig4_adversarial.png
    │   ├── fig5_sensitivity.png
    │   └── fig6_positioning.png
    ├── docx/                           # Generated DOCX papers
    │   ├── TASUKI_JASSS_English.docx
    │   └── TASUKI_JASSS_Japanese.docx
    └── pptx/                           # Generated PPTX presentations
        ├── TASUKI_Figures_English.pptx  # Editable slides (English)
        └── TASUKI_Figures_Japanese.pptx # Editable slides (Japanese)
```

## Dependencies

```
pip install matplotlib numpy python-docx python-pptx Pillow
```

## Regenerating Output Files

```bash
# Generate figures first (required by other scripts)
python src/create_figures.py

# Generate papers
python src/create_paper_en.py
python src/create_paper_ja.py

# Generate presentations
python src/create_pptx.py
```

**Note:** The source scripts currently use hardcoded paths (`/home/ubuntu/figures/` and `/home/ubuntu/`). Adjust paths as needed for your environment.

## Paper Contents

- **ODD Protocol** compliant agent-based model description
- **6 figures**: conceptual overview, influence functions, simulation results, adversarial robustness, sensitivity analysis, theoretical positioning
- **Bilingual**: Full paper in both English and Japanese
- **Editable presentations**: PPTX with editable shapes for flow diagrams (Slides 1 & 6) and embedded images for simulation plots (Slides 2-5)

## License

All rights reserved. This is unpublished academic work.

---

# English Translation

---

# TASUKI: Trust-Adjusted Scoring with Unified Knowledge Integration (sash)

A novel electoral accountability mechanism that institutionalizes retrospective evaluation by linking candidate trust coefficients to measured policy fulfillment.

**Target Journal:** JASSS (Journal of Artificial Societies and Social Simulation)

##Overview

TASUKI introduces a continuous accountability loop into representative democracy. The name derives from the Japanese 襷 (tasuki), the relay sash passed between runners in ekiden races — symbolizing the passing of accountability across electoral cycles.
### Core Mechanism
1. **Pledge Declaration** — Candidates declare weighted policy pledges before elections
2. **Election** — Citizens vote; effective votes are modulated by candidate trust coefficients
3. **Term in Office** — Elected officials implement policies
4. **Fulfillment Evaluation** — Independent body assesses pledge fulfillment
5. **Accountability Score** — Weighted sum of fulfillment scores: S = Σ wⱼ·fⱼ
6. **Trust Coefficient Update** — Score mapped to trust via influence function: τ = ω(S)

### Key Innovation
The trust coefficient attaches to **candidates**, not voters, preserving the one-person-one-vote principle while creating performance-based electoral incentives.

## Repository Structure

````
tasuki-electoral-model/
├── README.md # This file
├── DRD-CT_Prior Literature Comparison Report.md # Literature comparison report (Japanese)
├── src/
│ ├── create_figures.py # Generate 6 PNG figures (matplotlib)
│ ├── create_pptx.py # Generate English & Japanese PPTX slides
│ ├── create_paper_en.py # Generate English DOCX paper
│   └── create_paper_ja.py             # Generate Japanese DOCX paper
└── output/
    ├── figures/                        # Generated PNG figures (6 files)
    │   ├── fig1_conceptual_overview.png
    │   ├── fig2_influence_functions.png
    │   ├── fig3_simulation_results.png
    │   ├── fig4_adversarial.png
    │   ├── fig5_sensitivity.png
    │   └── fig6_positioning.png
    ├── docx/                           # Generated DOCX papers
    │   ├── TASUKI_JASSS_English.docx
    │   └── TASUKI_JASSS_Japanese.docx
    └── pptx/                           # Generated PPTX presentations
        ├── TASUKI_Figures_English.pptx  # Editable slides (English)
        └── TASUKI_Figures_Japanese.pptx # Editable slides (Japanese)
```

## Dependencies

```
pip install matplotlib numpy python-docx python-pptx Pillow
```

## Regenerating Output Files

```bash
# Generate figures first (required by other scripts)
python src/create_figures.py

# Generate papers
python src/create_paper_en.py
python src/create_paper_ja.py

# Generate presentations
python src/create_pptx.py
```

**Note:** The source scripts currently use hardcoded paths (`/home/ubuntu/figures/` and `/home/ubuntu/`). Adjust paths as needed for your environment.

## Paper Contents

- **ODD Protocol** compliant agent-based model description
- **6 figures**: conceptual overview, influence functions, simulation results, adversarial robustness, sensitivity analysis, theoretical positioning
- **Bilingual**: Full paper in both English and Japanese
- **Editable presentations**: PPTX with editable shapes for flow diagrams (Slides 1 & 6) and embedded images for simulation plots (Slides 2-5)

## License

All rights reserved. This is unpublished academic work.

