import os
from decouple import config


# Данные для запуска Бота


BOT_TOKEN = config('BOT_TOKEN')
HEROKU_APP_NAME = 'skillbox-telegram-bot'


webhook_host = f'https://{HEROKU_APP_NAME}.herokuapp.com'
webhook_path = f'/webhook/{BOT_TOKEN}'
webhook_url = f'{webhook_host}{webhook_path}'

webapp_host = '0.0.0.0'
webapp_port = int(os.environ.get('PORT', '5000'))

# Данные для запросов на RAPID_API

RAPID_API_KEY = config('RAPID_API_KEY')
RAPID_API_HOST = "hotels4.p.rapidapi.com"
BASE_URL = "https://hotels4.p.rapidapi.com"

headers = {
    'x-rapidapi-host': RAPID_API_HOST,
    'x-rapidapi-key': RAPID_API_KEY
}

locales = {
    'en': {
        'locale':'en_US',
        'currency': 'USD'
    },
    'ru': {
        'locale': 'ru_RU',
        'currency': 'RUR'
    }
}

MAX_HOTELS_TO_SHOW = 25
MAX_PHOTO_TO_SHOW = 10
