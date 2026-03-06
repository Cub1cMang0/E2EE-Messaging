from sqlalchemy import Column, Integer, String, create_engine, ForeignKey, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from pydantic import BaseModel
from typing import List
import datetime

SQLALCHEMY_DATABASE_URL = "sqlite:///./e2ee_messaging.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Defining database structure and contents
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    display_name = Column(String, unique=True, index=True)
    id_pub_key = Column(String)
    dh_pub_key = Column(String)

class Group(Base):
    __tablename__ = "group_chats"
    id = Column(Integer, primary_key=True, index=True)
    chat_name = Column(String, index=True)
    creator = Column(Integer, ForeignKey("users.id"))
    created_on = Column(DateTime, default=datetime.datetime.utcnow)
    members = relationship("Group_Member", back_populates="group")

class Group_Member(Base):
    __tablename__ = "group_members"
    id = Column(Integer, primary_key=True, index=True)
    group_id = Column(Integer, ForeignKey("group_chats.id"))
    user_id = Column(Integer, ForeignKey("users.id"))
    role = Column(String, default="member")
    joined_at = Column(DateTime, default=datetime.datetime.utcnow)
    group = relationship("Group", back_populates="members")

class Group_Create(BaseModel):
    name: str
    creator_display_name: str
    members_display_names: List[str]

Base.metadata.create_all(bind=engine)