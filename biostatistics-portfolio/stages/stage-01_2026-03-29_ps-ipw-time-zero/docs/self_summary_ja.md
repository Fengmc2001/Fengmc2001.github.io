# 今日の学習内容の要約

今日は主に、**propensity score と IPW の基礎**、および **time-zero 問題に対する複数の考え方**を整理した。

まず、baseline covariates から treatment assignment の確率を推定するために、logistic regression を用いて propensity score を計算する流れを確認した。その上で、treatment group には `1 / PS`、control group には `1 / (1 - PS)` を割り当てることで、観測データから pseudo-population を作るという IPW の考え方を理解した。さらに重要なのは、IPW を計算しただけで満足するのではなく、**weighting 後に covariate balance が本当に改善したかを SMD で確認する必要がある**という点である。ここでは、IPW 後の SMD は厳密に 0 でなければならないと考えるのではなく、**0 に近づいているか**、そして実務上は `|SMD| < 0.1` のような基準を参考にすることが大切だと理解した。

次に、time-zero 問題に関して、naive、landmark、time-dependent treatment coding の 3 つを比較した。naive な扱いでは、治療開始時点の情報を適切に処理しないと、状況によっては immortal time bias が生じ得る。一方で、landmark analysis はある時点まで生存した人に限定することで時間順序を整理しやすくするが、その代わりに survivor selection を導入し、target population を変えてしまう。これに対して、time-dependent treatment coding は treatment status を時間とともに更新することで、time order をより自然に扱える点が強みである。ただし、**time-dependent Cox model を使えば全て解決するわけではなく、time-varying confounding が残る場合には MSM など追加の方法が必要になる**ことも理解した。

全体として、今日の学習を通じて、因果推論や生存時間解析では、単にモデルを当てはめるだけでは不十分であり、**何を推定したいのか（estimand）、どの時点を起点とするのか（time-zero）、そして weighting 後に本当に balance が達成されたのか**まで含めて考える必要があることを確認できた。

## 次に学ぶ内容と目標

- stabilized weight の考え方を理解する。  
- positivity / overlap violation があるときの問題を整理する。  
- doubly robust estimation の最小例を実装する。  
- time-varying confounding と MSM の関係を、図とコードで説明できるようにする。
