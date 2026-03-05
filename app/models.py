from dataclasses import dataclass
from typing import List


@dataclass
class UserProfile:
    weight_kg: float
    goal: str  # "減量" | "維持" | "増量"


@dataclass
class Recipe:
    name: str
    ingredients: List[str]
    calories: int
    protein_g: int
    fat_g: int
    carbs_g: int
    tags: List[str]
    steps: List[str]


@dataclass
class RecommendationResult:
    recipe: Recipe
    reason: str
    substitutions: List[str]
    weekly_plan: List[str]
