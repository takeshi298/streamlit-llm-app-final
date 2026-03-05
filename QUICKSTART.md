# 🛍️ ECサイト商品レコメンドチャットボット - クイックスタート

## セットアップ

### 自動セットアップ（推奨）
```bash
bash setup.sh
```

### 手動セットアップ
```bash
# 仮想環境を作成
python3 -m venv .venv

# 仮想環境を有効化
source .venv/bin/activate  # macOS/Linux
# または
.venv\Scripts\activate  # Windows

# パッケージをインストール
pip install -r requirements.txt
```

---

## 実行

### 自動実行（推奨）
```bash
bash run.sh
```

### 手動実行
```bash
source .venv/bin/activate
streamlit run ecommerce_chatbot.py
```

ブラウザが自動的に開き、チャットボットが表示されます。

---

## テスト

### 自動テスト実行（推奨）
```bash
bash test.sh
```

### 手動テスト実行
```bash
source .venv/bin/activate
pytest tests/test_ecommerce.py -v
```

---

## 使用例

チャットボットを起動後、以下のような入力をしてみてください：

### 例1: 防水性の高い商品を探す
```
防水で軽いジャケット
```
→ **予想される結果**: 防水ワークジャケット (¥8,900)

### 例2: 予算を指定
```
予算3000円以下のスポーツ用品
```
→ **予想される結果**: フィットネスヨガマット (¥2,200)

### 例3: 特定のカテゴリを探す
```
在宅勤務用の快適なグッズ
```
→ **予想される結果**: ワイヤレス充電パッド、LED電球など

---

## ファイル構成

```
.
├── ecommerce_chatbot.py           # メインアプリケーション
├── app/
│   ├── ecommerce_data.py          # 商品データベース
│   ├── product_recommender.py     # レコメンドロジック
│   └── ecommerce_llm_service.py   # LLM連携
├── tests/
│   └── test_ecommerce.py          # ユニットテスト
├── setup.sh                        # セットアップスクリプト
├── run.sh                          # 起動スクリプト
├── test.sh                         # テストスクリプト
├── requirements.txt                # 依存パッケージ
└── README.md                       # プロジェクト説明
```

---

## トラブルシューティング

### Issue: `streamlit: command not found`
**解決策**: 仮想環境が有効化されていません
```bash
source .venv/bin/activate
```

### Issue: `ModuleNotFoundError: No module named 'streamlit'`
**解決策**: パッケージがインストールされていません
```bash
pip install -r requirements.txt
```

### Issue: `OPENAI_API_KEY not set`
**解決策**: LLMなしでも動作します（簡易解析が自動的に使用されます）
```bash
# LLMを使いたい場合は環境変数を設定
export OPENAI_API_KEY=sk-...
```

---

## パフォーマンス情報

| メトリック | 値 |
|-----------|-----|
| 処理時間 | <1秒 |
| 商品数 | 21個 |
| テスト数 | 14個 |
| テスト成功率 | 100% ✅ |

---

## 今後の改善予定

- [ ] 商品DBをPostgreSQLに移行
- [ ] ベクトル検索の導入
- [ ] ユーザー行動分析機能
- [ ] パーソナライズレコメンド
- [ ] A/Bテスト機能

---

## サポート

問題が発生した場合は、以下のコマンドで動作確認できます：

```bash
# 全機能の動作確認
python << 'EOF'
from app.ecommerce_data import get_all_products
from app.product_recommender import recommend_products
from app.ecommerce_llm_service import parse_user_needs_with_llm

products = get_all_products()
print(f"✅ {len(products)}個の商品がロードされました")

needs = parse_user_needs_with_llm("防水で軽い商品")
print(f"✅ ニーズ解析: {needs['keywords']}")

recs = recommend_products("防水で軽い商品", top_n=3)
print(f"✅ {len(recs)}個の商品をレコメンド")
EOF
```

---

**Happy Shopping! 🎉**
