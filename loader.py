from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.middlewares.logging import LoggingMiddleware

from data import config

WEBHOOK_HOST: str = config.webhook_host

WEBHOOK_PATH: str = config.webhook_path
WEBHOOK_URL: str = config.webhook_url

WEBAPP_HOST: str = config.webapp_host
WEBAPP_PORT: str = config.webapp_port

bot = Bot(token=config.BOT_TOKEN, parse_mode=types.ParseMode.HTML)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
dp.middleware.setup(LoggingMiddleware())
