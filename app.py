"""
Входная точка приложения
"""
from flask import Flask
from sources.models import User, db
from sources.routes import create_user, get_users, increase_balance, decrease_balance
import random

# Подключаем логирование
from loguru import logger

logger.add("debug.log", 
           format="{time} | {level} | {message}",
           level="DEBUG", rotation="10MB",
           compression='zip')

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///./mybase.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
    
    app.add_url_rule('/users', methods=['POST'], view_func=create_user)
    app.add_url_rule('/users', methods=['GET'], view_func=get_users)
    app.add_url_rule('/increase_balance', methods=['POST'], view_func=increase_balance)
    app.add_url_rule('/decrease_balance', methods=['POST'], view_func=decrease_balance)

    # Привязываем экземпляр SQLAlchemy к приложению
    db.init_app(app)

    return app

app = create_app()

def create_users():
    """
    Генерация 5 пользователей при запуске программы
    """
    
    with app.app_context():
        db.create_all()  # Create tables if they do not exist

        # Create 5 users with balances between 5000 and 15000
        for i in range(5):
            username = f'user{i + 1}'
            balance = random.randint(5000, 15000)
            new_user = User(username=username, balance=balance)
            db.session.add(new_user)

        db.session.commit()

if __name__ == '__main__':
    create_users()
    app.run()