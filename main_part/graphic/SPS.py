import math
import random

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy import interpolate

# Функция ближайщего соседа
def nearest(lst, target):
    try:
        pressMAX = lst.tolist().index(max(lst))
    except:
        pressMAX = lst.index(max(lst))
    return min(lst[:pressMAX], key=lambda x: abs(x - target))


def combination(choice, differencePress, dct_Combination: dict):

    # можно передавать конечные значения, котоые не включают в себя значения с других графиков
    endE1 = dct_Combination.get("endE1")

    pressStart1 = dct_Combination.get("pressStart1")

    pressEnd1 = dct_Combination.get("pressEnd1")



    y_1, x_1 = [], []
    if choice == 1:
        while not len(y_1) and not len(x_1):
            try:
                # Первая комбинация
                handle_y1 = random.randint(20, 60) / 10 # Макс точка
                handle_x1 = (1 - random.randint(3, 15) / 100) * pressEnd1

                y_1 = np.array([0.0, handle_y1, endE1])
                x_1 = np.array([0.0, pressEnd1, handle_x1])
                pass

            except:
                continue



    y_2, x_2 = [], []
    if choice == 2:
        while not len(y_2) and not len(x_2):
            try:
                # Вторая комбинация
                handle_y1 = random.randint(20, 50) / 10 # Макс точка
                handle_x1 = (1 - random.randint(2, 7) / 100) * pressEnd1

                handle_y2 = handle_y1 + random.randint(10, 20) / 10
                handle_x2 = (1 - random.randint(8, 15) / 100) * pressEnd1

                y_2 = np.array([0.0, handle_y1, handle_y2, endE1])
                x_2 = np.array([0.0, pressEnd1, handle_x1, handle_x2])

            except:
                continue



    y_3, x_3 = [], []
    if choice == 3:
        while not len(y_3) and not len(x_3):
            try:
                #  Третья комбинация
                handle_y1 = random.randint(30, 60) / 10 # Макс точка
                handle_x1 = (1 - random.randint(20, 30) / 100) * pressEnd1

                handle_y2 = random.randint(10, 20) / 10
                handle_x2 = (1 - random.randint(2, 10) / 100) * pressEnd1

                y_3 = np.array([0.0, handle_y2, handle_y1, endE1])
                x_3 = np.array([0.0, handle_x1, pressEnd1, handle_x2])

            except:
                continue



    y_4, x_4 = [], []
    if choice == 4:
        while not len(y_4) and not len(x_4):
            try:
                # Четвертая комбинация
                handle_y1 = random.randint(30, 50) / 10  # Макс точка
                handle_x1 = (1 - random.randint(20, 30) / 100) * pressEnd1

                handle_y2 = random.randint(10, 20) / 10
                handle_x2 = (1 - random.randint(2, 10) / 100) * pressEnd1

                handle_y3 = random.randint(55, 70) / 10
                handle_x3 = (1 + random.randint(1, 6) / 100) * handle_x2

                y_4 = np.array([0.0, handle_y2, handle_y1, handle_y3, endE1])
                x_4 = np.array([0.0, handle_x1, pressEnd1, handle_x3, handle_x2])

            except:
                continue

    return (x_1, y_1) if choice == 1 \
        else (x_2, y_2) if choice == 2 \
        else (x_3, y_3) if choice == 3 \
        else (x_4, y_4)

def start_SPS_CD(dct: dict, name: str, methodINTERPOLATION):

    F = dct.get("F")
    C = dct.get("C")
    countPoint = dct.get("countPoint")
    endE1 = dct.get("endE1")
    stepE1 = endE1 / countPoint

    pressStart1 = dct.get("pressStart")
    pressEnd1 = dct.get("pressEnd")



    y_press33 = random.randint(55, 75) / 10
    y_press66 = random.randint(30, 50) / 10


    press33 = pressEnd1 - random.randint(3, 8) / 1000
    press66 = pressEnd1 - random.randint(3, 8) / 1000 # (pressEnd1) * (random.randint(70, 85) / 100)



    # Выделение возможной максимальной разницы между точками
    # (что если сделать ее процентной, она ведь будет просто пропорционально
    # увеличиваться в соответствии с увеличением давления)
    differencePress = pressEnd1 / 100
    typeGrunt = "sandy_loam"
    dct_Combination = {
        "pressStart1": pressStart1,
        "endE1": endE1,
        "pressEnd1": pressEnd1,
    }

    # Контрольные точки
    # Контрольные точки
    # Контрольные точки
    # Контрольные точки
    # Списки контрольных точек
    if typeGrunt == "gravel":
        y = np.array([0.0, y_press66, y_press33, endE1])
        x = np.array([0.0, pressEnd1, press33, press66, ])

    if typeGrunt == "sand":
        y = np.array([0.0, y_press66, y_press33, endE1])
        x = np.array([0.0, pressEnd1, press33, press66, ])

    if typeGrunt == "sandy_loam":
        choice = 4  # random.choice([2, 3, 4])
        x, y = combination(choice, differencePress, dct_Combination)

    if typeGrunt == "loam":
        choice = random.choice([1, 2, 3])
        x, y = combination(choice, differencePress, dct_Combination)

    if typeGrunt == "clay":
        choice = random.choice([1, 2])
        x, y = combination(choice, differencePress, dct_Combination)







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
        return start_SPS_CD(dct, name, methodINTERPOLATION)

    xnew = pchip(yfit)

    index_x = xnew.tolist().index(nearest(xnew, pressEnd1))
    xnew[index_x] = pressEnd1


    # Рандом для значений, исключая те, которые являются необходимыми для расчетов необходимых парамтров
    for count, x_value in enumerate(xnew, 0):
        if count in (0, index_x):
            continue
        valueRandom = random.randint(0, int(pressEnd1 * 100)) / 2000
        if xnew[count] - valueRandom <= 0:
            continue
        xnew[count] = xnew[count] - valueRandom

    # Дамп в csv
    curve1 = np.array([(x, y) for x, y in zip(xnew, yfit)])

    NewDF = pd.DataFrame(curve1)
    NewDF.reset_index(drop=True, inplace=True)

    # Построение графика
    # plt.plot(y, x, '.')
    # plt.plot(yfit, xnew)
    # plt.grid()
    # plt.show()

    values_for_Excel = {}

    return NewDF, values_for_Excel