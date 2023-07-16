import math
import random

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy import interpolate

from GEOF.main_part.graphic.combination import AnalyzeGraph


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



    analyze = AnalyzeGraph("test")
    analyze.get_first_data()
    analyze.calculate_perc()
    return analyze.points_reload([pressStart1, press16, pressE50, pressEnd1], [0, y_press16, y_pressE50])

def start_TPDS_CF(dct: dict, name: str, methodINTERPOLATION):

    # Выбор давлений
    pressStart1 = dct.get("pressStart")
    press16 = pressStart1 * 1.6


    name = dct.get('name')
    if name == 'graph1' or name == 'graph0':
        E_0 = dct.get("E_0")
        E_50 = dct.get("E_50")
    if name == 'graph2':

        random_press = dct.get("pressStart") / dct.get("pressStart1") * random.randint(90, 110) / 100
        E_0 = dct.get("E_0") * random_press
        E_50 = dct.get("E_50") * random_press
    if name == 'graph3':
        random_press = dct.get("pressStart") / dct.get("pressStart1") * random.randint(90, 110) / 100

        E_0 = dct.get("E_0") * random_press
        E_50 = dct.get("E_50") * random_press


    F = dct.get("F")
    C = dct.get("C")
    countPoint = dct.get("countPoint")
    endE1 = dct.get("endE1")

    stepE1 = endE1 / countPoint

    pressEnd1 = dct.get("pressEnd")


    ## Проверка на максимальное возможное давление второй точки модуля E0 и перерасчет коэффициента домножения
    ## второй точки
    pressMAX_nowE50 = (pressEnd1 + pressStart1) / 2
    if pressMAX_nowE50 <= press16:
        try:
            press16 = random.randint(int(round(pressStart1, 3) * 1000 + 3), int(round(pressMAX_nowE50, 3) * 1000 - 3)) / 1000
        except:
            press16 = random.randint(int(round(pressStart1, 3) * 1000 + 1), int(round(pressMAX_nowE50, 3) * 1000 - 1)) / 1000


    ### Разница для расчёта коэффициента отклонения давления в функции комбинации
    differencePress = (press16 - pressStart1) / 5

    # Расчет E1 и относительных вертикальных деформаций
    otn_pStart = 0

    otn_p16 = (press16 - pressStart1 + E_0 * otn_pStart) / E_0
    y_press16 = 76 * otn_p16 - otn_p16 * stepE1

    pressE50 = (pressEnd1 + pressStart1) / 2
    otn_E50 = (((pressEnd1 + pressStart1) / 2) - pressStart1 + E_50 * otn_pStart) / E_50
    y_pressE50 = 76 * otn_E50 - otn_E50 * stepE1


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
        x, y = combination(differencePress, dct_Combination)

    if typeGrunt == "loam":
        x, y = combination(differencePress, dct_Combination)

    if typeGrunt == "clay":
        x, y = combination(differencePress, dct_Combination)


    # Значения по E1 (Y)
    yfit = np.linspace(min(y), max(y), num=countPoint)



    #### Здесь меняются разные типы интерполяций

    try:
        if methodINTERPOLATION == "interp1d":
            pchip = interpolate.interp1d(y, x, kind='cubic')

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

        if methodINTERPOLATION == "interp1d":
            pchip = interpolate.interp1d(y, x)

        if methodINTERPOLATION == "interp1d":
            pchip = interpolate.interp1d(y, x)

        if methodINTERPOLATION == "splrep":
            # pchip = interpolate.splrep(y, x)

            # x = np.linspace(0, 10, 10)
            x = np.sin(y)
            spl = interpolate.splrep(y, x)
            y2 = np.linspace(0, 10, 200)
            x2 = interpolate.splev(x, y)
            plt.plot(x2, y2)
            plt.show()


        # if methodINTERPOLATION == "RegularGridInterpolator":
        #     pchip = interpolate.RegularGridInterpolator(y, x)

        # if methodINTERPOLATION == "NearestNDInterpolator":
        #     pchip = interpolate.NearestNDInterpolator(x, y)

        # if methodINTERPOLATION == "LinearNDInterpolator":
        #     pchip = interpolate.LinearNDInterpolator(y, x)

        # if methodINTERPOLATION == "CloughTocher2DInterpolator":
        #     pchip = interpolate.CloughTocher2DInterpolator(y, x)

        # if methodINTERPOLATION == "RBFInterpolator":
        #     pchip = interpolate.RBFInterpolator(y, x)
    except:
        return start_TPDS_CF(dct, name, methodINTERPOLATION)

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
        valueRandom = random.randint(0, int((pressEnd1 - pressStart1) * 100)) / 10000
        if xnew[count] - valueRandom <= 0:
            continue
        xnew[count] = xnew[count] - valueRandom

    # Кривая для датафрейма и дапма файла (Девиаторное нагружение - Относительная вертикальная деформация)
    otnVertDef = yfit / 76
    deviator = [x - pressStart1 for x in xnew]

    curve1 = np.array([(x, y) for x, y in zip(deviator, otnVertDef)])

    NewDF = pd.DataFrame(curve1)
    NewDF.reset_index(drop=True, inplace=True)

    # Дамп в csv
    # NewDF.to_csv(fr"C:\Users\MSI GP66\PycharmProjects\dj_project\BEZIER\ENGGEO_program\prot\{name}.log",
    #              sep='\t', index_label=False, index=False, header=False)



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
