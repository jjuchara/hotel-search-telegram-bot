from decouple import config

# Данные для запуска Бота

BOT_TOKEN = config('BOT_TOKEN')

webhook_host = 'https://09c9-37-147-190-231.ngrok.io'
webhook_path = '/bot.py'
webhook_url = f'{webhook_host}{webhook_path}'

webapp_host = 'localhost'
webapp_port = 3001

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
