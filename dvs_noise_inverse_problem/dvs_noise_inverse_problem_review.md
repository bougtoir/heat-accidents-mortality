# DVS × ノイズ逆問題: 先行研究の体系的整理と未開拓領域の同定

## 背景

従来のノイズ除去は「信号の逆問題」（観測 = 信号 ⊛ PSF + ノイズ → 信号を解く）として定式化されてきた。
本レビューでは逆の発想——**ノイズの生成機構を物理モデルとして逆問題的に定式化し、ノイズを再構成・除去する**——をDynamic Vision Sensor (DVS) に適用する可能性を検討する。

DVSは各ピクセルが独立・非同期に輝度変化をイベントとして出力するニューロモルフィックセンサーであり、
昆虫の複眼における変化検出ニューロンを模倣した設計思想を持つ。
対数応答・高ダイナミックレンジ・マイクロ秒時間分解能という特性から、
天文観測や宇宙状況認識 (SSA) への応用が進んでいるが、
低照度条件下ではショットノイズに起因するバックグラウンドアクティビティ (BA) が支配的になる。

本文書では先行研究を4領域に分類し、その交差点にある**未開拓領域（ギャップ G1–G5）**を特定する。

---

## A. DVSノイズの物理モデリング（5件）

DVSピクセルの回路物理に基づくノイズ特性の理論的解明。UZH/ETH Zurich の Graça & Delbrück グループが中心。

| # | 文献 | 主な貢献 |
|---|------|---------|
| A1 | Graca, Delbruck (2023) "Optimal biasing and physical limits of DVS event noise" arXiv:2304.04019 | DVSフォトレセプタのショットノイズ限界を理論的に証明：**光子ノイズの2倍（2× photon shot noise）**が下限。バイアス最適化の指針を提示。 |
| A2 | McReynolds, Graca, Delbruck (2023) "Exploiting Alternating DVS Shot Noise Event Pair Statistics" arXiv:2304.03494 | ON/OFFイベントの交互出現統計を利用したノイズ識別。ショットノイズイベントはON→OFF（またはOFF→ON）の交互パターンを示すことを実証。 |
| A3 | Graca, Zhou, McReynolds, Delbruck (2024) "SciDVS: A Scientific Event Camera with 1.7% Temporal Contrast Sensitivity at 0.7 lux" ESSERC 2024 | 科学応用向けDVS。180nm CMOSで1.7%感度@0.7 lux。自動センタリングプリアンプ、帯域制御、ピクセルビニングの3つの新機能。 |
| A4 | Delbruck, Graca, Paluch (2021) "Feedback Control of Event Cameras" CVPRW 2021 | DVSの閾値・帯域・不応期をフィードバック制御する枠組み。ノイズ特性がバイアス設定に強く依存することを実証。 |
| A5 | Graca, Delbruck (2025) "Towards a physically realistic computationally efficient DVS pixel model" arXiv:2505.07386 | **大信号微分方程式ベースのDVSピクセルモデル。** First-passage-time理論に基づく確率的イベント生成機構を組み込み、従来手法の1000倍以上の効率で現実的なノイズ生成が可能。**ノイズ逆問題のフォワードモデルとして原理的に使用可能な段階。** |

**小括**: Graça–Delbrück グループの一連の研究により、DVSノイズの物理的生成機構は回路レベルで高精度にモデル化されつつある。特にA5のピクセルモデルは、ノイズ逆問題のフォワードモデル $\mathcal{F}(\theta)$ として直接利用できるポテンシャルを持つ。

---

## B. DVSノイズフィルタリング手法（7件）

経験的手法から確率的手法、さらに運動との同時推定へと進化。

| # | 文献 | 手法カテゴリ | 主な貢献 |
|---|------|-------------|---------|
| B1 | Delbruck (2008) "Frame-free dynamic digital vision" | 経験的 | 最初期の時空間近傍フィルタ。一定時間窓内に近傍ピクセルからイベントがなければノイズとして棄却。 |
| B2 | Liu, Delbruck (2008) "Adaptive time-slice block-matching optical flow" | 経験的 | オプティカルフローベースのフィルタリング。運動パターンに整合しないイベントを除去。 |
| B3 | Baldwin, Almatrafi, Asari, Hirakawa (2020) "Event Probability Mask (EPM) and EDnCNN" CVPR 2020 | 確率的 + DL | **Event Probability Mask**: 短時間窓内でのイベント生成確率を計算し、教師ラベルとして使用。最初の実世界ラベル付きDVSノイズデータセット DVSNOISE20 を提供。 |
| B4 | McReynolds, Graca, Delbruck (2023) arXiv:2304.03494 | 物理統計的 | ON/OFF交互統計によるフィルタリング（A2と同一論文）。物理モデルに基づく最初のフィルタ。 |
| B5 | Fang et al. (2024) "Fast Window-Based Event Denoising" IEEE TPAMI | DL | 窓ベースのイベントデノイジング。時間窓モジュール + ソフト空間特徴埋め込み (SSFE) による多スケールネットワーク WedNet。リアルタイム処理を実現。 |
| B6 | Wu et al. (2024) "ASTEDNet" ISPRS Archives | DL | 非同期時空間イベントデノイジングネットワーク。イベントストリームを直接処理し、フレーム変換を回避。 |
| B7 | **Shiba, Aoki, Gallego (2025) "Simultaneous Motion And Noise Estimation with Event Cameras" ICCV 2025** | 同時推定 | **概念的に最も近い先行研究。** Contrast Maximization枠組みを拡張し、運動推定とノイズ推定を同時に行う初の手法。E-MLBベンチマークでSOTA。ただし天文条件・回路物理モデル・補助チャンネルは未使用。 |

**小括**: B7 (Shiba et al.) は運動とノイズの同時推定という点で、ノイズ逆問題アプローチに概念的に最も近い。しかし、ノイズモデルは現象論的（データ駆動）であり、A5のような物理ベースのフォワードモデルとは統合されていない。

---

## C. DVSの天文・宇宙応用（5件）

DVSの高速・高ダイナミックレンジ特性を天文観測・宇宙状況認識 (SSA) に活用する研究。

| # | 文献 | 応用領域 | 主な貢献 |
|---|------|---------|---------|
| C1 | Afshar, Nicholson, van Schaik, Cohen (2019) "Event-based Object Detection and Tracking for Space Situational Awareness" arXiv:1911.08730 | SSA | **最初のイベントベース宇宙観測データセット**。236録画、572ラベル付き宇宙物体。検出・追跡アルゴリズムの比較評価。 |
| C2 | Chin, Bagchi, Eriksson, van Schaik (2019) "Star Tracking Using an Event Camera" CVPRW 2019 | 姿勢推定 | イベントカメラを用いた恒星追跡。回転平均化とバンドル調整の新定式化。イベントカメラ星追跡データセットを公開。 |
| C3 | Joubert, Afshar et al. (2022) "FIESTA: Real-Time Event-Based Unsupervised Feature Consolidation and Tracking for SSA" Front. Neurosci. | SSA | FIESTAアルゴリズム。教師なし・リアルタイム・少パラメータでの宇宙物体検出・追跡。 |
| C4 | Gędek, Żołnowski, Delbruck et al. (2019) "Observational evaluation of event cameras in optical space surveillance" EESA | SSA | DVS、DAVIS、ATISカメラの観測的評価。裏面照射DAVISと高感度DVSの初のSSA特性評価。昼間観測を含む。 |
| C5 | **Hoang (2023) "Neuromorphic cameras for Atmospheric Cherenkov Telescopes and fast optical astronomy" arXiv:2310.16321** | 高エネルギー天文学 | **大気チェレンコフ望遠鏡へのニューロモルフィックカメラ適用の展望。** ナノ秒スケールのチェレンコフ閃光検出にDVSの非同期・高速特性が有利。シミュレーションで有効性を示唆。 |

**小括**: DVSの天文応用は主にSSA（軌道上物体の検出・追跡）に集中している。C5のチェレンコフ望遠鏡応用は萌芽的。**微弱天体の検出（NEO、高速移動暗天体）にDVSを用いた研究は未だ存在しない。**

---

## D. 非DVS領域におけるノイズ逆問題アプローチ（7件）

信号ではなくノイズを逆問題として解く発想の先行事例。

| # | 文献 | 領域 | 主な貢献 |
|---|------|------|---------|
| D1 | **Vajente et al. (2020) "Machine-learning nonstationary noise out of gravitational-wave detectors" Phys. Rev. D 101, 042003** | 重力波 (LIGO) | **最も成功したノイズ逆問題の事例。** 補助センサー（ウィットネスチャンネル）で非定常ノイズ源を独立計測し、機械学習で主信号から差し引く。ノイズの物理的生成機構（地震、磁場、散乱光等）が既知であることを活用。 |
| D2 | Dooney et al. (2025) "DeepExtractor: Time-domain reconstruction of signals and glitches in GW data" arXiv:2501.18423 | 重力波 | ノイズ分布（ガウス・定常）をモデル化し、ノイズ成分を予測・差し引くことで信号/グリッチを復元するDLフレームワーク。 |
| D3 | Wang et al. (2024) "WaveFormer: transformer-based denoising for GW data" MLST 5, 015046 | 重力波 | Transformerベースのノイズ除去。ノイズとグリッチを1桁以上低減、位相誤差1%、振幅誤差7%。 |
| D4 | Chatterjee, Jani (2025) "No Glitch in the Matrix: Robust Reconstruction of GW Signals under Noise Artifacts" ApJ | 重力波 | グリッチ存在下でもロバストな信号再構成。ノイズアーティファクトの構造を学習して除去。 |
| D5 | **Cao, Galor, Kohli, Yates, Waller (2024) "Noise2Image: Noise-Enabled Static Scene Recovery for Event Cameras" Optica (arXiv:2404.01298)** | DVS + 計算イメージング | **DVSのノイズ逆問題に最も近い先行研究。** ノイズイベントの発生率が照度に依存することを利用し、静的シーンをノイズイベントのみから復元。「ノイズは情報を持つ」というパラダイム転換。 |
| D6 | **Essick et al. (2021) "iDQ: Statistical inference of non-astrophysical noise transients in gravitational-wave detectors" MLST 2, 015004** | 重力波 (LIGO) | **イベントごとのノイズ確率推定。** 補助チャンネル情報から各タイムスタンプにおける「そのイベントがノイズグリッチである確率」をリアルタイム出力。DVSの個別イベントノイズ分類への直接的な方法論的前例。 |
| D7 | **Selig, Enßlin (2015) "D3PO – Denoising, Deconvolving, and Decomposing Photon Observations" A&A 574, A74** | 天文画像 | **ノイズ・信号の同時ベイズ再構成。** フォトン計数データに対し、信号（点源＋拡散成分）とノイズを同時にベイズ推定。情報場理論に基づく非パラメトリック手法。DVSイベントストリームのベイズ分解への理論的前例。 |

**小括**: LIGO (D1–D4, D6) では「ノイズの物理モデル + 補助チャンネル → ノイズ再構成・差し引き」というパイプラインが確立済み。特にDeepClean (D1) の補助チャンネル回帰とiDQ (D6) のイベントレベルノイズ確率推定は、DVSへの方法論的移植の核となる。D5 (Noise2Image) はDVSノイズの情報的価値を初めて実証。D7 (D3PO) はフォトン計数データの信号/ノイズ同時ベイズ再構成を示し、DVSイベントストリームへの拡張可能性を持つ。手法のテンプレートは成熟している。

---

## E. 特定されたギャップ（5つ）

4領域（A–D）の交差点分析から、以下の5つの未開拓領域（ギャップ）を特定した（Fig. 1）。

| ギャップ | 内容 | 関連領域 |
|---------|------|---------|
| G1 | DVS回路物理からの厳密なベイズ逆問題定式化が未存在 | A→D |
| G2 | LIGO DeepClean的な「補助チャンネルからのDVSノイズ予測」が未検討 | D→A |
| G3 | 天文特化のDVSノイズ逆問題パイプラインが未存在 | A+B+D→C |
| G4 | 「信号の形態に仮定を置かない」天体検出（ノイズを解いて残差から発見）が天文で未検討 | C+D統合 |
| G5 | SciDVS＋大口径望遠鏡＋ノイズ逆問題の統合実証がない | A+C+D実証 |

**G3とG4が最も探索価値の高い未開拓領域である。必要なピースはすべて揃っており、統合されていないだけという状況にある。**

---

### G1: DVS回路物理からの厳密なベイズ逆問題定式化

**現状**: A5 (Graca & Delbruck 2025) がDVSピクセルの物理的に現実的なフォワードモデルを確立した。First-passage-time理論に基づくイベント生成モデルは精密だが、これは**フォワード方向**（パラメータ→ノイズイベント生成）としてのみ使用されている。**ベイズ逆問題**（観測イベントストリーム + 事前分布 → ノイズパラメータの事後分布推定）としての定式化は存在しない。

**ギャップの本質**: D7 (D3PO) はフォトン計数データに対して信号とノイズの同時ベイズ推定を実現しているが、DVSイベントストリームに対する同等の定式化がない。

**提案する定式化**:

- フォワードモデル: $e_{\text{noise}} = \mathcal{F}(\theta_{\text{pixel}}, I_{\text{bg}}, T, \text{bias})$
  - $\theta_{\text{pixel}}$: ピクセル固有パラメータ（閾値ミスマッチ $\sigma_\theta$、暗電流、リーク電流等）
  - $I_{\text{bg}}$: 背景照度, $T$: 温度, bias: バイアス電流設定
- ベイズ逆問題:
  - 事前分布: $p(\theta)$ — A5の物理モデルが提供するパラメータ範囲から構成
  - 尤度: $p(e_{\text{obs}} | \theta)$ — 非一様ポアソン過程尤度
  - 事後分布: $p(\theta | e_{\text{obs}}) \propto p(e_{\text{obs}} | \theta) \cdot p(\theta)$
- D3PO (D7) 的拡張 — 信号 $s$ とノイズパラメータ $\theta$ の同時推定:
  - $p(\theta, s | e_{\text{obs}}) \propto p(e_{\text{obs}} | \theta, s) \cdot p(\theta) \cdot p(s)$
  - 情報場理論に基づく非パラメトリック事前分布の適用可能性

**必要な研究**: A5モデルの微分可能な実装、イベントストリームに対する適切な尤度関数の設計（点過程尤度）、変分推論またはMCMCによる効率的な事後推定アルゴリズム。

---

### G2: LIGO DeepClean的な「補助チャンネルからのDVSノイズ予測」

**現状**: D1 (DeepClean) はLIGO重力波検出器において、補助センサー（ウィットネスチャンネル: 加速度計、磁力計、マイクロフォン等）からの情報を用いて非定常ノイズを学習・予測・差し引くことに成功した。D6 (iDQ) はさらに進んで、個々のイベント（グリッチ）が天体物理起源でない確率をリアルタイム出力する。**DVSに対してこのアプローチを適用した研究は存在しない。**

**ギャップの本質**: DVSのノイズは温度・振動・背景照度等の環境条件に強く依存することが知られているが（A1, A2）、これらを「補助チャンネル」として独立計測し、ノイズ予測に活用するシステムは未構築。

**DVSにおける補助チャンネルの設計** (D1のLIGOアーキテクチャに倣う):

| LIGO補助チャンネル | DVS対応 | ノイズ寄与 |
|-----------------|---------|----------|
| 加速度計（地震ノイズ） | 加速度計（マイクロフォニックノイズ） | 機械振動→電気ノイズ変換 |
| 磁力計（磁場ノイズ） | 温度センサー | 暗電流 $I_{\text{dark}} \propto \exp(-E_g/2k_BT)$ |
| マイクロフォン（音響ノイズ） | 背景照度モニタ（フォトダイオード） | ショットノイズレート $\propto I_{\text{bg}}$ |
| 散乱光モニタ | 電源電圧モニタ | 電源リプルによるノイズ |

**iDQ (D6) 的拡張**: 各DVSイベントに対し「そのイベントがノイズ起源である確率」$P_{\text{noise}}(e_i | \text{aux})$ を補助チャンネル情報から推定。バイナリな閾値ベース除去ではなく、確率的重み付けによるソフトな除去が可能になる。

**必要な研究**: 補助チャンネルシステムの設計・構築、DeepClean的NN（補助チャンネル→ノイズイベントレート予測）のDVS版アーキテクチャ、iDQ的イベントレベルノイズ確率推定器の実装。

---

### G3: 天文特化のDVSノイズ逆問題パイプライン

**現状**: G1（ベイズ逆問題定式化）とG2（補助チャンネルノイズ予測）の構成要素は個別に先行研究で示されているが、これらを**天文観測に特化して統合したパイプライン**は存在しない。C1–C5のDVS天文応用は閾値ベースの単純なノイズ除去に留まっており、物理モデルベースのノイズ逆問題アプローチを取り入れていない。

**ギャップの本質**: LIGOでは「ノイズの物理モデル + 補助チャンネル → ノイズ再構成・差し引き」のパイプラインが確立済み（D1–D4, D6）。同じ設計哲学をDVS天文観測に移植するだけであり、原理的な障壁はない。**ピースはすべて揃っており、統合されていないだけ。**

#### G3パイプラインのシステムアーキテクチャ（Fig. 2）

```
┌──────────────────────────────────────────────────────────────────────────┐
│              G3: 天文特化DVSノイズ逆問題パイプライン                        │
│                                                                          │
│  入力層                                                                   │
│  ┌──────────────┐  ┌────────────────┐  ┌──────────────┐                  │
│  │ DVS主チャンネル │  │ 補助チャンネル    │  │ 物理モデル    │                  │
│  │ e(t,x,y,p)   │  │ T(t),a(t),I(t)│  │ A5ピクセル    │                  │
│  └──────┬───────┘  └───────┬────────┘  └──────┬───────┘                  │
│         │                  │                   │                          │
│  Stage 1: ノイズフォワードモデル構築                                        │
│  ┌──────────────────────────────────────────────────────────────────┐     │
│  │ λ_noise(x,y,t) = F(θ_pixel, T(t), bias, I_bg(x,y,t))          │     │
│  │ 各ピクセルの期待ノイズレートを物理モデル(A5)+補助チャンネルで計算     │     │
│  └──────────────────────────────┬───────────────────────────────────┘     │
│                                 │                                         │
│  Stage 2: ベイズ逆問題求解 (G1)                                            │
│  ┌──────────────────────────────────────────────────────────────────┐     │
│  │ p(θ|e_obs) ∝ p(e_obs|θ)·p(θ)                                   │     │
│  │ + DeepClean型NN (G2) で非定常結合を学習                            │     │
│  │ + iDQ的イベントレベルノイズ確率 P_noise(e_i)                       │     │
│  └──────────────────────────────┬───────────────────────────────────┘     │
│                                 │                                         │
│  Stage 3: 残差イベントストリーム生成                                        │
│  ┌──────────────────────────────────────────────────────────────────┐     │
│  │ e_residual = e_obs ⊖ F(θ̂)                                      │     │
│  │ 手法: 確率的薄化 / レート引き算 / マーク付き点過程差分              │     │
│  └──────────────────────────────┬───────────────────────────────────┘     │
│                                 │                                         │
│  Stage 4: 天文校正・検証                                                   │
│  ┌──────────────────────────────────────────────────────────────────┐     │
│  │ PSD検証 / 注入・回収テスト / 既知天体テスト / ブラインドテスト      │     │
│  └──────────────────────────────────────────────────────────────────┘     │
│                                                                          │
│  出力: 天文解析用クリーンイベントストリーム                                  │
└──────────────────────────────────────────────────────────────────────────┘
```

#### G3の各ステージの詳細

##### Stage 1: ノイズフォワードモデル構築

A5 (Graca & Delbruck 2025) の大信号微分方程式モデルを基盤とする。

**DVSピクセルのノイズ生成機構**:
- フォトレセプタの対数応答: $V_{\text{pr}} = V_T \ln(I_{\text{photo}} / I_0)$
- 差分増幅器: $\Delta V = V_{\text{pr}}(t) - V_{\text{pr}}(t_{\text{last}})$
- コンパレータ: $|\Delta V| > \theta$ のとき ON/OFF イベントを発火
- ノイズ源:
  - **ショットノイズ**: $\sigma_{\text{shot}}^2 = 2qI_{\text{photo}} \cdot \text{BW}$ （BWは帯域幅）
  - **熱ノイズ**: $\sigma_{\text{thermal}}^2 = 4k_B T / R \cdot \text{BW}$
  - **ミスマッチ**: ピクセル間の閾値バラツキ $\sigma_\theta$

A5はこれらを微分方程式として統合し、first-passage-time理論でイベント生成をモデル化:
$$\tau_{\text{event}} \sim \text{InverseGaussian}\left(\frac{\theta}{\mu_{\text{drift}}}, \frac{\theta^2}{\sigma_{\text{diff}}^2}\right)$$

**天文条件での拡張要件**:
- 極低照度: $I_{\text{bg}} < 0.1$ lux（暗天条件）での暗電流支配領域のモデル精度検証
- 長時間運用: 温度ドリフト・経年変化の影響のモデル化
- 大口径望遠鏡: 大きなイメージサークルに対するピクセル間特性バラツキの統計的扱い

**補助チャンネルによる拡張** (G2, LIGO D1 に倣う):
- **温度センサー**: 暗電流は温度に指数関数的に依存。$I_{\text{dark}} \propto \exp(-E_g / 2k_B T)$。温度1°C上昇で暗電流は約2倍。リアルタイム温度計測でノイズレートを予測。
- **振動センサー（加速度計）**: マイクロフォニックノイズ（機械振動→電気ノイズ変換）の検出。望遠鏡のドーム回転、風揺れ等に対応。
- **背景照度モニタ**: フレームカメラまたはフォトダイオードで背景光度を独立計測。光害、月明かり、薄明の影響をモデルに入力。

##### Stage 2: ベイズ逆問題求解

G1の定式化を実装に落とし込む。3つのアプローチを統合的に使用:

**(a) 最尤推定 (MLE)**:
- イベントストリームを非一様ポアソン過程としてモデル化。
- レート関数: $\lambda(x,y,t) = \lambda_{\text{signal}}(x,y,t) + \lambda_{\text{noise}}(x,y,t;\theta)$
- 尤度: $\mathcal{L}(\theta) = \prod_{i} \lambda(x_i,y_i,t_i;\theta) \cdot \exp\left(-\int \lambda(x,y,t;\theta) \, dx \, dy \, dt\right)$
- EM的求解（信号部分を潜在変数として扱う）。

**(b) 変分推論** (D3PO (D7) 的アプローチ):
- ノイズパラメータ $\theta$ と信号 $s$ を同時に推定。
- ELBO: $\mathbb{E}_{q(\theta,s)}[\log p(e_{\text{obs}}|\theta,s)] - \text{KL}(q(\theta,s) \| p(\theta,s))$
- 物理モデル A5 が事前分布 $p(\theta)$ を提供。

**(c) DeepClean型NN** (G2の成果を統合):
- D1 (Vajente et al.) に倣い、補助チャンネル → ノイズイベント予測のNNを学習。
- 入力: 補助チャンネル時系列 $[T(t), a(t), I_{\text{bg}}(t)]$
- 出力: 各ピクセルの期待ノイズイベントレート $\hat{\lambda}_{\text{noise}}(x,y,t)$
- 物理モデル A5 がアーキテクチャの帰納的バイアスと初期化を提供（Physics-Informed Neural Network的）。
- D6 (iDQ) 的なイベントレベルノイズ確率出力を統合。

**推奨**: (c) を実用基盤とし、(b) で理論的正当性を担保。物理モデルをNNの構造的制約として埋め込む (Physics-Informed) ことで、データ効率と解釈可能性を両立。

##### Stage 3: 残差イベントストリーム生成

DVSイベントは $(t_i, x_i, y_i, p_i)$ の4タプル。ノイズイベントの「引き算」は自明ではない。

**提案する3つの手法**:

1. **確率的薄化 (Probabilistic Thinning)**:
   - 各イベントに対し、ノイズモデルから計算した「そのイベントがノイズである確率」 $P_{\text{noise}}(e_i)$ を付与（iDQ (D6) の方法論を移植）。
   - $P_{\text{noise}}(e_i)$ に基づいて確率的に棄却。
   - 利点: 計算が軽い。欠点: 個々のイベントレベルでの判定精度に限界。

2. **レート引き算 (Rate Subtraction)**:
   - 時空間ビン $(x,y,t)$ 内のイベント数から、ノイズモデルの期待イベント数を差し引き。
   - $n_{\text{residual}}(x,y,\Delta t) = n_{\text{obs}}(x,y,\Delta t) - \hat{\lambda}_{\text{noise}}(x,y) \cdot \Delta t$
   - 利点: 統計的に頑健。欠点: 時間分解能がビン幅に依存。

3. **マーク付き点過程の差分 (Marked Point Process Subtraction)**:
   - ノイズモデルからシミュレートしたイベントストリームを生成し、観測ストリームとマッチング。
   - 最近傍マッチング（時空間距離）でペアリングし、マッチしたイベントを除去。
   - 利点: 最も原理的。欠点: 計算量大、マッチング基準の設計が困難。

**推奨**: 通常はレート引き算 (2) を使用し、候補検出後の確認フェーズで確率的薄化 (1) を適用。

##### Stage 4: 天文校正・検証

LIGO (D1) の検証方法論を移植:

1. **パワースペクトル密度 (PSD) テスト**: ノイズ差し引き前後のイベントレートPSDを比較。差し引き後のPSDが理論的な白色ポアソン + 1/f 成分に一致するか。
2. **注入・回収テスト (Injection-Recovery)**: 既知の模擬天体信号をノイズ差し引き前のストリームに注入し、パイプライン通過後に正しく回収できるか。回収効率と偽検出率のROC曲線を評価。
3. **既知天体テスト**: カタログ天体（等級が既知）の再検出率。検出限界等級の測定。
4. **ブラインドテスト**: 注入信号の有無を隠した状態での解析者の判定。

#### G3の先行研究との差分

| 手法 | ノイズモデル | 補助チャンネル | 天文対応 | ベイズ定式化 |
|------|-------------|-------------|---------|------------|
| Shiba et al. (B7) | データ駆動 | × | × | × |
| Noise2Image (D5) | 照度依存 | × | × | × |
| FIESTA (C3) | 閾値ベース | × | ○ | × |
| DeepClean (D1) | 物理+ML | ○ | ×（LIGO） | × |
| D3PO (D7) | ベイズ | × | ○（γ線） | ○ |
| **G3提案** | **物理モデル(A5)+ML** | **○** | **○** | **○** |

#### G3の研究課題

| 課題 | 内容 | 難易度 | 依存関係 |
|------|------|--------|---------|
| G3-a | A5モデルの天文条件（極低照度、長時間運用）への拡張・検証 | 中 | G1 |
| G3-b | 補助チャンネルシステムの天文台向け設計・構築 | 高 | G2 |
| G3-c | DeepClean型NN + iDQ的確率推定のDVS版実装 | 中 | G1, G2 |
| G3-d | イベントストリーム差分演算の理論的基礎と実装 | 高 | G3-c |
| G3-e | 注入・回収テストフレームワーク構築 | 中 | G3-d |
| G3-f | SciDVS (A3) + 小口径望遠鏡での概念実証観測 | 高 | G3-a〜e |

---

### G4: 「信号の形態に仮定を置かない」天体検出 — ノイズを解いて残差から発見

**現状**: 天文学における天体検出は伝統的に「信号のテンプレート」を前提とする。重力波検出ではマッチドフィルタリング（波形テンプレートとの相関）、可視光天文学ではPSFフィッティング・SExtractor等のモデルベース検出が標準。DVS天文学でも、C1–C5は「十分に明るい天体」の検出に限定されており、検出の前提として信号が一定の強度・形態を持つことを暗黙に仮定している。

**ギャップの本質**: 「信号がどのような形態をしているか分からない」場合にも天体を検出できる枠組みが天文で未検討。**ノイズを精密に解く（G3パイプライン）ことで、残差に構造が見えれば、それが信号である**——という逆転の発想。信号のモデルを一切必要とせず、ノイズモデルの精度だけが検出感度を決定する。

#### G4のパラダイムシフト: テンプレート依存 vs テンプレートフリー

| 項目 | 従来アプローチ | G4アプローチ |
|------|-------------|------------|
| 検出原理 | 信号テンプレートとのマッチング | ノイズモデルからの逸脱検出 |
| 前提知識 | 信号の形態・スペクトルが既知 | ノイズの生成機構が既知 |
| 検出対象 | 既知タイプの天体のみ | 未知タイプの天体も含む |
| 感度決定要因 | テンプレートの正確さ | ノイズモデルの精度 |
| LIGO対応 | マッチドフィルタリング | バースト探索 (unmodeled search) |
| 弱点 | 未知信号への盲目 | ノイズの体系的誤差に脆弱 |

**LIGO分野でのアナロジー**: LIGOにおいてもテンプレートフリー探索（unmodeled burst search）は重要な探索カテゴリであり、cWB (coherent WaveBurst) 等のアルゴリズムが開発されている。G4はこの発想をDVS天文学に移植する。

#### G4の検出アルゴリズム

G3パイプラインが出力する**残差イベントストリーム**に対して、以下の手順で天体候補を検出する。

**ステップ1: 残差の統計的特性化**
- ノイズ差し引きが完全であれば、残差はポアソン過程（ランダム）に従う。
- 残差の時空間統計がポアソンから逸脱する領域を検出 → 信号候補。

**ステップ2: 微弱天体のためのイベントレベル shift-and-stack**
- 候補軌道パラメータ $(v_x, v_y)$ に沿って残差イベントを時空間的にシフトし累積。
- CMax (Contrast Maximization; Gallego et al. [22]) 枠組みの自然な拡張。
- ノイズモデル引き算済みのため、フレームベースshift-and-stack (Stetzler et al. [23]) より偽検出率が大幅に低い。
- **テンプレートフリーの核心**: shift-and-stackのパラメータは軌道（運動方向・速度）のみであり、天体の明るさ・スペクトル・形態に関する仮定は不要。

**ステップ3: 統計的有意性の評価**
- 残差ストリームでのイベント累積がポアソンノイズの期待値を有意に超えるか検定。
- ノイズの統計的性質が既知（G3 Stage 2出力）であるため、FAR (False Alarm Rate) の理論的計算が可能。
- 多重検定補正（Bonferroni or BH-FDR）を適用。

**ステップ4: テンプレートフリー候補の特性化**
- 検出された候補の時空間プロファイルを抽出。
- 既知天体カタログとのクロスマッチ。
- 未知天体の場合: 軌道要素の初期推定、フォローアップ観測計画の生成。

**ステップ5: 物理的検証**
- 候補のイベント統計が物理的に妥当か（光度曲線の一貫性、軌道力学との整合性）。
- 独立な観測手段（フレームカメラ、レーダー等）での確認。

#### G4の LIGO → DVS 対応表

| LIGO要素 | DVS対応 | 状態 |
|---------|---------|------|
| 主チャンネル（ひずみデータ） | DVSイベントストリーム | 利用可能 |
| 補助チャンネル（加速度計等） | 温度・振動・照度センサー | **要構築** (G2) |
| ノイズ物理モデル | A5 DVSピクセルモデル | 利用可能（天文条件未検証） |
| DeepClean（非定常ノイズ学習） | DeepClean的NN | **要開発** (G2) |
| マッチドフィルタリング（テンプレート探索） | — | **不使用**（G4の核心） |
| バースト探索（テンプレートフリー） | 残差統計逸脱検出 + shift-and-stack | **要開発** |
| 信号注入テスト | 模擬天体注入テスト | **要設計** (G3 Stage 4) |

#### G4の研究課題

| 課題 | 内容 | 難易度 | 依存関係 |
|------|------|--------|---------|
| G4-a | テンプレートフリー検出の理論的基礎（残差統計からの逸脱検出の最適化） | 高 | G3 |
| G4-b | イベントレベル shift-and-stack アルゴリズムの設計と計算量評価 | 中 | G3 |
| G4-c | 多重検定問題への対処（探索パラメータ空間の効率的探索） | 中 | G4-a |
| G4-d | 未知天体候補の自動分類・特性化パイプライン | 中 | G4-b |
| G4-e | シミュレーションによるテンプレートフリー検出の感度評価 | 中 | G4-a, G4-b |

#### G4の期待されるインパクト

1. **検出限界の拡張**: ノイズ逆問題 + テンプレートフリー検出により、DVSの検出限界等級を2–4等級改善する可能性。フレームカメラの√N改善（スタッキング枚数Nに対して）と異なる、**構造的な改善**。
2. **新しいクラスの天体発見**: 高速移動 + 暗い + 近傍の小天体（10–50m級NEO）。フレームカメラでは像の流れにより原理的に検出困難。
3. **未知現象の発見可能性**: テンプレートフリーであるため、予期しない天文現象（高速光学トランジェント等）の発見にも感度を持つ。
4. **方法論の他分野への波及**: DVSノイズ逆問題のフレームワークは、神経カルシウムイメージング、工業検査（微弱欠陥検出）、自動運転の悪条件センシング等にも適用可能。

---

### G5: SciDVS＋大口径望遠鏡＋ノイズ逆問題の統合実証

**現状**: SciDVS (A3) は1.7%の時間的コントラスト感度を実現した科学用DVSであり、天文応用のハードウェア基盤として最も有望。しかし、SciDVSを**大口径望遠鏡に搭載し、G3/G4のノイズ逆問題パイプラインと組み合わせた統合実証**は存在しない。

**ギャップの本質**: G1–G4の理論・アルゴリズムが完成しても、実際の天文台環境での実証がなければ手法の実用性は検証されない。

**統合実証のロードマップ**:

| 段階 | 内容 | 望遠鏡口径 | 目標 |
|------|------|----------|------|
| Phase 1 | SciDVS + 小口径望遠鏡 (0.3–0.5m) | 小 | パイプラインの動作検証、既知天体再検出 |
| Phase 2 | SciDVS + 中口径望遠鏡 (1–2m) | 中 | 微弱天体検出限界の実測、ノイズモデル精度評価 |
| Phase 3 | SciDVS + 大口径望遠鏡 (4m級) | 大 | G4テンプレートフリー検出の実証、新天体候補の探索 |

**技術的課題**:
- 大口径望遠鏡のイメージサークルに対するDVSの画素数制約
- 望遠鏡の追尾誤差がDVSイベントに与える影響の定量化
- 天文台環境（温度変動、振動、光害）での補助チャンネルシステム (G2) の実装
- 長時間観測（数時間〜一晩）でのシステム安定性

---

## 総括: 5ギャップの関係性と優先順位

```
  G1 (ベイズ逆問題定式化)  G2 (補助チャンネルノイズ予測)
       │                       │
       └───────────┬───────────┘
                   ▼
           G3 (天文パイプライン統合)  ←─ G1 + G2 + LIGO テンプレート
                   │
                   ▼
           G4 (テンプレートフリー検出) ←─ G3残差からの発見
                   │
                   ▼
           G5 (大口径望遠鏡実証)     ←─ G3 + G4 + SciDVS
```

**優先順位**:
- **G1, G2**: 基盤研究。並行して進行可能。G1はA5モデルのベイズ逆問題拡張、G2はLIGO D1/D6の方法論移植。
- **G3**: G1+G2の成果を天文パイプラインとして統合。**最も探索価値が高い**——必要なピースはすべて揃っており、統合されていないだけ。
- **G4**: G3パイプラインの残差を入力としたテンプレートフリー検出。G3と並行して概念設計可能。**G3と並び最も探索価値が高い。**
- **G5**: G3+G4の成果を実望遠鏡で実証。最も野心的だが、G3/G4の成果に依存。

---

## 文献一覧（出現順）

1. Graca, R., Delbruck, T. (2023) "Optimal biasing and physical limits of DVS event noise" arXiv:2304.04019
2. McReynolds, B., Graca, R., Delbruck, T. (2023) "Exploiting Alternating DVS Shot Noise Event Pair Statistics to Reduce Background Activity Rates" arXiv:2304.03494
3. Graca, R., Zhou, S., McReynolds, B., Delbruck, T. (2024) "SciDVS: A Scientific Event Camera with 1.7% Temporal Contrast Sensitivity at 0.7 lux" ESSERC 2024. DOI:10.1109/esserc62670.2024.10719521
4. Delbruck, T., Graca, R., Paluch, M. (2021) "Feedback Control of Event Cameras" CVPRW 2021
5. Graca, R., Delbruck, T. (2025) "Towards a physically realistic computationally efficient DVS pixel model" arXiv:2505.07386
6. Delbruck, T. (2008) "Frame-free dynamic digital vision" Proc. Intl. Symp. on Secure-Life Electronics
7. Liu, S.-C., Delbruck, T. (2008) "Adaptive time-slice block-matching optical flow algorithm for dynamic vision sensors" BMVC
8. Baldwin, R.W., Almatrafi, M., Asari, V., Hirakawa, K. (2020) "Event Probability Mask (EPM) and Event Denoising Convolutional Neural Network (EDnCNN) for Neuromorphic Cameras" CVPR 2020
9. Fang, H., Wu, J., Hou, Q., Dong, W., Shi, G. (2024) "Fast Window-Based Event Denoising with Spatiotemporal Correlation Enhancement" IEEE TPAMI
10. Wu, W., Yao, H., Zhai, C., Dai, Z., Zhu, X. (2024) "Event Camera Denoising Using Asynchronous Spatio-Temporal Event Denoising Neural Network" ISPRS Archives XLVIII-4-2024
11. Shiba, S., Aoki, Y., Gallego, G. (2025) "Simultaneous Motion And Noise Estimation with Event Cameras" ICCV 2025
12. Afshar, S., Nicholson, A.P., van Schaik, A., Cohen, G. (2019) "Event-based Object Detection and Tracking for Space Situational Awareness" arXiv:1911.08730
13. Chin, T.-J., Bagchi, S., Eriksson, A., van Schaik, A. (2019) "Star Tracking Using an Event Camera" CVPRW 2019
14. Joubert, D., Afshar, S., et al. (2022) "FIESTA: Real-Time Event-Based Unsupervised Feature Consolidation and Tracking for Space Situational Awareness" Front. Neurosci. 16, 821157
15. Gędek, M., Żołnowski, M., Delbruck, T., et al. (2019) "Observational evaluation of event cameras performance in optical space surveillance" EESA
16. Hoang, J. (2023) "Neuromorphic cameras for Atmospheric Cherenkov Telescopes and fast optical astronomy" arXiv:2310.16321
17. Vajente, G., Huang, Y., Isi, M., et al. (2020) "Machine-learning nonstationary noise out of gravitational-wave detectors" Phys. Rev. D 101, 042003
18. Dooney, T., Narola, H., et al. (2025) "DeepExtractor: Time-domain reconstruction of signals and glitches in gravitational wave data with deep learning" arXiv:2501.18423
19. Wang, H., Zhou, Y., Cao, Z., et al. (2024) "WaveFormer: transformer-based denoising method for gravitational-wave data" MLST 5, 015046
20. Chatterjee, C., Jani, K. (2025) "No Glitch in the Matrix: Robust Reconstruction of Gravitational Wave Signals under Noise Artifacts" ApJ
21. Cao, R., Galor, D., Kohli, A., Yates, J.L., Waller, L. (2024) "Noise2Image: Noise-Enabled Static Scene Recovery for Event Cameras" Optica (arXiv:2404.01298)
22. Gallego, G., et al. (2020) "Event-based Vision: A Survey" IEEE TPAMI 42(1), 154–180
23. Stetzler, S., Jurić, M., et al. (2025) "An Efficient Shift-and-stack Algorithm Applied to Detection Catalogs" AJ 170, 352
24. Essick, R., Godwin, P., Hanna, C., et al. (2021) "iDQ: Statistical inference of non-astrophysical noise transients in gravitational-wave detectors" MLST 2, 015004
25. Selig, M., Enßlin, T.A. (2015) "D3PO – Denoising, Deconvolving, and Decomposing Photon Observations" A&A 574, A74
