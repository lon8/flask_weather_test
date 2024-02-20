"""
Создание сессии базы данных для добавления и изменения информации
"""
from flask_sqlalchemy import SQLAlchemy
from pydantic import BaseModel

db = SQLAlchemy()

#SQLAlchemy model
class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True, index=True)
    username = db.Column(db.String, index=True)
    balance = db.Column(db.Integer)
    
# Pydantic Models
class UserCreate(BaseModel):
    username: str
    balance: int