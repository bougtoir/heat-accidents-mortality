# 術後疼痛の地域差・文化差：オープンデータによる検証可能性と研究デザイン提案

## はじめに

痛みの表現・知覚には地域差・文化差があることは広く認められています。この報告では、**手術あたりの術後疼痛（postoperative pain per surgery）に地域差が存在するか**を、(1) オープンデータで検証可能かどうか、(2) 研究デザインとしてどうあるべきかについて整理します。

---

## 1. 既存エビデンスの概要

### 1.1 術後疼痛の国際比較に関する先行研究

| 研究 | データソース | 対象 | 主な知見 |
|------|-------------|------|---------|
| Zaslansky et al. (2018) BJA | PAIN OUT | 整形外科手術、米国 vs 国際 | 米国患者はworst pain intensity が高く、オピオイド使用量も多い。国際比較で有意差あり |
| PAIN OUT 10カ国研究 (2022) Eur J Pain | PAIN OUT | 10カ国10,415名 | 国・術科で説明できる分散は約12%に留まり、88%は施設間・個人間変動 |
| Huang et al. (2025) Glob Health Res Policy | PAIN OUT (アジア7地域) | 5,093名 | アジア地域内でも疼痛アウトカム・オピオイド使用量にネットワーク構造の差を確認 |
| Macchia et al. (2025) Commun Med | Gallup World Poll等 | 22カ国202,898名 | 一般痛の有病割合に大きな国間差（エジプト60% vs イスラエル25%） |
| Zimmer et al. (2022) Pain | WHO WHS等 | 52カ国 | 国レベルの文脈要因（GDP、医療費等）が痛み有病率と関連 |
| Al-Hashimi et al. (2015) Br J Pain | 単施設（英国） | 民族別（白人・南アジア・黒人） | 南アジア系患者は術後NRS疼痛スコアが高く、オピオイド処方が少ない |
| Rogger et al. (2023) Curr Pain Headache Rep | レビュー | 文化的枠組みと急性痛 | 文化・民族背景が疼痛の知覚・表出・管理に強く影響 |
| Jones et al. (2025) J Clin Anesth | メタ分析 | 人種・民族別術後疼痛管理 | 非白人患者は区域麻酔を受ける可能性が18%低い |

**要点**: 術後疼痛スコアと疼痛管理に地域差・文化差が存在する強いエビデンスがある。ただし「地域差」の内訳として、(a) 疼痛の知覚・表出の差、(b) 鎮痛プロトコルの差、(c) 施設レベルの質の差 が混在しており、純粋な「文化的疼痛知覚差」の分離は困難。

---

## 2. オープンデータによる検証可能性

### 2.1 候補データソース一覧

| データソース | アクセス | 国際比較 | 術後疼痛スコア | 手術種別 | 人種/民族/国 | 評価 |
|-------------|---------|---------|---------------|---------|------------|------|
| **PAIN OUT** (Jena大学) | 共同研究契約が必要（完全オープンではない） | 40カ国以上 | NRS (IPO-Q) | 術科別 | 国・施設 | **最適** |
| **MIMIC-IV** (PhysioNet) | 認証制（CITI修了後無料） | 米国単一施設 | pain score記録あり | 手術コードあり | 人種/民族あり | **次善** |
| **eICU-CRD** (PhysioNet) | 認証制 | 米国多施設 | 限定的 | ICU患者中心 | 人種あり | 補助的 |
| **INSPIRE** (韓国) | PhysioNet経由 | 韓国単一施設 | バイタルのみ | 手術コードあり | 単一国 | 限定的 |
| **NIS/HCUP** (AHRQ) | 有料ライセンス | 米国全国 | 疼痛スコアなし | ICD手術コード | 人種あり | 不適 |
| **ACS-NSQIP** | 参加施設のみ | 米国+カナダ一部 | 疼痛スコアなし | 術式別 | 人種あり | 不適 |
| **GBD 2021** (IHME) | 無料ダウンロード | 204カ国 | 慢性疼痛DALYs | 術後に非特異的 | 国別 | 間接的 |
| **Gallup World Poll** | 有料ライセンス | 140カ国以上 | "physical pain yesterday" | 術後に非特異的 | 国別 | 間接的 |
| **QUIPS** (ドイツ) | ドイツ国内共同研究 | ドイツ国内 | NRS | 術式別 | 限定的 | ドイツ限定 |

### 2.2 各データソースの詳細評価

#### A. PAIN OUT レジストリ（最有力）
- **概要**: Jena大学が運営する国際術後疼痛レジストリ（NCT02083835）。2009年開始、目標200,000例、2030年まで継続。
- **変数**: IPO-Q（International Pain Outcomes Questionnaire）による多次元疼痛アウトカム（worst pain, time in severe pain, 機能障害, 満足度等）、鎮痛薬使用量、患者背景
- **地域**: 40カ国以上、20言語以上でバリデーション済み
- **アクセス**: 完全オープンデータではない。共同研究提案を Jena 大学 PAIN OUT チーム（ruth.zaslansky@med.uni-jena.de）に提出する必要がある。ただし、既に多数の外部共同研究論文が出版されており、アクセスのハードルは比較的低い。
- **検証可能性**: **高い**。国・地域を独立変数、術式を層別因子として、術後疼痛スコアの地域差を多水準モデルで検証可能。

#### B. MIMIC-IV（単独で検証可能）
- **概要**: Beth Israel Deaconess Medical Center（米国ボストン）のEHR、約130,000入院、ICU含む
- **変数**: pain score（chartevents内）、手術コード、人種/民族、年齢、性別、各種臨床データ
- **制限**: 単一施設・単一国のため「地域差」は直接検証不可。ただし、**同一施設内での人種/民族間差**は検証可能
- **アクセス**: PhysioNet credentialed access（CITI Human Subjects Research コース修了後、無料）
- **検証可能性**: **中程度**。「地域差」ではなく「同一医療環境下での民族間差」として部分的に検証可能。同一鎮痛プロトコル下での差を見ることで、文化的疼痛知覚差に迫れる可能性。

#### C. GBD 2021 + Gallup World Poll（生態学的研究として）
- **概要**: 国レベルの疼痛負荷（DALYs）や痛み有病率の国際比較データ
- **制限**: 術後疼痛に特異的でない。慢性疼痛（腰痛、頸部痛、変形性関節症等）が中心。
- **検証可能性**: **低い（間接的）**。「手術あたりの術後疼痛」の検証には不向きだが、背景としての国民の疼痛感受性の地域差を示す補助データとして有用。

### 2.3 総合判定

| 検証レベル | 実現可能性 | 推奨データ |
|-----------|-----------|----------|
| 国際間比較（本命） | 共同研究契約が必要 | PAIN OUT |
| 同一施設内の民族間比較 | すぐに着手可能 | MIMIC-IV |
| 国レベルの生態学的相関 | すぐに着手可能 | GBD 2021 + 手術件数データ |

**結論: オープンデータで「ある程度」検証可能だが、最も適切なデータ（PAIN OUT）は完全オープンではなく共同研究契約が必要。MIMIC-IVを用いた民族間比較は即座に実施可能。**

---

## 3. 研究デザイン提案

### 3.1 なぜ単純な国際比較では不十分か

PAIN OUT 10カ国研究(2022)が示したように、「国」変数が説明する分散は全体のわずか数%であり、施設間・個人間変動が圧倒的に大きい。これは以下の交絡因子が混在するためです：

- **鎮痛プロトコルの施設差**（最大の交絡）
- **術式構成の国間差**
- **患者背景の系統的差異**（年齢、BMI、併存疾患）
- **医療制度・アクセスの差**
- **疼痛評価スケールの言語的同等性**

### 3.2 推奨デザイン

#### デザイン案A: 多水準横断研究（PAIN OUT活用・本命）

```
研究構造（3水準ネスト構造）:
  Level 3: 国 / 地域（文化圏）
  Level 2: 施設（病院）
  Level 1: 患者（個人）
```

**方法論**:
- **目的**: 術後疼痛アウトカムの分散を「国」「施設」「個人」に分割し、国レベルの効果量を推定
- **統計モデル**: 3水準ランダム切片モデル（multilevel model / hierarchical linear model）
  - アウトカム: worst pain NRS, % time in severe pain, 機能障害, 満足度
  - Level 1 共変量: 年齢, 性別, BMI, ASA-PS, 術式, 麻酔法, 併存疾患
  - Level 2 共変量: 病院規模, 疼痛管理体制（APS有無等）, 教育病院か否か
  - Level 3 共変量: 国（文化圏プロキシ）, HDI, 医療費対GDP比, オピオイド規制レベル
- **サンプルサイズ**: Level 3 で最低15カ国（ICC推定の安定性のため）、各施設50-100例以上
- **主要解析**: ICC（級内相関係数）の分解 → 国レベルICCが有意であれば地域差の存在を示唆
- **感度分析**: 術式を層別化（例: TKA, 帝王切開, 腹部手術）して術式交絡を除去

**利点**: 交絡の階層的制御が可能、既存PAIN OUTインフラを活用
**課題**: PAIN OUTデータアクセスの交渉が必要

#### デザイン案B: 同一施設内民族間比較（MIMIC-IV・即時実施可能）

```
研究構造: 後ろ向きコホート
  対象: MIMIC-IV内の手術患者
  曝露: 人種/民族（White, Black, Asian, Hispanic, Other）
  アウトカム: 術後pain score（NRS）の時系列
```

**方法論**:
- **目的**: 同一施設・同一鎮痛環境下で、人種/民族間の術後疼痛スコアに差があるか
- **統計モデル**: 
  - 混合効果モデル（反復測定: 術後0-72hのpain score trajectory）
  - 傾向スコアマッチング or IPTW（inverse probability of treatment weighting）で術式・背景因子を調整
- **強み**: 施設差・プロトコル差を完全に除去できる（単一施設のため）
- **交絡制御**: 年齢, 性別, BMI, ASA-PS, 術式（CPTコード）, 麻酔法, 術中オピオイド使用量, 併存疾患（Elixhauser/Charlson）
- **追加分析**: オピオイド消費量の民族間差（疼痛スコアだけでなく鎮痛需要も比較）
- **サンプルサイズ**: MIMIC-IVには約130,000入院があり、手術患者はその相当割合を占める。人種別にも十分なサンプルが期待できる（White ~68%, Black ~8%, Asian ~3%, Hispanic ~3%）

**利点**: 完全オープンデータで即時開始可能、施設差の交絡を完全排除
**課題**: 単一施設（ボストン）のため一般化可能性に限界。「地域差」というよりは「民族差」の検証。

#### デザイン案C: 生態学的研究（GBD + 手術件数データ）

```
研究構造: 国レベル生態学的横断研究
  単位: 国
  曝露: 文化圏/地域/SDI
  アウトカム: 疼痛関連DALYs / 手術件数 の比
```

**方法論**:
- GBD 2021の慢性疼痛DALYsデータ（国別）と、Lancet Commission on Global Surgery の手術件数推定データを組み合わせる
- **限界**: 術後疼痛に特異的でなく、生態学的誤謬のリスク大

### 3.3 改善提案のまとめ

| 現状の課題 | 改善提案 |
|-----------|---------|
| 国と施設の効果が分離できない | 3水準マルチレベルモデルを採用し、ICCを階層分解 |
| 術式構成の交絡 | 術式を層別化（TKA, C-section等の標準手術に限定） |
| 鎮痛プロトコルの施設差 | Level 2共変量に鎮痛管理体制を含める or MIMIC-IV型の単一施設デザイン |
| NRSの言語的同等性が不明 | IPO-Qの言語バリデーション論文を確認 + DIF（Differential Item Functioning）分析を追加 |
| 「文化」の操作的定義が曖昧 | Hofstedeの文化次元（個人主義vs集団主義等）やWVS（世界価値観調査）データをLevel 3共変量に |
| サンプルサイズが不十分な地域 | アジア・アフリカ・南米の施設リクルートを優先（PAIN OUT拡張） |
| 横断研究の限界 | 可能であれば同一患者の術前疼痛閾値測定（QST: 定量的感覚テスト）を追加する前向きデザイン |

---

## 4. 具体的アクションプラン

### Phase 1: 即時実施（0-3ヶ月）— MIMIC-IV分析
1. PhysioNet認証取得（CITI course修了）
2. MIMIC-IV内の手術患者コホート抽出
3. pain scoreデータの可用性・完全性を確認
4. 人種/民族別の術後疼痛スコア比較（調整済み）
5. プレプリント公開

### Phase 2: 共同研究開始（3-6ヶ月）— PAIN OUT
1. PAIN OUTチーム（Jena大学 Zaslansky教授）に研究提案書を送付
2. データ使用契約の締結
3. 3水準マルチレベルモデルの解析プラン策定
4. SAP（Statistical Analysis Plan）の事前登録（PROSPERO or OSF）

### Phase 3: 前向き研究（6-24ヶ月）— 新規データ収集
1. 3-5カ国（例: 日本, ドイツ, ブラジル, ナイジェリア, 米国）の施設リクルート
2. 標準手術（TKA or 帝王切開）に限定
3. IPO-Q + QST（術前疼痛閾値）+ 文化的変数（言語, 信仰, 痛みの信念尺度）の統一プロトコル
4. 事前登録（ClinicalTrials.gov）
5. 本論文

---

## 5. 結論

**Q1: オープンデータで検証可能か → 部分的にYES**
- MIMIC-IV を用いた「同一施設内の民族間差」は即座に検証可能（完全オープン）
- 国際間比較の本命である PAIN OUT レジストリは完全オープンではないが、共同研究契約により比較的容易にアクセス可能
- GBD等の完全オープンデータは術後疼痛に特異的でなく、間接的なエビデンスに留まる

**Q2: デザイン改善提案**
- **最大の課題は「国差」と「施設差」の分離**。3水準マルチレベルモデルが必須
- **術式の標準化**（TKA, C-section等に限定）により、術式交絡を排除
- **疼痛評価の文化的妥当性**（DIF分析）を組み込むべき
- **文化の操作的定義**にHofstede文化次元やWVSデータを活用
- 最も強力なデザインは、**複数国の標準手術患者に対する前向き統一プロトコル研究 + QST**

---

## 参考文献（主要）

1. Zaslansky R et al. (2018) Pain after orthopaedic surgery: differences in patient reported outcomes in the United States vs internationally. *Br J Anaesth* 120(4):790-797.
2. PAIN OUT Research Group (2022) Status quo of pain-related PROs and perioperative pain management in 10,415 patients from 10 countries. *Eur J Pain* 26:2120-2140.
3. Huang Y et al. (2025) Differentiating network structures and sex differences of pain-related outcomes in seven Asian regions. *Glob Health Res Policy* 10:51.
4. Macchia L et al. (2025) Demographic variation in pain across 22 countries. *Commun Med* 5:154.
5. Rogger R et al. (2023) Cultural Framing and the Impact on Acute Pain and Pain Services. *Curr Pain Headache Rep* 27:429-436.
6. Al-Hashimi M et al. (2015) Influence of ethnicity on the perception and treatment of early post-operative pain. *Br J Pain* 9(3):167-172.
7. Jones A et al. (2025) Racial and ethnic differences in acute post-operative pain management: Systematic review and meta-analysis. *J Clin Anesth.*
8. Zimmer Z et al. (2022) A global study of pain prevalence across 52 countries. *Pain* 163(9):1740-1750.
9. Shah N et al. (2024) Unraveling the Tapestry of Pain: Ethnic Variations, Cultural Influences, and Physiological Mechanisms. *Cureus* 16(5):e60692.
10. PAIN OUT website: https://www.pain-out.eu/
11. MIMIC-IV: https://physionet.org/content/mimiciv/
12. GBD 2021: https://ghdx.healthdata.org/gbd-2021/data-input-sources
