from datetime import datetime

from aiogram import types
from aiogram.dispatcher.filters import Command
from loguru import logger

from loader import dp
from utils.db_api.hotels_bot_sqlite_db import fetch_all


@dp.message_handler(Command(['history']))
async def handling_history_command(message: types.Message) -> None:
    """
    Обрабатывает запук команды history
    :param message:
    :return:
    """
    user_id = message.from_user.id
    logger.info(f'Пользователь {user_id}: {message.from_user.username} запросил команду /start ')

    await message.answer('Проверяю историю запросов....')

    db_fetch_messages = fetch_all(table='messages', columns=['message_id', 'command', 'created_at'],
                                  detail=f'user_id = {user_id}')[:5]
    for message_ in db_fetch_messages:
        db_fetch_hotels = fetch_all(table='hotels', columns=['hotel_id', 'hotel_name'],
                                    detail=f'message_id = {message_["message_id"]}')
        message_['hotels'] = db_fetch_hotels
        command = message_['command']
        create_at = datetime.strptime(message_['created_at'], '%Y-%m-%d %H:%M:%S.%f').strftime('%d.%m.%Y г. %H:%M:%S')
        hotels = message_['hotels']
        answer_command = f'Введенная команда: {command},\n дата создания: {create_at},\n'
        for hotel in hotels:
            hotel_str = f' {hotel["hotel_name"]}: ru.hotels.com/ho{hotel["hotel_id"]},\n'
            answer_command += hotel_str

        await message.answer(answer_command)
