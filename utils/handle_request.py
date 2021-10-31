import re
from typing import Any, Optional

from loguru import logger

from bot_requests.anyprice import get_photos
from utils.db_api.hotels_bot_sqlite_db import insert


async def prepare_data(hotel, is_photo, message_data) -> dict:
    """
    Подготавливает данные для возврата пользователю.
    :param hotel:
    :param is_photo:
    :param message_data:
    :return:
    """
    hotel_id = hotel.get('id')
    hotel_name = hotel.get('name')
    base_address = hotel.get('address')
    address = f'Город {base_address.get("region")}, {base_address.get("locality")},' \
              f'{hotel.get("address").get("streetAddress")}'
    price = hotel.get('ratePlan').get('price').get('current')
    distance_from_center = hotel.get('landmarks')[0].get('distance')

    logger.info('Созраняю данные запроса отелей в базу данных!')
    insert('hotels', {
        'hotel_id': hotel_id,
        'hotel_name': hotel_name,
        'address': address,
        'price': price,
        'message_id': message_data['message_id'],
        'distance_from_center': distance_from_center
    })

    if is_photo:
        photo_url_list = await get_photos(hotel_id=hotel['id'], hotels_amount=message_data.get('photo_amount'))
        logger.info('Сохраняю фото в базу данных.')
        for url in photo_url_list:
            insert('photos', {
                'photo_url': url,
                'hotel_id': hotel_id,
            })

    data_to_return = {
        'hotel_id': hotel_id,
        'hotel_name': hotel_name,
        'address': address,
        'distance_from_center': distance_from_center,
        'price': price,
        'photo_url': photo_url_list if is_photo else None
    }
    return data_to_return


async def handle_request(request: list, message_data: dict, is_photo: bool) -> list:
    """
    Обрабатывает ответ от сервера на запрос отелей. Если необходимы фото, делает запрос за фото.
    Сохраняет поулченные данные в базу данных, и возвращает данные для ответа в виде списка.

    :param is_photo:
    :param request:
    :param message_data:
    :return:
    """
    data_to_return: list = []
    for hotel in request:
        hotel_data = await prepare_data(hotel, is_photo, message_data)
        data_to_return.append(hotel_data)
    return data_to_return


async def handle_best_deal_request(request: list, message_data: dict, is_photo: bool) -> Optional[list]:
    """
        Обрабатывает ответ от сервера на запрос отелей. Если необходимы фото, делает запрос за фото.
        Сохраняет поулченные данные в базу данных, и возвращает данные для ответа в виде списка.

        :param is_photo:
        :param request:
        :param message_data:
        :return:
        """
    data_to_return: list = []
    hotel_to_return = [hotel for hotel in request if
                       float(re.sub(r',', '.', hotel.get('landmarks')[0].get('distance').split()[0])) <=
                       message_data['distance_from_center'] and hotel.get('ratePlan').get('price').get(
                           'exactCurrent') <= message_data['max_price']]
    price_sorted_data: list[Any] = sorted(hotel_to_return,
                                          key=lambda t: t.get('ratePlan').get('price').get('exactCurrent'))

    for hotel in price_sorted_data[:message_data['hotels_amount']]:
        hotel_data = await prepare_data(hotel, is_photo, message_data)
        data_to_return.append(hotel_data)

    if len(data_to_return) >= message_data['hotels_amount']:
        return data_to_return
    return None
