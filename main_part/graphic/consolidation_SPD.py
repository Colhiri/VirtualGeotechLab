import math
import random
import pandas as pd
import numpy as np
import scipy.stats as stats
import scipy.interpolate
from GEOF.main_part import bezier_curve, interpolation
import matplotlib.pyplot as plt

def consolidation_curve():
    """
    Строит кривую консиоладацию в объемной и вертиклаьной деформации
    :return:
    """
    F_temperature = 1

    # старт по времени идет после стадии wait
    start_time = 0 # сек
    start_volume = 0 # мм3
    start_otn_vert = 0 #
    start_height = 76 # мм
    start_diametr = 38 # мм
    Radius = 38 / 2 # мм

    percent_volume_deformation = 0.0003 # д.е. 0.003 %

    Square_calc = math.pi * Radius ** 2 # мм2
    start_value_volume = 86192 # мм3
    V_calc = math.pi * Radius ** 2 * start_height # мм3
    V_after_consolidation = 86192 - 86192 * percent_volume_deformation # мм3
    print(f"Square_calc: {Square_calc}")
    print(f"V_calc: {V_calc}")
    print(f"V_after_consolidation: {V_after_consolidation}")
    end_height = V_after_consolidation / (math.pi * Radius ** 2) # мм
    print(f"end_height: {end_height}")
    middle_height = end_height + (start_height - end_height) / 2 # мм
    print(f"middle_height: {middle_height}")

    T90 = 0.848
    T50 = 0.197

    Cv = 0.105 # см2/мин

    time_90_calc = ((T90 * middle_height ** 2) / Cv) # мин -- Квадратный корень из времени
    Cv_calc_90 = ((T90 * middle_height ** 2) / time_90_calc) * F_temperature # см2/мин Квадратный корень из времени
    time_100 = middle_height / 0.9
    print(f"time_90_calc: {time_90_calc}")
    print(f"Cv_calc: {Cv_calc_90}")
    print(f"time_100: {time_100}")

    time_50_calc = (T50 * (start_height - end_height) ** 2) / Cv # мин -- Логарифмический метод
    Cv_calc_50 = ((T50 * (start_height - end_height) ** 2) / time_50_calc) * F_temperature  # см2/мин Логарифмический метод