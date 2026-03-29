# 学習段階一覧

このディレクトリでは、生物統計学・因果推論・生存時間解析の学習内容を、**段階ごと**に保存する。

## 一覧

### Stage 01 — 2026-03-29
主題：Propensity score, IPW, SMD, time-zero 問題

学んだ内容の概要：
- Logistic regression を用いて propensity score を推定する基本形
- inverse probability weighting (IPW) の計算方法
- weighting 後に SMD を確認して balance を診断する必要性
- time-zero 問題に対する naive, landmark, time-dependent treatment coding の違い
- time-dependent Cox model の利点と限界（time-varying confounding の問題）

対応ディレクトリ：
- `stage-01_2026-03-29_ps-ipw-time-zero/`

## 今後の予定

次の段階では、以下を優先して整理したい。

- stabilized weight の導入
- overlap / positivity の確認
- doubly robust estimation の最小例
- marginal structural model の導入準備
