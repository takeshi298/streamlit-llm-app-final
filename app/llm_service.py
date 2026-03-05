from __future__ import annotations

import os
from typing import List


def build_weekly_plan(recipe_name: str, goal: str) -> List[str]:
    templates = {
        "減量": [
            f"月: {recipe_name} + サラダ",
            "火: たんぱく質中心のスープ",
            "水: 魚メイン定食",
            "木: 鶏むね肉の蒸し料理",
            "金: 豆腐ハンバーグ",
            "土: 低脂質パスタ",
            "日: 野菜多め鍋",
        ],
        "維持": [
            f"月: {recipe_name}",
            "火: 魚と玄米の定食",
            "水: 鶏肉と野菜炒め",
            "木: 豆類カレー",
            "金: 卵と野菜の丼",
            "土: 豚しゃぶサラダ",
            "日: 和食バランス定食",
        ],
        "増量": [
            f"月: {recipe_name} + ご飯大盛り",
            "火: 鶏肉とじゃがいものグラタン",
            "水: 牛肉丼 + 卵",
            "木: 魚とアボカドボウル",
            "金: パスタ + ツナ",
            "土: 親子丼",
            "日: 豚肉しょうが焼き定食",
        ],
    }
    return templates.get(goal, templates["維持"])


def explain_balance_with_llm(recipe_name: str, goal: str, protein_g: int, calories: int) -> str:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        return (
            f"このレシピは{goal}を意識した設計です。"
            f"1食あたり約{calories}kcal、たんぱく質{protein_g}gで、"
            "筋肉維持と満腹感の両立を狙います。"
        )

    try:
        from openai import OpenAI

        client = OpenAI(api_key=api_key)
        prompt = (
            "あなたは管理栄養士です。次の情報をもとに、"
            "日本語で80文字前後の栄養バランス解説を返してください。"
            f"レシピ: {recipe_name}, 目標: {goal}, カロリー: {calories}, たんぱく質: {protein_g}"
        )
        response = client.responses.create(
            model="gpt-4.1-mini",
            input=prompt,
            temperature=0.4,
        )
        text = response.output_text.strip()
        return text or "栄養バランス解説の生成に失敗しました。"
    except Exception:
        return (
            f"このレシピは{goal}向けで、{calories}kcal・たんぱく質{protein_g}gを確保。"
            "不足しがちな野菜を足すと、さらにバランスが良くなります。"
        )
