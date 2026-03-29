# トークン最適化監査レポート

作成日: 2026-03-28

---

## 1. 常時読み込まれるもの（全会話で発生するコスト）

| ファイル | サイズ | 削減可否 |
|---------|--------|---------|
| `CLAUDE.md`（ルート） | 3.9 KB | 大幅削減は禁止 |
| `.claude/agents/` 全9ファイル | 36 KB | → 軽量モードでは不要なものを読まない |
| スキルメタデータ（名前のみ） | 小さい | そのまま |

**ベースライン推定: 40〜50 KB / 会話**

---

## 2. 必要時だけ読むべきもの（現状は混入している）

### ES執筆時に過剰ロードされているもの
| ファイル | サイズ | 問題点 |
|---------|--------|-------|
| `ES/components/best_answers.md` | 27 KB | 毎回全文を読んでいる |
| `ES/components/motivation.md` | 39 KB | 志望動機設問以外では不要 |
| `ES/components/gakuchika.md` | 38 KB | ガクチカ設問以外では不要 |
| `ES/components/self_pr.md` | 27 KB | 自己PR設問以外では不要 |
| `company-info/*/research_brief.md` | 5〜20 KB | briefが薄い場合は詳細調査ファイルも読む |

**ES1本生成時の想定ロード量: 60〜110 KB**

### 面接準備時に過剰ロードされているもの
| ファイル | サイズ | 問題点 |
|---------|--------|-------|
| `interview-prep` SKILL.md | 9 KB | 面接以外で読まれることがある |
| interview 系 skill 群（7ファイル） | 35 KB | ES執筆時に混入することがある |
| `stages/final-interview-depth-mode` | 3 KB | 1次面接では不要 |

---

## 3. 圧縮すべきもの

| ファイル | 現状サイズ | 対処 |
|---------|---------|------|
| `company-info/*/research_brief.md` | 5〜20 KB | 既に brief 形式だが、長いものは ES/面接 向けに圧縮 |
| `ES/components/*.md` | 27〜39 KB | 設問タイプ別に分割、呼ばれた設問タイプのみロード |
| `company-researcher` SKILL.md | 463 lines | 実調査フェーズのみ読む |
| `interview-prep` SKILL.md | 398 lines | 面接フェーズのみ読む |

---

## 4. 同時起動を避けるべき agent の組み合わせ

| 組み合わせ | 理由 |
|-----------|------|
| 全5 reviewer の同時起動 | es-review-protocol が毎回全て呼ぶ → 段階起動に変更 |
| company-fit + role-fit + consistency の草案段階での起動 | 草案では不要。仕上げ段階のみ |
| skeptical-interviewer の ES草案段階での起動 | ES未確定段階では質問精度が低い |
| research-gap-reviewer のES執筆中の起動 | 調査フェーズと執筆フェーズを混在させない |

---

## 5. script 化できる hook（Claude不要）

以下は文字列マッチ・数値比較で判定可能なので script に寄せられる:

| チェック項目 | 現状 | 改善後 |
|------------|------|-------|
| 文字数チェック（超過・不足） | 手動 or agent | `es_checker.py` に追加 |
| 禁止表現チェック（「思います」等） | 手動 | `es_checker.py` に実装済み |
| 企業名表記ゆれ | なし | script 追加 |
| 設問未回答警告 | なし | script 追加 |
| 重複表現検出（同一文内） | なし | script 追加 |
| 技術用語過多警告（閾値判定） | なし | script 追加 |
| 抽象語過多警告 | なし | script 追加 |
| 数字不足警告 | なし | script 追加 |
| research_brief 必須項目の存在確認 | なし | `research_checker.py` に追加 |

---

## 6. quality gate として残すべき reviewer

軽量化後も以下は省略しない:

| reviewer | 残す理由 |
|---------|---------|
| `question-fit-reviewer` | 設問ズレは最も致命的な欠陥 |
| `readability-reviewer` | 人事通過に直結する |
| `company-fit-reviewer` | 汎用ES排除のため |
| `role-fit-reviewer` | 職種適合は落とされる主因 |
| `consistency-overlap-reviewer` | 3問以上で重複リスク大 |
| `skeptical-interviewer` | 面接前の必須確認 |

省略できる reviewer:
- `editor-refiner`: 時間がない場合は自己修正で代替可

---

## 7. 軽量化の優先順位

### 優先度 HIGH
1. reviewer の段階起動（毎回全部回すのをやめる）
2. ES執筆時の components の設問タイプ別ロード
3. session 分割運用の標準化（調査→執筆→レビュー→面接を別会話に）
4. command hook / script の有効化（文字数・禁止表現を自動チェック）

### 優先度 MEDIUM
5. research_brief を一次参照に統一（詳細調査ファイルを直接読まない）
6. skill selector で面接系 skill をES執筆時に除外
7. 軽量モデルで十分な reviewer の分類

### 優先度 LOW
8. components ファイルの設問タイプ別分割
9. ES/components/best_answers.md の要約版作成
