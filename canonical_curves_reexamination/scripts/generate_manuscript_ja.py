"""
Generate the manuscript as .docx (Japanese version).
"""

import os
import sys
import json
import re
import numpy as np
import pandas as pd
from docx import Document
from docx.shared import Inches, Pt, Cm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FIGURES_DIR = os.path.join(BASE_DIR, 'figures')
RESULTS_DIR = os.path.join(BASE_DIR, 'results')


def load_results():
    with open(os.path.join(RESULTS_DIR, 'full_results.json'), 'r') as f:
        return json.load(f)


def add_superscript_refs(paragraph, text):
    parts = re.split(r'(\{[^}]+\})', text)
    for part in parts:
        if part.startswith('{') and part.endswith('}'):
            run = paragraph.add_run(part[1:-1])
            run.font.superscript = True
            run.font.size = Pt(8)
        else:
            run = paragraph.add_run(part)
            run.font.size = Pt(10.5)


def create_manuscript_ja():
    doc = Document()

    style = doc.styles['Normal']
    font = style.font
    font.name = 'Times New Roman'
    font.size = Pt(10.5)

    sections = doc.sections
    for section in sections:
        section.top_margin = Cm(2.54)
        section.bottom_margin = Cm(2.54)
        section.left_margin = Cm(2.54)
        section.right_margin = Cm(2.54)

    results = load_results()
    verdicts = [r['verdict']['verdict'] for r in results]
    n_ns = verdicts.count('NOT_SIGNIFICANT')
    n_outlier = verdicts.count('OUTLIER_DEPENDENT')
    n_robust = verdicts.count('ROBUST_NONLINEAR')
    n_overfit = verdicts.count('OVERFITTING')

    # Title
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = p.add_run('定説曲線52本の現代的再検証：\n'
                    '外れ値依存性・サンプルサイズ・確立された非線形関係の脆弱性')
    run.bold = True
    run.font.size = Pt(14)

    doc.add_paragraph()
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = p.add_run('大西 龍輝')
    run.font.size = Pt(12)

    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = p.add_run('2026年')

    doc.add_page_break()

    # Abstract
    p = doc.add_paragraph()
    run = p.add_run('要旨')
    run.bold = True
    run.font.size = Pt(12)

    abstract = (
        f"【背景】多くの曲線関係が様々な学問分野で「定説」として引用されているが、現代のモデル選択手法で"
        f"体系的に再検証されたものは少ない。【方法】経済学、公衆衛生学、人口学、環境科学、心理学、物理学、"
        f"政治学、農学の8分野にまたがる52本の定説曲線を、ネストF検定（線形 vs 二次）、AIC/BIC、"
        f"Leave-One-Out交差検証（LOOCV）RMSE、およびCookの距離に基づく感度分析（上位3点除外）を用いて"
        f"統一的に再検証した。【結果】52本中、{n_ns}本（{100*n_ns/52:.0f}%）は非線形性が統計的に有意でなく、"
        f"{n_outlier}本（{100*n_outlier/52:.0f}%）は外れ値依存（1〜3点の除外で有意性消失）、"
        f"{n_overfit}本（{100*n_overfit/52:.0f}%）は過適合であり、頑健な非線形性を示したのは"
        f"{n_robust}本（{100*n_robust/52:.0f}%）のみであった。外れ値依存カテゴリには、クズネッツ曲線、"
        f"環境クズネッツ曲線、グレートギャツビー曲線、リプセット仮説、種数-面積関係などの著名な曲線が含まれる。"
        f"【結論】教科書的な曲線関係の相当部分が現代的再検証に耐えず、これらの曲線に基づく政策提言には"
        f"慎重さが求められる。"
    )
    doc.add_paragraph(abstract)

    p = doc.add_paragraph()
    run = p.add_run('キーワード：')
    run.bold = True
    p.add_run('モデル選択、非線形性、外れ値依存、F検定、AIC、BIC、交差検証、Cookの距離、定説曲線')

    doc.add_page_break()

    # 1. 序論
    h = doc.add_heading('1. 序論', level=1)

    intro_paras = [
        ("曲線関係は社会科学・自然科学において特権的な地位を占めている。マクロ経済学のフィリップス曲線から"
         "公衆衛生学のプレストン曲線に至るまで、これらの非線形関数形は広く教育され、政策文書で頻繁に引用され、"
         "確立された経験則として扱われている。{1-3}しかし、これらの関係の多くは限られたデータ、初歩的な統計手法、"
         "そしてAICやBICなどのモデル選択基準が標準化される以前の時代に確立されたものである。{4,5}"),

        ("近年の研究は、いくつかの著名な曲線がサンプルサイズ不足、外れ値依存、または不適切なモデル特定の"
         "アーティファクトである可能性を示している。例えば、プレストン曲線の見かけの凹性は米国の外れ値としての"
         "位置に大きく依存することが示されている。{6}CO2排出に関する環境クズネッツ曲線は繰り返し異議を"
         "唱えられている。{7,8}ダニング・クルーガー効果は平均への回帰という統計的アーティファクトである"
         "という批判がある。{9}"),

        ("しかし、これらの個別的な再検証にもかかわらず、学際的な体系的監査は行われてこなかった。本研究は、"
         "8つの学問分野にまたがる52本の定説曲線に統一的な方法論的フレームワークを適用することで、"
         "このギャップを埋めるものである。"),
    ]
    for text in intro_paras:
        p = doc.add_paragraph()
        add_superscript_refs(p, text)

    # 2. 方法
    h = doc.add_heading('2. 方法', level=1)

    doc.add_heading('2.1 曲線の選定', level=2)
    doc.add_paragraph(
        "以下の基準を満たす52本の曲線を選定した：(a) 学術文献で命名された関係であること、"
        "(b) 非線形性（凹性、凸性、U字型、J字型、べき乗則）が主張されていること、"
        "(c) 二変量分析が可能であること、(d) 公開データで検証可能であること。"
        "対象分野は経済学（12本）、公衆衛生/疫学（10本）、人口学（6本）、環境科学（6本）、"
        "心理学（5本）、物理学（4本）、政治学（5本）、農学/栄養学（4本）である。"
    )

    doc.add_heading('2.2 統計的フレームワーク', level=2)
    methods = [
        "ネストF検定：制約モデル（線形：y = a + bx）と非制約モデル（二次：y = a + bx + cx²）を最小二乗法で推定し、二次項の追加パラメータに対するF統計量を計算。",
        "情報量規準：線形、二次、対数モデルについてAICとBICを計算し、最小値のモデルを選択。",
        "Leave-One-Out交差検証：線形・二次モデルのLOOCV RMSEを計算し、サンプル外予測精度を評価。",
        "Cookの距離感度分析：線形モデルのCookの距離を計算し、上位3点の影響力のある観測値を除外して F検定を再実施。完全データでは有意（p < 0.05）だが除外後に非有意（p > 0.05）となる曲線を「外れ値依存」と分類。",
    ]
    for m in methods:
        doc.add_paragraph(m, style='List Bullet')

    # 3. 結果
    h = doc.add_heading('3. 結果', level=1)

    doc.add_heading('3.1 全体的な判定分布', level=2)
    doc.add_paragraph(
        f"検証した52本の定説曲線のうち、{n_robust}本（{100*n_robust/52:.0f}%）が頑健な非線形性を示し、"
        f"{n_outlier}本（{100*n_outlier/52:.0f}%）が外れ値依存、{n_ns}本（{100*n_ns/52:.0f}%）が"
        f"非有意、{n_overfit}本（{100*n_overfit/52:.0f}%）が過適合であった（図1）。"
        f"これは教科書的な非線形関係の約3分の2が、有意性に達しないか少数の影響力のある観測値に"
        f"依存していることを示唆している。"
    )

    # Figure 1
    doc.add_paragraph()
    doc.add_picture(os.path.join(FIGURES_DIR, 'fig1_verdict_distribution.png'), width=Inches(6.0))
    p = doc.add_paragraph()
    run = p.add_run('図1. ')
    run.bold = True
    p.add_run('52本の定説曲線の判定分布。(A) 全体の円グラフ。(B) 学問分野別の判定。')
    p.paragraph_format.space_before = Pt(6)

    # Domain results
    doc.add_heading('3.2 分野別結果', level=2)

    domain_results = [
        ("経済学（12本）", "7本が非有意、4本が外れ値依存、1本のみ（J曲線）が頑健。フィリップス曲線は"
         "米国1960-2023年データで非線形性なし（p=0.82）。クズネッツ曲線の逆U字は60か国データで"
         "統計的に有意でない（p=0.25）。環境クズネッツ曲線（CO2）は有意だが（p=0.003）、"
         "高所得高排出3か国の除外で非有意に（p=0.11）。"),
        ("公衆衛生（10本）", "最も頑健な分野（8本が頑健）。BMI死亡J曲線、飲酒死亡J曲線、"
         "バーカー仮説U字、LNT線量反応はすべて検証に耐えた。ウィルキンソン曲線のみ非有意（p=0.75）。"),
        ("人口学（6本）", "リー・カーター死亡率低下とコール・トラッセル出生力スケジュールは頑健。"
         "人口転換モデルは過適合（二次項有意だがLOOCVで線形が優位）。"),
        ("環境科学（6本）", "キーリング曲線の加速は頑健（p < 10\u207b\u00b9\u2075）。"
         "種数-面積関係は対数-対数空間で外れ値依存（p=0.009→除外後p=0.38）。"
         "ハバートピークは米国シェール革命により二次トレンドなし（p=0.90）。"),
        ("心理学（5本）", "4本が頑健（ヤーキーズ・ドッドソン、エビングハウス、ダニング・クルーガー、"
         "幸福U字）。ウェーバー・フェヒナーは対数空間で線形からの逸脱なし（p=0.07）。"),
        ("物理学（4本）", "ハッブル法則は外れ値依存（近傍銀河の固有速度の影響）。"
         "クライバー法則は対数空間で頑健に線形（p=0.36）。"
         "グーテンベルグ・リヒター則は巨大地震に依存。"),
        ("政治学（5本）", "リプセット仮説が最も劇的な外れ値依存例：完全データではp=0.0001だが"
         "湾岸産油国除外でp=0.37。デュヴェルジェ法則は非有意（p=0.45）。"),
        ("農学（4本）", "ミッチェルリッヒ収量曲線は頑健（p < 10\u207b\u2079）。"
         "微量栄養素U字も頑健。緑の革命曲線は非線形減速なし（p=0.28）。"),
    ]

    for title, text in domain_results:
        p = doc.add_paragraph()
        run = p.add_run(title + '：')
        run.bold = True
        p.add_run(text)

    # Figure 2
    doc.add_paragraph()
    doc.add_picture(os.path.join(FIGURES_DIR, 'fig2_sensitivity_analysis.png'), width=Inches(5.5))
    p = doc.add_paragraph()
    run = p.add_run('図2. ')
    run.bold = True
    p.add_run('F検定p値の外れ値除外に対する感度。各点は1本の曲線を表す。'
              '水平破線（p=0.05）より上の点は、上位3点の除外で有意性を失った曲線。')
    p.paragraph_format.space_before = Pt(6)

    # 4. 考察
    h = doc.add_heading('4. 考察', level=1)

    doc.add_heading('4.1 横断的パターン', level=2)
    patterns = [
        "外れ値駆動型非線形性（23%）：最も一般的な失敗モードは1-3点の観測値による曲率の駆動である。",
        "分野間非対称性：公衆衛生・心理学の曲線は経済学の曲線より格段に頑健（80% vs 8%）。",
        "時系列 vs 横断面：時系列曲線は横断面曲線より頑健である。",
        "対数変換による解消：多くの場合、予測変数の対数変換で線形関係が得られる。",
        "BICの保守性：BICはAICが二次を選ぶ場合でも線形を選ぶことが多い。",
    ]
    for pat in patterns:
        doc.add_paragraph(pat, style='List Number')

    doc.add_heading('4.2 政策的含意', level=2)
    doc.add_paragraph(
        "外れ値依存の曲線の中には直接的な政策的含意を持つものがある。ラッファー曲線は減税政策の正当化に"
        "用いられるが、OECD諸国間での経験的根拠は脆弱である。CO2に関する環境クズネッツ曲線は"
        "経済成長がいずれ排出問題を解決するという議論に頻繁に引用されるが、この関係は高所得産油国の"
        "除外で崩壊する。リプセット仮説は政治学の近代化論を支えるが、その非線形性は湾岸産油国の"
        "外れ値にほぼ全面的に依存している。"
    )

    doc.add_heading('4.3 限界', level=2)
    doc.add_paragraph(
        "本研究にはいくつかの限界がある。第一に、二変量関係のみを対象としており、多変量設定での"
        "再検証は含まない。第二に、統一的に二次モデルを代替仮説としているが、一部の曲線には"
        "特定の関数形（べき乗則、ロジスティック関数等）が適切である。第三に、一部の曲線では"
        "代表的データまたはメタ分析データに依拠しており、個人レベルのミクロデータではない。"
    )

    # 5. 結論
    h = doc.add_heading('5. 結論', level=1)
    doc.add_paragraph(
        f"52本の定説曲線の体系的再検証により、確立された非線形関係の"
        f"{100*(n_ns + n_outlier + n_overfit)/52:.0f}%が少なくとも1つの現代的頑健性検定に"
        f"不合格であることが明らかになった。最も一般的な失敗モードは外れ値依存"
        f"（{100*n_outlier/52:.0f}%）であり、次いで非有意（{100*n_ns/52:.0f}%）である。"
        f"頑健な非線形性を示したのは{100*n_robust/52:.0f}%のみであった。"
        f"これらの知見は、特に関係の形状が最適介入を決定する政策関連の文脈において、"
        f"定説曲線を非線形理論の経験的根拠として引用することに慎重さを促すものである。"
    )

    # References
    doc.add_page_break()
    h = doc.add_heading('参考文献', level=1)
    references = [
        "Phillips AW. The relation between unemployment and the rate of change of money wage rates in the United Kingdom, 1861-1957. Economica. 1958;25(100):283-299.",
        "Kuznets S. Economic growth and income inequality. Am Econ Rev. 1955;45(1):1-28.",
        "Preston SH. The changing relation between mortality and level of economic development. Popul Stud. 1975;29(2):231-248.",
        "Akaike H. A new look at the statistical model identification. IEEE Trans Automat Contr. 1974;19(6):716-723.",
        "Schwarz G. Estimating the dimension of a model. Ann Stat. 1978;6(2):461-464.",
        "Onishi T. Re-examination of the Preston Curve: outlier dependence of quadratic fit. Working paper. 2026.",
        "Grossman GM, Krueger AB. Environmental impacts of a North American free trade agreement. NBER Working Paper 3914. 1991.",
        "Stern DI. The rise and fall of the environmental Kuznets curve. World Dev. 2004;32(8):1419-1439.",
        "Krueger J, Mueller RA. Unskilled, unaware, or both? J Pers Soc Psychol. 2002;82(2):180-188.",
    ]
    for i, ref in enumerate(references, 1):
        p = doc.add_paragraph()
        run = p.add_run(f"{i}. ")
        run.bold = True
        p.add_run(ref)
        p.paragraph_format.left_indent = Cm(1)

    # Save
    output_path = os.path.join(BASE_DIR, 'manuscript_canonical_curves_ja.docx')
    doc.save(output_path)
    print(f"Japanese manuscript saved to: {output_path}")
    return output_path


if __name__ == "__main__":
    create_manuscript_ja()
