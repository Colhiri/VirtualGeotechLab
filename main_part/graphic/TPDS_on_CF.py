import math
import random

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy import interpolate
from scipy.stats import stats

from GEOF.main_part.graphic.combination import AnalyzeGraph


# Функция ближайщего соседа
def nearest(lst, target):
    try:
        pressMAX = lst.tolist().index(max(lst))
    except:
        pressMAX = lst.index(max(lst))
    return min(lst[:pressMAX], key=lambda x: abs(x - target))

def start_TPDS_CF(name: str, data_mech: dict, organise_dct, dct_combination: dict, type_grunt_schemas: dict):

    # Выбор давлений
    pressStart1 = data_mech.get("pressStart")
    press16 = pressStart1 * 1.6
    otn_pStart = 0

    name = data_mech.get('name')
    if name == 'graph1' or name == 'graph0':
        E_0 = data_mech.get("E_0")
        E_50 = data_mech.get("E_50")

    if name == 'graph2':
        random_press = (data_mech.get("pressStart") / data_mech.get("pressStart1")) * random.randint(90, 110) / 100
        E_0 = data_mech.get("E_0") * random_press
        E_50 = data_mech.get("E_50") * random_press

    if name == 'graph3':
        random_press = (data_mech.get("pressStart") / data_mech.get("pressStart1")) * random.randint(90, 110) / 100

        E_0 = data_mech.get("E_0") * random_press
        E_50 = data_mech.get("E_50") * random_press

    F = data_mech.get("F")
    C = data_mech.get("C")
    countPoint = data_mech.get("countPoint")
    endE1 = data_mech.get("endE1")
    stepE1 = endE1 / countPoint
    pressEnd1 = data_mech.get("pressEnd")

    ### Разница для расчёта коэффициента отклонения давления в функции комбинации
    differencePress = (press16 - pressStart1) / 5

    # Расчет E1 и относительных вертикальных деформаций
    press16 = pressStart1 * 1.6
    otn_p16 = (press16 - pressStart1 + E_0 * otn_pStart) / E_0
    y_press16 = 76 * otn_p16 - otn_p16 * stepE1

    pressE50 = (pressEnd1 - pressStart1) / 2 + pressStart1
    otn_E50 = (pressE50 - pressStart1 + E_50 * otn_pStart) / E_50 # otn_p16 * 3
    y_pressE50 = 76 * otn_E50 - otn_E50 * stepE1

    max_epsila_otn = 2.5 / (76 - 1 * stepE1)

    res = stats.linregress([press16, pressE50], [otn_p16, otn_E50])
    otn_END_NOW = pressEnd1 * res.slope + res.intercept

    if (otn_END_NOW > max_epsila_otn or press16 > pressE50) and pressE50 < pressEnd1:
        press16 = pressStart1 * 1.3
        otn_p16 = (press16 - pressStart1 + E_0 * otn_pStart) / E_0
        y_press16 = 76 * otn_p16 - otn_p16 * stepE1

        res = stats.linregress([press16, pressE50], [otn_p16, otn_E50])
        otn_END_NOW = pressEnd1 * res.slope + res.intercept

        if (otn_END_NOW > max_epsila_otn or press16 > pressE50) and pressE50 < pressEnd1:
            press16 = pressStart1 * 1.15
            otn_p16 = (press16 - pressStart1 + E_0 * otn_pStart) / E_0
            y_press16 = 76 * otn_p16 - otn_p16 * stepE1

            if press16 > pressE50:
                press16 = pressStart1 * 1.075
                otn_p16 = (press16 - pressStart1 + E_0 * otn_pStart) / E_0
                y_press16 = 76 * otn_p16 - otn_p16 * stepE1

    if ((press16 - pressStart1) / (pressE50 - pressStart1)) * 100 > 60:
        press16 = (pressE50 - pressStart1) * (random.randint(40, 60) / 100) + pressStart1
        otn_p16 = (press16 - pressStart1 + E_0 * otn_pStart) / E_0
        y_press16 = 76 * otn_p16 - otn_p16 * stepE1

    # Словарь для передачи в функцию комбинации
    control_point = {
    "y_press16": y_press16,
    "y_pressE50": y_pressE50,
    "endE1": endE1,

    "pressStart1": pressStart1,
    "press16": press16,
    "pressE50": pressE50,
    "pressEnd1": pressEnd1,
    }

    analyze = AnalyzeGraph(organise_values=organise_dct,
                           control_points=control_point,
                           data=dct_combination,
                           type_grunt_dct=type_grunt_schemas)
    analyze.calculate_perc()
    analyze.points_reload()
    xnew, yfit = analyze.interpolation()

    # Вставка значений по найденному индексу приближенного значения для нахождения модулей для E0, E50, pressMax
    index_x_E_0 = xnew.index(nearest(xnew, press16))
    index_x_E_50 = xnew.index(nearest(xnew, pressE50))
    index_x_pressMax = xnew.index(nearest(xnew, pressEnd1))

    index_y_E_0 = yfit.index(nearest(yfit, y_press16))
    index_y_E_50 = yfit.index(nearest(yfit, y_pressE50))
    index_y_pressMax = yfit.index(nearest(yfit, endE1))

    yfit[index_y_E_0] = y_press16
    yfit[index_y_E_50] = y_pressE50
    # yfit[index_y_pressMax] = endE1

    xnew[index_y_E_0] = press16
    xnew[index_y_E_50] = pressE50
    xnew[index_x_pressMax] = pressEnd1

    # Рандом для значений, исключая те, которые являются необходимыми для расчетов необходимых парамтров
    for count, x_value in enumerate(xnew, 0):
        if count in (0, index_x_E_0, index_x_E_50, index_x_pressMax, index_y_E_0, index_y_E_50, index_y_pressMax):
            continue
        valueRandom = random.randint(0, int((pressEnd1 - pressStart1) * 100)) / 10000
        if xnew[count] - valueRandom <= 0:
            continue
        xnew[count] = xnew[count] - valueRandom

    # Кривая для датафрейма и дапма файла (Девиаторное нагружение - Относительная вертикальная деформация)
    otnVertDef = [value / 76 for value in yfit]
    deviator = [x - pressStart1 for x in xnew]

    curve1 = np.array([(x, y) for x, y in zip(deviator, otnVertDef)])

    NewDF = pd.DataFrame(curve1)
    NewDF.reset_index(drop=True, inplace=True)

    values_for_Excel = {"epsE0": otnVertDef[index_y_E_0],
                        "epsE50": otnVertDef[index_y_E_50],
                        "epsMAX": otnVertDef[index_x_pressMax],

                        "devE0": deviator[index_y_E_0],
                        "devE50": deviator[index_y_E_50],
                        "devMAX": deviator[index_x_pressMax]}

    return NewDF, values_for_Excel
