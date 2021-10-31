from aiogram.dispatcher.filters.state import StatesGroup, State


class Bestdeal(StatesGroup):
    city = State()
    max_price = State()
    distance_from_center = State()
    hotel_amount = State()
    check_in_date = State()
    check_out_date = State()
    adults_qnt = State()
    IsPhoto = State()
    Photo_amount = State()
