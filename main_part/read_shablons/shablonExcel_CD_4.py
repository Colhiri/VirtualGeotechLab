import math
import random
import os
import shutil
from time import strftime
import time
import datetime

import numpy as np
import openpyxl
import pandas as pd

def shablonExcel_TPS_CD_4(row, dataframes: list, dct: dict, organise_dct: dict, values_Excel: dict, mode: int) -> None:
    # Организационные моменты
    LAB_NO = organise_dct.get("LAB_NO")
    N_IG = organise_dct.get("N_IG")
    boreHole = organise_dct.get("boreHole")
    depth = organise_dct.get("depth")
    nameSoil = organise_dct.get("nameSoil")


    # Путь для сохранения протоколов
    pathSave = dct.get("pathSave")

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
    try:
        shutil.copy('..\\srcs\\shablons\\TPDS_CD.xlsx'
                    ,f'{pathSave}\\{prot_name}')
        os.rename(
            f'..\\prot\\TPDS_CD.xlsx',
            f'{pathSave}\\{prot_name}')
    except:
        pass

    wb = openpyxl.load_workbook(
        f'{pathSave}\\{prot_name}')
    ws = wb.active

    ws['O20'] = LAB_NO
    ws['O21'] = boreHole
    ws['O22'] = depth
    ws['O23'] = nameSoil

    ws['U20'] = We
    ws['U21'] = p
    ws['U22'] = ps
    ws['U23'] = e
    ws['U24'] = IL

    ### Модули
    ws['A65'] = values_Excel.get('devE50')
    ws['B65'] = values_Excel.get('epsE50')
    ws['B70'] = values_Excel.get('devE0')
    ws['A70'] = values_Excel.get('epsE0')

    ws['O53'] = dct.get('F')
    ws['O54'] = dct.get('C')

    if mode in [1, 2, 3]:
        # Давления
        # K_0
        ws['B47'] = 'K0, д.е.'
        ws['C47'] = (1 - math.sin(math.radians(dct.get('F'))))

        ws['B48'] = 'q_zg, МПа'
        ws['C48'] = dct.get('pressStart1') * (1 - math.sin(math.radians(dct.get('F'))))

        ws['F50'] = 'Точки модуля (полное напр.), МПа'
        ws['F51'] = 'qf (полное напр.), МПа'

        # Первая точка модуля E0
        ws['J50'] = dct.get('pressStart1') * (1 - math.sin(math.radians(dct.get('F'))))
        # Вторая точка модуля E0
        ws['K50'] = dct.get('pressStart1') * (1 - math.sin(math.radians(dct.get('F')))) * 1.6
        # Точка на Е50
        ws['J51'] = values_Excel.get('devE50') + dct.get('pressStart1')

    ws['N47'] = dct.get('pressStart1')
    ws['N48'] = dct.get('pressStart2')
    ws['N49'] = dct.get('pressStart3')

    ws['O47'] = dct.get('pressEnd1')
    ws['O48'] = dct.get('pressEnd2')
    ws['O49'] = dct.get('pressEnd3')

    date_protocol = [str(x) for x in date_protocol.replace(' 00:00:00', '').split('-')]
    date_protocol.reverse()
    str_prot = "Протокол испытаний № " + number_protocol + ' от ' + str('-'.join(map(str, date_protocol)))
    ws['M9'] = str_prot

    ws['M11'] = 'Наименование и адрес заказчика: ' + nameClient
    ws['M12'] = 'Наименование объекта: ' + nameObject

    date_isp_object = [str(x) for x in date_isp_object.replace(' 00:00:00', '').split('-')]
    date_isp_object.reverse()
    ws['M15'] = 'Дата получение объекта подлежащего испытаниям: ' + str('-'.join(map(str, date_isp_object)))

    if isinstance(date_isp, str):
        ws['M16'] = 'Дата испытания: ' + date_isp
    else:
        ws['M16'] = 'Дата испытания: ' + date_isp

    wb.save(f'{pathSave}\\{prot_name}')

    writer = pd.ExcelWriter(
        f'{pathSave}\\{prot_name}', mode='a',
        engine="openpyxl",
        if_sheet_exists='overlay')

    if mode in [2, 3]:
        dataframe0 = dataframes[0]
        dataframe1 = dataframes[1]
        dataframe2 = dataframes[2]
        dataframe3 = dataframes[3]

        dataframe0.to_excel(writer, sheet_name='1', startcol=5, startrow=64, index=False,
                            index_label=False,
                            header=False)

        dataframe1.to_excel(writer, sheet_name='1', startcol=9, startrow=64, index=False,
                            index_label=False,
                            header=False)

        dataframe2.to_excel(writer, sheet_name='1', startcol=11, startrow=64, index=False,
                            index_label=False,
                            header=False)

        dataframe3.to_excel(writer, sheet_name='1', startcol=13, startrow=64, index=False,
                            index_label=False,
                            header=False)

    else:
        dataframe0 = dataframes[0]
        dataframe1 = dataframes[1]
        dataframe2 = dataframes[2]

        dataframe0.to_excel(writer, sheet_name='1', startcol=5, startrow=64, index=False,
                            index_label=False,
                            header=False)

        dataframe0.to_excel(writer, sheet_name='1', startcol=9, startrow=64, index=False,
                            index_label=False,
                            header=False)

        dataframe1.to_excel(writer, sheet_name='1', startcol=11, startrow=64, index=False,
                            index_label=False,
                            header=False)

        dataframe2.to_excel(writer, sheet_name='1', startcol=13, startrow=64, index=False,
                            index_label=False,
                            header=False)
    writer.close()