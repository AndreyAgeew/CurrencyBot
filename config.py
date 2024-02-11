import os

from dotenv import load_dotenv
load_dotenv()

TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')  # Токен бота
CURRENCY_API_URL = 'https://api.exchangerate-api.com/v4/latest/'  # API URL
