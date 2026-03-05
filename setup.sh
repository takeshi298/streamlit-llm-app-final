#!/bin/bash

# ECサイト商品レコメンドチャットボット - セットアップスクリプト

echo "=========================================="
echo "🛍️  セットアップを開始します"
echo "=========================================="

# 仮想環境の確認
if [ ! -d ".venv" ]; then
    echo "📦 仮想環境を作成中..."
    python3 -m venv .venv
fi

# 仮想環境を有効化
source .venv/bin/activate

# パッケージをインストール
echo "📚 パッケージをインストール中..."
pip install -q -r requirements.txt

echo ""
echo "=========================================="
echo "✅ セットアップが完了しました!"
echo "=========================================="
echo ""
echo "🚀 チャットボットを起動するには:"
echo "   streamlit run ecommerce_chatbot.py"
echo ""
