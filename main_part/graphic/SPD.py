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


def SPD_start(dct: dict, name: str, organise_dct: dict, methodINTERPOLATION):

    IP = organise_dct.get('IP')
    IL = organise_dct.get('IL')
    e = organise_dct.get('e')
    p = organise_dct.get('p')
    g = 9.80665
    depth = organise_dct.get('depth')

    Eoed01_02_MPa = dct.get('Eoed01_02_MPa')
    Eoed_k_opr = dct.get('Eobs01_02_Mpa')


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
            press_spd = [0, 0.0125, 0.025, 0.05, 0.1, 0.2] # [0, 0.005, 0.01, 0.02, 0.04, 0.08]
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
            press_spd = [0, 0.0125, 0.025, 0.05, 0.1, 0.2] # [0, 0.005, 0.01, 0.02, 0.04, 0.08]
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


    delta_h = (0.1 * 20) / Eoed01_02_MPa

    degree_d = Eoed_k_opr / Eoed01_02_MPa # random.randint(4, 6) / 10

    a = delta_h / ((0.2 ** degree_d) - (0.1 ** degree_d))

    # расчет точек по y, т.е. давления в миллиметрах
    p_y = [a * x ** degree_d for x in press_spd]

    # относительная вертикальная деформация
    # простановка нужного модуля по последней точке давления для касательного модуля
    otn_vert_def = [(p_y[x] / 20) for x in range(len(p_y))] # [0.0, 0.027, 0.049, 0.066, 0.086, 0.101]
    if press_spd[index_2] == 0.2:
        pass
    else:
        otn_vert_def[index_2] = otn_vert_def[index_1] + (press_spd[index_2] - press_spd[index_1]) / Eoed_k_opr
    # otn_vert_def[index_2] = 0.058

    # пористость по ступеням
    por_list = [(e - (otn_vert_def[x] * (1 + e))) for x in range(len(otn_vert_def))]

    # Старый касательный одометрический модуль по бете
    E_k = Eoed01_02_MPa * beta

    # коэффициент сжимаемости
    koef_m0 = [(por_list[x] - por_list[x + 1]) / (press_spd[x + 1] - press_spd[x]) for x in range(len(press_spd) - 1)]
    koef_m0.insert(0, 0)

    # Нужно сделать определение максиаально близких точек к природному давлению
    # Возвращает функцию линейной регрессии, позволяющей узнать точки при домножении x * a + b
    import scipy.stats as stats
    res = stats.linregress(press_spd[index_1:index_2+1], otn_vert_def[index_1:index_2+1])
    otn_vert_def_ZG = press_zg * res.slope + res.intercept
    otn_END_A = 0 * res.slope + res.intercept



    res_max = stats.linregress([otn_END_A, otn_vert_def_ZG], [0, press_zg])
    press_MAX = (otn_vert_def[-1] * res_max.slope + res_max.intercept)

    # Текущий касательный модуль
    E_oed_K_now = press_zg / (otn_vert_def_ZG - otn_END_A)

    # Проверка секущего модуля
    E_oed_calc_SIMPLE = 0.1 / (otn_vert_def[index_2] - otn_vert_def[index_1])




    prepare_df = np.asarray([(press, otn, por, m0) for press, otn, por, m0 in zip(press_spd, otn_vert_def, por_list, koef_m0)])

    NewDF = pd.DataFrame(prepare_df)
    NewDF.reset_index(drop=True, inplace=True)

    # NewDF.to_csv(fr"C:\Users\MSI GP66\PycharmProjects\dj_project\ENGGEO_program\prot\{name}.log",
    #              sep='\t', index_label=False, index=False, header=False)

    # Построение графика
    # plt.plot(press_spd, otn_vert_def, '.')
    # plt.plot(press_spd, otn_vert_def)
    # plt.grid()
    # plt.show()

    values_for_Excel = {"E_oed": E_oed_calc_SIMPLE,
                        "E_oed_k": E_oed_K_now,
                        "q_zg": press_zg,
                        "otn_zg": otn_vert_def_ZG,
                        "otn_END_A": otn_END_A,
                        'press_MAX': press_MAX,
                        'otn_MAX': otn_vert_def[-1],

                        }

    return NewDF, values_for_Excel
