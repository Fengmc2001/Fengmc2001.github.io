# Biostatistics Portfolio / 生物統計ポートフォリオ

This small portfolio summarizes several simulation-based examples that were created to study core ideas in biostatistics, survival analysis, and causal inference using real-world-data-like settings.

この小さなポートフォリオは、生物統計学・生存時間解析・因果推論における重要な考え方を、RWD（Real-World Data）を意識したシミュレーションを通じて整理したものである。

The main purpose is not to present a finished research product, but to demonstrate methodological understanding: how bias arises, why estimands change depending on design choices, and how temporal structure must be handled carefully in survival analysis.

本資料の目的は、完成済みの研究成果を示すことではなく、方法論的理解を示すことにある。すなわち、どのようにバイアスが生じるのか、解析設計によって estimand がどのように変化するのか、また生存時間解析では時間順序をどのように厳密に扱うべきかを示すことである。

## Topics

### 1. Propensity score model misspecification
- Simulates high-dimensional covariates.
- Generates treatment assignment using nonlinear confounding.
- Estimates propensity scores with a misspecified linear logistic model.
- Applies inverse probability weighting and a weighted Cox model.
- Demonstrates that IPW is sensitive to model misspecification.

### 2. Naive analysis vs landmark analysis
- Simulates a treatment with severe early toxicity and a favorable late-phase pattern among survivors.
- Compares a full-period Cox analysis with a landmark analysis at day 30.
- Shows that landmark analysis may remove early harm and change the target population.
- Highlights survivor selection and the distinction between overall effect and post-landmark effect.

### 3. Time-dependent treatment coding
- Provides a minimal time-varying Cox example.
- Illustrates why delayed treatment initiation should not be coded as a baseline-fixed exposure.
- Emphasizes the importance of respecting temporal ordering in survival analysis.

## Why this matters for biostatistics

In biostatistics, a method is not only a computational tool. The validity of an analysis depends on the target estimand, the timing of treatment assignment, the structure of confounding, and the possibility of selection bias. Even simple simulation studies can clarify these issues and help connect statistical models to substantive clinical questions.

生物統計学において、手法は単なる計算手段ではない。解析の妥当性は、target estimand、治療割付のタイミング、交絡構造、そして選択バイアスの有無に強く依存する。シンプルなシミュレーションであっても、こうした問題を明示化し、統計モデルと臨床的問いを結びつける訓練になる。

## Files

- `scripts/01_ps_model_misspecification.py`  
  非線形交絡の下で、誤って線形に指定された propensity score model が IPW 推定に与える影響を確認する。

- `scripts/02_landmark_analysis_demo.py`  
  早期毒性をもつ治療を想定し、全期間解析と landmark analysis の結論がどのように変わり得るかを示す。

- `scripts/03_time_dependent_cox_demo.py`  
  治療開始時点が後ろにずれる場合、time-dependent Cox model によって時間順序を適切に扱う最小例を示す。

- `requirements.txt`  
  実行に必要な Python パッケージ一覧。

## Future directions

Potential next steps include marginal structural models for time-varying confounding, doubly robust estimation, overlap weighting, and sensitivity analyses for unmeasured confounding.

今後は、time-varying confounding に対する marginal structural model、doubly robust estimation、overlap weighting、さらに unmeasured confounding に対する感度分析へと拡張したい。

## Note

These examples are intentionally simple and educational. They are not intended to replace formal applied analyses with real clinical data, but they reflect an effort to understand the statistical logic required for rigorous work in biostatistics.

これらの例は教育目的の簡略化されたシミュレーションであり、実データを用いた正式な応用解析を置き換えるものではない。ただし、生物統計学において厳密な解析を行うために必要な統計的思考を、自分なりに整理し理解しようとした過程を示している。