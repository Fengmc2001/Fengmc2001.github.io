# 最初に読むファイル / ポートフォリオ更新ルール

このディレクトリは、生物統計学・生存時間解析・因果推論に関する学習内容を、**学習段階ごとに整理して蓄積するためのポートフォリオ**である。大学院出願時の自己推薦資料としても読めるように、単なるコード置き場ではなく、**学んだ概念・コード・解釈・次に学ぶべき内容**を一体として残すことを目的とする。

## 基本方針

1. 各学習段階は `stages/` 以下に 1 つのフォルダとして保存する。  
2. 各フォルダ名は `stage-XX_日付_主題` の形式にする。  
3. 各段階フォルダには、原則として次の内容を含める。  
   - `README.md`：その段階で学んだ内容の要約
   - `scripts/`：再現可能なコード
   - `docs/`：補足説明、出力例、自己推薦書用の文章案など
   - `figures/`：必要に応じて図や概念図
4. 説明文は**日本語を優先**する。英語は必要なときのみ補助的に付ける。  
5. 各段階の `README.md` には、少なくとも次の 5 項目を入れる。  
   - 何を学んだか
   - どのコードで確認できるか
   - どの点が方法論的に重要か
   - 何を誤解しやすいか
   - 次に学ぶ内容と目標

## ChatGPT に今後このリポジトリ更新を依頼するときのルール

今後 ChatGPT にこのリポジトリの更新を依頼する際は、以下の形式で追記・整理すること。

- 新しい学習内容は、既存ファイルを雑に上書きせず、まず `stages/` の新しい段階フォルダとして追加すること。  
- その段階の説明は、大学院出願資料として読まれても不自然でないように、**簡潔だが方法論的に正確な日本語**でまとめること。  
- コードだけでなく、**そのコードが何のバイアスや推定上の問題を扱っているのか**を必ず明記すること。  
- 各段階の最後に、**次の学習内容と目標**を箇条書きで入れること。  
- 因果推論や propensity score を扱うときは、可能であれば **SMD などの balance 診断**も含めること。  
- `IPW 後の SMD は 0 でなければならない` のような強すぎる断定は避け、**0 に近づくことが望ましく、実務上は |SMD| < 0.1 などを目安にする**という形で記述すること。  
- time-zero、immortal time bias、landmark analysis、time-dependent treatment coding を扱うときは、**各方法が何を解決し、何を新たに引き起こすか**まで整理すること。  
- time-dependent Cox model を扱う場合でも、**time-varying confounding が残る場合には追加の方法（例：MSM など）が必要になる**ことに触れること。  

## 推奨ディレクトリ構造

```text
biostatistics-portfolio/
├── 00_READ_ME_FIRST_JA.md
├── README.md
├── requirements.txt
├── scripts/
├── docs/
├── figures/
└── stages/
    ├── README.md
    └── stage-XX_date_topic/
        ├── README.md
        ├── scripts/
        ├── docs/
        └── figures/
```

## このポートフォリオの読み方

- まず `00_READ_ME_FIRST_JA.md` を読む  
- 次に `stages/README.md` で学習段階の一覧を見る  
- その後、各段階の `README.md` と `scripts/` を確認する  

## 現時点での学習の方向性

現時点では、主として次の流れで学習を整理していく。

1. Propensity score と IPW の基礎  
2. SMD による balance 診断  
3. Time-zero 問題（naive, landmark, time-dependent treatment）  
4. time-varying confounding と marginal structural model  
5. doubly robust estimation  
6. 実世界データにおける survival analysis と causal inference の接続
