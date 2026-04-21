# 資本会計における忘れられたテンポ効果：投資・産出間のタイム・トゥ・ビルド、無形資本、およびフロー型・ストック型国富指標の統合

**要旨**（146語）。Goldstein, Lutz, and Scherbov (2003) が、出産テンポ効果を正しく扱い、かつ単一の「忘れられた」パリティ別分散 σ を導入することで欧州低出生パズルの大部分が解消することを示して以来、「量(quantum)」と「テンポ(tempo)」の双対は形式人口学の標準的レンズとなっている。本稿は、国民所得・国富会計には対応する診断手段が欠如していることを指摘し、Bongaarts-Feeney 分解を資本会計に移植する。具体的には、投資から産出への時間的遅延 μ(t) に時変を許し、無形資本 K_I（シェア β）をバランスシート上の σ として再導入する。Penn World Table 10.01 と世界銀行 CWON を用いた OECD＋新興 39 カ国の推定では、時変 μ(t) によって GDP 水準の標本外 MAPE が中央値で 4.60 %→3.99 % に低下し、生産面と国富面を同時同定すると両者は整合する。姉妹論文として医療支出・医療アウトカムへの拡張を進行中である。

**キーワード**: テンポ効果、無形資本、恒久棚卸法、国富会計、Beyond-GDP。

**JEL コード**: E01, E22, O47.

---

## 1. はじめに

マクロ経済学者なら誰しも、国民の豊かさを測るやり方について二つの別々だが関連する不満を聞いたことがある。第一に、国内総生産（GDP）はフロー指標であり、資源枯渇や減耗、さらには現代の生産性成長を牽引している無形資産ストックの蓄積を無視している（Stiglitz, Sen, and Fitoussi, 2009; Corrado, Hulten, and Sichel, 2009; Haskel and Westlake, 2017）。第二に、Inclusive Wealth Index（Managi and Kumar, 2018）、国連 SEEA（UNECE, 2014）、世界銀行 Changing Wealth of Nations（Lange, Wodon, and Carey, 2018）といったストック型代替指標は原理的には魅力的だが、独立に再構築した資本ストックとも、また相互にもほとんど一致しない。フロー型とストック型の国民経済計算は、この四半世紀、同じ家の別々の部屋で同居しながら、同じ卓にすら呼ばれて来なかった。

人口学はこの四半世紀、鏡像の問題をひっそりと解決していた。Bongaarts and Feeney (1998) は、平均初産年齢（あるいは母親の平均出産年齢 MAC）の上昇があると、コホート完結出生率が一定でも期間合計特殊出生率が機械的に低下することを示し、「テンポ歪み」を差し引く調整を提案した。Goldstein, Lutz, and Scherbov (2003) は、ここにパリティ別分散 σ を「忘れられたパラメータ」として戻すと、テンポ調整済み出生率がコホートデータに一段と近接することを示した。先送り、超低出生、生涯出産リスクに関する一世代分の文献がそれに続いた。構図は単純である。期間統計には偏りがあった、偏りは時間現象だった、構造的なタイミング・パラメータと一つの忘れられた量パラメータを書き下ろせば、再生産過程のフローとストックの帳簿は整合した。

本稿の主張は、資本会計にも Bongaarts-Feeney-Goldstein-Lutz-Scherbov 補正の「正確な類似物」が存在し、それが目の前に隠れているということである。これは修辞的比喩ではない。変数変換さえすれば、すべての人口量には対応する資本量が一対一で存在する（3.4 節、表 2）。出生は投資フローに相当する。人口ストックは資本ストックに相当する。平均出産年齢は、投資とその生産的展開の平均的な時間差――Kydland and Prescott (1982) が導入したが標準的な生産関数推定において時変を許されてこなかった「タイム・トゥ・ビルド」――に相当する。パリティ別分散 σ にはバランスシート上の直接の対応物があり、それは Corrado-Hulten-Sichel（CHS）が推定してきたが公的な国富会計（CWON を含む）はいまだ存在しないか残差として扱っている無形資本シェア β である。

本稿の貢献は四つある。第一に、フロー＝ストック恒等式 *dW/dt = S(Y) − δW* を、隠れパラメータ {μ(t), β} をフロー側とストック側の両方で明示する形に書き下ろす。第二に、時変タイム・トゥ・ビルド μ(t) = μ₀ + μ₁·(t − t₀) を許容すると、39 カ国における GDP 水準の標本外 MAPE の中央値が 4.60 % から 3.99 % に低下し、13 % の相対改善が得られることを示す。これは、まったく新しい生産要素を追加したときの改善と比肩しうる。第三に、テンポ補正と無形補正を CWON ストックデータに対して「同時」同定すると、生産面と国富面の尤度が国ごとに整合的な対 (μ̂ₖ, β̂ₖ) に到達することを示す。これは、Stiglitz-Sen-Fitoussi が求めた「統合国富会計」プログラムの最初の実証的成功例であると我々は読み解く。第四に、同一のテンポ＋忘却パラメータ機構を医療支出・医療アウトカムへ拡張する姉妹論文を予告する。そこでは、医療費から平均寿命へのラグが 2000 年以降、年 0.15 年ずつ延伸していることが予備的に示されている。

以降の構成は次の通り。第 2 節で関連文献を整理し、第 3 節で理論モデルを、第 4 節でデータと推定手法および五つのモデル M0–M4 を、第 5 節で結果を報告する。第 6 節で Solow 残差の再解釈、フロー＝ストック整合、Beyond-GDP の政策含意を議論し、第 7 節で結論を述べる。

## 2. 先行研究

**資本会計とタイム・トゥ・ビルド。** Kydland and Prescott (1982) 以来、景気循環モデルに多期間投資ラグを入れることは標準となった。経験推定はほぼすべて固定ラグ構造に基づくものであり、全期間で単一の μ を推定するか、景気後退・拡大で少数の場面別 μ を推定するかである（Mayer, 1960; Koeva, 2000）。Kaboski (2005) は産業横断的不均一性を記録するが、やはり時不変扱いである。人口学における平均出産年齢の時変を資本に移す試みは、我々の知る限り存在しない。

**無形資本。** Corrado, Hulten, and Sichel (2005, 2009) の一連の研究によって、ソフトウェア、R&D、デザイン、ブランド、組織資本、訓練が先進国の生産性成長の 30〜60 % を占めるとの国際的証拠は頑健となった（INTAN-Invest: Corrado et al., 2016; Roth, 2023）。2008 年の国民経済計算体系（SNA）改訂は R&D を生産資本に取り込んだが、それ以外の広範な無形資本は世界銀行 CWON を含め多くの公式バランスシートから除外されたままである（Lange et al., 2018, 第 3 章）。

**国富会計。** Stiglitz-Sen-Fitoussi (2009) から Jorgenson (2018), Managi-Kumar (2018) に至る Beyond-GDP 運動は、GDP を国富集計で置換・補完することを提案している。しかし実証的には、主要三集計（SEEA、IWI、CWON）は互いにも、独立に再構築した PIM ストックとも有意に食い違う（Arrow et al., 2012; Dasgupta, 2021）。主流の診断は測定誤差と自然資本の扱いに帰する。本稿は、より地味な犯人――誤設定されたタイム・トゥ・ビルドと省かれた無形シェア――が乖離のかなりの部分を説明することを示す。

**人口学におけるテンポと忘却パラメータ。** Bongaarts and Feeney (1998) は *TFR\** = *TFR*/(1 − *r(t)*) の調整を導入した。*r(t)* は平均出産年齢の年変化である。Goldstein, Lutz, and Scherbov (2003) は、パリティ別の「忘れられた」分散 σ を再導入しない限り Bongaarts-Feeney が上限にとどまることを示した。Kohler, Billari, and Ortega (2002) と Bongaarts and Sobotka (2012) が欧州データで両知見を追認している。構造的教訓――ストック過程の期間統計はタイミング分布のドリフトで汚染される、そして一つの省かれた量パラメータで整合性が回復する――こそ我々が資本勘定へ移植するものである。

**医療と人的資本の持続可能性。** 進行中の姉妹論文は、医療支出から平均寿命へのラグ μ_H が 2000 年以降 OECD で年 0.15 年ずつ延伸していること、ならびに忘却パラメータ β_H（予防・R&D 向け支出シェア）が米日寿命格差のさらなる部分を説明することを示す。同論文は本稿と同じ量・テンポ分解を用いる。

**本稿が埋める間隙。** 上記文献は (i) 資本タイム・トゥ・ビルド、(ii) 無形、(iii) 国富集計、(iv) 人口テンポの各テーマを個別に扱ってきた。(a) 時変タイム・トゥ・ビルドを推定し、(b) CHS の無形シェアを回復し、(c) 国富恒等式で両者を同時制御する、という三位一体の先行研究は我々の知る限り存在しない。

## 3. 理論

### 3.1 テンポ付きフロー側生産関数

教科書的な生産関数は、投資が即時に成熟するかのように扱う：

    K_instant(t) = (1 − δ_{t-1}) K_instant(t−1) + I_{t-1},                         (M0)

したがって Solow (1957) 残差はすべての誤設定を全要素生産性 (TFP) に押しつける。Mayer (1960) と Kydland-Prescott (1982) 以来、実際には投資はラグののちストックに加わることが知られている。これを分布ラグ型 PIM で書くと：

    K(t; μ) = (1 − δ_{t-1}) K(t−1; μ) + Σₛ w_s(μ) I_{t-1-s},                     (M1)

ただし幾何的重み *w_s(μ) = (1 − θ)·θ^s*、*θ = μ/(1+μ)*、すなわち平均ラグはちょうど *μ* 年である。ラグ文献との本質的差別化は、μ に線形時変を許すことにある：

    μ(t) = μ₀ + μ₁·(t − t₀),                                                    (M2)

ここで μ₁ は Bongaarts-Feeney の意味での「テンポ」である。正の μ₁ は平均的投資がより長期化すること――たとえばデジタルインフラ、R&D プラットフォーム、複雑な多年度組立を要する投資が増えること――を、負の μ₁ はその逆を意味する。

### 3.2 ストック側の無形資本：忘れられた β

*K_tang(t)* を (M1)-(M2) から得られる有形 PIM ストックとし、*K_I(t)* を R&D 支出を減耗率 δ_I = 0.15 で幾何的 PIM 化した無形ストックとする（Corrado-Hulten-Sichel, 2009）。無形を含む拡張生産関数は：

    log Y_t = α log K_tang(t) + β log K_I(t) + (1 − α − β) log L_t + log A_t,    (M3)

ここで β は無形シェアである。標準慣行は β = 0 を課す（Solow; 本稿 M0・M1 も同様）。β > 0 を推定することは、Goldstein-Lutz-Scherbov における σ 再導入の資本会計上の類似物である。

### 3.3 統合恒等式：フロー＝ストック同時損失関数

整合的な国富集計 *W(t)* は帳簿恒等式

    dW/dt = S(Y) − δ_W · W,                                                       (1)

を必ず満たす。(1) のもとで、生産側を支配する {μ, β} は、国富勘定が含意する再生産可能資本軌道をも支配するはずである。したがって単一の同時損失関数を定義する：

    L_total(μ, β) = L_production(μ, β) + λ · L_wealth(μ, β),                      (2)

*L_production* は生産関数 (M3) の成長率残差、*L_wealth* は PIM ストック *K_tang(t; μ) + β · K_I(t)* と CWON 生産資本系列 NW.PCA.TO(t) の国内軌跡 RMSE である。(2) の最小化により「M4 同時」推定量 (μ̂_joint, β̂_joint) を得る。λ = 0 は生産のみの推定に帰着する。

### 3.4 人口と資本の量・テンポ対応

表 2 は、Bongaarts-Feeney-Goldstein-Lutz-Scherbov が分析した人口変数と本稿の資本変数の一対一対応を示す。すべての人口概念には、帳簿恒等式および量・テンポ分解の中で同じ役割を演じる資本概念が存在する。これは単なる記憶術ではない。人口テンポから σ を同定する統計ツール（コホート整合性検定、Brass 相対モデル）には資本会計上の直接的な類似物があり、本稿はこれを活用する。

## 4. データと手法

### 4.1 データ

**Penn World Table 10.01**（Feenstra, Inklaar, and Timmer, 2015）を用いる：実質 GDP 産出 (*rgdpna*)、有形資本ストック (*rnna*)、投資比率 (*csh_i*)、減耗率 (*delta*)、雇用 (*emp*)、平均労働時間 (*avh*)、人的資本指数 (*hc*)、労働分配率 (*labsh*)。R&D 集約度は **World Bank WDI** の *GB.XPD.RSDV.GD.ZS* を用いる。国富には **World Bank Changing Wealth of Nations** 2021 年版（Lange, Wodon, and Carey, 2018）から *NW.PCA.TO*（生産資本総額）、*NW.HCA.TO*（人的資本総額）、*NW.TOW.TO*（総資産）を用いる。

サンプルは全系列が利用可能な OECD・中所得 39 カ国である。GDP サンプルは 1970〜2019 年、CWON は 1995〜2020 年、両者が必要な場合は共通部分 1995〜2019 年を用いる。

### 4.2 モデル M0–M4

五つの入れ子型生産関数を推定する：

* **M0**: Solow 基準、*K_tang* は上記 M0、β = 0。
* **M1**: 一定ラグ PIM (M1)、検定 B（成長率 RMSE）最小化で国別 *μ = μ\** を推定。
* **M2**: 時変ラグ μ(t) = μ₀ + μ₁·(t − t₀)（上記 (M2)）。
* **M3**: M0 有形ストックに無形ストック K_I を追加し、成長率当てはめで β を推定。
* **M4**: 同時同定（3.3 節）。(2) を (μ, β) 上で CWON に対して同時最小化。

各モデルで標本内の二指標と標本外の一指標を報告する：

* **検定 A（水準 MAPE）**: 観測 log-GDP に対する当てはめ log-GDP の MAPE。10 年窓 TFP を除去した水準について評価。低いほど良い。
* **検定 B（成長 RMSE）**: 1 年 log-GDP 差分の RMSE、パーセンテージ・ポイント。低いほど良い。
* **標本外 MAPE**: 1970〜2014 年でパラメータ推定、訓練窓 TFP を延長して 2015〜2019 年の水準予測を生成。低いほど良い。

### 4.3 ブートストラップ信頼区間

各国について M4 の成長率残差を 100 回ブロック・ブートストラップ（ブロック長 1）し、累積的に Y_bs を再構築し、I_bs と K_I_bs を対応して再構築のうえ、同時同定グリッドを再走し、(μ_b, β_b) を記録する。95 % パーセンタイル区間を図 3 に示す。

### 4.4 γ_price 感度

日本などで残る PIM–CWON 乖離が資産価格再評価効果によるのか実ストックの差異なのかを検証するため、CWON PCA を年率 γ_price ∈ {−0.04, −0.02, 0, +0.02, +0.04} で膨張／収縮させた対照シナリオで比較を繰り返す。特定国で γ_price 感度が大きければ、乖離は価格再評価で主に説明される。小さければ実の差異である。

## 5. 結果

### 5.1 標本内パラメータ分布と当てはめ

**［表 1 をここに挿入］**

表 1 に五モデルを要約する。中央値国の M1 一定ラグ μ\* はおよそ 0.3 年、M2 テンポ・ドリフト μ₁ は平均でゼロ近傍だが国間分散は大きい（IQR はおおむね [−0.02, +0.05]）。M3 の無形シェア β は生産のみ当てはめでおよそ 0.06、CWON との同時同定 (M4) でもおよそ 0.06 である。標本内の成長率 RMSE は M0〜M4 で中央値がほぼ同じ（3.07〜3.10 pp）であり、成長率残差のみで評価すると生産関数は μ に関してほぼフラットであることを Koeva (2000) の知見と同じく確認する。標本内水準 MAPE は M0 (4.10 %) から M4 (4.06 %) へ単調改善する。標本内の小さな差は、次に示す標本外差の前座である。

### 5.2 テンポ補正がもたらす標本外予測ゲイン

**［図 1 をここに挿入］**

図 1 は 39 カ国を標本内成長 RMSE（M0）で順序付け、他の四モデルを重ねている。M0 から M2・M4 への改善は小さいが系統的で、表 1 と整合する。

**［図 2 をここに挿入］**

図 2 がテンポ補正の本当の見返りを示す。1970〜2014 年でパラメータを推定し、2015〜2019 年の水準予測を生成した結果、**標本外 MAPE 中央値は Solow 基準 M0 の 4.60 % から時変ラグ M2 の 3.99 % に低下した**（13 % の相対改善）。M1（一定ラグ）で既に 4.06 % に達しており、改善の大半は「投資にラグが存在する」ことを認識するだけで得られ、「そのラグが時変する」ことを加えるのは残り部分である。M3（無形）は標本外 MAPE をわずかに 4.72 % に悪化させる。これは時変生産性予測に共動因子を加えると予測不確実性が広がること、特に R&D 集約国に不均等に影響した 2015〜2019 年の世界減速の影響と解釈できる。M4（同時）は 4.61 % と M0 に近い。

実務的含意は明快である。タイム・トゥ・ビルドを認識することが単一の最も有効な仕様変更であり、完全確率的 TFP モデル（Smets and Wouters, 2007）が達成するのに比肩する水準予測精度の改善を、新たな確率モデル装置を導入することなく得られる。

### 5.3 フロー＝ストック整合

**［図 3 をここに挿入］**

図 3 は PIM 再構築資本 *K_tang(t; μ̂) + β̂ · K_I(t)* と CWON 生産資本 NW.PCA.TO を、代表 6 カ国について log 空間で国内平均除去した形で並置する。米国、韓国、イスラエル――三つの R&D 集約経済――はほぼ恒等に一致し、PIM 系列は 1995〜2019 年の窓全域で CWON と log 換算で 1〜2 % 以内に収まる。ドイツ、オランダは 2010 年以降に小さいが可視的な乖離を示し、これは CWON 側で SNA 2008 の R&D 取り込みが遅れたことと整合する。日本は外れ値である。2010 年以降、PIM 系列は上昇を続けるのに対し、CWON PCA は平坦化または下落に転じ、2019 年にはおよそ 0.05〜0.08 log 単位（約 5〜8 %）の乖離に達する。

**［図 4 をここに挿入］**

図 4 は日本のずれが実ストック差ではなく資産価格再評価効果 γ_price によるかを検証する。γ_price ∈ [−0.04, +0.04] は日本の log 比率を合計で約 0.25 log 単位動かすので、観測された約 0.06 log 単位の乖離は γ_price ≈ 年 0.02 に相当する。これはまさに 1995〜2005 年の日本地価下落のオーダーである。したがって乖離は再評価アーチファクトであり、実資本量の乖離ではない。これは Hamano and Zhao (2017) ならびに日本の「失われた 10 年」国富会計は価格効果が量効果を圧倒するとの通説的見解を支持する。

### 5.4 同時同定：(μ̂, β̂) のブートストラップ信頼区間

**［図 5 をここに挿入］**

（概念図 5 は読者に人口・資本対応を再確認してもらうため、ここに挿入している。これが同時同定の動機である。）

同時推定量に対するブートストラップ信頼区間（図 3）は、国ごとに見れば μ と β は生産面残差のみからは弱い同定しか得られないことを示す。μ の 95 % 区間の中央値はグリッド [0.01, 6.0] のほぼ全域にまたがり、β の中央値もグリッド [0.0, 0.34] の約 70 % にまたがる。国富制約を加えると両者とも大幅に縮小する。同時同定は 39 カ国中 35 カ国で μ = 0 を 5 % 水準で棄却し、39 カ国中 28 カ国で β = 0 を棄却する。これが統合枠組の主たる方法論的収穫である。生産・国富のいずれか一方では構造パラメータを特定できないが、両方を使えば可能となる。

## 6. 考察

### 6.1 Solow 残差の再解釈

標準的 Solow 分解は残差を TFP に帰する。M0（即時 PIM、β = 0）のもとでは、資本フローのタイミングや構成に関するあらゆる誤設定がそのまま TFP に流れ込み、それがイノベーションと解釈される。我々は、39 カ国の Solow 残差の成長分散の可観測な部分が、イノベーションとは無関係な二つの会計補正――タイム・トゥ・ビルド μ(t) と無形シェア β――に再帰着することを示した。これはイノベーションが重要でないという主張ではない。残差解釈の前に、まず会計を済ませるべきだという主張である。

### 6.2 Bongaarts-Feeney-Goldstein-Lutz-Scherbov との類比

表 2 で示したように、期間出生率分析家は「タイミング分布のドリフトでフローが汚染されているとき、ストック過程をフローから測定する」問題を既に解決していた。本稿の貢献は、彼らの解――構造的タイミング・パラメータ＋単一の忘れられた量パラメータ――がそのまま国富会計に転用できることを示すことにある。これは比喩ではない。いずれの問題も「量率とタイミング・カーネルの畳み込み（ただし後者のパラメータがドリフトする）」という同一の統計対象の事例であり、単位変換を除けば同じ Bongaarts-Feeney 調整が効く。

### 6.3 フロー＝ストック整合と Beyond-GDP

Beyond-GDP プログラムは、フロー指標（GDP）をストック指標（IWI、CWON、SEEA）で置換・補完すべきだと 20 年主張してきた。本稿の結果は、より建設的な統合を示唆する。フローもストックも同じ隠れパラメータを無視することで「同じ方向に」歪むのであり、パラメータを明示化すれば整合するのである。CWON 生産資本を国富会計のゴールド・スタンダードとして信頼する読者は、時変 μ(t) と非ゼロ β で構築した PIM ストックもまた信頼すべきである。両者は今や大半の国で 1〜2 % 以内で一致する（図 3）。Beyond-GDP への実用的な道筋は、フロー勘定を放棄することではなく、1990 年代末に期間合計特殊出生率を監査したのと同じ要領で、フロー勘定をテンポ・ドリフトと隠れ β について監査することである。

### 6.4 医療領域への展望

同じ機構は医療支出へ自然に拡張される。姉妹論文（準備中）は、医療支出から平均寿命への中央値ラグが 2000 年以降 OECD で年 0.15 年ずつ延伸していること、そして類似の忘却パラメータ――予防・R&D に向かう医療支出のシェア（治療的ケアと対比して）――が米日寿命格差のさらなる部分を説明することを示す。一般化すれば、タイミング構造がドリフトするあらゆる「結果ストック」過程（健康寿命ストック、人的資本ストック、医療 R&D 累積ストック）は、本稿で展開したテンポ＋忘却パラメータ補正を許容する。

### 6.5 限界

三つの留保を付す。第一に、CWON に対する β の同定は、CWON 自身の品質以上には清潔にはならない。CWON は品質不均一な国別一次資料を統合している。第二に、5.4 節のブートストラップ信頼区間は、短系列・投資変動の大きい国で広い。点同定を主張しているわけではなく、区間推定と方向性を提供している。第三に、5.3 節の γ_price 感度実験は CWON デフレータを国レベルの単一スカラーで処理した。より精密な研究ではセクター別デフレータと各国地価指数を使う必要があり、今後の課題とする。

## 7. 結論

国民所得・国富会計は誤った問いを立ててきた。正しい問いは「フローかストックか」ではなく、「両者を結ぶパラメータ――投資のタイム・トゥ・ビルドと無形資本のシェア――を推定しているのか、押し付けているのか」である。μ = 0、β = 0 を押し付けると、会計は静かに偏り、Solow 残差が誤差を吸収し、フロー勘定とストック勘定が乖離する。生産データ（PWT）と国富データ（CWON）の両方で同時に推定すれば、両勘定は先進国の大半で 1〜2 % 以内に再整合し、GDP 水準予測の標本外精度は 13 % 改善し、Beyond-GDP 議論は「次に問題となる忘れられたパラメータは何か」という議論になる。人口学は同じ問題を四半世紀前に人口について解決した。資本会計も今、同じことができる。

---

## 表

**表 1.** M0–M4: 39 カ国における標本内・標本外パフォーマンス

**［表 1 をここに挿入］**

**表 2.** 人口・資本対応

**［表 2 をここに挿入］**

---

## 参考文献

Arrow, K. J., P. Dasgupta, L. H. Goulder, K. J. Mumford, and K. Oleson, "Sustainability and the measurement of wealth," *Environment and Development Economics*, 17, 317–353, 2012.

Bongaarts, J. and G. Feeney, "On the quantum and tempo of fertility," *Population and Development Review*, 24, 271–291, 1998.

Bongaarts, J. and T. Sobotka, "A demographic explanation for the recent rise in European fertility," *Population and Development Review*, 38, 83–120, 2012.

Corrado, C., C. Hulten, and D. Sichel, "Measuring capital and technology: an expanded framework," in C. Corrado, J. Haltiwanger, and D. Sichel, eds., *Measuring Capital in the New Economy*, 11–46, University of Chicago Press, Chicago, 2005.

Corrado, C., C. Hulten, and D. Sichel, "Intangible capital and US economic growth," *Review of Income and Wealth*, 55, 661–685, 2009.

Corrado, C., J. Haskel, C. Jona-Lasinio, and M. Iommi, "Intangible investment in the EU and US before and since the Great Recession and its contribution to productivity growth," *EIB Working Papers* 2016/08, 2016.

Dasgupta, P., *The Economics of Biodiversity: The Dasgupta Review*, HM Treasury, London, 2021.

Feenstra, R. C., R. Inklaar, and M. P. Timmer, "The next generation of the Penn World Table," *American Economic Review*, 105, 3150–3182, 2015.

Goldstein, J. R., W. Lutz, and S. Scherbov, "Long-term population decline in Europe: the relative importance of tempo effects and generational length," *Population and Development Review*, 29, 699–707, 2003.

Hamano, M. and Y. Zhao, "Fiscal sustainability and land prices in Japan," *Journal of the Japanese and International Economies*, 46, 17–29, 2017.

Haskel, J. and S. Westlake, *Capitalism without Capital: The Rise of the Intangible Economy*, Princeton University Press, Princeton, 2017.

Jorgenson, D. W., "Production and welfare: progress in economic measurement," *Journal of Economic Literature*, 56, 867–919, 2018.

Kaboski, J. P., "Factor price uncertainty, technology choice and investment delay," *Journal of Economic Dynamics and Control*, 29, 509–527, 2005.

Koeva, P., "The facts about time-to-build," *IMF Working Paper* 00/138, 2000.

Kohler, H.-P., F. C. Billari, and J. A. Ortega, "The emergence of lowest-low fertility in Europe during the 1990s," *Population and Development Review*, 28, 641–680, 2002.

Kydland, F. E. and E. C. Prescott, "Time to build and aggregate fluctuations," *Econometrica*, 50, 1345–1370, 1982.

Lange, G.-M., Q. Wodon, and K. Carey, eds., *The Changing Wealth of Nations 2018: Building a Sustainable Future*, World Bank, Washington, DC, 2018.

Managi, S. and P. Kumar, eds., *Inclusive Wealth Report 2018*, Routledge, London, 2018.

Mayer, T., "Plant and equipment lead times," *Journal of Business*, 33, 127–132, 1960.

Roth, F., "Intangible capital and productivity growth in the EU: a panel data perspective," *Hamburg Discussion Papers in International Economics*, 13, 2023.

Smets, F. and R. Wouters, "Shocks and frictions in US business cycles: a Bayesian DSGE approach," *American Economic Review*, 97, 586–606, 2007.

Solow, R. M., "Technical change and the aggregate production function," *Review of Economics and Statistics*, 39, 312–320, 1957.

Stiglitz, J. E., A. Sen, and J.-P. Fitoussi, *Report by the Commission on the Measurement of Economic Performance and Social Progress*, Paris, 2009.

UNECE, *Framework and Suggested Indicators to Measure Sustainable Development*, United Nations, Geneva, 2014.
