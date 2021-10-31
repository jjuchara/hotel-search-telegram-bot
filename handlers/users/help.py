from typing import List

from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandHelp
from loguru import logger

from loader import dp, bot


@dp.message_handler(CommandHelp())
async def help_msg(message: types.Message):
    """
    Возвращает полюзователю список доступных команд с описанием.\n
    :param message: Входящее сообщение
    :return: None
    """
    logger.info(f'Пользователь {message.from_user.id}: {message.from_user.username} запросил команду /help ')
    logger.info('Загружаю команды с сервера...')
    commands_list: List[types.BotCommand] = await bot.get_my_commands()
    answer_message: str = 'Список доступных команд: \n'
    for command, descr in commands_list:
        answer_message += f'/{command[1]}: {descr[1]}\n'
    await message.answer(answer_message)
    logger.info('Команды отправлены.')
