import pandas as pd
import numpy as np
from lifelines import CoxPHFitter


np.random.seed(42)
n_samples = 2000

# 0 = control, 1 = treatment
groups = np.array([0] * (n_samples // 2) + [1] * (n_samples // 2))
durations = []

for g in groups:
    if g == 0:
        durations.append(np.random.exponential(100))
    else:
        if np.random.rand() < 0.5:
            durations.append(np.random.uniform(1, 30))
        else:
            durations.append(np.random.exponential(150) + 30)

df = pd.DataFrame({
    "group": groups,
    "duration": durations,
    "event": 1,
})

# 全期間の Cox 解析
cph_naive = CoxPHFitter().fit(df, duration_col="duration", event_col="event")
hr_naive = cph_naive.hazard_ratios_["group"]

# 30 日 landmark 解析
df_landmark = df[df["duration"] >= 30].copy()
df_landmark["duration"] = df_landmark["duration"] - 30
cph_landmark = CoxPHFitter().fit(df_landmark, duration_col="duration", event_col="event")
hr_landmark = cph_landmark.hazard_ratios_["group"]

treated_30d_mortality = len(df[(df.group == 1) & (df.duration < 30)]) / (n_samples / 2)
control_30d_mortality = len(df[(df.group == 0) & (df.duration < 30)]) / (n_samples / 2)

print(f"30-day mortality in treatment group: {treated_30d_mortality:.1%}")
print(f"30-day mortality in control group:   {control_30d_mortality:.1%}")
print("-" * 40)
print(f"Naive Cox analysis over the full follow-up: HR = {hr_naive:.4f}")
print("Interpretation: the treatment appears harmful when the full period is analyzed.")
print("-" * 40)
print(f"Landmark analysis after day 30: HR = {hr_landmark:.4f}")
print("Interpretation: once early deaths are removed, the remaining survivors may make the treatment look favorable.")
print("This illustrates how landmark analysis changes the target population and may introduce survivor selection.")
