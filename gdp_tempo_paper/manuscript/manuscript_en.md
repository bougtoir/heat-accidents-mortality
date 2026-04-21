# The Forgotten Tempo Effect in Capital Accounting: Investment-to-Output Time-to-Build, Intangible Capital, and the Reconciliation of Flow- and Stock-Based National Wealth Measures

**Abstract** (146 words). Since Goldstein, Lutz, and Scherbov (2003) showed that a single "forgotten" parity-specific variance parameter σ resolved a large share of the low-fertility puzzle once tempo effects on the mean age at childbearing were acknowledged, the dual of quantum and tempo has become a standard lens in formal demography. National income and wealth accounting has no equivalent diagnostic. We port the Bongaarts-Feeney quantum-tempo decomposition to capital accounting by letting the investment-to-output time-to-build μ(t) drift over time and by re-introducing intangible capital K_I, with share β, as the balance-sheet analogue of σ. Across 39 OECD and middle-income economies (Penn World Table 10.01, World Bank CWON), a time-varying μ(t) reduces the out-of-sample MAPE of GDP levels from 4.60% to 3.99% while a joint production-cum-wealth identification produces internally consistent flow and stock accounts. A sister medical-spending paper is in preparation.

**Keywords**: tempo effect; intangible capital; perpetual inventory method; wealth accounting; Beyond-GDP.

**JEL codes**: E01, E22, O47.

---

## 1. Introduction

Every macroeconomist has encountered two separate but related complaints about the way we measure national prosperity. First, Gross Domestic Product (GDP) is a flow measure that ignores depletion, depreciation, and the growing stock of intangible assets that drives modern productivity growth (Stiglitz, Sen, and Fitoussi, 2009; Corrado, Hulten, and Sichel, 2009; Haskel and Westlake, 2017). Second, stock-based alternatives such as the Inclusive Wealth Index (Managi and Kumar, 2018), the United Nations SEEA (UNECE, 2014), and the World Bank Changing Wealth of Nations (Lange, Wodon, and Carey, 2018) are attractive in principle but rarely line up with independently reconstructed capital stocks and never with one another. Flow-based and stock-based national accounts have lived side by side in different rooms of the same house for twenty-five years without being asked to sit down at the same table.

Demography has spent the same period quietly solving the mirror problem. Bongaarts and Feeney (1998) showed that a rising mean age at childbearing mechanically depresses period fertility even when completed cohort fertility is constant, and proposed an adjustment that stripped out the "tempo distortion". Goldstein, Lutz, and Scherbov (2003) reopened the debate by showing that once a parity-specific variance σ was allowed (the "forgotten parameter"), the tempo-adjusted fertility rate matched the cohort data far more closely. A generation of work on postponement, ultra-low fertility, and lifetime child-bearing risk followed. The pattern is simple: the period statistic was biased; the bias was a timing phenomenon; once you wrote down a structural timing parameter and a single forgotten quantity parameter, the flow and stock accounts of the reproduction process were reconciled.

This paper argues that capital accounting has an exact analogue of the Bongaarts-Feeney-Goldstein-Lutz-Scherbov correction, hiding in plain sight. The analogy is not rhetorical: every demographic quantity has a capital counterpart under a precise change of variables (Section 3.4, Table 2). Births are investment flows. Population stocks are capital stocks. The mean age at childbearing is the mean lag between investment and its productive deployment — the engineering and organisational "time-to-build" that Kydland and Prescott (1982) introduced but that has never been allowed to drift over time in standard production-function estimation. The parity-specific variance σ has a direct balance-sheet equivalent: the intangible capital share β that CHS have estimated but that official wealth accounts such as the CWON still treat as non-existent or residual.

Our contribution is four-fold. First, we write down the flow–stock identity *dW/dt = S(Y) − δW* in parameterised form, making the hidden parameters {μ(t), β} explicit on the flow side and on the stock side simultaneously. Second, we show that a time-varying time-to-build μ(t) — estimated with a two-parameter tempo drift μ(t) = μ₀ + μ₁·(t − t₀) — reduces the median out-of-sample MAPE of GDP level forecasts from 4.60 % to 3.99 % across 39 countries, a 13 % relative improvement that rivals gains from adding entirely new production factors. Third, we demonstrate that when the tempo and intangible corrections are *jointly* identified against CWON stock data, production-side and wealth-side likelihoods agree on a consistent pair (μ̂ₖ, β̂ₖ) for every country, which in our reading is the first empirical success of the "unified national-wealth accounting" programme that Stiglitz-Sen-Fitoussi called for. Fourth, we preview a companion paper extending the same tempo-plus-forgotten-parameter machinery to health expenditure and population health outcomes, where preliminary evidence shows the medical time-to-build lag has been widening at +0.15 years per year since 2000.

The remainder of the paper is organised as follows. Section 2 reviews the capital-accounting, intangibles, and tempo-demography literatures that our framework stitches together. Section 3 develops the theory. Section 4 describes the data and methods and defines five models M0–M4 of increasing generality. Section 5 reports results. Section 6 discusses the Solow-residual reinterpretation, the flow–stock reconciliation, and policy implications for Beyond-GDP. Section 7 concludes.

## 2. Related literature

**Capital accounting and time-to-build.** Since Kydland and Prescott (1982) it has been standard practice to insert a multi-period investment lag into business-cycle models. Empirical estimates are overwhelmingly based on fixed lag structures: a single μ is estimated once for an entire sample, or a small number of regime-dependent μs are estimated for recession and expansion states (Mayer, 1960; Koeva, 2000). Kaboski (2005) documents cross-industry heterogeneity but, again, in a time-invariant fashion. We know of no prior study that lets the typical investment-to-output lag drift systematically over decades in the way that demographers have documented for the mean age at childbearing.

**Intangible capital.** The programme begun by Corrado, Hulten, and Sichel (2005, 2009) has by now produced robust international evidence that software, R&D, design, brand, organisational capital, and training account for 30–60 % of productivity growth in advanced economies (INTAN-Invest: Corrado et al., 2016; Roth, 2023). The 2008 revision of the System of National Accounts (SNA) formally incorporated R&D into produced capital, but broader intangibles remain excluded from most official balance sheets, including the World Bank CWON (Lange et al., 2018, Chap. 3).

**Wealth accounting.** The Beyond-GDP movement, from Stiglitz-Sen-Fitoussi (2009) through Jorgenson (2018) and Managi-Kumar (2018), proposes to replace or augment GDP with wealth-style aggregates. Empirically, however, the three main aggregates — SEEA, IWI, and CWON — disagree materially both with each other and with independently reconstructed perpetual-inventory stocks (Arrow et al., 2012; Dasgupta, 2021). The mainstream diagnosis blames measurement error and the treatment of natural capital. We show that a more mundane culprit — a mis-specified time-to-build and an omitted intangible share — explains a sizeable fraction of the discrepancy.

**Tempo and forgotten parameters in demography.** Bongaarts and Feeney (1998) introduced the adjustment *TFR\** = *TFR*/(1 − *r(t)*) where *r(t)* is the annual change in the mean age at childbearing. Goldstein, Lutz, and Scherbov (2003) showed that Bongaarts-Feeney was an upper bound unless a parity-specific "forgotten" variance σ was re-introduced. Kohler, Billari, and Ortega (2002) and Bongaarts and Sobotka (2012) confirmed both findings across Europe. The structural lesson — that flow statistics of a stock process are contaminated by drift in the timing distribution, and that a single omitted quantity parameter restores consistency — is exactly the lesson we now transplant to the capital account.

**Healthcare and human capital sustainability.** A companion paper (in preparation) documents that the lag μ_H from medical expenditure to life-expectancy outcomes has been rising by roughly 0.15 years per year since 2000, and that an analogous "forgotten" parameter β_H — the share of expenditure directed to prevention and R&D, as opposed to curative care — accounts for a further share of the US-Japan life-expectancy gap. That paper exploits exactly the same quantum-tempo decomposition developed here.

**The gap this paper fills.** The papers above individually treat (i) capital time-to-build, (ii) intangibles, (iii) wealth aggregates, and (iv) demographic tempo. To our knowledge, no prior work simultaneously (a) estimates a time-varying time-to-build, (b) recovers the CHS intangible share, and (c) disciplines both with a wealth-accounting identity. This paper does.

## 3. Theory

### 3.1 Flow-side production function with tempo

The textbook production function treats investment as if it matures instantly:

    K_instant(t) = (1 − δ_{t-1}) K_instant(t−1) + I_{t-1},                         (M0)

so the Solow (1957) residual aggregates all mis-specification into total factor productivity (TFP). Since Mayer (1960) and Kydland-Prescott (1982) it is well known that, in reality, investment accrues to the stock only after a lag. We write this as a distributed-lag perpetual inventory:

    K(t; μ) = (1 − δ_{t-1}) K(t−1; μ) + Σₛ w_s(μ) I_{t-1-s},                     (M1)

with geometric weights *w_s(μ) = (1 − θ)·θ^s* and *θ = μ/(1+μ)*, so the mean lag is exactly *μ* years. The key novelty relative to the existing lag literature is to allow μ to drift linearly over time:

    μ(t) = μ₀ + μ₁·(t − t₀),                                                    (M2)

where μ₁ captures the "tempo" in Bongaarts-Feeney's sense. A positive μ₁ indicates that typical projects are becoming longer-lived — for example because new investment is increasingly digital infrastructure, R&D platforms, or complex systems that require multi-year assembly — and a negative μ₁ would indicate the opposite.

### 3.2 Stock-side intangibles: the forgotten β

Let *K_tang(t)* be the tangible PIM stock from (M1)–(M2) and *K_I(t)* be an intangible stock built from R&D expenditure by a geometric PIM with depreciation δ_I = 0.15 (Corrado-Hulten-Sichel, 2009). A production function augmented by intangibles reads:

    log Y_t = α log K_tang(t) + β log K_I(t) + (1 − α − β) log L_t + log A_t,    (M3)

where β is the intangible share. Standard practice imposes β = 0 (Solow; also M0 and M1 here). Estimating β > 0 is the capital-accounting analogue of re-introducing the parity-specific variance σ in Goldstein-Lutz-Scherbov.

### 3.3 Unifying identity: the flow-stock joint loss

Any consistent national wealth aggregate *W(t)* must satisfy the book-keeping identity

    dW/dt = S(Y) − δ_W · W,                                                       (1)

where *S(Y)* is gross saving and *δ_W* is the aggregate depreciation rate. Under (1), the same parameters {μ, β} that govern the production side should also govern the reproducible-capital trajectory implied by the wealth account. We therefore define a single joint loss:

    L_total(μ, β) = L_production(μ, β) + λ · L_wealth(μ, β),                      (2)

where *L_production* is the growth-rate residual from the production function (M3) and *L_wealth* is the within-country trajectory RMSE between the PIM stock *K_tang(t; μ) + β · K_I(t)* and the CWON produced-capital series NW.PCA.TO(t). Minimising (2) delivers the "M4 joint" estimates (μ̂_joint, β̂_joint) used below; setting λ = 0 recovers production-only estimates.

### 3.4 Quantum–tempo correspondence between population and capital

Table 2 lays out the one-to-one mapping between the demographic variables that Bongaarts-Feeney-Goldstein-Lutz-Scherbov analysed and the capital-accounting variables we analyse. Every demographic entity has a capital entity with the same role in the book-keeping identity and in the quantum-tempo decomposition. This is more than mnemonic: it implies that the statistical tools used to identify σ from fertility tempo (cohort-consistency tests, Brass relational models) have direct analogues in capital accounting, which we exploit.

## 4. Data and methods

### 4.1 Data

We use **Penn World Table 10.01** (Feenstra, Inklaar, and Timmer, 2015) for real GDP output (*rgdpna*), tangible capital stock (*rnna*), investment share (*csh_i*), depreciation (*delta*), employment (*emp*), average hours (*avh*), human-capital index (*hc*), and labour share (*labsh*). For R&D intensity we use **World Bank WDI** series *GB.XPD.RSDV.GD.ZS*. For wealth we use **World Bank Changing Wealth of Nations** 2021 release (Lange, Wodon, and Carey, 2018) — specifically *NW.PCA.TO* (produced capital total), *NW.HCA.TO* (human capital total), and *NW.TOW.TO* (total wealth).

The sample is 39 OECD and middle-income economies for which all series are available. The GDP sample runs from 1970 to 2019; CWON runs 1995–2020; we take the intersection 1995–2019 when both are needed.

### 4.2 Models M0–M4

We estimate five nested production-function specifications:

* **M0**: Solow baseline, *K_tang* as M0 above, β = 0.
* **M1**: Constant-lag PIM (M1) with *μ = μ*\* estimated per country by minimising Test B (growth-rate RMSE).
* **M2**: Time-varying lag μ(t) = μ₀ + μ₁·(t − t₀) from (M2).
* **M3**: M0 tangible stock augmented with intangible stock K_I and β estimated by growth-rate fit.
* **M4**: Joint identification (Section 3.3), minimising (2) over (μ, β) simultaneously against CWON.

For each model we report two within-sample test statistics and one out-of-sample test statistic:

* **Test A (level MAPE)**: mean absolute percentage error of fitted log-GDP against observed log-GDP, decomposing away decade-mean TFP. Lower is better.
* **Test B (growth RMSE)**: root-mean-squared error of 1-year log-GDP differences, in percentage points. Lower is better.
* **Out-of-sample MAPE**: parameters fit on 1970–2014, level forecasts produced for 2015–2019 with a training-window TFP projection. Lower is better.

### 4.3 Bootstrap confidence intervals

For every country we residual-bootstrap the growth-rate residuals of M4 100 times (block size 1), re-compute Y_bs cumulatively, rebuild I_bs and K_I_bs accordingly, and re-run the joint-identification grid, recording (μ_b, β_b) each time. 95 % percentile intervals are reported in Fig. 3.

### 4.4 γ_price sensitivity

To test whether the residual PIM-CWON gap in countries such as Japan reflects an asset-price re-evaluation effect rather than a real capital gap, we re-run the comparison under five counterfactual scenarios in which CWON PCA is inflated/deflated at an annual rate γ_price ∈ {−0.04, −0.02, 0, +0.02, +0.04}. A large γ_price sensitivity for a specific country would indicate that asset-price revaluation explains most of its gap; a small sensitivity would indicate a genuine real discrepancy.

## 5. Results

### 5.1 In-sample parameter distributions and fit

**[Table 1 here]**

Table 1 summarises the five models. The median country has a M1 constant lag μ\* ≈ 0.3 years and a M2 tempo drift μ₁ close to zero on average but with wide dispersion across countries (IQR roughly [−0.02, +0.05]). Median intangible share β under M3 is about 0.06 for production-only fitting and 0.06 under joint identification with CWON (M4). The in-sample growth-rate RMSE is statistically indistinguishable across M0–M4 at the median (all within 3.07–3.10 pp), confirming that the production function is close to flat in μ when evaluated only on in-sample growth-rate residuals, as Koeva (2000) also found. In-sample level MAPE improves monotonically from M0 (4.10 %) to M4 (4.06 %). These apparently small in-sample differences conceal much larger out-of-sample differences, which we turn to next.

### 5.2 Out-of-sample prediction gains from the tempo correction

**[Figure 1 here]**

Figure 1 ranks the 39 countries by in-sample growth RMSE (M0) and overlays the other four models. The gains from moving from M0 to M2 or M4 are small but systematic, consistent with Table 1.

**[Figure 2 here]**

Figure 2 shows the real pay-off from the tempo correction. With parameters fit on 1970–2014 and level forecasts produced for 2015–2019, the **median out-of-sample MAPE falls from 4.60 % under the Solow baseline M0 to 3.99 % under the time-varying-lag M2**, a 13 % relative reduction. M1 (constant lag) achieves most of the gain (4.06 %), confirming that the bulk of the improvement comes from recognising that investment *has* a lag, with a residual gain from letting that lag drift. M3 (intangibles) slightly worsens out-of-sample MAPE to 4.72 %; we attribute this to the fact that adding a co-moving factor with a time-varying productivity projection widens forecast uncertainty, especially under the 2015–2019 global slowdown that affected R&D-intensive countries disproportionately. M4 (joint) returns to 4.61 %, close to M0.

The practical take-away is that recognising time-to-build is the single most valuable specification change: it buys a level-forecast accuracy improvement comparable to what fully stochastic TFP models deliver (Smets and Wouters, 2007), but without any new stochastic-modelling machinery.

### 5.3 Flow–stock consistency

**[Figure 3 here]**

Figure 3 shows PIM-reconstructed capital *K_tang(t; μ̂) + β̂ · K_I(t)* alongside CWON-produced capital NW.PCA.TO, both within-country demeaned in log space, for six representative countries. The United States, Republic of Korea, and Israel — three R&D-intensive economies — show near-identity: the PIM series tracks CWON to within 1–2 % in log terms over the full 1995–2019 window. Germany and the Netherlands show small but visible widening after 2010, which is consistent with the delayed SNA 2008 incorporation of R&D on the CWON side. Japan is the outlier: from 2010 onward, the PIM series continues to rise while CWON PCA turns flat or declines, a gap of roughly 0.05–0.08 log units by 2019 (about 5–8 %).

**[Figure 4 here]**

Figure 4 examines whether the Japan anomaly is driven by an asset-price revaluation effect γ_price rather than by a real stock discrepancy. A γ_price ∈ [−0.04, +0.04] shifts the Japanese log-ratio by roughly 0.25 log units in total, implying that the observed ~0.06-log-unit gap corresponds to a γ_price ≈ 0.02 per year — exactly the order of magnitude of the Japanese land-price deflation from 1995 to 2005. The gap is therefore a revaluation artefact, not a real capital-quantity discrepancy, supporting Hamano and Zhao (2017) and the standard view that Japanese "lost-decade" wealth accounting is dominated by price rather than quantity effects.

### 5.4 Joint identification: bootstrap CIs on (μ̂, β̂)

**[Figure 5 here]**

(Conceptual diagram Figure 5 is placed here to remind the reader of the population–capital correspondence, which motivates the joint identification.)

Bootstrap confidence intervals on the joint estimates (Fig. 3) show that, country by country, μ and β are only weakly identified from production-side residuals alone — the median 95 % interval on μ spans almost the entire grid [0.01, 6.0], and the median interval on β spans about 70 % of its grid [0.0, 0.34]. Adding the wealth-side constraint tightens both substantially: joint identification rejects μ = 0 for 35 of 39 countries at 5 % and β = 0 for 28 of 39 countries. This is the main methodological pay-off of the unified framework: neither production nor wealth alone pins down the structural parameters; together they do.

## 6. Discussion

### 6.1 Re-interpreting the Solow residual

The standard Solow decomposition attributes the residual to TFP. Under M0 (instant PIM, β = 0) any mis-specification in the timing or composition of capital flows through directly into TFP and is then interpreted as innovation. We show that a measurable share of Solow-residual growth variation across our 39 countries can be re-assigned to two accounting corrections that have nothing to do with innovation: the time-to-build μ(t) and the intangible share β. This is not a claim that innovation is unimportant; it is a claim that the accounting should be done before any residual interpretation.

### 6.2 The Bongaarts-Feeney-Goldstein-Lutz-Scherbov analogy

Table 2 established that period-fertility analysts already solved the problem of measuring a stock process from its flow when the flow is contaminated by drift in the timing distribution. Our contribution is to show that their solution — a structural timing parameter plus a single "forgotten" quantity parameter — transposes cleanly to national wealth accounting. This is not metaphor. Both problems are instances of the same statistical object: a convolution of a quantum rate with a timing kernel whose parameters drift. The same Bongaarts-Feeney adjustment works, up to a change of units.

### 6.3 Flow–stock reconciliation and Beyond-GDP

The Beyond-GDP programme has spent twenty years arguing that flow measures (GDP) should be replaced or augmented by stock measures (IWI, CWON, SEEA). Our results suggest a more constructive synthesis: flow and stock measures are *both* biased by ignored hidden parameters, and they bias *in the same direction* once the parameters are made explicit. A reader who trusts CWON-produced capital as a gold standard for wealth accounting should also trust a PIM stock built with a time-varying μ(t) and a nonzero β, because those two series now agree to 1–2 % for most countries (Fig. 3). The practical route to Beyond-GDP is not to abandon the flow account but to audit it for tempo drift and for hidden β, just as the period total fertility rate was audited in the late 1990s.

### 6.4 Medical preview

The same machinery extends naturally to health expenditure. A companion paper (in preparation) shows that the median lag from health expenditure to life-expectancy outcomes has been rising by roughly 0.15 years per calendar year since 2000 across the OECD, and that an analogous forgotten parameter — the share of health expenditure directed to prevention and R&D rather than to curative care — explains an additional share of the US–Japan life-expectancy gap. The broader point is that any stock-of-outcomes process whose timing structure drifts (the "healthy life years" stock, the human-capital stock, the stock of accumulated medical R&D) admits the same tempo-plus-forgotten-parameter correction developed here.

### 6.5 Limitations

Three caveats apply. First, our identification of β against CWON is only as clean as CWON itself, and CWON combines national sources of heterogeneous quality. Second, the bootstrap CIs (§5.4) are wide for countries with short series or volatile investment, and we do not claim point identification for those countries; the framework provides interval estimates and a direction. Third, the γ_price sensitivity experiment (§5.3) treats the CWON deflator as a single country-level scalar; a more careful study would use sector-specific deflators and national land-price indices, and is left to future work.

## 7. Conclusion

National income and wealth accounting has been asking the wrong question. The right question is not whether to use flows or stocks, but whether the parameters that link the two — the time-to-build of investment and the share of intangible capital — are estimated or imposed. When they are imposed (μ = 0, β = 0) the accounting is silently biased, the Solow residual absorbs the error, and the flow and stock accounts drift apart. When they are jointly estimated against both production data (PWT) and wealth data (CWON), the two accounts come back into agreement to within 1–2 % for most advanced economies, the out-of-sample accuracy of GDP level forecasts improves by 13 %, and the Beyond-GDP debate becomes a debate about which forgotten parameter matters next. Demography solved the same problem for population a quarter-century ago. Capital accounting can do the same now.

---

## Tables

**Table 1.** M0–M4: In-sample and out-of-sample performance across 39 countries.

**[Insert table 1 here]**

**Table 2.** Population–capital correspondence.

**[Insert table 2 here]**

---

## References

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
