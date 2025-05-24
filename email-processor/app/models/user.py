from sqlalchemy import Column, Integer, String, Text, delete, select
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session

Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    name = Column(String)
    access_token = Column(Text)
    refresh_token = Column(Text)

def delete_user_by_email(session: Session, email: str):
    stmt = delete(User).where(User.email == email)
    session.execute(stmt)

def insert_user(session: Session, user: User):
    session.merge(user)

def get_user_by_email(session: Session, email: str) -> User | None:
    stmt = select(User).where(User.email == email)
    result = session.execute(stmt).scalar_one_or_none()
    return result