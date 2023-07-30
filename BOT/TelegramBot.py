import telebot
from telebot import types
import subprocess
from DataDistributor_DB import DataDitributor as DD
import zipfile
from GEOF.MECHANIC import start as start_mech

# Токен вашего бота, полученный от BotFather
TOKEN = '5817177597:AAFldPHKS5vSco58icQU56ALbgiQAqyrxT4'

# Инициализация бота
bot = telebot.TeleBot(TOKEN)

# Объявляем состояния
states = {}

@bot.message_handler(content_types=['document'])
def handle_file(message):
    # Проверяем, что сообщение содержит документ
    if message.document:
        # Получаем информацию о документе
        document = message.document
        file_id = document.file_id
        file_name = document.file_name

        # Скачиваем документ по его file_id
        file_info = bot.get_file(file_id)
        file_url = f'https://api.telegram.org/file/bot{bot.token}/{file_info.file_path}'

        # Обрабатываем документ по необходимости
        # В данном примере мы просто отправим сообщение с информацией о файле
        bot.send_message(message.chat.id, f"Получен файл: {file_name}")

        start_mech(file_url)

    else:
        # Если пользователь отправил что-то кроме документа, просим отправить файл снова
        bot.send_message(message.chat.id, "Пожалуйста, отправьте мне файл.")

# Обработчик команды /give_mech
@bot.message_handler(commands=['give_mech'])
def give_mech(message):

    # Отправляем сообщение с запросом файла и клавиатурой
    bot.send_message(message.chat.id, "Пожалуйста, отправьте мне файл.")

    us_id = message.from_user.id
    us_name = message.from_user.first_name
    us_sname = message.from_user.last_name
    username = message.from_user.username

# Обработчик команды /get_mech_shablon
@bot.message_handler(commands=['get_mech_shablon'])
def get_mech_shablon(message):

    file_path = '../srcs/shablons/Data.xlsx'
    with open(file_path, 'rb') as file:
        bot.send_document(message.chat.id, file)

    us_id = message.from_user.id
    us_name = message.from_user.first_name
    us_sname = message.from_user.last_name
    username = message.from_user.username

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

    distribut = DD(id_people=us_id)
    distribut.write_temporary_user(user_id=us_id, user_name=us_name, user_surname=us_sname, username=username)

# Обработчик команды /run_program
@bot.message_handler(commands=['run_program'])
def run_program(message):
    us_id = message.from_user.id
    us_name = message.from_user.first_name
    us_sname = message.from_user.last_name
    username = message.from_user.username

    distribut = DD(id_people=us_id)
    distribut.check_schemas_people()
    distribut.write_data_in_database()

    # Запуск программы для графиков
    # Команда для запуска локального сервера Bokeh
    # Путь к исполняемому файлу вашей программы для графиков
    BOKEH_SERVER_PORT = 5009
    PROGRAM_PATH = [r'Graph_server.py', us_id]
    args = [f'bokeh serve --show --port {BOKEH_SERVER_PORT} {PROGRAM_PATH}']

    BOKEH_SERVER_COMMAND = f'bokeh serve --show --port {BOKEH_SERVER_PORT} {PROGRAM_PATH[0]} --args {us_id}'
    subprocess.Popen(BOKEH_SERVER_COMMAND, shell=True)

    bot.send_message(message.chat.id, "Программа для графиков запущена.")

    # Отправка кликабельной ссылки на локальный сервер Bokeh
    bot.send_message(message.chat.id, f"Ссылка на локальный сервер Bokeh: http://localhost:{BOKEH_SERVER_PORT}/Graph_server")
    """except Exception as e:
        bot.send_message(message.chat.id, "Произошла ошибка при запуске программы для графиков.")"""

# Запуск бота
bot.polling()
