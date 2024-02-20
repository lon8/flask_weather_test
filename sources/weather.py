"""
Модуль с функцией запроса к API openweathermap.org
"""
from decouple import config
import requests
from typing import Union
from loguru import logger
from cachetools import cached, TTLCache

# Создаем кэш с временем жизни в секундах (300)
cache = TTLCache(maxsize=100, ttl=300)

WEATHER_API_KEY = config('API_KEY')

@cached(cache)
def fetch_weather(city: str) -> Union[int, False]:
    """
    Функция для запроса текущей температуры в городе
    Используется сервис openweathermap.org. Если количество запросов будет превышено,
    перепишите один из других ключей, указаных в keys.txt, в файл .env
    """
    
    req = requests.get(f'https://api.openweathermap.org/data/2.5/weather?q={city}&units=metric&appid={WEATHER_API_KEY}')

    if req.status_code == 200:
        data = req.json()['main']
        temp = data['temp']
        
        return int(temp)
    else:
        logger.warning(f'Запрос завершился с кодом {req.status_code}')
        return False