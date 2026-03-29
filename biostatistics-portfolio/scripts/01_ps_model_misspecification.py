import numpy as np
import pandas as pd
from lifelines import CoxPHFitter
from sklearn.linear_model import LogisticRegression


np.random.seed(42)
n_samples = 1000
n_features = 50

X = np.random.normal(0, 1, size=(n_samples, n_features))

# 真の治療割付は非線形交絡を含む
confounder_effect = (
    0.5 * X[:, 0]
    - 0.5 * X[:, 1]
    + 0.8 * (X[:, 0] ** 2)
    - 0.5 * (X[:, 0] * X[:, 1])
)

true_ps = 1 / (1 + np.exp(-confounder_effect))
A = np.random.binomial(1, true_ps)

# 真の治療効果: log(HR) = -0.693
true_log_hr = -0.693
log_hazard = true_log_hr * A + 0.3 * X[:, 0] - 0.3 * X[:, 1]

T = np.random.exponential(scale=np.exp(-log_hazard))
C = np.random.uniform(0, 10, size=n_samples)
time = np.minimum(T, C)
event = (T <= C).astype(int)

df = pd.DataFrame(X, columns=[f"X{i}" for i in range(n_features)])
df["A"] = A
df["time"] = time
df["event"] = event

# 誤指定: 線形 logistic model だけで PS を推定
features = [f"X{i}" for i in range(n_features)]
ps_model = LogisticRegression(penalty=None, solver="lbfgs", max_iter=1000)
ps_model.fit(df[features], df["A"])
estimated_ps = ps_model.predict_proba(df[features])[:, 1]

estimated_ps = np.clip(estimated_ps, 0.01, 0.99)
weights = np.where(df["A"] == 1, 1 / estimated_ps, 1 / (1 - estimated_ps))
df["weight"] = weights

cph_ipw = CoxPHFitter()
cph_ipw.fit(
    df[["A", "time", "event", "weight"]],
    duration_col="time",
    event_col="event",
    weights_col="weight",
    robust=True,
)

print(f"True log(HR): {true_log_hr:.3f}")
print(f"Estimated log(HR) under misspecified PS model: {cph_ipw.params_['A']:.3f}")
print("This example shows that IPW may remain biased if the propensity score model is misspecified.")
