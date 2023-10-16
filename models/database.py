from sqlalchemy import Column, Integer, String, DATETIME

from database.main import Base


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    usr = Column(String, index=True, nullable=False)
    pwd = Column(String, nullable=False)


class Note(Base):
    __tablename__ = "notes"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True, nullable=False)
    author_id = Column(Integer, index=True, nullable=True)
    content = Column(String)
    update_at = Column(DATETIME)


class Comment(Base):
    __tablename__ = "comments"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True, nullable=False)
    author_id = Column(Integer, index=True, nullable=True)
    note_id = Column(Integer, index=True, nullable=False)
    content = Column(String)
    update_at = Column(DATETIME)
