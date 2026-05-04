"""
Generate A2 manuscript docx for JAMIA/JBI submission.
Ensemble Causal Discovery with Feedback Quantification.
"""

import os
import re
from docx import Document
from docx.shared import Pt, Inches, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FIG_DIR = os.path.join(BASE_DIR, 'figures')


GREEK = {
    r'\alpha': '\u03b1', r'\beta': '\u03b2', r'\gamma': '\u03b3',
    r'\delta': '\u03b4', r'\epsilon': '\u03b5', r'\varepsilon': '\u03b5',
    r'\zeta': '\u03b6', r'\eta': '\u03b7', r'\theta': '\u03b8',
    r'\iota': '\u03b9', r'\kappa': '\u03ba', r'\lambda': '\u03bb',
    r'\mu': '\u03bc', r'\nu': '\u03bd', r'\xi': '\u03be',
    r'\pi': '\u03c0', r'\rho': '\u03c1', r'\sigma': '\u03c3',
    r'\tau': '\u03c4', r'\phi': '\u03c6', r'\chi': '\u03c7',
    r'\psi': '\u03c8', r'\omega': '\u03c9', r'\Phi': '\u03a6',
    r'\Psi': '\u03a8', r'\Omega': '\u03a9', r'\Delta': '\u0394',
}

SYMBOLS = {
    r'\infty': '\u221e', r'\partial': '\u2202', r'\times': '\u00d7',
    r'\in': '\u2208', r'\to': '\u2192', r'\rightarrow': '\u2192',
    r'\leftarrow': '\u2190', r'\leftrightarrow': '\u2194',
    r'\leq': '\u2264', r'\geq': '\u2265', r'\neq': '\u2260',
    r'\approx': '\u2248', r'\equiv': '\u2261', r'\sim': '\u223c',
    r'\cdot': '\u00b7', r'\pm': '\u00b1', r'\perp': '\u22a5',
}

SUB_MAP = {
    '0': '\u2080', '1': '\u2081', '2': '\u2082', '3': '\u2083',
    '4': '\u2084', '5': '\u2085', '6': '\u2086', '7': '\u2087',
    '8': '\u2088', '9': '\u2089', 'i': '\u1d62', 'j': '\u2c7c',
    'k': '\u2096', 'n': '\u2099',
}

SUP_MAP = {
    '0': '\u2070', '1': '\u00b9', '2': '\u00b2', '3': '\u00b3',
    '4': '\u2074', '5': '\u2075', '6': '\u2076', '7': '\u2077',
    '8': '\u2078', '9': '\u2079', '*': '*', 'n': '\u207f',
}


def convert_math(text):
    """Convert inline $...$ to Unicode."""
    def process(m):
        s = m.group(1)
        for k, v in GREEK.items():
            s = s.replace(k, v)
        for k, v in SYMBOLS.items():
            s = s.replace(k, v)
        s = re.sub(r'\\text\{([^}]+)\}', r'\1', s)
        s = re.sub(r'\\mathrm\{([^}]+)\}', r'\1', s)
        s = re.sub(r'\\mathcal\{([^}])\}', lambda m2: m2.group(1), s)
        s = re.sub(r'\\hat\{([^}]+)\}', lambda m2: m2.group(1) + '\u0302', s)
        s = re.sub(r'\\bar\{([^}]+)\}', lambda m2: m2.group(1) + '\u0304', s)
        def sub_repl(m2):
            return ''.join(SUB_MAP.get(c, c) for c in m2.group(1))
        s = re.sub(r'_\{([^}]+)\}', sub_repl, s)
        s = re.sub(r'_([a-z0-9])', lambda m2: SUB_MAP.get(m2.group(1), '_' + m2.group(1)), s)
        def sup_repl(m2):
            return ''.join(SUP_MAP.get(c, c) for c in m2.group(1))
        s = re.sub(r'\^\{([^}]+)\}', sup_repl, s)
        s = re.sub(r'\^([a-z0-9*])', lambda m2: SUP_MAP.get(m2.group(1), '^' + m2.group(1)), s)
        s = s.replace('\\', '').replace('{', '').replace('}', '')
        return s
    # Inline math
    text = re.sub(r'(?<!\$)\$(?!\$)(.+?)(?<!\$)\$(?!\$)', process, text)
    return text


def add_figure(doc, image_path, caption, width=Inches(5.5)):
    """Add figure with caption."""
    if not os.path.exists(image_path):
        p = doc.add_paragraph(f'[Figure missing: {os.path.basename(image_path)}]')
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        return
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(12)
    run = p.add_run()
    run.add_picture(image_path, width=width)
    cap_p = doc.add_paragraph()
    cap_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    cap_p.paragraph_format.space_before = Pt(4)
    cap_p.paragraph_format.space_after = Pt(12)
    cap_run = cap_p.add_run(convert_math(caption))
    cap_run.font.size = Pt(9)
    cap_run.italic = True


def add_rich_paragraph(doc, text, style=None):
    """Add paragraph with bold/italic formatting."""
    text = convert_math(text)
    p = doc.add_paragraph(style=style)
    parts = re.split(r'\*\*(.+?)\*\*', text)
    for i, part in enumerate(parts):
        if i % 2 == 1:
            run = p.add_run(part)
            run.bold = True
        else:
            iparts = re.split(r'\*(.+?)\*', part)
            for j, ipart in enumerate(iparts):
                run = p.add_run(ipart)
                if j % 2 == 1:
                    run.italic = True
    return p


def generate_manuscript(md_file='manuscript_a2_ecd.md', out_file='manuscript_a2_ecd.docx', lang='en'):
    """Generate the A2 manuscript docx from markdown."""
    md_path = os.path.join(BASE_DIR, md_file)
    with open(md_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    doc = Document()
    style = doc.styles['Normal']
    style.font.name = 'Times New Roman'
    style.font.size = Pt(11)
    style.paragraph_format.space_after = Pt(6)
    style.paragraph_format.line_spacing = 1.15

    # Figure insertion points (after which section heading's content)
    if lang == 'ja':
        FIGURES = [
            ('## 5.', 'fig6_causal_dag.png',
             '\u56f31. DirectLiNGAM\u306b\u3088\u308b\u63a8\u5b9a\u56e0\u679cDAG\u3002\u77e2\u5370\u306e\u592a\u3055\u306f\u63a8\u5b9a\u56e0\u679c\u52b9\u679c|B_ij|\u3092\u793a\u3059\u3002'),
            ('### 3.1', 'fig5_hill_radar.png',
             '\u56f32. Hill\u306e9\u57fa\u6e96\u30ab\u30d0\u30ec\u30c3\u30b8\u3002ECD\uff08\u7d2b\uff09\u304c\u5358\u4e00\u624b\u6cd5\u3088\u308a\u5e83\u7bc4\u306a\u30ab\u30d0\u30ec\u30c3\u30b8\u3092\u9054\u6210\u3002'),
            ('### 5.3', 'fig3_hodge_decomposition.png',
             '\u56f33. \u56e0\u679c\u30d5\u30ed\u30fc\u306eHodge\u5206\u89e3\u3002\u5de6\uff1a\u52fe\u914d\uff08DAG\uff09\u6210\u5206\u3001\u4e2d\u592e\uff1a\u30ab\u30fc\u30eb\uff08\u30d5\u30a3\u30fc\u30c9\u30d0\u30c3\u30af\uff09\u6210\u5206\u3001\u53f3\uff1a\u7d71\u5408\u30d5\u30ed\u30fc\u3002'),
            ('### 6.1', 'fig4_direction_comparison.png',
             '\u56f34. 3\u624b\u6cd5\u306b\u3088\u308b\u56e0\u679c\u65b9\u5411\u6bd4\u8f03\u3002\u5168\u8fba\u30da\u30a2\u3067\u306e\u4e00\u81f4\u30fb\u4e0d\u4e00\u81f4\u3002'),
            ('### 6.2', 'fig7_lingam_vs_spectral.png',
             '\u56f35. LiNGAM DAG\uff08\u5de6\uff09vs \u30b9\u30da\u30af\u30c8\u30eb\u56e0\u679c\u6027DCG\uff08\u53f3\uff09\u3002\u7834\u7dda\uff1a\u30d5\u30a3\u30fc\u30c9\u30d0\u30c3\u30af\u8fba\u3002'),
            ('### 8.2', 'fig9_ecd_pruning_analysis.png',
             '\u56f36. ECD\u30a2\u30f3\u30b5\u30f3\u30d6\u30eb\u30fb\u30d7\u30eb\u30fc\u30cb\u30f3\u30b0\u89e3\u6790\u3002\u8fba\u30ec\u30d9\u30eb\u30d5\u30a3\u30fc\u30c9\u30d0\u30c3\u30af\u7387\u3002'),
            ('### 7.1', 'fig8_alpha_sweep.png',
             '\u56f37. DAG\u8ee2\u79fb\u89e3\u6790\u3002(A) r_gradient vs \u03b1\u3001(B) \u8fba\u6570\u3068LiNGAM\u4e00\u81f4\u7387\u3002'),
        ]
    else:
        FIGURES = [
            ('## 5.', 'fig6_causal_dag.png',
             'Figure 1. Estimated causal DAG from DirectLiNGAM. Arrow weight indicates estimated causal effect |B_ij|.'),
            ('### 3.1', 'fig5_hill_radar.png',
             "Figure 2. Hill's nine criteria coverage. ECD (purple) achieves broader coverage than any single method."),
            ('### 6.1', 'fig4_direction_comparison.png',
             'Figure 3. Three-method causal direction comparison across all edge pairs.'),
            ('### 6.2', 'fig7_lingam_vs_spectral.png',
             'Figure 4. LiNGAM DAG (left) vs. Spectral Causality DCG (right). Dashed lines: feedback edges.'),
            ('### 8.2', 'fig9_ecd_pruning_analysis.png',
             'Figure 5. ECD ensemble and pruning analysis with edge-level feedback rates.'),
        ]

    figure_triggers = {}  # section_key -> (fig_file, caption)
    for trigger, fig_file, caption in FIGURES:
        figure_triggers[trigger] = (fig_file, caption)

    i = 0
    current_heading = ''
    in_display_math = False
    math_buffer = []
    table_buffer = []
    in_table = False
    figures_inserted = set()

    while i < len(lines):
        line = lines[i].rstrip('\n')
        i += 1

        # Display math block
        if line.strip() == '$$':
            if in_display_math:
                # End of display math
                math_text = ' '.join(math_buffer)
                p = doc.add_paragraph()
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER
                p.paragraph_format.space_before = Pt(6)
                p.paragraph_format.space_after = Pt(6)
                run = p.add_run(convert_math('$' + math_text + '$'))
                run.font.name = 'Cambria Math'
                in_display_math = False
                math_buffer = []
            else:
                in_display_math = True
                math_buffer = []
            continue

        if in_display_math:
            math_buffer.append(line.strip())
            continue

        # Table handling
        if line.strip().startswith('|') and '|' in line.strip()[1:]:
            if not in_table:
                in_table = True
                table_buffer = []
            table_buffer.append(line)
            continue
        elif in_table:
            # Flush table
            _flush_table(doc, table_buffer)
            in_table = False
            table_buffer = []

        # Skip image links
        if re.match(r'^!\[.*\]\(.*\)', line.strip()):
            continue

        # Horizontal rule
        if line.strip() == '---':
            continue

        # Headings
        if line.startswith('# ') and not line.startswith('## '):
            p = doc.add_paragraph()
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p.paragraph_format.space_before = Pt(24)
            run = p.add_run(line[2:].strip())
            run.bold = True
            run.font.size = Pt(14)
            continue

        if line.startswith('## '):
            heading = line[3:].strip()
            doc.add_heading(heading, level=1)
            current_heading = line.strip()
            continue

        if line.startswith('### '):
            heading = line[4:].strip()
            doc.add_heading(heading, level=2)
            current_heading = line.strip()
            continue

        if line.startswith('#### '):
            heading = line[5:].strip()
            doc.add_heading(heading, level=3)
            continue

        # Blockquote
        if line.startswith('> '):
            text = line[2:].strip()
            p = add_rich_paragraph(doc, text)
            p.paragraph_format.left_indent = Inches(0.5)
            continue

        # Bullet list
        if line.strip().startswith('- ') or line.strip().startswith('* '):
            text = line.strip()[2:]
            add_rich_paragraph(doc, text, style='List Bullet')
            continue

        # Numbered list
        num_match = re.match(r'^(\d+)\.\s+(.+)', line.strip())
        if num_match:
            text = f'{num_match.group(1)}. {num_match.group(2)}'
            add_rich_paragraph(doc, text)
            continue

        # Inline display math ($$...$$on single line)
        if line.strip().startswith('$$') and line.strip().endswith('$$') and len(line.strip()) > 4:
            math_text = line.strip()[2:-2]
            p = doc.add_paragraph()
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            run = p.add_run(convert_math('$' + math_text + '$'))
            run.font.name = 'Cambria Math'
            continue

        # Empty line
        if not line.strip():
            # Check if we should insert a figure
            for trigger, (fig_file, caption) in figure_triggers.items():
                if trigger in current_heading and fig_file not in figures_inserted:
                    fig_path = os.path.join(FIG_DIR, fig_file)
                    add_figure(doc, fig_path, caption)
                    figures_inserted.add(fig_file)
                    break
            continue

        # Regular paragraph
        add_rich_paragraph(doc, line.strip())

    # Flush any remaining table
    if in_table and table_buffer:
        _flush_table(doc, table_buffer)

    out_path = os.path.join(BASE_DIR, out_file)
    doc.save(out_path)
    print(f'Saved: {out_path}')
    return out_path


def _flush_table(doc, table_lines):
    """Parse and add a markdown table."""
    data_lines = [l for l in table_lines if not re.match(r'^\s*\|[-:\s|]+\|\s*$', l)]
    if not data_lines:
        return
    rows = []
    for line in data_lines:
        cells = [c.strip() for c in line.strip().strip('|').split('|')]
        rows.append(cells)
    if len(rows) < 1:
        return
    ncols = max(len(r) for r in rows)
    table = doc.add_table(rows=len(rows), cols=ncols)
    table.style = 'Table Grid'
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    for ri, row_data in enumerate(rows):
        for ci, cell_text in enumerate(row_data):
            if ci < ncols:
                cell = table.rows[ri].cells[ci]
                cell.text = ''
                p = cell.paragraphs[0]
                run = p.add_run(convert_math(cell_text))
                run.font.size = Pt(9)
                if ri == 0:
                    run.bold = True
    doc.add_paragraph('')


def generate_cover_letter():
    """Generate cover letter for JBI."""
    doc = Document()
    style = doc.styles['Normal']
    style.font.name = 'Times New Roman'
    style.font.size = Pt(11)
    style.paragraph_format.space_after = Pt(6)
    style.paragraph_format.line_spacing = 1.15

    doc.add_paragraph('[Date]')
    doc.add_paragraph('')

    p = doc.add_paragraph()
    p.add_run('Editors-in-Chief').bold = True
    doc.add_paragraph('Journal of Biomedical Informatics')
    doc.add_paragraph('Elsevier')
    doc.add_paragraph('')

    p = doc.add_paragraph()
    p.add_run('Re: Submission of manuscript entitled ')
    run = p.add_run('"Ensemble Causal Discovery with Feedback Quantification: '
        'Integrating Spectral Graph Methods and LiNGAM for Clinical Causal Inference"')
    run.italic = True
    doc.add_paragraph('')

    doc.add_paragraph('Dear Editors,')
    doc.add_paragraph('')

    doc.add_paragraph(
        'We are pleased to submit the above-titled manuscript for consideration as an '
        'Original Research Article in the Journal of Biomedical Informatics. This manuscript '
        'presents Ensemble Causal Discovery (ECD), a novel pipeline that integrates LiNGAM\u2019s '
        'identifiability guarantees with spectral causality\u2019s feedback quantification to '
        'enable clinically meaningful causal inference that accommodates feedback loops.'
    )

    doc.add_paragraph(
        'We believe JBI is the ideal venue for this work because: (1) It directly addresses '
        'the gap between causal discovery methods and clinical applicability\u2014a topic of '
        'growing interest in biomedical informatics. (2) The ECD pipeline produces interventionability '
        'scores that map graph-theoretic quantities to clinical actionability, providing a bridge '
        'between mathematical methods and clinical decision support. (3) We provide a practical '
        'deployment pipeline with bootstrap-based pruning that clinician-researchers can apply to '
        'their own datasets.'
    )

    doc.add_paragraph('Key contributions include:')
    items = [
        'A principled method for quantifying edge-level feedback rates in clinical causal graphs, '
        'allowing clinicians to identify when the DAG assumption is appropriate and when it masks '
        'important pathophysiological cycles.',
        'An interventionability score linking Hodge causal potential to clinical actionability, '
        'validated against established treatment guidelines (statins for cholesterol, antihypertensives '
        'for blood pressure).',
        'Broader coverage of Hill\u2019s nine epidemiological criteria than any single method alone, '
        'with spectral causality contributing H6 (biological plausibility), H7 (coherence), and H9 (analogy).',
        'A DAG transition analysis revealing that knowledge quality (p*_flip \u2248 0.15) '
        'rather than quantity is the critical threshold for valid causal structure.',
    ]
    for item in items:
        doc.add_paragraph(item, style='List Bullet')

    doc.add_paragraph('')
    doc.add_paragraph(
        'We confirm that this manuscript has not been previously published and is not under '
        'simultaneous consideration elsewhere. A companion paper presenting the full mathematical '
        'foundations and identifiability theory of spectral causality has been submitted separately '
        'to a theoretical venue [Reference 7 in the manuscript]. The present manuscript focuses '
        'exclusively on the ensemble framework, clinical interpretation, and practical deployment '
        'aspects that are not covered in the companion paper. All authors have approved the '
        'manuscript and agree with its submission. The authors declare no conflicts of interest.'
    )

    doc.add_paragraph('')
    p = doc.add_paragraph()
    p.add_run('Suggested reviewers:').bold = True
    reviewers = [
        'Prof. Markus P\u00fcschel (ETH Z\u00fcrich) \u2014 Graph signal processing and causal structure',
        'Prof. Kun Zhang (Carnegie Mellon University) \u2014 Causal discovery and identifiability',
        'Prof. Lucila Ohno-Machado (Yale University) \u2014 Biomedical informatics and clinical causal inference',
    ]
    for r in reviewers:
        doc.add_paragraph(r, style='List Bullet')

    doc.add_paragraph('')
    doc.add_paragraph('Sincerely,')
    doc.add_paragraph('')
    p = doc.add_paragraph()
    p.add_run('[Author Name]').bold = True
    doc.add_paragraph('[Affiliation]')
    doc.add_paragraph('[Email]')

    out_path = os.path.join(BASE_DIR, 'cover_letter_a2_jbi.docx')
    doc.save(out_path)
    print(f'Saved: {out_path}')


def generate_pptx():
    """Generate editable figures pptx."""
    from pptx import Presentation
    from pptx.util import Inches as PInches, Pt as PPt

    prs = Presentation()
    prs.slide_width = PInches(13.333)
    prs.slide_height = PInches(7.5)

    FIGURES = [
        ('fig6_causal_dag.png', 'Figure 1: Estimated Causal DAG (DirectLiNGAM)',
         'Arrow weight indicates estimated causal effect size |B_ij|.'),
        ('fig5_hill_radar.png', "Figure 2: Hill's Nine Criteria Coverage",
         'ECD (purple) achieves broader coverage than any single method.'),
        ('fig4_direction_comparison.png', 'Figure 3: Three-Method Direction Comparison',
         'Green = agreement, Red = disagreement between methods.'),
        ('fig7_lingam_vs_spectral.png', 'Figure 4: LiNGAM DAG vs. Spectral Causality DCG',
         'Dashed lines indicate feedback edges absent in the DAG.'),
        ('fig9_ecd_pruning_analysis.png', 'Figure 5: ECD Ensemble & Pruning Analysis',
         'Edge-level feedback rates and bootstrap confidence intervals.'),
    ]

    for fname, title, caption in FIGURES:
        slide = prs.slides.add_slide(prs.slide_layouts[6])  # blank
        # Title
        txBox = slide.shapes.add_textbox(PInches(0.5), PInches(0.2), PInches(12.3), PInches(0.8))
        tf = txBox.text_frame
        p = tf.paragraphs[0]
        p.text = title
        p.font.size = PPt(20)
        p.font.bold = True
        p.alignment = 1  # center

        # Image
        img_path = os.path.join(FIG_DIR, fname)
        if os.path.exists(img_path):
            slide.shapes.add_picture(img_path, PInches(2.0), PInches(1.2), PInches(9.3), PInches(5.2))

        # Caption
        txBox2 = slide.shapes.add_textbox(PInches(1.0), PInches(6.6), PInches(11.3), PInches(0.7))
        tf2 = txBox2.text_frame
        p2 = tf2.paragraphs[0]
        p2.text = caption
        p2.font.size = PPt(12)
        p2.font.italic = True
        p2.alignment = 1

    out_path = os.path.join(BASE_DIR, 'figures_a2_ecd.pptx')
    prs.save(out_path)
    print(f'Saved: {out_path}')


if __name__ == '__main__':
    import sys
    if '--ja' in sys.argv:
        generate_manuscript('manuscript_a2_ecd_ja.md', 'manuscript_a2_ecd_ja.docx', lang='ja')
    else:
        generate_manuscript()
        generate_manuscript('manuscript_a2_ecd_ja.md', 'manuscript_a2_ecd_ja.docx', lang='ja')
        generate_cover_letter()
        generate_pptx()
