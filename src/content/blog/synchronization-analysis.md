---
title: "メトロノーム同期現象の動画解析"
description: "OpenCV による色領域抽出、重心検出、角度計算、ピーク検出を用いて、単体メトロノームの周期推定と 2 個のメトロノームの同相同期を時系列データとして解析したプロジェクト。"
pubDate: "2025-07-10"
heroImage: "/synchronization-analysis/Figure_4.png"
badge: "CV / Dynamics"
tags: ["synchronization", "computer-vision", "time-series-analysis", "opencv", "python"]
---

## 身近な同期現象

同期現象は、実験室だけで見られる特別な現象ではない。ばらばらに始まった拍手が、しばらくすると自然に同じテンポへ近づくことがある。夜に鳴く蛙の声が周囲のリズムに引き込まれるように聞こえることもあり、ホタルの発光、歩行者の足取り、機械や電気回路の振動にも似た現象が現れる。

このような現象に共通しているのは、個々の要素が完全に独立して動いているわけではなく、周囲からの小さな影響を受けながら、自分のリズムを少しずつ変えていく点である。メトロノーム同期は、その仕組みを目に見える形で観察できる身近なモデルである。

## 1. プロジェクトの概要 (Introduction)

本プロジェクトの背景には、複数の振動体がどのような条件で互いに影響し合い、最終的に同じリズムへ近づくのかを調べるという目的がある。メトロノーム同期は、同期現象を観察しやすい物理系であり、個々のメトロノームが直接接触していなくても、板の揺れを介して相互作用する点に特徴がある。

本プロジェクトでは、メトロノームの運動を撮影した動画から針の位置を抽出し、角度の時系列データとして解析した。対象は、単体メトロノームの周期推定と、2 個のメトロノームが可動な板を介して同相同期する現象である。

同期現象は、複数の振動系が相互作用を通じてリズムや位相を揃える非線形現象の一つである。本実験では、目視による観察だけでなく、OpenCV を用いた画像処理によってメトロノームの針と板の動きを数値化し、時間変化として可視化した。

動画撮影は授業内の班実験として行われた。本記事では、その動画データをもとに、フレーム抽出、色領域検出、重心計算、角度推定、ピーク検出を組み合わせた解析手順を整理する。

![単体メトロノームの撮影フレーム](/synchronization-analysis/centroidframe.jpg)

---

## 2. 解析対象と実験条件 (Data & Setup)

解析では、主に次の 2 種類の動画を扱った。

1. 単体メトロノームの針運動を撮影した動画
2. 2 個のメトロノームを可動な板に載せ、同相同期を観察した動画

単体メトロノームの解析では、針に付けた色マーカーを追跡し、1 周期に要する時間から BPM を推定した。同期実験では、左右 2 個のメトロノームの針先と、板の代表点を同時に検出し、それぞれの角度を時系列信号として記録した。

同期実験では、メトロノームを BPM 160 に設定し、2 つのブックエンド間の距離を 41 cm、カメラと板の距離を 39 cm、板を吊るす紐の長さを約 13.7 cm として撮影した。

---

## 3. 動画から角度時系列を得る方法 (Method)

### 3.1 色領域抽出と重心検出

動画はフレーム画像の列として読み込み、各フレームを BGR から HSV 色空間へ変換した。HSV を用いることで、照明条件の影響を受けながらも、付箋やマーカーの色に基づいて対象領域を抽出しやすくなる。

処理の流れは以下の通りである。

1. `cv2.VideoCapture()` により動画を読み込む。
2. `cv2.cvtColor()` により BGR 画像を HSV 画像に変換する。
3. `cv2.inRange()` により、メトロノームのマーカー色に対応する領域を抽出する。
4. `cv2.medianBlur()` により、マスク画像のノイズを抑える。
5. `cv2.moments()` から重心座標を求める。
6. 支点座標と重心座標のベクトルから角度を計算する。

次の画像は、色領域抽出によりメトロノームのマーカー部分を追跡している様子である。

![色領域抽出によるメトロノーム針先の検出](/synchronization-analysis/ezgif-5021e2ff62aeed46.gif)

### 3.2 重心座標から角度を計算する

支点を $p=(p_x,p_y)$、検出された重心を $c=(c_x,c_y)$ とする。画像座標では下方向が正になるため、実装では縦方向の向きを補正しながら、支点から重心へのベクトルを用いて角度を計算した。

概念的には、縦方向を基準軸として次のように角度を求める。

$$
\theta
= \operatorname{sgn}(c_x - p_x)
\arccos
\left(
\frac{|p_y - c_y|}
{\sqrt{(c_x - p_x)^2 + (p_y - c_y)^2}}
\right)
$$

実装では、左右の向きを保つために、重心が支点の左側にある場合は負の角度、右側にある場合は正の角度として扱った。

```python
def calc_angle(centroid, pivot, frame_h):
    if centroid is None:
        return None

    cx, cy = centroid
    px, py = pivot
    vx = cx - px
    vy = py - cy

    if vy > 0:
        cosine_value = vy / math.sqrt(vx ** 2 + vy ** 2)
    else:
        cosine_value = -vy / math.sqrt(vx ** 2 + vy ** 2)

    theta = math.acos(cosine_value)

    if vx < 0:
        degree = -math.degrees(theta)
    else:
        degree = math.degrees(theta)

    return degree
```

---

## 4. 単体メトロノームの周期推定 (Single Metronome Analysis)

単体メトロノームの動画では、各フレームで検出した針先の角度を時系列信号として記録した。得られた角度波形は、おおむね周期的な振動を示しており、ピーク間隔から周期を推定できる。

![単体メトロノームの角度時系列](/synchronization-analysis/angle_plot.png)

ピーク検出には `scipy.signal.find_peaks()` を用いた。同じ向きの極大値の間隔を $\Delta f$ フレーム、動画のフレームレートを $\mathrm{fps}$ とすると、1 周期の時間 $T$ は次のように表される。

$$
T = \frac{\Delta f}{\mathrm{fps}}
$$

メトロノームは 1 周期で左右の拍を 2 回刻むため、BPM は次の式で推定した。

$$
\mathrm{BPM}
= \frac{120}{T}
= \frac{120 \cdot \mathrm{fps}}{\Delta f}
$$

実行結果の一例では、動画のフレームレートは約 59.94 fps、平均ピーク間隔は約 80 フレームであり、推定 BPM は約 89.91 となった。撮影時の設定値は BPM 92 であり、推定値との差は、機械的な揺らぎ、カメラ角度、HSV マスクのノイズ、重心検出の誤差などに由来すると考えられる。

---

## 5. 2 個のメトロノームの同相同期解析 (Synchronization Analysis)

同期実験では、左右のメトロノームに同系統の色マーカーを付け、板には別の色領域を用意した。左右のメトロノームは同色で検出されるため、各フレームで得られた上位 2 つの輪郭を抽出し、前フレームの位置に近い方を同じメトロノームとして対応付けた。

板については、別の HSV 範囲で抽出し、最大輪郭の重心を板の代表点として扱った。これにより、左メトロノーム、右メトロノーム、板の 3 つの角度系列を同時に得ることができる。

次の GIF は、メトロノームと板を検出し、角度を動画上に重ねて表示したものである。

![同期実験におけるメトロノームと板の検出結果](/synchronization-analysis/result2.gif)

検出された角度系列をプロットすると、左右のメトロノームの角度は時間とともにほぼ同じ位相で振動していることが確認できる。板の角度変化はメトロノームに比べて小さいが、同じ周期で変化しており、板が 2 つのメトロノーム間の相互作用を媒介していることが読み取れる。

![左右メトロノームと板の角度時系列](/synchronization-analysis/Figure_4.png)

図では、Angle1 と Angle2 が左右のメトロノームの角度、Angle3 が板の角度を表す。Angle1 と Angle2 は大きな振幅を持つ周期信号として表れ、同期状態ではピークと谷のタイミングが揃っている。Angle3 は小振幅であるが、メトロノームの運動と同期した周期変動を示す。

---

## 6. 実装上の工夫 (Implementation Notes)

本解析で重要だった点は、単に色領域を抽出するだけでなく、時系列解析に使える形で対象を安定して追跡することである。

特に、2 個のメトロノームの解析では、同じ色のマーカーが 2 つ存在するため、各フレームで検出された輪郭を左右のメトロノームへ安定して割り当てる必要があった。初回は x 座標の大小で左右を決め、その後は前フレームの位置に近い輪郭を同一対象として対応付けることで、時系列中でラベルが入れ替わる問題を抑えた。

```python
if prev_m1 is not None and prev_m2 is not None and len(cents) == 2:
    d0 = (cents[0][0] - prev_m1[0]) ** 2 + (cents[0][1] - prev_m1[1]) ** 2
    d1 = (cents[1][0] - prev_m1[0]) ** 2 + (cents[1][1] - prev_m1[1]) ** 2
    if d0 < d1:
        metro1_centroid, metro2_centroid = cents[0], cents[1]
    else:
        metro1_centroid, metro2_centroid = cents[1], cents[0]
else:
    metro1_centroid, metro2_centroid = sorted(cents, key=lambda p: p[0])
```

また、板とメトロノームを別々の HSV 範囲で検出することで、板の微小な揺れも角度系列として取り出せるようにした。

---

## 7. 考察と限界 (Discussion)

本解析により、メトロノームの周期運動を動画から抽出し、単体メトロノームの BPM 推定と、2 個のメトロノームの同相同期の可視化を行うことができた。視覚的な観察だけではなく、角度時系列として扱うことで、同期状態をより定量的に確認できる。

一方で、解析精度にはいくつかの制約がある。HSV による色領域抽出は照明条件や反射に影響されやすく、手指や背景の色が一時的なノイズになる可能性がある。また、支点座標は手動で設定しているため、カメラ角度や設置位置が変わると再調整が必要になる。

今後は、カメラ位置の固定、支点の自動推定、位相差の明示的な計算、相互相関や Hilbert 変換を用いた位相解析などを導入することで、同相同期と逆相同期の違いをより定量的に比較できると考えられる。

---

## 8. 関連リポジトリ

<div class="not-prose my-10">
  <a
    href="https://github.com/Fengmc2001/portfolio-projects/tree/main/synchronization-analysis"
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
        <p class="m-0 mt-1 text-lg font-semibold text-slate-900">synchronization-analysis</p>
        <p class="m-0 mt-2 text-sm leading-relaxed text-slate-600">
          Python code and Markdown source for the metronome synchronization analysis project.
        </p>
      </div>
    </div>
  </a>
</div>
