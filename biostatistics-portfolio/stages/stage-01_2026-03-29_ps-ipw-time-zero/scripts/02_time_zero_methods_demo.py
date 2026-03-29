import numpy as np
import pandas as pd
from lifelines import CoxPHFitter, CoxTimeVaryingFitter


# --------------------------------------------------
# Part 1: 「致命的な毒薬」シミュレーション
# naive と landmark の違いを確認する
# --------------------------------------------------
np.random.seed(42)
n_samples = 2000

groups = np.array([0] * (n_samples // 2) + [1] * (n_samples // 2))
durations = []

for g in groups:
    if g == 0:
        # 対照群：平均寿命 100 日
        durations.append(np.random.exponential(100))
    else:
        # 治療群：最初の 30 日に非常に強い毒性がある設定
        if np.random.rand() < 0.5:
            durations.append(np.random.uniform(1, 30))
        else:
            durations.append(np.random.exponential(150) + 30)

df = pd.DataFrame({
    "group": groups,
    "duration": durations,
    "event": 1,
})

# Naive analysis: 全期間をそのまま比較
cph_naive = CoxPHFitter().fit(df, duration_col="duration", event_col="event")
hr_naive = cph_naive.hazard_ratios_["group"]

# Landmark analysis: day 30 まで生存した人だけを比較
df_landmark = df[df["duration"] >= 30].copy()
df_landmark["duration"] = df_landmark["duration"] - 30
cph_landmark = CoxPHFitter().fit(df_landmark, duration_col="duration", event_col="event")
hr_landmark = cph_landmark.hazard_ratios_["group"]

print("=== Part 1: naive vs landmark ===")
print(f"治療群の 30 日以内死亡率: {len(df[(df.group == 1) & (df.duration < 30)]) / (n_samples / 2):.1%}")
print(f"対照群の 30 日以内死亡率: {len(df[(df.group == 0) & (df.duration < 30)]) / (n_samples / 2):.1%}")
print(f"Naive analysis (全期間): HR = {hr_naive:.4f}")
print(f"Landmark analysis (30 日以降): HR = {hr_landmark:.4f}")
print("解釈:")
print("- Naive は全期間の有害性をそのまま反映する。")
print("- Landmark は 30 日までに死亡した人を除外するため、survivor selection が入り得る。")
print()

# --------------------------------------------------
# Part 2: time-dependent treatment coding の最小例
# 治療開始時点を A(t) として扱う
# --------------------------------------------------
df_tv = pd.DataFrame([
    {"id": 1, "start": 0,  "stop": 40,  "treated": 0, "event": 0},
    {"id": 1, "start": 40, "stop": 90,  "treated": 1, "event": 1},
    {"id": 2, "start": 0,  "stop": 70,  "treated": 0, "event": 1},
    {"id": 3, "start": 0,  "stop": 20,  "treated": 0, "event": 0},
    {"id": 3, "start": 20, "stop": 120, "treated": 1, "event": 0},
])

ctv = CoxTimeVaryingFitter()
ctv.fit(df_tv, id_col="id", start_col="start", stop_col="stop", event_col="event")

print("=== Part 2: time-dependent treatment coding ===")
print(df_tv)
print(ctv.summary[["coef", "exp(coef)"]])
print("解釈:")
print("- time-dependent treatment coding では、治療開始前の時間を untreated として扱える。")
print("- そのため、治療開始時点の遅れを baseline 固定変数として誤って扱うより自然である。")
print("- ただし、time-varying confounding がある場合にはこれだけでは不十分で、MSM などが必要になり得る。")
