from aiogram import types


async def set_default_commands(dp):
    """
    Создает дефолтные команды в боте на основе списка ниже.
    :param dp:
    :return:
    """
    await dp.bot.set_my_commands([
        types.BotCommand('start', 'Запустить бота'),
        types.BotCommand('help', 'Помощь'),
        types.BotCommand('lowprice', 'Отели с минимальными ценами'),
        types.BotCommand('highprice', 'Отели с максимальными ценами'),
        types.BotCommand('highprice', 'Отели с максимальными ценами'),
        types.BotCommand('bestdeal', 'Лучший вариант (цена/качество)'),
        types.BotCommand('history', 'История просмотров'),
    ])
