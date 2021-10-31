from aiogram import types
from loguru import logger

from loader import dp
from utils.user import add_user_to_db


@dp.message_handler()
async def get_all_non_filters_msg(message: types.Message):
    user_id = message.from_user.id
    f_name = message.from_user.first_name
    l_name = message.from_user.last_name
    user_name: str = message.from_user.username

    add_user_to_db(user_name=user_name, user_id=user_id, f_name=f_name, l_name=l_name)
    logger.info(f'Пользователь {user_name}: {user_id} добавлен в базу!')
