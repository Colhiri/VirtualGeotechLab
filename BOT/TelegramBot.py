import subprocess
import patoolib
import os
import requests

import telebot
from telebot import types
import numpy as np

# from GEOF.MECHANIC import start as start_mech
import GEOF.main_part.main_tools as main_tools
from DataDistributor_DB import DataDitributor as DD


TOKEN = '5817177597:AAFldPHKS5vSco58icQU56ALbgiQAqyrxT4'
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['help'])
def commands_bot(message):
    bot.send_message(message.chat.id, "Список доступных команд:")
    bot.send_message(message.chat.id, "Для настройки трехосных графиков (вертикальные и объемные деформации): /run_traxial")
    bot.send_message(message.chat.id, "Для настройки графиков консолидации: /run_consolidation")
    bot.send_message(message.chat.id, "Для настройки графиков одноплоскостного среза: /run_unaxial")
    bot.send_message(message.chat.id, "Для инициализация пользователя в системе: /initialize")
    bot.send_message(message.chat.id, "Для отправки файла шаблона механики: /get_mech_shablon")
    bot.send_message(message.chat.id, "Для запуска записи по шаблону: /give_mech и после отправьте шаблон")

def initialize_user(message):
    global us_id, us_name, us_sname, username, chat_id
    """
    Инициализация пользователя по любому сообщению
    :return:
    """
    us_id = message.from_user.id
    us_name = message.from_user.first_name
    us_sname = message.from_user.last_name
    username = message.from_user.username
    chat_id = message.chat.id

@bot.message_handler(content_types=['document'])
def handle_file(message):
    """
    Временная функция обработчика файлов
    :param message:
    :return:
    """
    initialize_user(message)
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

        ### Удалить строки без механики
        deleteRows = main_tools.ExcelModules(
            path=file_url,
            sheetName='Sheet1',
            howRowsSkip=5,
            howColumnSkip=0
        )

        deleteRows.DeleteDefinitionRows(['P1', 'P_r', 'ocr',
                                         'fi', 'c',
                                         'Eoed01_02_MPa', 'Eobs01_02_Mpa',
                                         # 'CD_sigma1', 'CD_sigma2', 'CD_sigma3',
                                         'CD_E0', 'E50', 'CD_fi', 'CD_c',
                                         'CU_sigma1', 'CU_sigma2', 'CU_sigma3', 'CU_E50', 'CU_fi', 'CU_c',
                                         'UU_sigma1', 'UU_sigma2', 'UU_sigma3', 'UU_c',
                                         ], [None, np.NAN, "None", np.NaN, "nan"])

        deleteRows.replaceChar(',', '.', ['Depth', 'We', 'ps', 'p', 'pd', 'n', 'e', 'Sr', 'WL', 'WP', 'IP', 'IL', 'Ir',
                                          'P1', 'P_r', 'ocr',
                                          'fi', 'c',
                                          'Eoed01_02_MPa', 'Eobs01_02_Mpa',
                                          'CD_sigma1', 'CD_sigma2', 'CD_sigma3',
                                          'CD_u1', 'CD_u2', 'CD_u3',
                                          'CD_v',
                                          'CD_E0', 'E50', 'CD_fi', 'CD_c',
                                          'CU_sigma1', 'CU_sigma2', 'CU_sigma3', 'CU_E50', 'CU_fi', 'CU_c',
                                          'UU_sigma1', 'UU_sigma2', 'UU_sigma3', 'UU_c',
                                          'Dilatanci',    'E_rzg',    'CD_v_rzg',
                                          'GGR10', 'G10_5', 'G5_2', 'G2_1', 'G1_05', 'G05_025', 'G025_01',
                                          'G01_005', 'G005_001', 'G001_0002', 'G0002',
                                          ], typeRewrite='float64')

        worksheet_journal = deleteRows.returnDATAFRAME()

        distribut = DD(id_people=us_id)
        distribut.check_schemas_people()
        dct_combination = distribut.data_give()

        start_mech(worksheet_journal, us_id, dct_combination)

        # Путь к папке, которую нужно добавить в архив
        folder_to_add = f'C:\\Users\\MSI GP66\\PycharmProjects\\dj_project\\GEOF\\prot\\{us_id}'

        files = os.listdir(folder_to_add)
        if os.path.exists(f"temp.rar"):
            os.remove(f"temp.rar")
        if os.path.exists(f"{us_id}.rar"):
            os.remove(f"{us_id}.rar")

        # files = folder_to_add # tuple([folder_to_add+excel for excel in files])

        # Создаем архив
        patoolib.create_archive(f"temp.rar", tuple([folder_to_add]))
        patoolib.create_archive(f"{us_id}.rar", (f"temp.rar",))

        # Отправляем Zip-архив пользователю
        with open(f"{us_id}.rar", 'rb') as zip_file:
            bot.send_document(message.chat.id, zip_file)

        os.remove(f"{us_id}.rar")

    else:
        # Если пользователь отправил что-то кроме документа, просим отправить файл снова
        bot.send_message(message.chat.id, "Пожалуйста, отправьте мне файл.")

@bot.message_handler(commands=['give_mech'])
def give_mech(message):
    initialize_user(message)
    """
    В будущем функция, которая принимает файл от пользователя
    :param message:
    :return:
    """
    # Отправляем сообщение с запросом файла и клавиатурой
    bot.send_message(message.chat.id, "Пожалуйста, отправьте мне файл.")

@bot.message_handler(commands=['get_mech_shablon'])
def get_mech_shablon(message):
    initialize_user(message)
    """
    Отправляет шаблон для заполнения механики
    :param message:
    :return:
    """

    file_path = f"..\\srcs\\shablons\\Data.xlsx"
    with open(file_path, 'rb') as file:
        bot.send_document(message.chat.id, file)


@bot.message_handler(commands=['start'])
def start(message):
    initialize_user(message)

    commands_bot(message)

    distribut = DD(id_people=us_id)
    distribut.write_temporary_user(user_id=us_id,
                                   user_name=us_name,
                                   user_surname=us_sname,
                                   username=username)

@bot.message_handler(commands=['run_unaxial'])
def run_unaxial(message):
    initialize_user(message)

    distribut = DD(id_people=us_id)
    distribut.check_schemas_people()
    distribut.write_data_in_database()

    # Команда для запуска локального сервера Bokeh
    BOKEH_SERVER_PORT = 5020
    PROGRAM_PATH = [r'Graph_unaxial.py', us_id, 'unaxial']

    BOKEH_SERVER_COMMAND = f'bokeh serve --show --port {BOKEH_SERVER_PORT} {PROGRAM_PATH[0]} --args {us_id} {"unaxial"}'
    subprocess.Popen(BOKEH_SERVER_COMMAND, shell=True)

    # Отправка кликабельной ссылки на локальный сервер Bokeh
    bot.send_message(message.chat.id, f"Ссылка на настройки трехосных графиков: http://localhost:{BOKEH_SERVER_PORT}/Unaxial")


@bot.message_handler(commands=['run_traxial'])
def run_traxial(message):
    initialize_user(message)

    distribut = DD(id_people=us_id)
    distribut.check_schemas_people()
    distribut.write_data_in_database()

    # Команда для запуска локального сервера Bokeh
    BOKEH_SERVER_PORT = 5007
    PROGRAM_PATH = [r'Graph_server_volume.py', us_id, 'traxial']

    BOKEH_SERVER_COMMAND = f'bokeh serve --show --port {BOKEH_SERVER_PORT} {PROGRAM_PATH[0]} --args {us_id} {"traxial"}'
    subprocess.Popen(BOKEH_SERVER_COMMAND, shell=True)

    # Отправка кликабельной ссылки на локальный сервер Bokeh
    bot.send_message(message.chat.id, f"Ссылка на настройки трехосных графиков: http://localhost:{BOKEH_SERVER_PORT}/Traxial")

@bot.message_handler(commands=['run_consolidation'])
def run_consolidation(message):
    initialize_user(message)

    distribut = DD(id_people=us_id)
    distribut.check_schemas_people()
    distribut.write_data_in_database()

    # Команда для запуска локального сервера Bokeh
    BOKEH_SERVER_PORT = 5011
    PROGRAM_PATH = [r'Graph_consolidation.py', us_id, 'consolidation']

    BOKEH_SERVER_COMMAND = f'bokeh serve --show --port {BOKEH_SERVER_PORT} {PROGRAM_PATH[0]} --args {us_id} {"consolidation"}'
    subprocess.Popen(BOKEH_SERVER_COMMAND, shell=True)

    # Отправка кликабельной ссылки на локальный сервер Bokeh
    bot.send_message(message.chat.id, f"Ссылка на настройки графика консолидации: http://localhost:{BOKEH_SERVER_PORT}/Consolidation")

bot.polling()
