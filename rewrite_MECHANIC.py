import math
import random
import os
import sys
import time
from typing import List, Any
import logging

import numpy as np

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
from GEOF.main_part.main_tools.normative_parameters import GruntNormative
from GEOF.BOT.DataDistributor_DB import DataDitributor as DD
from GEOF.main_part.main_tools.rewrite_GOST import IdentifySoil

from GEOF.main_part.log_isp_write import SPS_LOG
from GEOF.main_part.log_isp_write import SPD_LOG
from GEOF.main_part.log_isp_write import OCR_LOG
from GEOF.main_part.log_isp_write import TRAXIAL_LOG

from GEOF.main_part.logs_create import isp_SPD_OCR
from GEOF.main_part.logs_create import isp_SPS
from GEOF.main_part.logs_create import isp_TRAXIAL

logging.basicConfig(level=logging.INFO, filename="py_log.log",filemode="w",
                    format="%(asctime)s %(levelname)s %(message)s")

class MechanicStart:
    def __init__(self, worksheet_journal, id_user, dct_combination):
        self.worksheet_journal = worksheet_journal
        self.id_user = id_user
        self.dct_combination = dct_combination
        self.count_rows = len(self.worksheet_journal)

        if not self.worksheet_journal or not self.id_user or not self.dct_combination or not self.count_rows:
            logging.warning(f"Multiple parameters without value")
        logging.info(f"Initialize successful.")

    def main_cycle(self):
        """
        Запускает основной цикл, проходя по основному датафрейму для каждоый пробы
        :return:
        """
        for row in range(0, self.count_rows):
            self.LAB_NO = self.worksheet_journal['Ind_lab'][row],

            self.pathSave = self.create_main_path(row=row)
            self.organise_dct = self.create_dict_sample(row=row)

            self.analyze_soil = IdentifySoil(organise_dct=self.organise_dct)
            self.analyze_soil.aggregation_parameters()

            self.type_grunt_schemas = self.interactive_schemas_type()

            self.normative_analyze = GruntNormative(organise_dct=self.organise_dct)
            self.organise_dct = self.normative_analyze.return_parameters()


    def add_new_dir(self, name_dir, key_dict) -> str:
        """
        Добавляет новый путь для распределения испытания по папкам
        :param name_dir:
        :param key_dict:
        :return:
        """
        new_pathSave = os.path.join(self.pathSave, name_dir)
        if not os.path.exists(new_pathSave):
            os.mkdir(new_pathSave)
        self.organise_dct.update({key_dict: new_pathSave})
        logging.info(f"Additional path created and successfully added.")
        return new_pathSave

    def traxial_CC_isp_run(self, row, mode_main_isp, mode) -> bool:

        # mode = 'CC'
        F = self.organise_dct.get(f'F_traxial_{mode_main_isp}')
        C = self.organise_dct.get(f'C_traxial_{mode_main_isp}')

        logging.info(f"Traxial test: mode test - {mode_main_isp}, mode write - {mode}\n"
                     f"Main parameters: F - {F}, C - {C}")

        if F and C:
            save_DF = []
            pathSave_traxial = self.add_new_dir(name_dir='Трехосные_КД', key_dict='pathSave_traxial_CD')
            pressStarts, pressEnds = self.Traxial_press_value()

            match mode:
                case 1 | 4:
                    namesISP = ["graph1", "graph2", "graph3"]
                case 2 | 3:
                    namesISP = ["graph0", "graph1", "graph2", "graph3"]
                    K_0 = 1 - math.sin(math.radians(F)) if mode_main_isp == 'CC' else 1
                    pressStarts.insert(0, pressStarts[0] * K_0)
                    pressEnds.insert(0, pressEnds[0])

            for name, start, end in zip(namesISP, pressStarts, pressEnds):
                match mode:
                    case 1:
                        DF_ISP, values_for_Excel = TPDSCF.start_TPDS_CF(organise_dct=self.organise_dct,
                                                                        dct_combination=dct_combination,
                                                                        type_grunt_schemas=self.type_grunt_schemas)
                    case 2:
                        if name != "graph0":
                            DF_ISP, _ = TPDSCF.start_TPDS_CF(organise_dct=self.organise_dct,
                                                                        dct_combination=dct_combination,
                                                                        type_grunt_schemas=self.type_grunt_schemas)
                        else:
                            DF_ISP, values_for_Excel = TPDS50.start_TPDS_E50(organise_dct=self.organise_dct,
                                                                        dct_combination=dct_combination,
                                                                        type_grunt_schemas=self.type_grunt_schemas)
                    case 3:
                        if name != "graph0":
                            DF_ISP, _ = TPDSCF.start_TPDS_CF(organise_dct=self.organise_dct,
                                                                        dct_combination=dct_combination,
                                                                        type_grunt_schemas=self.type_grunt_schemas)
                        else:
                            DF_ISP, values_for_Excel = TPDSRZG50.start_TPDS_RZG(organise_dct=self.organise_dct,
                                                                        dct_combination=dct_combination,
                                                                        type_grunt_schemas=self.type_grunt_schemas)
                    case 4:
                        if name != "graph1":
                            DF_ISP, _ = TPDSCF.start_TPDS_CF(organise_dct=self.organise_dct,
                                                             dct_combination=dct_combination,
                                                             type_grunt_schemas=self.type_grunt_schemas)
                        if name == "graph1":
                            DF_ISP, values_for_Excel = TPDSRZG.start_TPDS_RZG(organise_dct=self.organise_dct,
                                                                        dct_combination=dct_combination,
                                                                        type_grunt_schemas=self.type_grunt_schemas)
                logging.info(f"The graph - {name} is succesfully created.")

                save_DF.append(DF_ISP)

            read_shablons.shablonExcel_TPS_CD_4(row=row,
                                                dataframes=save_DF,
                                                organise_dct=self.organise_dct,
                                                values_Excel=values_for_Excel,
                                                mode=mode,
                                                mode_traxial='КД',)
        return True


    def interactive_schemas_type(self) -> dict:
        """
        Отвечает за распределение схем по типам грунта
        :return:
        """
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

        logging.info(f"For {self.LAB_NO} initialize type grunt schemas complete.")

        return type_grunt_schemas

    def create_main_path(self, row) -> str:
        """
        Создает основной путь, который везде используется
        :return:
        """
        # Создание папки для складирования испытаний в объекте
        pathSave = os.path.join(f"..\\GEOF\\prot\\{self.id_user}")
        if not os.path.exists(pathSave):
            os.mkdir(pathSave)

        nameObject = self.worksheet_journal['nameObject'][row][0] if isinstance(self.worksheet_journal['nameObject'][row], tuple) else self.worksheet_journal['nameObject'][row]
        pathSave = os.path.join(f"..\\GEOF\\prot\\{self.id_user}\\{nameObject}")
        if not os.path.exists(pathSave):
            os.mkdir(pathSave)

        logging.info(f"Path create: {pathSave}.")

        return pathSave

    def create_dict_sample(self, row) -> dict:
        """
        Возвращает словарь, для каждой строки
        :param row:
        :return:
        """
        organise_dct = {
            # Распаковка параметров из Датафрейма
            'LAB_NO': self.worksheet_journal['Ind_lab'][row],
            'N_IG': self.worksheet_journal['Ind'][row],
            'boreHole': self.worksheet_journal['BH'][row],
            'nameSoil': self.worksheet_journal['name_soil'][row][0] if isinstance(self.worksheet_journal['name_soil'][row], tuple) else self.worksheet_journal['name_soil'][row],
            'depth': self.worksheet_journal['Depth'][row],
            # Дата получение объекта подлежащего испытаниям
            'date_isp_object': self.worksheet_journal['data_f'][row],
            # Дата испытания
            'date_isp': self.worksheet_journal['data_test'][row],
            # Дата протокола
            'date_protocol': self.worksheet_journal['data_prot'][row],
            # Номер протокола
            'number_protocol': self.worksheet_journal['Np'][row],
            # Заказчик
            'nameClient': self.worksheet_journal['nameClient'][row][0] if isinstance(self.worksheet_journal['nameObject'][row], tuple) else self.worksheet_journal['nameClient'][row],
            # Объект
            'nameObject': self.pathSave,

            'pathSave': None,
            'pathSave_traxial_CD': None,
            'pathSave_traxial_CU': None,
            'pathSave_traxial_UU': None,

            'pathSave_unaxial': None,
            'pathSave_spd': None,
            'pathSave_OCR': None,

            # Физические параметры для протокола
            'We': self.worksheet_journal['We'][row],
            'p': self.worksheet_journal['p'][row],
            'ps': self.worksheet_journal['ps'][row],
            'e': self.worksheet_journal['e'][row],
            'IP': self.worksheet_journal['IP'][row],
            'IL': self.worksheet_journal['IL'][row],
            'Sr': self.worksheet_journal['Sr'][row],
            'WL': self.worksheet_journal['WL'][row],
            'WP': self.worksheet_journal['WP'][row],
            'Ir': self.worksheet_journal['Ir'][row],

            # Грансостав
            'GGR10': self.worksheet_journal['GGR10'][row],
            'G10_5': self.worksheet_journal['G10_5'][row],
            'G5_2': self.worksheet_journal['G5_2'][row],
            'G2_1': self.worksheet_journal['G2_1'][row],
            'G1_05': self.worksheet_journal['G1_05'][row],
            'G05_025': self.worksheet_journal['G05_025'][row],
            'G025_01': self.worksheet_journal['G025_01'][row],
            'G01_005': self.worksheet_journal['G01_005'][row],
            'G005_001': self.worksheet_journal['G005_001'][row],
            'G001_0002': self.worksheet_journal['G001_0002'][row],
            'G0002': self.worksheet_journal['G0002'][row],

            # Трехосники КД
            'pressStart1_traxial_CC': self.worksheet_journal['CD_sigma1'][row],
            'pressStart2_traxial_CC': self.worksheet_journal['CD_sigma2'][row],
            'pressStart3_traxial_CC': self.worksheet_journal['CD_sigma3'][row],
            'pressEnd1_traxial_CC': None,
            'pressEnd2_traxial_CC': None,
            'pressEnd3_traxial_CC': None,
            'E_0': self.worksheet_journal['CD_E0'][row],
            'E_50': self.worksheet_journal['E50'][row],
            'F_traxial_CC': self.worksheet_journal['CD_fi'][row],
            'C_traxial_CC': self.worksheet_journal['CD_c'][row],
            'E_rzg': self.worksheet_journal['E_rzg'][row],
            'CD_v_rzg': self.worksheet_journal['CD_v_rzg'][row],
            't_100': self.worksheet_journal['t_100'][row],
            'Dilatanci': self.worksheet_journal['Dilatanci'][row],
            'CD_v': self.worksheet_journal['CD_v'][row],
            'CD_u1': self.worksheet_journal['CD_u1'][row],
            'CD_u2': self.worksheet_journal['CD_u2'][row],
            'CD_u3': self.worksheet_journal['CD_u3'][row],

            # Трехосники КН
            'pressStart1_traxial_CU': self.worksheet_journal['CU_sigma1'][row],
            'pressStart2_traxial_CU': self.worksheet_journal['CU_sigma2'][row],
            'pressStart3_traxial_CU': self.worksheet_journal['CU_sigma3'][row],
            'pressEnd1_traxial_CU': None,
            'pressEnd2_traxial_CU': None,
            'pressEnd3_traxial_CU': None,
            'F_traxial_CU': self.worksheet_journal['CU_fi'][row],
            'C_traxial_CU': self.worksheet_journal['CU_c'][row],

            # Трехосники НН
            'pressStart1_traxial_UU': self.worksheet_journal['UU_sigma1'][row],
            'pressStart2_traxial_UU': self.worksheet_journal['UU_sigma2'][row],
            'pressStart3_traxial_UU': self.worksheet_journal['UU_sigma3'][row],
            'pressEnd1_traxial_UU': None,
            'pressEnd2_traxial_UU': None,
            'pressEnd3_traxial_UU': None,
            'UU_c': self.worksheet_journal['UU_c'][row],

            # OCR и компрессия
            'OCR': self.worksheet_journal['ocr'][row],
            'effective_press': self.worksheet_journal['P1'][row],
            'Eoed01_02_MPa': self.worksheet_journal['Eoed01_02_MPa'][row],
            'Eobs01_02_Mpa': self.worksheet_journal['Eobs01_02_Mpa'][row],

            # Консолидация по компрессии
            'Cv': self.worksheet_journal['Cv'][row],

            # Одноплоскостной срез
            'F_unaxial': self.worksheet_journal['fi'][row],
            'C_unaxial': self.worksheet_journal['c'][row],
            'pressStart1_unaxial': self.worksheet_journal['UN_sigma1'][row],
            'pressStart2_unaxial': self.worksheet_journal['UN_sigma2'][row],
            'pressStart3_unaxial': self.worksheet_journal['UN_sigma3'][row],
            'pressEnd1_unaxial': None,
            'pressEnd2_unaxial': None,
            'pressEnd3_unaxial': None,

            ### Текущие давления на срезах, трехосниках
            'name_traxial_now': None,
            'name_unaxial_now': None,

            'PressStart_traxial_now': None,
            'PressStart_unaxial_now': None,

            'PressEnd_traxial_now': None,
            'PressEnd_unaxial_now': None,
        }

        logging.info(f"Sample {row} create successful.")

        return organise_dct

    def Unaxial_press_value(self) -> (list[float | None], list[float | None]):
        """
        Возвращает значения конечных давления на одноплоскостном срезе
        :return:
        """
        F = self.organise_dct.get('F_unaxial')
        C = self.organise_dct.get('C_unaxial')

        pressStart1, pressStart2, pressStart3 = self.analyze_soil.GOST_SPS()

        pressEnd1, pressEnd2, pressEnd3 = None, None, None

        if F and C:

            Rad = math.radians(F)

            valueRANDOM_to_press2 = random.choice([x for x in [random.randint(-10, 10) / 1000 for x in range(5)] if x != 0.0])

            pressEnd1 = (pressStart1 * math.tan(Rad) + C) - valueRANDOM_to_press2 / 2
            pressEnd2 = (pressStart2 * math.tan(Rad) + C) + valueRANDOM_to_press2
            pressEnd3 = (pressStart3 * math.tan(Rad) + C) - valueRANDOM_to_press2 / 2

            tan_RAD_F = ((3 * (pressStart1 * pressEnd1 + pressStart2 * pressEnd2 + pressStart3 * pressEnd3) -
                          (pressStart1 + pressStart2 + pressStart3) * (pressEnd1 + pressEnd2 + pressEnd3))
                         /
                         (3 * (pressStart1 ** 2 + pressStart2 ** 2 + pressStart3 ** 2) - (
                                 pressStart1 + pressStart2 + pressStart3) ** 2))

            F_CALC = math.degrees(math.atan(tan_RAD_F))

        self.organise_dct.update({'pressStart1_unaxial': pressStart1,
                                  'pressStart2_unaxial': pressStart2,
                                  'pressStart3_unaxial': pressStart3,
                                  'pressEnd1_unaxial': pressEnd1,
                                  'pressEnd2_unaxial': pressEnd2,
                                  'pressEnd3_unaxial': pressEnd3,})

        logging.info(f"Unaxial pressures are selected for the {self.LAB_NO}:\n"
                     f"Press Start 1: {pressStart1}, Press End 1: {pressEnd1}\n"
                     f"Press Start 2: {pressStart2}, Press End 2: {pressEnd2}\n"
                     f"Press Start 3: {pressStart3}, Press End 3: {pressEnd3}\n")

        return [pressStart1, pressStart2, pressStart3], [pressEnd1, pressEnd2, pressEnd3]

    def Traxial_press_value(self, mode='CC') -> (list[float | None], list[float | None]):
        """
        Возвращает значения конечных давления на трехосном испытании КД и КН
        :return:
        """
        F = self.organise_dct.get(f'F_traxial_{mode}')
        C = self.organise_dct.get(f'C_traxial_{mode}')

        pressStart1, pressStart2, pressStart3 = self.analyze_soil.GOST_TP(mode=mode)

        pressEnd1, pressEnd2, pressEnd3 = None, None, None

        if F and C:
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

        self.organise_dct.update({f'pressStart1_traxial_{mode}': pressStart1,
                                  f'pressStart2_traxial_{mode}': pressStart2,
                                  f'pressStart3_traxial_{mode}': pressStart3,
                                  f'pressEnd1_traxial_{mode}': pressEnd1,
                                  f'pressEnd2_traxial_{mode}': pressEnd2,
                                  f'pressEnd3_traxial_{mode}': pressEnd3,})

        logging.info(f"Traxial pressures are selected for the {self.LAB_NO}:\n"
                     f"Press Start 1: {pressStart1}, Press End 1: {pressEnd1}\n"
                     f"Press Start 2: {pressStart2}, Press End 2: {pressEnd2}\n"
                     f"Press Start 3: {pressStart3}, Press End 3: {pressEnd3}\n")

        return [pressStart1, pressStart2, pressStart3], [pressEnd1, pressEnd2, pressEnd3]


if __name__ == "__main__":
    us_id = '356379915'
    # Скачиваем документ по его file_id
    file_url = f'C:\\Users\\MSI GP66\\PycharmProjects\\dj_project\\GEOF\\Data.xlsx'

    ### Удалить строки без механики
    deleteRows = main_tools.ExcelModules(
        path=file_url,
        sheetName='Sheet1',
        howRowsSkip=5,
        howColumnSkip=0
    )

    deleteRows.DeleteDefinitionRows(['P1', 'P_r', 'ocr',
                                     'fi', 'c',
                                     'Eoed01_02_MPa', 'Eobs01_02_Mpa',
                                     # 'CD_sigma1', 'CD_sigma2', 'CD_sigma3',
                                     'CD_E0', 'E50', 'CD_fi', 'CD_c',
                                     'CU_sigma1', 'CU_sigma2', 'CU_sigma3', 'CU_fi', 'CU_c',
                                     'UU_sigma1', 'UU_sigma2', 'UU_sigma3', 'UU_c',
                                     ], [None, np.NAN, "None", np.NaN, "nan"])

    deleteRows.replaceChar(',', '.', ['Depth', 'We', 'ps', 'p', 'pd', 'n', 'e', 'Sr', 'WL', 'WP', 'IP', 'IL', 'Ir',
                                      'P1', 'P_r', 'ocr',
                                      'fi', 'c', 'UN_sigma1', 'UN_sigma2', 'UN_sigma3',
                                      'Eoed01_02_MPa', 'Eobs01_02_Mpa',
                                      'CD_sigma1', 'CD_sigma2', 'CD_sigma3',
                                      'CD_u1', 'CD_u2', 'CD_u3',
                                      'CD_v',
                                      'CD_E0', 'E50', 'CD_fi', 'CD_c',
                                      'CU_sigma1', 'CU_sigma2', 'CU_sigma3', 'CU_fi', 'CU_c',
                                      'UU_sigma1', 'UU_sigma2', 'UU_sigma3', 'UU_c',
                                      'Dilatanci', 'E_rzg', 'CD_v_rzg',
                                      'GGR10', 'G10_5', 'G5_2', 'G2_1', 'G1_05', 'G05_025', 'G025_01',
                                      'G01_005', 'G005_001', 'G001_0002', 'G0002',
                                      ], typeRewrite='float64')

    worksheet_journal = deleteRows.returnDATAFRAME()

    distribut = DD(id_people=us_id, path_to_data='..\\GEOF\\BOT\\geofvck.db')
    distribut.check_schemas_people()
    dct_combination = distribut.data_give()

    test = MechanicStart(worksheet_journal, us_id, dct_combination)
    test.main_cycle()

