import math
import random
import time
from functools import wraps

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy import interpolate
from scipy.stats import stats

from GEOF.main_part.graphic.combination import AnalyzeGraph
from GEOF.main_part.graphic.combination_volume import AnalyzeGraph as AnalyzeGraphVolume
from GEOF.main_part.main_tools.main_functions import interpolation, nearest, bezier_curve, random_values


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
    otn_E50 = (pressE50 - pressStart1 + E_50 * otn_pStart) / E_50  # otn_p16 * 3
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

    """
    Объемные деформации
    """

    koef_puasson = data_mech.get("Puasson")
    angle_dilatanci = data_mech.get("Dilatanci")

    # Словарь для передачи в функцию комбинации
    control_point = {
        "y_press16": y_press16,
        "y_pressE50": y_pressE50,
        "endE1": endE1,

        "pressStart1": pressStart1,
        "press16": press16,
        "pressE50": pressE50,
        "pressEnd1": pressEnd1,

        'Puasson': koef_puasson,
        'Dilatanci': angle_dilatanci,
    }

    analyze = AnalyzeGraph(organise_values=organise_dct,
                           control_points=control_point,
                           data=dct_combination,
                           type_grunt_dct=type_grunt_schemas)
    analyze.calculate_perc()
    new_point_x, new_point_y = analyze.points_reload()
    parameters_points_dct = analyze.get_parameters_points()
    xnew, yfit = interpolation(x=new_point_x, y=new_point_y, parameters=parameters_points_dct)

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

    xnew = random_values(points_x=xnew,
                         dont_touch_indexes=[0, index_x_E_0, index_x_E_50, index_x_pressMax, index_y_E_0, index_y_E_50,
                                             index_y_pressMax],
                         parameters_points=parameters_points_dct
                         )

    # Кривая для датафрейма и дапма файла (Девиаторное нагружение - Относительная вертикальная деформация)
    otnVertDef = [value / 76 for value in yfit]
    deviator = [x - pressStart1 for x in xnew]

    """
    Угол дилатансии
    Коэффициент Пуассона
    """
    delta_EV_E0 = (koef_puasson * otn_p16) * 2 + otn_p16

    control_point = {
        "y_press16": y_press16,
        "y_pressE50": y_pressE50,
        "endE1": endE1,

        "pressStart1": pressStart1,
        "press16": press16,
        "pressE50": pressE50,
        "pressEnd1": pressEnd1,

        'Puasson': koef_puasson,
        'Dilatanci': angle_dilatanci,

        "delta_EV_E0": delta_EV_E0,
        "EV_END_1": 1,
        "EV_END_2": 1,
        'y_done': yfit,

        'otnVertDef': otnVertDef,
        'deviator': deviator,
    }
    """
    Пробник угла дилатансии + коэффициент Пуасссона
    """
    analyze_volume = AnalyzeGraphVolume(organise_values=organise_dct,
                                        control_points=control_point,
                                        data=dct_combination,
                                        type_grunt_dct=type_grunt_schemas)
    analyze_volume.calculate_perc()
    new_point_x, _, EV_END_1, EV_END_2 = analyze_volume.points_reload()
    parameters_points_dct = analyze_volume.get_parameters_points()

    parameters_points_dct.update({'method_interpolate': 'nearest_volume'})


    xnew, yfit = interpolation(x=new_point_x, y=new_point_y, parameters=parameters_points_dct)

    # index_x_delta_EV_E0 = xnew.index(nearest(xnew, delta_EV_E0))
    # index_x_EV_END_1 = xnew.index(nearest(xnew, EV_END_1))
    # index_x_EV_END_2 = xnew.index(nearest(xnew, EV_END_2))


    xnew = random_values(points_x=xnew,
                         dont_touch_indexes=[0, ],
                         parameters_points=parameters_points_dct
                         )

    curve1 = np.array([(x, y, z) for x, y, z in zip(deviator, otnVertDef, xnew)])

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
