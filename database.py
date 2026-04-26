import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Idea
from datetime import datetime

load_dotenv()

DATABASE = os.environ["DATABASE_URL"]

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





def add_idea(db, title, content, tags=None, user_id=None):
    new_idea = Idea(
        title=title,
        content=content,
        tags=tags,
        user_id=user_id,
    )
    db.add(new_idea)
    db.commit()
    db.refresh(new_idea)
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




def search_ideas(session, keyword, user_id=None):
    keyword_pattern = f"%{keyword}%"

    query = session.query(Idea)

    if user_id is not None:
        query = query.filter(Idea.user_id == user_id)

    return query.filter(
        (Idea.title.ilike(keyword_pattern)) |
        (Idea.content.ilike(keyword_pattern)) |
        ((Idea.tags != None) & (Idea.tags.ilike(keyword_pattern)))
    ).all()


def filter_ideas(session, date):
    return session.query(Idea).filter(Idea.created_at >= date).all()




