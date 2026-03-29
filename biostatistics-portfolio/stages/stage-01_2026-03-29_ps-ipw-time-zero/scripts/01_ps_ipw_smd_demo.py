import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression


np.random.seed(42)
n = 1000

age = np.random.normal(65, 10, size=n)
severity = np.random.normal(0, 1, size=n)
income = np.random.normal(500, 120, size=n)

# 真の治療割付メカニズム
logit_ps = -1.5 + 0.03 * age + 1.0 * severity - 0.002 * income
true_ps = 1 / (1 + np.exp(-logit_ps))
treatment = np.random.binomial(1, true_ps)

df = pd.DataFrame({
    "age": age,
    "severity": severity,
    "income": income,
    "treatment": treatment,
})

X = df[["age", "severity", "income"]]
A = df["treatment"]

# Logistic regression による propensity score 推定
ps_model = LogisticRegression(penalty=None, solver="lbfgs", max_iter=1000)
ps_model.fit(X, A)
df["propensity_score"] = ps_model.predict_proba(X)[:, 1]

# 極端な値を少し防ぐため clip
df["propensity_score"] = df["propensity_score"].clip(0.01, 0.99)

# IPW
df["ipw_weight"] = np.where(
    df["treatment"] == 1,
    1 / df["propensity_score"],
    1 / (1 - df["propensity_score"]),
)


def weighted_mean(x, w):
    return np.sum(w * x) / np.sum(w)


def weighted_var(x, w):
    mu = weighted_mean(x, w)
    return np.sum(w * (x - mu) ** 2) / np.sum(w)


def smd_unweighted(df, var):
    x1 = df.loc[df["treatment"] == 1, var]
    x0 = df.loc[df["treatment"] == 0, var]
    m1 = x1.mean()
    m0 = x0.mean()
    v1 = x1.var(ddof=0)
    v0 = x0.var(ddof=0)
    return (m1 - m0) / np.sqrt((v1 + v0) / 2)


def smd_weighted(df, var):
    x1 = df.loc[df["treatment"] == 1, var].to_numpy()
    w1 = df.loc[df["treatment"] == 1, "ipw_weight"].to_numpy()
    x0 = df.loc[df["treatment"] == 0, var].to_numpy()
    w0 = df.loc[df["treatment"] == 0, "ipw_weight"].to_numpy()
    m1 = weighted_mean(x1, w1)
    m0 = weighted_mean(x0, w0)
    v1 = weighted_var(x1, w1)
    v0 = weighted_var(x0, w0)
    return (m1 - m0) / np.sqrt((v1 + v0) / 2)


variables = ["age", "severity", "income"]
rows = []
for var in variables:
    rows.append({
        "variable": var,
        "SMD_before_IPW": smd_unweighted(df, var),
        "SMD_after_IPW": smd_weighted(df, var),
    })

result = pd.DataFrame(rows)
result["|SMD_before_IPW|"] = result["SMD_before_IPW"].abs()
result["|SMD_after_IPW|"] = result["SMD_after_IPW"].abs()

print("=== Propensity score summary ===")
print(df["propensity_score"].describe())
print()
print("=== SMD before and after IPW ===")
print(result.round(4))
print()
print("Interpretation:")
print("- IPW の目的は、weighting 後に treatment/control の baseline covariates をよりバランスさせることである。")
print("- 実務では、|SMD| が 0 に近づいているかを確認する。")
print("- しばしば |SMD| < 0.1 が 1 つの目安として用いられる。")
