---
title: "バーガース方程式の数値解法"
description: "風上差分、保存型差分、およびGodunov法を用いた非線形偏微分方程式の数値解法。"
pubDate: "2025-07-15"
heroImage: "/numerical-computation-burgers-equation/result3.jpg"
badge: "Academic"
tags: ["numerical-methods", "pde"]
---

## 背景 (Background)

天気予報における大気の流れ、飛行機の翼を流れる空気、あるいは高速道路で突如として発生する交通渋滞の波。これら自然界や社会で観察されるダイナミックな「流れ」や「波」の現象は、多くの場合、複雑な「非線形偏微分方程式」によって記述されます。しかし、これらの数式はあまりにも複雑で、紙と鉛筆だけで完璧な答え（解析解）を導き出すことはほとんど不可能です。そこで現代の科学技術では、コンピュータの力を使って空間と時間を細かく区切り、近似的に解を求める「数値計算」が不可欠となっています。本研究では、流体力学における衝撃波の形成を記述する代表的なモデル「バーガース（Burgers）方程式」を題材に、複数の高度な数値計算アルゴリズムを実装し、目に見えない数学の波をコンピュータ上でシミュレーションします。

本プロジェクトでは、非線形偏微分方程式であるBurgers（バーガース）方程式に対して、風上差分格式、保存型差分格式、およびGodunov法を用いて数値求解を行いました。さらに、Pythonを用いてそれぞれの数値解をシミュレーション・可視化し、異なる差分手法が解の挙動（不連続面や衝撃波の伝播など）に与える影響を比較・考察しました。

## 非保存型バーガース方程式の数値計算

バーガース方程式を非保存型のまま差分化して数値的に解きます。

$$
  q_j^{n+1} = q_j^n - \Delta t \cdot q_j^n \cdot \frac{q_j^n - q_{j-1}^n}{\Delta x}
$$

これは非保存型バーガース方程式の流れが正（$q > 0$）の場合の風上差分であり、流れの向きによって差分形式を切り替える必要があります。そのため、非保存型のバーガース方程式を統一的に記述できるように、以下の形とします。

$$
  q_j^{n+1} = q_j^n - \Delta t \left[
    s_1 \cdot \frac{q_j^n - q_{j-1}^n}{\Delta x} +
    s_2 \cdot \frac{q_{j+1}^n - q_j^n}{\Delta x}
  \right]
$$

ここで：

$$
  s_1 = \frac{q_j^n + |q_j^n|}{2}, \qquad
  s_2 = \frac{q_j^n - |q_j^n|}{2}
$$

この式により、統一的な計算が可能です。以下のPythonコードを用いて非保存型差分法を実装しました。

```python
import numpy as np
import matplotlib.pyplot as plt
%matplotlib inline

c = 1
dt = 0.05
dx = 0.1

jmax = int(21 * 0.1 / dx)
nmax = 10

interval = 2

# q < 0
x = np.linspace(0, dx * (jmax - 1), jmax)

q = np.zeros(jmax)
for j in range(jmax):
    if (j < jmax / 2):
        q[j] = 0
    else:
        q[j] = -1

plt.figure(figsize=(7,7), dpi=100)
plt.rcParams["font.size"] = 22

# 初期分布の可視化
plt.plot(x, q, marker='o', lw=2, label='n=0')

for n in range(1, nmax + 1):
    qold = q.copy()
    for j in range(1, jmax-1):
        s1 = (qold[j] + np.abs(qold[j])) / 2
        s2 = (qold[j] - np.abs(qold[j])) / 2
        q[j] = qold[j] - dt * (s1 * (qold[j] - qold[j - 1]) / dx + s2 * (qold[j + 1] - qold[j]) / dx)

    # 各ステップの可視化
    if n % interval == 0 and n >= 0 :
        plt.plot(x, q, marker='o', lw=2, label=f'n={n}')

plt.grid(color='black', linestyle='dashed', linewidth=0.5)
plt.xlim([0, 2.0])
plt.xlabel('x')
plt.ylabel('q')
plt.legend()
plt.show()
```

ここで初期条件としては $dx = 0.1$, $dt = 0.05$, $n_{\text{max}} = 10$、$q(x) = -1 \, (x \geq 1.0)$, $q(x) = 0 \, (x < 1.0)$とし、非保存型の風上差分を計算しました。その結果は以下の通りです。

![非保存型差分q<0の数値解（n=0 から n=10）](/numerical-computation-burgers-equation/result1.jpg)

初期に存在する不連続なステップ関数（$q=0$ と $q=-1$ の境界）は、時間の経過とともにその形状を維持したまま移動していないことがわかります。ここで、

$$
s_1 = \frac{q_j^n + |q_j^n|}{2}, \quad
s_2 = \frac{q_j^n - |q_j^n|}{2}
$$

これにより、$q_j^n = 0$ のときは $s_1 = 0$, $s_2 = 0$ のため、値が移動しません。しかし、$q_j^n =-1$ の領域では、$s_1 = 0$, $s_2 = -1 $ となり、代入して以下の形となります。

$$
  q_j^{n+1} = -1 - \Delta t \left[
 0  +
    (-1) \cdot \frac{-1 - (-1)}{\Delta x}
  \right]
  = -1 =  q_j^{n}
$$

つまり、どの領域の格子点も時間とともに $q$ の値が一切変化せず、数値解が更新されない状態となります。これにより、非保存型バーガース方程式は計算が簡潔で方向の風上差分が自動的に実装される一方で、初期条件に依存して解が“凍結”する場合があります。本計算においては、$q(x)=0$ または $q(x)=-1$ のように定数で構成されたステップ関数が入力されたため、差分項が消滅し、更新が発生しなかったことがわかります。

## 保存型バーガース方程式とMurman-Cole法

バーガース方程式を保存型の形に変形すると、以下のようになります。

$$
  \frac{\partial q}{\partial t} + \frac{\partial}{\partial x} \left( \frac{q^2}{2} \right) = 0
$$

この形式では物理量 $q$ が時間とともに移流しながら保存される性質を持っています。方程式を差分化するために、数値流束 $F_{j+1/2}$ を導入し、以下のような保存型差分形式で離散化し、$F_{j+1/2}$ として Murman–Cole 法を用いました。

$$
  q_j^{n+1} = q_j^n - \frac{\Delta t}{\Delta x} \left( F_{j+\frac{1}{2}} - F_{j-\frac{1}{2}} \right)
$$
$$
  f(q) = \frac{q^2}{2}, 
$$
$$
  c = \frac{q_j + q_{j+1}}{2}, 
$$
$$
  F_{j+\frac{1}{2}} = \frac{f(q_j) + f(q_{j+1})}{2} - \frac{\mathrm{sgn}(c)}{2} \left( f(q_{j+1}) - f(q_j) \right)
$$

このような形では、境界面で $c$ の符号に応じて適切な方向の差分を自動的に計算できます。

```python
import numpy as np
import matplotlib.pyplot as plt
%matplotlib inline

dt = 0.02
dx = 0.1

jmax = 21
nmax = 10

def init(q1, q2, dx, jmax):
    xs = -1.0 # 始点
    x = np.linspace(xs, xs + dx * (jmax-1), jmax)
    q = np.array([(float(q1) if i < 0.0 else float(q2)) for i in x])
    return (x, q)

def do_computing(x, q, dt, dx, nmax, ff, order = 1, interval = 2):
    plt.figure(figsize=(7,7), dpi=100)
    plt.rcParams["font.size"] = 22

    # 初期分布の可視化
    plt.plot(x, q, marker='o', lw=2, label='n=0')

    for n in range(1, nmax + 1):
        qold = q.copy()
        for j in range(order, jmax - order):
            ff1 = ff(qold, qold[j], dt, dx, j)
            ff2 = ff(qold, qold[j], dt, dx, j-1)
            q[j] = qold[j] - dt / dx * (ff1 - ff2)

        # 各ステップの可視化
        if n % interval == 0:
            plt.plot(x, q, marker='o', lw=2, label=f'n={n}')

    plt.grid(color='black', linestyle='dashed', linewidth=0.5)
    plt.xlabel('x')
    plt.ylabel('q')
    plt.legend()
    plt.show()

def MC(q, c, dt, dx, j):
    ur = q[j + 1]
    ul = q[j]
    fr = 0.5 * ur**2
    fl = 0.5 * ul**2
    c = 0.5 * (ur + ul)
    return 0.5 * (fr + fl - np.sign(c) * (fr - fl))

x = np.linspace(0, dx * (jmax - 1), jmax)

q = np.zeros(jmax)
for j in range(jmax):
    if (j <= jmax / 2):
        q[j] = 0
    else:
        q[j] = -1

nmax = 20
do_computing(x, q, dt, dx, nmax, MC, interval = 4)
```

![保存型差分の数値シミュレーション（n=0 から n=10）](/numerical-computation-burgers-equation/result2.jpg)

分布の初期条件は前述と同様にし、他の計算条件としては $\Delta x = 0.1, \Delta t = 0.02, n_{\max}=20$ とし、Murman–Cole 法を用いた保存型数値流束差分スキームで計算を行いました。

結果より、初期に存在した $q=0$ と $q=-1$ の境界は時間の経過とともに左方向へ移動しています。初期の $q=-1$ の位置が、総時間 $t=20\Delta t=0.4$ の間に $x_{\rm shock}=0 + (-0.5)\times0.4 = -0.2$ まで左方向に移動していることが確認できました。

一方、境界付近に約1セル分の幅の拡散領域が見えるのは、Murman–Cole 法が持つ一次精度の影響です。ここでCFL数は

$$
  \mathrm{CFL} = \max|q|\,\frac{\Delta t}{\Delta x}
              = 1\times\frac{0.02}{0.1}=0.2 <1
$$

であり、CFL条件の下で安定に計算されていることが確認できました。

非保存型の風上差分において初期のステップ関数が移動せず、時間とともに不連続位置がそのまま保持されたのに対し、本手法で導入した保存型Murman–Cole 法では、時間経過とともにステップ境界が適切に移動しました。差分形式で保存性を確保し、物理的な保存則を満たしています。一次精度スキームに伴う数値粘性により境界は平滑化されますが、非保存型の完全凍結した場合と比べれば波動の伝播が忠実に捉えられています。

以上により、非保存型は実装が容易であるものの不連続解を正しく扱えない場合があること、そして保存型Murman–Cole 法を用いることで物理的意味のある波動の伝播と保存性が得られることが確認されました。

## Godunov法による局所リーマン問題の解法

次に、バーガース方程式に対して Godunov 法を適用します。Godunov 法では各セル境界での数値流束 $F_{j+1/2}$ を次のように定義します。

$$
  q_j^{n+1}
  = q_j^n
     - \frac{\Delta t}{\Delta x}
       \Bigl(\tilde f_{j+\frac12}^n - \tilde f_{j-\frac12}^n\Bigr)
$$
$$
\tilde f_{j+\frac12}^n   =
\begin{cases}
\displaystyle \tfrac12\,q_{j+1}^2
  &\bigl(q_j>0>q_{j+1}\;\land\;\tilde c_{j+\frac12}
   =\tfrac{q_j+q_{j+1}}2<0\bigr),\\
\displaystyle \tfrac12\,q_{j}^2
  &\bigl(q_j>0>q_{j+1}\;\land\;\tilde c_{j+\frac12}
   =\tfrac{q_j+q_{j+1}}2>0\bigr),\\
0 & (q_j<0<q_{j+1})
\end{cases}
$$

Godunov 法の実装において、状態の分岐を用いることで以下のようにPythonプログラムを作成しました。

```python
import numpy as np
import matplotlib.pyplot as plt
%matplotlib inline

dt = 0.05
dx = 0.1

jmax = 21
nmax = 10

def init(q1, q2, dx, jmax):
    xs = -1 # 始点
    x = np.linspace(xs, xs + dx * (jmax-1), jmax)
    q = np.array([(float(q1) if i < 0.0 else float(q2)) for i in x])
    return (x, q)

def do_computing(x, q, dt, dx, nmax, ff, order = 1, interval = 4):
    plt.figure(figsize=(7,7), dpi=100)
    plt.rcParams["font.size"] = 22

    # 初期分布の可視化
    plt.plot(x, q, marker='o', lw=2, label='n=0')

    for n in range(1, nmax + 1):
        qold = q.copy()
        for j in range(order, jmax - order):
            ff1 = ff(qold, qold[j], dt, dx, j)
            ff2 = ff(qold, qold[j], dt, dx, j-1)
            q[j] = qold[j] - dt / dx * (ff1 - ff2)

        # 各ステップの可視化
        if n % interval == 0:
            plt.plot(x, q, marker='o', lw=2, label=f'n={n}')

    plt.grid(color='black', linestyle='dashed', linewidth=0.5)
    plt.xlabel('x')
    plt.ylabel('q')
    plt.legend()
    plt.show()

def GODUNOV(q, c, dt, dx, j):
    ur = q[j + 1]
    ul = q[j]
    fr = 0.5 * ur**2
    fl = 0.5 * ul**2
    c = 0.5 * (ur + ul)

    if q[j] <= 0 and q[j+1] <= 0:
        return fr
    elif q[j] >= 0 and q[j+1] >= 0:
        return fl
    elif q[j] > 0 > q[j+1]:
        if c < 0:
            return fr
        else:
            return fl
    else:
        return 0

q1 = 1
q2 = 0
x, q = init(q1, q2, dx, jmax)

nmax = 20
do_computing(x, q, dt, dx, nmax, GODUNOV)
```

Godunov 数値流束は分岐を用いて各ケースを判定することで、解を正確に再現できました。プログラムを実行し、以下の結果が得られました。

![保存型差分の数値解（ Godunov 法）](/numerical-computation-burgers-equation/result3.jpg)

Godunov法は、保存型バーガース方程式に対して、各セルの界面（$j+\frac{1}{2}$）における局所リーマン問題を解くことで数値流束 $\tilde{f}_{j+1/2}$ を定義する手法であり、状態に応じた分岐により物理的に妥当な波形を再現できます。

図より、初期状態で不連続に配置された $q=1$ と $q=0$ のステップ関数が、時間の経過とともに拡散して右方向へ移動している様子が確認できます。また、一次精度であるため衝撃波部分には数値的な平滑化が見られますが、非保存型で観察されたような凍結現象は生じていません。

以上より、Godunov法は保存則を守りながら、衝撃波や膨張波を忠実に表現できる数値的信頼性の高い手法であると言えます。