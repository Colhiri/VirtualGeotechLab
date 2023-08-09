import math
import random

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy import interpolate
from scipy.stats import stats
from scipy.special import comb

from GEOF.main_part.graphic.combination import AnalyzeGraph
from GEOF.main_part.main_tools.main_functions import interpolation, nearest, bezier_curve

def start_TPDS_RZG(organise_dct: dict, dct_combination: dict, type_grunt_schemas: dict):
    # Выбор давлений
    pressStart1 = organise_dct.get("PressStart_traxial_now")
    name = organise_dct.get('name_traxial_now')
    pressEnd1 = organise_dct.get("PressEnd_traxial_now")

    F = organise_dct.get("F_traxial")
    C = organise_dct.get("C_traxial")

    E_0 = organise_dct.get("E_0")
    E_50 = organise_dct.get("E_50")


    E_rzg = organise_dct.get("E_rzg")
    CD_v_rzg = organise_dct.get("CD_v_rzg")
    if not E_rzg:
        E_rzg = E_0 * random.randint(4, 5)
    if not CD_v_rzg:
        CD_v_rzg = random.randint(14, 16) / 100

    koef_puasson = organise_dct.get("CD_v")
    angle_dilatanci = organise_dct.get("Dilatanci")

    get_parameters = AnalyzeGraph(organise_values=organise_dct,
                                  control_points={},
                                  data=dct_combination,
                                  type_grunt_dct=type_grunt_schemas)
    parameters_points_dct = get_parameters.get_parameters_points()
    countPoint = parameters_points_dct.get("count_point")
    endE1 = parameters_points_dct.get("endE1")

    otn_pStart = 0
    stepE1 = endE1 / countPoint




    # Расчет E1 и относительных вертикальных деформаций
    press16 = pressStart1 * 1.6
    otn_p16 = (press16 - pressStart1 + E_0 * otn_pStart) / E_0
    y_press16 = 76 * otn_p16 - otn_p16 * stepE1

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

    print(E_rzg_calc)

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
    parameters_points_dct = analyze.get_parameters_points()

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

    fifth_x, fifth_y = interpolation(x=x_end, y=y_end,
                                     count_point=100,
                                     parameters=parameters_points_dct)

    y = np.array(
        [0.0, y_press16, y_pressE50, y_pressR_RZG])
    x = np.array(
        [pressStart1, press16, pressE50, press_rzg])
    xnew, yfit = interpolation(x=x_end, y=y_end,
                               count_point=100,
                               parameters=parameters_points_dct)

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

    x = np.concatenate((xnew, low_curve_x, high_curve_x, fifth_x))
    y = np.concatenate((yfit, low_curve_y, high_curve_y, fifth_y))

    # Кривая для датафрейма и дапма файла (Девиаторное нагружение - Относительная вертикальная деформация)
    otnVertDef = y / 76
    deviator = [press - pressStart1 for press in x]

    curve1 = np.array([(x, y) for x, y in zip(deviator, otnVertDef)])

    NewDF = pd.DataFrame(curve1)
    NewDF.reset_index(drop=True, inplace=True)

    values_for_Excel = {"epsE0": otnVertDef[index_y_E_0],
                        "epsE50": otnVertDef[index_y_E_50],
                        "epsMAX": otnVertDef[index_x_pressMax],

                        "devE0": deviator[index_y_E_0],
                        "devE50": deviator[index_y_E_50],
                        "devMAX": pressEnd1 - pressStart1,
                        }

    return NewDF, values_for_Excel
