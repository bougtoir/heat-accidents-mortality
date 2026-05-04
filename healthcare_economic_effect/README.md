# Healthcare Expenditure as Economic Effect

A neutral sustainability framework that reframes healthcare spending from
"cost to be contained" to "investment with measurable economic returns."

## Core Thesis

Healthcare expenditure is simultaneously a **cost** and an **economic effect**.
This project integrates three analytical lenses:

1. **Input-Output (I-O) Multipliers** — healthcare spending as demand stimulus
   (Japan: 2.78x, OECD range: 1.7–2.9x)
2. **Health-Led Growth Hypothesis (HLGH)** — bidirectional causality between
   health spending and GDP growth (confirmed across 38 OECD countries)
3. **Health-Capital Tempo Effect** — deferred supply-side returns from
   health-capital stock accumulation (from `healthcare_tempo_poc`)

## Key Result

The **fiscal return ratio** τ·m / pf (effective tax rate × I-O multiplier ÷
public financing share) exceeds 1.0 in 8 of 9 countries examined, meaning
tax revenues from healthcare-induced economic activity **surpass** public
healthcare expenditure.

## Structure

```
healthcare_economic_effect/
├── scripts/
│   ├── analyze_healthcare_economic_effect.py   # Data + figures
│   ├── create_manuscript_ja.py                 # 日本語原稿 (docx + pptx)
│   └── create_manuscript_en.py                 # English manuscript (docx + pptx)
├── data/                                       # CSV outputs
├── output/
│   ├── docx/     # Manuscripts
│   ├── pptx/     # Editable figures (1 slide per figure)
│   └── figures/  # PNG figures
└── README.md
```

## Reproduce

```bash
cd healthcare_economic_effect
pip install python-docx python-pptx numpy pandas matplotlib
python scripts/analyze_healthcare_economic_effect.py
python scripts/create_manuscript_ja.py
python scripts/create_manuscript_en.py
```

## Connection to healthcare_tempo_poc

This project extends the tempo-effect PoC (Candidate A-H) by adding the
demand-side I-O multiplier dimension. The combined "dual-return" framework
captures both the immediate economic stimulus (demand) and the deferred
health-capital accumulation (supply) to evaluate sustainability neutrally.

## References

Key sources:
- Yamada & Imanaka (2015) *Environ Health Prev Med* — Japan I-O multiplier 2.78
- Dupor & Guerrero (2021) *Econ Inq* — US Medicare multiplier 1.7
- Ertuğrul et al. (2024) *Front Public Health* — HLGH in 38 OECD countries
- Maeda (2008) JMARI WP172 — Healthcare employment ripple effects in Japan
