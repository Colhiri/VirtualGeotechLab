import math
import random
import os
import sys
import time

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
from GEOF.main_part.main_tools import calculate_press_gost
from GEOF.main_part.main_tools.normative_parameters import GruntNormative
from GEOF.BOT.DataDistributor_DB import DataDitributor as DD

from GEOF.main_part.log_isp_write import SPS_LOG
from GEOF.main_part.log_isp_write import SPD_LOG
from GEOF.main_part.log_isp_write import OCR_LOG
from GEOF.main_part.log_isp_write import TRAXIAL_LOG

from GEOF.main_part.logs_create import isp_SPD_OCR
from GEOF.main_part.logs_create import isp_SPS
from GEOF.main_part.logs_create import isp_TRAXIAL

from typing import List, Any



class MechanicStart:
    def __init__(self, worksheet_journal, id_user, dct_combination):
        self.worksheet_journal = worksheet_journal
        self.id_user = id_user
        self.dct_combination = dct_combination
        self.count_rows = len(self.worksheet_journal)

    def main_cycle(self):
        """
        Запускает основной цикл, проходя по основному датафрейму для каждоый пробы
        :return:
        """
        for row in range(0, self.count_rows):
            self.create_main_path(row=row)
            self.create_dict_test(row=row)

    def interactive_schemas_type(self):
        """
        Отвечает за распределение схем по типам грунта
        :return:
        """
        self.type_grunt_schemas = {
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

    def create_main_path(self, row) -> str:
        """
        Создает основной путь, который везде используется
        :return:
        """
        # Создание папки для складирования испытаний в объекте
        self.pathSave = os.path.join(f"..\\GEOF\\prot\\{self.id_user}")
        if not os.path.exists(self.pathSave):
            os.mkdir(self.pathSave)

        nameObject = self.worksheet_journal['nameObject'][row][0] if isinstance(self.worksheet_journal['nameObject'][row], tuple) else self.worksheet_journal['nameObject'][row]
        self.pathSave = os.path.join(f"..\\GEOF\\prot\\{self.id_user}\\{nameObject}")
        if not os.path.exists(self.pathSave):
            os.mkdir(self.pathSave)

        return self.pathSave

    def create_dict_test(self, row) -> dict:
        """
        Возвращает словарь, для каждой строки
        :param row:
        :return:
        """
        self.organise_dct = {
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
            'pressStart1_traxial': self.worksheet_journal['CD_sigma1'][row],
            'pressStart2_traxial': self.worksheet_journal['CD_sigma2'][row],
            'pressStart3_traxial': self.worksheet_journal['CD_sigma3'][row],
            'E_0': self.worksheet_journal['CD_E0'][row],
            'E_50': self.worksheet_journal['E50'][row],
            'F_traxial': self.worksheet_journal['CD_fi'][row],
            'C_traxial': self.worksheet_journal['CD_c'][row],
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
            'CU_fi': self.worksheet_journal['CU_fi'][row],
            'CU_c': self.worksheet_journal['CU_c'][row],

            # Трехосники НН
            'pressStart1_traxial_UU': self.worksheet_journal['UU_sigma1'][row],
            'pressStart2_traxial_UU': self.worksheet_journal['UU_sigma2'][row],
            'pressStart3_traxial_UU': self.worksheet_journal['UU_sigma3'][row],
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

            ### Текущие давления на срезах, трехосниках
            'name_traxial_now': None,
            'name_unaxial_now': None,

            'PressStart_traxial_now': None,
            'PressStart_unaxial_now': None,

            'PressEnd_traxial_now': None,
            'PressEnd_unaxial_now': None,
        }

        return self.organise_dct

    def analyze_soil(self):
        """

        :return:
        """

    def press_end_SPS(self) -> list[float | None]:
        """
        Возвращает значения конечных давления на одноплоскостном срезе
        :return:
        """
        F = self.organise_dct.get('F_unaxial')
        C = self.organise_dct.get('C_unaxial')
        pressStart1 = self.organise_dct.get('pressStart1_unaxial')
        pressStart2 = self.organise_dct.get('pressStart2_unaxial')
        pressStart3 = self.organise_dct.get('pressStart3_unaxial')

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

        self.organise_dct.update({})

        return [pressEnd1, pressEnd2, pressEnd3]


    def calculate_press(self):
        """
        Обновляет значения давлений в основном словаре для всех возможных испытаний
        :return:
        """
        _, pressStart1, pressStart2, pressStart3 = calculate_press_gost("SPS", self.organise_dct)
        self.organise_dct.setdefault('pressStart1_unaxial', pressStart1)
        self.organise_dct.setdefault('pressStart2_unaxial', pressStart2)
        self.organise_dct.setdefault('pressStart3_unaxial', pressStart3)

        pressEnd1, pressEnd2, pressEnd3 = calculate_values.SPS_value(organise_dct=self.organise_dct)
        self.organise_dct.setdefault('pressEnd1_unaxial', pressEnd1)
        self.organise_dct.setdefault('pressEnd2_unaxial', pressEnd2)
        self.organise_dct.setdefault('pressEnd3_unaxial', pressEnd3)

        self.organise_dct.setdefault('pressStart1_traxial', pressStart1)
        self.organise_dct.setdefault('pressStart2_traxial', pressStart2)
        self.organise_dct.setdefault('pressStart3_traxial', pressStart3)

        pressEnd1, pressEnd2, pressEnd3 = calculate_values.Traxial_value(organise_dct=self.organise_dct)
        self.organise_dct.setdefault('pressEnd1_traxial', pressEnd1)
        self.organise_dct.setdefault('pressEnd2_traxial', pressEnd2)
        self.organise_dct.setdefault('pressEnd3_traxial', pressEnd3)

        normative_analyze = GruntNormative(organise_dct=self.organise_dct)
        self.organise_dct = normative_analyze.return_parameters()
