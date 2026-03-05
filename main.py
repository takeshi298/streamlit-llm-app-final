"""ECサイト商品レコメンドチャットボット"""
import streamlit as st
from app.product_recommender import recommend_products, search_products
from app.ecommerce_llm_service import parse_user_needs_with_llm, format_recommendation_response
from app.ecommerce_data import get_categories


def initialize_session_state():
    """セッション状態の初期化"""
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    if "recommendations" not in st.session_state:
        st.session_state.recommendations = []


def chatbot_main():
    """チャットボットメイン処理"""
    st.set_page_config(
        page_title="ECサイト商品レコメンドボット",
        page_icon="🛍️",
        layout="wide",
    )

    st.title("🛍️ ECサイト商品レコメンドチャットボット")
    st.caption("「こんな商品が欲しい」と入力すると、ぴったりな商品を見つけてくれます！")

    initialize_session_state()

    # サイドバーで詳細フィルタ
    with st.sidebar:
        st.header("🔍 検索フィルタ")

        # 予算フィルタ
        budget_range = st.slider(
            "予算（円）",
            min_value=0,
            max_value=50000,
            value=(0, 50000),
            step=500,
        )

        # カテゴリフィルタ
        categories = get_categories()
        selected_categories = st.multiselect(
            "カテゴリを選択",
            categories,
            default=categories,
        )

        # 結果数
        top_n = st.slider(
            "表示する商品数",
            min_value=1,
            max_value=10,
            value=5,
        )

        st.divider()
        st.info(
            "💡 ヒント: より詳しくニーズを説明すると、より正確な商品が見つかります！"
        )

    # メインチャットエリア
    col1, col2 = st.columns([3, 1])

    with col1:
        user_input = st.text_input(
            "欲しい商品について教えてください",
            placeholder="例: 在宅勤務用の快適な椅子が欲しい / 防水で軽いジャケット / 予算3000円以下のギフト",
            label_visibility="collapsed",
        )

    with col2:
        search_button = st.button("🔍 検索", use_container_width=True)

    # 検索処理
    if search_button and user_input:
        # ニーズを解析
        with st.spinner("ニーズを分析中..."):
            needs_analysis = parse_user_needs_with_llm(user_input)

        # 抽出されたニーズを表示
        with st.expander("📊 分析結果"):
            col1, col2, col3 = st.columns(3)
            with col1:
                st.write("**抽出キーワード:**")
                for kw in needs_analysis.get("keywords", []):
                    st.write(f"  • {kw}")

            with col2:
                st.write("**予算範囲:**")
                st.write(
                    f"¥{needs_analysis.get('budget_min', 0):,} ～ ¥{needs_analysis.get('budget_max', 50000):,}"
                )

            with col3:
                st.write("**対象カテゴリ:**")
                for cat in needs_analysis.get("categories", []):
                    st.write(f"  • {cat}")

        # 推奨商品を取得
        with st.spinner("おすすめ商品を探索中..."):
            recommendations = recommend_products(
                user_needs=user_input,
                budget_min=budget_range[0],
                budget_max=budget_range[1],
                preferred_categories=selected_categories if selected_categories else None,
                top_n=top_n,
            )

        # 結果を表示
        st.subheader("✨ おすすめ商品")

        if not recommendations:
            st.warning("条件に合う商品が見つかりませんでした。フィルタを調整してお試しください。")
        else:
            # タブで商品を表示
            tabs = st.tabs([f"商品 {i+1}" for i in range(len(recommendations))])

            for tab_idx, (product, score, reason) in enumerate(recommendations):
                with tabs[tab_idx]:
                    col1, col2 = st.columns([2, 1])

                    with col1:
                        st.write(format_recommendation_response(
                            product.name,
                            product.description,
                            product.price,
                            product.features,
                            product.rating,
                            reason,
                        ))

                    with col2:
                        st.metric("適合度", f"{score:.1f}%")
                        st.metric("在庫", f"{product.stock}個")
                        st.metric("カテゴリ", product.category)

                        if st.button(
                            "📧 詳細を見る",
                            key=f"details_{product.product_id}",
                            use_container_width=True,
                        ):
                            st.info(
                                f"商品ID: {product.product_id}\n\n"
                                f"キーワード: {', '.join(product.keywords)}"
                            )

            # チャット履歴に追加
            st.session_state.chat_history.append({
                "user_input": user_input,
                "needs_analysis": needs_analysis,
                "recommendations": recommendations,
            })

    # チャット履歴を表示
    if st.session_state.chat_history:
        st.divider()
        with st.expander("📜 検索履歴"):
            for idx, item in enumerate(reversed(st.session_state.chat_history), 1):
                st.write(f"**検索 {idx}:** {item['user_input']}")
                st.caption(f"条件: 予算 ¥{item['needs_analysis'].get('budget_min', 0):,} ～ ¥{item['needs_analysis'].get('budget_max', 50000):,}")


if __name__ == "__main__":
    chatbot_main()
