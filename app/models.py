from sqlalchemy.sql.sqltypes import Boolean
from .database import Base
from sqlalchemy import Column, Integer, String, ForeignKey, UniqueConstraint, column, Text

class User(Base):
    __tablename__ = 'users'
    user_id = Column(Integer, primary_key=True)
    user_number = Column(Integer, unique=True)
    user_email = Column(String, nullable=False)
    user_password = Column(String, nullable=False)
    is_admin = Column(Boolean, nullable=False, default=False)

class AdminUser(Base):
    __tablename__ = 'admins'
    user_id_admin = Column(Integer, primary_key=True)
    user_name_admin = Column(String, nullable=False)
    user_email_admin = Column(String, nullable=False)
    user_password_admin = Column(String, nullable=False)
    is_admin = Column(Boolean, nullable=False, default=True)

class Post(Base):
    __tablename__ = 'posts'
    id = Column(Integer, primary_key=True, index=True, nullable=False)
    title = Column(String, index=True, nullable=False)
    content = Column(Text, nullable=False)
    category = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey('users.user_id'), nullable=False)