---
title: "統計的推測と単回帰分析"
description: "ピアソン相関係数の計算と、最小二乗法による単回帰分析の正規方程式の導出。"
pubDate: "2024-12-17"
heroImage: "/simple-linear-regression-analysis/zu1.jpg"
badge: "Academic"
tags: ["biostatistics", "linear-regression", "least-squares", "matrix-formulation"]
---

## 背景 (Background)

私たちの日常生活や社会活動において、「ある要素が変化したとき、別の要素がどのように変化するか」を予測することは非常に重要です。例えば、「気温が上がればアイスクリームの売上が伸びる」「都市の人口が増えれば、その都市を管理するための行政職員の数も増える」といった関係性が挙げられます。このような二つの変数間の関係性をデータから数理的に明らかにし、将来の予測や現状の分析に役立てる統計手法が「単回帰分析」です。本研究では、単回帰分析の基本的なメカニズムを深く理解するため、身近な実データ（人口と行政職員数）を用いて、数式レベルからのモデル構築と検証を行います。

## 概要

本研究では、単回帰分析の考え方と手順を実験を通じて学び、行列表現を用いた統計的推測の手法を理解することを目的とする。人口と行政職員数に関するデータに基づき、Pearsonの積率相関係数の計算、正規方程式の導出、最小二乗法によるパラメータ推定を行い、実データへの適用を通じて回帰モデルの有用性を検証した。

## 目的

1. 単回帰分析の考え方と手順
実験を通じて単回帰分析の目的、考え方、手順を理解する。
2. 単回帰分析における行列表現
実験を通じて単回帰分析における行列表現（線形回帰モデル、正規方程式、最小二乗推定量など）を実践して理解する。
3. 実際のデータ解析
実際のデータに回帰分析を適用することで、解析法を実践的に利用・応用できるようにする。

## 実験方法

解析ソフトにはExcelとRを使用する。各市町村の人口を $x_i$、職員数を $y_i$ $(i = 1, \ldots, n(=6))$ と表記する。

### 実験1：基礎的な単回帰モデルの構築

人口 $x$ を横軸、職員数 $y$ を縦軸とした散布図を作成し、両者の関係を調べる。単回帰モデルは以下のように表される。

$$
y_i = \beta_0 + \beta_1 x_i + \varepsilon_i \quad (i = 1, \ldots, n)
$$

残差平方和 $S_e$ を最小化するための正規方程式を導出し、$\beta_0$ と $\beta_1$ の最小二乗推定量を求める。

$$
S_e = \sum_{i=1}^n (y_i - \hat{y}_i)^2 = \sum_{i=1}^n (y_i - (\hat{\beta}_0 + \hat{\beta}_1 x_i))^2
$$

### 実験2：行列表現を用いた回帰分析

目的変数ベクトル $\mathbf{Y}$ と説明変数を含む定数行列 $\mathbf{X}$ を以下のように定義する。

$$
\mathbf{Y} = 
\begin{bmatrix}
y_1 \\
y_2 \\
\vdots \\
y_n
\end{bmatrix}, \quad
\mathbf{X} = 
\begin{bmatrix}
1 & x_1 \\
1 & x_2 \\
\vdots & \vdots \\
1 & x_n
\end{bmatrix}
$$

単回帰モデルの行列表現は次の通りである。

$$
\mathbf{y} = \mathbf{X} \boldsymbol{\beta} + \boldsymbol{\varepsilon}
$$

残差平方和を行列で表現し、$\boldsymbol{\beta}$ で微分して得られる正規方程式から最小二乗推定量 $\hat{\boldsymbol{\beta}} = (\mathbf{X}^T \mathbf{X})^{-1} \mathbf{X}^T \mathbf{y}$ を導出する。

## 理論と導出

### 偏差平方和と交差和

式変形により、以下の関係が成り立つ。

$$
\sum_{i=1}^n (x_i - \bar{x})^2 = \sum_{i=1}^n x_i^2 - n\bar{x}^2
$$

$$
\sum_{i=1}^n (y_i - \bar{y})^2 = \sum_{i=1}^n y_i^2 - n\bar{y}^2
$$

$$
\sum_{i=1}^n (x_i - \bar{x})(y_i - \bar{y}) = \sum_{i=1}^n x_i y_i - n\bar{x} \bar{y}
$$

### 正規方程式の導出

誤差平方和 $S_e$ を $\hat{\beta}_0$ および $\hat{\beta}_1$ で偏微分し、0と置くことで以下の推定量が得られる。

切片 $\hat{\beta}_0$ について：

$$
\frac{\partial S_e}{\partial \hat{\beta}_0} = -2 \sum_{i=1}^n ( y_i - \hat{\beta}_0 - \hat{\beta}_1 x_i ) = 0
$$
$$
\hat{\beta}_0 = \bar{y} - \hat{\beta}_1 \bar{x}
$$

傾き $\hat{\beta}_1$ について：

$$
\frac{\partial S_e}{\partial \hat{\beta}_1} = -2 \sum_{i=1}^n x_i ( y_i - \hat{\beta}_0 - \hat{\beta}_1 x_i ) = 0
$$
$$
\hat{\beta}_1 = \frac{\sum_{i=1}^n x_i y_i - n\bar{x}\bar{y}}{\sum_{i=1}^n x_i^2 - n\bar{x}^2}
$$

### 行列表現による正規方程式

残差平方和 $S_e = (\mathbf{Y} - \mathbf{X} \hat{\boldsymbol{\beta}})^T (\mathbf{Y} - \mathbf{X} \hat{\boldsymbol{\beta}})$ を $\boldsymbol{\beta}$ で微分すると次式が得られる。

$$
\frac{\partial S_e}{\partial \boldsymbol{\beta}} = -2 \mathbf{X}^T (\mathbf{Y} - \mathbf{X} \boldsymbol{\beta}) = 0
$$
$$
\mathbf{X}^T \mathbf{Y} = \mathbf{X}^T \mathbf{X} \hat{\boldsymbol{\beta}}
$$

これにより最小二乗推定量は以下のように求まる。

$$
\hat{\boldsymbol{\beta}} = (\mathbf{X}^T \mathbf{X})^{-1} \mathbf{X}^T \mathbf{Y}
$$

## 実装と結果

### 基本統計量の計算と回帰モデル

市町村の人口 $x$ と職員数 $y$ のデータを基に計算を行った。

人口の平均：3.17、分散：2.57
職員数の平均：29.17、分散：204.17

回帰係数の推定量は、傾き $\hat{\beta}_1 = 7.857143$、切片 $\hat{\beta}_0 = 4.285714$ であり、得られた回帰直線は以下の通りである。

$$
\hat{y} = 4.285714 + 7.857143x
$$

Pearsonの積率相関係数は $r = 0.881$ であり、人口と職員数には強い正の相関が確認された。

![Excelの散布図と回帰直線](/simple-linear-regression-analysis/zu1.jpg)
![Excelの回帰分析の結果](/simple-linear-regression-analysis/zu2.jpg)

### R言語による行列表現の実装

Rを用いて行列演算により回帰分析を実装し、Excelの計算結果と一致するかを確認した。

残差平方和 $RSS = 228.5714$
モデル平方和 $ESS = 792.2619$
総平方和 $TSS = 1020.8333$

$$
TSS = ESS + RSS
$$

決定係数 $R^2$ (寄与率) は次のように求められた。

$$
R^2 = \frac{ESS}{TSS} = 0.7761
$$

この結果から、本回帰モデルはデータの変動の約77.6%を説明可能である。

![R手順実行結果](/simple-linear-regression-analysis/4.jpg)
![R手順実行結果](/simple-linear-regression-analysis/6.jpg)
![R手順実行結果](/simple-linear-regression-analysis/8and9.jpg)

### 実データへの適用：食料消費支出の分析

総務省統計局の家計調査時系列データを用い、2020年1月から2024年10月までの食料の平均消費支出について回帰分析を行った。

![Pythonによる食料消費支出の回帰分析](/simple-linear-regression-analysis/zu3.jpg)

回帰方程式は以下のように求められた。

$$
\hat{Y} = 7.617 \times 10^4 + 230.15 X
$$

時間経過とともに食料消費支出が緩やかに増加している傾向が観察され、実データの可視化と予測における回帰分析の有効性が示された。

## 考察

行列を用いた統計演算には、Excelや手計算と比較して、計算効率、理論の明確化、再利用性に大きな利点がある。プログラムとして実装することで、変数の多い大規模なデータに対しても統一的な処理が可能となる。特に、射影行列や残差平方和を行列として扱うことで、数学的構造がより明確になり、多変量解析への拡張も容易となる。

## まとめ

本実験では、単回帰分析をテーマとしてデータの回帰係数推定法を学び、実践した。手計算と行列演算（R言語）の双方から正規方程式を解き、同様の結果が得られることを確認した。公表データを用いた分析からも、統計的推測の手法が実社会のデータ分析において強力なアプローチとなることが確認できた。