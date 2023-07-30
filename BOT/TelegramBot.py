import telebot
from telebot import types
import subprocess
from DataDistributor_DB import DataDitributor as DD

# Токен вашего бота, полученный от BotFather
TOKEN = '5817177597:AAFldPHKS5vSco58icQU56ALbgiQAqyrxT4'

# Создание экземпляра бота
bot = telebot.TeleBot(TOKEN)

BOKEH_SERVER_PORT = 5009

# Путь к исполняемому файлу вашей программы для графиков
PROGRAM_PATH = r'Graph_server.py'

# Команда для запуска локального сервера Bokeh
BOKEH_SERVER_COMMAND = f'bokeh serve --show --port {BOKEH_SERVER_PORT} {PROGRAM_PATH}'

# Инициализация бота
bot = telebot.TeleBot(TOKEN)

# Обработчик команды /start
@bot.message_handler(commands=['start'])
def start(message):
    # Отправка приветственного сообщения и инструкций
    bot.send_message(message.chat.id, "Привет! Я бот для работы с графиками.")
    bot.send_message(message.chat.id, "Для запуска программы для графиков нажмите /run_program.")

    us_id = message.from_user.id
    us_name = message.from_user.first_name
    us_sname = message.from_user.last_name
    username = message.from_user.username

    print(us_id)
    print(us_name)
    print(us_sname)
    print(username)

    distribut = DD()

    DD.write_temporary_user(user_id=us_id, user_name=us_name, user_surname=us_sname, username=username)

# Обработчик команды /run_program
@bot.message_handler(commands=['run_program'])
def run_program(message):
    try:

        us_id = message.from_user.id
        us_name = message.from_user.first_name
        us_sname = message.from_user.last_name
        username = message.from_user.username

        print(us_id)
        print(us_name)
        print(us_sname)
        print(username)

        """
        Получи IP как нибудь,
        us_id можно использовать для идентификатора пользователя в базе данных
        """

        distribut = DD(ip_people=us_id, )


        # Запуск программы для графиков
        subprocess.Popen(BOKEH_SERVER_COMMAND, shell=True)
        bot.send_message(message.chat.id, "Программа для графиков запущена.")

        # Отправка кликабельной ссылки на локальный сервер Bokeh
        bot.send_message(message.chat.id, f"Ссылка на локальный сервер Bokeh: http://localhost:{BOKEH_SERVER_PORT}/Graph_server")
    except Exception as e:
        bot.send_message(message.chat.id, "Произошла ошибка при запуске программы для графиков.")

# Запуск бота
bot.polling()
