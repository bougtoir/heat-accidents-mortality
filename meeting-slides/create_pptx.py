#!/usr/bin/env python3
"""入職後初面談スライド (10枚) を PowerPoint (.pptx) で生成するスクリプト"""

from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE
import os

# ===== Color palette =====
PRIMARY = RGBColor(0x1A, 0x36, 0x5D)
ACCENT = RGBColor(0x2B, 0x6C, 0xB0)
ACCENT_LIGHT = RGBColor(0xBE, 0xE3, 0xF8)
BG = RGBColor(0xF7, 0xFA, 0xFC)
TEXT_COLOR = RGBColor(0x1A, 0x20, 0x2C)
TEXT_LIGHT = RGBColor(0x4A, 0x55, 0x68)
GOLD = RGBColor(0xB7, 0x79, 0x1F)
GOLD_LIGHT = RGBColor(0xFE, 0xFC, 0xBF)
GREEN = RGBColor(0x27, 0x67, 0x49)
GREEN_LIGHT = RGBColor(0xC6, 0xF6, 0xD5)
RED = RGBColor(0x9B, 0x2C, 0x2C)
RED_LIGHT = RGBColor(0xFE, 0xD7, 0xD7)
WHITE = RGBColor(0xFF, 0xFF, 0xFF)
DARK_BG = RGBColor(0x1A, 0x36, 0x5D)
DARK_BG2 = RGBColor(0x2A, 0x4A, 0x7F)

prs = Presentation()
prs.slide_width = Inches(13.333)
prs.slide_height = Inches(7.5)

SLIDE_W = prs.slide_width
SLIDE_H = prs.slide_height


def add_bg(slide, color):
    """Set slide background color."""
    background = slide.background
    fill = background.fill
    fill.solid()
    fill.fore_color.rgb = color


def add_text_box(slide, left, top, width, height, text, font_size=18,
                 color=TEXT_COLOR, bold=False, alignment=PP_ALIGN.LEFT,
                 font_name="Yu Gothic"):
    """Add a simple text box."""
    txBox = slide.shapes.add_textbox(left, top, width, height)
    tf = txBox.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = text
    p.font.size = Pt(font_size)
    p.font.color.rgb = color
    p.font.bold = bold
    p.font.name = font_name
    p.alignment = alignment
    return txBox


def add_rich_text_box(slide, left, top, width, height):
    """Add a text box and return the text frame for manual paragraph building."""
    txBox = slide.shapes.add_textbox(left, top, width, height)
    tf = txBox.text_frame
    tf.word_wrap = True
    return tf


def add_bullet(tf, text, font_size=18, color=TEXT_COLOR, bold=False, level=0,
               sub_text=None):
    """Add a bullet point to a text frame."""
    p = tf.add_paragraph()
    p.level = level
    p.space_before = Pt(6)
    p.space_after = Pt(4)
    run = p.add_run()
    run.text = text
    run.font.size = Pt(font_size)
    run.font.color.rgb = color
    run.font.bold = bold
    run.font.name = "Yu Gothic"
    if sub_text:
        p2 = tf.add_paragraph()
        p2.level = level + 1
        p2.space_before = Pt(2)
        run2 = p2.add_run()
        run2.text = sub_text
        run2.font.size = Pt(14)
        run2.font.color.rgb = TEXT_LIGHT
        run2.font.name = "Yu Gothic"


def add_rounded_rect(slide, left, top, width, height, fill_color, border_color=None):
    """Add a rounded rectangle."""
    shape = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
    shape.fill.solid()
    shape.fill.fore_color.rgb = fill_color
    if border_color:
        shape.line.color.rgb = border_color
        shape.line.width = Pt(2)
    else:
        shape.line.fill.background()
    return shape


def add_heading(slide, text, left=None, top=None):
    """Add a slide heading with underline."""
    if left is None:
        left = Inches(0.8)
    if top is None:
        top = Inches(0.4)
    add_text_box(slide, left, top, Inches(11), Inches(0.7),
                 text, font_size=36, color=PRIMARY, bold=True)
    # Underline
    line = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, left, top + Inches(0.7),
                                  Inches(11.5), Pt(3))
    line.fill.solid()
    line.fill.fore_color.rgb = ACCENT
    line.line.fill.background()


def add_flow_box(slide, left, top, title, subtitle, border_color=ACCENT):
    """Add a flow diagram box."""
    w, h = Inches(2.8), Inches(1.2)
    box = add_rounded_rect(slide, left, top, w, h, WHITE, border_color)
    # Title
    add_text_box(slide, left + Inches(0.1), top + Inches(0.15),
                 w - Inches(0.2), Inches(0.5),
                 title, font_size=16, color=PRIMARY, bold=True,
                 alignment=PP_ALIGN.CENTER)
    # Subtitle
    add_text_box(slide, left + Inches(0.1), top + Inches(0.6),
                 w - Inches(0.2), Inches(0.4),
                 subtitle, font_size=12, color=TEXT_LIGHT,
                 alignment=PP_ALIGN.CENTER)


def add_flow_arrow(slide, left, top):
    """Add a flow arrow."""
    add_text_box(slide, left, top, Inches(0.6), Inches(1.2),
                 "→", font_size=28, color=ACCENT, alignment=PP_ALIGN.CENTER)


def add_highlight_box(slide, left, top, width, label, text, label_color=ACCENT,
                      bg_color=RGBColor(0xEB, 0xF8, 0xFF),
                      border_color=ACCENT, emp_parts=None):
    """Add a highlight box with label and text."""
    h = Inches(1.2)
    # Background rect
    box = add_rounded_rect(slide, left, top, width, h, bg_color)
    # Left border accent
    border = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE,
                                    left, top, Pt(5), h)
    border.fill.solid()
    border.fill.fore_color.rgb = border_color
    border.line.fill.background()
    # Label
    add_text_box(slide, left + Inches(0.3), top + Inches(0.1),
                 width - Inches(0.4), Inches(0.3),
                 label, font_size=11, color=label_color, bold=True)
    # Text
    tf = add_rich_text_box(slide, left + Inches(0.3), top + Inches(0.4),
                           width - Inches(0.4), Inches(0.7))
    tf.paragraphs[0].clear()
    if emp_parts:
        for part_text, is_emp in emp_parts:
            run = tf.paragraphs[0].add_run()
            run.text = part_text
            run.font.size = Pt(17)
            run.font.name = "Yu Gothic"
            if is_emp:
                run.font.color.rgb = ACCENT
                run.font.bold = True
            else:
                run.font.color.rgb = TEXT_COLOR
    else:
        run = tf.paragraphs[0].add_run()
        run.text = text
        run.font.size = Pt(17)
        run.font.color.rgb = TEXT_COLOR
        run.font.name = "Yu Gothic"


def add_tag(slide, left, top, text, color=ACCENT):
    """Add a tag/badge."""
    w = Inches(0.2 + len(text) * 0.18)
    tag = add_rounded_rect(slide, left, top, w, Inches(0.35), color)
    add_text_box(slide, left, top + Inches(0.02), w, Inches(0.3),
                 text, font_size=11, color=WHITE, bold=True,
                 alignment=PP_ALIGN.CENTER)
    return w


def add_page_number(slide, num, total):
    """Add page number to bottom-left."""
    add_text_box(slide, Inches(0.5), Inches(6.9), Inches(1), Inches(0.4),
                 f"{num} / {total}", font_size=11, color=TEXT_LIGHT)


# ===========================================================
# Slide 1: Title
# ===========================================================
slide1 = prs.slides.add_slide(prs.slide_layouts[6])  # blank
add_bg(slide1, DARK_BG)

add_text_box(slide1, Inches(1), Inches(2.2), Inches(11.3), Inches(1.2),
             "入職後初面談", font_size=54, color=WHITE, bold=True,
             alignment=PP_ALIGN.CENTER)

# Divider line
div = slide1.shapes.add_shape(MSO_SHAPE.RECTANGLE,
                               Inches(5.5), Inches(3.5), Inches(2.3), Pt(2))
div.fill.solid()
div.fill.fore_color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
div.line.fill.background()

add_text_box(slide1, Inches(1), Inches(3.8), Inches(11.3), Inches(0.6),
             "研究・産学連携ビジョンのご共有", font_size=22, color=RGBColor(0xCC, 0xCC, 0xCC),
             alignment=PP_ALIGN.CENTER)

add_text_box(slide1, Inches(1), Inches(5.0), Inches(11.3), Inches(0.5),
             "2026年5月15日", font_size=16, color=RGBColor(0x99, 0x99, 0x99),
             alignment=PP_ALIGN.CENTER)

add_page_number(slide1, 1, 10)

# ===========================================================
# Slide 2: Agenda
# ===========================================================
slide2 = prs.slides.add_slide(prs.slide_layouts[6])
add_bg(slide2, BG)
add_heading(slide2, "本日のアジェンダ")

agenda_items = [
    "自己紹介 — コーディング能力・コードレビュー実績",
    "生成AI時代の研究支援 — Devin × 伊藤忠 × 滋賀大学",
    "研究者としての目標",
    "麻酔科の診療科特異性",
    "大学発ベンチャー・法人補助金還流モデル",
    "産学連携 — シフト最適化・学術支援の展開",
]

tf2 = add_rich_text_box(slide2, Inches(1.2), Inches(1.6), Inches(10), Inches(5))
tf2.paragraphs[0].clear()
for item in agenda_items:
    add_bullet(tf2, f"◆  {item}", font_size=22, color=TEXT_COLOR)

add_page_number(slide2, 2, 10)

# ===========================================================
# Slide 3: Code Ability
# ===========================================================
slide3 = prs.slides.add_slide(prs.slide_layouts[6])
add_bg(slide3, BG)
add_heading(slide3, "コーディング能力の証明")

add_highlight_box(slide3, Inches(0.8), Inches(1.8), Inches(11.5),
                  "課題認識", "生成AI時代においてはコード能力の客観的評価が困難に")

add_highlight_box(slide3, Inches(0.8), Inches(3.3), Inches(11.5),
                  "強み", "",
                  label_color=GREEN,
                  bg_color=GREEN_LIGHT,
                  border_color=GREEN,
                  emp_parts=[
                      ("生成AI登場以前", True),
                      ("のプログラミングコンペティションにおける受賞歴あり\n→ コーディング能力、および", False),
                      ("コードレビュー能力", True),
                      ("の客観的裏付け", False),
                  ])

# Tags
x = Inches(0.8)
y = Inches(4.9)
tags = [("数値最適化", ACCENT), ("統計モデリング", ACCENT),
        ("コードレビュー", ACCENT), ("AI前受賞実績", GREEN)]
for text, color in tags:
    w = add_tag(slide3, x, y, text, color)
    x += w + Inches(0.15)

add_page_number(slide3, 3, 10)

# ===========================================================
# Slide 4: Devin × Itochu × Shiga
# ===========================================================
slide4 = prs.slides.add_slide(prs.slide_layouts[6])
add_bg(slide4, BG)
add_heading(slide4, "Devin × 伊藤忠 × 滋賀大学")

flow_y = Inches(2.2)
add_flow_box(slide4, Inches(1.5), flow_y, "Cognition AI", "Devin 開発元", ACCENT)
add_flow_arrow(slide4, Inches(4.3), flow_y)
add_flow_box(slide4, Inches(5.0), flow_y, "伊藤忠テクノソリューションズ", "日本代理店", GOLD)
add_flow_arrow(slide4, Inches(7.8), flow_y)
add_flow_box(slide4, Inches(8.5), flow_y, "滋賀大学", "伊藤忠と縁あり", GREEN)

add_highlight_box(slide4, Inches(0.8), Inches(3.8), Inches(11.5),
                  "提案", "",
                  label_color=GOLD, bg_color=GOLD_LIGHT, border_color=GOLD,
                  emp_parts=[
                      ("伊藤忠が日本におけるDevin代理店となった今、\n", False),
                      ("滋賀大学でのDevin導入", True),
                      ("を検討できないか？", False),
                  ])

tf4 = add_rich_text_box(slide4, Inches(1.2), Inches(5.3), Inches(10), Inches(1.5))
tf4.paragraphs[0].clear()
add_bullet(tf4, "AI駆動型ソフトウェアエンジニアリングによる研究加速",
           sub_text="コーディング、データ分析、論文整備の自動化")
add_bullet(tf4, "大学全体のDX推進の先行事例になり得る")

add_page_number(slide4, 4, 10)

# ===========================================================
# Slide 5: Research Goal
# ===========================================================
slide5 = prs.slides.add_slide(prs.slide_layouts[6])
add_bg(slide5, BG)
add_heading(slide5, "研究者としての目標")

add_text_box(slide5, Inches(1), Inches(2.5), Inches(11.3), Inches(1),
             "蝋人形になること", font_size=42, color=PRIMARY, bold=True,
             alignment=PP_ALIGN.CENTER)

add_highlight_box(slide5, Inches(3), Inches(3.8), Inches(7.3),
                  "", "",
                  emp_parts=[
                      ("後世に残る研究業績を確立し、\nその分野で", False),
                      ("不朽の存在", True),
                      ("として認知される", False),
                  ])

tf5 = add_rich_text_box(slide5, Inches(3), Inches(5.3), Inches(7.3), Inches(1.5))
tf5.paragraphs[0].clear()
add_bullet(tf5, "特定の研究領域で圧倒的な成果を積み上げる")
add_bullet(tf5, "独自のアプローチで分野に永続的な貢献を残す")

add_page_number(slide5, 5, 10)

# ===========================================================
# Slide 6: Anesthesiology Specificity
# ===========================================================
slide6 = prs.slides.add_slide(prs.slide_layouts[6])
add_bg(slide6, BG)
add_heading(slide6, "麻酔科の診療科特異性")

# Left column
box_l = add_rounded_rect(slide6, Inches(0.8), Inches(1.6), Inches(5.6), Inches(4.2),
                         WHITE, RGBColor(0xE2, 0xE8, 0xF0))
add_text_box(slide6, Inches(1.1), Inches(1.8), Inches(5), Inches(0.5),
             "臨床面の特徴", font_size=22, color=PRIMARY, bold=True)
tf6l = add_rich_text_box(slide6, Inches(1.1), Inches(2.5), Inches(5), Inches(3))
tf6l.paragraphs[0].clear()
for item in ["リアルタイムデータが豊富（生体モニター）",
             "薬物動態（PK/PD）モデリングとの親和性",
             "手術スケジュール管理の複雑さ",
             "周術期管理のプロトコル標準化"]:
    add_bullet(tf6l, f"▸ {item}", font_size=16)

# Right column
box_r = add_rounded_rect(slide6, Inches(6.8), Inches(1.6), Inches(5.6), Inches(4.2),
                         WHITE, RGBColor(0xE2, 0xE8, 0xF0))
add_text_box(slide6, Inches(7.1), Inches(1.8), Inches(5), Inches(0.5),
             "研究面の特徴", font_size=22, color=PRIMARY, bold=True)
tf6r = add_rich_text_box(slide6, Inches(7.1), Inches(2.5), Inches(5), Inches(3))
tf6r.paragraphs[0].clear()
for item in ["数理モデル・シミュレーションの需要大",
             "多変量時系列データの宝庫",
             "シフト制勤務 → 最適化問題と直結",
             "他科連携が多く横断的研究が可能"]:
    add_bullet(tf6r, f"▸ {item}", font_size=16)

# Bottom highlight
add_highlight_box(slide6, Inches(0.8), Inches(6.0), Inches(11.5),
                  "", "",
                  emp_parts=[
                      ("データサイエンス × 麻酔科学", True),
                      (" の交差点に大きなポテンシャル", False),
                  ])

add_page_number(slide6, 6, 10)

# ===========================================================
# Slide 7: Venture / Subsidy Model
# ===========================================================
slide7 = prs.slides.add_slide(prs.slide_layouts[6])
add_bg(slide7, BG)
add_heading(slide7, "法人補助金の大学還流モデル")

flow_y7 = Inches(2.0)
add_flow_box(slide7, Inches(1.5), flow_y7, "大学発ベンチャー", "技術・知見の事業化", GREEN)
add_flow_arrow(slide7, Inches(4.3), flow_y7)
add_flow_box(slide7, Inches(5.0), flow_y7, "法人補助金取得", "公的資金の獲得", GOLD)
add_flow_arrow(slide7, Inches(7.8), flow_y7)
add_flow_box(slide7, Inches(8.5), flow_y7, "大学への還流", "研究基盤の強化", ACCENT)

add_highlight_box(slide7, Inches(0.8), Inches(3.6), Inches(11.5),
                  "ビジョン", "",
                  label_color=GOLD, bg_color=GOLD_LIGHT, border_color=GOLD,
                  emp_parts=[
                      ("大学発ベンチャーが獲得した法人補助金を\n", False),
                      ("大学の研究基盤に還流させるサステナブルなモデル", True),
                      ("を構築", False),
                  ])

tf7 = add_rich_text_box(slide7, Inches(1.2), Inches(5.2), Inches(10), Inches(1.5))
tf7.paragraphs[0].clear()
add_bullet(tf7, "産学連携の成果を大学運営に直接貢献させる仕組み")
add_bullet(tf7, "ベンチャー → 補助金 → 大学 の好循環サイクル")

add_page_number(slide7, 7, 10)

# ===========================================================
# Slide 8: Industry-Academia Collaboration
# ===========================================================
slide8 = prs.slides.add_slide(prs.slide_layouts[6])
add_bg(slide8, BG)
add_heading(slide8, "産学連携の展開")

# Left column - Shift optimization
box8l = add_rounded_rect(slide8, Inches(0.8), Inches(1.6), Inches(5.6), Inches(4.5),
                         WHITE, RGBColor(0xE2, 0xE8, 0xF0))
# Left accent border
border8l = slide8.shapes.add_shape(MSO_SHAPE.RECTANGLE,
                                    Inches(0.8), Inches(1.6), Pt(5), Inches(4.5))
border8l.fill.solid()
border8l.fill.fore_color.rgb = ACCENT
border8l.line.fill.background()

add_text_box(slide8, Inches(1.1), Inches(1.8), Inches(5), Inches(0.5),
             "シフト作成の最適化", font_size=22, color=PRIMARY, bold=True)
tf8l = add_rich_text_box(slide8, Inches(1.1), Inches(2.5), Inches(5), Inches(2.5))
tf8l.paragraphs[0].clear()
for item in ["アプローチ：数値最適化",
             "実績：導入実績あり",
             "制約充足（公平性・連続勤務制限）",
             "医療機関特有の複雑な制約に対応",
             "コスト削減と職員満足度の両立"]:
    add_bullet(tf8l, f"▸ {item}", font_size=15)

x8l = Inches(1.1)
for text, color in [("最適化", ACCENT), ("OR", ACCENT), ("導入済", ACCENT)]:
    w = add_tag(slide8, x8l, Inches(5.2), text, color)
    x8l += w + Inches(0.1)

# Right column - Academic support
box8r = add_rounded_rect(slide8, Inches(6.8), Inches(1.6), Inches(5.6), Inches(4.5),
                         WHITE, RGBColor(0xE2, 0xE8, 0xF0))
border8r = slide8.shapes.add_shape(MSO_SHAPE.RECTANGLE,
                                    Inches(6.8), Inches(1.6), Pt(5), Inches(4.5))
border8r.fill.solid()
border8r.fill.fore_color.rgb = GREEN
border8r.line.fill.background()

add_text_box(slide8, Inches(7.1), Inches(1.8), Inches(5), Inches(0.5),
             "学術支援", font_size=22, color=PRIMARY, bold=True)
tf8r = add_rich_text_box(slide8, Inches(7.1), Inches(2.5), Inches(5), Inches(2.5))
tf8r.paragraphs[0].clear()
for item in ["実績：導入実績あり",
             "論文執筆・データ解析支援",
             "統計コンサルティング",
             "研究デザインのアドバイス",
             "再現可能な研究環境構築"]:
    add_bullet(tf8r, f"▸ {item}", font_size=15)

x8r = Inches(7.1)
for text, color in [("統計", GREEN), ("論文支援", GREEN), ("導入済", GREEN)]:
    w = add_tag(slide8, x8r, Inches(5.2), text, color)
    x8r += w + Inches(0.1)

# Bottom highlight
add_highlight_box(slide8, Inches(0.8), Inches(6.3), Inches(11.5),
                  "目標", "",
                  label_color=GREEN, bg_color=GREEN_LIGHT, border_color=GREEN,
                  emp_parts=[
                      ("両分野の", False),
                      ("導入実績", True),
                      ("を基盤に、学内外への展開を推進", False),
                  ])

add_page_number(slide8, 8, 10)

# ===========================================================
# Slide 9: Research Policy
# ===========================================================
slide9 = prs.slides.add_slide(prs.slide_layouts[6])
add_bg(slide9, BG)
add_heading(slide9, "研究上の方針")

add_highlight_box(slide9, Inches(0.8), Inches(2.0), Inches(11.5),
                  "留意事項", "",
                  label_color=RED, bg_color=RED_LIGHT, border_color=RED,
                  emp_parts=[
                      ("特定の研究者（佐藤俊哉氏）との共同研究は", False),
                      ("行わない", True),
                      ("方針", False),
                  ])

tf9 = add_rich_text_box(slide9, Inches(1.2), Inches(3.8), Inches(10), Inches(3))
tf9.paragraphs[0].clear()
add_bullet(tf9, "独自の研究ラインを確立・維持する", font_size=20,
           sub_text="研究の独立性と方向性を自ら決定")
add_bullet(tf9, "共同研究は研究ビジョンが合致する相手と進める", font_size=20,
           sub_text="相互補完的で建設的なパートナーシップを重視")

add_page_number(slide9, 9, 10)

# ===========================================================
# Slide 10: Summary
# ===========================================================
slide10 = prs.slides.add_slide(prs.slide_layouts[6])
add_bg(slide10, DARK_BG)

add_text_box(slide10, Inches(1), Inches(1.2), Inches(11.3), Inches(1),
             "まとめ", font_size=44, color=WHITE, bold=True,
             alignment=PP_ALIGN.CENTER)

# Divider
div10 = slide10.shapes.add_shape(MSO_SHAPE.RECTANGLE,
                                  Inches(5.5), Inches(2.3), Inches(2.3), Pt(2))
div10.fill.solid()
div10.fill.fore_color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
div10.line.fill.background()

summary_items = [
    "AI前の実績に基づくコード能力の裏付け",
    "Devin導入による大学DXの可能性",
    "麻酔科 × データサイエンスの融合",
    "法人補助金の大学還流モデル",
    "シフト最適化・学術支援の実績を展開",
]

tf10 = add_rich_text_box(slide10, Inches(3), Inches(2.8), Inches(7.3), Inches(3.5))
tf10.paragraphs[0].clear()
for item in summary_items:
    add_bullet(tf10, f"◆  {item}", font_size=20, color=RGBColor(0xDD, 0xDD, 0xDD))

add_text_box(slide10, Inches(1), Inches(6.2), Inches(11.3), Inches(0.6),
             "ご清聴ありがとうございました", font_size=18,
             color=RGBColor(0x99, 0x99, 0x99), alignment=PP_ALIGN.CENTER)

add_page_number(slide10, 10, 10)

# ===========================================================
# Save
# ===========================================================
output_path = os.path.join(os.path.dirname(__file__), "meeting_slides.pptx")
prs.save(output_path)
print(f"Saved: {output_path}")
