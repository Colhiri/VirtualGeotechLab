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

def combination(differencePress, dct_Combination: dict):

    # можно передавать конечные значения, котоые не включают в себя значения с других графиков
    y_press16 = dct_Combination.get("y_press16")
    y_pressE50 = dct_Combination.get("y_pressE50")
    endE1 = dct_Combination.get("endE1")

    pressStart1 = dct_Combination.get("pressStart1")
    press16 = dct_Combination.get("press16")
    pressE50 = dct_Combination.get("pressE50")
    pressEnd1 = dct_Combination.get("pressEnd1")

    press_rzg_END = dct_Combination.get("press_rzg_END")
    y_pressR_RZG = dct_Combination.get("y_pressR_RZG")

    analyze = AnalyzeGraph("test_1")
    analyze.get_first_data()
    analyze.calculate_perc('rzg')

    return analyze.points_reload([pressStart1, press16, pressE50, press_rzg_END, pressEnd1], [0, y_press16, y_pressE50, y_pressR_RZG], 'rzg')

def start_TPDS_RZG(dct: dict, name: str, methodINTERPOLATION):
    # Выбор давлений
    pressStart1 = dct.get("pressStart")
    otn_pStart = 0

    # Выбор значений механики
    E_0 = dct.get("E_0")
    E_50 = dct.get("E_50")
    F = dct.get("F")
    C = dct.get("C")
    countPoint = dct.get("countPoint")
    endE1 = dct.get("endE1")
    stepE1 = endE1 / countPoint
    pressEnd1 = dct.get("pressEnd")


    name = dct.get('name')
    if name == 'graph1' or name == 'graph0':
        E_0 = dct.get("E_0")
        E_50 = dct.get("E_50")

    if name == 'graph2':
        random_press = (dct.get("pressStart") / dct.get("pressStart1")) * random.randint(90, 110) / 100
        E_0 = dct.get("E_0") * random_press
        E_50 = dct.get("E_50") * random_press

    if name == 'graph3':
        random_press = (dct.get("pressStart") / dct.get("pressStart1")) * random.randint(90, 110) / 100

        E_0 = dct.get("E_0") * random_press
        E_50 = dct.get("E_50") * random_press

    # Расчет E1 и относительных вертикальных деформаций
    press16 = pressStart1 * 1.6
    otn_p16 = (press16 - pressStart1 + E_0 * otn_pStart) / E_0
    y_press16 = 76 * otn_p16 - otn_p16 * stepE1

    ### Разница для расчёта коэффициента отклонения давления в функции комбинации
    differencePress = (press16 - pressStart1) / 5


    pressE50 = (pressEnd1 - pressStart1) / 2 + pressStart1
    otn_E50 = (pressE50 - pressStart1 + E_50 * otn_pStart) / E_50  # otn_p16 * 3
    y_pressE50 = 76 * otn_E50 - otn_E50 * stepE1


    ### Расчет правильных модулей
    ### Расчет правильных модулей
    ### Расчет правильных модулей

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



    E_rzg = E_0 * random.randint(45,60) / 10
    press_rzg = (pressE50 - pressStart1) / 2 + pressE50

    press_rzg_END = press_rzg - random.randint(1, 2) / 1000

    otn_E_RZG = otn_E50 + random.randint(4, 5) / 100
    y_pressR_RZG = 76 * otn_E_RZG - otn_E_RZG * stepE1

    # Стартовое напряжение повторного нагружения
    press_repeat_RZG = pressStart1 + 0.005
    otn_repeat_RZG = (press_repeat_RZG - press_rzg_END) / E_rzg + otn_E_RZG
    y_repeat_RZG = 76 * otn_repeat_RZG - otn_repeat_RZG * stepE1

    # Проверим модуль
    E_rzg_calc = (press_rzg_END - press_repeat_RZG) / (otn_E_RZG - otn_repeat_RZG)

    print(E_rzg_calc)

    # Середины петель
    pressRZG_up = (press_rzg - press_repeat_RZG) / 2 + press_repeat_RZG + 0.004
    pressRZG_down = (press_rzg - press_repeat_RZG) / 2 + press_repeat_RZG - 0.004
    y_RZG_up = y_repeat_RZG - 0.001
    y_RZG_down = y_pressR_RZG - 0.001

    # первый участок петли (нижняя - первая)
    y_middle_point_first = ((y_pressR_RZG - y_RZG_down) / 2 + y_RZG_down)
    x_middle_point_first = ((press_rzg - pressRZG_down) / 2 + pressRZG_down) * 0.95

    first_y = [y_RZG_down, y_middle_point_first, y_pressR_RZG] # от середины разгрузки первой петли до начала
    first_x = [pressRZG_down, x_middle_point_first, press_rzg] # от середины разгрузки первой петли до начала

    first_x, first_y = splain(x=first_x, y=first_y, count_point=50, methodINTERPOLATION="PchipInterpolator")
    first_y.reverse()
    first_x.reverse()

    # второй участок петли (нижняя - первая)
    y_middle_point_second = ((y_RZG_down - y_repeat_RZG) / 2 + y_repeat_RZG)
    x_middle_point_second = ((pressRZG_down - press_repeat_RZG) / 2 + press_repeat_RZG) * 0.95

    second_y = [y_repeat_RZG, y_middle_point_second, y_RZG_down]  # от конца первой ветви до середины первлй пелтли
    second_x = [press_repeat_RZG, x_middle_point_second, pressRZG_down]  # от конца первой ветви до середины первлй пелтли

    second_x, second_y = splain(x=second_x, y=second_y, count_point=50, methodINTERPOLATION="PchipInterpolator")
    second_y.reverse()
    second_x.reverse()

    # третий участок петли (верхняя - вторая)
    y_middle_point_third = ((y_RZG_up - y_repeat_RZG) / 2 + y_repeat_RZG)
    x_middle_point_third = ((pressRZG_up - press_repeat_RZG) / 2 + press_repeat_RZG) * 1.02

    third_y = [y_repeat_RZG, y_middle_point_third, y_RZG_up]  # от конца первой ветви до середины второй петли
    third_x = [press_repeat_RZG, x_middle_point_third, pressRZG_up]  # от конца первой ветви до середины второй петли
    third_y.reverse()

    third_x, third_y = splain(x=third_x, y=third_y, count_point=50, methodINTERPOLATION="PchipInterpolator")

    # четвертый участок петли (верхняя - вторая)
    y_middle_point_foufth = ((y_pressR_RZG - y_RZG_up) / 2 + y_RZG_up)
    x_middle_point_foufth = ((press_rzg_END - pressRZG_up) / 2 + pressRZG_up) * 1.02

    foufth_y = [y_RZG_up, y_middle_point_foufth, y_pressR_RZG]  # от середины второй петли до конца
    foufth_x = [pressRZG_up, x_middle_point_foufth, press_rzg_END]  # от середины второй петли до конца

    foufth_x, foufth_y = splain(x=foufth_x, y=foufth_y, count_point=50, methodINTERPOLATION="PchipInterpolator")

    typeGrunt = "sand"

    # Словарь для передачи в функцию комбинации
    dct_Combination = {
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

    # Списки контрольных точек
    if typeGrunt == "gravel":
        y = np.array([0.0, y_press16, y_pressE50, 3.6, 5.7, endE1])
        x = np.array([pressStart1, press16, pressE50, pressEnd1, pressEnd1 - 0.01, pressEnd1])


    if typeGrunt == "sand":


        y = np.array(
            [0.0, y_press16, y_pressE50, y_pressR_RZG])
        x = np.array(
            [pressStart1, press16, pressE50, press_rzg])

        x_end, y_end = combination(differencePress, dct_Combination)

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

    if typeGrunt == "sandy_loam":
        x_end, y_end = combination(differencePress, dct_Combination)

    if typeGrunt == "loam":
        x, y = combination(differencePress, dct_Combination)

    if typeGrunt == "clay":
        x, y = combination(differencePress, dct_Combination)


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

    x = np.concatenate((xnew, first_x, second_x, third_x, foufth_x, fifth_x))
    y = np.concatenate((yfit, first_y, second_y, third_y, foufth_y, fifth_y))

    # Кривая для датафрейма и дапма файла (Девиаторное нагружение - Относительная вертикальная деформация)
    otnVertDef = y / 76
    deviator = [press - pressStart1 for press in x]

    curve1 = np.array([(x, y) for x, y in zip(deviator, otnVertDef)])

    NewDF = pd.DataFrame(curve1)
    NewDF.reset_index(drop=True, inplace=True)

    # xnew_gr = np.concatenate((xnew, first_x, second_x, third_x, foufth_x, fifth_x))
    # yfit_gr = np.concatenate((yfit, first_y, second_y, third_y, foufth_y, fifth_y))
    # # Построение графика
    # plt.plot(x, y, '.')
    # plt.plot(xnew_gr, yfit_gr)
    # plt.grid()
    # plt.show()

    values_for_Excel = {"epsE0": otnVertDef[index_y_E_0],
                        "epsE50": otnVertDef[index_y_E_50],
                        "epsMAX": otnVertDef[index_x_pressMax],

                        "devE0": deviator[index_y_E_0],
                        "devE50": deviator[index_y_E_50],
                        "devMAX": deviator[index_x_pressMax]}

    return NewDF, values_for_Excel
