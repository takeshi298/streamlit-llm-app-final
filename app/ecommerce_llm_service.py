"""ECサイト用のLLMベースのニーズ解析"""
from __future__ import annotations

import os
import json
from typing import Optional


def parse_user_needs_with_llm(user_input: str) -> dict:
    """
    LLMを使ってユーザー入力からニーズを解析
    
    Args:
        user_input: ユーザーの入力テキスト
    
    Returns:
        {
            "keywords": [...],
            "budget_min": int,
            "budget_max": int,
            "categories": [...],
            "summary": str
        }
    """
    api_key = os.getenv("OPENAI_API_KEY")

    # APIキーがない場合、簡易的な解析を行う
    if not api_key:
        return _fallback_parse_needs(user_input)

    try:
        from openai import OpenAI

        client = OpenAI(api_key=api_key)

        prompt = f"""
以下のユーザー入力から、ECサイトの商品レコメンドに必要な情報を抽出してください。
JSON形式で返してください。

ユーザー入力: "{user_input}"

以下のフォーマットでJSON形式で返してください:
{{
    "keywords": ["キーワード1", "キーワード2", ...],
    "budget_min": 最小予算（円、数字のみ）,
    "budget_max": 最大予算（円、数字のみ。指定されていなければ50000）,
    "categories": ["カテゴリ1", "カテゴリ2", ...],
    "summary": "ユーザーのニーズの要約"
}}

注意:
- キーワードは3-5個程度に絞る
- 予算が明確に指定されていない場合は、文脈から判断する
- categories は以下から選択: ファッション, 家電, キッチン用品, スポーツ・アウトドア, 美容・ヘルスケア, 書籍・学習, その他
- 複数該当する場合は複数選択可能
"""

        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3,
            max_tokens=500,
        )

        response_text = response.choices[0].message.content
        
        # JSONを抽出（```で囲まれている場合がある）
        if "```json" in response_text:
            response_text = response_text.split("```json")[1].split("```")[0]
        elif "```" in response_text:
            response_text = response_text.split("```")[1].split("```")[0]

        parsed = json.loads(response_text.strip())
        return parsed

    except Exception as e:
        print(f"LLMエラー: {e}")
        return _fallback_parse_needs(user_input)


def _fallback_parse_needs(user_input: str) -> dict:
    """
    APIなしで簡易的にニーズを解析
    """
    input_lower = user_input.lower()

    keywords = []
    # 重要キーワードを抽出
    for word in user_input.split():
        if len(word) > 2:
            keywords.append(word)
    keywords = keywords[:5]

    # 予算を抽出
    budget_min = 0
    budget_max = 50000

    if "万" in user_input:
        try:
            import re

            match = re.search(r"(\d+)万", user_input)
            if match:
                budget_max = int(match.group(1)) * 10000
        except:
            pass

    if "千円" in user_input or "千" in user_input:
        try:
            import re

            match = re.search(r"(\d+)千", user_input)
            if match:
                budget_max = int(match.group(1)) * 1000
        except:
            pass

    # カテゴリを判定
    categories = []
    category_keywords = {
        "ファッション": ["服", "衣類", "ジャケット", "パンツ", "Tシャツ", "ウェア"],
        "家電": ["家電", "電子", "充電", "ライト", "扇風機", "LED"],
        "キッチン用品": ["キッチン", "調理", "鍋", "フライパン", "料理", "調理器具"],
        "スポーツ・アウトドア": ["スポーツ", "アウトドア", "ヨガ", "ジム", "ダンベル", "テント", "キャンプ"],
        "美容・ヘルスケア": ["美容", "健康", "マスク", "スキンケア", "歯", "アロマ"],
        "書籍・学習": ["本", "書籍", "学習", "学ぶ", "プログラミング", "英語"],
    }

    for category, category_kws in category_keywords.items():
        if any(kw in input_lower for kw in category_kws):
            categories.append(category)

    return {
        "keywords": keywords,
        "budget_min": budget_min,
        "budget_max": budget_max,
        "categories": categories if categories else ["その他"],
        "summary": user_input[:100],
    }


def format_recommendation_response(
    product_name: str,
    product_description: str,
    price: int,
    features: list[str],
    rating: float,
    reason: str,
) -> str:
    """
    レコメンド結果をテキスト形式でフォーマット
    """
    formatted = f"""
📦 **{product_name}**

💰 価格: ¥{price:,}
⭐ 評価: {rating}/5.0

📝 説明:
{product_description}

✨ 特徴:
{chr(10).join(f"  • {feature}" for feature in features)}

💡 推奨理由:
{reason}
"""
    return formatted.strip()
