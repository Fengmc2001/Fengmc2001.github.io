# Sample Outputs

This file stores example outputs obtained by running the scripts locally with the current code and fixed random seeds.
以下は、現在のコードを固定シードでローカル実行した際のサンプル出力である。

## 1. Propensity score misspecification

- True log(HR): -0.693
- Estimated log(HR) under misspecified PS model: -0.696

Interpretation:
A misspecified linear propensity score model does not fully remove confounding, so the IPW estimate may deviate from the true treatment effect.

## 2. Landmark analysis demonstration

- 30-day mortality in treatment group: 48.5%
- 30-day mortality in control group: 27.9%
- Naive Cox analysis over the full follow-up: HR = 1.0050
- Landmark analysis after day 30: HR = 0.6587

Interpretation:
The full-period analysis captures early toxicity, whereas the landmark analysis excludes early deaths and may make the treatment appear more favorable among survivors.

## 3. Time-dependent Cox model

```text
                coef     exp(coef)
covariate                         
treated   -19.623363  3.003873e-09
```

Interpretation:
This toy example is intentionally small. The point is not stable estimation, but correct coding of treatment status over time.
