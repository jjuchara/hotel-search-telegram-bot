from utils.db_api.hotels_bot_sqlite_db import insert


def add_user_to_db(user_id: int, user_name: str, f_name: str, l_name: str) -> None:
    """
    Доавляет пользователя в базу данных
    :param user_id: Id пользователя в телеграмм
    :param user_name: user_name пользователя в телеграмм
    :param f_name: Имя пользователя в телеграмм
    :param l_name: Фамилия пользователя в телеграмм
    :return: None
    """
    user = {'user_id': user_id,
            'f_name': f_name,
            'l_name': l_name,
            'user_name': user_name
            }

    insert('users', user)
