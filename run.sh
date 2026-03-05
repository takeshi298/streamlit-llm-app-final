#!/bin/bash

# ECサイト商品レコメンドチャットボット - 起動スクリプト

echo "=========================================="
echo "🛍️  チャットボットを起動中..."
echo "=========================================="
echo ""

# 仮想環境を有効化
source .venv/bin/activate

# Streamlitアプリを起動
streamlit run ecommerce_chatbot.py
