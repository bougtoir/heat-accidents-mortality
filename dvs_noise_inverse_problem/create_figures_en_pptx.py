#!/usr/bin/env python3
"""Generate English figures for DVS × Noise Inverse Problem review as PPTX."""

from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch


def create_gap_map_figure_en():
    """Create English version of the 4-domain gap map."""
    fig, ax = plt.subplots(1, 1, figsize=(12, 8))

    domains = {
        'A': {'pos': (0.15, 0.7), 'label': 'A. DVS Noise\nPhysical Modeling\n(5 papers)', 'color': '#4ECDC4'},
        'B': {'pos': (0.55, 0.7), 'label': 'B. DVS Noise\nFiltering Methods\n(7 papers)', 'color': '#45B7D1'},
        'C': {'pos': (0.15, 0.15), 'label': 'C. DVS Astronomy\n& Space Apps\n(5 papers)', 'color': '#96CEB4'},
        'D': {'pos': (0.55, 0.15), 'label': 'D. Noise Inverse\nProblem (non-DVS)\n(5 papers)', 'color': '#FFEAA7'},
    }

    box_w, box_h = 0.28, 0.22
    for key, d in domains.items():
        x, y = d['pos']
        rect = FancyBboxPatch((x, y), box_w, box_h,
                              boxstyle="round,pad=0.02",
                              facecolor=d['color'], edgecolor='#333',
                              linewidth=2, alpha=0.85,
                              transform=ax.transAxes)
        ax.add_patch(rect)
        ax.text(x + box_w/2, y + box_h/2, d['label'],
                ha='center', va='center', fontsize=11, fontweight='bold',
                transform=ax.transAxes)

    gaps = {
        'g1': {'pos': (0.35, 0.55), 'label': 'g1\nA\u2192D Bridge\nForward Model\nInversion', 'color': '#FF6B6B'},
        'g2': {'pos': (0.7, 0.55), 'label': 'g2\nB\u2192D Bridge\nSelf-supervised\nNoise Learning', 'color': '#C44D58'},
        'g3': {'pos': (0.15, 0.48), 'label': 'g3\nA+B+C Integration\nFaint Astronomical\nObject Detection', 'color': '#E74C3C'},
        'g4': {'pos': (0.55, 0.48), 'label': 'g4\nA+B+C+D Full Integration\nLIGO-templated\nUnified Pipeline', 'color': '#C0392B'},
    }

    for key, g in gaps.items():
        x, y = g['pos']
        ellipse = mpatches.Ellipse((x + 0.12, y + 0.03), 0.26, 0.14,
                                   facecolor=g['color'], edgecolor='white',
                                   linewidth=2, alpha=0.9,
                                   transform=ax.transAxes)
        ax.add_patch(ellipse)
        ax.text(x + 0.12, y + 0.03, g['label'],
                ha='center', va='center', fontsize=8, color='white',
                fontweight='bold', transform=ax.transAxes)

    arrow_style = dict(arrowstyle='->', color='#555', lw=2)
    ax.annotate('', xy=(0.35, 0.82), xytext=(0.43, 0.82),
                xycoords='axes fraction', arrowprops=arrow_style)
    ax.annotate('', xy=(0.29, 0.7), xytext=(0.29, 0.37),
                xycoords='axes fraction', arrowprops=arrow_style)
    ax.annotate('', xy=(0.69, 0.7), xytext=(0.69, 0.37),
                xycoords='axes fraction', arrowprops=arrow_style)

    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.set_aspect('equal')
    ax.axis('off')
    ax.set_title('DVS \u00d7 Noise Inverse Problem: Four Domains and Unexplored Gaps',
                 fontsize=14, fontweight='bold', pad=20)

    plt.tight_layout()
    out = 'fig1_gap_map_en.png'
    fig.savefig(out, dpi=200, bbox_inches='tight', facecolor='white')
    plt.close()
    print(f'Saved: {out}')
    return out


def create_pipeline_figure_en():
    """Create English version of the g4 pipeline."""
    fig, ax = plt.subplots(1, 1, figsize=(14, 10))
    ax.set_xlim(0, 14)
    ax.set_ylim(0, 10)
    ax.axis('off')

    ax.text(7, 9.7, 'g4 Unified Pipeline: LIGO \u2192 DVS Transplant Architecture',
            ha='center', va='center', fontsize=14, fontweight='bold')

    inputs = [
        (1.5, 8.8, 'DVS Main Channel\ne(t,x,y,p)', '#4ECDC4'),
        (5.5, 8.8, 'Auxiliary Channels\nT(t), a(t), I(t)', '#45B7D1'),
        (9.5, 8.8, 'Physics Model\n(A5 Pixel Model)', '#96CEB4'),
    ]
    for x, y, label, color in inputs:
        rect = FancyBboxPatch((x-1.3, y-0.4), 2.6, 0.8,
                              boxstyle="round,pad=0.1",
                              facecolor=color, edgecolor='#333', linewidth=1.5)
        ax.add_patch(rect)
        ax.text(x, y, label, ha='center', va='center', fontsize=9)

    stages = [
        (7, 7.2, 'Stage 1: Noise Forward Model Construction\n\u03bb_noise(x,y,t) = F(\u03b8, T(t), bias, I_bg)', '#FFF3CD', 10, 0.8),
        (7, 5.8, 'Stage 2: Noise Inverse Problem Solving\n\u03b8\u0302 = argmin_\u03b8 D(e_obs, F(\u03b8)) \u2014 MLE / Variational / DeepClean-type NN', '#D1ECF1', 10, 0.8),
        (7, 4.4, 'Stage 3: Residual Event Stream Generation\ne_residual = e_obs \u2296 F(\u03b8\u0302) \u2014 Probabilistic Thinning / Rate Subtraction', '#D4EDDA', 10, 0.8),
        (7, 3.0, 'Stage 4: Faint Object Detection (= g3 Pipeline)\nCandidate trajectory shift-and-stack \u2192 Statistical test \u2192 Cataloging', '#F8D7DA', 10, 0.8),
        (7, 1.6, 'Stage 5: Physical Validation\nPSD test / Injection-Recovery / Known Object / Blind test', '#E2D5F1', 10, 0.8),
    ]

    for x, y, label, color, w, h in stages:
        rect = FancyBboxPatch((x - w/2, y - h/2), w, h,
                              boxstyle="round,pad=0.05",
                              facecolor=color, edgecolor='#333', linewidth=1.5)
        ax.add_patch(rect)
        ax.text(x, y, label, ha='center', va='center', fontsize=9)

    for y_from, y_to in [(8.4, 7.6), (6.8, 6.2), (5.4, 4.8), (4.0, 3.4), (2.6, 2.0)]:
        ax.annotate('', xy=(7, y_to), xytext=(7, y_from),
                    arrowprops=dict(arrowstyle='->', color='#333', lw=2))

    for x_from in [1.5, 5.5, 9.5]:
        ax.annotate('', xy=(7, 7.6), xytext=(x_from, 8.4),
                    arrowprops=dict(arrowstyle='->', color='#666', lw=1.5))

    plt.tight_layout()
    out = 'fig2_g4_pipeline_en.png'
    fig.savefig(out, dpi=200, bbox_inches='tight', facecolor='white')
    plt.close()
    print(f'Saved: {out}')
    return out


def create_pptx(fig_files):
    """Create English PPTX with figures."""
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)

    titles = [
        'Fig. 1: DVS \u00d7 Noise Inverse Problem \u2014 Four Research Domains and Unexplored Gaps',
        'Fig. 2: g4 Unified Pipeline \u2014 LIGO \u2192 DVS Transplant Architecture',
    ]
    captions = [
        'Prior work categorized into four domains (A: DVS noise physical modeling, B: DVS noise filtering, '
        'C: DVS astronomical applications, D: Noise inverse problem in non-DVS fields). '
        'Four unexplored gaps (g1\u2013g4) identified at domain intersections. g4 represents the most ambitious fully integrated approach.',
        'Five-stage architecture transplanting the LIGO noise reconstruction pipeline (Vajente et al. 2020) to DVS astronomical observation. '
        'Inputs: DVS main channel, auxiliary sensors (temperature, vibration, illuminance), and physics-based pixel model (A5). '
        'Pipeline: noise forward model \u2192 inverse problem solving \u2192 residual generation \u2192 faint object detection \u2192 physical validation.',
    ]

    for fig_path, title, caption in zip(fig_files, titles, captions):
        slide = prs.slides.add_slide(prs.slide_layouts[6])

        txBox = slide.shapes.add_textbox(Inches(0.5), Inches(0.2), Inches(12.3), Inches(0.6))
        tf = txBox.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.text = title
        p.font.size = Pt(20)
        p.font.bold = True
        p.alignment = PP_ALIGN.CENTER

        from PIL import Image
        img = Image.open(fig_path)
        img_w, img_h = img.size
        max_w = Inches(11)
        max_h = Inches(5.5)
        scale = min(max_w / Emu(int(img_w * 914400 / 200)),
                    max_h / Emu(int(img_h * 914400 / 200)))
        final_w = int(img_w * 914400 / 200 * scale)
        final_h = int(img_h * 914400 / 200 * scale)
        left = (prs.slide_width - final_w) // 2
        top = Inches(1.0)
        slide.shapes.add_picture(fig_path, left, top, final_w, final_h)

        txBox2 = slide.shapes.add_textbox(Inches(0.5), Inches(6.5), Inches(12.3), Inches(0.8))
        tf2 = txBox2.text_frame
        tf2.word_wrap = True
        p2 = tf2.paragraphs[0]
        p2.text = caption
        p2.font.size = Pt(11)
        p2.font.color.rgb = RGBColor(0x55, 0x55, 0x55)
        p2.alignment = PP_ALIGN.CENTER

    out = 'dvs_noise_inverse_problem_figures_en.pptx'
    prs.save(out)
    print(f'Saved: {out}')


if __name__ == '__main__':
    fig1 = create_gap_map_figure_en()
    fig2 = create_pipeline_figure_en()
    create_pptx([fig1, fig2])
