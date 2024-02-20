"""
Модуль с маршрутами для управления пользователями и балансом.
"""
from flask import request, jsonify
from loguru import logger
from sources.models import db, UserCreate, User
from sources.weather import fetch_weather


def create_user():
    user_data = request.get_json()
    user = UserCreate(**user_data)
    db_user = User(**user.__dict__)
    db.session.add(db_user)
    db.session.commit()
    return jsonify({
        'id': db_user.id,
        'username': db_user.username,
        'balance': db_user.balance
    })

def get_users():
    users = User.query.all()
    user_list = [{'id': user.id, 'username': user.username, 'balance': user.balance} for user in users]
    return jsonify(user_list)

# Маршрут для увеличения баланса пользователя
def increase_balance():
    """
    Роут для увеличения баланса пользователя
    """
    
    data = request.get_json()
    user_id = data.get('userId')
    city = data.get('city')

    # Получаем температуру воздуха
    temperature = fetch_weather(city)
    if temperature is False:
        logger.error('Не удалось получить температуру')
        return jsonify({'error': 'Не удалось получить температуру'}), 500

    # Находим пользователя
    user = User.query.get(user_id)
    if user is None:
        return jsonify({'error': 'Пользователь не найден'}), 404

    # Увеличиваем баланс пользователя на основе температуры
    user.balance = max(user.balance + temperature, 0)
    db.session.commit()

    return jsonify({'success': True, 'message': f'Баланс пользователя увеличен. Температура воздуха: {temperature}°C'})

    
# Маршрут для уменьшения баланса пользователя

def decrease_balance():
    
    data = request.get_json()
    user_id = data.get('userId')
    city = data.get('city')

    # Получаем температуру воздуха
    temperature = fetch_weather(city)
    if temperature is False:
        return jsonify({'error': 'Не удалось получить температуру, проверьте пожалуйста правильность ввода города'}), 500

    # Находим пользователя
    user = User.query.get(user_id)
    if user is None:
        return jsonify({'error': 'Пользователь не найден'}), 404

    # Уменьшаем баланс пользователя на основе температуры
    user.balance = max(user.balance - temperature, 0)
    db.session.commit()

    return jsonify({'success': True, 'message': f'Баланс пользователя уменьшен. Температура воздуха: {temperature}°C'})
