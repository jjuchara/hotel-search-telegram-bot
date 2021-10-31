from loguru import logger

from data import config
import handlers
from loader import bot, dp
from utils.set_default_commands import set_default_commands


async def on_startup(dp):
    logger.add('info.log', format='{time} {level} {message}', level='INFO')
    logger.info('Бот запускается')
    await bot.set_webhook(config.webhook_url)
    logger.info('веб хуки настроены и запущены!')
    await set_default_commands(dp)
    logger.info('Дефолтные команды созданы!')
    # insert code here to run it after start


async def on_shutdown(dp):
    logger.info('Бот завершает свою работу')
    # insert code here to run it before shutdown

    # Remove webhook (not acceptable in some cases)
    await bot.delete_webhook()

    # Close DB connection (if used)
    await dp.storage.close()
    await dp.storage.wait_closed()


if __name__ == '__main__':
    from aiogram import executor

    executor.start_webhook(
        dispatcher=dp,
        webhook_path=config.webhook_path,
        on_startup=on_startup,
        on_shutdown=on_shutdown,
        skip_updates=True,
        host=config.webapp_host,
        port=config.webapp_port,
    )
