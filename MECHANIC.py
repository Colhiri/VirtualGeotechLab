import math
import random
import os
import sys
import time

import GEOF.main_part.graphic.TPDS_on_CF as TPDSCF
import GEOF.main_part.graphic.TPDS_on_E50 as TPDS50

import GEOF.main_part.graphic.SPS as SPS
import GEOF.main_part.graphic.SPD as SPD
import GEOF.main_part.graphic.TPDS_on_CF_RZG as TPDSRZG
import GEOF.main_part.graphic.TPDS_on_CF_RZG_50 as TPDSRZG50
import GEOF.main_part.graphic.OCR as OCR_ISP
import GEOF.main_part.main_tools as main_tools
import GEOF.main_part.read_shablons as read_shablons
import GEOF.main_part.main_tools.calculate_values_for_graph as calculate_values
from GEOF.main_part.main_tools import calculate_press_gost
from GEOF.main_part.main_tools.normative_parameters import GruntNormative


def start(worksheet_journal, id_user, dct_combination):

    count_rows = len(worksheet_journal)
    for row in range(0, count_rows):

        # Список для сохранения датафреймов, которые возвращаются из TPDS
        save_DF = []

        # Распаковка параметров из Датафрейма
        LAB_NO = worksheet_journal['Ind_lab'][row]
        N_IG = worksheet_journal['Ind'][row]
        boreHole = worksheet_journal['BH'][row]
        depth = worksheet_journal['Depth'][row]
        nameSoil = worksheet_journal['name_soil'][row]
        # Заказчик
        nameClient = worksheet_journal['nameClient'][row]
        # Объект
        nameObject = worksheet_journal['nameObject'][row]
        if isinstance(nameSoil, tuple):
            nameSoil = nameSoil[0]
        if isinstance(nameObject, tuple):
            nameObject = nameObject[0]
        if isinstance(nameObject, tuple):
            nameClient = nameClient[0]
        print(LAB_NO)

        # Создание папки для складирования испытаний в объекте
        pathSave = os.path.join(f"..\\prot\\{id_user}")
        if not os.path.exists(pathSave):
            os.mkdir(pathSave)
        pathSave = os.path.join(f"..\\prot\\{id_user}\\{nameObject}")
        if not os.path.exists(pathSave):
            os.mkdir(pathSave)

        organise_dct = {
            # Распаковка параметров из Датафрейма
            'LAB_NO': worksheet_journal['Ind_lab'][row],
            'N_IG': worksheet_journal['Ind'][row],
            'boreHole': worksheet_journal['BH'][row],
            'nameSoil': nameSoil,
            'depth': worksheet_journal['Depth'][row],
            # Дата получение объекта подлежащего испытаниям
            'date_isp_object': worksheet_journal['data_f'][row],
            # Дата испытания
            'date_isp': worksheet_journal['data_test'][row],
            # Дата протокола
            'date_protocol': worksheet_journal['data_prot'][row],
            # Номер протокола
            'number_protocol': worksheet_journal['Np'][row],
            # Заказчик
            'nameClient': nameClient,
            # Объект
            'nameObject': nameObject,

            'pathSave': pathSave,
            'pathSave_traxial_CD': None,
            'pathSave_traxial_CU': None,
            'pathSave_traxial_UU': None,

            'pathSave_unaxial': None,
            'pathSave_spd': None,
            'pathSave_OCR': None,

            # Физические параметры для протокола
            'We': worksheet_journal['We'][row],
            'p': worksheet_journal['p'][row],
            'ps': worksheet_journal['ps'][row],
            'e': worksheet_journal['e'][row],
            'IP': worksheet_journal['IP'][row],
            'IL': worksheet_journal['IL'][row],
            'Sr': worksheet_journal['Sr'][row],
            'WL': worksheet_journal['WL'][row],
            'WP': worksheet_journal['WP'][row],
            'Ir': worksheet_journal['Ir'][row],

            # Грансостав
            'GGR10': worksheet_journal['GGR10'][row],
            'G10_5': worksheet_journal['G10_5'][row],
            'G5_2': worksheet_journal['G5_2'][row],
            'G2_1': worksheet_journal['G2_1'][row],
            'G1_05': worksheet_journal['G1_05'][row],
            'G05_025': worksheet_journal['G05_025'][row],
            'G025_01': worksheet_journal['G025_01'][row],
            'G01_005': worksheet_journal['G01_005'][row],
            'G005_001': worksheet_journal['G005_001'][row],
            'G001_0002': worksheet_journal['G001_0002'][row],
            'G0002': worksheet_journal['G0002'][row],

            # Трехосники КД
            'pressStart1_traxial': worksheet_journal['CD_sigma1'][row],
            'pressStart2_traxial': worksheet_journal['CD_sigma2'][row],
            'pressStart3_traxial': worksheet_journal['CD_sigma3'][row],
            'E_0': worksheet_journal['CD_E0'][row],
            'E_50': worksheet_journal['E50'][row],
            'F_traxial': worksheet_journal['CD_fi'][row],
            'C_traxial': worksheet_journal['CD_c'][row],
            'E_rzg': worksheet_journal['E_rzg'][row],
            'CD_v_rzg': worksheet_journal['CD_v_rzg'][row],
            'Dilatanci': worksheet_journal['Dilatanci'][row],
            'CD_v': worksheet_journal['CD_v'][row],
            'CD_u1': worksheet_journal['CD_u1'][row],
            'CD_u2': worksheet_journal['CD_u2'][row],
            'CD_u3': worksheet_journal['CD_u3'][row],

            # Трехосники КН
            'pressStart1_traxial_CU': worksheet_journal['CU_sigma1'][row],
            'pressStart2_traxial_CU': worksheet_journal['CU_sigma2'][row],
            'pressStart3_traxial_CU': worksheet_journal['CU_sigma3'][row],
            'CU_E50': worksheet_journal['CU_E50'][row],
            'CU_fi': worksheet_journal['CU_fi'][row],
            'CU_c': worksheet_journal['CU_c'][row],

            # Трехосники НН
            'pressStart1_traxial_UU': worksheet_journal['UU_sigma1'][row],
            'pressStart2_traxial_UU': worksheet_journal['UU_sigma2'][row],
            'pressStart3_traxial_UU': worksheet_journal['UU_sigma3'][row],
            'UU_c': worksheet_journal['UU_c'][row],

            # OCR и компрессия
            'OCR': worksheet_journal['ocr'][row],
            'effective_press': worksheet_journal['P1'][row],
            'Eoed01_02_MPa': worksheet_journal['Eoed01_02_MPa'][row],
            'Eobs01_02_Mpa': worksheet_journal['Eobs01_02_Mpa'][row],

            # Одноплоскостной срез
            'F_unaxial': worksheet_journal['fi'][row],
            'C_unaxial': worksheet_journal['c'][row],

            ### Текущие давления на срезах, трехосниках
            'name_traxial_now': None,
            'name_unaxial_now': None,

            'PressStart_traxial_now': None,
            'PressStart_unaxial_now': None,

            'PressEnd_traxial_now': None,
            'PressEnd_unaxial_now': None,
        }

        _, pressStart1, pressStart2, pressStart3 = calculate_press_gost("SPS", organise_dct.get('F_unaxial'),
                                                                        organise_dct.get('C_unaxial'), organise_dct)
        organise_dct.setdefault('pressStart1_unaxial', pressStart1)
        organise_dct.setdefault('pressStart2_unaxial', pressStart2)
        organise_dct.setdefault('pressStart3_unaxial', pressStart3)

        pressEnd1, pressEnd2, pressEnd3 = calculate_values.SPS_value(organise_dct=organise_dct)
        organise_dct.setdefault('pressEnd1_unaxial', pressEnd1)
        organise_dct.setdefault('pressEnd2_unaxial', pressEnd2)
        organise_dct.setdefault('pressEnd3_unaxial', pressEnd3)




        organise_dct.setdefault('pressStart1_traxial', pressStart1)
        organise_dct.setdefault('pressStart2_traxial', pressStart2)
        organise_dct.setdefault('pressStart3_traxial', pressStart3)

        pressEnd1, pressEnd2, pressEnd3 = calculate_values.Traxial_value(organise_dct=organise_dct)
        organise_dct.setdefault('pressEnd1_traxial', pressEnd1)
        organise_dct.setdefault('pressEnd2_traxial', pressEnd2)
        organise_dct.setdefault('pressEnd3_traxial', pressEnd3)

        normative_analyze = GruntNormative(organise_dct=organise_dct)
        organise_dct = normative_analyze.return_parameters()

        type_grunt_schemas = {
            "traxial": {
                "gravel": 'gravel',
                "sand": 'sand',
                "sandy_loam": 'sandy_loam',
                "loam": 'loam',
                "clay": 'clay',
                        },
            "unaxial": {
                "gravel": 'gravel',
                "sand": 'sand',
                "sandy_loam": 'sandy_loam',
                "loam": 'loam',
                "clay": 'clay',
                        },
                        }

        # Графики по трехосникам КД
        if str(worksheet_journal['CD_sigma1'][row]) not in ["None", "nan"]:

            pathSave_traxial = os.path.join(pathSave, 'Трехосные_КД_ПП')
            if not os.path.exists(pathSave_traxial):
                os.mkdir(pathSave_traxial)
            organise_dct.update({'pathSave_traxial_CD': pathSave_traxial})

            # mode = 1 --- запись по 3 графика (деформация на первой прочности + 2 прочности с модулями)
            # mode = 2 --- запись 4 графиков (деформация + прочности с модулями)
            # mode = 3 --- запись 4 графиков (деформация с разгрузкой + прочности с модулями)
            # mode = 4 --- запись 3 графиков (деформация с разгрузкой на первой прочности + 2 прочности с модулями)

            mode = 2

            # Стандартная формула
            K_0 = 1 - math.sin(math.radians(organise_dct.get('F_traxial')))

            pressStart1 = organise_dct.get('pressStart1_traxial')
            pressStart2 = organise_dct.get('pressStart2_traxial')
            pressStart3 = organise_dct.get('pressStart3_traxial')

            pressEnd1 = organise_dct.get('pressEnd1_traxial')
            pressEnd2 = organise_dct.get('pressEnd2_traxial')
            pressEnd3 = organise_dct.get('pressEnd3_traxial')

            if mode == 1 or mode == 4:
                namesISP = ["graph1", "graph2", "graph3"]
                pressStarts = [pressStart1, pressStart2, pressStart3]
                pressEnds = [pressEnd1, pressEnd2, pressEnd3]

            if mode == 2 or mode == 3:
                namesISP = ["graph0", "graph1", "graph2", "graph3"]
                pressStarts = [pressStart1 * K_0, pressStart1, pressStart2, pressStart3]
                pressEnds = [pressEnd1, pressEnd1, pressEnd2, pressEnd3]

            for name, pressStart, pressEnd in zip(namesISP, pressStarts, pressEnds):

                organise_dct = normative_analyze.randomise()

                organise_dct.update({'name_traxial_now': name})
                organise_dct.update({'PressStart_traxial_now': pressStart})
                organise_dct.update({'PressEnd_traxial_now': pressEnd})

                if mode == 1:

                    DF_ISP, values_for_Excel = TPDSCF.start_TPDS_CF(organise_dct=organise_dct,
                                                                    dct_combination=dct_combination,
                                                                    type_grunt_schemas=type_grunt_schemas)
                if mode == 2:
                    if name != "graph0":
                        DF_ISP, values_for_Excel = TPDSCF.start_TPDS_CF(organise_dct=organise_dct,
                                                                    dct_combination=dct_combination,
                                                                    type_grunt_schemas=type_grunt_schemas)
                    else:
                        DF_ISP, values_for_Excel = TPDS50.start_TPDS_E50(organise_dct=organise_dct,
                                                                    dct_combination=dct_combination,
                                                                    type_grunt_schemas=type_grunt_schemas)
                if mode == 3:
                    if name != "graph0":
                        DF_ISP, values_for_Excel = TPDSCF.start_TPDS_CF(organise_dct=organise_dct,
                                                                    dct_combination=dct_combination,
                                                                    type_grunt_schemas=type_grunt_schemas)
                    else:
                        DF_ISP, values_for_Excel = TPDSRZG50.start_TPDS_RZG(organise_dct=organise_dct,
                                                                    dct_combination=dct_combination,
                                                                    type_grunt_schemas=type_grunt_schemas)
                if mode == 4:
                    if name == "graph1":
                        DF_ISP, values_for_Excel = TPDSRZG.start_TPDS_RZG(organise_dct=organise_dct,
                                                                    dct_combination=dct_combination,
                                                                    type_grunt_schemas=type_grunt_schemas)
                    if name != "graph1":
                        DF_ISP, _ = TPDSCF.start_TPDS_CF(organise_dct=organise_dct,
                                                         dct_combination=dct_combination,
                                                         type_grunt_schemas=type_grunt_schemas)

                if mode == 1:
                    if name == "graph1":
                        values_for_Excel_right = values_for_Excel
                if mode == 2:
                    if name == "graph0":
                        values_for_Excel_right = values_for_Excel
                if mode == 3:
                    if name == "graph0":
                        values_for_Excel_right = values_for_Excel
                if mode == 4:
                    if name == "graph1":
                        values_for_Excel_right = values_for_Excel

                save_DF.append(DF_ISP)

                print(f"{row}--{LAB_NO}--{name}--------DONE")

            start = time.time()
            read_shablons.shablonExcel_TPS_CD_4(row=row,
                                                dataframes=save_DF,
                                                organise_dct=organise_dct,
                                                values_Excel=values_for_Excel_right,
                                                mode=mode)
            stop = time.time()
            print(f'Время работы: {stop - start}')

        # Графики по срезам КД
        if str(worksheet_journal['fi'][row]) not in ["None", "nan"]:
            # Список для сохранения датафреймов, которые возвращаются из TPDS
            save_DF = []

            pathSave_unaxial = os.path.join(pathSave, 'Cрезы КД')
            if not os.path.exists(pathSave_unaxial):
                os.mkdir(pathSave_unaxial)
            organise_dct.update({'pathSave_unaxial': pathSave_unaxial})

            pressStart1 = organise_dct.get('pressStart1_unaxial')
            pressStart2 = organise_dct.get('pressStart2_unaxial')
            pressStart3 = organise_dct.get('pressStart3_unaxial')

            pressEnd1 = organise_dct.get('pressEnd1_unaxial')
            pressEnd2 = organise_dct.get('pressEnd2_unaxial')
            pressEnd3 = organise_dct.get('pressEnd3_unaxial')

            namesISP = ["graph1", "graph2", "graph3"]
            pressStarts = [pressStart1, pressStart2, pressStart3]
            pressEnds = [pressEnd1, pressEnd2, pressEnd3]

            for name, pressStart, pressEnd in zip(namesISP, pressStarts, pressEnds):

                organise_dct.update({'name_unaxial_now': name})
                organise_dct.update({'PressStart_unaxial_now': pressStart})
                organise_dct.update({'PressEnd_unaxial_now': pressEnd})

                NewDF, values_for_Excel_right = SPS.start_SPS_CD(organise_dct=organise_dct,
                                                                dct_combination=dct_combination,
                                                                type_grunt_schemas=type_grunt_schemas)

                save_DF.append(NewDF)

            read_shablons.shablonExcel_SPS_CD(row=row,
                                              dataframes=save_DF,
                                              organise_dct=organise_dct,
                                              values_Excel=values_for_Excel_right,
                                              )

        # Графики по компрессия КД
        if str(worksheet_journal['Eoed01_02_MPa'][row]) not in ["None", "nan"]:

            pathSave_spd = os.path.join(pathSave, 'Компрессии')
            if not os.path.exists(pathSave_spd):
                os.mkdir(pathSave_spd)
            organise_dct.update({'pathSave_spd': pathSave_spd})

            NewDF, values_for_Excel = SPD.SPD_start_new(organise_dct)

            read_shablons.shablonExcel_SPD(row, [NewDF], organise_dct, values_for_Excel)

        # Графики по компрессия КД
        if str(worksheet_journal['ocr'][row]) not in ["None", "nan"]:

            pathSave_OCR = os.path.join(pathSave, 'OCR')
            if not os.path.exists(pathSave_OCR):
                os.mkdir(pathSave_OCR)
            organise_dct.update({'pathSave_OCR': pathSave_OCR})

            values_for_Excel = OCR_ISP.OCR_start(organise_dct)

            read_shablons.shablonExcel_OCR(row=row,
                                           dataframes=[values_for_Excel.get('DATA_CASAGRANDE'), values_for_Excel.get('DATA_BEKKER')],
                                           organise_dct=organise_dct,
                                           values_Excel=values_for_Excel)

        print(f"{LAB_NO} -- DONE \n")
        print()
