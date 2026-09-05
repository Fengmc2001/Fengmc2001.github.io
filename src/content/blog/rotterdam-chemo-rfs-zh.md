---
title: "Rotterdam乳腺癌数据：从混杂到重叠加权"
description: "基于最终发表的生存分析完整流程、复现结果与解释边界。"
pubDate: "2026-09-05"
heroImage: "/biostatistics/rotterdam-chemo-rfs/presentation-plot-04.png"
badge: "Biostatistics"
tags: ["biostatistics", "survival-analysis", "causal-inference", "overlap-weighting", "r"]
---

[日本語](/ja/blog/rotterdam-chemo-rfs) · [中文](/zh/blog/rotterdam-chemo-rfs-zh) · [English](/blog/rotterdam-chemo-rfs-en)

**[GitHub · Code / コード / 代码](https://github.com/Fengmc2001/rotterdam-chemo-rfs)**

作者：Ziyin Wu（WU ZIYIN）。本文基于 2026 年 8 月 18 日的最终汇报及配套 R 代码。这是一份个人学习解答，并非官方答案、经过同行评审的研究或医疗建议。公开文档的整理与翻译使用了 AI 辅助；汇报代码另行保留。

**[打开原稿逐页 HTML 幻灯片](https://fengmc2001.github.io/rotterdam-chemo-rfs/slides/)** — 删除原 PDF 整个第1页，按原顺序保留第2～28页（27页）的排版与内容；采用字形路径 SVG，并附可选择、可检索的原文 HTML。幻灯片保持日语，解说文章保留三语。后续页的文献及所属信息按原稿保留。

[复现与发布记录](https://github.com/Fengmc2001/rotterdam-chemo-rfs/blob/main/REPRODUCIBILITY.md) · 验证命令：`python3 analysis/verify.py`

## 1. 问题与范围

使用 `survival::rotterdam`，比较记录为接受化疗与未接受化疗患者的无复发生存（recurrence-free survival，RFS），并解释为什么观察性比较并不自动等同于治疗效应。该登记数据包含 2,982 名原发性乳腺癌患者。时间零点为初次手术；RFS 以首次观察到的复发或死亡为终点。最终汇报先报告全队列的未调整比较，再进行一项目标人群不同的补充调整分析。

## 2. 复现

在仓库根目录下，如有需要，先在 R 中安装所需软件包：

```r
install.packages(c("survival", "ggplot2", "survminer", "WeightIt",
                  "cobalt", "adjustedCurves", "pammtools"))
```

```sh
Rscript analysis/run.R > results/run.log 2>&1
```

`analysis/survival.R` 是最终汇报的原始脚本，而非早期的探索性审查脚本。`analysis/run.R` 在不改变统计公式的前提下，增加了图形设备以及 CSV 和会话信息导出。按上述方式运行时，它只向 `results/` 目录写入文件。Bootstrap 使用随机种子 `20260717`，进行 500 次患者层面的重抽样，并使用单核运行。软件版本见 [sessionInfo](https://github.com/Fengmc2001/rotterdam-chemo-rfs/blob/main/results/sessionInfo.txt)；所安装的软件包版本变化可能导致数值结果变化。原始绘图代码指定了 macOS 上可用的 **Hiragino Sans** 字体。其他平台可能需要为图形替换日文字体；这不会改变统计模型。

数据直接从 R 软件包加载，并非从其他 Rotterdam/Stata 数据集复制。运行时生成的患者级 CSV 文件不纳入公开发布。公开内容不包含入学申请文件、第三方论文 PDF、课程幻灯片或备份文件。

## 3. 分析流程

1. **正确定义 RFS。** 未观察到复发时，将复发时间设为无穷大；未观察到死亡时，将死亡时间设为无穷大。两者的最小值若为有限值，即确定发生事件及其时间。若两种事件均未发生，则按照题目给定的定义，使用两个已记录随访时间中的最大值。以 365.25 天为一年，将天数换算为年数。不能不加区分地直接取两个随访时间列的最小值。
2. **核查数据。** 确认共有 2,982 名不重复的患者、无缺失值，其中 580 人接受化疗、2,402 人未接受化疗，复合终点事件为 1,713 例，删失观察为 1,269 例。
3. **未调整比较。** 估计 Kaplan–Meier 曲线，采用 log–log 变换构建置信区间；使用整个随访期间的数据进行 log-rank 检验。基于独立组的 Greenwood 标准误，采用正态近似报告五年生存率差。检验不显著并不构成两组等效的证据。
4. **解释混杂与重叠。** 治疗并非随机分配。患者背景既与治疗选择相关，也与预后相关。全部 580 名接受化疗的患者均为淋巴结阳性；1,436 名淋巴结阴性患者中没有接受化疗的对照对象。因此，这一分层存在经验性正值性问题，数据无法支持在该分层内进行接受治疗与未接受治疗的比较。
5. **明确改变目标人群。** 将补充分析限制在 1,546 名淋巴结阳性患者中（966 人未接受化疗，580 人接受化疗），随后以其重叠人群为目标，而非原始全队列。
6. **拟合倾向评分。** Logistic 回归对年龄使用自然样条（4 个自由度），对 log(1 + nodes)、log(1 + ER) 和 log(1 + PgR) 分别使用自然样条（各 3 个自由度），并纳入绝经状态、肿瘤大小和分级。最终模型未纳入手术年份和激素治疗。未纳入这些变量并不证明它们不会对所观察到的关联产生混杂。
7. **重叠加权。** 设倾向评分为 e(L)，接受治疗的患者赋予权重 1 − e(L)，未接受治疗的患者赋予权重 e(L)。`WeightIt::weightit(method="glm", estimand="ATO")` 的目标人群，其协变量密度与 e(L)[1 − e(L)]f(L) 成正比。
8. **诊断。** 检查加权前后的标准化均值差（SMD）和有效样本量（ESS）。复现得到的 ESS 为未接受治疗组 277.81、接受治疗组 328.31；所报告的加权后 SMD 绝对值最大约为 0.0126。已测量变量达到良好平衡，并不能证明不存在未测量混杂。
9. **调整后的生存曲线与 RMST。** 使用 `adjustedCurves::adjustedsurv(method="iptw_km", estimand="ATO")`。尽管方法名称含有 IPTW，这里使用的是重叠权重，而非针对 ATE 的逆概率权重。在每一个 bootstrap 样本内重新估计倾向评分和权重。将生存函数积分至五年，得到限制平均生存时间（restricted mean survival time，RMST）；代码也导出十年汇总结果。

## 4. 最终五年结果

以下所有对比均为**化疗组减去未化疗组**。RFS 差值以百分点表示，而非相对百分比。方括号内为 95% 置信区间。

| 分析／指标 | 未化疗 | 化疗 | 差值 |
|---|---:|---:|---:|
| 全队列未调整 RFS | 57.5% [55.5, 59.5] | 53.7% [49.5, 57.7] | −3.8 个百分点 [−8.4, +0.7] |
| 淋巴结阳性重叠人群 RFS | 37.4% [32.4, 42.8] | 47.4% [42.4, 52.7] | +10.0 个百分点 [+2.4, +17.7] |
| 淋巴结阳性重叠人群 RMST | 3.00 年 [2.80, 3.20] | 3.53 年 [3.36, 3.70] | +194 天 [+98, +289] |

未调整的全随访期 log-rank 检验 p 值为 **0.4078**（幻灯片中为 0.408）。精确导出值和执行日志见 [results](https://github.com/Fengmc2001/rotterdam-chemo-rfs/blob/main/results/)。原始幻灯片将 RMST 差值四舍五入至整数天。

![未调整的 Kaplan–Meier 曲线](/biostatistics/rotterdam-chemo-rfs/presentation-plot-02.png)

![协变量平衡](/biostatistics/rotterdam-chemo-rfs/presentation-plot-03.png)

![重叠加权生存曲线](/biostatistics/rotterdam-chemo-rfs/presentation-plot-04.png)

## 5. 如何解释表面上的方向反转

粗略比较结果**不能**说明化疗对患者有害，调整后的结果也**不能**证明化疗带来了因果上的获益。治疗组之间的基线特征存在显著差异。此外，两项分析之间不仅进行了调整，目标人群也发生了变化；因此，不能将差值符号的变化完全归因于消除了混杂。

一个通俗的类比是：冰淇淋购买量与中暑人数可能同时上升，因为炎热天气会使两者都增加。同样，患者特征可能同时影响治疗选择和复发／死亡风险。加权使两组的*已测量*背景更具可比性，但无法找回未测量的变量，也无法为某个分层中不存在的治疗组创造证据。

RMST 对比为 +194 天，表示在淋巴结阳性重叠人群中，**最初五年内**累积的平均无复发时间相差 194 天。它不是总预期寿命的增加，也不能预测某一位患者的获益。

## 6. 局限性与方法探索历程

- 这是历史观察性数据。未测量混杂、治疗时点、治疗异质性以及删失假设均限制了结果解释。分析以手术为时间零点，而化疗以一个记录的指示变量表示；该分析未确立与时间零点对齐的治疗分配，也未排除不死时间偏倚（immortal-time bias）。
- 要作因果解释，需要有充分依据的一致性、可交换性／无未测量混杂、目标人群内的正值性，以及恰当的删失假设。一致性是一项假设，并非总会自动成立。
- 本分析忠实复现了题目给定的 RFS 删失约定；该约定是否适用，取决于底层的随访过程。
- 在已验证的运行环境中，bootstrap 执行产生了 **23 条倾向评分分离警告**。这些警告已记录，并未被悄悄丢弃。导出的五年／十年分组汇总包含 500 次 bootstrap 的贡献，但这并不能消除统计推断潜在的不稳定性。
- 汇报附录讨论了探索性的 Cox 比例风险诊断和极端 ATE-IPTW 权重。这些分析**未在最终的 `survival.R` 中实现**，本文也不将其声称为已复现的结果。它们用于说明方法探索过程，而非第二个最终模型。
- 公开说明文字澄清了百分点和因果假设，但并非对每张幻灯片的逐字重发。HTML 播放器以字形路径 SVG 和提取原文 HTML 逐页展示原 PDF 第2～28页；不分发原 PDF/PPTX 文件及隐藏演讲备注。后续页源自课程的内容、文献及所属信息按原稿保留。

## 参考文献

- R `survival` 软件包，[Rotterdam 数据集文档](https://stat.ethz.ch/R-manual/R-devel/library/survival/html/rotterdam.html)。
- Royston P, Altman DG. External validation of a Cox prognostic model: principles and methods. *BMC Med Res Methodol*. 2013;13:33. https://doi.org/10.1186/1471-2288-13-33
- Elkin EB et al. Adjuvant chemotherapy and survival in older women with hormone receptor-negative breast cancer. *J Clin Oncol*. 2006;24:2757–2764. https://doi.org/10.1200/JCO.2005.03.6053
- Du XL et al. Effectiveness of adjuvant chemotherapy for node-positive operable breast cancer in older women. *J Gerontol A*. 2005;60:1137–1144. https://doi.org/10.1093/gerona/60.9.1137
- Li F, Morgan KL, Zaslavsky AM. Balancing covariates via propensity score weighting. *JASA*. 2018;113:390–400. https://doi.org/10.1080/01621459.2016.1260466
- Li F, Thomas LE, Li F. Addressing extreme propensity scores via the overlap weights. *Am J Epidemiol*. 2019;188:250–257. https://doi.org/10.1093/aje/kwy201
- Denz R, Klaaßen-Mielke R, Timmesfeld N. A comparison of different methods to adjust survival curves for confounders. *Stat Med*. 2023;42:1461–1479. https://doi.org/10.1002/sim.9681
- Royston P, Parmar MKB. Restricted mean survival time: an alternative to the hazard ratio. *BMC Med Res Methodol*. 2013;13:152. https://doi.org/10.1186/1471-2288-13-152
- Hernán MA, Robins JM. [Causal Inference: What If](https://www.hsph.harvard.edu/miguel-hernan/causal-inference-book/)。

本材料供学习参考与批判性检视，不供直接抄入考试提交内容。代码和文档的权利由各自作者保留；不对第三方数据集或参考文献授予一揽子许可。
