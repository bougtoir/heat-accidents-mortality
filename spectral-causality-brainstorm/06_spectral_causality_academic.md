# スペクトル因果性の数理的基礎

**— 有向グラフのスペクトル理論に基づく因果推論の新しいアプローチ —**

> **想定読者**: 線形代数（固有値分解）と基礎的な確率論を既習の学部上級生〜大学院生。因果推論やグラフ理論の事前知識は不要。

---

## 目次

1. [導入：因果推論とスペクトル理論の交差点](#1-導入)
2. [準備：グラフラプラシアンの基礎](#2-準備)
3. [磁気ラプラシアン：方向性の複素位相符号化](#3-磁気ラプラシアン)
4. [スペクトル因果性の定式化](#4-スペクトル因果性の定式化)
5. [Hodge分解：因果フローの直交分解](#5-hodge分解)
6. [既存手法との関係](#6-既存手法との関係)
7. [実データによる例示](#7-実データによる例示)
8. [理論的課題と展望](#8-理論的課題と展望)

---

## 1. 導入

### 1.1 問題設定

因果推論（causal inference）の中心的な問い — 「$X$ は $Y$ の原因か？」— に対して、様々なアプローチが提案されてきた。代表的なものとして：

- **構造方程式モデル（SEM）と do-calculus** (Pearl, 2009): 介入に基づく反事実的定義
- **潜在結果モデル** (Rubin, 1974): 処置群と対照群の潜在結果の差
- **LiNGAM** (Shimizu et al., 2006): データの非ガウス性を利用した因果方向の同定
- **Granger因果** (Granger, 1969): 時系列における予測改善に基づく因果性

本稿では、これらとは異なる原理 — **グラフのスペクトル構造（固有値・固有ベクトル）から因果的方向性を読み取る** — に基づく手法を定式化する。この手法を**スペクトル因果性（spectral causality）**と呼ぶ。

### 1.2 基本的着想

ある $n$ 個の変数 $\{X_1, \dots, X_n\}$ の間に因果関係があるとする。これらの関係を**有向グラフ** $G = (V, E)$ で表現したとき、グラフの**ラプラシアン行列**のスペクトル（固有値と固有ベクトル）には、因果的方向性に関する情報が含まれうる。

**注意 1.1**（グラフの種類と因果モデル）因果推論で用いるグラフは必ずしも**DAG（有向非巡回グラフ）**に限定されない。LiNGAMはDAG仮定を置くが、現実の生体システムにはフィードバックループ（例：炎症 → 臓器障害 → 炎症）が普遍的に存在する。本稿のスペクトル因果性は**有向巡回グラフ（DCG; directed cyclic graph）**も許容する — Hodge分解（§5）がカール成分として循環フローを定量化するためである。図1に、LiNGAMがDAG仮定の下で推定した因果構造の例を示す。

![図1: DirectLiNGAMによる推定因果DAG（UCI心疾患データ, n=297）](figures/fig6_causal_dag.png)

*図1: DirectLiNGAM (Shimizu et al., 2011) により推定された因果DAG。UCI心疾患データ（Cleveland subset, n=297）の5つの臨床変数に対して適用。上流（原因側）から下流（結果側）へ因果的フローが流れる。青線は正の因果効果、赤線は負の因果効果を示す。LiNGAMはDAG仮定を置くため循環は許容されないが、スペクトル因果性ではHodge分解によりフィードバック（循環成分）も定量化可能である。*

特に、**磁気ラプラシアン（magnetic Laplacian）**と呼ばれるエルミート行列を用いると、エッジの方向性が固有ベクトルの**複素位相（complex phase）**として符号化され、因果方向の推定が可能になる。

### 1.3 本稿の構成

§2でグラフラプラシアンの基礎を復習し、§3で磁気ラプラシアンを導入する。§4でスペクトル因果性を厳密に定式化し、§5でHodge分解との関係を示す。§6で既存手法（LiNGAM、Granger因果）との比較を行い、§7で実データ（UCI心疾患データ）への適用例を示す。§8で理論的課題を議論する。

---

## 2. 準備：グラフラプラシアンの基礎

### 2.1 無向グラフのラプラシアン

**定義 2.1**（グラフラプラシアン）
重み付き無向グラフ $G = (V, E, w)$（$|V| = n$, $w: E \to \mathbb{R}_{>0}$）に対して、**重み付き隣接行列** $W \in \mathbb{R}^{n \times n}$, **次数行列** $D = \operatorname{diag}(d_1, \dots, d_n)$（$d_i = \sum_j W_{ij}$）を用いて、以下を定義する：

$$L = D - W \quad \text{（非正規化ラプラシアン）}$$

$$\mathcal{L} = I - D^{-1/2} W D^{-1/2} \quad \text{（正規化ラプラシアン）}$$

**命題 2.1**（基本性質）
$L$ および $\mathcal{L}$ について以下が成り立つ：

(i) $L$ は対称半正定値行列であり、固有値は $0 = \lambda_1 \leq \lambda_2 \leq \dots \leq \lambda_n$ を満たす。

(ii) $\lambda_1 = 0$ に対応する固有ベクトルは $\mathbf{1} = (1, \dots, 1)^\top$（定数ベクトル）。

(iii) $\lambda_2 > 0$ であることは、$G$ が連結であることと同値（**Fiedler値**）。

(iv) 任意のベクトル $f \in \mathbb{R}^n$ に対して、$f^\top L f = \sum_{(i,j) \in E} w_{ij}(f_i - f_j)^2 \geq 0$。

**証明のスケッチ**：(iv) は $L$ の二次形式を展開すれば直接示せる。(i) は (iv) から従う。(ii) は $L\mathbf{1} = \mathbf{0}$ の直接計算による。(iii) は代数的連結度の定理。 $\square$

性質 (iv) は重要である：$f^\top L f$ が小さいほど、$f$ は隣接ノードで類似した値をとる — つまり、ラプラシアンの低固有値固有ベクトルは**グラフ上で滑らかな信号**を表す。

### 2.2 スペクトル分解の幾何学的意味

$\mathcal{L}$ のスペクトル分解 $\mathcal{L} = U \Lambda U^\top$（$U = [u_1, \dots, u_n]$, $\Lambda = \operatorname{diag}(\lambda_1, \dots, \lambda_n)$）において：

- **$u_k$ の各成分 $u_k(i)$** = ノード $i$ が第 $k$ 固有モードにどれだけ「荷重（load）」するかを表す
- **$\lambda_k$** = 第 $k$ モードの「周波数」（大きいほど高周波 = 局所変動）
- **$u_2$**（第2固有ベクトル, Fiedler vector）は**グラフの最適2分割**を与える

この枠組みは、信号処理における**フーリエ変換のグラフ上への一般化**（Graph Signal Processing; GSP）の基礎となっている (Shuman et al., 2013)。

### 2.3 問題：無向ラプラシアンは方向性を失う

$L = D - W$ は**対称行列**であるため、エッジの方向性 $i \to j$ と $j \to i$ を区別できない。因果推論では「$X$ が $Y$ の原因」という方向性が本質的であり、無向ラプラシアンでは情報が不足する。

有向グラフのラプラシアン $L_d = D_{\text{out}} - W$（$D_{\text{out}}$ は出次数行列）を直接用いる手もあるが、$L_d$ は一般に**非対称**であり、固有値が**複素数**になりうる。これは理論的に扱いにくい。

---

## 3. 磁気ラプラシアン：方向性の複素位相符号化

### 3.1 物理的背景

磁気ラプラシアンの名前は量子力学に由来する。磁場 $\mathbf{B}$ 中の荷電粒子のハミルトニアンは $H = (\mathbf{p} - e\mathbf{A})^2 / 2m$（$\mathbf{A}$ はベクトルポテンシャル）であり、粒子が閉じた経路を一周すると Aharonov-Bohm 位相 $\exp(i \oint \mathbf{A} \cdot d\mathbf{r})$ を獲得する。この位相の**向き依存性**が、グラフ上のエッジ方向性の符号化に利用できる。

### 3.2 定義

**定義 3.1**（磁気ラプラシアン; de Resende & da Costa, 2020; Zhang et al., 2021）
重み付き有向グラフ $G = (V, E, w)$ と**電荷パラメータ** $q \in [0, 0.5]$ に対して、**エルミート隣接行列** $H^{(q)} \in \mathbb{C}^{n \times n}$ を以下で定義する：

$$H^{(q)}_{ij} = w_{ij} \cdot \exp\bigl(i \cdot 2\pi q \cdot \sigma_{ij}\bigr)$$

ここで $\sigma_{ij} \in \{-1, 0, +1\}$ はエッジの方向性符号であり：

$$\sigma_{ij} = \begin{cases} +1 & \text{if } i \to j \\\ -1 & \text{if } j \to i \\\ 0 & \text{if エッジなし} \end{cases}$$

重み $w_{ij}$ は対称化して用いる（$w_{ij} = w_{ji} = (w^{\text{orig}}_{ij} + w^{\text{orig}}_{ji})/2$）。

**正規化磁気ラプラシアン**を以下で定義する：

$$\mathcal{L}^{(q)} = I - D^{-1/2} H^{(q)} D^{-1/2}$$

ここで $D = \operatorname{diag}(d_1, \dots, d_n)$, $d_i = \sum_j |H^{(q)}_{ij}|$。

**命題 3.1**（磁気ラプラシアンの基本性質）

(i) $H^{(q)}$ はエルミート行列である：$H^{(q)}_{ji} = \overline{H^{(q)}_{ij}}$。

(ii) $\mathcal{L}^{(q)}$ はエルミート半正定値であり、固有値は**実数**かつ非負。

(iii) 固有ベクトルは一般に**複素数値**をとる。

(iv) $q = 0$ のとき、$\mathcal{L}^{(0)}$ は通常の正規化ラプラシアン $\mathcal{L}$ に退化する（方向情報なし）。

**命題 3.1 (i) の証明**：

$$H^{(q)}_{ji} = w_{ji} \cdot \exp(i \cdot 2\pi q \cdot \sigma_{ji})$$

$w_{ji} = w_{ij}$（対称化済み）かつ $\sigma_{ji} = -\sigma_{ij}$ より：

$$H^{(q)}_{ji} = w_{ij} \cdot \exp(-i \cdot 2\pi q \cdot \sigma_{ij}) = \overline{w_{ij} \cdot \exp(i \cdot 2\pi q \cdot \sigma_{ij})} = \overline{H^{(q)}_{ij}}$$

$\square$

### 3.3 電荷パラメータ $q$ の意味

$q$ は方向性に対する**感度**を制御するパラメータである：

| $q$ | 位相 $2\pi q$ | 効果 |
|---|---|---|
| $0$ | $0$ | 方向性を完全無視。$\exp(i \cdot 0) = 1$ より実行列に退化 |
| $0.25$ | $\pi/2$ | 最大方向性感度。$e^{i\pi/2} = i$, $e^{-i\pi/2} = -i$ |
| $0.5$ | $\pi$ | 方向を反転。$e^{i\pi} = -1$ |

**注意 3.1** $q = 0.25$ のとき、$H^{(q)}_{ij} = i \cdot w_{ij}$（$i \to j$ のエッジ）かつ $H^{(q)}_{ji} = -i \cdot w_{ij}$ となり、方向性が虚数単位 $i$ によって最も鋭く分離される。

### 3.4 固有ベクトルの複素位相と方向性

$\mathcal{L}^{(q)}$ の固有ベクトル $u_k \in \mathbb{C}^n$ の各成分は極形式で表すことができる：

$$u_k(j) = |u_k(j)| \cdot \exp\bigl(i \cdot \theta_k(j)\bigr)$$

ここで $|u_k(j)|$ は**振幅**（ノード $j$ がモード $k$ にどれだけ荷重するか）、$\theta_k(j) = \arg(u_k(j))$ は**位相角**である。

**核心的な主張**：$q > 0$ のとき、位相角 $\theta_k(j)$ の順序が因果的フローの方向を反映する。

直感的には、因果の上流（原因側）のノードと下流（結果側）のノードは、固有ベクトル上で異なる位相角を持つ。これは、磁場中の電子がループを一周する際に方向依存の位相を獲得するのと類似のメカニズムである。

---

## 4. スペクトル因果性の定式化

### 4.1 ユーティリティ有向グラフ

変数間の因果的方向性を符号化するために、**ユーティリティ（臨床的有用性）の非対称性**を用いる。

**定義 4.1**（ユーティリティ有向グラフ）
$n$ 個の変数 $\{X_1, \dots, X_n\}$ に対して、**ユーティリティ関数** $U: \{1, \dots, n\}^2 \to \mathbb{R}_{\geq 0}$ を：

$$U(i, j) = \text{「変数 } X_i \text{ の情報が変数 } X_j \text{ に関する問いにどれだけ有用か」}$$

と定義する。**ユーティリティ有向グラフ** $G_U = (V, E, w, \sigma)$ は：

- $V = \{1, \dots, n\}$
- $w(i, j) = \bigl(U(i, j) + U(j, i)\bigr) / 2$（対称化された重み）
- $\sigma(i, j) = \operatorname{sign}\bigl(U(i, j) - U(j, i)\bigr)$（方向性符号）

で定義される。

**注意 4.1** ユーティリティ関数 $U$ の具体的な構成には、(a) 臨床知識の手動符号化、(b) 大規模言語モデル（LLM）による自動生成、(c) データ駆動の予測性指標、あるいはこれらの組み合わせが考えられる。本稿では $U$ は所与とし、その構成方法の議論は§8に譲る。

### 4.2 スペクトル因果結合度と因果方向

**定義 4.2**（スペクトル因果結合度; Spectral Causal Coupling, SCC）
磁気ラプラシアン $\mathcal{L}^{(q)}$ の固有値分解 $\mathcal{L}^{(q)} = U \Lambda U^*$（$U = [u_1, \dots, u_n]$, $\Lambda = \operatorname{diag}(\lambda_1, \dots, \lambda_n)$）に対して、ノード $i, j$ の**スペクトル因果結合度**を：

$$\mathrm{SCC}(i, j) = \sum_{k=1}^n f(\lambda_k) \cdot |u_k(i)| \cdot |u_k(j)| \cdot \cos\bigl(\theta_k(i) - \theta_k(j)\bigr)$$

と定義する。ここで $f: \mathbb{R}_{\geq 0} \to \mathbb{R}_{\geq 0}$ は固有値重み関数（典型的には $f(\lambda) = \lambda$）、$\theta_k(i) = \arg(u_k(i))$。

**命題 4.1** SCC は**対称**である：$\mathrm{SCC}(i, j) = \mathrm{SCC}(j, i)$。

**証明**：$\cos(\alpha - \beta) = \cos(\beta - \alpha)$ より直ちに従う。 $\square$

SCCは因果的結合の**強さ**を測るが、**方向**は測れない。方向の定量化には以下を用いる。

**定義 4.3**（スペクトル因果方向; Spectral Causal Direction, SCD）

$$\mathrm{SCD}(i, j) = \sum_{k=1}^n f(\lambda_k) \cdot |u_k(i)| \cdot |u_k(j)| \cdot \sin\bigl(\theta_k(i) - \theta_k(j)\bigr)$$

**命題 4.2** SCD は**反対称**である：$\mathrm{SCD}(i, j) = -\mathrm{SCD}(j, i)$。

**証明**：$\sin(\alpha - \beta) = -\sin(\beta - \alpha)$ より直ちに従う。 $\square$

**系 4.1**（自己因果方向はゼロ）$\mathrm{SCD}(i, i) = 0$。

$\mathrm{SCD}(i, j) > 0$ は「$i$ から $j$ への因果的方向」を、$\mathrm{SCD}(i, j) < 0$ は逆方向を示唆する。

### 4.3 SCC と SCD の統一的理解

SCC と SCD は、複素内積の実部と虚部として統一的に理解できる。

**命題 4.3**（複素因果指標）
以下の**複素因果指標（Complex Causal Index, CCI）**を定義すると：

$$\mathrm{CCI}(i, j) = \sum_{k=1}^n f(\lambda_k) \cdot |u_k(i)| \cdot |u_k(j)| \cdot \exp\bigl(i(\theta_k(i) - \theta_k(j))\bigr)$$

SCC と SCD は CCI の実部と虚部に対応する：

$$\mathrm{SCC}(i, j) = \mathrm{Re}\bigl[\mathrm{CCI}(i, j)\bigr], \qquad \mathrm{SCD}(i, j) = \mathrm{Im}\bigl[\mathrm{CCI}(i, j)\bigr]$$

**証明**：$\exp(i\alpha) = \cos\alpha + i\sin\alpha$（Euler公式）を適用すればよい。 $\square$

**幾何学的解釈**：CCI を複素平面上のベクトルとみなすと、**偏角** $\arg(\mathrm{CCI}(i,j))$ が因果の方向を、**絶対値** $|\mathrm{CCI}(i,j)|$ が因果的結合の強さを表す。

### 4.4 SCD行列の性質

$n$ 個のノードに対する SCD 行列 $S \in \mathbb{R}^{n \times n}$（$S_{ij} = \mathrm{SCD}(i,j)$）は以下の性質を持つ：

**命題 4.4**

(i) $S$ は**歪対称（skew-symmetric）**：$S = -S^\top$。

(ii) $\operatorname{tr}(S) = 0$（対角成分はすべて0）。

(iii) $q = 0$ のとき $S = O$（ゼロ行列）。すなわち、方向性情報がなければ因果方向は推定できない。

**証明**：(i) は命題4.2の行列版。(ii) は系4.1から。(iii) は $q = 0$ のとき $\theta_k(i) = 0$ または $\pi$（実固有ベクトル）なので $\sin(\theta_k(i) - \theta_k(j)) = 0$。 $\square$

性質 (iii) は重要である：スペクトル因果性は、方向性情報（$q > 0$）が**なければ機能しない**。これはLiNGAMが非ガウス性なしには機能しないのと対照的である。

### 4.5 因果順序の推定

SCD行列から因果順序（causal ordering）を推定する方法を示す。

**定義 4.4**（スペクトル因果スコア）
各ノード $i$ の**スペクトル因果スコア**を：

$$s(i) = \sum_{j \neq i} \mathrm{SCD}(i, j)$$

と定義する。$s(i)$ が大きいノードほど「原因側（上流）」、小さいノードほど「結果側（下流）」と解釈される。

**注意 4.2** $S$ の歪対称性より $\sum_{i} s(i) = 0$ であり、スコアは零和（zero-sum）である。

---

## 5. Hodge分解：因果フローの直交分解

### 5.1 グラフ上の微分形式

有向グラフ上のエッジフローを微分幾何学の言葉で記述する。

**定義 5.1**（鎖複体）
グラフ $G = (V, E)$ に対して、以下の線形写像を定義する：

- **0-コチェイン** $C^0 = \mathbb{R}^{|V|}$（ノード上の関数）
- **1-コチェイン** $C^1 = \mathbb{R}^{|E|}$（エッジ上の関数 = フロー）
- **コバウンダリ作用素** $\delta_0: C^0 \to C^1$：$(\delta_0 f)(i \to j) = f(j) - f(i)$（勾配）
- **コバウンダリ作用素** $\delta_1: C^1 \to C^2$：三角形上のカール

### 5.2 Hodge分解定理

**定理 5.1**（グラフ上の Hodge 分解; Jiang et al., 2011）
任意の 1-コチェイン（エッジフロー）$\omega \in C^1$ は、以下のように直交分解される：

$$\omega = \underbrace{\delta_0 \phi}_{\text{勾配成分}} + \underbrace{\delta_1^* \psi}_{\text{カール成分}} + \underbrace{h}_{\text{調和成分}}$$

ここで $\delta_1^*$ は $\delta_1$ の随伴（adjoint）であり、3つの成分は互いに直交する。

**各成分の因果的解釈**：

| 成分 | 数学的意味 | 因果的解釈 |
|---|---|---|
| $\delta_0 \phi$（勾配） | ポテンシャル差に駆動されるフロー | **因果的フロー**（DAG的な一方向の流れ） |
| $\delta_1^* \psi$（カール） | 局所的な循環フロー | **フィードバックループ**（局所的な相互作用） |
| $h$（調和） | 大域的な循環フロー | **恒常性維持**（全身性の調節メカニズム） |

### 5.3 因果ポテンシャル

**定義 5.2**（因果ポテンシャル）
勾配成分 $\delta_0 \phi$ における**ポテンシャル関数** $\phi: V \to \mathbb{R}$ を**因果ポテンシャル**と呼ぶ。$\phi$ は以下の最小二乗問題の解として求まる：

$$\phi = \arg\min_{\tilde{\phi}} \sum_{(i,j) \in E} \bigl(\omega(i,j) - (\tilde{\phi}(j) - \tilde{\phi}(i))\bigr)^2$$

これは $\delta_0^* \delta_0 \phi = \delta_0^* \omega$、すなわちグラフラプラシアンに関する**ポアソン方程式**：

$$L \phi = \delta_0^* \omega$$

に帰着する。$L$ が半正定値であるため、$\phi$ は定数の不定性を除いて一意に定まる。

**命題 5.1**（因果ポテンシャルとLiNGAM因果順序の関係）
エッジフロー $\omega$ が完全なDAGの因果効果を表すとき（すなわちカール成分と調和成分がゼロ）、$\phi$ によるノードの順序付けはDAGのトポロジカルソートに一致する。

**注意 5.1** 実際のデータでは $\omega$ は完全なDAGからのフローとは限らず、カール成分（フィードバック）が存在する。Hodge分解の勾配成分のエネルギー比：

$$r_{\text{gradient}} = \frac{\|\delta_0 \phi\|^2}{\|\omega\|^2}$$

は、データがDAG的構造にどの程度適合するかの指標となる。$r_{\text{gradient}} \approx 1$ ならばDAG仮定が妥当、$r_{\text{gradient}} \ll 1$ ならばフィードバックが支配的である。

---

## 6. 既存手法との関係

### 6.1 LiNGAMとの比較

LiNGAM (Linear Non-Gaussian Acyclic Model; Shimizu et al., 2006) は以下の構造方程式モデルを仮定する：

$$\mathbf{x} = B\mathbf{x} + \mathbf{e}, \qquad \mathbf{e} \sim \text{非ガウス独立}$$

ここで $B$ は因果効果行列（$B_{ij} \neq 0$ ⇔ $X_j \to X_i$）。$(I - B)$ が因果順序に対応する置換で下三角行列になることが、同定の鍵である。

| 観点 | LiNGAM | スペクトル因果性 |
|---|---|---|
| **同定の原理** | 非ガウス性（分布の高次モーメント） | ユーティリティ非対称性（情報的有用性の方向差） |
| **仮定** | 線形, 非ガウス, DAG, 共通原因なし | ユーティリティ非対称性が因果方向を反映 |
| **出力** | 因果効果行列 $B$（変数ペアの効果量） | SCD行列 $S$（方向性スコア）+ 因果ポテンシャル $\phi$ |
| **フィードバック** | 不可（DAG仮定） | Hodge分解のカール成分で定量化 |
| **識別可能性** | 理論的保証あり (Shimizu et al., 2006) | 理論的保証なし（仮説段階） |

**重要な相違点**：LiNGAMはデータの**統計的性質**（分布の形状）のみから因果方向を推定するのに対し、スペクトル因果性はユーティリティ関数を通じて**ドメイン知識**を注入する。これは利点でもあり、限界でもある — ユーティリティ関数の品質に結果が依存するためである。

### 6.2 Granger因果との比較

Granger因果 (Granger, 1969) は時系列データに対して、「$X$ の過去の値が $Y$ の予測を（$Y$ の過去だけのモデルを超えて）改善するか」で因果方向を定義する。

スペクトル因果性との主な違いは：

- Granger因果は**時間的先行性**に基づくが、スペクトル因果性は**横断データ**にも適用可能
- Granger因果は**変数ペア**の検定だが、スペクトル因果性は**グラフ全体のスペクトル構造**を利用

### 6.3 因果の梯子における位置づけ

Pearl (2009) が提唱した「因果の梯子（Ladder of Causation）」に照らすと：

| レベル | 問い | 代表手法 |
|---|---|---|
| **3: 反事実** | 「もし $X = x$ だったら $Y$ はどうなっていたか？」 | 潜在結果モデル, do-calculus |
| **2: 介入** | 「$X$ を操作したら $Y$ は変わるか？」 | RCT, IV, メンデルランダム化 |
| **1.5: 情報的因果** ★ | 「$X$ を知ると $Y$ について何が分かるか？」 | **スペクトル因果性**, Utility Causality |
| **1: 関連** | 「$X$ と $Y$ は共変動するか？」 | 相関, 回帰 |

スペクトル因果性は Level 2（介入的因果）を直接扱うものではない。むしろ、Level 1（相関）よりは深いが Level 2 よりは浅い、**情報的因果性**の定量化として位置づけられる。

### 6.4 Hill の9基準とスペクトル因果性

疫学における因果判断の古典的枠組みである Hill の9基準 (Hill, 1965) に照らすと、スペクトル因果性は従来手法がカバーしていなかった基準に貢献する：

| Hill 基準 | 従来手法のカバー状況 | スペクトル因果性の貢献 |
|---|---|---|
| H1: 強さ（Strength） | ◎ 効果量の推定 | ○ SCD の絶対値 |
| H2: 一貫性（Consistency） | △ 個別研究に依存 | ○ 手法間一致で自動評価 |
| H3: 特異性（Specificity） | ◎ 変数ペアの同定 | △ テーマレベルでの同定 |
| H4: 時間性（Temporality） | ◎ 時系列で直接扱う | ○ 位相角の順序で符号化 |
| H5: 量反応（Dose-response） | ○ 非線形モデルで扱える | △ 重みの連続性で部分的 |
| H6: 妥当性（Plausibility） | **—** 手法なし | **◎** ユーティリティを通じて知識注入 |
| H7: 整合性（Coherence） | **—** 主観的判断に依存 | **◎** Eigentheme が既知概念と整合 |
| H8: 実験（Experiment） | ◎ RCT | — |
| H9: 類似性（Analogy） | **—** 手法なし | **◎** Eigentheme のスペクトル類似性 |

**核心的発見**：既存の計算的因果推論手法は H1, H3, H4, H8 に集中しており、H6（生物学的妥当性）, H7（整合性）, H9（類似性）は「研究者の主観」に委ねられてきた。スペクトル因果性/Utility Causality は、この空白を計算可能にする最初の試みとして位置づけられる（図2）。

![図2: Hill の9基準に対する各手法のカバレッジ](figures/fig5_hill_radar.png)

*図2: Hill の9基準に対する各手法のカバレッジをレーダーチャートで表示。LiNGAMは H1（強さ）と H3（特異性）に優れるが H6/H7/H9 を欠く。Utility Causality は H6（妥当性）、H7（整合性）、H9（類似性）をカバー。アンサンブル（ECD）は両者を統合し、ほぼ全基準をカバーする。*

---

## 7. 実データによる例示

### 7.1 データと変数

UCI Heart Disease Dataset (Cleveland subset; Detrano et al., 1989) の連続変数5つを用いた：

$$\mathbf{X} = \bigl(X_1, X_2, X_3, X_4, X_5\bigr) = \bigl(\text{Age}, \text{RestingBP}, \text{Cholesterol}, \text{MaxHR}, \text{STDepression}\bigr)$$

標本数 $n = 297$。各変数を標準化（平均0, 分散1）して用いた。

### 7.2 LiNGAM による因果順序（ベースライン）

DirectLiNGAM (Shimizu et al., 2011) を適用し、因果順序と因果効果行列 $B$ を推定した：

**推定因果順序**: $X_1 \prec X_4 \prec X_5 \prec X_2 \prec X_3$（Age → MaxHR → STDep → RestBP → Chol）

**主要な因果効果**:
- $B_{42} = -0.395$: Age → MaxHR（加齢による最大心拍数低下）
- $B_{21} = +0.309$: Age → RestingBP（加齢による血圧上昇）
- $B_{54} = -0.348$: MaxHR → STDepression（運動耐容能低下による心筋虚血）

### 7.3 磁気ラプラシアンの固有ベクトル

ユーティリティ有向グラフを構築し（$\alpha = 0.6$ で臨床知識と相関情報を混合）、$q \in \{0, 0.1, 0.25\}$ で磁気ラプラシアンを計算した。

**$q = 0$**（方向性なし）：全固有ベクトルは実数値。ノード間の位相差はすべて $0$ または $\pi$。方向性情報は失われている。

**$q = 0.25$**（最大方向性感度）：固有ベクトルが複素数値をとり、各ノードの位相角 $\theta_k(j)$ が分離する。

第2固有ベクトル $u_2$ の位相角：

| 変数 | $|u_2|$（振幅） | $\theta_2$（位相角, 度） |
|---|---|---|
| Age | 0.53 | 0.0° |
| Resting BP | 0.35 | 164.6° |
| Cholesterol | 0.42 | -84.3° |
| Max HR | 0.47 | 34.7° |
| ST Depression | 0.44 | -40.6° |

位相角の分布は、因果的上流（Age, Max HR; 正の位相近傍）と下流（Cholesterol, ST Depression; 負の位相近傍）を分離している（図3）。

![図3: 磁気ラプラシアン固有ベクトルの複素平面上の分布](figures/fig2_magnetic_laplacian_q.png)

*図3: 磁気ラプラシアンの第2固有ベクトルを複素平面上にプロットした結果。$q=0$ では全点が実軸上に並ぶ（方向情報なし）。$q=0.1$, $q=0.25$ では変数が複素平面に展開し、位相角の順序が因果フローの方向を符号化する。*

### 7.4 Hodge 分解の結果

エッジフロー $\omega(i,j) = w(i,j) \cdot \sigma(i,j)$ に対して Hodge 分解を行った結果：

$$\|\delta_0 \phi\|^2 / \|\omega\|^2 = 85.9\% \quad \text{（勾配成分 = DAG的因果フロー）}$$

$$\|\delta_1^* \psi\|^2 / \|\omega\|^2 = 14.1\% \quad \text{（カール成分 = フィードバック）}$$

$r_{\text{gradient}} = 85.9\%$ は、このデータの変数間関係が概ねDAG的であることを示唆する。

**因果ポテンシャル** $\phi$（降順 = 因果的上流から）:

| 順位 | 変数 | $\phi$ |
|---|---|---|
| 1 | Age | 0.000 |
| 2 | Cholesterol | -0.168 |
| 3 | Resting BP | -0.204 |
| 4 | Max Heart Rate | -0.204 |
| 5 | ST Depression | -0.324 |

Age が最上流、ST Depression が最下流という結果は臨床的に妥当である（図4）。LiNGAM の因果順序（Age → MaxHR → ST → BP → Chol）とHodge因果ポテンシャル（Age → Chol → BP ≈ MaxHR → ST）の Kendall 順位相関は $\tau = 0.00$ であり、Ageが最上流という点では一致するが、中間変数の順序は大きく異なる。これは両手法が因果を異なる観点（LiNGAM: 統計的非ガウス性、Hodge: ユーティリティ非対称性）から捉えていることを反映している。

![図4: Hodge分解による情報フローの直交分解](figures/fig3_hodge_decomposition.png)

*図4: (A) Hodge分解の結果：85.9%が勾配成分（DAG的因果フロー）、14.1%がカール成分（フィードバックループ）。(B) 各変数の因果ポテンシャル $\phi$。Ageが最上流、ST Depressionが最下流。*

### 7.5 手法間比較の考察

3手法（LiNGAM, SCD, Hodge）の全10変数ペアに対する因果方向の比較では、一致するペアと不一致のペアが存在した（図5）。

**一致例** — Age → Cholesterol: 3手法すべてが同方向。加齢によるコレステロール上昇は医学的に確立。

**不一致例** — Age vs MaxHR: LiNGAMは Age → MaxHR（加齢で最大心拍数↓）を検出。スペクトル手法は逆方向を示す。これはスペクトル手法が「MaxHR が Age に関する問いに情報を提供する」という**情報的方向**を捉えている可能性がある。

手法間の**不一致そのものが情報的**である — 単純なDAG因果ではなく、フィードバックや交絡の存在を示唆する。

![図5: 3手法による因果方向の比較](figures/fig4_direction_comparison.png)

*図5: 全10変数ペアに対する因果方向の比較。LiNGAM（赤）、スペクトル因果方向SCD（青）、Hodgeポテンシャル（緑）。+1 = 第1変数が第2変数の原因、−1 = 逆方向。緑背景 = 3手法が一致。*

---

## 8. 理論的課題と展望

### 8.1 識別可能性

LiNGAM には明確な識別可能性条件（非ガウス＋線形＋DAG＋共通原因なし → 因果方向が一意に同定; Shimizu et al., 2006）がある。

スペクトル因果性には**現時点で識別可能性の理論がない**。すなわち、SCD が真の因果方向と一致する条件が明らかではない。今後の研究課題として：

**予想 8.1** 以下の条件下で、SCD は因果方向と一致する：
1. ユーティリティ非対称性 $U(i,j) - U(j,i)$ が真の因果方向と同符号
2. ユーティリティ重み $w(i,j)$ が因果効果の強さの単調関数
3. グラフがDAG的構造を持つ（$r_{\text{gradient}} \approx 1$）

条件 1 が最も制約的であり、ユーティリティ関数の構成方法に依存する。

### 8.2 ユーティリティ関数の構成

ユーティリティ関数 $U(i,j)$ をどのように構成するかは未解決の問題である。考えうる手法として：

(a) **専門家符号化**: 臨床専門家が手動で $U(i,j)$ を設定。再現性に難あり。

(b) **LLMベース**: 大規模言語モデルに「変数 $X_i$ の情報は変数 $X_j$ に関する問いにどの程度有用か？」と質問し、応答を数値化。モデル依存性が課題。

(c) **データ駆動**: $U(i,j) = |\hat{\rho}_{ij}|$（予測的相関の非対称性）。純粋にデータ駆動だが、交絡に弱い。

(d) **ハイブリッド**: $U(i,j) = \alpha \cdot U_{\text{expert}}(i,j) + (1 - \alpha) \cdot U_{\text{data}}(i,j)$。本稿の実データ解析ではこの手法を用いた（$\alpha = 0.6$）。

### 8.3 電荷パラメータ $q$ の選択

$q$ の値は結果に大きく影響する。$q$ の選択基準として：

- **交差検証**: LiNGAM等の既存手法との因果方向一致率を最大化する $q$ を選択
- **安定性**: $q$ の微小変動に対するSCDの安定性（感度解析）
- **理論的**: $q = 0.25$ が数学的に「最大方向性感度」を与える（注意3.1参照）

### 8.4 スケーラビリティ

- 磁気ラプラシアンの固有分解：$O(n^3)$。ランダム化SVDで $O(nk^2)$（上位 $k$ 個のみ）
- Hodge分解：$O(|E|)$（スパースグラフなら高速）
- ユーティリティ関数の計算：$O(n^2)$ ペアに対する LLM 呼び出しがボトルネック

### 8.5 今後の方向性

1. **識別可能性の理論構築**: 特殊ケース（ツリーDAG + 線形SEM）での SCD と因果方向の一致証明
2. **アンサンブル因果推定**: $\mathrm{ECD}(i,j) = \alpha \cdot \mathrm{LiNGAM}(i,j) + \beta \cdot \mathrm{SCD}(i,j) + \gamma \cdot \mathrm{Granger}(i,j)$ の統計的性質
3. **経時データへの拡張**: 時間的ユーティリティグラフの構築と Eigentrajectories の抽出
4. **大規模データでの検証**: 日本健診コホート（$n > 10^5$; Okuda et al., 2025）やMIMIC-IV等

---

## 記号一覧

| 記号 | 意味 |
|---|---|
| $G = (V, E, w)$ | 重み付き（有向）グラフ |
| $W$, $D$ | 隣接行列, 次数行列 |
| $L = D - W$ | 非正規化グラフラプラシアン |
| $\mathcal{L} = I - D^{-1/2}WD^{-1/2}$ | 正規化グラフラプラシアン |
| $H^{(q)}$ | エルミート隣接行列（磁気ラプラシアン用） |
| $\mathcal{L}^{(q)} = I - D^{-1/2}H^{(q)}D^{-1/2}$ | 正規化磁気ラプラシアン |
| $q$ | 電荷パラメータ（方向性感度, $[0, 0.5]$） |
| $\sigma_{ij}$ | エッジ方向性符号（$\{-1, 0, +1\}$） |
| $u_k$, $\lambda_k$ | $k$ 番目の固有ベクトル, 固有値 |
| $\theta_k(i) = \arg(u_k(i))$ | ノード $i$ の第 $k$ モードにおける位相角 |
| $U(i,j)$ | ユーティリティ関数 |
| $\mathrm{SCC}(i,j)$ | スペクトル因果結合度（対称） |
| $\mathrm{SCD}(i,j)$ | スペクトル因果方向（反対称） |
| $\mathrm{CCI}(i,j)$ | 複素因果指標（$\mathrm{SCC} + i \cdot \mathrm{SCD}$） |
| $\phi(i)$ | 因果ポテンシャル（Hodge分解より） |
| $r_{\text{gradient}}$ | 勾配エネルギー比（DAG適合度） |

---

## 参考文献

1. Pearl, J. (2009). *Causality: Models, Reasoning, and Inference* (2nd ed.). Cambridge University Press.
2. Shimizu, S., Hoyer, P.O., Hyvärinen, A. & Kerminen, A. (2006). A linear non-Gaussian acyclic model for causal discovery. *Journal of Machine Learning Research*, 7, 2003–2030.
3. Shimizu, S., Inazumi, T., Sogawa, Y., Hyvärinen, A., Kawahara, Y., Washio, T., Hoyer, P.O. & Bollen, K. (2011). DirectLiNGAM: A direct method for learning a linear non-Gaussian structural equation model. *Journal of Machine Learning Research*, 12, 1225–1248.
4. Hill, A.B. (1965). The environment and disease: Association or causation? *Proceedings of the Royal Society of Medicine*, 58, 295–300.
5. Granger, C.W.J. (1969). Investigating causal relations by econometric models and cross-spectral methods. *Econometrica*, 37(3), 424–438.
6. Shuman, D.I., Narang, S.K., Frossard, P., Ortega, A. & Vandergheynst, P. (2013). The emerging field of signal processing on graphs. *IEEE Signal Processing Magazine*, 30(3), 83–98.
7. Zhang, X., He, Y., Bruber, N., Hooi, B. & Zhu, L. (2022). MagNet: A neural network for directed graphs. In *Advances in Neural Information Processing Systems* (NeurIPS 2021).
8. de Resende, B.M.F. & da Costa, L.F. (2020). Characterization and comparison of large directed networks through the spectra of the magnetic Laplacian. *Chaos*, 30(7), 073141.
9. Seifert, B., Wendler, C. & Püschel, M. (2023). Causal Fourier analysis on directed acyclic graphs and posets. *IEEE Transactions on Signal Processing*, 71, 3516–3530.
10. Jiang, X., Lim, L.H., Yao, Y. & Ye, Y. (2011). Statistical ranking and combinatorial Hodge theory. *Mathematical Programming*, 127, 203–244.
11. Maehara, K. & Ohkawa, Y. (2019). Modeling latent flows on single-cell data using the Hodge decomposition. *bioRxiv*.
12. Kotoku, J. et al. (2020). Causal relations of health indices inferred statistically using the DirectLiNGAM algorithm from a cross-sectional study. *PLOS ONE*, 15(12), e0243229.
13. Okuda, S. et al. (2025). Operationalizing longitudinal causal discovery under real-world workflow constraints. *arXiv:2602.23800*.
14. Detrano, R. et al. (1989). International application of a new probability algorithm for the diagnosis of coronary artery disease. *American Journal of Cardiology*, 64, 304–310.
15. Rubin, D.B. (1974). Estimating causal effects of treatments in randomized and nonrandomized studies. *Journal of Educational Psychology*, 66(5), 688–701.
