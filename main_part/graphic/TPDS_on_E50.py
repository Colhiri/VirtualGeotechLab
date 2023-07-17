import math
import random
import sys


import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy import interpolate
import scipy.stats as stats

from GEOF.main_part.graphic.combination import AnalyzeGraph

"""
TPD, где последняя точка расчитывается исходя из модуля Е50 и нахождения его на вертикальном значении 
относительной деформации 

Не подходит для включения в прочность, так как точка разрушения не соответствует значению С и Ф

Всегда ищет модуль на точке 1.6 от бытового давления (Теперь уже иногда от 1.3 или от 1.15

Их надо будет смотреть, но в приоритете GUI комбинации
"""


# Функция ближайщего соседа
def nearest(lst, target):
    try:
        pressMAX = lst.tolist().index(max(lst))
    except:
        pressMAX = lst.index(max(lst))
    return min(lst[:pressMAX], key=lambda x: abs(x - target))


def combination(differencePress, dct_Combination: dict):

    # можно передавать конечные значения, котоые не включают в себя значения с других графиков
    y_press16 = dct_Combination.get("y_press16")
    y_pressE50 = dct_Combination.get("y_pressE50")
    endE1 = dct_Combination.get("endE1")

    pressStart1 = dct_Combination.get("pressStart1")
    press16 = dct_Combination.get("press16")
    pressE50 = dct_Combination.get("pressE50")
    pressEnd1 = dct_Combination.get("pressEnd1")

    analyze = AnalyzeGraph("test_1")
    analyze.get_first_data()
    analyze.calculate_perc()
    return analyze.points_reload([pressStart1, press16, pressE50, pressEnd1], [0, y_press16, y_pressE50])


def start_TPDS_E50(dct: dict, name: str, methodINTERPOLATION):

    # Выбор значений механики
    E_0 = dct.get("E_0")
    E_50 = dct.get("E_50")
    F = dct.get("F")
    C = dct.get("C")
    countPoint = dct.get("countPoint")

    endE1 = dct.get("endE1")
    stepE1 = endE1 / countPoint


    # Выбор давлений
    pressStart1 = dct.get("pressStart")
    otn_pStart = 0

    # Расчет E1 и относительных вертикальных деформаций
    press16 = pressStart1 * 1.6
    otn_p16 = (press16 - pressStart1 + E_0 * otn_pStart) / E_0
    y_press16 = 76 * otn_p16 - otn_p16 * stepE1

    # pressEnd1 = dct.get("pressEnd")

    ### Разница для расчёта коэффициента отклонения давления в функции комбинации
    differencePress = (press16 - pressStart1) / 5

    otn_E50 = otn_p16 * 3
    pressEnd1 = pressStart1 + 2 * E_50 * otn_E50 - 2 * E_50 * otn_pStart
    pressE50 = (pressEnd1 - pressStart1) / 2 + pressStart1
    y_pressE50 = 76 * otn_E50 - otn_E50 * stepE1

    max_epsila_otn = 2.5 / (76 - 1 * stepE1)

    res = stats.linregress([press16, pressE50], [otn_p16, otn_E50])
    otn_END_NOW = pressEnd1 * res.slope + res.intercept


    if otn_END_NOW > max_epsila_otn:
        press16 = pressStart1 * 1.3
        otn_p16 = (press16 - pressStart1 + E_0 * otn_pStart) / E_0
        y_press16 = 76 * otn_p16 - otn_p16 * stepE1

        otn_E50 = otn_p16 * 3
        pressEnd1 = pressStart1 + 2 * E_50 * otn_E50 - 2 * E_50 * otn_pStart
        pressE50 = (pressEnd1 - pressStart1) / 2 + pressStart1
        y_pressE50 = 76 * otn_E50 - otn_E50 * stepE1

        max_epsila_otn = 2.5 / (76 - 1 * stepE1)

        res = stats.linregress([press16, pressE50], [otn_p16, otn_E50])
        otn_END_NOW = pressEnd1 * res.slope + res.intercept

        if otn_END_NOW > max_epsila_otn:

            press16 = pressStart1 * 1.15
            otn_p16 = (press16 - pressStart1 + E_0 * otn_pStart) / E_0
            y_press16 = 76 * otn_p16 - otn_p16 * stepE1

            otn_E50 = otn_p16 * 3
            pressEnd1 = pressStart1 + 2 * E_50 * otn_E50 - 2 * E_50 * otn_pStart
            pressE50 = (pressEnd1 - pressStart1) / 2 + pressStart1
            y_pressE50 = 76 * otn_E50 - otn_E50 * stepE1


    pressEnd1 = 2 * pressE50 - pressStart1

    """
    "gravel"
    "sand"
    "sandy_loam"
    "loam"
    "clay"
    """
    typeGrunt = "sandy_loam"
    # Словарь для передачи в функцию комбинации
    dct_Combination = {
    "y_press16": y_press16,
    "y_pressE50": y_pressE50,
    "endE1": endE1,


    "pressStart1": pressStart1,
    "press16": press16,
    "pressE50": pressE50,
    "pressEnd1": pressEnd1,
    }

    # Списки контрольных точек
    if typeGrunt == "gravel":
        y = np.array([0.0, y_press16, y_pressE50, 3.6, 5.7, endE1])
        x = np.array([pressStart1, press16, pressE50, pressEnd1, pressEnd1 - 0.01, pressEnd1 - 0.011])
    if typeGrunt == "sand":
        y = np.array([0.0, y_press16, y_pressE50, 3.6, 5.7, endE1])
        x = np.array([pressStart1, press16, pressE50, pressEnd1, pressEnd1 - 0.01, pressEnd1 - 0.011])

    if typeGrunt == "sandy_loam":
        choice = random.choice([2])
        x, y = combination(differencePress, dct_Combination)

    if typeGrunt == "loam":
        choice = random.choice([1, 2, 3])
        x, y = combination(differencePress, dct_Combination)

    if typeGrunt == "clay":
        choice = random.choice([1, 2])
        x, y = combination(differencePress, dct_Combination)

    # Значения по E1 (Y)
    yfit = np.linspace(min(y), max(y), num=countPoint)

    #### Здесь меняются разные типы интерполяций

    try:
        if methodINTERPOLATION == "interp1d":
            pchip = interpolate.interp1d(y, x, kind='linear')

        if methodINTERPOLATION == "CubicSpline":
            pchip = interpolate.CubicSpline(y, x)

        if methodINTERPOLATION == "PchipInterpolator":
            pchip = interpolate.PchipInterpolator(y, x)

        if methodINTERPOLATION == "Akima1DInterpolator":
            pchip = interpolate.Akima1DInterpolator(y, x)

        if methodINTERPOLATION == "BarycentricInterpolator":
            pchip = interpolate.BarycentricInterpolator(y, x)

        if methodINTERPOLATION == "KroghInterpolator":
            pchip = interpolate.KroghInterpolator(y, x)

        if methodINTERPOLATION == "make_interp_spline":
            pchip = interpolate.make_interp_spline(y, x)

        if methodINTERPOLATION == "nearest":
            pchip = interpolate.interp1d(y, x, kind='nearest')

        if methodINTERPOLATION == "quadratic":
            pchip = interpolate.interp1d(y, x, kind='quadratic')

        if methodINTERPOLATION == "cubic":
            pchip = interpolate.interp1d(y, x, kind='cubic')

    except:
        return start_TPDS_E50(dct, name, methodINTERPOLATION)

    xnew = pchip(yfit)


    # Вставка значений по найденному индексу приближенного значения для нахождения модулей для E0, E50, pressMax
    index_x_E_0 = xnew.tolist().index(nearest(xnew, press16))
    index_x_E_50 = xnew.tolist().index(nearest(xnew, pressE50))
    index_x_pressMax = xnew.tolist().index(nearest(xnew, pressEnd1))

    index_y_E_0 = yfit.tolist().index(nearest(yfit, y_press16))
    index_y_E_50 = yfit.tolist().index(nearest(yfit, y_pressE50))
    index_y_pressMax = yfit.tolist().index(nearest(yfit, endE1))

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
        valueRandom = random.randint(0, int((pressEnd1 - pressStart1) * 100)) / 1000
        if xnew[count] - valueRandom <= 0:
            continue
        xnew[count] = xnew[count] - valueRandom

    # Кривая для датафрейма и дапма файла (Девиаторное нагружение - Относительная вертикальная деформация)
    otnVertDef = yfit / 76
    deviator = [x - pressStart1 for x in xnew]

    curve1 = np.array([(x, y) for x, y in zip(deviator, otnVertDef)])

    NewDF = pd.DataFrame(curve1)
    NewDF.reset_index(drop=True, inplace=True)

    # Построение графика
    # plt.plot(x, y, '.')
    # plt.plot(xnew, yfit)
    # plt.grid()
    # plt.show()

    values_for_Excel = {"epsE0": otnVertDef[index_y_E_0],
                        "epsE50": otnVertDef[index_y_E_50],
                        "epsMAX": otnVertDef[index_x_pressMax],

                        "devE0": deviator[index_y_E_0],
                        "devE50": deviator[index_y_E_50],
                        "devMAX": deviator[index_x_pressMax]}

    return NewDF, values_for_Excel
