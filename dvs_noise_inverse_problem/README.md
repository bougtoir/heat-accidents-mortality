# DVS Noise Inverse Problem — Results in Engineering submission

This repository contains the reproducible code and data pipeline for the
*Results in Engineering* (Elsevier) submission on event-camera noise removal.

## Quick start

```bash
pip install -r requirements.txt
python build_rie_submission.py
```

This regenerates every figure, summary JSON, and submission document from the
public EBSSA dataset and the code in this repository.

## Data

The public EBSSA event-camera dataset is downloaded automatically by
`tonic` on the first run of `noise_inverse_demo.py` and
`systematic_evaluation.py`.  The download is large (~12 GB, one file).

## Pipeline

| Script | Output |
|--------|--------|
| `create_figures_en_pptx.py` | `fig2_g3_pipeline_en.png` (Fig. 3, all-English pipeline) |
| `noise_inverse_demo.py` | `fig3_noise_inverse_demo.png`, `fig4_sn_improvement.png`, `results/demo_summary.json` |
| `systematic_evaluation.py` | `fig5_systematic_evaluation.png`, `fig6_a5_simulation.png`, `fig7_per_recording_comparison.png`, `results/evaluation_summary.json` |
| `results_in_engineering_submission/generate_sr_figures.py` | `sr_figures/fig1_schematic.png`, `fig2_sr_curves.png`, `fig3_optimal_rho.png`, `fig4_detection_probability.png`, `fig5_roc_comparison.png`, `fig7_dvs_application.png` |
| `results_in_engineering_submission/create_rie_*.py` | `manuscript_rie.docx`, `figures_rie.pptx`, `highlights_rie.docx`, `title_page_rie.docx`, `cover_letter_rie.docx` |

All numerical values in the submission documents are loaded from
`results/evaluation_summary.json` and `results/demo_summary.json`; nothing is
hard-coded.

## Requirements

See `requirements.txt`.  The `torch` CPU wheel is pulled from the PyTorch CPU
index.
