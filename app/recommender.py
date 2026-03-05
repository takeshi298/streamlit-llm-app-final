from __future__ import annotations

from typing import List, Tuple

from app.models import Recipe, UserProfile


GOAL_CONFIG = {
    "減量": {"target_cal": 500, "target_protein": 35},
    "維持": {"target_cal": 600, "target_protein": 30},
    "増量": {"target_cal": 750, "target_protein": 30},
}

INGREDIENT_NUTRITION = {
    "鶏むね肉": {"cal": 165, "protein": 31, "fat": 4, "carbs": 0},
    "鶏もも肉": {"cal": 200, "protein": 20, "fat": 14, "carbs": 0},
    "牛肉": {"cal": 250, "protein": 26, "fat": 17, "carbs": 0},
    "豚肉": {"cal": 230, "protein": 22, "fat": 16, "carbs": 0},
    "鮭": {"cal": 210, "protein": 22, "fat": 14, "carbs": 0},
    "卵": {"cal": 80, "protein": 6, "fat": 5, "carbs": 0},
    "豆腐": {"cal": 90, "protein": 7, "fat": 5, "carbs": 2},
    "米": {"cal": 240, "protein": 4, "fat": 1, "carbs": 53},
    "玄米": {"cal": 220, "protein": 5, "fat": 2, "carbs": 46},
    "ブロッコリー": {"cal": 35, "protein": 3, "fat": 0, "carbs": 5},
    "ほうれん草": {"cal": 20, "protein": 2, "fat": 0, "carbs": 3},
}

DEFAULT_NUTRITION = {"cal": 60, "protein": 2, "fat": 2, "carbs": 8}


def _estimate_nutrition(ingredients: List[str]) -> tuple[int, int, int, int]:
    total_cal = 0
    total_protein = 0
    total_fat = 0
    total_carbs = 0

    for ingredient in ingredients:
        nutrition = INGREDIENT_NUTRITION.get(ingredient, DEFAULT_NUTRITION)
        total_cal += nutrition["cal"]
        total_protein += nutrition["protein"]
        total_fat += nutrition["fat"]
        total_carbs += nutrition["carbs"]

    return total_cal, total_protein, total_fat, total_carbs


def _nutrition_penalty(recipe: Recipe, goal: str) -> float:
    config = GOAL_CONFIG.get(goal, GOAL_CONFIG["維持"])
    cal_diff = abs(recipe.calories - config["target_cal"])
    protein_diff = max(0, config["target_protein"] - recipe.protein_g)
    return cal_diff * 0.02 + protein_diff * 0.8


def _build_recipe_name(ingredients: List[str], goal: str) -> str:
    top_items = ingredients[:2]
    if not top_items:
        return f"{goal}向けバランスプレート"
    if len(top_items) == 1:
        return f"{top_items[0]}の{goal}向けアレンジ"
    return f"{top_items[0]}と{top_items[1]}の{goal}向けアレンジ"


def _build_steps(ingredients: List[str], goal: str) -> List[str]:
    ingredient_text = "、".join(ingredients)
    return [
        f"{ingredient_text}を食べやすい大きさに切り、火の通りをそろえる",
        "たんぱく質食材から先に加熱し、野菜を加えて食感を残す",
        f"{goal}を意識して味付けを調整し、全体をさっと仕上げる",
    ]


def generate_recipe_from_input(fridge_items: List[str], user: UserProfile) -> Recipe:
    ingredients = [item for item in fridge_items if item][:6]
    calories, protein, fat, carbs = _estimate_nutrition(ingredients)

    return Recipe(
        name=_build_recipe_name(ingredients, user.goal),
        ingredients=ingredients,
        calories=calories,
        protein_g=protein,
        fat_g=fat,
        carbs_g=carbs,
        tags=["入力生成", f"{user.goal}向け"],
        steps=_build_steps(ingredients, user.goal),
    )


def rank_recipes(fridge_items: List[str], user: UserProfile) -> List[Tuple[Recipe, float]]:
    generated = generate_recipe_from_input(fridge_items, user)
    penalty = _nutrition_penalty(generated, user.goal)
    score = max(0.0, 100.0 - penalty * 10)
    return [(generated, score)]


def suggest_substitutions(fridge_items: List[str], recipe: Recipe) -> List[str]:
    subs = {
        "鶏むね肉": ["鶏もも肉(脂質注意)", "豆腐"],
        "鮭": ["サバ", "鶏むね肉"],
        "牛肉": ["豚こま", "厚揚げ"],
        "豚肉": ["鶏むね肉", "木綿豆腐"],
        "米": ["オートミール", "玄米"],
        "ブロッコリー": ["ほうれん草", "小松菜"],
        "卵": ["納豆", "豆腐"],
    }
    result: List[str] = []

    for ingredient in fridge_items:
        alternatives = subs.get(ingredient)
        if alternatives:
            result.append(f"{ingredient} → {', '.join(alternatives)}")

    return result
