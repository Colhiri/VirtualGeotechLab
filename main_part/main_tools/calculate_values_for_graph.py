import math
import random

from GEOF.main_part.main_tools import calculate_press_gost

def SPS_value(organise_dct):

    pressEnd1, pressEnd2, pressEnd3 = None, None, None

    try:
        F = organise_dct.get('F_unaxial')
        C = organise_dct.get('C_unaxial')
        pressStart1 = organise_dct.get('pressStart1_unaxial')
        pressStart2 = organise_dct.get('pressStart2_unaxial')
        pressStart3 = organise_dct.get('pressStart3_unaxial')

        Rad = math.radians(F)

        valueRANDOM_to_press2 = random.choice([x for x in [random.randint(-10, 10) / 1000 for x in range(5)] if x != 0.0])

        pressEnd1 = (pressStart1 * math.tan(Rad) + C) - valueRANDOM_to_press2 / 2
        pressEnd2 = (pressStart2 * math.tan(Rad) + C) + valueRANDOM_to_press2
        pressEnd3 = (pressStart3 * math.tan(Rad) + C) - valueRANDOM_to_press2 / 2

        # math.tan(Rad)
        tan_RAD_F = ((3 * (pressStart1 * pressEnd1 + pressStart2 * pressEnd2 + pressStart3 * pressEnd3) -
                      (pressStart1 + pressStart2 + pressStart3) * (pressEnd1 + pressEnd2 + pressEnd3))
                     /
                     (3 * (pressStart1 ** 2 + pressStart2 ** 2 + pressStart3 ** 2) - (
                             pressStart1 + pressStart2 + pressStart3) ** 2))

        F_CALC = math.degrees(math.atan(tan_RAD_F))

    except: # TypeError
        pass

    return pressEnd1, pressEnd2, pressEnd3


def Traxial_value(organise_dct):

    pressEnd1, pressEnd2, pressEnd3 = None, None, None

    try:
        F = organise_dct.get('F_traxial')
        C = organise_dct.get('C_traxial')
        pressStart1 = organise_dct.get('pressStart1_traxial')
        pressStart2 = organise_dct.get('pressStart2_traxial')
        pressStart3 = organise_dct.get('pressStart3_traxial')

        N = 2 * math.tan(math.pi * F / 180) * (
                (((math.tan(math.pi * F / 180)) ** 2) + 1) ** (1 / 2)) + 2 * (
                    (math.tan(math.pi * F / 180)) ** 2) + 1
        M = 2 * (N ** (1 / 2)) * C
        pressEnd1 = (pressStart1 * N + M)
        pressEnd2 = pressStart2 * (
                2 * math.tan(math.pi * F / 180) * ((((math.tan(math.pi * F / 180)) ** 2) + 1) ** (1 / 2)) + 2 * (
                (math.tan(math.pi * F / 180)) ** 2) + 1) + (2 * ((2 * math.tan(math.pi * F / 180) * (
                (((math.tan(math.pi * F / 180)) ** 2) + 1) ** (1 / 2)) + 2 * ((math.tan(
            math.pi * F / 180)) ** 2) + 1) ** (1 / 2)) * C)
        pressEnd3 = (pressStart3 * N + M)

    except:  # TypeError
        pass

    return pressEnd1, pressEnd2, pressEnd3


