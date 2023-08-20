import math
import random

import numpy as np
import pandas as pd

from GEOF.main_part.graphic.combination_unaxial import AnalyzeGraph
from GEOF.main_part.main_tools.main_functions import interpolation, nearest, random_values

def start_SPS_CD(organise_dct, dct_combination: dict, type_grunt_schemas: dict) -> (pd.DataFrame, dict):
    """
    Создает график одноплоскостного среза по заданным значениям
    :param organise_dct:
    :param dct_combination:
    :param type_grunt_schemas:
    :return:
    """
    F = organise_dct.get("F_unaxial")
    C = organise_dct.get("C_unaxial")

    pressStart = organise_dct.get("PressStart_unaxial_now")
    pressEnd = organise_dct.get("PressEnd_unaxial_now")

    dct_Combination = {
        "pressStart": pressStart,
        "pressEnd": pressEnd,
    }

    analyze = AnalyzeGraph(organise_values=organise_dct,
                           control_points=dct_Combination,
                           data=dct_combination,
                           type_grunt_dct=type_grunt_schemas)
    analyze.calculate_perc()
    new_point_x, new_point_y = analyze.points_reload()
    parameters_points_dct = analyze.get_parameters_points()
    xnew, yfit = interpolation(x=new_point_x, y=new_point_y, parameters=parameters_points_dct)

    index_x = xnew.index(nearest(xnew, pressEnd))
    xnew[index_x] = pressEnd

    xnew = random_values(points_x=xnew,
                         dont_touch_indexes=[0, index_x],
                         parameters_points=parameters_points_dct
                         )

    # Дамп в csv
    curve1 = np.array([(x, y) for x, y in zip(xnew, yfit)])

    NewDF = pd.DataFrame(curve1)
    NewDF.reset_index(drop=True, inplace=True)

    values_for_Excel = {}

    return NewDF, values_for_Excel

def random_time() -> float:
    """
    Создает примерные значения по времени одной точки в испытании одноплоскостного среза
    :return:
    """
    return random.randint(900, 1500) / 100

def SPS_time(quantity_point) -> list[float]:
    """
    Создает лист времени испытания одноплоскостного среза
    :param quantity_point:
    :return:
    """
    return [random_time() * count for count in range(quantity_point)]

def ISP_SPS(dataframe_isp, organise_dct) -> pd.DataFrame:
    """
    Создает исходник испытания одноплоскостного среза
    :param pressStart:
    :return:
    """
    pressStart = organise_dct.get("PressStart_unaxial_now")

    SHEAR_DEF = list(dataframe_isp[1])
    TANGENT_PRESS = list(dataframe_isp[0])

    count_point = len(SHEAR_DEF)

    TIME = SPS_time(count_point)

    action_list = [str('Stabilization') for x in range(count_point)]

    action_changed_list = [str(True) for x in range(count_point)]

    press_sps = [pressStart for x in range(count_point)]

    empty_list = [str('') for x in range(count_point)]

    name = [str('Срез') for x in range(count_point)]

    df = pd.DataFrame({'Time': TIME, 'Action': action_list, 'Action_Changed': action_changed_list,
                       'VerticalPress_kPa': empty_list, 'ShearDeformation_mm': SHEAR_DEF, 'ShearPress_kPa': empty_list,
                       'VerticalPress_MPa': press_sps, 'ShearPress_MPa': TANGENT_PRESS, 'ShearStrain': empty_list,
                       'Stage': name})
    return df
