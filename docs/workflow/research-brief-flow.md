# research_brief 中心フロー

企業調査の結果を brief に圧縮し、ES/面接へ渡す標準フロー。

**原則: ES執筆・面接準備の一次参照は research_brief.md のみ。詳細調査ファイルを直接読まない。**

---

## フロー全体図

```
[詳細調査セッション]  →  [brief 整形セッション]  →  [ES/面接セッション]
         ↓                        ↓                         ↓
  company-researcher        research_brief.md         es-writer
  WebSearch結果            （一次参照として確定）       interview-prep
  生ファイル保存
```

---

## Step 1: 詳細調査（セッションA）

```
「[企業名]の企業調査をして。research_brief.md に圧縮して保存して」
```

- company-researcher スキルが起動
- WebSearch + WebFetch で情報収集
- **成果物**: `company-info/<企業名>/research_brief.md`
- この段階では ES を書かない

---

## Step 2: brief の品質確認（必要なら）

```
python tools/checks/research_checker.py <企業名>
```

または:

```
「[企業名]の research_brief の不足論点を確認して」
→ research-gap-reviewer が参照
```

不足があれば追加調査:

```
「[企業名]の競合比較の論点が薄い。補強して」
```

---

## Step 3: ES執筆での brief 参照

```
「[企業名]のESを書いて」→ es-writer が起動
```

es-writer は以下のみ参照する:
- `company-info/<企業名>/research_brief.md` ← **必ずこちら**
- `ES/素材/INDEX.md`（エピソード確認）
- `ES/部品/best_answers.md`（コアテンプレ）

⚠️ 詳細調査ファイル（research.md 等）は直接参照しない

---

## Step 4: 面接準備での brief 参照

```
「[企業名]の1次面接の準備をして」→ interview-prep が起動
```

interview-prep は以下のみ参照する:
- `company-info/<企業名>/research_brief.md` ← **必ずこちら**
- 対応する interview 系 skill（stage に応じた最小セット）

---

## brief を中間に挟む理由

| 直接参照（廃止） | brief 経由（推奨） |
|--------------|----------------|
| 詳細調査ファイル全文読む（10〜30 KB） | brief のみ読む（3〜7 KB） |
| 不必要な調査内容もロード | ES/面接に必要な情報だけ |
| 調査→執筆が1セッションに混在 | セッション間の引継ぎが明確 |
| brief の質が担保されない | brief 更新時にのみ詳細を読む |

---

## brief の命名規則

```
company-info/<企業名>/research_brief.md   ← 常にこのファイル名
```

企業名はディレクトリ名と一致させる:
```
company-info/ニッセイアセットマネジメント/research_brief.md
company-info/三菱UFJ銀行/research_brief.md
company-info/JCB/research_brief.md
```

---

## 既存調査から brief を作る

調査ファイルはあるが brief がない場合:

```
「company-info/[企業名]/ 以下の調査資料を読んで、
 research_brief テンプレートに従って brief を作って保存して」
```

テンプレート: `docs/schemas/research-brief-template.md`
