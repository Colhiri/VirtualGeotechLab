import math
import random
import os
import shutil
from time import strftime
import time
import datetime

import matplotlib.pyplot as plt
import numpy as np
import openpyxl
import pandas as pd
from scipy import interpolate

def shablonExcel_OCR(row, dataframes: list, organise_dct: dict, values_Excel):
    # Организационные моменты
    LAB_NO = organise_dct.get("LAB_NO")
    N_IG = organise_dct.get("N_IG")
    boreHole = organise_dct.get("boreHole")
    depth = organise_dct.get("depth")
    nameSoil = organise_dct.get("nameSoil")

    # Путь для сохранения протоколов
    pathSave = organise_dct.get("pathSave")

    # Дата получение объекта подлежащего испытаниям
    date_isp_object = str(organise_dct.get("date_isp_object"))

    # Дата испытания
    date_isp = str(organise_dct.get("date_isp"))

    # Дата протокола
    date_protocol = str(organise_dct.get("date_protocol"))

    # Номер протокола
    number_protocol = organise_dct.get("number_protocol")

    # Заказчик
    nameClient = organise_dct.get("nameClient")

    # Объект
    nameObject = organise_dct.get("nameObject")

    # Параметры образца
    We = organise_dct.get('We')
    p = organise_dct.get('p')
    ps = organise_dct.get('ps')
    e = organise_dct.get('e')
    IL = organise_dct.get('IL')

    if LAB_NO is None or LAB_NO == np.nan or LAB_NO == np.NAN or LAB_NO == "None" or LAB_NO == "nAn":
        prot_name = str(row) + '.xlsx'
    else:
        prot_name = LAB_NO + '.xlsx'


    shutil.copy('..\\srcs\\shablons\\OCR.xlsx'
                ,f'{pathSave}\\{prot_name}')


    wb = openpyxl.load_workbook(
        f'{pathSave}\\{prot_name}')
    ws = wb.active

    ws['E16'] = LAB_NO
    ws['E14'] = boreHole
    ws['E15'] = depth
    # ws['C23'] = nameSoil

    ws['D22'] = We
    ws['E22'] = p
    ws['C22'] = ps
    ws['H22'] = e
    ws['L22'] = IL

    # ### Значения для касательного модуля
    # ws['G36'] = values_Excel.get('q_zg')
    # ws['G37'] = values_Excel.get('otn_zg')
    # ws['I36'] = values_Excel.get('otn_END_A')
    # ws['I37'] = values_Excel.get('otn_MAX')
    # ws['K37'] = values_Excel.get('press_MAX')


    # ws['A70'] = values_Excel.get('epsE0')

    # ws['O53'] = dct.get('F')
    # ws['O54'] = dct.get('C')

    # Давления
    # ws['N47'] = dct.get('pressStart1')
    # ws['N48'] = dct.get('pressStart2')
    # ws['N49'] = dct.get('pressStart3')

    # ws['O47'] = dct.get('pressEnd1')
    # ws['O48'] = dct.get('pressEnd2')
    # ws['O49'] = dct.get('pressEnd3')

    date_protocol = [str(x) for x in date_protocol.replace(' 00:00:00', '').split('-')]
    date_protocol.reverse()
    str_prot = "Протокол испытаний № " + number_protocol + ' от ' + str('-'.join(map(str, date_protocol)))
    ws['A9'] = str_prot

    ws['E13'] = 'Наименование и адрес заказчика: ' + nameClient
    ws['E12'] = 'Наименование объекта: ' + nameObject

    # date_isp_object = [str(x) for x in date_isp_object.replace(' 00:00:00', '').split('-')]
    # date_isp_object.reverse()
    # ws['A15'] = 'Дата получение объекта подлежащего испытаниям: ' + str('-'.join(map(str, date_isp_object)))

    # if isinstance(date_isp, str):
    #     ws['A16'] = 'Дата испытания: ' + date_isp
    # else:
    #     ws['A16'] = 'Дата испытания: ' + date_isp
    # Беккер
    ws['K52'] = values_Excel.get('Sigma_Beccer')
    ws['K53'] = values_Excel.get('effective_press')
    ws['K54'] = values_Excel.get('OCR')
    ws['K55'] = values_Excel.get('POP')

    # Казагранде
    ws['K35'] = values_Excel.get('Sigma_CASAGRANDE')
    ws['K36'] = values_Excel.get('effective_press')
    ws['K37'] = values_Excel.get('OCR_CASAGRANDE')
    ws['K38'] = values_Excel.get('POP_CASAGRANDE')

    wb.save(f'{pathSave}\\{prot_name}')

    writer = pd.ExcelWriter(
        f'{pathSave}\\{prot_name}', mode='a',
        engine="openpyxl",
        if_sheet_exists='overlay')

    dataframe1 = dataframes[0]

    dataframe1 = dataframe1.astype('float64')



    # метод Беккера
    (dataframe1.iloc[:, 3:]).to_excel(writer, sheet_name='1', startcol=1, startrow=44, index=False,
                        index_label=False,
                        header=False, float_format="%.20f")
    # Значения для линий
    BECCER = values_Excel.get('BECCER').astype('float64')
    BECCER.to_excel(writer, sheet_name='1', startcol=13, startrow=44, index=False,
                        index_label=False,
                        header=False, float_format="%.20f")


    # метод Казагранде
    (dataframe1.iloc[:, :3]).to_excel(writer, sheet_name='1', startcol=1, startrow=27, index=False,
                                      index_label=False,
                                      header=False, float_format="%.20f")
    # Значения для линий
    CASAGRANDE = values_Excel.get('VALUES_LINES').astype('float64')
    CASAGRANDE.to_excel(writer, sheet_name='1', startcol=13, startrow=27, index=False,
                                      index_label=False,
                                      header=False, float_format="%.20f")



    writer.close()