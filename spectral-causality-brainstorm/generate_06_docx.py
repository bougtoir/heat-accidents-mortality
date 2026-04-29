"""
Generate docx for 06_spectral_causality_academic.md
Uses python-docx with OML (Office Math Markup Language) for equations.
"""

import os
import re
import lxml.etree as ET
from docx import Document
from docx.shared import Inches, Pt, Cm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn, nsmap

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# ============================================================
# Math XML helper: wrap LaTeX-like text as Word equation via OMML
# ============================================================

def add_math_paragraph(doc, math_text, alignment=WD_ALIGN_PARAGRAPH.CENTER):
    """Add a paragraph containing math as styled monospace text.
    For proper OMML we'd need a full LaTeX-to-OMML converter;
    here we use a clean monospace rendering that preserves readability."""
    p = doc.add_paragraph()
    p.alignment = alignment
    p.paragraph_format.space_before = Pt(6)
    p.paragraph_format.space_after = Pt(6)
    run = p.add_run(math_text)
    run.font.name = 'Cambria Math'
    run.font.size = Pt(11)
    run.italic = True
    return p


def add_display_equation(doc, equation_text, label=None):
    """Add a display equation (centered, with optional label)."""
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(8)
    p.paragraph_format.space_after = Pt(8)
    run = p.add_run(equation_text)
    run.font.name = 'Cambria Math'
    run.font.size = Pt(11)
    run.italic = True
    if label:
        tab_run = p.add_run(f'    ({label})')
        tab_run.font.size = Pt(10)
    return p


def generate_docx():
    doc = Document()

    # -- Styles --
    style = doc.styles['Normal']
    style.font.name = 'Times New Roman'
    style.font.size = Pt(11)
    style.paragraph_format.space_after = Pt(4)
    style.paragraph_format.line_spacing = 1.15

    # ============================================================
    # Title
    # ============================================================
    title_p = doc.add_paragraph()
    title_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    title_run = title_p.add_run('スペクトル因果性の数理的基礎')
    title_run.bold = True
    title_run.font.size = Pt(18)

    sub_p = doc.add_paragraph()
    sub_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    sub_run = sub_p.add_run(
        '— 有向グラフのスペクトル理論に基づく因果推論の新しいアプローチ —'
    )
    sub_run.font.size = Pt(12)
    sub_run.font.color.rgb = RGBColor(80, 80, 80)

    reader_p = doc.add_paragraph()
    reader_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = reader_p.add_run(
        '想定読者: 線形代数（固有値分解）と基礎的な確率論を既習の学部上級生〜大学院生'
    )
    r.italic = True
    r.font.size = Pt(10)
    r.font.color.rgb = RGBColor(100, 100, 100)

    # ============================================================
    # 1. 導入
    # ============================================================
    doc.add_heading('1. 導入', level=1)

    doc.add_heading('1.1 問題設定', level=2)
    doc.add_paragraph(
        '因果推論（causal inference）の中心的な問い — 「X は Y の原因か？」— に対して、'
        '様々なアプローチが提案されてきた。代表的なものとして：'
    )
    items = [
        '構造方程式モデル（SEM）と do-calculus (Pearl, 2009): 介入に基づく反事実的定義',
        '潜在結果モデル (Rubin, 1974): 処置群と対照群の潜在結果の差',
        'LiNGAM (Shimizu et al., 2006): データの非ガウス性を利用した因果方向の同定',
        'Granger因果 (Granger, 1969): 時系列における予測改善に基づく因果性',
    ]
    for item in items:
        doc.add_paragraph(item, style='List Bullet')

    doc.add_paragraph(
        '本稿では、これらとは異なる原理 — グラフのスペクトル構造（固有値・固有ベクトル）から'
        '因果的方向性を読み取る — に基づく手法を定式化する。この手法をスペクトル因果性'
        '（spectral causality）と呼ぶ。'
    )

    doc.add_heading('1.2 基本的着想', level=2)
    doc.add_paragraph(
        'n 個の変数 {X\u2081, ..., X\u2099} の間に因果関係があるとする。'
        'これらの関係を有向グラフ G = (V, E) で表現したとき、グラフのラプラシアン行列のスペクトル'
        '（固有値と固有ベクトル）には、因果的方向性に関する情報が含まれうる。'
    )
    doc.add_paragraph(
        '特に、磁気ラプラシアン（magnetic Laplacian）と呼ばれるエルミート行列を用いると、'
        'エッジの方向性が固有ベクトルの複素位相（complex phase）として符号化され、'
        '因果方向の推定が可能になる。'
    )

    doc.add_heading('1.3 本稿の構成', level=2)
    doc.add_paragraph(
        '§2でグラフラプラシアンの基礎を復習し、§3で磁気ラプラシアンを導入する。'
        '§4でスペクトル因果性を厳密に定式化し（§4.1.1 でデータ駆動の非対称統計量DPIを導入する）、'
        '§5でHodge分解との関係を示す。'
        '§6で既存手法（LiNGAM、Granger因果）との比較を行い、§7で実データ（UCI心疾患データ）'
        'への適用例を示す。§8で理論的課題を議論する。'
    )

    doc.add_paragraph('本手法の主要な貢献は以下の5点に集約される：')
    contributions = [
        'DPI（非対称統計量）の導入: α = 0（ドメイン知識なし）でも有向辺を検出し因果方向を推定可能'
        '（UCI心疾患データで9本の有向辺, 67% LiNGAM方向一致）',
        'DAG仮定不要: Hodge分解によりDAG成分（勾配）とフィードバック成分（カール）を自然に分離',
        'ドメイン知識による精度向上: r_gradient: 0.581（α = 0）→ 0.859（α = 0.6）と滑らかに改善',
        'LiNGAM連携: ドメイン知識がない場合、LiNGAMの推定DAGから高確信辺を C に設定可能',
        'ECDアンサンブル: Hill の9基準の網羅性向上（H6/H7/H9をカバー）',
    ]
    for c in contributions:
        doc.add_paragraph(c, style='List Number')

    # ============================================================
    # 2. 準備
    # ============================================================
    doc.add_heading('2. 準備：グラフラプラシアンの基礎', level=1)

    doc.add_heading('2.1 無向グラフのラプラシアン', level=2)

    p = doc.add_paragraph()
    run = p.add_run('定義 2.1')
    run.bold = True
    p.add_run(
        '（グラフラプラシアン）重み付き無向グラフ G = (V, E, w)（|V| = n, w: E → ℝ₊）に対して、'
        '重み付き隣接行列 W ∈ ℝⁿˣⁿ, 次数行列 D = diag(d₁, ..., dₙ)（dᵢ = Σⱼ Wᵢⱼ）を用いて、以下を定義する：'
    )

    add_display_equation(doc, 'L = D − W    （非正規化ラプラシアン）')
    add_display_equation(doc, '\u2112 = I − D⁻¹ᐟ² W D⁻¹ᐟ²    （正規化ラプラシアン）')

    p = doc.add_paragraph()
    run = p.add_run('命題 2.1')
    run.bold = True
    p.add_run('（基本性質）L および \u2112 について以下が成り立つ：')

    props = [
        '(i) L は対称半正定値行列であり、固有値は 0 = λ₁ ≤ λ₂ ≤ ... ≤ λₙ を満たす。',
        '(ii) λ₁ = 0 に対応する固有ベクトルは 1 = (1, ..., 1)ᵀ（定数ベクトル）。',
        '(iii) λ₂ > 0 であることは、G が連結であることと同値（Fiedler値）。',
        '(iv) 任意のベクトル f ∈ ℝⁿ に対して、fᵀLf = Σ₍ᵢ,ⱼ₎∈E wᵢⱼ(fᵢ − fⱼ)² ≥ 0。',
    ]
    for prop in props:
        doc.add_paragraph(prop, style='List Bullet')

    p = doc.add_paragraph()
    run = p.add_run('証明のスケッチ')
    run.italic = True
    p.add_run(
        '：(iv) は L の二次形式を展開すれば直接示せる。(i) は (iv) から従う。'
        '(ii) は L1 = 0 の直接計算による。(iii) は代数的連結度の定理。 □'
    )

    doc.add_paragraph(
        '性質 (iv) は重要である：fᵀLf が小さいほど、f は隣接ノードで類似した値をとる — '
        'つまり、ラプラシアンの低固有値固有ベクトルはグラフ上で滑らかな信号を表す。'
    )

    doc.add_heading('2.2 スペクトル分解の幾何学的意味', level=2)
    doc.add_paragraph(
        '\u2112 のスペクトル分解 \u2112 = UΛUᵀ（U = [u₁, ..., uₙ], Λ = diag(λ₁, ..., λₙ)）において：'
    )
    items = [
        'uₖ の各成分 uₖ(i) = ノード i が第 k 固有モードにどれだけ「荷重（load）」するかを表す',
        'λₖ = 第 k モードの「周波数」（大きいほど高周波 = 局所変動）',
        'u₂（第2固有ベクトル, Fiedler vector）はグラフの最適2分割を与える',
    ]
    for item in items:
        doc.add_paragraph(item, style='List Bullet')

    doc.add_paragraph(
        'この枠組みは、信号処理におけるフーリエ変換のグラフ上への一般化'
        '（Graph Signal Processing; GSP）の基礎となっている (Shuman et al., 2013)。'
    )

    doc.add_heading('2.3 問題：無向ラプラシアンは方向性を失う', level=2)
    doc.add_paragraph(
        'L = D − W は対称行列であるため、エッジの方向性 i → j と j → i を区別できない。'
        '因果推論では「X が Y の原因」という方向性が本質的であり、無向ラプラシアンでは情報が不足する。'
    )
    doc.add_paragraph(
        '有向グラフのラプラシアン Ld = Dout − W を直接用いる手もあるが、Ld は一般に非対称であり、'
        '固有値が複素数になりうる。これは理論的に扱いにくい。'
    )

    # ============================================================
    # 3. 磁気ラプラシアン
    # ============================================================
    doc.add_heading('3. 磁気ラプラシアン：方向性の複素位相符号化', level=1)

    doc.add_heading('3.1 物理的背景', level=2)
    doc.add_paragraph(
        '磁気ラプラシアンの名前は量子力学に由来する。磁場 B 中の荷電粒子のハミルトニアンは '
        'H = (p − eA)²/2m（A はベクトルポテンシャル）であり、粒子が閉じた経路を一周すると '
        'Aharonov-Bohm 位相 exp(i∮A·dr) を獲得する。この位相の向き依存性が、'
        'グラフ上のエッジ方向性の符号化に利用できる。'
    )

    doc.add_heading('3.2 定義', level=2)

    p = doc.add_paragraph()
    run = p.add_run('定義 3.1')
    run.bold = True
    p.add_run(
        '（磁気ラプラシアン; de Resende & da Costa, 2020; Zhang et al., 2021）'
        '重み付き有向グラフ G = (V, E, w) と電荷パラメータ q ∈ [0, 0.5] に対して、'
        'エルミート隣接行列 H⁽ᑫ⁾ ∈ ℂⁿˣⁿ を以下で定義する：'
    )

    add_display_equation(doc, 'H⁽ᑫ⁾ᵢⱼ = wᵢⱼ · exp(i · 2πq · σᵢⱼ)')

    doc.add_paragraph(
        'ここで σᵢⱼ ∈ {−1, 0, +1} はエッジの方向性符号であり：'
    )
    items = [
        'σᵢⱼ = +1  if i → j',
        'σᵢⱼ = −1  if j → i',
        'σᵢⱼ =  0  if エッジなし',
    ]
    for item in items:
        doc.add_paragraph(item, style='List Bullet')

    doc.add_paragraph(
        '重み wᵢⱼ は対称化して用いる（wᵢⱼ = wⱼᵢ = (w_orig_ij + w_orig_ji)/2）。'
        '正規化磁気ラプラシアンを以下で定義する：'
    )

    add_display_equation(doc, '\u2112⁽ᑫ⁾ = I − D⁻¹ᐟ² H⁽ᑫ⁾ D⁻¹ᐟ²')

    doc.add_paragraph('ここで D = diag(d₁, ..., dₙ), dᵢ = Σⱼ |H⁽ᑫ⁾ᵢⱼ|。')

    # Proposition 3.1
    p = doc.add_paragraph()
    run = p.add_run('命題 3.1')
    run.bold = True
    p.add_run('（磁気ラプラシアンの基本性質）')

    props = [
        '(i) H⁽ᑫ⁾ はエルミート行列である：H⁽ᑫ⁾ⱼᵢ = H̄⁽ᑫ⁾ᵢⱼ。',
        '(ii) \u2112⁽ᑫ⁾ はエルミート半正定値であり、固有値は実数かつ非負。',
        '(iii) 固有ベクトルは一般に複素数値をとる。',
        '(iv) q = 0 のとき、\u2112⁽⁰⁾ は通常の正規化ラプラシアン \u2112 に退化する。',
    ]
    for prop in props:
        doc.add_paragraph(prop, style='List Bullet')

    p = doc.add_paragraph()
    run = p.add_run('命題 3.1 (i) の証明')
    run.bold = True
    run.italic = True
    p.add_run('：')

    add_display_equation(doc, 'H⁽ᑫ⁾ⱼᵢ = wⱼᵢ · exp(i · 2πq · σⱼᵢ)')

    doc.add_paragraph(
        'wⱼᵢ = wᵢⱼ（対称化済み）かつ σⱼᵢ = −σᵢⱼ より：'
    )

    add_display_equation(doc,
        'H⁽ᑫ⁾ⱼᵢ = wᵢⱼ · exp(−i · 2πq · σᵢⱼ) = w̄ᵢⱼ · exp(i · 2πq · σᵢⱼ) = H̄⁽ᑫ⁾ᵢⱼ   □')

    doc.add_heading('3.3 電荷パラメータ q の意味', level=2)
    doc.add_paragraph(
        'q は方向性に対する感度を制御するパラメータである：'
    )

    # Table for q values
    table = doc.add_table(rows=4, cols=3)
    table.style = 'Table Grid'
    headers = ['q', '位相 2πq', '効果']
    for i, h in enumerate(headers):
        cell = table.cell(0, i)
        cell.text = h
        for paragraph in cell.paragraphs:
            for run in paragraph.runs:
                run.bold = True
                run.font.size = Pt(10)

    rows_data = [
        ['0', '0', '方向性を完全無視。exp(i·0) = 1 より実行列に退化'],
        ['0.25', 'π/2', '最大方向性感度。exp(iπ/2) = i, exp(−iπ/2) = −i'],
        ['0.5', 'π', '方向を反転。exp(iπ) = −1'],
    ]
    for ri, row_data in enumerate(rows_data):
        for ci, cell_text in enumerate(row_data):
            cell = table.cell(ri + 1, ci)
            cell.text = cell_text
            for paragraph in cell.paragraphs:
                for run in paragraph.runs:
                    run.font.size = Pt(10)

    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(8)
    run = p.add_run('注意 3.1')
    run.bold = True
    p.add_run(
        ' q = 0.25 のとき、H⁽ᑫ⁾ᵢⱼ = i·wᵢⱼ（i → j のエッジ）かつ '
        'H⁽ᑫ⁾ⱼᵢ = −i·wᵢⱼ となり、方向性が虚数単位 i によって最も鋭く分離される。'
    )

    doc.add_heading('3.4 固有ベクトルの複素位相と方向性', level=2)
    doc.add_paragraph(
        '\u2112⁽ᑫ⁾ の固有ベクトル uₖ ∈ ℂⁿ の各成分は極形式で表すことができる：'
    )

    add_display_equation(doc, 'uₖ(j) = |uₖ(j)| · exp(i · θₖ(j))')

    doc.add_paragraph(
        'ここで |uₖ(j)| は振幅（ノード j がモード k にどれだけ荷重するか）、'
        'θₖ(j) = arg(uₖ(j)) は位相角である。'
    )
    p = doc.add_paragraph()
    run = p.add_run('核心的な主張')
    run.bold = True
    p.add_run(
        '：q > 0 のとき、位相角 θₖ(j) の順序が因果的フローの方向を反映する。'
        '因果の上流（原因側）のノードと下流（結果側）のノードは、'
        '固有ベクトル上で異なる位相角を持つ。'
    )

    # ============================================================
    # 4. スペクトル因果性の定式化
    # ============================================================
    doc.add_heading('4. スペクトル因果性の定式化', level=1)

    doc.add_heading('4.1 ユーティリティ有向グラフ', level=2)

    p = doc.add_paragraph()
    run = p.add_run('定義 4.1')
    run.bold = True
    p.add_run(
        '（ユーティリティ有向グラフ）n 個の変数 {X₁, ..., Xₙ} に対して、'
        'ユーティリティ関数 U: {1, ..., n}² → ℝ≥₀ を：'
    )

    add_display_equation(doc, 'U(i, j) = 「変数 Xᵢ の情報が変数 Xⱼ に関する問いにどれだけ有用か」')

    doc.add_paragraph('と定義する。ユーティリティ有向グラフ G_U = (V, E, w, σ) は：')
    items = [
        'V = {1, ..., n}',
        'w(i, j) = (U(i, j) + U(j, i)) / 2（対称化された重み）',
        'σ(i, j) = sign(U(i, j) − U(j, i))（方向性符号）',
    ]
    for item in items:
        doc.add_paragraph(item, style='List Bullet')

    # -- 4.1.1 DPI --
    doc.add_heading('4.1.1 データ駆動成分の構成：方向性予測指標（DPI）', level=3)

    doc.add_paragraph(
        'ユーティリティ関数のデータ駆動成分として、従来は |ρ̂ᵢⱼ|（相関係数の絶対値）が'
        '用いられてきた。しかし |ρ̂ᵢⱼ| = |ρ̂ⱼᵢ| であるため、データ駆動成分が完全に対称となり、'
        'α = 0（ドメイン知識なし）では方向性信号がゼロになる。これは統計的因果推論としての'
        '要件を満たさない。この理論的限界を克服するため、方向性予測指標（Directional '
        'Predictability Index, DPI）を提案する。'
    )

    p = doc.add_paragraph()
    run = p.add_run('定義 4.1a')
    run.bold = True
    p.add_run(
        '（方向性予測指標; DPI）n 個の変数 {X₁, ..., Xₙ} の観測データ X ∈ ℝ^(N×n) に対して、'
        'DPI行列 D_DPI ∈ ℝ^(n×n) を：'
    )

    add_display_equation(doc, 'D_DPI(i → j) = |ρ̂ᵢⱼ| · (1 + γ · Ā(i, j))')

    doc.add_paragraph(
        'と定義する。ここで γ > 0 は方向性強度パラメータ（本稿では γ = 1）であり、'
        'Ā(i,j) は 3 つの正規化非対称統計量の平均である：'
    )

    add_display_equation(doc, 'Ā(i,j) = (1/3) [Â_reg(i,j) + Â_ANM(i,j) + Â_ent(i,j)]')

    doc.add_paragraph('各成分は以下のように定義される：')

    doc.add_paragraph(
        '(i) 回帰係数非対称性 Â_reg：非標準化データにおける単回帰係数 '
        'β_j|i = Cov(Xᵢ, Xⱼ)/Var(Xᵢ) は、Var(Xᵢ) ≠ Var(Xⱼ) のとき '
        '|β_j|i| ≠ |β_i|j| となり非対称である。この非対称性を [−1, 1] に正規化する。'
    )
    doc.add_paragraph(
        '(ii) ANM残差独立性 Â_ANM：加法的ノイズモデル（Additive Noise Model）の原理に基づき、'
        '各ペア (i, j) に対して Xⱼ = βXᵢ + ε の残差 ε̂ と Xᵢ の独立性を HSIC'
        '（Hilbert-Schmidt Independence Criterion; カーネル帯域幅はメディアンヒューリスティック）'
        'で評価する。HSIC値が小さいほど独立性が高く、Xᵢ → Xⱼ の方向がもっともらしい。'
    )
    doc.add_paragraph(
        '(iii) 条件付きエントロピー縮減 Â_ent：Xᵢ を知ることによる Xⱼ のエントロピー縮減量 '
        'H(Xⱼ) − H(Xⱼ|Xᵢ) を kNN推定量で計算する。'
        'H(Xⱼ) − H(Xⱼ|Xᵢ) ≠ H(Xᵢ) − H(Xᵢ|Xⱼ) のとき方向性情報を持つ。'
    )

    p = doc.add_paragraph()
    run = p.add_run('命題 4.0a')
    run.bold = True
    p.add_run(' D_DPI は一般に非対称であり、D_DPI(i → j) ≠ D_DPI(j → i) である。')

    p = doc.add_paragraph()
    run = p.add_run('証明')
    run.italic = True
    p.add_run(
        '：Ā(i,j) = −Ā(j,i)（各成分の正規化非対称性は反対称）であるから、'
        'D_DPI(i → j) = |ρ̂ᵢⱼ|(1 + γĀ(i,j)) ≠ |ρ̂ᵢⱼ|(1 − γĀ(i,j)) = D_DPI(j → i)'
        '（Ā(i,j) ≠ 0 のとき）。□'
    )

    p = doc.add_paragraph()
    run = p.add_run('ユーティリティ関数のハイブリッド構成')
    run.bold = True
    p.add_run('：上記を用いて')

    add_display_equation(doc, 'U(i, j) = α · C_domain(i, j) + (1 − α) · D_DPI(i → j)')

    doc.add_paragraph(
        'とする。α = 0（ドメイン知識なし）でも D_DPI の非対称性により方向性信号が保たれ、'
        'α > 0 でドメイン知識の注入により精度が向上する。'
    )

    doc.add_heading('4.2 スペクトル因果結合度と因果方向', level=2)

    p = doc.add_paragraph()
    run = p.add_run('定義 4.2')
    run.bold = True
    p.add_run(
        '（スペクトル因果結合度; Spectral Causal Coupling, SCC）'
        '磁気ラプラシアン \u2112⁽ᑫ⁾ の固有値分解に対して、ノード i, j のスペクトル因果結合度を：'
    )

    add_display_equation(doc, 'SCC(i, j) = Σₖ f(λₖ) · |uₖ(i)| · |uₖ(j)| · cos(θₖ(i) − θₖ(j))')

    doc.add_paragraph(
        'と定義する。ここで f: ℝ≥₀ → ℝ≥₀ は固有値重み関数（典型的には f(λ) = λ）、'
        'θₖ(i) = arg(uₖ(i))。'
    )

    p = doc.add_paragraph()
    run = p.add_run('命題 4.1')
    run.bold = True
    p.add_run(' SCC は対称である：SCC(i, j) = SCC(j, i)。')

    p = doc.add_paragraph()
    run = p.add_run('証明')
    run.italic = True
    p.add_run('：cos(α − β) = cos(β − α) より直ちに従う。 □')

    doc.add_paragraph(
        'SCCは因果的結合の強さを測るが、方向は測れない。方向の定量化には以下を用いる。'
    )

    p = doc.add_paragraph()
    run = p.add_run('定義 4.3')
    run.bold = True
    p.add_run('（スペクトル因果方向; Spectral Causal Direction, SCD）')

    add_display_equation(doc, 'SCD(i, j) = Σₖ f(λₖ) · |uₖ(i)| · |uₖ(j)| · sin(θₖ(i) − θₖ(j))')

    p = doc.add_paragraph()
    run = p.add_run('命題 4.2')
    run.bold = True
    p.add_run(' SCD は反対称である：SCD(i, j) = −SCD(j, i)。')

    p = doc.add_paragraph()
    run = p.add_run('証明')
    run.italic = True
    p.add_run('：sin(α − β) = −sin(β − α) より直ちに従う。 □')

    p = doc.add_paragraph()
    run = p.add_run('系 4.1')
    run.bold = True
    p.add_run('（自己因果方向はゼロ）SCD(i, i) = 0。')

    doc.add_paragraph(
        'SCD(i, j) > 0 は「i から j への因果的方向」を、SCD(i, j) < 0 は逆方向を示唆する。'
    )

    doc.add_heading('4.3 SCC と SCD の統一的理解', level=2)

    doc.add_paragraph(
        'SCC と SCD は、複素内積の実部と虚部として統一的に理解できる。'
    )

    p = doc.add_paragraph()
    run = p.add_run('命題 4.3')
    run.bold = True
    p.add_run('（複素因果指標）以下の Complex Causal Index (CCI) を定義すると：')

    add_display_equation(doc, 'CCI(i, j) = Σₖ f(λₖ) · |uₖ(i)| · |uₖ(j)| · exp(i(θₖ(i) − θₖ(j)))')

    doc.add_paragraph('SCC と SCD は CCI の実部と虚部に対応する：')

    add_display_equation(doc, 'SCC(i, j) = Re[CCI(i, j)],    SCD(i, j) = Im[CCI(i, j)]')

    p = doc.add_paragraph()
    run = p.add_run('証明')
    run.italic = True
    p.add_run('：exp(iα) = cosα + i·sinα（Euler公式）を適用すればよい。 □')

    p = doc.add_paragraph()
    run = p.add_run('幾何学的解釈')
    run.bold = True
    p.add_run(
        '：CCI を複素平面上のベクトルとみなすと、偏角 arg(CCI(i,j)) が因果の方向を、'
        '絶対値 |CCI(i,j)| が因果的結合の強さを表す。'
    )

    doc.add_heading('4.4 SCD行列の性質', level=2)

    p = doc.add_paragraph()
    run = p.add_run('命題 4.4')
    run.bold = True
    p.add_run('')

    props = [
        '(i) S は歪対称（skew-symmetric）：S = −Sᵀ。',
        '(ii) tr(S) = 0（対角成分はすべて0）。',
        '(iii) q = 0 のとき S = O（ゼロ行列）。すなわち、方向性情報がなければ因果方向は推定できない。',
    ]
    for prop in props:
        doc.add_paragraph(prop, style='List Bullet')

    p = doc.add_paragraph()
    run = p.add_run('証明')
    run.italic = True
    p.add_run(
        '：(i) は命題4.2の行列版。(ii) は系4.1から。'
        '(iii) は q = 0 のとき θₖ(i) = 0 または π（実固有ベクトル）なので '
        'sin(θₖ(i) − θₖ(j)) = 0。 □'
    )

    doc.add_paragraph(
        '性質 (iii) は重要である：スペクトル因果性は、方向性情報（q > 0）がなければ機能しない。'
        'これはLiNGAMが非ガウス性なしには機能しないのと対照的である。'
    )

    doc.add_heading('4.5 因果順序の推定', level=2)

    p = doc.add_paragraph()
    run = p.add_run('定義 4.4')
    run.bold = True
    p.add_run('（スペクトル因果スコア）各ノード i のスペクトル因果スコアを：')

    add_display_equation(doc, 's(i) = Σⱼ≠ᵢ SCD(i, j)')

    doc.add_paragraph(
        'と定義する。s(i) が大きいノードほど「原因側（上流）」、小さいノードほど「結果側（下流）」。'
    )

    p = doc.add_paragraph()
    run = p.add_run('注意 4.2')
    run.bold = True
    p.add_run(' S の歪対称性より Σᵢ s(i) = 0 であり、スコアは零和（zero-sum）である。')

    # ============================================================
    # 5. Hodge分解
    # ============================================================
    doc.add_heading('5. Hodge分解：因果フローの直交分解', level=1)

    doc.add_heading('5.1 グラフ上の微分形式', level=2)

    p = doc.add_paragraph()
    run = p.add_run('定義 5.1')
    run.bold = True
    p.add_run('（鎖複体）グラフ G = (V, E) に対して、以下の線形写像を定義する：')

    items = [
        '0-コチェイン C⁰ = ℝ|V|（ノード上の関数）',
        '1-コチェイン C¹ = ℝ|E|（エッジ上の関数 = フロー）',
        'コバウンダリ作用素 δ₀: C⁰ → C¹：(δ₀f)(i→j) = f(j) − f(i)（勾配）',
        'コバウンダリ作用素 δ₁: C¹ → C²：三角形上のカール',
    ]
    for item in items:
        doc.add_paragraph(item, style='List Bullet')

    doc.add_heading('5.2 Hodge分解定理', level=2)

    p = doc.add_paragraph()
    run = p.add_run('定理 5.1')
    run.bold = True
    p.add_run('（グラフ上の Hodge 分解; Jiang et al., 2011）'
              '任意の 1-コチェイン（エッジフロー）ω ∈ C¹ は、以下のように直交分解される：')

    add_display_equation(doc, 'ω = δ₀φ  +  δ₁*ψ  +  h')
    doc.add_paragraph('       勾配成分    カール成分    調和成分')

    # Table
    table = doc.add_table(rows=4, cols=3)
    table.style = 'Table Grid'
    headers = ['成分', '数学的意味', '因果的解釈']
    for i, h in enumerate(headers):
        cell = table.cell(0, i)
        cell.text = h
        for paragraph in cell.paragraphs:
            for run in paragraph.runs:
                run.bold = True
                run.font.size = Pt(10)

    rows_data = [
        ['δ₀φ（勾配）', 'ポテンシャル差に駆動されるフロー', '因果的フロー（DAG的な一方向の流れ）'],
        ['δ₁*ψ（カール）', '局所的な循環フロー', 'フィードバックループ（局所的な相互作用）'],
        ['h（調和）', '大域的な循環フロー', '恒常性維持（全身性の調節メカニズム）'],
    ]
    for ri, row_data in enumerate(rows_data):
        for ci, cell_text in enumerate(row_data):
            cell = table.cell(ri + 1, ci)
            cell.text = cell_text
            for paragraph in cell.paragraphs:
                for run in paragraph.runs:
                    run.font.size = Pt(10)

    doc.add_heading('5.3 因果ポテンシャル', level=2)

    p = doc.add_paragraph()
    run = p.add_run('定義 5.2')
    run.bold = True
    p.add_run(
        '（因果ポテンシャル）勾配成分 δ₀φ におけるポテンシャル関数 φ: V → ℝ を因果ポテンシャルと呼ぶ。'
        'φ は以下の最小二乗問題の解として求まる：'
    )

    add_display_equation(doc, 'φ = argmin_φ̃ Σ₍ᵢ,ⱼ₎∈E (ω(i,j) − (φ̃(j) − φ̃(i)))²')

    doc.add_paragraph('これはグラフラプラシアンに関するポアソン方程式 Lφ = δ₀*ω に帰着する。')

    p = doc.add_paragraph()
    run = p.add_run('注意 5.1')
    run.bold = True
    p.add_run(' 勾配成分のエネルギー比：')

    add_display_equation(doc, 'r_gradient = ‖δ₀φ‖² / ‖ω‖²')

    doc.add_paragraph(
        'は、データがDAG的構造にどの程度適合するかの指標となる。'
        'r_gradient ≈ 1 ならばDAG仮定が妥当、r_gradient ≪ 1 ならばフィードバックが支配的である。'
    )

    # ============================================================
    # 6. 既存手法との関係
    # ============================================================
    doc.add_heading('6. 既存手法との関係', level=1)

    doc.add_heading('6.1 LiNGAMとの比較', level=2)

    doc.add_paragraph(
        'LiNGAM (Shimizu et al., 2006) は x = Bx + e（e ~ 非ガウス独立）を仮定し、'
        '非ガウス性を利用して因果効果行列 B を同定する。'
    )

    table = doc.add_table(rows=7, cols=3)
    table.style = 'Table Grid'
    headers = ['観点', 'LiNGAM', 'スペクトル因果性']
    for i, h in enumerate(headers):
        cell = table.cell(0, i)
        cell.text = h
        for paragraph in cell.paragraphs:
            for run in paragraph.runs:
                run.bold = True
                run.font.size = Pt(10)

    rows_data = [
        ['同定の原理', '非ガウス性', 'ユーティリティ非対称性'],
        ['仮定', '線形, 非ガウス, DAG', 'ユーティリティ非対称性が因果方向を反映'],
        ['出力', '因果効果行列 B', 'SCD行列 S + 因果ポテンシャル φ'],
        ['フィードバック', '不可（DAG仮定）', 'Hodge分解で定量化'],
        ['識別可能性', '理論的保証あり', '理論的保証なし（仮説段階）'],
        ['ドメイン知識', '不使用', 'ユーティリティ関数で注入'],
    ]
    for ri, row_data in enumerate(rows_data):
        for ci, cell_text in enumerate(row_data):
            cell = table.cell(ri + 1, ci)
            cell.text = cell_text
            for paragraph in cell.paragraphs:
                for run in paragraph.runs:
                    run.font.size = Pt(10)

    doc.add_heading('6.2 因果の梯子における位置づけ', level=2)

    table = doc.add_table(rows=5, cols=3)
    table.style = 'Table Grid'
    headers = ['レベル', '問い', '代表手法']
    for i, h in enumerate(headers):
        cell = table.cell(0, i)
        cell.text = h
        for paragraph in cell.paragraphs:
            for run in paragraph.runs:
                run.bold = True
                run.font.size = Pt(10)
    rows_data = [
        ['3: 反事実', '「もし X=x だったら Y は？」', '潜在結果モデル, do-calculus'],
        ['2: 介入', '「X を操作したら Y は変わるか？」', 'RCT, IV, MR'],
        ['1.5: 情報的因果 ★', '「X を知ると Y について何が分かるか？」', 'スペクトル因果性, Utility Causality'],
        ['1: 関連', '「X と Y は共変動するか？」', '相関, 回帰'],
    ]
    for ri, row_data in enumerate(rows_data):
        for ci, cell_text in enumerate(row_data):
            cell = table.cell(ri + 1, ci)
            cell.text = cell_text
            for paragraph in cell.paragraphs:
                for run in paragraph.runs:
                    run.font.size = Pt(10)

    doc.add_heading('6.3 Hillの9基準とスペクトル因果性', level=2)

    doc.add_paragraph(
        '既存の計算的因果推論手法は H1(強さ), H3(特異性), H4(時間性), H8(実験) に集中しており、'
        'H6(生物学的妥当性), H7(整合性), H9(類似性) は「研究者の主観」に委ねられてきた。'
        'スペクトル因果性/Utility Causality は、この空白を計算可能にする最初の試みとして位置づけられる。'
    )

    # ============================================================
    # 7. 実データ
    # ============================================================
    doc.add_heading('7. 実データによる例示', level=1)

    doc.add_heading('7.1 データと変数', level=2)
    doc.add_paragraph(
        'UCI Heart Disease Dataset (Cleveland subset; Detrano et al., 1989) の連続変数5つを用いた：'
        'X = (Age, RestingBP, Cholesterol, MaxHR, STDepression)。標本数 n = 297。'
    )

    doc.add_heading('7.2 LiNGAM による因果順序', level=2)
    doc.add_paragraph(
        '推定因果順序: Age → MaxHR → STDep → RestBP → Chol'
    )
    doc.add_paragraph('主要な因果効果:')
    items = [
        'B₄₂ = −0.395: Age → MaxHR（加齢による最大心拍数低下）',
        'B₂₁ = +0.309: Age → RestingBP（加齢による血圧上昇）',
        'B₅₄ = −0.348: MaxHR → STDepression（運動耐容能低下による心筋虚血）',
    ]
    for item in items:
        doc.add_paragraph(item, style='List Bullet')

    doc.add_heading('7.3 Hodge分解の結果', level=2)

    add_display_equation(doc, '‖δ₀φ‖² / ‖ω‖² = 85.9%    （勾配成分 = DAG的因果フロー）')
    add_display_equation(doc, '‖δ₁*ψ‖² / ‖ω‖² = 14.1%    （カール成分 = フィードバック）')

    doc.add_paragraph('因果ポテンシャル φ（降順 = 因果的上流から）:')

    table = doc.add_table(rows=6, cols=3)
    table.style = 'Table Grid'
    headers = ['順位', '変数', 'φ']
    for i, h in enumerate(headers):
        cell = table.cell(0, i)
        cell.text = h
        for paragraph in cell.paragraphs:
            for run in paragraph.runs:
                run.bold = True
                run.font.size = Pt(10)
    rows_data = [
        ['1', 'Age', '0.000'],
        ['2', 'Cholesterol', '−0.168'],
        ['3', 'Resting BP', '−0.204'],
        ['4', 'Max Heart Rate', '−0.204'],
        ['5', 'ST Depression', '−0.324'],
    ]
    for ri, row_data in enumerate(rows_data):
        for ci, cell_text in enumerate(row_data):
            cell = table.cell(ri + 1, ci)
            cell.text = cell_text
            for paragraph in cell.paragraphs:
                for run in paragraph.runs:
                    run.font.size = Pt(10)

    doc.add_paragraph(
        'Age が最上流、ST Depression が最下流という結果は臨床的に妥当である。'
        'LiNGAM の因果順序との Kendall 順位相関は τ = 0.50。'
    )

    # ============================================================
    # 8. 理論的課題と展望
    # ============================================================
    doc.add_heading('8. 理論的課題と展望', level=1)

    doc.add_heading('8.1 識別可能性', level=2)
    doc.add_paragraph(
        'LiNGAM には明確な識別可能性条件がある。スペクトル因果性には現時点で識別可能性の理論がない。'
    )

    p = doc.add_paragraph()
    run = p.add_run('予想 8.1')
    run.bold = True
    p.add_run(' 以下の条件下で、SCD は因果方向と一致する：')

    items = [
        '1. ユーティリティ非対称性 U(i,j) − U(j,i) が真の因果方向と同符号',
        '2. ユーティリティ重み w(i,j) が因果効果の強さの単調関数',
        '3. グラフがDAG的構造を持つ（r_gradient ≈ 1）',
    ]
    for item in items:
        doc.add_paragraph(item, style='List Number')

    doc.add_heading('8.2 ユーティリティ関数の構成とDPIの役割', level=2)

    doc.add_paragraph(
        '初期モデルではデータ駆動成分に |ρ̂ᵢⱼ|（相関係数の絶対値）を用いていた。'
        'しかし |ρ̂ᵢⱼ| は対称であり、α = 0 では方向性信号が消失する。'
    )

    p = doc.add_paragraph()
    run = p.add_run('ベース手法の理論的限界: ')
    run.bold = True
    p.add_run(
        '対称な統計量を用いるかぎり、ドメイン知識なし（α = 0）での因果方向推定は原理的に不可能である。'
        '本稿では §4.1.1 で定義した DPI（方向性予測指標）を導入することにより、この理論的限界を克服した。'
    )

    doc.add_paragraph(
        'DPIの導入により、スペクトル因果性の運用は以下の段階的フレームワークとなる：'
    )
    items = [
        '(a) ドメイン知識なし（α = 0）: U(i,j) = D_DPI(i → j)。DPIの非対称性のみで因果方向を推定。'
        'UCI心疾患データで r_gradient = 0.581, 9本の有向辺を検出, LiNGAM方向一致率67%。',
        '(b) ドメイン知識あり（α > 0）: U(i,j) = α·C_domain + (1−α)·D_DPI。'
        'r_gradient は 0.581 → 0.859 へ滑らかに増加。',
        '(c) LiNGAMとのアンサンブル（ECD）: LiNGAMの推定DAGから高確信辺のみを C_domain に設定可能。'
        'Hill の9基準の網羅性も向上（H6/H7/H9をカバー）。',
    ]
    for item in items:
        doc.add_paragraph(item, style='List Bullet')

    doc.add_heading('8.3 今後の方向性', level=2)
    items = [
        '識別可能性の理論構築: 特殊ケース（ツリーDAG + 線形SEM）での証明',
        'アンサンブル因果推定: ECD(i,j) = α·LiNGAM + β·SCD + γ·Granger の統計的性質',
        '経時データへの拡張: 時間的ユーティリティグラフの構築',
        '大規模データでの検証: 日本健診コホート（n > 10⁵）やMIMIC-IV',
    ]
    for item in items:
        doc.add_paragraph(item, style='List Number')

    # ============================================================
    # 記号一覧
    # ============================================================
    doc.add_heading('記号一覧', level=1)

    symbols = [
        ('G = (V, E, w)', '重み付き（有向）グラフ'),
        ('W, D', '隣接行列, 次数行列'),
        ('L = D − W', '非正規化グラフラプラシアン'),
        ('\u2112 = I − D⁻¹ᐟ²WD⁻¹ᐟ²', '正規化グラフラプラシアン'),
        ('H⁽ᑫ⁾', 'エルミート隣接行列（磁気ラプラシアン用）'),
        ('\u2112⁽ᑫ⁾ = I − D⁻¹ᐟ²H⁽ᑫ⁾D⁻¹ᐟ²', '正規化磁気ラプラシアン'),
        ('q', '電荷パラメータ（方向性感度, [0, 0.5]）'),
        ('σᵢⱼ', 'エッジ方向性符号（{−1, 0, +1}）'),
        ('uₖ, λₖ', '第 k 固有ベクトル, 固有値'),
        ('θₖ(i) = arg(uₖ(i))', 'ノード i の第 k モードにおける位相角'),
        ('U(i,j)', 'ユーティリティ関数'),
        ('SCC(i,j)', 'スペクトル因果結合度（対称）'),
        ('SCD(i,j)', 'スペクトル因果方向（反対称）'),
        ('CCI(i,j)', '複素因果指標（SCC + i·SCD）'),
        ('φ(i)', '因果ポテンシャル（Hodge分解より）'),
        ('r_gradient', '勾配エネルギー比（DAG適合度）'),
        ('D_DPI(i → j)', '方向性予測指標（非対称データ駆動成分）'),
        ('Ā(i,j)', '正規化非対称統計量の平均（DPIの方向性成分）'),
        ('γ', 'DPIの方向性強度パラメータ'),
        ('α', 'ドメイン知識の混合比率'),
    ]

    table = doc.add_table(rows=len(symbols) + 1, cols=2)
    table.style = 'Table Grid'
    table.cell(0, 0).text = '記号'
    table.cell(0, 1).text = '意味'
    for paragraph in table.cell(0, 0).paragraphs:
        for run in paragraph.runs:
            run.bold = True
    for paragraph in table.cell(0, 1).paragraphs:
        for run in paragraph.runs:
            run.bold = True

    for ri, (sym, meaning) in enumerate(symbols):
        table.cell(ri + 1, 0).text = sym
        table.cell(ri + 1, 1).text = meaning
        for ci in range(2):
            for paragraph in table.cell(ri + 1, ci).paragraphs:
                for run in paragraph.runs:
                    run.font.size = Pt(10)

    # ============================================================
    # 参考文献
    # ============================================================
    doc.add_heading('参考文献', level=1)

    refs = [
        'Pearl, J. (2009). Causality: Models, Reasoning, and Inference (2nd ed.). Cambridge University Press.',
        'Shimizu, S., Hoyer, P.O., Hyvärinen, A. & Kerminen, A. (2006). A linear non-Gaussian acyclic model for causal discovery. JMLR, 7, 2003–2030.',
        'Shimizu, S. et al. (2011). DirectLiNGAM: A direct method for learning a linear non-Gaussian structural equation model. JMLR, 12, 1225–1248.',
        'Hill, A.B. (1965). The environment and disease: Association or causation? Proc. R. Soc. Med., 58, 295–300.',
        'Granger, C.W.J. (1969). Investigating causal relations by econometric models and cross-spectral methods. Econometrica, 37(3), 424–438.',
        'Shuman, D.I. et al. (2013). The emerging field of signal processing on graphs. IEEE Signal Processing Magazine, 30(3), 83–98.',
        'Zhang, X. et al. (2022). MagNet: A neural network for directed graphs. NeurIPS 2021.',
        'de Resende, B.M.F. & da Costa, L.F. (2020). Characterization of large directed networks through the spectra of the magnetic Laplacian. Chaos, 30(7), 073141.',
        'Seifert, B., Wendler, C. & Püschel, M. (2023). Causal Fourier analysis on directed acyclic graphs and posets. IEEE Trans. Signal Processing, 71, 3516–3530.',
        'Jiang, X. et al. (2011). Statistical ranking and combinatorial Hodge theory. Mathematical Programming, 127, 203–244.',
        'Maehara, K. & Ohkawa, Y. (2019). Modeling latent flows on single-cell data using the Hodge decomposition. bioRxiv.',
        'Kotoku, J. et al. (2020). Causal relations of health indices inferred statistically using DirectLiNGAM. PLOS ONE, 15(12), e0243229.',
        'Okuda, S. et al. (2025). Operationalizing longitudinal causal discovery under real-world workflow constraints. arXiv:2602.23800.',
        'Detrano, R. et al. (1989). International application of a new probability algorithm for the diagnosis of coronary artery disease. Am. J. Cardiol., 64, 304–310.',
        'Rubin, D.B. (1974). Estimating causal effects of treatments in randomized and nonrandomized studies. J. Educ. Psychol., 66(5), 688–701.',
    ]

    for i, ref in enumerate(refs):
        p = doc.add_paragraph()
        run_num = p.add_run(f'[{i+1}] ')
        run_num.bold = True
        run_num.font.size = Pt(10)
        run_text = p.add_run(ref)
        run_text.font.size = Pt(10)

    # Save
    output_path = os.path.join(BASE_DIR, '06_spectral_causality_academic.docx')
    doc.save(output_path)
    print(f'Saved: {output_path}')
    return output_path


if __name__ == '__main__':
    generate_docx()
