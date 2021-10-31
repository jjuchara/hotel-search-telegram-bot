import typing

import aiohttp
from loguru import logger

from data import config


async def get_hotels(city_id: int, hotels_amount: int, currency: str, locale: str, check_in: str,
                     check_out: str, adults_qnt: int) -> typing.Optional[list]:
    """
    Запрашивает отели в id города
    :param check_out:
    :param adults_qnt:
    :param check_in:
    :param hotels_amount: Количество городов
    :param city_id: id города
    :param currency: Код валюты
    :param locale: Код страны
    :return: Список отелей
    """

    url = f'{config.BASE_URL}/properties/list'
    params = [("destinationId", city_id), ("pageNumber", 1), ("pageSize", 25), ("checkIn", check_in),
              ("checkOut", check_out), ("adults1", adults_qnt), ("sortOrder", "DISTANCE_FROM_LANDMARK"),
              ("locale", locale), ("currency", currency), ("landmarkIds", "City center")]
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=config.headers, params=params) as resp:
                logger.info(f'Отправляю запрос на сервер {resp.url}')
                response = await resp.json()
                hotels = response.get('data').get('body').get('searchResults').get('results')
                if hotels:
                    return hotels
                logger.error('Гостиниц по вашему запросу не найдено!')
                return None
    except Exception as err:
        logger.error(err)
