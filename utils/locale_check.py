import re


def locale_check(text: str) -> str:
    """
   Возвращает наименование языка на которм делается запрос
    :param text:
    :return:
    """
    if re.match(r'[a-z]', text):
        return 'en'
    elif re.match(r'[а-я]', text):
        return 'ru'

