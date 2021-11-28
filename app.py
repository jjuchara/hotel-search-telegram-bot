from loguru import logger
from aiogram import executor
from data import config
import handlers
from loader import bot, dp
from utils.set_default_commands import set_default_commands


async def on_startup(dp):
    logger.add('info.log', format='{time} {level} {message}', level='INFO')
    logger.info('Бот запускается')
    await set_default_commands(dp)
    logger.info('Дефолтные команды созданы!')


async def on_shutdown(dp):
    logger.info('Бот завершает свою работу')

    await bot.delete_webhook()

    # Close DB connection (if used)
    await dp.storage.close()
    await dp.storage.wait_closed()


if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup)



