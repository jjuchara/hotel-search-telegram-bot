# Установка и настройка бота:

1. Скачать и установить **ngrock** по ссылке:
   > <https://ngrok.com>
2. Установить **poetry**:
   > curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python -
3. Клонировать бота с удаленного репозитория:
   > git clone https://gitlab.skillbox.ru/jjuchara/python_basic_diploma.git
4. Установить зависимоти командой:
   > poetry install
5. Зайти в виртуальное окружение командой:
   > poetry shell
6. В файле **data/config.py** поменять данные **webhook_host**, **webapp_host**, **webapp_port** на свои:
    - [ ] *webhook_host*: можно получить после запуска ngrock командой: ->
      > ./ngrock http 3001(Ваш порт)

      и взять данные из строки: *Forwarding* [Пример] ->
      > **https://09c9-37-143-190-231.ngrok.io**
    - [ ] *webapp_host* host вашего соединения. [Пример] ->
      > **localhost**
    - [ ] *webapp_port порт, который указали в ngrock. [Пример] ->
      > **3001**

7. Регистрируем бота через **@BotFather** a также регистрируемся на сайте **rapidapi.com** и получаем token's
8. Переименовать фаил **.env.dist** в **.env** и в файле поменять данные на свои. *BOT_TOKEN* - токен, полученный от @BotFather,
   *RAPID_API_KEY* - ключ, который получили после регистрации приложения
   <https://rapidapi.com/apidojo/api/hotels4/> *(Берем ключ из поля X-RapidAPI-Key)*
9. Запускаем фаил app.py
10. Общаемся с ботом