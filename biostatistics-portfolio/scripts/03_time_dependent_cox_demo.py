import pandas as pd
from lifelines import CoxTimeVaryingFitter


# 1 人の患者が途中で治療を開始する状況を counting-process 形式で表現
# id=1 は day 40 で治療開始, day 90 でイベント発生
# id=2 は終始未治療, day 70 でイベント発生
# id=3 は day 20 で治療開始, day 120 で打ち切り

df_tv = pd.DataFrame([
    {"id": 1, "start": 0,  "stop": 40,  "treated": 0, "event": 0},
    {"id": 1, "start": 40, "stop": 90,  "treated": 1, "event": 1},
    {"id": 2, "start": 0,  "stop": 70,  "treated": 0, "event": 1},
    {"id": 3, "start": 0,  "stop": 20,  "treated": 0, "event": 0},
    {"id": 3, "start": 20, "stop": 120, "treated": 1, "event": 0},
])

ctv = CoxTimeVaryingFitter()
ctv.fit(df_tv, id_col="id", start_col="start", stop_col="stop", event_col="event")

print(df_tv)
print("-" * 40)
print(ctv.summary[["coef", "exp(coef)"]])
print("This minimal example illustrates how treatment status can be updated over time instead of being incorrectly fixed at baseline.")
