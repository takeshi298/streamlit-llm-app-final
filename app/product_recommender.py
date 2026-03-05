"""ECサイト商品レコメンドロジック"""
from __future__ import annotations

from typing import List, Tuple
from app.ecommerce_data import Product, get_all_products


def calculate_relevance_score(
    product: Product,
    keywords: List[str],
    budget_min: int = 0,
    budget_max: int = 50000,
    preferred_categories: List[str] | None = None,
) -> float:
    """
    商品の関連度スコアを計算
    
    Args:
        product: 評価対象の商品
        keywords: ユーザーが指定したキーワード
        budget_min: 最小予算
        budget_max: 最大予算
        preferred_categories: 好みのカテゴリ
    
    Returns:
        0-100の関連度スコア
    """
    score = 0.0

    # キーワードマッチング（最大50点）
    matched_keywords = 0
    for keyword in keywords:
        keyword_lower = keyword.lower()
        if (
            keyword_lower in product.name.lower()
            or keyword_lower in product.description.lower()
            or any(keyword_lower in feat.lower() for feat in product.features)
            or any(keyword_lower in kw.lower() for kw in product.keywords)
        ):
            matched_keywords += 1

    if keywords:
        keyword_score = (matched_keywords / len(keywords)) * 50
        score += keyword_score

    # 予算スコア（最大30点）
    if budget_min <= product.price <= budget_max:
        # 予算内は満点
        budget_score = 30
    else:
        # 予算外は減点
        if product.price < budget_min:
            budget_score = max(0, 30 - (budget_min - product.price) / 1000)
        else:
            budget_score = max(0, 30 - (product.price - budget_max) / 1000)
    score += budget_score

    # カテゴリボーナス（最大15点）
    if preferred_categories and product.category in preferred_categories:
        score += 15

    # 在庫ボーナス（最大3点）
    if product.stock > 50:
        score += 3
    elif product.stock > 0:
        score += 1.5

    # レーティングボーナス（最大2点）
    score += (product.rating / 5.0) * 2

    return min(100.0, score)


def recommend_products(
    user_needs: str,
    budget_min: int = 0,
    budget_max: int = 50000,
    preferred_categories: List[str] | None = None,
    top_n: int = 5,
) -> List[Tuple[Product, float, str]]:
    """
    ユーザーのニーズに基づいて商品をレコメンド
    
    Args:
        user_needs: ユーザーのニーズ（テキスト）
        budget_min: 最小予算
        budget_max: 最大予算
        preferred_categories: 好みのカテゴリ
        top_n: 返す商品数
    
    Returns:
        (商品, スコア, 理由)のリスト
    """
    # ニーズからキーワードを抽出（簡易版）
    keywords = user_needs.lower().split()
    keywords = [kw for kw in keywords if len(kw) > 2]

    products = get_all_products()
    scored_products = []

    for product in products:
        score = calculate_relevance_score(
            product,
            keywords,
            budget_min,
            budget_max,
            preferred_categories,
        )
        scored_products.append((product, score))

    # スコアでソート
    scored_products.sort(key=lambda x: x[1], reverse=True)

    # 理由を生成
    result = []
    for product, score in scored_products[:top_n]:
        reason = _generate_recommendation_reason(product, user_needs, keywords)
        result.append((product, score, reason))

    return result


def _generate_recommendation_reason(
    product: Product,
    user_needs: str,
    keywords: List[str],
) -> str:
    """推奨理由を生成"""
    reasons = []

    # キーワードマッチの理由
    matched_features = []
    for keyword in keywords:
        keyword_lower = keyword.lower()
        for feature in product.features:
            if keyword_lower in feature.lower():
                matched_features.append(feature)

    if matched_features:
        reasons.append(f"【特徴】{', '.join(matched_features)}")

    # レーティングの理由
    if product.rating >= 4.5:
        reasons.append("【評価】高い満足度でおすすめ")
    elif product.rating >= 4.0:
        reasons.append("【評価】多くのユーザーに支持されています")

    # 在庫の理由
    if product.stock > 100:
        reasons.append("【在庫】十分あり、すぐに配送可能")

    # 価格の理由
    reasons.append(f"【価格】¥{product.price:,}")

    return " ".join(reasons)


def search_products(query: str, limit: int = 10) -> List[Tuple[Product, float]]:
    """
    キーワードで商品を検索
    
    Args:
        query: 検索キーワード
        limit: 返す結果の最大数
    
    Returns:
        (商品, マッチスコア)のリスト
    """
    products = get_all_products()
    query_lower = query.lower()

    results = []
    for product in products:
        score = 0.0

        # 名前でのマッチ
        if query_lower in product.name.lower():
            score += 50

        # 説明でのマッチ
        if query_lower in product.description.lower():
            score += 30

        # キーワードでのマッチ
        for keyword in product.keywords:
            if query_lower in keyword.lower():
                score += 20
                break

        # 特性でのマッチ
        for feature in product.features:
            if query_lower in feature.lower():
                score += 10
                break

        if score > 0:
            results.append((product, score))

    results.sort(key=lambda x: x[1], reverse=True)
    return results[:limit]
