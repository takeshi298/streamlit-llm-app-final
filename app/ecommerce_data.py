"""ECサイト商品データベース"""
from __future__ import annotations

from dataclasses import dataclass
from typing import List


@dataclass
class Product:
    """ECサイトの商品"""
    product_id: str
    name: str
    category: str
    price: int
    description: str
    features: List[str]
    keywords: List[str]
    rating: float
    stock: int


# サンプル商品データ（実際にはデータベースから取得）
PRODUCTS_DATABASE: List[Product] = [
    # ファッション
    Product(
        product_id="fashion_001",
        name="防水ワークジャケット",
        category="ファッション",
        price=8900,
        description="耐久性と防水性を兼ね備えたワークジャケット。屋外作業に最適。",
        features=["防水", "耐久性", "多機能ポケット", "軽量"],
        keywords=["ジャケット", "防水", "ワーク", "アウトドア"],
        rating=4.5,
        stock=45,
    ),
    Product(
        product_id="fashion_002",
        name="コットンTシャツセット（3枚組）",
        category="ファッション",
        price=2990,
        description="シンプルで快適な100%コットンTシャツ。3色セット。",
        features=["綿100%", "吸収性", "丈夫", "シンプルデザイン"],
        keywords=["Tシャツ", "コットン", "セット", "カジュアル"],
        rating=4.2,
        stock=150,
    ),
    Product(
        product_id="fashion_003",
        name="スポーツパンツ（メンズ）",
        category="ファッション",
        price=4500,
        description="通気性に優れたスポーツパンツ。ジムやランニングに最適。",
        features=["通気性", "ストレッチ", "速乾", "軽量"],
        keywords=["パンツ", "スポーツ", "メンズ", "ジム"],
        rating=4.6,
        stock=80,
    ),

    # 家電
    Product(
        product_id="electronics_001",
        name="ポータブル扇風機",
        category="家電",
        price=3500,
        description="USB充電式のコンパクト扇風機。オフィスや屋外で活躍。",
        features=["USB充電", "コンパクト", "静音", "3段階速度"],
        keywords=["扇風機", "USB", "ポータブル", "冷却"],
        rating=4.3,
        stock=120,
    ),
    Product(
        product_id="electronics_002",
        name="スマートLED電球",
        category="家電",
        price=1980,
        description="アプリ制御可能なLED電球。色温度調整対応。",
        features=["スマート制御", "色温度調整", "エネルギー効率", "長寿命"],
        keywords=["LED", "スマート", "電球", "照明"],
        rating=4.4,
        stock=200,
    ),
    Product(
        product_id="electronics_003",
        name="高速ワイヤレス充電パッド",
        category="家電",
        price=2280,
        description="15W高速充電対応。複数デバイス対応。",
        features=["15W高速充電", "安全認証済み", "滑り止め", "LED表示"],
        keywords=["充電", "ワイヤレス", "高速", "マルチデバイス"],
        rating=4.5,
        stock=90,
    ),

    # キッチン用品
    Product(
        product_id="kitchen_001",
        name="ステンレス鋼保温弁当箱",
        category="キッチン用品",
        price=3800,
        description="長時間保温できるステンレス製弁当箱。1段式で使いやすい。",
        features=["保温", "ステンレス鋼", "分解可能", "軽量"],
        keywords=["弁当箱", "保温", "ステンレス", "オフィス"],
        rating=4.4,
        stock=65,
    ),
    Product(
        product_id="kitchen_002",
        name="シリコン調理ツールセット（5点）",
        category="キッチン用品",
        price=1500,
        description="耐熱シリコン製の調理ツール5点セット。色分け可能。",
        features=["耐熱性", "シリコン素材", "カラフル", "収納ケース付き"],
        keywords=["調理ツール", "シリコン", "セット", "キッチン"],
        rating=4.1,
        stock=180,
    ),
    Product(
        product_id="kitchen_003",
        name="電動フードプロセッサー",
        category="キッチン用品",
        price=6500,
        description="野菜のみじん切り、練り、混ぜが簡単。調理時間短縮。",
        features=["電動", "複数機能", "大容量", "簡単操作"],
        keywords=["フードプロセッサー", "電動", "調理", "時短"],
        rating=4.7,
        stock=40,
    ),

    # スポーツ・アウトドア
    Product(
        product_id="sports_001",
        name="フィットネスヨガマット",
        category="スポーツ・アウトドア",
        price=2200,
        description="滑り止め加工のヨガマット。6mm厚で快適。",
        features=["滑り止め", "6mm厚", "軽量", "持ち運びやすい"],
        keywords=["ヨガ", "マット", "フィットネス", "運動"],
        rating=4.3,
        stock=110,
    ),
    Product(
        product_id="sports_002",
        name="アジャスタブルダンベル（5-20kg）",
        category="スポーツ・アウトドア",
        price=14800,
        description="5kgから20kgまで調整可能。スペース効率的。",
        features=["調整可能", "安全グリップ", "省スペース", "高品質"],
        keywords=["ダンベル", "ウェイト", "筋トレ", "自宅"],
        rating=4.8,
        stock=35,
    ),
    Product(
        product_id="sports_003",
        name="キャンプテント（2人用）",
        category="スポーツ・アウトドア",
        price=9800,
        description="軽量で組み立て簡単な2人用テント。防水加工済み。",
        features=["軽量", "防水", "簡単設営", "通気性"],
        keywords=["テント", "キャンプ", "アウトドア", "2人用"],
        rating=4.6,
        stock=25,
    ),

    # 美容・ヘルスケア
    Product(
        product_id="beauty_001",
        name="顔用フェイスマスク（10枚入り）",
        category="美容・ヘルスケア",
        price=1280,
        description="保湿成分配合の顔用マスク。毎日のスキンケアに。",
        features=["保湿", "安全成分", "使いやすい", "大容量"],
        keywords=["マスク", "スキンケア", "保湿", "美容"],
        rating=4.2,
        stock=250,
    ),
    Product(
        product_id="beauty_002",
        name="アロマテラピー用ディフューザー",
        category="美容・ヘルスケア",
        price=3200,
        description="超音波式アロマディフューザー。LED照明付き。",
        features=["超音波", "LED照明", "タイマー機能", "静音"],
        keywords=["アロマ", "ディフューザー", "リラックス", "香り"],
        rating=4.5,
        stock=75,
    ),
    Product(
        product_id="beauty_003",
        name="電動歯ブラシ",
        category="美容・ヘルスケア",
        price=4800,
        description="音波歯ブラシで歯垢をしっかり除去。防水設計。",
        features=["電動", "防水", "充電式", "複数モード"],
        keywords=["歯ブラシ", "電動", "口腔衛生", "健康"],
        rating=4.6,
        stock=95,
    ),

    # 書籍・学習
    Product(
        product_id="books_001",
        name="Python入門書",
        category="書籍・学習",
        price=3200,
        description="初心者向けのPython学習書。実践例豊富。",
        features=["初心者向け", "実践的", "カラー図解", "サンプルコード付き"],
        keywords=["Python", "プログラミング", "学習", "入門"],
        rating=4.4,
        stock=55,
    ),
    Product(
        product_id="books_002",
        name="ビジネス英会話トレーニング",
        category="書籍・学習",
        price=2500,
        description="ビジネスシーンでよく使う英会話表現。CD付き。",
        features=["ビジネス英語", "CD付き", "実用的", "会話表現"],
        keywords=["英語", "ビジネス", "学習", "会話"],
        rating=4.3,
        stock=70,
    ),
    Product(
        product_id="books_003",
        name="機械学習実装ガイド",
        category="書籍・学習",
        price=5500,
        description="機械学習の実装方法を詳しく解説。コード例豊富。",
        features=["高度な内容", "実装重視", "コード例豊富", "最新技術"],
        keywords=["機械学習", "AI", "プログラミング", "データサイエンス"],
        rating=4.7,
        stock=42,
    ),

    # その他
    Product(
        product_id="misc_001",
        name="多機能卓上ライト",
        category="その他",
        price=2800,
        description="調光・色温度調整可能な卓上ライト。USB充電。",
        features=["調光", "色温度調整", "USB充電", "眼に優しい"],
        keywords=["ライト", "卓上", "LED", "調光"],
        rating=4.4,
        stock=85,
    ),
    Product(
        product_id="misc_002",
        name="トラベルポーチ",
        category="その他",
        price=1800,
        description="旅行やバッグの中の整理に便利。複数ポケット。",
        features=["防水", "複数ポケット", "コンパクト", "軽量"],
        keywords=["ポーチ", "トラベル", "収納", "持ち運び"],
        rating=4.2,
        stock=140,
    ),
    Product(
        product_id="misc_003",
        name="キーボード&マウスセット",
        category="その他",
        price=3500,
        description="ワイヤレスセット。静音設計で快適な操作感。",
        features=["ワイヤレス", "静音", "長寿命", "セット販売"],
        keywords=["キーボード", "マウス", "ワイヤレス", "PC周辺機器"],
        rating=4.3,
        stock=65,
    ),
]


def get_all_products() -> List[Product]:
    """全商品を取得"""
    return PRODUCTS_DATABASE


def get_products_by_category(category: str) -> List[Product]:
    """カテゴリで商品をフィルタリング"""
    return [p for p in PRODUCTS_DATABASE if p.category == category]


def get_categories() -> List[str]:
    """全カテゴリを取得"""
    return sorted(list(set(p.category for p in PRODUCTS_DATABASE)))
