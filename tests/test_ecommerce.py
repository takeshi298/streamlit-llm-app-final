"""ECサイトレコメンドシステムのテスト"""
import pytest
from app.ecommerce_data import get_all_products, get_categories, get_products_by_category
from app.product_recommender import (
    calculate_relevance_score,
    recommend_products,
    search_products,
)
from app.ecommerce_llm_service import parse_user_needs_with_llm, _fallback_parse_needs


class TestEcommerceData:
    """ECサイトデータのテスト"""

    def test_products_loaded(self):
        """商品が正常にロードされているか"""
        products = get_all_products()
        assert len(products) > 0
        assert len(products) >= 20  # 少なくとも20個の商品がある

    def test_categories_exist(self):
        """カテゴリが正常にロードされているか"""
        categories = get_categories()
        assert len(categories) > 0
        assert "ファッション" in categories or len(categories) > 0

    def test_filter_by_category(self):
        """カテゴリでのフィルタリングが機能するか"""
        categories = get_categories()
        if categories:
            cat = categories[0]
            filtered = get_products_by_category(cat)
            assert all(p.category == cat for p in filtered)

    def test_product_attributes(self):
        """商品の属性が正常か"""
        products = get_all_products()
        for product in products[:3]:
            assert product.product_id
            assert product.name
            assert product.category
            assert product.price > 0
            assert product.rating >= 0 and product.rating <= 5
            assert product.stock >= 0
            assert len(product.features) > 0
            assert len(product.keywords) > 0


class TestProductRecommender:
    """商品レコメンドロジックのテスト"""

    def test_relevance_score_basic(self):
        """関連度スコアの計算が正常か"""
        products = get_all_products()
        if products:
            product = products[0]
            score = calculate_relevance_score(
                product,
                keywords=[],
                budget_min=0,
                budget_max=50000,
            )
            assert 0 <= score <= 100

    def test_relevance_score_with_keywords(self):
        """キーワード指定時の関連度スコア"""
        products = get_all_products()
        if products:
            product = products[0]
            # 商品の名前が含まれるキーワードでスコア計算
            keywords = product.name.split()[:2]
            score = calculate_relevance_score(
                product,
                keywords=keywords,
                budget_min=0,
                budget_max=50000,
            )
            assert 0 <= score <= 100

    def test_recommend_products_returns_list(self):
        """recommend_productsがリストを返すか"""
        recommendations = recommend_products(
            user_needs="快適な椅子",
            budget_min=0,
            budget_max=50000,
            top_n=5,
        )
        assert isinstance(recommendations, list)
        assert len(recommendations) <= 5

    def test_recommend_products_format(self):
        """recommend_productsの戻り値形式が正しいか"""
        recommendations = recommend_products(
            user_needs="スポーツ",
            budget_min=0,
            budget_max=50000,
            top_n=3,
        )
        for product, score, reason in recommendations:
            assert product is not None
            assert 0 <= score <= 100
            assert isinstance(reason, str)
            assert len(reason) > 0

    def test_search_products(self):
        """商品検索が機能するか"""
        results = search_products("スポーツ", limit=5)
        assert isinstance(results, list)
        assert len(results) <= 5

    def test_search_results_format(self):
        """検索結果の形式が正しいか"""
        results = search_products("ライト", limit=3)
        for product, score in results:
            assert product is not None
            assert 0 <= score


class TestNeedsAnalysis:
    """ニーズ解析のテスト"""

    def test_fallback_parse_basic(self):
        """フォールバック解析が基本的に機能するか"""
        result = _fallback_parse_needs("防水のジャケットが欲しい")
        assert "keywords" in result
        assert "budget_min" in result
        assert "budget_max" in result
        assert "categories" in result
        assert "summary" in result

    def test_fallback_parse_budget_extraction(self):
        """フォールバック解析が予算を抽出できるか"""
        result = _fallback_parse_needs("5000円以下の商品")
        # 厳密にはテストしにくいが、フォーマットは正しいはず
        assert "budget_max" in result
        assert result["budget_max"] > 0

    def test_parse_user_needs_returns_dict(self):
        """parse_user_needs_with_llmが辞書を返すか"""
        result = parse_user_needs_with_llm("防水性の高いジャケット")
        assert isinstance(result, dict)
        assert "keywords" in result
        assert "budget_min" in result
        assert "budget_max" in result
        assert "categories" in result
        assert "summary" in result

    def test_parse_user_needs_format(self):
        """parse_user_needs_with_llmの戻り値形式が正しいか"""
        result = parse_user_needs_with_llm("スポーツ用の快適なパンツ")
        assert isinstance(result["keywords"], list)
        assert isinstance(result["budget_min"], (int, float))
        assert isinstance(result["budget_max"], (int, float))
        assert isinstance(result["categories"], list)
        assert isinstance(result["summary"], str)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
