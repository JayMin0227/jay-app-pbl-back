from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base

# PostgreSQLの接続情報
path = 'postgresql+psycopg://user:postgres@localhost:5432/postgres'

# エンジンの作成（データベースに接続するためのエンジン）
Engine = create_engine(
    path,  # 接続するデータベースのURL
    echo=True  # SQLの実行内容を表示（デバッグ用）
)

# Baseクラスを定義（モデルを定義するためのベースクラス）
Base = declarative_base()
