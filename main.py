# from fastapi import FastAPI
# from fastapi.middleware.cors import CORSMiddleware
# from database import SessionLocal, read_ideas, search_ideas
# from fastapi import FastAPI, HTTPException
# #fhiuhddd

# app = FastAPI()

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_credentials=True,     
#     allow_methods=["*"],
#     allow_headers=["*"],
# )


# @app.get("/")
# async def root():
#     return {"message": "Hello World From Fast API!"}


# @app.get("/ideas")
# def get_ideas():
#     with SessionLocal() as session:
#         return read_ideas(session)
    



# @app.get("/ideas/search")
# def search_idea(keyword: str):
#     try:
#         with SessionLocal() as session:
#             results = search_ideas(session, keyword)
#             if not results:
#                 return {"message": "No results found for the keyword."}
#             return results
#     except Exception as e:
#         print(f"Error: {e}")  # ログをターミナルに出力
#         raise HTTPException(status_code=500, detail="Internal Server Error")

    
# # @app.get("/auth")
# # def auth_page():
# #     return {"message": "Auth Page"}

# @app.get("/book")
# def book_page():
#     return {"message": "Book Page"}




















from fastapi import FastAPI, Depends, HTTPException, Header
from sqlalchemy.orm import Session
from database import SessionLocal, read_ideas, add_idea, delete_idea_by_id, search_ideas, filter_ideas
from pydantic import BaseModel
from datetime import datetime
from models import Idea
from fastapi import HTTPException
from fastapi.middleware.cors import CORSMiddleware  # 追加
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
from sqlalchemy.types import Date
from datetime import timedelta

import os
import json
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError
from dotenv import load_dotenv

app = FastAPI()

# CORS設定の追加


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



load_dotenv()

SUPABASE_URL = os.environ["SUPABASE_URL"].rstrip("/")
SUPABASE_ANON_KEY = os.environ["SUPABASE_ANON_KEY"]


def get_current_user_id(authorization: str | None = Header(default=None)) -> str:
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="ログインが必要です。")

    token = authorization.replace("Bearer ", "", 1).strip()

    request = Request(
        f"{SUPABASE_URL}/auth/v1/user",
        headers={
            "apikey": SUPABASE_ANON_KEY,
            "Authorization": f"Bearer {token}",
        },
    )

    try:
        with urlopen(request, timeout=10) as response:
            user = json.loads(response.read().decode("utf-8"))
    except HTTPError:
        raise HTTPException(status_code=401, detail="認証トークンが無効です。")
    except URLError:
        raise HTTPException(status_code=503, detail="Supabase Authに接続できません。")
    except Exception as e:
        print("認証確認エラー:", e)
        raise HTTPException(status_code=500, detail="認証確認中にエラーが発生しました。")

    user_id = user.get("id")
    if not user_id:
        raise HTTPException(status_code=401, detail="ユーザー情報を取得できません。")

    return user_id


# 入力データの型を定義
class IdeaCreate(BaseModel):
    title: str
    content: str
    tags: str = None

# データベースセッションの取得
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
        
# ルートエンドポイント
@app.get("/")
def read_root():
    return {"message": "Welcome to the FastAPI Ideas API!"}



@app.get("/ideas")
def get_ideas(
    db: Session = Depends(get_db),
    user_id: str = Depends(get_current_user_id),
):
    try:
        print("ログインユーザー:", user_id)
        print("データベース接続確認...")

        ideas = (
            db.query(Idea)
            .filter(Idea.user_id == user_id)
            .order_by(Idea.created_at.desc())
            .all()
        )
        print("データ取得成功:", ideas)

        return [
            {
                "id": idea.id,
                "created_at": idea.created_at.strftime("%Y-%m-%d %H:%M:%S"),
                "title": idea.title,
                "content": idea.content,
                "tags": idea.tags.split(",") if idea.tags else [],
            }
            for idea in ideas
        ]
    except HTTPException:
        raise
    except Exception as e:
        print("エラー発生:", e)
        raise HTTPException(status_code=500, detail=str(e))








@app.post("/ideas")
def create_idea(
    idea: IdeaCreate,
    db: Session = Depends(get_db),
    user_id: str = Depends(get_current_user_id),
):
    return add_idea(db, idea.title, idea.content, idea.tags, user_id)


# @app.delete("/ideas/reset")
# def reset_ids(db: Session = Depends(get_db)):
#     """
#     全メモのIDを1から連番で振り直すエンドポイント
#     """
#     ideas = db.query(Idea).order_by(Idea.created_at).all()  # 全てのメモを作成日時順に取得

#     if not ideas:
#         return {"message": "リセットするメモがありません。"}

#     for index, idea in enumerate(ideas, start=1):  # 1から新しいIDを割り振る
#         idea.id = index
#     db.commit()  # 変更を確定

#     # PostgreSQL のシーケンスをリセット
#     db.execute("ALTER SEQUENCE ideas_id_seq RESTART WITH 1;")
#     db.commit()

#     return {"message": "IDリセット完了"}


# @app.delete("/ideas/id/{idea_id}")
# def delete_idea_by_id_endpoint(idea_id: int, db: Session = Depends(get_db)):
#     return delete_idea_by_id(db, idea_id)



from datetime import datetime

@app.delete("/ideas/{idea_id}")
def delete_idea(
    idea_id: int,
    db: Session = Depends(get_db),
    user_id: str = Depends(get_current_user_id),
):
    idea = (
        db.query(Idea)
        .filter(Idea.id == idea_id, Idea.user_id == user_id)
        .first()
    )

    if not idea:
        raise HTTPException(status_code=404, detail="Idea not found")

    db.delete(idea)
    db.commit()

    return {"message": "Idea deleted successfully"}


# @app.delete("/ideas/date/{created_at}")
# def delete_idea_by_date(created_at: str, db: Session = Depends(get_db)):
#     try:
#         # created_atをDate型にパース（時間なし）
#         created_at_date = datetime.strptime(created_at, "%Y-%m-%d").date()
#         # created_atを比較してレコードを取得
#         idea = db.query(Idea).filter(Idea.created_at.cast(Date) == created_at_date).first()
#         if not idea:
#             raise HTTPException(status_code=404, detail="Idea not found")
#         db.delete(idea)
#         db.commit()
#         return {"message": "Idea deleted successfully"}
#     except ValueError:
#         raise HTTPException(status_code=400, detail="Invalid date format. Use YYYY-MM-DD")








# # メモの検索
# @app.get("/ideas/search")
# def search_idea(keyword: str, db: Session = Depends(get_db)):
#     return search_ideas(db, keyword)


@app.get("/ideas/search")
def search_idea(
    keyword: str,
    db: Session = Depends(get_db),
    user_id: str = Depends(get_current_user_id),
):
    ideas = search_ideas(db, keyword, user_id)
    return [
        {
            "id": idea.id,
            "created_at": idea.created_at.strftime("%Y-%m-%d"),
            "title": idea.title,
            "content": idea.content,
            "tags": idea.tags.split(",") if idea.tags else []
        }
        for idea in ideas
    ]


# # メモの編集
# @app.put("/ideas/{idea_id}")
# def update_idea(idea_id: int, idea: IdeaCreate, db: Session = Depends(get_db)):
#     existing_idea = db.query(Idea).filter(Idea.id == idea_id).first()
#     if not existing_idea:
#         return {"error": "Idea not found"}
#     existing_idea.title = idea.title
#     existing_idea.content = idea.content
#     existing_idea.tags = idea.tags
#     db.commit()
#     return existing_idea



@app.put("/ideas/{idea_id}")
def update_idea(
    idea_id: int,
    idea: IdeaCreate,
    db: Session = Depends(get_db),
    user_id: str = Depends(get_current_user_id),
):
    existing_idea = (
        db.query(Idea)
        .filter(Idea.id == idea_id, Idea.user_id == user_id)
        .first()
    )

    if not existing_idea:
        raise HTTPException(status_code=404, detail="Idea not found")

    existing_idea.title = idea.title
    existing_idea.content = idea.content
    existing_idea.tags = idea.tags
    db.commit()
    db.refresh(existing_idea)

    return {
        "id": existing_idea.id,
        "title": existing_idea.title,
        "content": existing_idea.content,
        "tags": existing_idea.tags,
        "created_at": existing_idea.created_at.strftime("%Y-%m-%d"),
    }



# # メモのフィルタリング
# @app.get("/ideas/filter")
# def filter_idea(date: datetime, db: Session = Depends(get_db)):
#     return filter_ideas(db, date)


# **ここが追加**
# /auth のエンドポイント
@app.get("/auth")
def auth_page():
    return {"message": "Auth Page"}

# /book のエンドポイント
@app.get("/book")
def book_page():
    return {"message": "Book Page"}



# @app.route("/ideas/reset", methods=["DELETE"])
# def reset_ids(db: Session = Depends(get_db)):
#     """
#     全メモのIDをリセットするエンドポイント
#     """
#     ideas = db.query(Idea).order_by(Idea.created_at).all()

#     if not ideas:
#         return {"message": "リセットするメモがありません。"}

#     for index, idea in enumerate(ideas, start=1):
#         idea.id = index  # IDを順番に設定
#     db.commit()

#     # シーケンスをリセット
#     db.execute("ALTER SEQUENCE ideas_id_seq RESTART WITH 1;")
#     db.commit()

#     return {"message": "IDリセット完了"}
