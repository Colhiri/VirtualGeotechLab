import math
import random

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy import interpolate

"""
Прочность для добавления на трех графиках с отсутствием возможности находить модуль (или его рандомности).

Используется для совмещения с скриптом TPDS_on_E50

"""

# Функция ближайщего соседа
def nearest(lst, target):
    try:
        pressMAX = lst.tolist().index(max(lst))
    except:
        pressMAX = lst.index(max(lst))
    return min(lst[:pressMAX], key=lambda x: abs(x - target))

def combination(choice, differencePress, dct_Combination: dict):

    # можно передавать конечные значения, котоые не включают в себя значения с других графиков
    y_press16 = dct_Combination.get("y_press16")
    y_pressE50 = dct_Combination.get("y_pressE50")
    endE1 = dct_Combination.get("endE1")

    pressStart1 = dct_Combination.get("pressStart1")
    press16 = dct_Combination.get("press16")
    pressE50 = dct_Combination.get("pressE50")
    pressEnd1 = dct_Combination.get("pressEnd1")

    # Первая комбинация без хвостов
    y_1 = np.array([0.0, y_press16, y_pressE50, endE1])
    x_1 = np.array([pressStart1, press16, pressE50, pressEnd1])

    y_2, x_2 = [], []
    if choice == 2:
        while not len(y_2) and not len(x_2):
            try:
                # Вторая комбинация
                handle_y1 = random.randint(int(round(y_pressE50 + 1, 2) * 100),
                                       int(round(endE1 - 2, 2) * 100)) / 100
                handle_x1 = random.randint(int(round(pressE50 + differencePress, 3) * 1000),
                                       int(round(pressEnd1 - differencePress, 3) * 1000)) / 1000

                y_2 = np.array([0.0, y_press16, y_pressE50, handle_y1, endE1])
                x_2 = np.array([pressStart1, press16, pressE50, pressEnd1, handle_x1])
            except:
                continue

    y_3, x_3 = [], []
    if choice == 3:
        while not len(y_3) and not len(x_3):
            try:
                #  Третья комбинация
                handle_y1 = random.randint(int(round(y_pressE50 + 2, 2) * 100),
                                       int(round((endE1 - y_pressE50) / 2 + y_pressE50, 2) * 100)) / 100
                handle_x1 = random.randint(int(round(pressE50 + differencePress, 3) * 1000),
                                       int(round((pressEnd1 - pressE50) / 2 + pressE50, 3) * 1000)) / 1000

                handle_y2 = random.randint(int(round(handle_y1 + 1, 2) * 100),
                                       int(round(endE1 - 2, 1) * 100)) / 100
                handle_x2 = random.randint(int(round(press16 + differencePress, 3) * 1000),
                                       int(round(handle_x1 - differencePress, 3) * 1000)) / 1000

                y_3 = np.array([0.0, y_press16, y_pressE50, handle_y1, handle_y2, endE1])
                x_3 = np.array([pressStart1, press16, pressE50, pressEnd1, handle_x1, handle_x2])
            except:
                continue

    y_4, x_4 = [], []
    if choice == 4:
        while not len(y_4) and not len(x_4):
            try:
                # Четвертая комбинация
                handle_y1 = random.randint(int(round(y_pressE50 + 2, 2) * 100),
                                       int(round((endE1 - y_pressE50) / 3 + y_pressE50, 2) * 100)) / 100
                handle_x1 = random.randint(int(round(pressE50 + differencePress, 3) * 1000),
                                       int(round((pressEnd1 - pressE50) / 3 + pressE50, 3) * 1000)) / 1000

                handle_y2 = random.randint(int(round((endE1 - y_pressE50) / 3 + y_pressE50, 2) * 100),
                                       int(round((endE1 - handle_y1) / 2 + handle_y1, 1) * 100)) / 100
                handle_x2 = random.randint(int(round(press16 + differencePress, 3) * 1000),
                                       int(round((pressEnd1 - pressE50) / 3 + pressE50, 3) * 1000)) / 1000

                handle_y3 = random.randint(int(round((endE1 - handle_y1) / 2 + handle_y1, 1) * 100),
                                       int(round(endE1 - 1, 2) * 100)) / 100
                handle_x3 = random.randint(int(round((press16 + differencePress - pressStart1) / 2 + pressStart1, 3) * 1000),
                                       int(round(press16 + differencePress, 3) * 1000)) / 1000

                y_4 = np.array([0.0, y_press16, y_pressE50, handle_y1, handle_y2, handle_y3, endE1])
                x_4 = np.array([pressStart1, press16, pressE50, pressEnd1, handle_x1, handle_x2, handle_x3])

            except:
                continue

    return (x_1, y_1) if choice == 1 \
        else (x_2, y_2) if choice == 2 \
        else (x_3, y_3) if choice == 3 \
        else (x_4, y_4)

def start_TPS(dct: dict, name: str):
    # Выбор давлений
    pressStart1 = dct.get("pressStart")


    # Выбор значений механики
    E_0 = dct.get("E_0")
    E_50 = dct.get("E_50")


    countPoint = dct.get("countPoint")
    endE1 = dct.get("endE1")

    stepE1 = endE1 / countPoint

    pressEnd1 = dct.get("pressEnd")





    press16 = pressStart1 + (pressEnd1 - pressStart1) / 2



    ### Разница для расчёта коэффициента отклонения давления в функции комбинации
    differencePress = (press16 - pressStart1) / 5


    # Расчет E1 и относительных вертикальных деформаций
    otn_pStart = 0

    otn_p16 = random.randint(3, 10) / 1000
    y_press16 = 76 * otn_p16 - otn_p16 * stepE1

    pressE50 = press16 + 0.001
    otn_E50 = otn_p16 + 0.001
    y_pressE50 = 76 * otn_E50 - otn_E50 * stepE1

    """
    "gravel"
    "sand"
    "sandy_loam"
    "loam"
    "clay"
    """

    ####
    ####
    ####
    ####
    ####
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
        choice = random.choice([2, 3, 4])
        print(choice)
        x, y = combination(choice, differencePress, dct_Combination)

    if typeGrunt == "loam":
        choice = random.choice([1, 2, 3])
        print(choice)
        x, y = combination(choice, differencePress, dct_Combination)

    if typeGrunt == "clay":
        choice = random.choice([1, 2])
        print(choice)
        x, y = combination(choice, differencePress, dct_Combination)

    # Значения по E1 (Y)
    yfit = np.linspace(min(y), max(y), num=countPoint)
    try:
        pchip = interpolate.PchipInterpolator(y, x)
    except:
        return start_TPS(dct, name)

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
    yfit[index_y_pressMax] = endE1

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

    print(f"E0 -- {deviator[index_y_E_0]} -- {otnVertDef[index_y_E_0]}")
    print(f"E50 -- {deviator[index_y_E_50]} -- {otnVertDef[index_y_E_50]}")

    NewDF = pd.DataFrame(curve1)
    NewDF.reset_index(drop=True, inplace=True)



    values_for_Excel = {"epsE0": otnVertDef[index_y_E_0],
                        "epsE50": otnVertDef[index_y_E_50],
                        "epsMAX": otnVertDef[index_x_pressMax],

                        "devE0": deviator[index_y_E_0],
                        "devE50": deviator[index_y_E_50],
                        "devMAX": deviator[index_x_pressMax]}

    return NewDF, values_for_Excel

