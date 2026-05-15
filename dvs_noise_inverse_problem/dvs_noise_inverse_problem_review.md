# DVS × ノイズ逆問題: 先行研究の体系的整理と未開拓領域の同定

## 背景

従来のノイズ除去は「信号の逆問題」（観測 = 信号 ⊛ PSF + ノイズ → 信号を解く）として定式化されてきた。
本レビューでは逆の発想——**ノイズの生成機構を物理モデルとして逆問題的に定式化し、ノイズを再構成・除去する**——をDynamic Vision Sensor (DVS) に適用する可能性を検討する。

DVSは各ピクセルが独立・非同期に輝度変化をイベントとして出力するニューロモルフィックセンサーであり、
昆虫の複眼における変化検出ニューロンを模倣した設計思想を持つ。
対数応答・高ダイナミックレンジ・マイクロ秒時間分解能という特性から、
天文観測や宇宙状況認識 (SSA) への応用が進んでいるが、
低照度条件下ではショットノイズに起因するバックグラウンドアクティビティ (BA) が支配的になる。

本文書では先行研究を4領域に分類し、その交差点にある**未開拓領域（ギャップ g1–g4）**を特定する。

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

## D. 非DVS領域におけるノイズ逆問題アプローチ（5件）

信号ではなくノイズを逆問題として解く発想の先行事例。

| # | 文献 | 領域 | 主な貢献 |
|---|------|------|---------|
| D1 | **Vajente et al. (2020) "Machine-learning nonstationary noise out of gravitational-wave detectors" Phys. Rev. D 101, 042003** | 重力波 (LIGO) | **最も成功したノイズ逆問題の事例。** 補助センサー（ウィットネスチャンネル）で非定常ノイズ源を独立計測し、機械学習で主信号から差し引く。ノイズの物理的生成機構（地震、磁場、散乱光等）が既知であることを活用。 |
| D2 | Dooney et al. (2025) "DeepExtractor: Time-domain reconstruction of signals and glitches in GW data" arXiv:2501.18423 | 重力波 | ノイズ分布（ガウス・定常）をモデル化し、ノイズ成分を予測・差し引くことで信号/グリッチを復元するDLフレームワーク。 |
| D3 | Wang et al. (2024) "WaveFormer: transformer-based denoising for GW data" MLST 5, 015046 | 重力波 | Transformerベースのノイズ除去。ノイズとグリッチを1桁以上低減、位相誤差1%、振幅誤差7%。 |
| D4 | Chatterjee, Jani (2025) "No Glitch in the Matrix: Robust Reconstruction of GW Signals under Noise Artifacts" ApJ | 重力波 | グリッチ存在下でもロバストな信号再構成。ノイズアーティファクトの構造を学習して除去。 |
| D5 | **Cao, Galor, Kohli, Yates, Waller (2024) "Noise2Image: Noise-Enabled Static Scene Recovery for Event Cameras" Optica (arXiv:2404.01298)** | DVS + 計算イメージング | **DVSのノイズ逆問題に最も近い先行研究。** ノイズイベントの発生率が照度に依存することを利用し、静的シーンをノイズイベントのみから復元。「ノイズは情報を持つ」というパラダイム転換。 |

**小括**: LIGO (D1–D4) では「ノイズの物理モデル + 補助チャンネル → ノイズ再構成・差し引き」というパイプラインが確立済み。D5 (Noise2Image) はDVSノイズの情報的価値を初めて実証したが、動的シーン・天文条件への拡張は未検討。

---

## 未開拓領域（ギャップ）の同定

4領域の交差から、以下の4つのギャップを特定する。

### g1: 物理ベースDVSノイズフォワードモデルの逆問題定式化（A→D ブリッジ）

**現状**: A5 (Graca & Delbruck 2025) が物理的に現実的なDVSピクセルモデルを報告。しかしこれは**フォワードモデル**（パラメータ→ノイズイベント生成）としてのみ使用されており、**逆問題**（観測されたイベントストリーム→ノイズパラメータ推定→ノイズ除去）としては定式化されていない。

**提案**: A5のfirst-passage-time理論ベースのモデルを逆問題として定式化する。
- フォワードモデル: $e_{\text{noise}} = \mathcal{F}(\theta_{\text{pixel}}, I_{\text{bg}}, T, \text{bias})$
  - $\theta_{\text{pixel}}$: ピクセル固有パラメータ（閾値ミスマッチ、暗電流等）
  - $I_{\text{bg}}$: 背景照度
  - $T$: 温度
  - bias: ユーザー設定バイアス電流
- 逆問題: $\hat{\theta} = \arg\min_\theta \| e_{\text{obs}} - \mathcal{F}(\theta) \|$ （適切な距離関数を定義）
- ノイズ除去: $e_{\text{signal}} = e_{\text{obs}} - \mathcal{F}(\hat{\theta})$

**必要な研究**: フォワードモデルの微分可能な実装、適切な距離関数の設計（イベントストリームは点過程であるため、通常の $L_2$ ノルムは不適切）、計算効率の確保。

---

### g2: 自己教師ありノイズ学習によるDVSデノイジング（B→D ブリッジ）

**現状**: B3 (EPM) は統計的ラベル生成、B7 (Shiba et al.) は運動とノイズの同時推定を行うが、いずれもノイズの物理モデルを内包していない。D5 (Noise2Image) はノイズの照度依存性を利用するが、動的シーンには未対応。

**提案**: Noise2Noise / Noise2Image の枠組みをDVSの動的シーンに拡張する。
- DVSの時間的冗長性を活用: 同一ピクセルからの連続ノイズイベント列を「ペア」としてNoise2Noise学習。
- A2/B4のON/OFF交互統計をペア生成の物理的根拠として使用。
- D5の照度依存ノイズモデルを動的シーンの「静的背景成分」推定に拡張。

---

### g3: DVS × ノイズ逆問題による天文学的微弱天体検出（A+B+C 統合）

**現状**: C1–C5のDVS天文応用は、すべて「十分に明るい」天体（恒星、衛星等）の検出・追跡に限られている。**微弱天体（暗いNEO、高速移動小天体など）のDVS検出は未踏。** 従来のフレームカメラではshift-and-stack（フレーム合成）が使われるが、DVSのイベントストリームに対する等価な手法は確立されていない。

**提案**: ノイズ逆問題アプローチによる微弱天体のDVS検出パイプライン。

#### g3の問題構造

微弱天体のDVS検出における根本的困難:

1. **信号がノイズ以下**: 微弱天体からのイベントレートがバックグラウンドノイズイベントレートを下回る。
2. **非定常性**: 天体は移動するため、単一ピクセルでの時間積分が困難。
3. **テンプレート不在**: 検出すべき天体の軌道パラメータが未知。

#### g3の提案アプローチ: イベントレベル shift-and-stack + ノイズモデル引き算

**ステップ1: ノイズマップの構築**
- A5の物理モデルを用いて、各ピクセルの期待ノイズイベントレート $\lambda_{\text{noise}}(x,y,t)$ を推定。
  - 温度、バイアス設定、背景照度から決定可能。
  - 暗黙の前提: これらのパラメータは計測可能または推定可能。
- 観測イベントストリームから $\lambda_{\text{noise}}$ を差し引いた**残差イベントストリーム**を得る。

**ステップ2: 残差ストリーム上でのイベントレベル shift-and-stack**
- 候補軌道パラメータ $(v_x, v_y)$ に沿ってイベントを時空間的にシフトし、累積。
- フレームベースのshift-and-stackとの違い:
  - イベントは離散的・非同期 → 連続的な軌跡との整合性をスコアリング。
  - Contrast Maximization (CMax) 枠組み (Gallego et al.) の自然な拡張。
  - ノイズモデル引き算により、誤検出率を大幅に低減。

**ステップ3: 統計的有意性の評価**
- 残差ストリームでのイベント累積が、ポアソンノイズの期待値を有意に超えるかを検定。
- 検出閾値の設定に物理モデルが寄与: ノイズの統計的性質が既知であるため、FAR (False Alarm Rate) の理論的計算が可能。

#### g3の具体的な研究課題

| 課題 | 内容 | 難易度 |
|------|------|--------|
| g3-a | A5モデルの天文条件（極低照度、長時間運用）への適用可能性検証 | 中 |
| g3-b | イベントレベル shift-and-stack のアルゴリズム設計と計算量評価 | 中 |
| g3-c | ノイズ引き算後の残差統計の理論的特性化（ポアソン性からの逸脱） | 高 |
| g3-d | SciDVS (A3) のような高感度DVSでの実観測的検証 | 高（ハードウェア依存） |
| g3-e | 既存SSAデータセット (C1) での検証とベンチマーク | 中 |

#### g3の期待される成果

- **検出限界等級の改善**: ノイズモデル引き算により、従来のスレッショルドベース検出で見逃していた微弱イベントを救済。
- **FAR制御の改善**: 物理モデルに基づくFAR推定により、フレームカメラの5σ閾値に相当する厳密な検出基準を設定可能。
- **高速移動天体への適用**: DVSのマイクロ秒時間分解能 + shift-and-stack により、フレームカメラでは「像が流れて」検出不能な高速天体に対応。

#### g3の先行研究との差分

| 手法 | ノイズモデル | 天文対応 | 微弱天体 | 運動推定 |
|------|-------------|---------|---------|---------|
| Shiba et al. (B7) | データ駆動 | × | × | ○（CMax） |
| Noise2Image (D5) | 照度依存 | × | △（静的のみ） | × |
| FIESTA (C3) | 閾値ベース | ○ | × | ○ |
| shift-and-stack (天文) | なし | ○ | ○ | ○ |
| **g3提案** | **物理モデル (A5)** | **○** | **○** | **○** |

---

### g4: 全統合パイプライン — 物理情報付きDVSノイズ再構成 + 補助チャンネル融合 + 天文微弱ターゲット回復（A+B+C+D 完全統合）

**現状**: g1–g3は個別の拡張方向だが、これらを**LIGOの成功事例 (D1) をテンプレートとして**統合するアプローチは存在しない。LIGOでは以下の要素が成功の鍵であった:
1. ノイズの物理モデル（地震ノイズ、熱ノイズ、散乱光等の既知の生成機構）
2. 補助センサー（ウィットネスチャンネル: 加速度計、磁力計、マイクロフォン等）
3. 機械学習による非定常ノイズ結合の学習
4. 結果の物理的検証（ノイズ差し引き後のスペクトルが理論予測と一致するか）

**提案**: LIGOのノイズ再構成パイプラインをDVS天文観測に移植する全統合アプローチ。

#### g4のシステムアーキテクチャ

```
┌─────────────────────────────────────────────────────────────────┐
│                    g4 全統合パイプライン                          │
│                                                                 │
│  ┌──────────────┐   ┌──────────────────┐   ┌───────────────┐   │
│  │ DVS主チャンネル│   │ 補助チャンネル      │   │ 物理モデル     │   │
│  │ イベントストリーム│   │ (温度, 振動, 照度) │   │ (A5 ピクセル  │   │
│  │ e(t,x,y,p)   │   │ T(t), a(t), I(t) │   │  モデル)       │   │
│  └──────┬───────┘   └────────┬─────────┘   └──────┬────────┘   │
│         │                    │                     │            │
│         ▼                    ▼                     ▼            │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │ Stage 1: ノイズフォワードモデル構築                         │   │
│  │   λ_noise(x,y,t) = F(θ_pixel, T(t), bias, I_bg(x,y,t)) │   │
│  │   - A5モデルで各ピクセルの期待ノイズレートを計算              │   │
│  │   - 補助チャンネルで時変パラメータ(T, 振動)をリアルタイム更新  │   │
│  └──────────────────────────┬───────────────────────────────┘   │
│                             │                                   │
│                             ▼                                   │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │ Stage 2: ノイズ逆問題求解                                   │   │
│  │   θ̂ = argmin_θ D(e_obs, F(θ))                            │   │
│  │   - θ̂: 推定されたピクセル固有パラメータ                      │   │
│  │   - D: イベントストリーム間の距離関数                         │   │
│  │     候補: Wasserstein距離, 点過程尤度, CMax類似度             │   │
│  │   - 非定常結合はNN (D1のDeepCleanに倣う) で学習              │   │
│  └──────────────────────────┬───────────────────────────────┘   │
│                             │                                   │
│                             ▼                                   │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │ Stage 3: 残差イベントストリーム生成                          │   │
│  │   e_residual = e_obs ⊖ F(θ̂)                              │   │
│  │   - ⊖: イベントストリームの差分演算                          │   │
│  │     (時空間的に最近傍のノイズイベントを相殺)                   │   │
│  │   - 残差のポアソン性・独立性を検証                            │   │
│  └──────────────────────────┬───────────────────────────────┘   │
│                             │                                   │
│                             ▼                                   │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │ Stage 4: 微弱天体検出 (g3パイプライン)                       │   │
│  │   - 残差ストリーム上で候補軌道に沿った shift-and-stack        │   │
│  │   - 統計検定: 累積イベント数 vs ポアソンノイズ期待値          │   │
│  │   - 多重検定補正 (Bonferroni or BH-FDR)                    │   │
│  │   - 検出候補のカタログ化                                     │   │
│  └──────────────────────────┬───────────────────────────────┘   │
│                             │                                   │
│                             ▼                                   │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │ Stage 5: 物理的検証                                        │   │
│  │   - ノイズ差し引き後のイベントレート分布が理論予測と一致するか  │   │
│  │   - 既知天体の再検出率                                      │   │
│  │   - 注入テスト (synthetic source injection and recovery)    │   │
│  └──────────────────────────────────────────────────────────┘   │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

#### g4の各ステージの詳細

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

**補助チャンネルによる拡張** (LIGO D1 に倣う):
- **温度センサー**: 暗電流は温度に指数関数的に依存。$I_{\text{dark}} \propto \exp(-E_g / 2k_B T)$。温度1°C上昇で暗電流は約2倍。リアルタイム温度計測でノイズレートを予測。
- **振動センサー（加速度計）**: マイクロフォニックノイズ（機械振動→電気ノイズ変換）の検出。望遠鏡のドーム回転、風揺れ等に対応。
- **背景照度モニタ**: フレームカメラまたはフォトダイオードで背景光度を独立計測。光害、月明かり、薄明の影響をモデルに入力。

##### Stage 2: ノイズ逆問題求解

**定式化の選択肢**:

**(a) 最尤推定 (MLE) アプローチ**:
- イベントストリームを非一様ポアソン過程としてモデル化。
- レート関数: $\lambda(x,y,t) = \lambda_{\text{signal}}(x,y,t) + \lambda_{\text{noise}}(x,y,t;\theta)$
- 尤度: $\mathcal{L}(\theta) = \prod_{i} \lambda(x_i,y_i,t_i;\theta) \cdot \exp\left(-\int \lambda(x,y,t;\theta) \, dx \, dy \, dt\right)$
- $\hat{\theta}_{\text{MLE}} = \arg\max_\theta \mathcal{L}(\theta)$ をEM的に求解（信号部分は未知→潜在変数として扱う）。

**(b) 変分推論アプローチ**:
- ノイズパラメータ $\theta$ と信号 $s$ を同時に推定。
- 変分下界: $\text{ELBO} = \mathbb{E}_{q(\theta,s)}[\log p(e_{\text{obs}}|\theta,s)] - \text{KL}(q(\theta,s) \| p(\theta,s))$
- 物理モデル A5 が事前分布 $p(\theta)$ を提供。

**(c) DeepClean型ニューラルネットワーク**:
- D1 (Vajente et al.) に倣い、補助チャンネル → ノイズイベント予測のNNを学習。
- 入力: 補助チャンネル時系列 $[T(t), a(t), I_{\text{bg}}(t)]$
- 出力: 各ピクセルの期待ノイズイベントレート $\hat{\lambda}_{\text{noise}}(x,y,t)$
- 物理モデル A5 がアーキテクチャの帰納的バイアスと初期化を提供（Physics-Informed Neural Network的）。

**推奨**: (c) を基本とし、(a) で理論的正当性を担保。物理モデルをNNの構造的制約として埋め込む (Physics-Informed) ことで、データ効率と解釈可能性を両立。

##### Stage 3: 残差イベントストリーム生成

**イベントストリームの差分演算 $\ominus$ の定義**:

DVSイベントは $(t_i, x_i, y_i, p_i)$ の4タプル。ノイズイベントの「引き算」は自明ではない。

**提案する3つの手法**:

1. **確率的薄化 (Probabilistic Thinning)**:
   - 各イベントに対し、ノイズモデルから計算した「そのイベントがノイズである確率」 $P_{\text{noise}}(e_i)$ を付与。
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

##### Stage 4: 微弱天体検出 = g3パイプライン

g3で詳述した通り。残差ストリーム上でのイベントレベル shift-and-stack。

##### Stage 5: 物理的検証

LIGO (D1) の検証方法論を移植:

1. **パワースペクトル密度 (PSD) テスト**: ノイズ差し引き前後のイベントレートPSDを比較。差し引き後のPSDが理論的な白色ポアソン + 1/f 成分に一致するか。
2. **注入・回収テスト (Injection-Recovery)**: 既知の模擬天体信号をノイズ差し引き前のストリームに注入し、パイプライン通過後に正しく回収できるか。回収効率と偽検出率のROC曲線。
3. **既知天体テスト**: カタログ天体（等級が既知）の検出率。検出限界等級の測定。
4. **ブラインドテスト**: 注入信号の有無を隠した状態での解析者の判定。

#### g4の LIGO → DVS 対応表

| LIGO要素 | DVS対応 | 状態 |
|---------|---------|------|
| 主チャンネル（ひずみデータ） | DVSイベントストリーム | 利用可能 |
| 補助チャンネル（加速度計、磁力計等） | 温度・振動・照度センサー | **要構築** |
| ノイズの物理モデル（地震、熱、散乱光） | A5 DVSピクセルモデル | 利用可能（天文条件未検証） |
| DeepClean (非定常ノイズ学習) | DeepClean的NN | **要開発** |
| テンプレートマッチング（ソース探索） | shift-and-stack（軌道探索） | 概念的に利用可能 |
| 信号注入テスト | 模擬天体注入テスト | **要設計** |
| 国際協力・オープンデータ | DVSコミュニティ + SSAデータセット | 部分的に利用可能 |

#### g4の研究課題（拡張版）

| 課題 | 内容 | 難易度 | 依存関係 |
|------|------|--------|---------|
| g4-a | 補助チャンネルシステムの設計・構築 | 高 | なし |
| g4-b | A5モデルの天文条件拡張（g3-a と共通） | 中 | なし |
| g4-c | DeepClean型NNのDVS版アーキテクチャ設計 | 中 | g4-a, g4-b |
| g4-d | イベントストリーム差分演算の理論的基礎 | 高 | g4-b |
| g4-e | 注入・回収テストフレームワークの構築 | 中 | g4-d |
| g4-f | SciDVS + 小口径望遠鏡での概念実証観測 | 高 | g4-a, g4-b, g4-c, g4-d |
| g4-g | 大口径望遠鏡（4m級）でのスケーラビリティ評価 | 非常に高 | g4-f |

#### g4の期待されるインパクト

1. **検出限界の拡張**: ノイズ逆問題パイプラインにより、DVSの検出限界等級を2–4等級改善する可能性。これはフレームカメラの√N改善（スタッキング枚数Nに対して）と異なる、**構造的な改善**。
2. **新しいクラスの天体発見**: 高速移動 + 暗い + 近傍の小天体（10–50m級NEO）の検出。フレームカメラでは像の流れにより原理的に困難。
3. **方法論の他分野への波及**: DVSノイズ逆問題のフレームワークは、神経活動のカルシウムイメージング、工業検査（微弱欠陥検出）、自動運転の悪条件センシングなどにも適用可能。

---

## 総括: 4ギャップの関係性と優先順位

```
      g1 (フォワードモデル逆問題化)
       │
       ▼
      g2 (自己教師ありノイズ学習)     独立して進行可能
       │
       ▼
      g3 (天文微弱天体検出)  ←── g1の成果が直接入力
       │
       ▼
      g4 (全統合パイプライン) ←── g1 + g3 + LIGOテンプレート + 補助チャンネル
```

**優先順位**:
- **g1 → g3**: フォワードモデルの逆問題定式化が基盤。これが無ければ g3, g4 のノイズ引き算の質が確保できない。
- **g2**: g1と並行して進行可能。g1の理論的基礎が弱い場合のフォールバック（データ駆動アプローチ）としても機能。
- **g4**: 最も野心的だが、g1とg3の成果に依存。概念設計（本文書の内容）は先行可能。

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
