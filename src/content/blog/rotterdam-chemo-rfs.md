---
title: "Rotterdam乳がんデータ：交絡からOverlap weightingへ"
description: "最終発表に基づく生存時間解析の手順、再現結果、解釈上の限界。"
pubDate: "2026-09-05"
locale: "ja"
translationGroup: "rotterdam-chemo-rfs"
heroImage: "/biostatistics/rotterdam-chemo-rfs/presentation-plot-04.png"
badge: "Biostatistics"
tags: ["biostatistics", "survival-analysis", "causal-inference", "overlap-weighting", "r"]
---

[日本語](/ja/blog/rotterdam-chemo-rfs) · [中文](/zh/blog/rotterdam-chemo-rfs-zh) · [English](/blog/rotterdam-chemo-rfs-en)

**[GitHub · Code / コード / 代码](https://github.com/Fengmc2001/rotterdam-chemo-rfs)**

著者：Ziyin Wu（WU ZIYIN）。2026年8月18日の最終発表と付属のRコードに基づきます。本資料は学習を目的とした個人の解答であり、公式解答、査読済み研究、医療上の助言ではありません。公開用ドキュメントの構成整理と翻訳にはAIの支援を利用しました。発表用コードは別途保存しています。

**[原稿逐頁HTMLスライドを開く](https://fengmc2001.github.io/rotterdam-chemo-rfs/slides/)** — 原PDFの第1ページ全体を除外し、第2〜28ページ（27ページ）を順番・版式・内容を変えずに掲載。字形パスSVGと選択・検索用の原文HTMLを使用しています。スライドは原文の日本語、解説記事は三言語です。第2ページ以降の文献・所属表記は原稿どおり残っています。

[再現・公開記録](https://github.com/Fengmc2001/rotterdam-chemo-rfs/blob/main/REPRODUCIBILITY.md) · 検証：`python3 analysis/verify.py`

## 1. 問いと対象範囲

`survival::rotterdam`を用いて、化学療法を受けたと記録されている患者と、受けていないと記録されている患者の無再発生存（RFS）を比較し、観察データにおける比較がそのまま治療効果を意味するわけではない理由を説明します。このレジストリには原発性乳癌患者2,982例が含まれます。時間の起点は初回手術とし、最初に観察された再発または死亡をRFSのイベントとします。最終発表では、コホート全体の未調整比較に続いて、異なる標的集団を対象とする追加の調整解析を報告しています。

## 2. 再現方法

必要に応じて、リポジトリのルートディレクトリからRを起動し、必要なパッケージをインストールしてください。

```r
install.packages(c("survival", "ggplot2", "survminer", "WeightIt",
                  "cobalt", "adjustedCurves", "pammtools"))
```

```sh
Rscript analysis/run.R > results/run.log 2>&1
```

`analysis/survival.R`は最終発表で使用した元のスクリプトであり、それ以前の探索的な検証用コードではありません。`analysis/run.R`は統計モデルの数式を変更せず、グラフィックスデバイスとCSV・セッション情報の出力を追加します。上記の方法で実行した場合、書き込み先は`results/`配下のみです。ブートストラップでは乱数シード`20260717`、患者単位の再標本化500回、1コアを使用します。ソフトウェアのバージョンは[sessionInfo](https://github.com/Fengmc2001/rotterdam-chemo-rfs/blob/main/results/sessionInfo.txt)に記録されています。インストールされているパッケージのバージョンにより、数値結果が変わる場合があります。元の作図コードでは、macOSで利用可能な**Hiragino Sans**を指定しています。他のプラットフォームでは、図の日本語フォントを置き換える必要がある場合がありますが、統計モデルには影響しません。

データはRパッケージから読み込み、別のRotterdam/Stataデータセットからは転用していません。実行時に生成される患者単位のCSVは公開対象から除外しています。入学関連書類、第三者の論文PDF、講義スライド、バックアップファイルは含めていません。

## 3. 解析の流れ

1. **RFSを正しく定義する。** 再発が観察されていない場合は再発時点を無限大とし、死亡が観察されていない場合は死亡時点を無限大とします。両者の最小値が有限であれば、その時点をイベント時点とします。いずれも発生していない場合は、課題で提示された定義に従い、記録された2つの追跡期間の最大値を用います。365.25で除して日を年に換算します。2つの追跡期間の列について、条件を考慮せず単純に最小値を取ってはいけません。
2. **データを点検する。** 重複のない患者2,982例、欠測値なし、化学療法あり580例・なし2,402例、複合イベント1,713例、打ち切り1,269例であることを確認します。
3. **未調整比較を行う。** log–log変換に基づく信頼区間を伴うKaplan–Meier曲線を推定し、全追跡期間に対してログランク検定を行います。独立した2群のGreenwood標準誤差を用いた正規近似により、5年時点の生存率差を報告します。検定で有意差が認められないことは、同等性の証拠ではありません。
4. **交絡とオーバーラップを説明する。** 治療は無作為に割り付けられていません。患者背景は治療選択と予後の両方に関連しています。化学療法ありの580例は全員リンパ節転移陽性であり、リンパ節転移陰性の1,436例には比較対象となる化学療法ありの患者が存在しません。したがって、観測データ上の正値性（positivity）の問題により、この層ではデータに裏付けられた治療あり対なしの比較を行えません。
5. **標的集団の変更を明示する。** 追加解析をリンパ節転移陽性の1,546例（化学療法なし966例、あり580例）に限定し、元のコホート全体ではなく、この集団のオーバーラップ集団を標的とします。
6. **傾向スコアを推定する。** ロジスティック回帰に、年齢の自然スプライン（自由度4）、log(1 + リンパ節転移数)、log(1 + ER)、log(1 + PgR)の自然スプライン（各自由度3）、ならびに閉経状態、腫瘍径、組織学的グレードを用います。手術年とホルモン療法は、この最終モデルに含めていません。これらを含めていないことは、関連に交絡をもたらし得ないという証明ではありません。
7. **オーバーラップ重み付けを行う。** 傾向スコアをe(L)とすると、化学療法ありの患者には1 − e(L)、なしの患者にはe(L)の重みを与えます。`WeightIt::weightit(method="glm", estimand="ATO")`は、共変量の密度がe(L)[1 − e(L)]f(L)に比例する集団を標的とします。
8. **診断を行う。** 重み付け前後の標準化平均差（SMD）と有効サンプルサイズ（ESS）を確認します。再現されたESSは化学療法なし277.81、あり328.31です。報告された重み付け後のSMDの絶対値の最大値は約0.0126です。測定された共変量のバランスが良好であっても、未測定交絡が存在しないとはいえません。
9. **調整生存曲線とRMSTを推定する。** `adjustedCurves::adjustedsurv(method="iptw_km", estimand="ATO")`を使用します。メソッド名にかかわらず、ここで用いるのはオーバーラップ重みであり、ATEを標的とする逆確率重みではありません。各ブートストラップ標本内で傾向スコアと重みを再推定します。5年までの生存曲線を積分して制限平均生存時間（RMST）を求めます。コードは10年時点の要約も出力します。

## 4. 最終的な5年時点の結果

以下の差はすべて、**化学療法あり − 化学療法なし**です。RFSの差は相対的な変化率ではなく、パーセントポイント（pp）で示します。角括弧内は95%信頼区間です。

| 解析／指標 | 化学療法なし | 化学療法あり | 差 |
|---|---:|---:|---:|
| コホート全体の未調整RFS | 57.5% [55.5, 59.5] | 53.7% [49.5, 57.7] | −3.8 pp [−8.4, +0.7] |
| リンパ節転移陽性のオーバーラップ集団におけるRFS | 37.4% [32.4, 42.8] | 47.4% [42.4, 52.7] | +10.0 pp [+2.4, +17.7] |
| リンパ節転移陽性のオーバーラップ集団におけるRMST | 3.00年 [2.80, 3.20] | 3.53年 [3.36, 3.70] | +194日 [+98, +289] |

未調整の全追跡期間に対するログランク検定のp値は**0.4078**です（スライドでは0.408）。出力された正確な数値と実行ログは[results](https://github.com/Fengmc2001/rotterdam-chemo-rfs/blob/main/results/)にあります。元のスライドでは、RMSTの差を整数の日数に丸めています。

![未調整Kaplan–Meier曲線](/biostatistics/rotterdam-chemo-rfs/presentation-plot-02.png)

![重み付け前後の共変量バランス](/biostatistics/rotterdam-chemo-rfs/presentation-plot-03.png)

![オーバーラップ重み付けによる調整生存曲線](/biostatistics/rotterdam-chemo-rfs/presentation-plot-04.png)

## 5. 見かけ上の逆転をどう解釈するか

粗解析の結果は、化学療法が患者に害を及ぼすことを示すものでは**ありません**。また、調整後の結果も、化学療法が利益をもたらすという因果関係を証明するものでは**ありません**。治療群間ではベースラインの患者背景が大きく異なっていました。さらに、2つの解析の間では調整の有無だけでなく標的集団も変わっているため、差の符号の変化を交絡の除去だけに帰することはできません。

身近な例で考えると、暑い天候がアイスクリームの購入と熱中症の両方を増やすため、両者が同時に増えることがあります。同様に、患者の特性は治療選択と再発・死亡リスクの双方に影響し得ます。重み付けによって、*測定された*患者背景はより比較可能になりますが、未測定の変数を復元したり、ある層に存在しない治療群についての証拠を作り出したりすることはできません。

RMSTの+194日という差は、リンパ節転移陽性のオーバーラップ集団において、**最初の5年間に限って**累積した平均無再発生存時間の差を意味します。生涯全体の平均余命の延長を意味するものではなく、個々の患者が得られる利益を予測するものでもありません。

## 6. 限界と方法論上の検討経緯

- 過去の観察データを用いた解析です。未測定交絡、治療開始時期、治療内容の異質性、打ち切りに関する仮定が解釈を制限します。時間の起点は手術ですが、化学療法は記録された指標で表されており、本解析は時間の起点と治療割り付けの整合性を確立するものではなく、不死時間バイアスを除外するものでもありません。
- 因果的に解釈するには、妥当な一致性（consistency）、交換可能性／未測定交絡がないこと、標的集団における正値性、適切な打ち切りの仮定が必要です。一致性は仮定であり、常に自動的に成立するものではありません。
- 提示されたRFSの打ち切り規則を忠実に再現しています。その規則の適切性は、実際の追跡過程に依存します。
- 検証済みの環境では、ブートストラップ実行中に**傾向スコア推定における分離に関する警告が23件**出力されました。これらは黙って破棄せず、記録しています。出力された5年／10年時点の群別要約には500回分のブートストラップ結果が含まれていますが、それによって推論が不安定になり得るという問題が解消されるわけではありません。
- 発表の付録では、探索的なCox比例ハザード性の診断と極端なATE-IPTW重みについて論じています。これらの解析は**最終版の`survival.R`には実装されておらず**、本資料でも再現済みの結果とはしていません。これらは方法論上の探索過程を説明するものであり、第2の最終モデルではありません。
- 公開用の解説文では、パーセントポイントと因果推論の仮定を明確化しています。すべてのスライドを逐語的に再掲載したものではありません。HTMLプレイヤーは原PDFの第2〜28ページを字形パスSVGと抽出原文HTMLとして逐頁表示します。原PDF/PPTXファイルや非表示の発表者ノートは配布していません。講義由来の内容と文献・所属表記は原稿どおり残っています。

## 参考文献

- Rの`survival`パッケージ：[Rotterdamデータセットのドキュメント](https://stat.ethz.ch/R-manual/R-devel/library/survival/html/rotterdam.html)。
- Royston P, Altman DG. External validation of a Cox prognostic model: principles and methods. *BMC Med Res Methodol*. 2013;13:33. https://doi.org/10.1186/1471-2288-13-33
- Elkin EB et al. Adjuvant chemotherapy and survival in older women with hormone receptor-negative breast cancer. *J Clin Oncol*. 2006;24:2757–2764. https://doi.org/10.1200/JCO.2005.03.6053
- Du XL et al. Effectiveness of adjuvant chemotherapy for node-positive operable breast cancer in older women. *J Gerontol A*. 2005;60:1137–1144. https://doi.org/10.1093/gerona/60.9.1137
- Li F, Morgan KL, Zaslavsky AM. Balancing covariates via propensity score weighting. *JASA*. 2018;113:390–400. https://doi.org/10.1080/01621459.2016.1260466
- Li F, Thomas LE, Li F. Addressing extreme propensity scores via the overlap weights. *Am J Epidemiol*. 2019;188:250–257. https://doi.org/10.1093/aje/kwy201
- Denz R, Klaaßen-Mielke R, Timmesfeld N. A comparison of different methods to adjust survival curves for confounders. *Stat Med*. 2023;42:1461–1479. https://doi.org/10.1002/sim.9681
- Royston P, Parmar MKB. Restricted mean survival time: an alternative to the hazard ratio. *BMC Med Res Methodol*. 2013;13:152. https://doi.org/10.1186/1471-2288-13-152
- Hernán MA, Robins JM. [Causal Inference: What If](https://www.hsph.harvard.edu/miguel-hernan/causal-inference-book/).

学習上の参考と批判的検討のための資料であり、試験の提出答案にそのまま転用するためのものではありません。コードおよびドキュメントに関する権利は各著者に帰属します。第三者のデータセットや参考文献に対する包括的なライセンスを付与するものではありません。
