
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Idea
from datetime import datetime
# from fastapi import HTTPException

#from database import SessionLocal


try:
    # FastAPI がない環境でも読み込めるようにする
    from fastapi import HTTPException
except ImportError:
    HTTPException = None  # Alembic実行時にはHTTPExceptionは不要
    

# 接続先DBの設定
# DATABASE = 'postgresql+psycopg://user:postgres@localhost:5432/postgres'
# DATABASE='postgresql+psycopg2://postgres:Ryoryo150227@db.vgdaqalcxfvdybyhtyjh.supabase.co:5432/postgres'
DATABASE='postgresql://postgres.vgdaqalcxfvdybyhtyjh:Ryoryo150227@aws-0-ap-northeast-1.pooler.supabase.com:5432/postgres'


# SQLAlchemy エンジンの作成
engine = create_engine(
    DATABASE,
    echo=True  # デバッグ用にSQLログを表示
)

# セッションファクトリの作成
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# # ユーザー定義関数（メモ操作関連）
# def read_ideas(session):
#     return session.query(Idea).order_by(Idea.created_at.desc()).all()

# def read_ideas(session):
#     # 作成日時でデータを降順に並べて全て取得するように修正
#     return session.query(Idea).order_by(Idea.created_at.desc()).all()

def read_ideas(session):
    try:
        print("データベースからデータを取得します...")
        ideas = session.query(Idea).order_by(Idea.created_at.desc()).all()  # 日付順でソート
        print("デバッグ: データベースから取得したデータ:", ideas)  # 追加
        return ideas
    except Exception as e:
        print("データ取得エラー:", e)
        raise





# def read_ideas(session):
#     ideas = session.query(Idea).order_by(Idea.created_at.desc()).all()
#     print(f"取得したアイデア数: {len(ideas)}")  # デバッグ用
#     for idea in ideas:
#         print(f"デバッグ: {idea.title}, {idea.content}, {idea.tags}, {idea.created_at}")  # デバッグ用
#     return ideas





def add_idea(db, title, content, tags=None):
    new_idea = Idea(title=title, content=content, tags=tags)
    db.add(new_idea)
    db.commit()
    db.refresh(new_idea)  # 追加: 新しいアイデアをリフレッシュ
    return new_idea


def delete_idea_by_created_at(session, created_at):
    idea = session.query(Idea).filter(Idea.created_at == created_at).first()
    if idea:
        session.delete(idea)
        session.commit()
        return idea
    return None

def delete_idea_by_id(db, idea_id):
    idea = db.query(Idea).filter(Idea.id == idea_id).first()
    if not idea:
        raise HTTPException(status_code=404, detail="Idea not found")
    db.delete(idea)
    db.commit()
    return {"message": "Idea deleted successfully"}




def search_ideas(session, keyword):
    keyword_pattern = f"%{keyword}%"
    return session.query(Idea).filter(
        (Idea.title.ilike(keyword_pattern)) |
        (Idea.content.ilike(keyword_pattern)) |
        ((Idea.tags != None) & (Idea.tags.ilike(keyword_pattern)))  # タグを文字列として検索
    ).all()



def filter_ideas(session, date):
    return session.query(Idea).filter(Idea.created_at >= date).all()




