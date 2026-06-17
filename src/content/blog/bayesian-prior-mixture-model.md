---
title: "ベイズ混合事前分布を用いた事後分布の推論とシミュレーション"
description: "ベータ分布の混合事前分布を用いたベイズ推論と分析"
pubDate: "2025-10-01"
heroImage: "/bayesian-prior-mixture-model/34.png"
badge: "Academic"
tags: ["biostatistics", "bayesian-inference", "beta-distribution", "mixture-model"]
---

## 背景 (Background)

ベイズ統計学において、未知のパラメータの確率分布（事後分布）を推定することは、不確実性を含むデータ解析の核心的な課題です。ベイズ推論では、観測データから得られる「尤度」と、データ観測前に持っていた信念である「事前分布」を掛け合わせることで、予測を事後分布としてアップデートします。通常の分析では単一の確率分布を事前分布として仮定することが多いですが、現実の複雑な問題においては、相反する複数の事前情報や異なる専門家の意見を統合する必要が生じることがあります。

本研究では、単一の事前分布に縛られず、異なる複数の信念を混ぜ合わせた「混合事前分布（Mixture of Priors）」という高度な統計的枠組みを導入します。二項分布のデータ生成プロセスに対し、共役事前分布であるベータ分布を複数組み合わせることで、事後分布がどのように変化するかを数理的に分析・シミュレーションし、柔軟なベイズ推論のメカニズムを探求します。

## 課題の設定

ある事象について、$n = 43$ 回の試行のうち $y = 15$ 回の成功（イベント発生）が観測されたという二項データに基づき、未知の確率パラメータ $\theta$ を推定することを目的としています。この際、事前情報として以下の3つのシナリオを検証します。

1. $\theta$ に対して、$\mathrm{Beta}(2,8)$ の事前分布を仮定するシナリオ。
2. $\theta$ に対して、$\mathrm{Beta}(8,2)$ の事前分布を仮定するシナリオ。
3. $\theta$ に対して、前述の2つの分布をそれぞれ 75%、25% の割合で混合した以下の事前分布を仮定するシナリオ。

$$
  p(\theta) = \frac{1}{4} \frac{\Gamma(10)}{\Gamma(2)\Gamma(8)}
    \Bigl[ 3\theta (1-\theta)^7 + \theta^7 (1-\theta) \Bigr]
$$

## Beta(2,8)事前分布に基づく推定結果と考察

まず、事前分布として $\mathrm{Beta}(2,8)$ を用いた場合の結果を示します。

![事前分布 P(θ)](/bayesian-prior-mixture-model/3-1.png)

![尤度関数 P(y|θ)](/bayesian-prior-mixture-model/3-2.png)

![事後分布](/bayesian-prior-mixture-model/3-3.png)

上図(a)の事前分布 $P(\theta)$ は $\mathrm{Beta}(2,8)$ に従い、成功確率 $\theta$ が小さい値、すなわち再犯確率が低いという事前信念を表しています。
図(b)の尤度関数 $P(y \mid \theta)$ は、観測データ $y=15, n=43$ に基づく二項分布であり、再犯率が $\theta \approx 0.35$ 付近で最も高い尤度を持つことを示しています。
図(c)の事後分布 $P(\theta \mid y)$ の青線は、事前分布と尤度の積 $P(\theta)P(y \mid \theta)$ を正規化（積分面積＝1）して求めたものです。ここで青線（$P(\theta \mid y)$）と理論的なベータ二項モデルの $\mathrm{Beta}(17,36)$ 分布（赤の点線）は完全に一致しました。
このことから、以下の関係式が数値的にも確認できました。

$$
P(\theta \mid y) \propto P(y \mid \theta)P(\theta)
$$

$$
p(\theta \mid y) = \mathrm{Beta}(a + y, b + n - y)
$$

## Beta(8,2)事前分布に基づく推定結果と考察

次に、同じ観測データ $n=43, y=15$ を用い、事前分布を $\mathrm{Beta}(8,2)$ に変更して推定を行いました。

![事前分布 P(θ)](/bayesian-prior-mixture-model/32_1.png)

![事後分布](/bayesian-prior-mixture-model/32-3.png)

![事後分布の比較](/bayesian-prior-mixture-model/32_4.png)

事前分布 $P(\theta)$ は、$\mathrm{Beta}(8,2)$ に従うため、$\theta$（再犯確率）が高いという事前信念を表しています。
事後分布 $P(\theta \mid y)$ は、事前分布と尤度の積 $P(\theta)P(y \mid \theta)$ を正規化することで求められ、その結果、$\mathrm{Beta}(23,30)$ の分布として数値的に確かめられました。計算により求めた事後分布と理論分布はほぼ完全に一致しています。

$\mathrm{Beta}(2,8)$ の場合と比較すると、事前分布が大きい $\theta$ に偏っているため、事後分布も全体として $\theta$ が大きい側にシフトしたことがわかります。これにより、観測データが同一であっても、事前信念の違いによって事後推定結果が大きく異なることが実証されました。

## 混合事前分布の導入と考察

最後に、事前分布として $\mathrm{Beta}(2,8)$ と $\mathrm{Beta}(8,2)$ の二つをそれぞれ 75%、25% の比率で混合した事前分布を考えます。

$$
p(\theta) = 0.75 \cdot \mathrm{Beta}(2,8) + 0.25 \cdot \mathrm{Beta}(8,2)
$$

![混合事前分布](/bayesian-prior-mixture-model/34.png)

この混合分布は、二つの対立する事前信念が統合された形となっています。具体的には、「確率 $\theta$ は低い（$\mathrm{Beta}(2,8)$）と推定する情報源と、比較的高い（$\mathrm{Beta}(8,2)$）と推定する情報源が混在している」という事前情報が設定されています。

図の通り、黒線は混合事前分布、灰色の点線はそれぞれ $\mathrm{Beta}(2,8)$ および $\mathrm{Beta}(8,2)$ の単独分布を示しています。低い $\theta$ を予想する信念と高い $\theta$ に偏る信念に対し、両者の特徴を併せ持つ二峰性を示す混合分布となっています。

このように、混合事前分布を用いることで、異なる事前予想を同時にモデル内に表現することができ、単一のベータ分布を用いるよりも柔軟に不確実さを扱えることが示されました。

## 実装（Rコード）

本分析で使用したRコードは以下の通りです。

```r
# サンプル数
n <- 43
# 成功回数（イベント発生数）
y <- 15

# 0〜1 の範囲を等間隔に500個分割した数値のベクトル
theta <- seq(0, 1, length.out = 500)

# 3-1: Beta(2,8)
prior <- dbeta(theta, shape1 = 2, shape2 = 8)
likelihood <- dbinom(y, size = n, prob = theta)

py_func <- function(theta) {
  dbinom(y, size = n, prob = theta) * dbeta(theta, 2, 8)
}
py <- integrate(py_func, lower = 0, upper = 1)$value
posterior <- prior * likelihood / py

# 3-2: Beta(8,2)
prior2 <- dbeta(theta, shape1 = 8, shape2 = 2)

py_func_2 <- function(theta) {
  dbinom(y, size = n, prob = theta) * dbeta(theta, 8, 2)
}
py2 <- integrate(py_func_2, lower = 0, upper = 1)$value
posterior2_calc <- prior2 * likelihood / py2

# 3-3: 混合事前分布
prior_mix <- 0.75 * prior + 0.25 * prior2

py_func_mix <- function(theta) {
  0.75 * dbeta(theta, 2, 8) + 0.25 * dbeta(theta, 8, 2)
}
area <- integrate(py_func_mix, lower = 0, upper = 1)$value
print(paste0("混合分布 areaの面積 = ", area))
```