from datetime import datetime

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram_calendar import simple_cal_callback, SimpleCalendar
from loguru import logger
import re

from bot_requests.anyprice import get_city_id, get_hotels
from data import config
from keyboards.inline.is_photo_btn import is_photo
from loader import dp
from states.anyprice import Anyprice
from utils.db_api.hotels_bot_sqlite_db import insert
from utils.handle_request import handle_request
from utils.locale_check import locale_check


@dp.message_handler(commands=['lowprice', 'highprice'], state='*')
async def get_low_price_init(message: types.Message, state: FSMContext):
    """
    По нажатию на команду /lowprice или /highprice запускает серию хендлеров для уточнения информации о запросе.
    Сохраняет ответы в state

    :param state: Данные из контекста
    :param message: Входящее сообщение
    :return: None
    """
    logger.info(f'Пользователь {message.from_user.id}: {message.from_user.username} запросил команду /lowprice ')
    await message.answer('Напишите город, где хотите подобрать отель.')
    logger.info('Сохраняю ответ в state: city')

    async with state.proxy() as data:
        data['command'] = message.get_command()
        data['message_id'] = message.message_id

        if message.get_command() == '/lowprice':
            data['price_sort'] = 'PRICE'
        elif message.get_command() == '/highprice':
            data['price_sort'] = 'PRICE_HIGHEST_FIRST'

    await Anyprice.city.set()


@dp.message_handler(state=Anyprice.city)
async def answer_city(message: types.Message, state: FSMContext):
    """
    Получает ответ из get_low_price_init хэндлера, сохраняет в кэш, спрашивает следующий вопрос,
    сохраняет в state следующего вопроса.

    :param message: входящее сообщение из state
    :param state: Переданный контекст
    :return: None
    """
    answer = message.text.lower()

    locale = config.locales[locale_check(answer)].get('locale')
    currency = config.locales[locale_check(answer)].get('currency')
    logger.info(f'Получил ответ: {answer}. Сохраняю в state')

    city_id = await get_city_id(answer, locale)

    async with state.proxy() as data:
        data['city'] = answer
        data['city_id'] = city_id
        data['locale'] = locale
        data['currency'] = currency

    await message.answer(f'Сколько отелей показать? (Max: {config.MAX_HOTELS_TO_SHOW})')
    logger.info('Сохраняю ответ в state: hotel_amount')
    await Anyprice.next()


@dp.message_handler(state=Anyprice.hotel_amount)
async def answer_hotel_amount(message: types.Message, state: FSMContext):
    """
       Получает ответ из answer_city хэндлера, сохраняет в кэш, спрашивает следующий вопрос,
       сохраняет в state следующего вопроса.

       :param message: входящее сообщение из state
       :param state: Переданный контекст
       :return: None
       """
    answer = message.text
    pattern = re.search(r'\D', answer)
    if pattern:
        await message.answer('Введите цифрами')
    logger.info(f'Получил ответ: {answer}. Сохраняю в state')
     
    async with state.proxy() as data:
        data['hotels_amount'] = int(answer)

    await message.answer('Выберите дату заезда', reply_markup=await SimpleCalendar().start_calendar())
    logger.info('Сохраняю ответ в state: hotel_amount')
    await Anyprice.next()


@dp.callback_query_handler(simple_cal_callback.filter(), state=Anyprice.check_in_date)
async def answer_check_in(call: types.CallbackQuery, callback_data: dict, state: FSMContext):
    """
    Получает ответ из хэндлера о дате заезда и сохраняет в state
    :param callback_data:
    :param call: входящее сообщение из state
    :param state: Переданный контекст
    :return:
    """

    logger.info('Вызываю Календарь...')
    selected, date = await SimpleCalendar().process_selection(call, callback_data)
    if selected:
        check_in_date = date.strftime("%Y-%m-%d")
        logger.info(f'Получили дату заселения: - {check_in_date}')

        logger.info('Отвечаем пользователю.')
        await call.message.answer(f'You selected {check_in_date}')
        logger.info(f'Добавляем {check_in_date} в state')

        async with state.proxy() as data:
            data['check_in'] = check_in_date

        logger.info('Спрашиваем у пользователя дату выезда!')
        await call.message.answer('Выберите дату выезда:', reply_markup=await SimpleCalendar().start_calendar())

        await Anyprice.next()


@dp.callback_query_handler(simple_cal_callback.filter(), state=Anyprice.check_out_date)
async def answer_check_out(call: types.CallbackQuery, callback_data: dict, state: FSMContext):
    """
    Получает ответ из хэндлера о дате выезда и сохраняет в state
    :param callback_data:
    :param call: входящее сообщение из state
    :param state: Переданный контекст
    :return:
    """
    logger.info('Вызываю Календарь...')
    selected, date = await SimpleCalendar().process_selection(call, callback_data)
    if selected:
        check_out_date = date.strftime("%Y-%m-%d")
        logger.info(f'Получили дату выезда: - {check_out_date}')

        logger.info('Отвечаем пользователю.')
        await call.message.answer(f'You selected {check_out_date}')
        logger.info(f'Добавляем {check_out_date} в state')

        async with state.proxy() as data:
            data['check_out'] = check_out_date

        logger.info('Спрашиваем у пользователя о количестве взрослых.')
        await call.message.answer('Сколько человек будет заселяться? ')
        logger.info('Сохраняю ответ в state: adult_qnt')
        await Anyprice.next()


@dp.message_handler(state=Anyprice.adults_qnt)
async def answer_adult_qnt(message: types.Message, state: FSMContext):
    """
    Получает ответ пользователя о количестве взрослых
    :param message:
    :param state:
    :return:
    """
    answer = message.text
    pattern = re.search(r'\D', answer)
    if pattern:
        await message.answer('Введите цифрами')

    logger.info(f'Получил ответ {answer}')

    async with state.proxy() as data:
        data['adults_qnt'] = int(answer)

    logger.info('Спрашиваем у пользователя о количестве взрослых.')
    await message.answer('Загрузить фотографии?', reply_markup=is_photo)
    logger.info('Сохраняю ответ в state: adult_qnt')
    await Anyprice.next()


@dp.callback_query_handler(state=Anyprice.IsPhoto)
async def answer_is_photo(call: types.CallbackQuery, state: FSMContext):
    """
        Получает ответ из answer_hotel_amount хэндлера, сохраняет в кэш, в зависимости от результата прошлого ответа,
        или спрашивает следующий вопрос и сохраняет в state следующего вопроса или обнуляет state

        :param call: входящее сообщение из state
        :param state: Переданный контекст
        :return: None
        """
    await call.answer(cache_time=60)
    answer: str = call.data
    logger.info(f'Получил ответ: {answer}. Сохраняю в state')

    async with state.proxy() as data:
        data['is_photo']: str = answer

        if data['is_photo'] == 'да':
            await call.message.answer(f'Укажите количество фотографий. (max: {config.MAX_PHOTO_TO_SHOW})')
            await Anyprice.next()

        elif data['is_photo'] == 'нет':

            await call.message.answer('Загружаю информацию, ожидайте...')
            hotels = await get_hotels(city_id=data['city_id'], hotels_amount=data['hotels_amount'],
                                      currency=data['currency'], locale=data['locale'],
                                      check_in=data['check_in'], check_out=data['check_out'],
                                      adults_qnt=data['adults_qnt'], price_sort=data['price_sort'])

            insert('messages', {
                'message_id': data.get('message_id'),
                'command': data.get('command'),
                'created_at': datetime.now(),
                'city_name': data.get('city'),
                'hotels_amount': data.get('hotels_amount'),
                'user_id': call.from_user.id,
                'check_in': data['check_in'],
                'check_out': data['check_out'],
                'adults_qnt': data['adults_qnt']

            })

            if not hotels:
                await call.message.answer('Гостиниц по Вашему запросу не найдено!')
            else:
                data_to_user_response = await handle_request(request=hotels, message_data=data, is_photo=False)
                for hotel in data_to_user_response:
                    hotel_id = hotel.get('hotel_id')
                    answer_message = f'{hotel.get("hotel_name")}\n' \
                                     f'адрес: {hotel.get("address")}\n' \
                                     f'расстояние от центра: {hotel.get("distance_from_center")}\n' \
                                     f'цена: {hotel.get("price")}\n' \
                                     f'ссылка на отель: {f"ru.hotels.com/ho{hotel_id}"}'

                    await call.message.answer(answer_message)

            await state.reset_state(with_data=False)
            logger.info('Очистил state')


@dp.message_handler(state=Anyprice.Photo_amount)
async def answer_photo_amount(message: types.Message, state: FSMContext):
    """
       Получает ответ из answer_is_photo хэндлера, сохраняет в кэш.
       Делает запрос к RapidApi, возвращает ответ пользователю.

       :param message: входящее сообщение из state
       :param state: Переданный контекст
       :return: None
       """
    answer = message.text
    pattern = re.search(r'\D', answer)
    if pattern:
        await message.answer('Введите цифрами')

    logger.info(f'Получил ответ: {answer}. Сохраняю в state')

    async with state.proxy() as data:
        data['photo_amount'] = int(answer)

        insert('messages', {
            'message_id': data.get('message_id'),
            'command': data.get('command'),
            'created_at': datetime.now(),
            'city_name': data.get('city'),
            'hotels_amount': data.get('hotels_amount'),
            'photo_amount': data.get('photo_amount'),
            'user_id': message.from_user.id,
            'check_in': data['check_in'],
            'check_out': data['check_out'],
            'adults_qnt': data['adults_qnt']
        })

        await message.answer('Загружаю информацию, ожидайте...')

    hotels: list = await get_hotels(city_id=data['city_id'], hotels_amount=data['hotels_amount'],
                                    currency=data['currency'], locale=data['locale'],
                                    check_in=data['check_in'], check_out=data['check_out'],
                                    adults_qnt=data['adults_qnt'], price_sort=data['price_sort'])

    if not hotels:
        await message.answer('Гостиниц по Вашему запросу не найдено!')
    else:
        data_to_user_response = await handle_request(request=hotels, message_data=data, is_photo=True)
        for hotel in data_to_user_response:

            hotel_id = hotel.get('hotel_id')
            answer_message = f'{hotel.get("hotel_name")}\n' \
                             f'адрес: {hotel.get("address")}\n' \
                             f'расстояние от центра: {hotel.get("distance_from_center")}\n' \
                             f'цена: {hotel.get("price")}\n' \
                             f'ссылка на отель: {f"ru.hotels.com/ho{hotel_id}"}'

            await message.answer(answer_message)
            if len(hotel['photo_url']) >= 2:
                media = types.MediaGroup()
                for photo in hotel['photo_url']:
                    media.attach_photo(photo)

                await message.answer_media_group(media)
            else:
                await message.answer_photo(hotel['photo_url'][0])

    await state.reset_state(with_data=False)
    logger.info('Очистил state')
