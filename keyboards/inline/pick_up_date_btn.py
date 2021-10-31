from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup

check_in_btn = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text='Дата приезда', callback_data='check in date')
    ],
])


check_out_btn = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text='Дата выезда', callback_data='check out date')
    ],
])

start_kb = ReplyKeyboardMarkup(resize_keyboard=True,)
start_kb.row('Navigation Calendar', 'Dialog Calendar')
