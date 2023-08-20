import math
import random
import pandas as pd
import numpy as np
import scipy.stats as stats
import scipy.interpolate
from GEOF.main_part import bezier_curve, interpolation
import matplotlib.pyplot as plt

def random_value():
    return random.randint(-10, 10) / 10000

def traxial_consolidation(organise_dct):
    start_time = 0  # сек
    start_volume = 0  # мм3
    start_otn_vert = 0  #
    start_height = 76  # мм
    start_diametr = 38  # мм
    Radius = 38 / 2  # мм

    IP = organise_dct.get('IP')
    pressStart = organise_dct.get('PressStart_traxial_now')
    if str(IP) in ['None', 'nan', 'NAN', 'nAn']:
        time_GOST = 30  # мин
        percent_volume_deformation = random.randint(10, 15) / 10000 # д.е. или 0.003 %
    if IP < 7:
        time_GOST = 3 * 60  # мин
        percent_volume_deformation = random.randint(8, 13) / 10000 # д.е. или 0.003 %
    elif IP < 12:
        time_GOST = 6 * 60  # мин
        percent_volume_deformation = random.randint(8, 12) / 10000 # д.е. или 0.003 %
    elif IP < 17:
        time_GOST = 12 * 60  # мин
        percent_volume_deformation = random.randint(7, 11) / 10000 # д.е. или 0.003 %
    elif IP < 22:
        time_GOST = 12 * 60  # мин
        percent_volume_deformation = random.randint(5, 10) / 10000 # д.е. или 0.003 %
    elif IP >= 22:
        time_GOST = 18 * 60  # мин
        percent_volume_deformation = random.randint(5, 8) / 10000 # д.е. или 0.003 %


    time_100_real = organise_dct.get('t_100') # мин
    if str(time_100_real) in ['None', 'nan', 'NAN', 'nAn']:
        time_100_real = time_GOST * random.randint(70, 90) / 100

    otn_volume_end = percent_volume_deformation * 1000

    Square_calc = math.pi * Radius ** 2  # мм2
    start_value_volume = 86192  # мм3
    V_calc = math.pi * Radius ** 2 * start_height  # мм3
    V_after_consolidation = start_value_volume - start_value_volume * percent_volume_deformation  # мм3
    print(f"Square_calc: {Square_calc}")
    print(f"V_calc: {V_calc}")
    print(f"V_after_consolidation: {V_after_consolidation}")

    end_height = V_after_consolidation / (math.pi * Radius ** 2) # мм
    print(f"end_height: {end_height}")

    otn_times = time_100_real / time_GOST
    print(f"otn_times: {otn_times}")
    volume_100 = otn_volume_end * 0.98
    print(f"volume_100: {volume_100}")

    count_point = time_GOST * random.randint(15, 20)

    time_90 = time_100_real * 0.9
    volume_90 = volume_100 - (time_GOST / time_100_real) * (otn_volume_end - volume_100) # volume_100 * 0.9

    time_50 = time_100_real * 0.5

    line_1_15_x = [0, time_90]
    line_1_15_y = [0, volume_90]

    line_1_x = [0, time_90 * 0.85]
    line_1_y = [0, volume_90]

    perpendicular_50_x = [time_50, time_50]
    perpendicular_50_y = [0, otn_volume_end]

    res = stats.linregress(line_1_x, line_1_y)
    volume_50 = time_50 * res.slope + res.intercept

    xpoints = np.array([start_time, time_50, time_90, time_100_real, time_GOST])
    ypoints = np.array([start_volume, volume_50, volume_90, volume_100, otn_volume_end])
    TIME, VOLUME = interpolation(x=xpoints, y=ypoints, count_point=count_point, method_interpolate="PchipInterpolator", parameters=None)
    TIME = [round(value * 60, 2) for value in TIME]
    volume_cm3 = [round(V_calc * otn_vol, 3) for otn_vol in VOLUME]

    end_e1 = random.randint(-10, 0) / 100

    VerticalDeformation_mm = [round(end_e1 + random_value(), 2) for count in range(count_point)]
    VerticalStrain = [round(VerticalDeformation_mm[count] / (76 - VerticalDeformation_mm[1]), 4) for count in range(count_point)]

    VerticalPress_MPa = [round(pressStart + random_value(), 4) for count in range(count_point)]
    VerticalPress_kPa = [round(press * 1000, 1) for press in VerticalPress_MPa]

    Action = ['Stabilization' for x in range(count_point)]
    Trajectory = ['Consolidation' for x in range(count_point)]
    Action_Changed = ['' for x in range(count_point)]
    CellPress_MPa = VerticalPress_MPa
    CellPress_kPa = VerticalPress_kPa

    Deviator_MPa = [round(0.00, 4) for x in range(count_point)]
    Deviator_kPa = [round(0.00, 1) for x in range(count_point)]


    df = pd.DataFrame({'Time': TIME, 'Action': Action, 'Action_Changed': Action_Changed,
                       'Deviator_kPa': Deviator_kPa, 'CellPress_kPa': CellPress_kPa, 'VerticalPress_kPa': VerticalPress_kPa,
                       'VerticalDeformation_mm': VerticalDeformation_mm,
                       'VerticalStrain': VerticalStrain, 'VolumeStrain': VOLUME,
                       'VolumeDeformation_cm3': volume_cm3, 'Deviator_MPa': Deviator_MPa,
                       'CellPress_MPa': CellPress_MPa, 'VerticalPress_MPa': VerticalPress_MPa, 'Trajectory': Trajectory})

    """ax = plt.gca()
    ax.invert_yaxis()
    # 1
    plt.plot(line_1_x, line_1_y)
    # 1.15
    plt.plot(line_1_15_x, line_1_15_y)
    # Перпендикуляр
    plt.plot(perpendicular_50_x, perpendicular_50_y)
    plt.plot(xpoints_new, ypoints_new)
    plt.plot(xpoints, ypoints, '*')
    plt.grid()
    plt.show()



    plt.plot(press, otn_vert_def)
    plt.grid()
    plt.show()"""

    return df

if __name__ == "__main__":
    traxial_consolidation()
