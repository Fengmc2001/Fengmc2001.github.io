---
title: "項目反応理論（IRT）に基づく動的e-Testingシステムの構築"
description: "従来のテスト理論の限界を克服し、IRT（2パラメータロジスティックモデル）、ベイズ推論、ニュートン法を用いて受験者の能力値を動的に推定するe-Testingシステムのフルスクラッチ開発。"
pubDate: "2024-05-09"
heroImage: "/irt-etesting/1.jpg"
badge: "IRT / Web Sys"
tags: ["item-response-theory", "bayesian", "maximum-likelihood", "newtons-method", "ui-ux"]
---

## 身近な出発点

同じ試験を受けても、受験者の得意分野や能力水準は大きく異なる。やさしすぎる問題だけでは高得点層の違いが見えにくく、難しすぎる問題だけでは初中級者の理解度を測りにくい。英語試験や資格試験の形式が見直されるときにも、限られた問題数でどのように受験者の能力を公平かつ細かく推定するかは重要な論点になる。

この問いに対して、項目反応理論（IRT）は、単なる正答率ではなく、問題ごとの難易度や識別力を考慮して能力値を推定する枠組みを与える。本プロジェクトでは、その考え方を Web 上で動く e-Testing システムとして実装することを試みた。

## 1. プロジェクトの概要 (Introduction)

本プロジェクトでは、従来のテスト理論（正答率＝能力値）の限界を克服するため、現代テスト理論である項目反応理論（Item Response Theory: IRT）を用いたe-Testingシステムをフルスクラッチで構築しました。
IRTは、TOEFLやSPIなどの大規模な適応型テスト（CAT）の基盤となる統計モデルであり、各問題の特性（難易度・識別力）と受験者の解答パターンから、受験者の真の能力値を確率的に推定します。

本プロジェクトの目的は、単に理論を学ぶだけでなく、Webフロントエンド（HTML/JavaScript）を用いて実際に動作するテストシステムを実装し、さらに最尤推定やニュートン法を用いた最適化アルゴリズムをバックエンド（またはクライアントサイドのロジック）に統合することです。

---

## 2. コアとなる理論 (Core Theory)

### 2.1 ベイズの定理と最尤推定
能力推定の根底には、結果（解答データ）から原因（受験者の能力）を逆算するベイズ推論と最尤推定（Maximum Likelihood Estimation: MLE）があります。

$$
P(\theta \mid X) = \frac{P(\theta)}{P(X)} P(X \mid \theta)
\propto P(\theta)P(X \mid \theta)
$$

ここで、$X$ は受験者の解答パターン、$\theta$ は受験者の能力値です。尤度 $P(X \mid \theta)$ を最大化する $\theta$ を探すことが、能力値推定の基本アプローチとなります。

### 2.2 2パラメータロジスティックモデル（2PLM）
本システムでは、項目 $i$ に対する受験者 $j$ の正答確率を以下の2パラメータロジスティックモデルで定義します。

$$
P_i(\theta_j) = \frac{1}{1 + \exp(-D a_i(\theta_j - b_i))}
$$

- $\theta_j$: 受験者 $j$ の能力値パラメータ
- $a_i$: 項目 $i$ の識別力パラメータ（曲線の傾き。能力の高低を区別する力）
- $b_i$: 項目 $i$ の困難度パラメータ（正答率が50%となる能力値）
- $D$: スケーリング定数（通常 $1.7$ を用い、正規累積分布に近似させる）

![2パラメータロジスティックモデルにおける項目特性曲線](/irt-etesting/1.jpg)

---

## 3. 数式の導出と展開 (Derivations & Expansions)

### 3.1 複数問題に対する対数尤度関数の最大化
局所独立性（各問題への解答が独立である）を仮定すると、複数問題の解答パターン $X_i = (x_{i1}, x_{i2}, \dots, x_{i n_i})$ に対する尤度は、各問題の正答・誤答確率の積となります。計算誤差を防ぐため、対数尤度関数 $\ln P(\theta \mid X_i)$ を最大化します。

$$
\hat{\theta}
= \operatorname*{arg\,max}_{\theta}
\left[
\ln P(\theta)
+ \sum_{j=1}^{n_i}
\left\{
x_{ij}\ln P_i(\theta)
+ (1 - x_{ij})\ln\left(1 - P_i(\theta)\right)
\right\}
\right]
$$

### 3.2 フィッシャー情報量と標準誤差
推定された能力値 $\hat{\theta}$ の信頼性を評価するため、項目情報量関数 $I_i(\theta)$ と標準誤差 $se(\hat{\theta})$ を計算します。

$$
I_i(\theta) = D^2 a_i^2 P_i(\theta)(1 - P_i(\theta))
$$
$$
\operatorname{se}(\hat{\theta})
= \frac{1}{\sqrt{\sum_i I_i(\hat{\theta})}}
$$

### 3.3 ニュートン法による最適化アルゴリズム
解析的に最大値を求めるため、対数尤度関数の一階微分（勾配）と二階微分（ヘッセ行列）を用いたニュートン法を実装しました。

$$
\theta_{\mathrm{new}}
= \theta_{\mathrm{old}}
- \frac{f'(\theta_{\mathrm{old}})}{f''(\theta_{\mathrm{old}})}
$$

---

## 4. 実装と独自の工夫 (Implementation & Ingenuity)

![システム全体の構成図](/irt-etesting/irt-system-overview.png)

### 4.1 ニュートン法による能力値推定ロジック (C言語)
対数尤度関数の最大化を解析的に行うため、C言語にてロジスティック関数から尤度、勾配、ヘッセ行列を算出するニュートン法アルゴリズムを実装しました。事前分布として標準正規分布 $N(0,1)$ を組み込んでいます。

```c
// 2パラメータロジスティック関数の定義
double logistic(double a, double theta, double b) {
    return 1.0 / (1.0 + exp(-a * (theta - b)));
}

// 対数尤度関数 (Log-likelihood + Log-prior)
double log_likelihood(double theta, double a[], double b[], int x[], int size) {
    double likelihood_sum = 0.0;
    for (int i = 0; i < size; i++) {
        double p_i = logistic(a[i], theta, b[i]);
        likelihood_sum += x[i] * log(p_i) + (1 - x[i]) * log(1 - p_i);
    }
    double prior = -0.5 * theta * theta;
    return likelihood_sum + prior;
}

// ヘッセ行列 (Second derivative) の算出
double log_likelihood_double_prime(double theta, double a[], double b[], int x[], int size) {
    double hessian_sum = 0.0;
    for (int i = 0; i < size; i++) {
        double p_i = logistic(a[i], theta, b[i]);
        hessian_sum -= a[i] * a[i] * p_i * (1 - p_i);
    }
    return hessian_sum - 1.0; 
}

// ニュートン法による最適化ループ
double newtons_method(double theta_init, double a[], double b[], int x[], int size) {
    double theta = theta_init;
    for (int i = 0; i < MAX_ITER; i++) {
        double grad = log_likelihood_prime(theta, a, b, x, size);
        double hess = log_likelihood_double_prime(theta, a, b, x, size);
        double theta_new = theta - grad / hess;
        if (fabs(theta_new - theta) < TOL) break;
        theta = theta_new;
    }
    return theta;
}
```

### 4.2 独自の工夫：UI/UX改善による能力値推定精度の向上
単なる理論の実装にとどまらず、動的e-Testingシステムのフロントエンド（JavaScript/HTML）開発において、ヒューマンエラー（誤操作や適当な解答）が能力値推定に与える悪影響（過小評価）を防ぐための独自のアプローチを実装しました。

1. 「わからない（スキップ）」機能: 解答に確信がない場合、適当に解答して誤答となる（=能力値が不当に下がる）のを防ぐため、未回答(`-1`)の選択肢を実装しました。この機能により、未回答の項目は能力値推定の計算（フィルター）から除外され、ノイズのない高精度な推定が可能になります。
2. 状態保存と復元機能（Undo）: テスト中に誤って選択してしまった場合のために、各設問解答時のすべての状態履歴（問題番号、現在の能力値、解答配列、出題履歴など）をオブジェクトとして `exam.history` スタックに保存し、「戻る」ボタンで完全に状態を復元（ポップ）できる機能を独自に設計・実装しました。

```javascript
// 独自の工夫1: 状態のバックアップと復元
const continueTesting = async () => {
  let item = await getItem(exam.n);
  if (item.type !== 'confidence') {
    // 現在のステータスを深いコピーで履歴スタックに保存
    exam.history.push({
      n: exam.n,
      theta: exam.theta,
      x: [...exam.x],
      bank: [...exam.bank],
      ans: [...exam.ans],
      time: [...exam.time]
    });
  }

  const choice = parseInt(document.getElementById('exam-box').choices.value);

  if (choice == 4) { 
    // 独自の工夫2: 「わからない」を選択した場合 (-1として記録)
    exam.x.push(-1); 
    exam.ans.push("未回答");
  } else {
    // 有効回答の場合
    exam.x.push(choice == item.correct ? 1 : 0);
    exam.ans.push(item.choices[choice]);
    exam.bank.push(item);
    
    // 未回答(-1)を filter 関数で除外して能力値(theta)を高精度に再計算
    exam.theta = estimation(exam.x.filter(v => v >= 0), exam.bank, -3, 3, 0.1);
  }
  exam.n++;
}

// 履歴スタックを用いたUndo（戻る）機能
const goBack = async () => {
  if (exam.history.length === 0) return;

  const prev = exam.history.pop();
  exam.n = prev.n;
  exam.theta = prev.theta;
  exam.x = prev.x;
  exam.bank = prev.bank;
  exam.ans = prev.ans;
  exam.time = prev.time;
  
  const item = await getItem(exam.n);
  createExam(item); // 前の問題を再描画
}
```

![解答画面のインタフェース例](/irt-etesting/samplegraph2.png)

![項目提示中の画面例](/irt-etesting/irt-answering.png)

![試験終了後の結果表示画面](/irt-etesting/irt-result.png)

### 4.3 統計的考察：主観的自信度と推定能力値の乖離分析
システム実装後、複数名の被験者データを収集し、算出した推定能力値 $\theta$ と正答率、および被験者の「主観的な自信度（5段階評価）」のピアソン相関係数 $r$ を算出して分析を行いました。

$$
r
= \frac{
\sum_i (C_i - \bar{C})(\theta_i - \bar{\theta})
}{
\sqrt{
\sum_i (C_i - \bar{C})^2
\sum_i (\theta_i - \bar{\theta})^2
}
}
\approx -0.039
$$

分析の結果、能力値 $\theta$ と正答率には強い正の相関が確認されましたが、「主観的な自信度」と「推定能力値」の相関係数はほぼゼロ（無相関）でした。
これは、識別力 $a$ が極端に高い問題（難易度 $b$ は低いが、能力の高低を鋭く分ける問題）において、被験者が誤答した場合にペナルティが大きく働き、本人の自信とは裏腹に能力値が低く推定されるという、IRT特有の現象を実証する結果となりました。

---

## 5. 結論と今後の展望 (Conclusion & Future Work)
本プロジェクトでは、統計理論である項目反応理論（IRT）を、数学的な導出からバックエンドのアルゴリズム実装、そしてフロントエンドの動的Webアプリケーション構築に至るまで一貫して実現しました。

特に、理論をシステムに落とし込む過程で発生するヒューマンエラーに対し、「わからない」ボタンによるノイズ除去と操作ミスの取り消し機能（Undoスタック）を独自に実装したことで、能力値推定の精度と信頼性を大幅に向上させることができました。

今後は、解答時間や誤謬率などの複数の評価指標を統合的に取り扱う多次元IRTアルゴリズムへの拡張や、受験者の特性を踏まえた個別最適化問題（適応的アイテム選択）の探索、さらに長期的な学習履歴に基づく予測モデルの開発へと展開していきたいと考えています。

---

## 関連リポジトリ

<div class="not-prose my-10">
  <a
    href="https://github.com/Fengmc2001/portfolio-projects/tree/main/irt-adaptive-testing-demo"
    target="_blank"
    rel="noreferrer"
    class="group block rounded-xl border border-slate-200 bg-slate-50/80 p-5 shadow-sm transition hover:-translate-y-0.5 hover:border-slate-300 hover:bg-white hover:shadow-md"
  >
    <div class="flex items-start gap-4">
      <div class="flex h-11 w-11 shrink-0 items-center justify-center rounded-full border border-slate-200 bg-white text-slate-800">
        <svg viewBox="0 0 24 24" aria-hidden="true" class="h-6 w-6 fill-current">
          <path d="M12 2C6.48 2 2 6.58 2 12.26c0 4.53 2.87 8.38 6.84 9.74.5.1.68-.22.68-.49 0-.24-.01-.88-.01-1.73-2.78.62-3.37-1.38-3.37-1.38-.45-1.19-1.11-1.5-1.11-1.5-.91-.64.07-.63.07-.63 1 .07 1.53 1.06 1.53 1.06.9 1.57 2.36 1.12 2.94.85.09-.67.35-1.12.63-1.38-2.22-.26-4.56-1.14-4.56-5.06 0-1.12.39-2.03 1.03-2.75-.1-.26-.45-1.31.1-2.72 0 0 .84-.28 2.75 1.05A9.3 9.3 0 0 1 12 6.98c.85 0 1.7.12 2.5.34 1.9-1.33 2.74-1.05 2.74-1.05.55 1.41.2 2.46.1 2.72.64.72 1.03 1.63 1.03 2.75 0 3.93-2.34 4.8-4.57 5.05.36.32.68.94.68 1.9 0 1.38-.01 2.49-.01 2.82 0 .27.18.59.69.49A10.08 10.08 0 0 0 22 12.26C22 6.58 17.52 2 12 2Z"></path>
        </svg>
      </div>
      <div>
        <p class="m-0 text-sm font-medium text-slate-500">GitHub</p>
        <p class="m-0 mt-1 text-lg font-semibold text-slate-900">irt-adaptive-testing-demo</p>
        <p class="m-0 mt-2 text-sm leading-relaxed text-slate-600">
          IRT に基づく適応型 e-Testing デモのソースコードと関連ファイル。
        </p>
      </div>
    </div>
  </a>
</div>
