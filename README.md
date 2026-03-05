# AI レコメンドシステム

## 🛍️ ECサイト商品レコメンドチャットボット（NEW）

顧客が「こんな商品が欲しい」と入力すると、ECサイト内の大量の商品の中からいくつか候補をレコメンドしてくれるチャットボットです。

### 使用方法

```bash
streamlit run ecommerce_chatbot.py
```

#### 主な機能
- **自然言語ニーズ解析**: LLMが顧客の要望から詳細なニーズを抽出（APIなしでも簡易解析可能）
- **インテリジェント検索**: キーワード、予算、カテゴリに基づいて商品を検索
- **関連度スコアリング**: 複数の要因（キーワードマッチ、予算、レーティング、在庫）から最適な商品を算出
- **カスタマイズ可能なフィルタ**: 予算・カテゴリの絞り込みが可能
- **推奨理由の表示**: なぜその商品がおすすめなのか、詳しく説明
- **検索履歴**: 過去の検索結果を保存・参照可能

#### 使用例
- 「在宅勤務用の快適な椅子が欲しい」
- 「防水で軽いジャケット」
- 「予算3000円以下のギフト」
- 「LED照明で省電力の製品」

---

# 🍽️ 冷蔵庫×健康状態レコメンドAI

冷蔵庫にある食材と健康目標（減量/維持/増量）を入力すると、
入力内容に応じてレシピを生成し、栄養バランス解説・食材代替案・週間プランを表示する生成AIアプリです。

### 使用方法

```bash
streamlit run main.py
```

## 実装ステップ

1. **要件整理**
   - 入力: 冷蔵庫食材、体重、目標
   - 出力: レシピ提案、栄養バランス説明、代替提案、週間プラン
2. **データモデル作成**
   - `UserProfile`, `Recipe` を `app/models.py` に定義
3. **推薦ロジック実装**
   - 固定レシピDBを使わず、入力食材と目標からレシピを動的生成
   - 推定栄養値と目標の差分で適合スコアを算出
4. **LLM機能実装**
   - 栄養バランス説明（OpenAI API、未設定時はフォールバック文）
   - 週間プラン生成
5. **UI実装（Streamlit）**
   - フォーム入力と結果表示を `main.py` に実装
6. **テスト追加**
   - 推薦・代替提案の単体テストを `tests/test_recommender.py` に追加

## ファイル構成

### ECサイト商品レコメンドシステム
- `ecommerce_chatbot.py`: Streamlit UI（メインチャットボット）
- `app/ecommerce_data.py`: 商品データベース（20+ 商品を含む）
- `app/product_recommender.py`: 商品検索・レコメンドロジック
- `app/ecommerce_llm_service.py`: LLMベースのニーズ解析・フォーマット処理
- `tests/test_ecommerce.py`: 単体テスト（14テスト）

### 冷蔵庫×健康状態レコメンドシステム
- `main.py`: Streamlit UI（料理レコメンド）
- `app/models.py`: データモデル（UserProfile, Recipe）
- `app/recommender.py`: 入力ベースのレシピ生成ロジック、代替提案
- `app/llm_service.py`: LLM連携（栄養説明、週間プラン）
- `tests/test_recommender.py`: 単体テスト
- `requirements.txt`: 依存ライブラリ

## セットアップ

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## 実行

```bash
streamlit run main.py
```

## 任意: OpenAI API有効化

```bash
export OPENAI_API_KEY="あなたのAPIキー"
streamlit run main.py
```

APIキー未設定でもフォールバック文で動作します。

## テスト

```bash
pytest -q
```
