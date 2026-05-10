---
title: "ベイズ事前分布の混合モデルを用いた再犯率の推定"
description: "ベータ分布の混合事前分布を用いたベイズ推論と分析"
pubDate: "2025-10-01"
heroImage: "/bayesian-prior-mixture-model/34.png"
badge: "Academic"
tags: ["biostatistics", "bayesian-inference"]
---

## 背景 (Background)

私たちの社会において、一度罪を犯した人が再び犯罪に手を染めてしまう「再犯率」を正確に予測・推定することは、効果的な更生プログラムの策定や司法政策の最適化において極めて重要です。しかし、実際のデータは常に不完全であり、個人の背景や社会環境といった不確実な要因が多く絡み合っています。ここで威力を発揮するのが、過去のデータ（事前情報）と新たに得られたデータ（尤度）を掛け合わせて予測をアップデートしていく「ベイズ推論」です。本研究では、単一の予測モデルに縛られるのではなく、異なる複数の信念を混ぜ合わせた「混合事前分布」という高度な統計アプローチを用いて、この複雑な社会課題に対するより柔軟で精度の高い数理的なアプローチを探求します。

本プロジェクトでは、服刑釈放者の再犯率データを基に、異なるベータ分布を事前分布として用いたベイズ推論を行いました。また、二つの分布を組み合わせた混合事前分布（Mixture of Priors）を導入し、異なる事前信念の統合による推論結果の違いを数学的に分析しました。

## 課題の背景と設定

36ヶ月以内に $n = 43$ 人が投獄から解放され、$y = 15$ 人の再犯者がいたという研究に基づき、10代の再犯確率 $\theta$ を推定することを目的としています。この際、事前情報として以下の3つのシナリオを検証します。

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
図(b)の尤度関数 $P(y|\theta)$ は、観測データ $y=15, n=43$ に基づく二項分布であり、再犯率が $\theta \approx 0.35$ 付近で最も高い尤度を持つことを示しています。
図(c)の事後分布 $P(\theta|y)$ の青線は、事前分布と尤度の積 $P(\theta)P(y|\theta)$ を正規化（積分面積＝1）して求めたものです。ここで青線（$P(\theta|y)$）と理論的なベータ二項モデルの $\mathrm{Beta}(17,36)$ 分布（赤の点線）は完全に一致しました。
このことから、以下の関係式が数値的にも確認できました。

$$
P(\theta|y) \propto P(y|\theta)P(\theta)
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
事後分布 $P(\theta|y)$ は、事前分布と尤度の積 $P(\theta)P(y|\theta)$ を正規化することで求められ、その結果、$\mathrm{Beta}(23,30)$ の分布として数値的に確かめられました。計算により求めた事後分布と理論分布はほぼ完全に一致しています。

$\mathrm{Beta}(2,8)$ の場合と比較すると、事前分布が大きい $\theta$ に偏っているため、事後分布も全体として $\theta$ が大きい側にシフトしたことがわかります。これにより、観測データが同一であっても、事前信念の違いによって事後推定結果が大きく異なることが実証されました。

## 混合事前分布の導入と考察

最後に、事前分布として $\mathrm{Beta}(2,8)$ と $\mathrm{Beta}(8,2)$ の二つをそれぞれ 75%、25% の比率で混合した事前分布を考えます。

$$
p(\theta) = 0.75 \cdot \mathrm{Beta}(2,8) + 0.25 \cdot \mathrm{Beta}(8,2)
$$

![混合事前分布](/bayesian-prior-mixture-model/34.png)

この混合分布は、二つの対立する事前信念が統合された形となっています。具体的には、「多くの人は再犯確率が低い（$\mathrm{Beta}(2,8)$）と考えるが、一部の人は比較的高い（$\mathrm{Beta}(8,2)$）と考える」という事前情報が設定されています。

図の通り、黒線は混合事前分布、灰色の点線はそれぞれ $\mathrm{Beta}(2,8)$ および $\mathrm{Beta}(8,2)$ の単独分布を示しています。低い $\theta$ を予想する信念と高い $\theta$ に偏る信念に対し、両者の特徴を併せ持つ二峰性を示す混合分布となっています。

このように、混合事前分布を用いることで、異なる事前予想を同時にモデル内に表現することができ、単一のベータ分布を用いるよりも柔軟に不確実さを扱えることが示されました。

## 実装（Rコード）

本分析で使用したRコードは以下の通りです。

```r
# サンプル数
n <- 43
# 事情あり
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