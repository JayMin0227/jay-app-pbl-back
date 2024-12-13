



# models.py
from sqlalchemy import String, Integer, Column, Text, DateTime
from sqlalchemy.orm import DeclarativeBase, Mapped
from datetime import datetime
# from pytz import timezone
from datetime import datetime, timedelta
from setting import Base

def get_jst_now():
    return datetime.utcnow() + timedelta(hours=9)

class Base(DeclarativeBase):
    pass

class Idea(Base):
    __tablename__ = "ideas"

    id: Mapped[int] = Column(Integer, primary_key=True, autoincrement=True)  # IDをプライマリキーとして追加
    created_at: Mapped[datetime] = Column(DateTime, default=get_jst_now)  # JST に変更 はい
    title: Mapped[str] = Column(Text, nullable=False)
    content: Mapped[str] = Column(Text, nullable=False)
    tags: Mapped[str] = Column(Text, nullable=True)


#追加
 # 表示用の文字列表現を定義
    def __repr__(self):
        return "<Idea('id={}, created_at={}, title={}, content={}, tags={}')>".format(
            self.id,
            self.created_at,
            self.title,
            self.content,
            self.tags
        )
        
        
        
        
        
#jhdha;





# class Project(Base):
#     __tablename__ = 'projects'

#     id = Column(Integer, primary_key=True)
#     name = Column(String, nullable=False)
#     description = Column(String)
#     created_at = Column(DateTime, default=datetime.utcnow)

#     def __repr__(self):
#         return "<Project(name={}, description={})>".format(
#             self.name,
#             self.description,
#             self.created_at
#         )