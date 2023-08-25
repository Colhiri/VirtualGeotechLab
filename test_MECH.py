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


class MechanicStart:
    def __init__(self, worksheet_journal, id_user, dct_combination):
        self.worksheet_journal = worksheet_journal
        self.id_user = id_user
        self.dct_combination = dct_combination
        self.count_rows = len(self.worksheet_journal)

        logging.basicConfig(level=logging.INFO, filename="Process write isp.log", filemode="w",
                            format="%(asctime)s %(levelname)s %(message)s")

        if not self.id_user or not self.dct_combination or not self.count_rows:
            logging.warning(f"Multiple parameters without value")
        logging.info(f"Initialize successful.")

    def main_cycle(self):
        """
        Запускает основной цикл, проходя по основному датафрейму для каждоый пробы
        :return:
        """
        for row in range(0, self.count_rows):
            self.LAB_NO = self.worksheet_journal['LAB_NO'][row],

            self.pathSave = self.create_main_path(row=row)
            self.organise_dct = self.create_dict_sample(row=row)

            self.analyze_soil = IdentifySoil(organise_dct=self.organise_dct)
            self.analyze_soil.aggregation_parameters()

            self.type_grunt_schemas = self.interactive_schemas_type()

            self.normative_analyze = GruntNormative(organise_dct=self.organise_dct)
            self.organise_dct = self.normative_analyze.return_parameters()

            self.traxial_isp_run(row=row, mode_main_isp='CD', mode=1)

            self.unaxial_sps_run(row=row)

            self.comp_isp_run(row=row)

            self.OCR_isp_run(row=row)

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

    def traxial_isp_run(self, row, mode_main_isp, mode):

        F = self.organise_dct.get(f'F_traxial_{mode_main_isp}')
        C = self.organise_dct.get(f'C_traxial_{mode_main_isp}')

        logging.info(f"Traxial test: mode test - {mode_main_isp}, mode write - {mode}\n"
                     f"Main parameters: F - {F}, C - {C}")
        if not C:
            logging.info(f"Traxial test is not start. Values F or C is missing.")
            return

        save_DF = []
        pathSave_traxial = self.add_new_dir(name_dir=f'Traxial_{mode_main_isp}',
                                            key_dict=f'pathSave_traxial_{mode_main_isp}')
        pressStarts, pressEnds = self.Traxial_press_value()

        ['CC', 'CU'], ['CC', 'UU'], ['CC'], ['UU'], ['CU']

        match mode_main_isp:
            case 'CU' | 4:
                namesISP = ["graph1", "graph2", "graph3"]
            case 2 | 3:
                namesISP = ["graph0", "graph1", "graph2", "graph3"]
                K_0 = 1 - math.sin(math.radians(F)) if mode_main_isp == 'CC' else 1
                pressStarts.insert(0, pressStarts[0] * K_0)
                pressEnds.insert(0, pressEnds[0])

        for name, start, end in zip(namesISP, pressStarts, pressEnds):
            self.organise_dct.update({'name_traxial_now': name})
            self.organise_dct.update({'PressStart_traxial_now': start})
            self.organise_dct.update({'PressEnd_traxial_now': end})
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
                                            mode_traxial='КД', )

    def unaxial_sps_run(self, row):
        """
        Создает испытание одноплоскостного среза
        :param row:
        :return:
        """
        F = self.organise_dct.get(f'F_unaxial')
        C = self.organise_dct.get(f'C_unaxial')

        if not F and not C:
            logging.info(f"Unaxial test is not start. Values F or C is missing.")
            return

        pathSave_unaxial = self.add_new_dir(name_dir=f'Unaxial',
                                            key_dict=f'pathSave_unaxial')
        pressStarts, pressEnds = self.Unaxial_press_value()

        logging.info(f"Unaxial test start.")

        namesISP = ["graph1", "graph2", "graph3"]
        save_DF = []
        for name, pressStart, pressEnd in zip(namesISP, pressStarts, pressEnds):
            self.organise_dct.update({'name_unaxial_now': name})
            self.organise_dct.update({'PressStart_unaxial_now': pressStart})
            self.organise_dct.update({'PressEnd_unaxial_now': pressEnd})

            NewDF, values_for_Excel_right = SPS.start_SPS_CD(organise_dct=self.organise_dct,
                                                             dct_combination=dct_combination,
                                                             type_grunt_schemas=self.type_grunt_schemas)

            dataframe_ISP = isp_SPS.ISP_SPS(dataframe_isp=NewDF,
                                            organise_dct=self.organise_dct)

            SPS_LOG.write_log(row=row,
                              dataframe=dataframe_ISP,
                              organise_dct=self.organise_dct)

            save_DF.append(NewDF)

            logging.info(f"Graph with start press - {pressStart} is done.")

        logging.info(f"Prepare to excel write protocol.")
        read_shablons.shablonExcel_SPS_CD(row=row,
                                          dataframes=save_DF,
                                          organise_dct=self.organise_dct,
                                          values_Excel=values_for_Excel_right,
                                          )
        logging.info(f"Protocol create. End unaxial test.")

    def comp_isp_run(self, row):

        Eoed = self.organise_dct.get(f'Eoed')

        if not Eoed:
            logging.info(f"Compression test is not start. Value Eoed is missing.")
            return

        logging.info(f"Compression test start.")

        pathSave_spd = self.add_new_dir(name_dir=f'Compression',
                                        key_dict=f'pathSave_spd')

        test = SPD.compression(organise_dct=self.organise_dct)
        test.aggregation()
        df = test.ret_dataframe()
        values_for_Excel = test.ret_values_to_excel()

        dataframe_ISP = isp_SPD_OCR.ISP_SPD(dataframe_isp=df,
                                            organise_dct=self.organise_dct)

        SPD_LOG.write_log(row=row,
                          dataframe=dataframe_ISP,
                          organise_dct=self.organise_dct)

        logging.info(f"Prepare to excel write protocol.")

        read_shablons.shablonExcel_SPD(row, [df], self.organise_dct, values_for_Excel)

        logging.info(f"Protocol create. End compression test.")

    def OCR_isp_run(self, row):

        OCR = self.organise_dct.get(f'OCR')

        if not OCR:
            logging.info(f"OCR test is not start. Value OCR is missing.")
            return

        logging.info(f"OCR test start.")

        pathSave_OCR = self.add_new_dir(name_dir=f'OCR',
                                        key_dict=f'pathSave_OCR')

        values_for_Excel = OCR_ISP.OCR_start(self.organise_dct)

        NewDF = values_for_Excel.get('DATA_CASAGRANDE')

        dataframe_ISP = isp_SPD_OCR.ISP_SPD(dataframe_isp=NewDF,
                                            organise_dct=self.organise_dct)

        OCR_LOG.write_log(row=row,
                          dataframe=dataframe_ISP,
                          organise_dct=self.organise_dct)

        logging.info(f"Prepare to excel write protocol.")

        read_shablons.shablonExcel_OCR(row=row,
                                       dataframes=[values_for_Excel.get('DATA_CASAGRANDE'),
                                                   values_for_Excel.get('DATA_BEKKER')],
                                       organise_dct=self.organise_dct,
                                       values_Excel=values_for_Excel)

        logging.info(f"Protocol create. End OCR test.")

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

        nameObject = self.worksheet_journal['nameObject'][row][0] if isinstance(
            self.worksheet_journal['nameObject'][row], tuple) else self.worksheet_journal['nameObject'][row]
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
        organise_dct = self.worksheet_journal.iloc[row].to_dict()

        for key, item in organise_dct.items():
            if isinstance(item, float | int) and math.isnan(item):
                organise_dct.update({key: None})

        organise_dct.update({
            'pathSave': None,
            'pathSave_traxial_CD': None,
            'pathSave_traxial_CU': None,
            'pathSave_traxial_UU': None,

            'pathSave_unaxial': None,
            'pathSave_spd': None,
            'pathSave_OCR': None,

            'End1_traxial_CD': None,
            'End2_traxial_CD': None,
            'End3_traxial_CD': None,

            'End1_traxial_CU': None,
            'End2_traxial_CU': None,
            'End3_traxial_CU': None,

            'End1_traxial_UU': None,
            'End2_traxial_UU': None,
            'End3_traxial_UU': None,

            'End1_unaxial': None,
            'End2_unaxial': None,
            'End3_unaxial': None,

            'name_traxial_now': None,
            'name_unaxial_now': None,

            'PressStart_traxial_now': None,
            'PressStart_unaxial_now': None,

            'PressEnd_traxial_now': None,
            'PressEnd_unaxial_now': None,
        })

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

            valueRANDOM_to_press2 = random.choice(
                [x for x in [random.randint(-10, 10) / 1000 for x in range(5)] if x != 0.0])

            pressEnd1 = (pressStart1 * math.tan(Rad) + C) - valueRANDOM_to_press2 / 2
            pressEnd2 = (pressStart2 * math.tan(Rad) + C) + valueRANDOM_to_press2
            pressEnd3 = (pressStart3 * math.tan(Rad) + C) - valueRANDOM_to_press2 / 2

            tan_RAD_F = ((3 * (pressStart1 * pressEnd1 + pressStart2 * pressEnd2 + pressStart3 * pressEnd3) -
                          (pressStart1 + pressStart2 + pressStart3) * (pressEnd1 + pressEnd2 + pressEnd3))
                         /
                         (3 * (pressStart1 ** 2 + pressStart2 ** 2 + pressStart3 ** 2) - (
                                 pressStart1 + pressStart2 + pressStart3) ** 2))

            F_CALC = math.degrees(math.atan(tan_RAD_F))

        self.organise_dct.update({'Start1_unaxial': pressStart1,
                                  'Start2_unaxial': pressStart2,
                                  'Start3_unaxial': pressStart3,
                                  'End1_unaxial': pressEnd1,
                                  'End2_unaxial': pressEnd2,
                                  'End3_unaxial': pressEnd3, })

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

        self.organise_dct.update({f'Start1_traxial_{mode}': pressStart1,
                                  f'Start2_traxial_{mode}': pressStart2,
                                  f'Start3_traxial_{mode}': pressStart3,
                                  f'End1_traxial_{mode}': pressEnd1,
                                  f'End2_traxial_{mode}': pressEnd2,
                                  f'End3_traxial_{mode}': pressEnd3, })

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

    deleteRows.DeleteDefinitionRows(['OCR', 'effective_press', 'Start1_unaxial', 'Start2_unaxial', 'Start3_unaxial',
                                     'F_unaxial', 'C_unaxial', 'Eoed', 'Ecas', 'Erzg_comp', 'press_rzg_comp', 'Cv',
                                     't_100', 'Dilatanci', 'E_rzg', 'CD_v_rzg', 'Start1_traxial_CD', 'CD_u1',
                                     'Start2_traxial_CD', 'CD_u2', 'Start3_traxial_CD', 'CD_u3', 'CD_v', 'E_0',
                                     'E_50', 'F_traxial_CD', 'C_traxial_CD', 'Start1_traxial_CU', 'Start2_traxial_CU',
                                     'Start3_traxial_CU', 'F_traxial_CU', 'C_traxial_CU', 'Start1_traxial_UU',
                                     'Start2_traxial_UU', 'Start3_traxial_UU', 'UU_c'
                                     ], [None, np.NAN, "None", np.NaN, "nan"])

    deleteRows.replaceChar(',', '.', ['depth', 'We', 'ps', 'p', 'pd', 'n', 'e', 'Sr', 'WL', 'WP', 'IP', 'IL', 'Ir',
                                      'OCR', 'effective_press', 'Start1_unaxial', 'Start2_unaxial', 'Start3_unaxial',
                                      'F_unaxial', 'C_unaxial', 'Eoed', 'Ecas', 'Erzg_comp', 'press_rzg_comp', 'Cv',
                                      't_100', 'Dilatanci', 'E_rzg', 'CD_v_rzg', 'Start1_traxial_CD', 'CD_u1',
                                      'Start2_traxial_CD', 'CD_u2', 'Start3_traxial_CD', 'CD_u3', 'CD_v', 'E_0',
                                      'E_50', 'F_traxial_CD', 'C_traxial_CD', 'Start1_traxial_CU', 'Start2_traxial_CU',
                                      'Start3_traxial_CU', 'F_traxial_CU', 'C_traxial_CU', 'Start1_traxial_UU',
                                      'Start2_traxial_UU', 'Start3_traxial_UU', 'UU_c', 'GGR10', 'G10_5', 'G5_2',
                                      'G2_1', 'G1_05', 'G05_025', 'G025_01', 'G01_005', 'G005_001', 'G001_0002', 'G0002'
                                      ], typeRewrite='float64')

    worksheet_journal = deleteRows.returnDATAFRAME()

    distribut = DD(id_people=us_id, path_to_data='..\\GEOF\\BOT\\geofvck.db')
    distribut.check_schemas_people()
    dct_combination = distribut.data_give()

    test = MechanicStart(worksheet_journal, us_id, dct_combination)
    test.main_cycle()

