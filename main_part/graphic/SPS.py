import numpy as np
import pandas as pd

from GEOF.main_part.graphic.combination_unaxial import AnalyzeGraph
from GEOF.main_part.main_tools.main_functions import interpolation, nearest, random_values

class Unaxial_isp:
    def __init__(self, organise_dct: dict, dct_combination: dict, type_grunt_schemas: dict):
        self.organise_dct = organise_dct
        self.dct_combination = dct_combination
        self.type_grunt_schemas = type_grunt_schemas

    def main_isp(self):
        pressStart = self.organise_dct.get("PressStart_unaxial_now")
        pressEnd = self.organise_dct.get("PressEnd_unaxial_now")

        control_points = {
            "pressStart": pressStart,
            "pressEnd": pressEnd,
        }

        analyze = AnalyzeGraph(organise_values=self.organise_dct,
                               control_points=control_points,
                               data=self.dct_combination,
                               type_grunt_dct=self.type_grunt_schemas)
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

        curve1 = np.array([(x, y) for x, y in zip(xnew, yfit)])

        NewDF = pd.DataFrame(curve1)
        NewDF.reset_index(drop=True, inplace=True)

        values_for_Excel = {'press': pressEnd,
                            'tau': max(yfit)}

        return NewDF, values_for_Excel
