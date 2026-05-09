---
title: "卒業研究：多言語マルチモーダル大規模言語モデルにおける機械的忘却の評価"
description: "卒業研究のテーマと、これまでに学んだ機械的忘却（machine unlearning）・多言語マルチモーダル評価に関する基礎知識のまとめ。"
pubDate: "2026-05-09"
heroImage: "/analysis.svg"
badge: "Trustworthy AI"
tags: ["machine-unlearning", "mllm", "trustworthy-ai", "multilingual"]
---

> 本ページは学習・調査の整理用ノートであり、進行中の実験設計や未公開の評価結果には触れない。今後随時更新する予定。

## 1. 概要

本研究のテーマは、**多言語マルチモーダル大規模言語モデル (Multilingual Multimodal Large Language Models, MLLMs) における機械的忘却 (machine unlearning) の評価** である。

- **期間：** 2026-04 –（進行中）
- **分野：** Trustworthy AI / Multimodal Machine Learning / Machine Unlearning
- **キーワード：** Machine Unlearning, MLLM, Multilingual Evaluation, Privacy, Reliability

近年、画像理解や Visual Question Answering (VQA) を行う大規模モデルが急速に発展している。一方で、こうしたモデルが個人情報・特定の人物画像・特定のエンティティに関する知識を保持し続けることへの懸念も高まっている。指定された知識を選択的に忘却させつつ、モデル全体の能力を可能な限り保持することは、Trustworthy AI における重要な課題のひとつである。

---

## 2. 研究の背景

### 2.1 機械的忘却 (Machine Unlearning)

学習済みモデルから、特定のデータ・概念・知識の影響を除去する手法群を指す。プライバシー保護、著作権、バイアス対策、安全性などの観点から重要性が増している。

### 2.2 マルチモーダル設定における困難

知識はテキスト表現だけでなく、視覚特徴と言語表現の対応関係 (visual–language association) として保持される可能性がある。そのため、テキスト的な指示に従って忘却が成功したように見えても、画像入力からの間接的な手がかりによって忘却対象が再生される場合がある。

### 2.3 多言語設定における追加の難しさ

モデルが複数言語で整合された場合、忘却の効果が **プロンプトに用いる言語に依存する** 可能性がある。英語では忘却に成功しているように見えても、日本語や中国語のクエリでは元の知識が再露出する、という現象が起こり得る。

> 多言語マルチモーダルモデルが、視覚–テキスト的知識を **言語横断的に一貫して** 忘却できるかは自明ではない。

---

## 3. これまでに学んだこと

### 3.1 基礎概念

- 機械的忘却の定義と、データ削除・モデル編集との違い
- Approximate unlearning と exact unlearning の区別
- Membership Inference Attack に対する忘却の効果
- Catastrophic forgetting と意図的忘却の区別

### 3.2 マルチモーダル基盤

- Vision-Language Models のアーキテクチャ概要（visual encoder + language model）
- CLIP 系の表現学習が下流のマルチモーダル理解にどのように寄与するか
- VQA、image captioning、visual grounding といった代表的タスク

### 3.3 評価設定

- Identity-related knowledge、entity recognition、visual–textual association など、忘却対象の類型
- 忘却の有無を評価する指標（target accuracy 低下、retain accuracy 維持、refusal rate など）
- 多言語プロンプトを設計する際の表現揺れと意味的整合性

### 3.4 文献調査の方向性

- オープンソースの MLLM のうち、再現性のある評価基盤を提供しているもの
- Machine unlearning 専用のベンチマークおよび、その多言語拡張可能性
- Trustworthy AI 周辺の議論（モデルの prompt-based 改変、red-teaming、residual knowledge）

---

## 4. 関心のある評価軸

進行中の実験詳細は本ノートには含めず、概念レベルの評価軸のみ記載する。

### 4.1 忘却の有効性 (Forgetting effectiveness)

忘却対象に関する正答・記述が、適切に減少しているか。

### 4.2 言語横断的一貫性 (Cross-lingual consistency)

英語・日本語・中国語など複数言語で同一対象を尋ねた場合、忘却の挙動が一致しているか。

### 4.3 残存知識 (Residual knowledge)

直接的なクエリでは忘却に成功しているように見えても、言い換え、間接質問、画像のみ／テキストのみ、複数ターン会話などから再構成可能ではないか。

### 4.4 一般性能の保持 (Utility preservation)

忘却対象と無関係なタスク（一般的な VQA、無関係な画像説明、一般言語応答）への副作用が大きすぎないか。

これらは互いにトレードオフを伴うため、単一指標ではなく **多次元的な評価プロトコル** を意識している。

---

## 5. 技術環境

学習および調査の段階で使用している（あるいは使用予定の）ツールは以下の通り。

- Python / PyTorch
- Hugging Face Transformers
- オープンソースの MLLM
- Linux GPU サーバ、VS Code Remote SSH
- Git / GitHub
- Markdown / LaTeX によるドキュメント化

---

## 6. 今後の関心

進行中の実験結果や具体的な実装詳細は本ノートでは扱わない。一般的な方向性として関心を持っているのは以下である。

1. 多言語マルチモーダル機械的忘却に対する、より整理された評価プロトコル。
2. 既存の忘却手法が、言語間でどの程度一貫した挙動を示すかの実証的観察。
3. 忘却に成功したと判断された後にも残る、間接的に取り出せる知識の存在。
4. 忘却の有効性と一般性能維持のトレードオフ。
5. 再現可能な実験要約と、将来の拡張に耐える形での記述。

本研究はまだ進行中であり、現段階の主目的は **信頼できる実験設定を組み、評価指標を慎重に定義する** ことにある。
