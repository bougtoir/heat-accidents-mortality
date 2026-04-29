"""
Generate docx files for:
  05_spectral_causality_explainer.docx (general audience)
  06_spectral_causality_academic.docx (university students)
  07_lingam_vs_spectral_comparison.docx (comparison report)

All figures are embedded inline after first mention.
"""

import re
from pathlib import Path
from docx import Document
from docx.shared import Inches, Pt, Cm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT

FIGURES_DIR = Path('/home/ubuntu/repos/wip/spectral-causality-brainstorm/figures')
OUTPUT_DIR = Path('/home/ubuntu/repos/wip/spectral-causality-brainstorm')

# Map markdown figure references to actual files
FIGURE_MAP = {
    'figures/fig1_three_approaches.png': FIGURES_DIR / 'fig1_three_approaches.png',
    'figures/fig2_magnetic_laplacian_q.png': FIGURES_DIR / 'fig2_magnetic_laplacian_q.png',
    'figures/fig3_hodge_decomposition.png': FIGURES_DIR / 'fig3_hodge_decomposition.png',
    'figures/fig4_direction_comparison.png': FIGURES_DIR / 'fig4_direction_comparison.png',
    'figures/fig5_hill_radar.png': FIGURES_DIR / 'fig5_hill_radar.png',
    'figures/fig6_causal_dag.png': FIGURES_DIR / 'fig6_causal_dag.png',
    'figures/fig7_lingam_vs_spectral.png': FIGURES_DIR / 'fig7_lingam_vs_spectral.png',
    'figures/fig8_alpha_sweep.png': FIGURES_DIR / 'fig8_alpha_sweep.png',
    'figures/fig9_ecd_pruning_analysis.png': FIGURES_DIR / 'fig9_ecd_pruning_analysis.png',
}


def set_cell_text(cell, text, bold=False, size=9):
    cell.text = ''
    p = cell.paragraphs[0]
    run = p.add_run(text)
    run.font.size = Pt(size)
    run.bold = bold
    p.alignment = WD_ALIGN_PARAGRAPH.LEFT


def add_table_from_md(doc, header_row, data_rows):
    ncols = len(header_row)
    table = doc.add_table(rows=1 + len(data_rows), cols=ncols)
    table.style = 'Table Grid'
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    for i, h in enumerate(header_row):
        set_cell_text(table.rows[0].cells[i], h.strip(), bold=True, size=9)
    for r, row_data in enumerate(data_rows):
        for c, val in enumerate(row_data):
            if c < ncols:
                set_cell_text(table.rows[r + 1].cells[c], val.strip(), size=9)
    return table


def parse_md_table(lines):
    """Parse markdown table lines into header and data rows."""
    if len(lines) < 2:
        return None, None
    header = [c.strip() for c in lines[0].strip('|').split('|')]
    # Skip separator line
    data = []
    for line in lines[2:]:
        if line.strip().startswith('|'):
            row = [c.strip() for c in line.strip('|').split('|')]
            data.append(row)
    return header, data


def md_to_docx(md_path, docx_path, title):
    """Convert markdown to docx with inline figures."""
    doc = Document()

    # Set default font
    style = doc.styles['Normal']
    font = style.font
    font.name = 'Times New Roman'
    font.size = Pt(11)

    # Title
    p = doc.add_heading(title, level=0)
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER

    with open(md_path, 'r', encoding='utf-8') as f:
        content = f.read()

    lines = content.split('\n')
    i = 0
    in_code_block = False
    code_lines = []
    table_lines = []
    in_table = False

    while i < len(lines):
        line = lines[i]

        # Code blocks
        if line.strip().startswith('```'):
            if in_code_block:
                # End code block
                code_text = '\n'.join(code_lines)
                p = doc.add_paragraph()
                p.style = doc.styles['Normal']
                run = p.add_run(code_text)
                run.font.name = 'Courier New'
                run.font.size = Pt(9)
                p.paragraph_format.left_indent = Cm(1)
                code_lines = []
                in_code_block = False
            else:
                # Flush table if any
                if in_table and table_lines:
                    header, data = parse_md_table(table_lines)
                    if header and data:
                        add_table_from_md(doc, header, data)
                        doc.add_paragraph()
                    table_lines = []
                    in_table = False
                in_code_block = True
            i += 1
            continue

        if in_code_block:
            code_lines.append(line)
            i += 1
            continue

        # Table detection
        if line.strip().startswith('|') and '|' in line.strip()[1:]:
            if not in_table:
                in_table = True
                table_lines = []
            table_lines.append(line)
            i += 1
            continue
        else:
            if in_table and table_lines:
                header, data = parse_md_table(table_lines)
                if header and data:
                    add_table_from_md(doc, header, data)
                    doc.add_paragraph()
                table_lines = []
                in_table = False

        # Skip YAML frontmatter / TOC links
        if line.strip().startswith('[') and '](#' in line:
            i += 1
            continue

        # Headings
        if line.startswith('# ') and not line.startswith('## '):
            # Skip the top-level heading (we already have the title)
            i += 1
            continue
        elif line.startswith('## '):
            doc.add_heading(line.lstrip('#').strip(), level=1)
            i += 1
            continue
        elif line.startswith('### '):
            doc.add_heading(line.lstrip('#').strip(), level=2)
            i += 1
            continue
        elif line.startswith('#### '):
            doc.add_heading(line.lstrip('#').strip(), level=3)
            i += 1
            continue

        # Figures: ![caption](path)
        fig_match = re.match(r'!\[([^\]]*)\]\(([^)]+)\)', line.strip())
        if fig_match:
            caption = fig_match.group(1)
            fig_path = fig_match.group(2)

            if fig_path in FIGURE_MAP and FIGURE_MAP[fig_path].exists():
                p = doc.add_paragraph()
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER
                run = p.add_run()
                run.add_picture(str(FIGURE_MAP[fig_path]), width=Inches(5.5))

            i += 1
            continue

        # Figure caption (italic line starting with *)
        if line.strip().startswith('*') and line.strip().endswith('*'):
            caption_text = line.strip().strip('*')
            p = doc.add_paragraph()
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            run = p.add_run(caption_text)
            run.italic = True
            run.font.size = Pt(9)
            p.paragraph_format.space_before = Pt(6)
            p.paragraph_format.space_after = Pt(12)
            i += 1
            continue

        # Horizontal rule
        if line.strip() == '---':
            i += 1
            continue

        # Blockquote
        if line.strip().startswith('>'):
            text = line.strip().lstrip('>').strip()
            p = doc.add_paragraph()
            p.paragraph_format.left_indent = Cm(1.5)
            # Handle bold within blockquote
            parts = re.split(r'(\*\*[^*]+\*\*)', text)
            for part in parts:
                if part.startswith('**') and part.endswith('**'):
                    run = p.add_run(part.strip('*'))
                    run.bold = True
                else:
                    p.add_run(part)
            i += 1
            continue

        # Bullet points
        if line.strip().startswith('- ') or line.strip().startswith('* '):
            text = line.strip().lstrip('-*').strip()
            p = doc.add_paragraph(style='List Bullet')
            # Handle bold/italic in text
            add_formatted_text(p, text)
            i += 1
            continue

        # Numbered list
        num_match = re.match(r'^(\d+)\.\s+(.+)', line.strip())
        if num_match:
            text = num_match.group(2)
            p = doc.add_paragraph(style='List Number')
            add_formatted_text(p, text)
            i += 1
            continue

        # Regular paragraph
        if line.strip():
            p = doc.add_paragraph()
            add_formatted_text(p, line.strip())

        i += 1

    # Flush remaining table
    if in_table and table_lines:
        header, data = parse_md_table(table_lines)
        if header and data:
            add_table_from_md(doc, header, data)

    doc.save(str(docx_path))
    print(f"Saved: {docx_path}")


def add_formatted_text(paragraph, text):
    """Add text with markdown bold/italic formatting to a paragraph."""
    # Split on bold (**text**) and italic (*text*) markers
    parts = re.split(r'(\*\*[^*]+\*\*|\*[^*]+\*)', text)
    for part in parts:
        if part.startswith('**') and part.endswith('**'):
            run = paragraph.add_run(part.strip('*'))
            run.bold = True
        elif part.startswith('*') and part.endswith('*') and len(part) > 2:
            run = paragraph.add_run(part.strip('*'))
            run.italic = True
        elif part:
            # Handle inline code `text`
            code_parts = re.split(r'(`[^`]+`)', part)
            for cp in code_parts:
                if cp.startswith('`') and cp.endswith('`'):
                    run = paragraph.add_run(cp.strip('`'))
                    run.font.name = 'Courier New'
                    run.font.size = Pt(9)
                else:
                    # Handle superscript refs {1-3}
                    ref_parts = re.split(r'(\{[^}]+\})', cp)
                    for rp in ref_parts:
                        if rp.startswith('{') and rp.endswith('}'):
                            run = paragraph.add_run(rp.strip('{}'))
                            run.font.superscript = True
                        else:
                            paragraph.add_run(rp)


if __name__ == '__main__':
    # Generate 05 (general audience explainer)
    md_to_docx(
        OUTPUT_DIR / '05_spectral_causality_explainer.md',
        OUTPUT_DIR / '05_spectral_causality_explainer.docx',
        'スペクトル因果性 — 「音の科学」で因果関係を見つける'
    )

    # Generate 06 (academic)
    md_to_docx(
        OUTPUT_DIR / '06_spectral_causality_academic.md',
        OUTPUT_DIR / '06_spectral_causality_academic.docx',
        'スペクトル因果性の数理的基礎\n— 有向グラフのスペクトル理論に基づく因果推論の新しいアプローチ —'
    )

    # Generate 07 (comparison report)
    md_to_docx(
        OUTPUT_DIR / '07_lingam_vs_spectral_comparison.md',
        OUTPUT_DIR / '07_lingam_vs_spectral_comparison.docx',
        'LiNGAM vs スペクトル因果性：UCI心疾患データによる構造比較'
    )
