import math
import random
import os
import shutil
from time import strftime
import time
import datetime
import json

import matplotlib.pyplot as plt
import numpy as np
import openpyxl
import pandas as pd
from scipy import interpolate

import main_part.graphic.TPDS_on_CF as TPDSCF
import main_part.graphic.TPDS_on_E50 as TPDS50


import main_part.graphic.SPS as SPS
import main_part.graphic.SPD as SPD
import main_part.graphic.TPDS_on_CF_RZG as TPDSRZG
import main_part.graphic.TPDS_on_CF_RZG_50 as TPDSRZG50
import main_part.graphic.OCR as OCR_ISP


import main_part.main_tools as main_tools

import main_part.read_shablons as read_shablons



### Удалить строки без механики
deleteRows = main_tools.ExcelModules(path=".\\Data.xlsx",
                                     sheetName='Sheet1',
                                     howRowsSkip=5,
                                     howColumnSkip=0
                                     )
"""
deleteRows.DeleteDefinitionRows(['P1', 'P_r', 'ocr',
                                 'fi', 'c',
                                 'fi_nn','c_nn',
                                 'Eoed01_02_MPa','Eobs01_02_Mpa',
                                 'CD_sigma1','CD_sigma2','CD_sigma3',
                                 'CD_E0','E50','CD_fi', 'CD_c',
                                 'CU_sigma1', 'CU_sigma2', 'CU_sigma3', 'CU_E50', 'CU_fi', 'CU_c',
                                 'UU_sigma1', 'UU_sigma2', 'UU_sigma3', 'UU_c',
                                 ], [None, np.NAN, "None", np.NaN, "nan"])
"""
deleteRows.DeleteDefinitionRows(['CD_fi', 'CD_c',], [None, np.NAN, "None", np.NaN, "nan"])


deleteRows.replaceChar(',', '.', ['Depth','We', 'ps', 'p', 'pd', 'n', 'e', 'Sr', 'WL', 'WP', 'IP', 'IL', 'Ir',
                                  'P1', 'P_r', 'ocr',
                                 'fi', 'c',
                                 'fi_nn','c_nn',
                                 'Eoed01_02_MPa','Eobs01_02_Mpa',
                                 'CD_sigma1','CD_sigma2','CD_sigma3',
                                 'CD_u1','CD_u2','CD_u3',
                                  'CD_v',
                                 'CD_E0','E50','CD_fi', 'CD_c',
                                 'CU_sigma1', 'CU_sigma2', 'CU_sigma3', 'CU_E50', 'CU_fi', 'CU_c',
                                 'UU_sigma1', 'UU_sigma2', 'UU_sigma3', 'UU_c',
                                 ], typeRewrite='float64')

worksheet_journal = deleteRows.returnDATAFRAME()


count_rows = len(worksheet_journal)
for row in range(0, count_rows):

    # Список для сохранения датафреймов, которые возвращаются из TPDS
    save_DF = []

    # Распаковка параметров из Датафрейма
    LAB_NO = worksheet_journal['Ind_lab'][row]
    N_IG = worksheet_journal['Ind'][row]
    boreHole = worksheet_journal['BH'][row]
    depth = worksheet_journal['Depth'][row]
    nameSoil = worksheet_journal['name_soil'][row]

    # Дата получение объекта подлежащего испытаниям
    date_isp_object = worksheet_journal['data_f'][row]

    # Дата испытания
    date_isp = worksheet_journal['data_test'][row]

    # Дата протокола
    date_protocol = worksheet_journal['data_prot'][row]

    # Номер протокола
    number_protocol = worksheet_journal['Np'][row]

    # Заказчик
    nameClient = "Переход трубопровода через р. Енисей"  # ['Ind_lab'][row]

    # Объект
    nameObject = 'ООО Регионстрой'  # ['Ind_lab'][row]

    # Физические параметры для протокола
    We = worksheet_journal['We'][row]
    p = worksheet_journal['p'][row]
    ps = worksheet_journal['ps'][row]
    e = worksheet_journal['e'][row]
    IP = worksheet_journal['IP'][row]
    IL = worksheet_journal['IL'][row]
    Sr = worksheet_journal['Sr'][row]

    # Создание папки для складирования испытаний в объекте
    pathSave = os.path.join(f".\\prot\\{nameObject}")
    if not os.path.exists(pathSave):
        os.mkdir(pathSave)

    organise_dct = {
        "LAB_NO": LAB_NO,
        "N_IG": N_IG,
        "boreHole": boreHole,
        "depth": depth,
        "nameSoil": nameSoil,
        "date_isp_object": date_isp_object,
        "date_isp": date_isp,
        "date_protocol": date_protocol,
        "number_protocol": number_protocol,
        "nameClient": nameClient,
        "nameObject": nameObject,
        'We': We,
        'p': p,
        'ps': ps,
        'e': e,
        'IP': IP,
        'IL': IL,

    }

    # Активация разгрузок
    rzg = False

    # Графики по трехосникам КД
    if not rzg and str(worksheet_journal['CD_sigma1'][row]) not in ["None", "nan"]:

        # Выбор давлений
        pressStart1 = worksheet_journal['CD_sigma1'][row]
        pressStart2 = worksheet_journal['CD_sigma2'][row]
        pressStart3 = worksheet_journal['CD_sigma3'][row]

        # Выбор значений механики
        E_0 = worksheet_journal['CD_E0'][row]
        E_50 = worksheet_journal['E50'][row]
        F = worksheet_journal['CD_fi'][row]
        C = worksheet_journal['CD_c'][row]


        pathSave = os.path.join(pathSave, 'Трехосные_КД_ПП')
        if not os.path.exists(pathSave):
            os.mkdir(pathSave)

        # Расчет для графиков по трем значениям
        press16 = pressStart1 * 1.6
        countPoint = 200
        endE1 = 11.4

        N = 2 * math.tan(math.pi * F / 180) * (
                (((math.tan(math.pi * F / 180)) ** 2) + 1) ** (1 / 2)) + 2 * (
                    (math.tan(math.pi * F / 180)) ** 2) + 1
        M = 2 * (N ** (1 / 2)) * C
        pressEnd1 = (pressStart1 * N + M)
        pressEnd2 = pressStart2 * (
                2 * math.tan(math.pi * F / 180) * ((((math.tan(math.pi * F / 180)) ** 2) + 1) ** (1 / 2)) + 2 * (
                (math.tan(math.pi * F / 180)) ** 2) + 1) + (2 * ((2 * math.tan(math.pi * F / 180) * (
                (((math.tan(math.pi * F / 180)) ** 2) + 1) ** (1 / 2)) + 2 * ((math.tan(
            math.pi * F / 180)) ** 2) + 1) ** (1 / 2)) * C)
        pressEnd3 = (pressStart3 * N + M)

        # mode = 1 --- запись по прочностям с модулями и неправильными линейными графиками
        # mode = 2 --- запись 4 графиков (деформация + прочности с модулями)
        # mode = 3 --- запись 4 графиков (деформация с разгрузкой + прочности с модулями)

        mode = 2

        # Стандартная формула
        K_0 = 1 - math.sin(math.radians(F))
        #
        #
        #
        if mode == 1:
            namesISP = ["graph1", "graph2", "graph3"]
            pressStarts = [pressStart1, pressStart2, pressStart3]
            pressEnds = [pressEnd1, pressEnd2, pressEnd3]


        if mode == 2:
            namesISP = ["graph0", "graph1", "graph2", "graph3"]
            pressStarts = [pressStart1 * K_0, pressStart1, pressStart2, pressStart3]
            pressEnds = [pressEnd1, pressEnd1, pressEnd2, pressEnd3]

        if mode == 3:
            namesISP = ["graph0", "graph1", "graph2", "graph3"]
            pressStarts = [pressStart1 * K_0, pressStart1, pressStart2, pressStart3]
            pressEnds = [pressEnd1, pressEnd1, pressEnd2, pressEnd3]


        for name, pressStart, pressEnd in zip(namesISP, pressStarts, pressEnds):
            dct = {'pressStart': pressStart,
                   'pressStart1': pressStart1,
                   'pressStart2': pressStart2,
                   'pressStart3': pressStart3,
                   'E_0': E_0,
                   'E_50': E_50,
                   'F': F,
                   'C': C,
                   'countPoint': countPoint,
                   'endE1': endE1,
                   'pressEnd1': pressEnd1,
                   'pressEnd2': pressEnd2,
                   'pressEnd3': pressEnd3,
                   'pressEnd': pressEnd,
                   'pathSave': pathSave,
                   'name': name,
                   }

            typeINTERPOLATION = ["interp1d",
                                 "CubicSpline",
                                 "PchipInterpolator", # очень неплохо
                                 "Akima1DInterpolator", # неплохо
                                 "BarycentricInterpolator",
                                 "KroghInterpolator",
                                 "make_interp_spline", # что-то в этом есть
                                 "interp1d", # плоская залупа
                                 # "RegularGridInterpolator",
                                 # "NearestNDInterpolator",
                                 # "LinearNDInterpolator",
                                 # "CloughTocher2DInterpolator",
                                 # "RBFInterpolator",
                                 "splrep",

                                 ]
            if mode == 1:
                DF_ISP, values_for_Excel = TPDSCF.start_TPDS_CF(dct, name, "PchipInterpolator")
            if mode == 2:
                if name != "graph0":
                    DF_ISP, values_for_Excel = TPDSCF.start_TPDS_CF(dct, name, "PchipInterpolator")
                else:
                    DF_ISP, values_for_Excel = TPDS50.start_TPDS_E50(dct, name, "PchipInterpolator")

            if mode == 3:
                DF_ISP, values_for_Excel = TPDSRZG50.start_TPDS_RZG(dct, name, "PchipInterpolator")
                if name != "graph0":
                    DF_ISP, values_for_Excel = TPDSCF.start_TPDS_CF(dct, name, "PchipInterpolator")

            if mode == 1:
                if name == "graph1":
                    values_for_Excel_right = values_for_Excel
            else:
                if name == "graph0":
                    values_for_Excel_right = values_for_Excel

            save_DF.append(DF_ISP)

            print(f"{row}--{LAB_NO}--{name}--------DONE")

        if mode == 1:
            read_shablons.shablonExcel_TPS_CD(row, save_DF, dct, organise_dct, values_for_Excel_right)
        else:
            read_shablons.shablonExcel_TPS_CD_4(row, save_DF, dct, organise_dct, values_for_Excel_right)


    # Графики по срезам КД
    if str(worksheet_journal['fi'][row]) not in ["None", "nan"]:

        # Список для сохранения датафреймов, которые возвращаются из TPDS
        save_DF = []

        pathSave = os.path.join(pathSave, 'Cрезы КД')
        if not os.path.exists(pathSave):
            os.mkdir(pathSave)

        F = worksheet_journal['fi'][row]
        C = worksheet_journal['c'][row]

        press, pressStart1, pressStart2, pressStart3 = main_tools.calculate_press_gost("SPS", F, C, organise_dct)

        countPoint = 200
        endE1 = 8

        Rad = math.radians(F)

        valueRANDOM_to_press2 = random.choice([x for x in [random.randint(-2, 2) / 100 for x in range(5)] if x != 0.0])

        pressEnd1 = (pressStart1 * math.tan(Rad) + C) - valueRANDOM_to_press2 / 2
        pressEnd2 = (pressStart2 * math.tan(Rad) + C) + valueRANDOM_to_press2
        pressEnd3 = (pressStart3 * math.tan(Rad) + C) - valueRANDOM_to_press2 / 2

        # math.tan(Rad)
        # math.tan(Rad)
        # math.tan(Rad)
        tan_RAD_F = ((3 * (pressStart1 * pressEnd1 + pressStart2 * pressEnd2 + pressStart3 * pressEnd3) -
                      (pressStart1 + pressStart2 + pressStart3) * (pressEnd1 + pressEnd2 + pressEnd3))
                     /
                     (3 * (pressStart1 ** 2 + pressStart2 ** 2 + pressStart3 ** 2) - (
                                 pressStart1 + pressStart2 + pressStart3) ** 2))
        F_CALC = math.degrees(math.atan(tan_RAD_F))

        namesISP = ["graph1", "graph2", "graph3"]
        pressStarts = [pressStart1, pressStart2, pressStart3]
        pressEnds = [pressEnd1, pressEnd2, pressEnd3]

        for name, pressStart, pressEnd in zip(namesISP, pressStarts, pressEnds):
            dct = {'pressStart': pressStart,
                   'pressStart1': pressStart1,
                   'pressStart2': pressStart2,
                   'pressStart3': pressStart3,
                   'F': F,
                   'C': C,
                   'countPoint': countPoint,
                   'endE1': endE1,
                   'pressEnd1': pressEnd1,
                   'pressEnd2': pressEnd2,
                   'pressEnd3': pressEnd3,
                   'pressEnd': pressEnd,
                   'pathSave': pathSave,
                   }

            typeINTERPOLATION = ["interp1d",
                                 "CubicSpline",
                                 "PchipInterpolator", # очень неплохо
                                 "Akima1DInterpolator", # неплохо
                                 "BarycentricInterpolator",
                                 "KroghInterpolator",
                                 "make_interp_spline", # что-то в этом есть
                                 "interp1d", # плоская залупа
                                 # "RegularGridInterpolator",
                                 # "NearestNDInterpolator",
                                 # "LinearNDInterpolator",
                                 # "CloughTocher2DInterpolator",
                                 # "RBFInterpolator",
                                 "splrep",
                                 ]

            NewDF, values_for_Excel_right = SPS.start_SPS_CD(dct, name, "PchipInterpolator")

            save_DF.append(NewDF)

        read_shablons.shablonExcel_SPS_CD(row, save_DF, dct, organise_dct, values_for_Excel_right)

    # Графики по компрессия КД
    if str(worksheet_journal['Eoed01_02_MPa'][row]) not in ["None", "nan"]:

        pathSave = os.path.join(pathSave, 'Компрессии')
        if not os.path.exists(pathSave):
            os.mkdir(pathSave)

        Eoed01_02_MPa = worksheet_journal['Eoed01_02_MPa'][row]
        Eobs01_02_Mpa = worksheet_journal['Eobs01_02_Mpa'][row]

        dct = {
            'Eoed01_02_MPa': Eoed01_02_MPa,
            'Eobs01_02_Mpa': Eobs01_02_Mpa,

            'pathSave': pathSave,
               }

        NewDF, values_for_Excel = SPD.SPD_start(dct, "main", organise_dct, None)

        read_shablons.shablonExcel_SPD(row, [NewDF], dct, organise_dct, values_for_Excel)




    if rzg and str(worksheet_journal['CD_sigma1'][row]) not in ["None", "nan"]:
        # Выбор давлений
        pressStart1 = worksheet_journal['CD_sigma1'][row]
        pressStart2 = worksheet_journal['CD_sigma2'][row]
        pressStart3 = worksheet_journal['CD_sigma3'][row]

        # Выбор значений механики
        E_0 = worksheet_journal['CD_E0'][row]
        E_50 = worksheet_journal['E50'][row]
        F = worksheet_journal['CD_fi'][row]
        C = worksheet_journal['CD_c'][row]

        pathSave = os.path.join(pathSave, 'Трехосные_КД_ПП')
        if not os.path.exists(pathSave):
            os.mkdir(pathSave)

        # Расчет для графиков по трем значениям
        press16 = pressStart1 * 1.6
        countPoint = 200
        endE1 = 11.4

        N = 2 * math.tan(math.pi * F / 180) * (
                (((math.tan(math.pi * F / 180)) ** 2) + 1) ** (1 / 2)) + 2 * (
                    (math.tan(math.pi * F / 180)) ** 2) + 1
        M = 2 * (N ** (1 / 2)) * C
        pressEnd1 = (pressStart1 * N + M)
        pressEnd2 = pressStart2 * (
                2 * math.tan(math.pi * F / 180) * ((((math.tan(math.pi * F / 180)) ** 2) + 1) ** (1 / 2)) + 2 * (
                (math.tan(math.pi * F / 180)) ** 2) + 1) + (2 * ((2 * math.tan(math.pi * F / 180) * (
                (((math.tan(math.pi * F / 180)) ** 2) + 1) ** (1 / 2)) + 2 * ((math.tan(
            math.pi * F / 180)) ** 2) + 1) ** (
                                                                         1 / 2)) * C)
        pressEnd3 = (pressStart3 * N + M)

        namesISP = ["graph1", "graph2", "graph3"]
        pressStarts = [pressStart1, pressStart2, pressStart3]
        pressEnds = [pressEnd1, pressEnd2, pressEnd3]

        for name, pressStart, pressEnd in zip(namesISP, pressStarts, pressEnds):
            dct = {'pressStart': pressStart,
                   'pressStart1': pressStart1,
                   'pressStart2': pressStart2,
                   'pressStart3': pressStart3,
                   'E_0': E_0,
                   'E_50': E_50,
                   'F': F,
                   'C': C,
                   'countPoint': countPoint,
                   'endE1': endE1,
                   'pressEnd1': pressEnd1,
                   'pressEnd2': pressEnd2,
                   'pressEnd3': pressEnd3,
                   'pressEnd': pressEnd,
                   'pathSave': pathSave,
                   }

            typeINTERPOLATION = ["interp1d",
                                 "CubicSpline",
                                 "PchipInterpolator",  # очень неплохо
                                 "Akima1DInterpolator",  # неплохо
                                 "BarycentricInterpolator",
                                 "KroghInterpolator",
                                 "make_interp_spline",  # что-то в этом есть
                                 "interp1d",  # плоская залупа
                                 # "RegularGridInterpolator",
                                 # "NearestNDInterpolator",
                                 # "LinearNDInterpolator",
                                 # "CloughTocher2DInterpolator",
                                 # "RBFInterpolator",
                                 "splrep",
                                 ]

            DF_ISP, values_for_Excel = TPDSRZG.start_TPDS_RZG(dct, name, "PchipInterpolator")

            if name == "graph1":
                values_for_Excel_right = values_for_Excel

            save_DF.append(DF_ISP)

            print(f"{row}--{LAB_NO}--{name}--------DONE")

        read_shablons.shablonExcel_TPS_CD(row, save_DF, dct, organise_dct, values_for_Excel_right)



    # Графики по компрессия КД
    if str(worksheet_journal['ocr'][row]) not in ["None", "nan"]:

        pathSave = os.path.join(pathSave, 'OCR')
        if not os.path.exists(pathSave):
            os.mkdir(pathSave)

        OCR = worksheet_journal['ocr'][row]
        effective_press = worksheet_journal['P1'][row]
        Eoed01_02_MPa = worksheet_journal['Eoed01_02_MPa'][row]
        Eobs01_02_Mpa = worksheet_journal['Eobs01_02_Mpa'][row]

        dct = {
            'OCR': OCR,
            'effective_press': effective_press,
            'pathSave': pathSave,
            'Eoed01_02_MPa': Eoed01_02_MPa,
            'Eobs01_02_Mpa': Eobs01_02_Mpa,
        }

        # Версия с модулем (модуль ловится, но график не очень)
        # ewDF, values_for_Excel = OCR_ISP.OCR_start_Eoed(dct, "main", organise_dct, None)
        # Версия без модуля
        NewDF, values_for_Excel = OCR_ISP.OCR_start(dct, "main", organise_dct, None)

        read_shablons.shablonExcel_OCR(row, [NewDF], dct, organise_dct, values_for_Excel)

    print(f"{LAB_NO} -- DONE \n")
    print()
