from app.models import UserProfile
from app.recommender import rank_recipes, suggest_substitutions


def test_rank_recipes_generates_recipe_from_input() -> None:
    user = UserProfile(weight_kg=60.0, goal="減量")
    items = ["鶏むね肉", "卵", "ブロッコリー"]
    ranked = rank_recipes(items, user)

    assert len(ranked) == 1
    recipe, score = ranked[0]
    assert recipe.ingredients == items
    assert recipe.name.startswith("鶏むね肉")
    assert score >= 0


def test_substitutions_for_input_items() -> None:
    user = UserProfile(weight_kg=60.0, goal="増量")
    recipe = rank_recipes(["牛肉"], user)[0][0]
    subs = suggest_substitutions(["牛肉"], recipe)

    assert isinstance(subs, list)
    assert any("牛肉" in item for item in subs)
