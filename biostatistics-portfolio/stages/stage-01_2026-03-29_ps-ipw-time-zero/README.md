# Stage 01 — Propensity score, IPW, SMD, time-zero 問題

## この段階で学んだこと

この段階では、主に次の 2 つのテーマを整理した。

1. **Logistic regression を用いた propensity score 推定と inverse probability weighting (IPW)**  
2. **time-zero 問題に対する 3 つの考え方：naive, landmark, time-dependent treatment coding**

単にコードを動かすのではなく、各方法が**どのようなバイアスを減らそうとしているのか**、逆に**どのような新しい問題を残すのか**を意識して整理した。

---

## 1. Propensity score, IPW, SMD

### 理解したポイント

- baseline covariates から treatment assignment の確率を推定するために、logistic regression を用いる。  
- treatment group には `1 / PS`、control group には `1 / (1 - PS)` を与えることで、観測データから pseudo-population を作る。  
- IPW を計算した後は、**本当に balance が改善したか**を SMD（standardized mean difference）で確認する必要がある。  
- `IPW 後の SMD は理論上ぴったり 0 でなければならない` と覚えるのではなく、**0 に近づくことが望ましい**と理解する方が正確である。実務ではしばしば `|SMD| < 0.1` が 1 つの目安として使われる。  
- propensity score model を作ること自体が目的ではなく、**weighting 後の balance を良くすること**が重要である。  

### 対応コード

- `scripts/01_ps_ipw_smd_demo.py`

### 方法論的に重要な点

- prediction accuracy が高いことと、causal inference における balance が良いことは同じではない。  
- PS model が誤指定されると、IPW を使っても交絡が十分に除去されない可能性がある。  
- したがって、PS 推定 → weighting → SMD 診断、という流れを 1 セットで理解する必要がある。  

### 誤解しやすい点

- 「logistic regression を使えば自動的に因果効果が分かる」という理解は誤りである。  
- 「IPW をかけたら必ず SMD = 0 になる」という理解も強すぎる。  
- 「予測モデルが良ければ PS model としても良い」と単純化するのも危険である。  

---

## 2. Time-zero 問題：naive, landmark, time-dependent treatment coding

### 理解したポイント

#### Naive
- 治療開始時点を無視して、最初から treated / untreated を固定的に割り当てると、time-zero の扱いを誤る可能性がある。  
- 状況によっては immortal time bias を生み、治療効果を過大評価し得る。  
- 一方で、今回の「致命的な毒薬」シミュレーションでは、group 自体が最初から固定されているため、そこでは immortal time bias というより、**全期間で見た有害性がそのまま出る**構造である。  

#### Landmark
- ある時点（例えば day 30）を新しいスタート地点にして、その時点まで生存した人だけを比較する。  
- これにより、時間順序をある程度明確にできる。  
- しかし、landmark 時点以前に死亡した人を除外するため、**survivor selection / selection bias** が入る。  
- したがって、landmark analysis は元の全患者集団に対する効果ではなく、**その時点まで生存した集団に対する効果**を見ていることになる。  

#### Time-dependent treatment coding
- 治療を baseline 固定変数として扱わず、`A(t)` として時間とともに更新する。  
- delayed treatment initiation を正しく扱えるため、time order を最も自然に反映しやすい。  
- ただし、これで全て解決するわけではない。特に、時間とともに変化する交絡（time-varying confounding）がある場合には、追加の方法が必要になる。  

### 対応コード

- `scripts/02_time_zero_methods_demo.py`

### 方法論的に重要な点

- どの方法が「正しいか」は、単純にコードの書き方ではなく、**どの estimand を目指しているか**と結びついている。  
- landmark は簡単で分かりやすいが、元の target population を変えてしまう。  
- time-dependent Cox model は時間順序の扱いとしては自然だが、time-varying confounding まで自動的に解決するわけではない。  

### 誤解しやすい点

- 「time-dependent Cox model を使えば全部終わり」という理解は誤りである。  
- 「landmark は bias を消す方法」とだけ理解するのも不十分で、**何を除外し、どの集団の効果に変わったのか**を明確にする必要がある。  

---

## この段階のコード一覧

- `scripts/01_ps_ipw_smd_demo.py`  
  Logistic regression による PS 推定、IPW 計算、SMD の before/after 比較。

- `scripts/02_time_zero_methods_demo.py`  
  「致命的な毒薬」シミュレーションによる naive と landmark の比較、および time-dependent treatment coding の最小例。

- `docs/self_summary_ja.md`  
  今日理解した内容を、日本語で簡潔にまとめたメモ。

---

## 次に学ぶ内容と目標

- stabilized weight を導入し、極端な weight を少し抑える考え方を理解する。  
- overlap / positivity violation があるときに何が起こるかを学ぶ。  
- doubly robust estimation の最小例を実装する。  
- time-varying confounding がある場合に、なぜ MSM が必要になるのかを整理する。  
- SMD 以外の balance 診断（weight distribution, effective sample size など）も確認する。
