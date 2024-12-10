


# models.py
from sqlalchemy import String, Integer, Column, Text, DateTime
from sqlalchemy.orm import DeclarativeBase, Mapped
from datetime import datetime
# from pytz import timezone
from datetime import datetime, timedelta


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
