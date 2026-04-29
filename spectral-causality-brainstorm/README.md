# Spectral Causality Brainstorm — 医療データへのGEM-RAG的因果性アプローチ

GEM-RAG（Graphical Eigen Memories for Retrieval Augmented Generation）のコアアイデア（ユーティリティ質問 → グラフ → スペクトル分解）を医療データの因果推論に応用するブレインストーミング文書群。

## 文書構成

| # | ファイル | 内容 |
|---|---|---|
| 01 | `01_gem_rag_medical_application.md` | GEM-RAGの医療データ応用（横断的スナップショット + 経時データ）。「ユーティリティ因果性」の基本提案。 |
| 02 | `02_lingam_x_utility_causality.md` | LiNGAMファミリーとの比較・統合アイデア。変数レベル因果 × テーマレベル因果の二段ロケット等。 |
| 03 | `03_spectral_causality_deep_dive.md` | スペクトル因果性の深掘り。磁気ラプラシアン、Hodge分解、因果フーリエ解析との接続。数学的定式化。 |
| 04 | `04_hill_criteria_mapping.md` | Hill の9基準 × 因果推論手法（40+手法）の包括的マッピング。既存手法のH6/H7/H9空白地帯と提案手法の位置づけ。 |

## 起点記事

- [GEM-RAGが拓く「グラフ×スペクトル」な次世代RAG](https://zenn.dev/lluminai_tech/articles/cc4b62b47936b3)

## キーコンセプト

- **Utility Causality（ユーティリティ因果性）**: 「同じ臨床問いに答える能力」の時間的連続として定義される因果性
- **Spectral Causal Intensity (SCI)**: 磁気ラプラシアンの固有ベクトル位相差に基づく因果強度
- **Hodge-Causal Decomposition**: エッジフローの勾配成分 = 因果的フロー、カール成分 = フィードバック
- **Ensemble Causal Direction (ECD)**: LiNGAM + SCD + Granger のアンサンブル因果方向推定

## 関連研究

- Kotoku et al. (2020) — 大阪府健診データ × DirectLiNGAM
- Okuda et al. (2025) — 日本健診コホート10万人超 × Longitudinal LiNGAM
- M'Charrak et al. (2025) — スペクトル正則化 × 因果DAG学習
- Seifert, Wendler & Püschel (2023) — DAG上の因果フーリエ解析
- Maehara & Ohkawa (2019) — 単一細胞データ × Hodge分解
