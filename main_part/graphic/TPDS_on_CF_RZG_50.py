import math
import random

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy import interpolate
from scipy.stats import stats
from scipy.special import comb

from GEOF.main_part.graphic.combination import AnalyzeGraph

def bernstein_poly(i, n, t):
    """
     The Bernstein polynomial of n, i as a function of t
    """

    return comb(n, i) * ( t**(n-i) ) * (1 - t)**i

def bezier_curve(points, nTimes=1000):
    """
       Given a set of control points, return the
       bezier curve defined by the control points.

       points should be a list of lists, or list of tuples
       such as [ [1,1],
                 [2,3],
                 [4,5], ..[Xn, Yn] ]
        nTimes is the number of time steps, defaults to 1000

        See http://processingjs.nihongoresources.com/bezierinfo/
    """

    nPoints = len(points)
    xPoints = np.array([p[0] for p in points])
    yPoints = np.array([p[1] for p in points])

    t = np.linspace(0.0, 1.0, nTimes)

    polynomial_array = np.array([ bernstein_poly(i, nPoints-1, t) for i in range(0, nPoints)   ])

    xvals = np.dot(xPoints, polynomial_array)
    yvals = np.dot(yPoints, polynomial_array)

    return xvals, yvals
# Функция ближайщего соседа
def nearest(lst, target):
    try:
        pressMAX = lst.tolist().index(max(lst))
    except:
        pressMAX = lst.index(max(lst))
    return min(lst[:pressMAX], key=lambda x: abs(x - target))

def splain(x, y, count_point, methodINTERPOLATION):

    yfit = np.linspace(min(y), max(y), num=count_point)

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

    xnew = pchip(yfit)

    if type(yfit) != list:
        yfit = yfit.tolist()
    if type(xnew) != list:
        xnew = xnew.tolist()

    if type(xnew) == list:
        pass

    return xnew, yfit

def start_TPDS_RZG(name: str, data_mech: dict, organise_dct, dct_combination: dict, type_grunt_schemas: dict):
    # Выбор давлений
    pressStart1 = data_mech.get("pressStart")

    # Выбор значений механики
    E_0 = data_mech.get("E_0")
    E_50 = data_mech.get("E_50")
    F = data_mech.get("F")
    C = data_mech.get("C")
    countPoint = data_mech.get("countPoint")
    endE1 = data_mech.get("endE1")
    stepE1 = endE1 / countPoint

    # Расчет E1 и относительных вертикальных деформаций
    otn_pStart = 0

    press16 = pressStart1 * 1.6
    otn_p16 = (press16 - pressStart1 + E_0 * otn_pStart) / E_0
    y_press16 = 76 * otn_p16 - otn_p16 * stepE1

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

    E_rzg = E_0 * random.randint(45, 60) / 10
    press_rzg = (pressE50 - pressStart1) / 2 + pressE50

    press_rzg_END = press_rzg - 0.0005

    otn_E_RZG = otn_E50 + random.randint(4, 5) / 100
    y_pressR_RZG = 76 * otn_E_RZG - otn_E_RZG * stepE1

    # Стартовое напряжение повторного нагружения
    press_repeat_RZG = pressStart1 + 0.005
    otn_repeat_RZG = (press_repeat_RZG - press_rzg_END) / E_rzg + otn_E_RZG
    y_repeat_RZG = 76 * otn_repeat_RZG - otn_repeat_RZG * stepE1

    # Проверим модуль
    E_rzg_calc = (press_rzg_END - press_repeat_RZG) / (otn_E_RZG - otn_repeat_RZG)

    # Середины петель
    pressRZG_up = (press_rzg - press_repeat_RZG) / 2 + press_repeat_RZG + 0.004
    pressRZG_down = (press_rzg - press_repeat_RZG) / 2 + press_repeat_RZG - 0.004
    y_RZG_up = y_repeat_RZG + 0.2
    y_RZG_down = y_pressR_RZG - 0.2

    # Кривая Безье
    # Кривая Безье
    # Кривая Безье
    xpoints = np.array([press_repeat_RZG, pressRZG_up, press_rzg_END])
    ypoints = np.array([y_repeat_RZG, y_RZG_up, y_pressR_RZG])
    points = np.array([(x, y) for x, y in zip(xpoints, ypoints)])
    low_curve_x, low_curve_y = bezier_curve(points, nTimes=100)

    xpoints = np.array([press_rzg, pressRZG_down, press_repeat_RZG])
    ypoints = np.array([y_pressR_RZG, y_RZG_down, y_repeat_RZG])

    points = np.array([(x, y) for x, y in zip(xpoints, ypoints)])
    high_curve_x, high_curve_y = bezier_curve(points, nTimes=100)
    # Словарь для передачи в функцию комбинации
    control_point = {
        "y_press16": y_press16,
        "y_pressE50": y_pressE50,
        "endE1": endE1,

        "pressStart1": pressStart1,
        "press16": press16,
        "pressE50": pressE50,
        "pressEnd1": pressEnd1,

        "press_rzg_END": press_rzg,
        "y_pressR_RZG": y_pressR_RZG,
    }

    analyze = AnalyzeGraph(organise_values=organise_dct,
                           control_points=control_point,
                           data=dct_combination,
                           type_grunt_dct=type_grunt_schemas)
    analyze.calculate_perc()
    x_end, y_end = analyze.points_reload()

    try:
        x_end = x_end.tolist()
    except AttributeError:
        pass
    try:
        y_end = y_end.tolist()
    except AttributeError:
        pass

    bad_indexes = [3, 2, 1, 0]
    for ind in bad_indexes:
        x_end.pop(ind)
        y_end.pop(ind)


    x_end.insert(0, press_rzg_END)
    y_end.insert(0, y_pressR_RZG)

    fifth_x, fifth_y = splain(x=x_end, y=y_end, count_point=100, methodINTERPOLATION="PchipInterpolator")

    y = np.array(
        [0.0, y_press16, y_pressE50, y_pressR_RZG])
    x = np.array(
        [pressStart1, press16, pressE50, press_rzg])
    xnew, yfit = splain(x, y, 100, 'PchipInterpolator')


    # Вставка значений по найденному индексу приближенного значения для нахождения модулей для E0, E50, pressMax
    index_x_E_0 = xnew.index(nearest(xnew, press16))
    index_x_E_50 = xnew.index(nearest(xnew, pressE50))
    index_x_pressMax = fifth_x.index(nearest(fifth_x, pressEnd1))

    index_y_E_0 = yfit.index(nearest(yfit, y_press16))
    index_y_E_50 = yfit.index(nearest(yfit, y_pressE50))
    index_y_pressMax = fifth_y.index(nearest(fifth_y, endE1))

    yfit[index_y_E_0] = y_press16
    yfit[index_y_E_50] = y_pressE50
    fifth_y[index_y_pressMax] = endE1

    xnew[index_y_E_0] = press16
    xnew[index_y_E_50] = pressE50
    fifth_x[index_x_pressMax] = pressEnd1

    # # Рандом для значений, исключая те, которые являются необходимыми для расчетов необходимых парамтров
    # for count, x_value in enumerate(xnew, 0):
    #     if count in (0, index_x_E_0, index_x_E_50, index_x_pressMax, index_y_E_0, index_y_E_50, index_y_pressMax):
    #         continue
    #     valueRandom = random.randint(0, int((pressEnd1 - pressStart1) * 100)) / 1000
    #     if xnew[count] - valueRandom <= 0:
    #         continue
    #     xnew[count] = xnew[count] - valueRandom

    x = np.concatenate((xnew, low_curve_x, high_curve_x, fifth_x))
    y = np.concatenate((yfit, low_curve_y, high_curve_y, fifth_y))

    # Кривая для датафрейма и дапма файла (Девиаторное нагружение - Относительная вертикальная деформация)
    otnVertDef = y / 76
    deviator = [press - pressStart1 for press in x]

    curve1 = np.array([(x, y) for x, y in zip(deviator, otnVertDef)])

    NewDF = pd.DataFrame(curve1)
    NewDF.reset_index(drop=True, inplace=True)

    # Нужно перестроить словарь так, чтобы он работал с общим шаблоном длля прочности.
    values_for_Excel = {"epsE0": otnVertDef[index_y_E_0],
                        "epsE50": otnVertDef[index_y_E_50],
                        "epsMAX": otnVertDef[index_x_pressMax],

                        "devE0": deviator[index_y_E_0],
                        "devE50": deviator[index_y_E_50],
                        "devMAX": deviator[index_x_pressMax]}

    return NewDF, values_for_Excel
