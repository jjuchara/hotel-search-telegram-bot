from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart
from loguru import logger

from loader import dp, bot
from utils.user import add_user_to_db


@dp.message_handler(CommandStart())
async def welcome_msg(message: types.Message):
    """
    Сохраняет в словарь Users пользователя нажавшего команду /start
     и отправляет приветственное сообщение.
    :param message: Входящее сообщение
    :return: None
    """
    logger.info(f'Пользователь {message.from_user.id}: {message.from_user.username} запросил команду /start ')
    user_id: int = message.from_user.id
    user_name: str = message.from_user.username
    f_name: str = message.from_user.first_name
    l_name: str = message.from_user.last_name

    add_user_to_db(user_name=user_name, user_id=user_id, f_name=f_name, l_name=l_name)

    me: types.User = await bot.get_me()
    answer_text: str = f'Вас приветствует <i>{me.first_name}.</i>\n' \
                       f' Я помогу Вам подобрать отель для отдыха!\n' \
                       f'Список доступных команд можно найти написав - /help'

    await message.answer(answer_text)
    logger.info(f'Бот ответил {answer_text}')
