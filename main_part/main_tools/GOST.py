import math

import numpy as np

def getting_parameters_from_enggeo(organise_dct: dict):

    IP = organise_dct.get('IP')
    IL = organise_dct.get('IL')
    e = organise_dct.get('e')
    Sr = organise_dct.get('Sr')

    # основной тип грунта для механики
    if str(IP) in [None, 'nan', 'None']:
        consistency = None
        water_saturation = None
        IL = None
        main_type = 'incoherent'  # несвязный

        GGR10 = organise_dct.get('GGR10')
        G10_5 = organise_dct.get('G10_5')
        G5_2 = organise_dct.get('G5_2')
        G2_1 = organise_dct.get('G2_1')
        G1_05 = organise_dct.get('G1_05')
        G05_025 = organise_dct.get('G05_025')
        G025_01 = organise_dct.get('G025_01')
        G01_005 = organise_dct.get('G01_005')

        # гравелистый
        if (G5_2 + G10_5 + GGR10) > 25:
            grunt_type = 'gravel'
            density = None

            # крупный
        elif (G1_05 + G2_1 + G5_2 + G10_5 + GGR10) > 50:
            grunt_type = 'large'
            density = None

            # средний
        elif (G05_025 + G1_05 + G2_1 + G5_2 + G10_5 + GGR10) > 50:
            grunt_type = 'mid'
            if e != None:
                if e <= 0.55:
                    density = 'plotn'  # плотность
                if 0.55 < e and e <= 0.7:
                    density = 'mid_plotn'
                if e > 0.7000000000000000001:
                    density = 'pihl'
            else:
                density = None

            #  мелкий
        elif (G025_01 + G05_025 + G1_05 + G2_1 + G5_2 + G10_5 + GGR10) >= 75:
            grunt_type = 'small'
            if e != None:
                if e <= 0.6:
                    density = 'plotn'
                if 0.6 < e and e <= 0.75:
                    density = 'mid_plotn'
                if e > 0.75:
                    density = 'pihl'
            else:
                density = None

            #  пылеватый
        elif (G025_01 + G05_025 + G1_05 + G2_1 + G5_2 + G10_5 + GGR10) < 75:
            grunt_type = 'dust'
            density = None
        else:
            grunt_type = 'mid'
            density = 'mid_plotn'
    else:
        IP = float(IP)
        IL = float(IL)
        density = None
        main_type = 'coherent'  # связный
        # супесь
        if IP <= 7:
            grunt_type = 'supes'
            if IL < 0:
                consistency = 'tverd'
            if 0 <= IL and IL <= 1:
                consistency = 'plast'
            if 1 < IL:
                consistency = 'tekuch'

        # суглинок
        if 7 < IP and IP <= 17:
            grunt_type = 'sugl'
            if IL < 0:
                consistency = 'tverd'
            if 0 <= IL <= 0.25:
                consistency = 'polutverd'
            if 0.25 < IL and IL <= 0.5:
                consistency = 'tugoplast'
            if 0.5 < IL and IL <= 0.75:
                consistency = 'mygkoplast'
            if 0.75 < IL and IL <= 1:
                consistency = 'tekuchplast'
            if 1 < IL:
                consistency = 'tekuch'

        # глина
        if IP > 17:
            grunt_type = 'glina'
            if IL < 0:
                consistency = 'tverd'
            if 0 <= IL and IL <= 0.25:
                consistency = 'polutverd'
            if 0.25 < IL and IL <= 0.5:
                consistency = 'tugoplast'
            if 0.5 < IL and IL <= 0.75:
                consistency = 'mygkoplast'
            if 0.75 < IL and IL <= 1:
                consistency = 'tekuchplast'
            if 1 < IL:
                consistency = 'tekuch'

    # водонасыщенность
    if Sr != None:
        if Sr <= 0.8:
            water_saturation = True
        else:
            water_saturation = False
    else:
        water_saturation = None

    parametr_proba = {}

    param_proba = ['grunt_type', 'consistency', 'density', 'water_saturation',
                   'main_type', 'IP', 'IL', 'e', 'Sr', 'parametr_write_temporary']
    param_proba_value = [grunt_type, consistency, density, water_saturation,
                         main_type, IP, IL, e]
    for parametr, value in zip(param_proba, param_proba_value):
        parametr_proba.setdefault(parametr, value)
    return parametr_proba


def calculate_press_gost(typeISP, F, C, organise_dct: dict, GRANSOST=None,
                         K_0=True, Calc_K_0=False, DOP = None):

    Depth = organise_dct.get('Depth')
    parametr_proba = getting_parameters_from_enggeo(organise_dct)

    press, press_1, press_3, press_3 = None, None, None, None

    if typeISP == "SPS":

        if DOP != None:
            press_1 = (((Depth * 20 + DOP) / 2) / 2) / 1000
            press_2 = ((Depth * 20 + DOP) / 2) / 1000
            press_3 = (Depth * 20 + DOP) / 1000
        else:
            if not parametr_proba.get('IP'):
                # песок
                if parametr_proba.get('grunt_type') == 'gravel_sand' or parametr_proba.get('grunt_type') == 'large_sand':
                    press_1 = 0.100
                    press_2 = 0.300
                    press_3 = 0.500
                if parametr_proba.get('grunt_type') == 'mid_sand':
                    if parametr_proba.get('density') == 'plotn':
                        press_1 = 0.100
                        press_2 = 0.300
                        press_3 = 0.500
                    if parametr_proba.get('density') == 'mid_plotn':
                        press_1 = 0.100
                        press_2 = 0.200
                        press_3 = 0.300
                    if parametr_proba.get('density') == 'pihl':
                        press_1 = 0.100
                        press_2 = 0.150
                        press_3 = 0.200

                if parametr_proba.get('grunt_type') == 'small_sand':
                    if parametr_proba.get('density') == 'plotn':
                        press_1 = 0.100
                        press_2 = 0.200
                        press_3 = 0.300
                    if parametr_proba.get('density') == 'mid_plotn':
                        press_1 = 0.100
                        press_2 = 0.200
                        press_3 = 0.300
                    if parametr_proba.get('density') == 'pihl':
                        press_1 = 0.100
                        press_2 = 0.150
                        press_3 = 0.200

                if parametr_proba.get('grunt_type') == 'dust_sand':
                    press_1 = 0.100
                    press_2 = 0.150
                    press_3 = 0.200
            else:
                # связные
                # супеси, суглинки
                if parametr_proba.get('grunt_type') == 'supes' or parametr_proba.get('grunt_type') == 'sugl':
                    if parametr_proba.get('IL') <= 0.5:
                        press_1 = 0.100
                        press_2 = 0.200
                        press_3 = 0.300
                    else:
                        press_1 = 0.100
                        press_2 = 0.150
                        press_3 = 0.200
                # глина
                if parametr_proba.get('grunt_type') == 'glina':
                    if parametr_proba.get('consistency') == 'tverd' or parametr_proba.get('consistency') == 'polutverd':
                        press_1 = 0.100
                        press_2 = 0.300
                        press_3 = 0.500
                    if parametr_proba.get('consistency') == 'tugoplast':
                        press_1 = 0.100
                        press_2 = 0.200
                        press_3 = 0.300
                    if parametr_proba.get('consistency') == 'mygkoplast' or parametr_proba.get(
                            'consistency') == 'tekuchplast' or parametr_proba.get('consistency') == 'tekuch':
                        press_1 = 0.100
                        press_2 = 0.150
                        press_3 = 0.200
    else:
        press_1, press_2, press_3 = 0.1, 0.2, 0.3

    if typeISP == "TPD" or typeISP == "TPS" or typeISP == "TPDS":

        K_0 = 1

        if parametr_proba.get('grunt_type') == 'supes' or parametr_proba.get(
                'grunt_type') == 'sugl' or parametr_proba.get('grunt_type') == 'glina' and K_0 and not Calc_K_0:
            if parametr_proba.get('IL') > 0.5:
                K_0 = 1
            if parametr_proba.get('IL') <= 0.5:
                K_0 = 0.7
        if parametr_proba.get('main_type') == 'incoherent' and K_0 and not Calc_K_0:
            K_0 = 0.5
        if K_0:
            K_0 = 1
        if Depth < 1:
            Depth = 1

        if Calc_K_0:
            K_0 = 1 - math.sin(math.radians(F))

        press = ((Depth * organise_dct.get('p')) / 1000) * K_0
        if press < 0.050:
            press = 0.050
        else:
            pass
    else:
        press = None
        press_1 = None
        press_2 = None
        press_3 = None

    # parametr_press = {'press': , 'press_1': press_1, 'press_2': press_2, 'press_3': press_3}

    return press, press_1, press_2, press_3