#!/usr/bin/env python3
"""Generate DVS × Noise Inverse Problem review as Word docx."""

import re
from docx import Document
from docx.shared import Pt, Inches, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT


def add_superscript_text(paragraph, text):
    """Parse {N} markers and create superscript runs."""
    parts = re.split(r'(\{[^}]+\})', text)
    for part in parts:
        if part.startswith('{') and part.endswith('}'):
            run = paragraph.add_run(part[1:-1])
            run.font.superscript = True
            run.font.size = Pt(8)
        else:
            run = paragraph.add_run(part)
            run.font.size = Pt(10.5)
    return paragraph


def set_cell_text(cell, text, bold=False, size=Pt(9)):
    """Set cell text with formatting."""
    cell.text = ''
    p = cell.paragraphs[0]
    run = p.add_run(text)
    run.font.size = size
    run.bold = bold


def add_table(doc, headers, rows, col_widths=None):
    """Add a formatted table."""
    table = doc.add_table(rows=1 + len(rows), cols=len(headers))
    table.style = 'Table Grid'
    table.alignment = WD_TABLE_ALIGNMENT.CENTER

    # Header
    for i, h in enumerate(headers):
        set_cell_text(table.rows[0].cells[i], h, bold=True)

    # Data rows
    for r_idx, row in enumerate(rows):
        for c_idx, val in enumerate(row):
            set_cell_text(table.rows[r_idx + 1].cells[c_idx], val)

    doc.add_paragraph()  # spacing after table
    return table


def build_document():
    doc = Document()

    # -- Styles --
    style = doc.styles['Normal']
    style.font.name = 'Times New Roman'
    style.font.size = Pt(10.5)
    style.paragraph_format.space_after = Pt(6)
    style.paragraph_format.line_spacing = 1.15

    # -- Title --
    title = doc.add_heading('DVS × ノイズ逆問題: 先行研究の体系的整理と未開拓領域の同定', level=0)
    title.alignment = WD_ALIGN_PARAGRAPH.CENTER

    # -- Background --
    doc.add_heading('背景', level=1)
    doc.add_paragraph(
        '従来のノイズ除去は「信号の逆問題」（観測 = 信号 ⊛ PSF + ノイズ → 信号を解く）として定式化されてきた。'
        '本レビューでは逆の発想——ノイズの生成機構を物理モデルとして逆問題的に定式化し、'
        'ノイズを再構成・除去する——をDynamic Vision Sensor (DVS) に適用する可能性を検討する。'
    )
    doc.add_paragraph(
        'DVSは各ピクセルが独立・非同期に輝度変化をイベントとして出力するニューロモルフィックセンサーであり、'
        '昆虫の複眼における変化検出ニューロンを模倣した設計思想を持つ。'
        '対数応答・高ダイナミックレンジ・マイクロ秒時間分解能という特性から、'
        '天文観測や宇宙状況認識 (SSA) への応用が進んでいるが、'
        '低照度条件下ではショットノイズに起因するバックグラウンドアクティビティ (BA) が支配的になる。'
    )
    doc.add_paragraph(
        '本文書では先行研究を4領域に分類し、その交差点にある未開拓領域（ギャップ g1–g4）を特定する。'
    )

    # ======== Section A ========
    doc.add_heading('A. DVSノイズの物理モデリング（5件）', level=1)
    doc.add_paragraph(
        'DVSピクセルの回路物理に基づくノイズ特性の理論的解明。'
        'UZH/ETH Zurich の Graça & Delbrück グループが中心。'
    )

    add_table(doc,
        ['#', '文献', '主な貢献'],
        [
            ['A1', 'Graca & Delbruck (2023)\n"Optimal biasing and physical limits of DVS event noise"\narXiv:2304.04019',
             'DVSフォトレセプタのショットノイズ限界を理論的に証明：光子ノイズの2倍が下限。バイアス最適化の指針を提示。'],
            ['A2', 'McReynolds, Graca, Delbruck (2023)\n"Exploiting Alternating DVS Shot Noise Event Pair Statistics"\narXiv:2304.03494',
             'ON/OFFイベントの交互出現統計を利用したノイズ識別。ショットノイズイベントはON→OFF交互パターンを示すことを実証。'],
            ['A3', 'Graca, Zhou, McReynolds, Delbruck (2024)\n"SciDVS" ESSERC 2024',
             '科学応用向けDVS。180nm CMOSで1.7%感度@0.7 lux。自動センタリングプリアンプ、帯域制御、ピクセルビニング。'],
            ['A4', 'Delbruck, Graca, Paluch (2021)\n"Feedback Control of Event Cameras"\nCVPRW 2021',
             'DVSの閾値・帯域・不応期をフィードバック制御する枠組み。ノイズ特性がバイアス設定に強く依存することを実証。'],
            ['A5', 'Graca & Delbruck (2025)\n"Towards a physically realistic computationally efficient DVS pixel model"\narXiv:2505.07386',
             '大信号微分方程式ベースのDVSピクセルモデル。First-passage-time理論に基づく確率的イベント生成。従来手法の1000倍以上の計算効率。ノイズ逆問題のフォワードモデルとして原理的に使用可能。'],
        ])

    p = doc.add_paragraph()
    p.add_run('小括: ').bold = True
    p.add_run(
        'Graça–Delbrück グループの一連の研究により、DVSノイズの物理的生成機構は回路レベルで高精度にモデル化されつつある。'
        '特にA5のピクセルモデルは、ノイズ逆問題のフォワードモデルとして直接利用できるポテンシャルを持つ。'
    )

    # ======== Section B ========
    doc.add_heading('B. DVSノイズフィルタリング手法（7件）', level=1)
    doc.add_paragraph('経験的手法から確率的手法、さらに運動との同時推定へと進化。')

    add_table(doc,
        ['#', '文献', '手法', '主な貢献'],
        [
            ['B1', 'Delbruck (2008)', '経験的', '最初期の時空間近傍フィルタ。'],
            ['B2', 'Liu & Delbruck (2008)', '経験的', 'オプティカルフローベースのフィルタリング。'],
            ['B3', 'Baldwin et al. (2020) CVPR', '確率的+DL', 'Event Probability Mask。最初の実世界ラベル付きDVSノイズデータセット DVSNOISE20。'],
            ['B4', 'McReynolds et al. (2023)', '物理統計的', 'ON/OFF交互統計によるフィルタリング（A2と同一論文）。'],
            ['B5', 'Fang et al. (2024) TPAMI', 'DL', '窓ベースWedNet。リアルタイム多スケールデノイジング。'],
            ['B6', 'Wu et al. (2024) ISPRS', 'DL', 'ASTEDNet。非同期時空間イベントデノイジング。'],
            ['B7', 'Shiba, Aoki, Gallego (2025) ICCV', '同時推定', '運動推定とノイズ推定を同時に行う初の手法。CMax枠組みの拡張。E-MLBでSOTA。'],
        ])

    p = doc.add_paragraph()
    p.add_run('小括: ').bold = True
    p.add_run(
        'B7 (Shiba et al.) は運動とノイズの同時推定という点で、ノイズ逆問題アプローチに概念的に最も近い。'
        'しかし、ノイズモデルは現象論的（データ駆動）であり、A5のような物理ベースのフォワードモデルとは統合されていない。'
    )

    # ======== Section C ========
    doc.add_heading('C. DVSの天文・宇宙応用（5件）', level=1)
    doc.add_paragraph('DVSの高速・高ダイナミックレンジ特性を天文観測・宇宙状況認識 (SSA) に活用する研究。')

    add_table(doc,
        ['#', '文献', '応用', '主な貢献'],
        [
            ['C1', 'Afshar et al. (2019)', 'SSA', '最初のイベントベース宇宙観測データセット。236録画、572ラベル付き宇宙物体。'],
            ['C2', 'Chin et al. (2019) CVPRW', '姿勢推定', 'イベントカメラを用いた恒星追跡。データセット公開。'],
            ['C3', 'Joubert et al. (2022) Front. Neurosci.', 'SSA', 'FIESTAアルゴリズム。教師なしリアルタイム追跡。'],
            ['C4', 'Gędek et al. (2019)', 'SSA', 'DVS、DAVIS、ATISカメラの観測的評価。昼間観測含む。'],
            ['C5', 'Hoang (2023)', '高エネルギー', '大気チェレンコフ望遠鏡へのニューロモルフィックカメラ適用の展望。'],
        ])

    p = doc.add_paragraph()
    p.add_run('小括: ').bold = True
    p.add_run(
        'DVSの天文応用は主にSSAに集中。微弱天体の検出（NEO、高速移動暗天体）にDVSを用いた研究は未だ存在しない。'
    )

    # ======== Section D ========
    doc.add_heading('D. 非DVS領域におけるノイズ逆問題アプローチ（5件）', level=1)
    doc.add_paragraph('信号ではなくノイズを逆問題として解く発想の先行事例。')

    add_table(doc,
        ['#', '文献', '領域', '主な貢献'],
        [
            ['D1', 'Vajente et al. (2020) Phys. Rev. D', 'LIGO', '最も成功したノイズ逆問題事例。補助センサーで非定常ノイズを独立計測し機械学習で差し引き。'],
            ['D2', 'Dooney et al. (2025)', '重力波', 'ノイズ分布モデル化→予測・差し引きのDLフレームワーク DeepExtractor。'],
            ['D3', 'Wang et al. (2024) MLST', '重力波', 'WaveFormer。Transformerベースのノイズ除去。'],
            ['D4', 'Chatterjee & Jani (2025) ApJ', '重力波', 'グリッチ存在下でもロバストな信号再構成。'],
            ['D5', 'Cao et al. (2024) Optica', 'DVS+計算イメージング', 'Noise2Image。ノイズイベントの照度依存性から静的シーンを復元。パラダイム転換。'],
        ])

    p = doc.add_paragraph()
    p.add_run('小括: ').bold = True
    p.add_run(
        'LIGO (D1–D4) では「ノイズの物理モデル + 補助チャンネル → ノイズ再構成・差し引き」パイプラインが確立済み。'
        'D5 (Noise2Image) はDVSノイズの情報的価値を初めて実証したが、動的シーン・天文条件への拡張は未検討。'
    )

    # ======== Gaps ========
    doc.add_heading('未開拓領域（ギャップ）の同定', level=1)
    doc.add_paragraph('4領域の交差から、以下の4つのギャップを特定する。')

    # -- g1 --
    doc.add_heading('g1: 物理ベースDVSノイズフォワードモデルの逆問題定式化（A→D ブリッジ）', level=2)
    doc.add_paragraph(
        '現状: A5が物理的に現実的なDVSピクセルモデルを報告。しかしフォワードモデルとしてのみ使用されており、'
        '逆問題（観測イベントストリーム→ノイズパラメータ推定→ノイズ除去）としては定式化されていない。'
    )
    doc.add_paragraph(
        '提案: A5のfirst-passage-time理論ベースモデルを逆問題として定式化。'
        'フォワードモデル F(θ) からの期待ノイズイベントと観測の距離を最小化する推定問題。'
        '必要な研究: 微分可能な実装、点過程に適した距離関数の設計、計算効率の確保。'
    )

    # -- g2 --
    doc.add_heading('g2: 自己教師ありノイズ学習によるDVSデノイジング（B→D ブリッジ）', level=2)
    doc.add_paragraph(
        '現状: B3は統計的ラベル生成、B7は運動とノイズの同時推定を行うが、いずれもノイズの物理モデルを内包していない。'
        'D5はノイズの照度依存性を利用するが、動的シーンには未対応。'
    )
    doc.add_paragraph(
        '提案: Noise2Noise/Noise2Image枠組みをDVSの動的シーンに拡張。'
        'DVSの時間的冗長性を活用し、同一ピクセルからの連続ノイズイベント列をペアとしてNoise2Noise学習。'
        'A2/B4のON/OFF交互統計をペア生成の物理的根拠として使用。'
    )

    # -- g3 --
    doc.add_heading('g3: DVS × ノイズ逆問題による天文学的微弱天体検出（A+B+C 統合）', level=2)

    doc.add_heading('g3の問題構造', level=3)
    doc.add_paragraph('微弱天体のDVS検出における根本的困難:')
    doc.add_paragraph('(1) 信号がノイズ以下: 微弱天体からのイベントレートがバックグラウンドノイズイベントレートを下回る。', style='List Number')
    doc.add_paragraph('(2) 非定常性: 天体は移動するため、単一ピクセルでの時間積分が困難。', style='List Number')
    doc.add_paragraph('(3) テンプレート不在: 検出すべき天体の軌道パラメータが未知。', style='List Number')

    doc.add_heading('g3の提案アプローチ: イベントレベル shift-and-stack + ノイズモデル引き算', level=3)

    p = doc.add_paragraph()
    p.add_run('ステップ1: ノイズマップの構築').bold = True
    doc.add_paragraph(
        'A5の物理モデルを用いて各ピクセルの期待ノイズイベントレート λ_noise(x,y,t) を推定。'
        '温度、バイアス設定、背景照度から決定。観測イベントストリームから λ_noise を差し引いた残差イベントストリームを得る。'
    )

    p = doc.add_paragraph()
    p.add_run('ステップ2: 残差ストリーム上でのイベントレベル shift-and-stack').bold = True
    doc.add_paragraph(
        '候補軌道パラメータ (v_x, v_y) に沿ってイベントを時空間的にシフトし累積。'
        'Contrast Maximization (CMax) 枠組みの自然な拡張。ノイズモデル引き算により誤検出率を大幅に低減。'
    )

    p = doc.add_paragraph()
    p.add_run('ステップ3: 統計的有意性の評価').bold = True
    doc.add_paragraph(
        '残差ストリームでのイベント累積がポアソンノイズの期待値を有意に超えるかを検定。'
        '物理モデルに基づくFAR (False Alarm Rate) の理論的計算が可能。'
    )

    doc.add_heading('g3の研究課題', level=3)
    add_table(doc,
        ['課題', '内容', '難易度'],
        [
            ['g3-a', 'A5モデルの天文条件（極低照度、長時間運用）への適用可能性検証', '中'],
            ['g3-b', 'イベントレベル shift-and-stack のアルゴリズム設計と計算量評価', '中'],
            ['g3-c', 'ノイズ引き算後の残差統計の理論的特性化（ポアソン性からの逸脱）', '高'],
            ['g3-d', 'SciDVS (A3) のような高感度DVSでの実観測的検証', '高'],
            ['g3-e', '既存SSAデータセット (C1) での検証とベンチマーク', '中'],
        ])

    doc.add_heading('g3の先行研究との差分', level=3)
    add_table(doc,
        ['手法', 'ノイズモデル', '天文対応', '微弱天体', '運動推定'],
        [
            ['Shiba et al. (B7)', 'データ駆動', '×', '×', '○ (CMax)'],
            ['Noise2Image (D5)', '照度依存', '×', '△ (静的のみ)', '×'],
            ['FIESTA (C3)', '閾値ベース', '○', '×', '○'],
            ['shift-and-stack (天文)', 'なし', '○', '○', '○'],
            ['g3提案', '物理モデル (A5)', '○', '○', '○'],
        ])

    # -- g4 --
    doc.add_heading('g4: 全統合パイプライン — 物理情報付きDVSノイズ再構成 + 補助チャンネル融合 + 天文微弱ターゲット回復（A+B+C+D 完全統合）', level=2)

    doc.add_paragraph(
        '現状: g1–g3は個別の拡張方向だが、これらをLIGOの成功事例 (D1) をテンプレートとして統合するアプローチは存在しない。'
    )

    doc.add_heading('LIGOの成功要因とDVSへの移植', level=3)
    doc.add_paragraph(
        'LIGOでは以下が成功の鍵: (1) ノイズの物理モデル、(2) 補助センサー（ウィットネスチャンネル）、'
        '(3) 機械学習による非定常ノイズ結合の学習、(4) 結果の物理的検証。'
        'これらすべてにDVS天文観測における対応物が存在する。'
    )

    doc.add_heading('g4のシステムアーキテクチャ', level=3)
    doc.add_paragraph(
        'Stage 1: ノイズフォワードモデル構築 — A5モデル + 補助チャンネル（温度・振動・照度）でリアルタイムノイズレート予測。'
    )
    doc.add_paragraph(
        'Stage 2: ノイズ逆問題求解 — 最尤推定 / 変分推論 / DeepClean型NNの3アプローチ。'
        '物理モデルがアーキテクチャの帰納的バイアスを提供（Physics-Informed Neural Network）。'
    )
    doc.add_paragraph(
        'Stage 3: 残差イベントストリーム生成 — 確率的薄化 / レート引き算 / マーク付き点過程差分の3手法。'
    )
    doc.add_paragraph(
        'Stage 4: 微弱天体検出 = g3パイプライン。残差ストリーム上でのshift-and-stack。'
    )
    doc.add_paragraph(
        'Stage 5: 物理的検証 — PSDテスト、注入・回収テスト、既知天体テスト、ブラインドテスト。'
    )

    doc.add_heading('LIGO → DVS 対応表', level=3)
    add_table(doc,
        ['LIGO要素', 'DVS対応', '状態'],
        [
            ['主チャンネル（ひずみデータ）', 'DVSイベントストリーム', '利用可能'],
            ['補助チャンネル（加速度計等）', '温度・振動・照度センサー', '要構築'],
            ['ノイズ物理モデル', 'A5 DVSピクセルモデル', '利用可能（天文条件未検証）'],
            ['DeepClean (非定常ノイズ学習)', 'DeepClean的NN', '要開発'],
            ['テンプレートマッチング', 'shift-and-stack（軌道探索）', '概念的に利用可能'],
            ['信号注入テスト', '模擬天体注入テスト', '要設計'],
        ])

    doc.add_heading('g4の研究課題', level=3)
    add_table(doc,
        ['課題', '内容', '難易度', '依存関係'],
        [
            ['g4-a', '補助チャンネルシステムの設計・構築', '高', 'なし'],
            ['g4-b', 'A5モデルの天文条件拡張', '中', 'なし'],
            ['g4-c', 'DeepClean型NNのDVS版設計', '中', 'g4-a, g4-b'],
            ['g4-d', 'イベントストリーム差分演算の理論的基礎', '高', 'g4-b'],
            ['g4-e', '注入・回収テストフレームワーク構築', '中', 'g4-d'],
            ['g4-f', 'SciDVS + 小口径望遠鏡での概念実証観測', '高', 'g4-a〜d'],
            ['g4-g', '大口径望遠鏡でのスケーラビリティ評価', '非常に高', 'g4-f'],
        ])

    doc.add_heading('g4の期待されるインパクト', level=3)
    doc.add_paragraph(
        '(1) 検出限界の拡張: ノイズ逆問題パイプラインにより、DVSの検出限界等級を2–4等級改善する可能性。'
        'フレームカメラの√N改善と異なる構造的な改善。',
        style='List Number'
    )
    doc.add_paragraph(
        '(2) 新しいクラスの天体発見: 高速移動 + 暗い + 近傍の小天体（10–50m級NEO）の検出。'
        'フレームカメラでは像の流れにより原理的に困難。',
        style='List Number'
    )
    doc.add_paragraph(
        '(3) 方法論の他分野への波及: カルシウムイメージング、工業検査、自動運転の悪条件センシングなどにも適用可能。',
        style='List Number'
    )

    # ======== Summary ========
    doc.add_heading('総括', level=1)
    doc.add_paragraph(
        '4ギャップの関係: g1（フォワードモデル逆問題化）→ g3（天文微弱天体検出）→ g4（全統合パイプライン）。'
        'g2は独立して進行可能であり、g1の理論的基礎が弱い場合のフォールバックとしても機能する。'
        'g4は最も野心的だが、LIGOの確立されたパイプラインをテンプレートとする点で方法論的リスクは限定的。'
    )

    # ======== References ========
    doc.add_heading('文献一覧', level=1)
    refs = [
        'Graca, R., Delbruck, T. (2023) "Optimal biasing and physical limits of DVS event noise" arXiv:2304.04019',
        'McReynolds, B., Graca, R., Delbruck, T. (2023) "Exploiting Alternating DVS Shot Noise Event Pair Statistics" arXiv:2304.03494',
        'Graca, R., Zhou, S., McReynolds, B., Delbruck, T. (2024) "SciDVS" ESSERC 2024',
        'Delbruck, T., Graca, R., Paluch, M. (2021) "Feedback Control of Event Cameras" CVPRW 2021',
        'Graca, R., Delbruck, T. (2025) "Towards a physically realistic computationally efficient DVS pixel model" arXiv:2505.07386',
        'Delbruck, T. (2008) "Frame-free dynamic digital vision" Proc. Intl. Symp. on Secure-Life Electronics',
        'Liu, S.-C., Delbruck, T. (2008) "Adaptive time-slice block-matching optical flow algorithm" BMVC',
        'Baldwin, R.W. et al. (2020) "Event Probability Mask (EPM) and EDnCNN" CVPR 2020',
        'Fang, H. et al. (2024) "Fast Window-Based Event Denoising" IEEE TPAMI',
        'Wu, W. et al. (2024) "ASTEDNet" ISPRS Archives XLVIII-4-2024',
        'Shiba, S., Aoki, Y., Gallego, G. (2025) "Simultaneous Motion And Noise Estimation with Event Cameras" ICCV 2025',
        'Afshar, S. et al. (2019) "Event-based Object Detection and Tracking for SSA" arXiv:1911.08730',
        'Chin, T.-J. et al. (2019) "Star Tracking Using an Event Camera" CVPRW 2019',
        'Joubert, D. et al. (2022) "FIESTA" Front. Neurosci. 16, 821157',
        'Gędek, M. et al. (2019) "Observational evaluation of event cameras" EESA',
        'Hoang, J. (2023) "Neuromorphic cameras for ACTs" arXiv:2310.16321',
        'Vajente, G. et al. (2020) "Machine-learning nonstationary noise out of GW detectors" Phys. Rev. D 101, 042003',
        'Dooney, T. et al. (2025) "DeepExtractor" arXiv:2501.18423',
        'Wang, H. et al. (2024) "WaveFormer" MLST 5, 015046',
        'Chatterjee, C., Jani, K. (2025) "No Glitch in the Matrix" ApJ',
        'Cao, R. et al. (2024) "Noise2Image" Optica (arXiv:2404.01298)',
        'Gallego, G. et al. (2020) "Event-based Vision: A Survey" IEEE TPAMI 42(1), 154–180',
        'Stetzler, S. et al. (2025) "An Efficient Shift-and-stack Algorithm" AJ 170, 352',
    ]
    for i, ref in enumerate(refs, 1):
        p = doc.add_paragraph()
        add_superscript_text(p, f'{{{i}}} {ref}')

    return doc


if __name__ == '__main__':
    doc = build_document()
    out = 'dvs_noise_inverse_problem_review.docx'
    doc.save(out)
    print(f'Saved: {out}')
