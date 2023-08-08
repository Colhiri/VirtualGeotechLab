import math
import random

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy import interpolate

from GEOF.main_part.graphic.combination_unaxial import AnalyzeGraph
from GEOF.main_part.main_tools.main_functions import interpolation, nearest, bezier_curve, random_values

def start_SPS_CD(name: str, data_mech: dict, organise_dct, dct_combination: dict, type_grunt_schemas: dict):

    F = data_mech.get("F")
    C = data_mech.get("C")
    countPoint = data_mech.get("countPoint")
    endE1 = data_mech.get("endE1")
    stepE1 = endE1 / countPoint

    pressStart = data_mech.get("pressStart")
    pressEnd = data_mech.get("pressEnd")

    # Выделение возможной максимальной разницы между точками


    differencePress = pressEnd / 100

    dct_Combination = {
        "pressStart": pressStart,
        "endE1": endE1,
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