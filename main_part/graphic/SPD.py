import math
import random

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy import interpolate
import scipy.stats as stats

from GEOF.main_part.main_tools.main_functions import interpolation, nearest, bezier_curve, random_values

def SPD_start_new(organise_dct: dict):
    IP = organise_dct.get('IP')
    IL = organise_dct.get('IL')
    e = organise_dct.get('e')
    p = organise_dct.get('p')
    g = 9.80665
    depth = organise_dct.get('depth')

    Eoed01_02_MPa = organise_dct.get('Eoed01_02_MPa')  # Основной одометрический
    Eoed_k_opr = organise_dct.get('Eobs01_02_Mpa')  # Касательный

    if 1 <= IP <= 7:
        beta = 0.7
        if e >= 0.45 and e <= 0.55:
            moed = 2.8

        if e > 0.55 and e <= 0.65:
            moed = ((0.65 - e) / (0.1)) * 0.3 + 2.5

        if e > 0.65 and e <= 0.75:
            moed = ((0.75 - e) / (0.1)) * 0.4 + 2.1

        if e > 0.75 and e <= 0.85:
            moed = ((0.85 - e) / (0.1)) * 0.7 + 1.4
    if 7 < IP <= 17:
        beta = 0.6
        if e >= 0.45 and e <= 0.55:
            moed = 3

        if e > 0.55 and e <= 0.65:
            moed = ((0.65 - e) / (0.1)) * 0.3 + 2.7

        if e > 0.65 and e <= 0.75:
            moed = ((0.75 - e) / (0.1)) * 0.3 + 2.4

        if e > 0.75 and e <= 0.85:
            moed = ((0.85 - e) / (0.1)) * 0.6 + 1.8

        if e > 0.85 and e <= 0.95:
            moed = ((0.95 - e) / (0.1)) * 0.3 + 1.5

        if e > 0.95 and e <= 1.05:
            moed = ((1.05 - e) / (0.1)) * 0.3 + 1.2
    if IP > 17:
        beta = 0.4
        if e > 0.65 and e <= 0.75:
            moed = 2.4

        if e > 0.75 and e <= 0.85:
            moed = ((0.85 - e) / (0.1)) * 0.2 + 2.2

        if e > 0.85 and e <= 0.95:
            moed = ((0.95 - e) / (0.1)) * 0.2 + 2

        if e > 0.95 and e <= 1.05:
            moed = ((1.05 - e) / (0.1)) * 0.2 + 1.8
    if not IP:
        beta = 0.8

    # Для глинистых грунтов
    if IP:
        if IL >= 1:
            press_spd = [0, 0.0125, 0.025, 0.05, 0.1, 0.2]  # [0, 0.005, 0.01, 0.02, 0.04, 0.08]
        if 1 > IL >= 0.75:
            press_spd = [0, 0.0125, 0.025, 0.05, 0.1, 0.2]
        if 0.75 > IL >= 0.5:
            press_spd = [0, 0.025, 0.05, 0.1, 0.2, 0.4]
        if 0.5 > IL >= 0.25:
            press_spd = [0, 0.05, 0.1, 0.2, 0.4, 0.8]
        if IL < 0.25:
            press_spd = [0, 0.1, 0.2, 0.4, 0.8, 1.6]
    else:
        if e >= 1:
            press_spd = [0, 0.0125, 0.025, 0.05, 0.1, 0.2]  # [0, 0.005, 0.01, 0.02, 0.04, 0.08]
        if 1 > e >= 0.75:
            press_spd = [0, 0.0125, 0.025, 0.05, 0.1, 0.2]
        if 0.75 > e > 0.6:
            press_spd = [0, 0.025, 0.05, 0.1, 0.2, 0.4]
        if e <= 0.6:
            press_spd = [0, 0.05, 0.1, 0.2, 0.4, 0.8]

    # Природное эффективное напряжение
    press_zg = (p * g * depth) / 1000

    for count, val in enumerate(press_spd, 0):
        if press_spd[count] < press_zg <= press_spd[count + 1]:
            index_1 = count
            index_2 = count + 1
            break

    if index_2 < press_spd.index(0.2):
        delta_h = (0.1 * 20) / Eoed01_02_MPa
        degree_d = Eoed_k_opr / Eoed01_02_MPa
        a = delta_h / ((0.2 ** degree_d) - (0.1 ** degree_d))
        p_y = [a * x ** degree_d for x in press_spd]
        otn_vert_def = [(p_y[x] / 20) for x in range(len(p_y))]

        otn_vert_def[index_2] = (press_spd[index_2] - press_spd[index_1] + Eoed_k_opr *
                                                  otn_vert_def[index_1]) / Eoed_k_opr

        otn_vert_def[press_spd.index(0.2)] = ((0.1) + Eoed01_02_MPa * otn_vert_def[
            press_spd.index(0.1)]) / Eoed01_02_MPa

        Eoed_CALC = 0.1 / (otn_vert_def[press_spd.index(0.2)] - otn_vert_def[press_spd.index(0.1)])
        Eoed_k_opr_CALC = (press_spd[index_2] - press_spd[index_1]) / (
                    otn_vert_def[index_2] - otn_vert_def[index_1])

        count = 2
        for val in press_spd:
            if val <= 0.2:
                continue
            otn_vert_def[press_spd.index(val)] = (val - (val / 2) + Eoed01_02_MPa * count * otn_vert_def[press_spd.index(val) - 1]) / (Eoed01_02_MPa * count)
            count *= 2

    if index_2 == press_spd.index(0.2):
        delta_h = (0.1 * 20) / Eoed01_02_MPa
        degree_d = random.randint(5, 6) / 10# Eoed_k_opr / Eoed01_02_MPa
        a = delta_h / ((0.2 ** degree_d) - (0.1 ** degree_d))
        p_y = [a * x ** degree_d for x in press_spd]
        otn_vert_def = [(p_y[x] / 20) for x in range(len(p_y))]

    if index_2 > press_spd.index(0.2):
        delta_h = (0.1 * 20) / Eoed01_02_MPa
        degree_d = Eoed_k_opr / Eoed01_02_MPa
        a = delta_h / ((0.2 ** degree_d) - (0.1 ** degree_d))
        p_y = [a * x ** degree_d for x in press_spd]
        otn_vert_def = [(p_y[x] / 20) for x in range(len(p_y))]

        otn_vert_def[press_spd.index(0.2)] = ((0.1) + Eoed01_02_MPa * otn_vert_def[
            press_spd.index(0.1)]) / Eoed01_02_MPa

        otn_vert_def[index_2] = ((press_spd[index_2] - press_spd[index_1]) + Eoed_k_opr *
                                 otn_vert_def[index_1]) / Eoed_k_opr

        count = 2
        for val in press_spd:
            if val <= press_spd[index_2]:
                continue
            otn_vert_def[press_spd.index(val)] = (val - (val / 2) + Eoed_k_opr * count * otn_vert_def[
                press_spd.index(val) - 1]) / (Eoed_k_opr * count)
            count *= 2

    # Возвращает функцию линейной регрессии, позволяющей узнать точки при домножении x * a + b
    res = stats.linregress(press_spd[index_1:index_2 + 1], otn_vert_def[index_1:index_2 + 1])
    otn_vert_def_ZG = press_zg * res.slope + res.intercept
    otn_END_A = 0 * res.slope + res.intercept

    res_max = stats.linregress([otn_END_A, otn_vert_def_ZG], [0, press_zg])
    press_MAX = (otn_vert_def[-1] * res_max.slope + res_max.intercept)

    # Старый касательный одометрический модуль по бете
    # E_k = Eoed01_02_MPa * beta

    # Текущий касательный модуль
    E_oed_K_now = press_zg / (otn_vert_def_ZG - otn_END_A)

    # Проверка секущего модуля
    E_oed_calc_SIMPLE = 0.1 / (otn_vert_def[press_spd.index(0.2)] - otn_vert_def[press_spd.index(0.1)])

    # пористость по ступеням
    por_list = [(e - (otn_vert_def[x] * (1 + e))) for x in range(len(otn_vert_def))]
    # коэффициент сжимаемости
    koef_m0 = [(por_list[x] - por_list[x + 1]) / (press_spd[x + 1] - press_spd[x]) for x in range(len(press_spd) - 1)]
    koef_m0.insert(0, 0)

    prepare_df = np.asarray(
        [(press, otn, por, m0) for press, otn, por, m0 in zip(press_spd, otn_vert_def, por_list, koef_m0)])

    NewDF = pd.DataFrame(prepare_df)
    NewDF.reset_index(drop=True, inplace=True)

    values_for_Excel = {"E_oed": E_oed_calc_SIMPLE,
                        "E_oed_k": E_oed_K_now,
                        "q_zg": press_zg,
                        "otn_zg": otn_vert_def_ZG,
                        "otn_END_A": otn_END_A,
                        'press_MAX': press_MAX,
                        'otn_MAX': otn_vert_def[-1],
                        }

    return NewDF, values_for_Excel
