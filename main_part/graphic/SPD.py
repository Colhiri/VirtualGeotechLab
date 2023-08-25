import logging
import random
from typing import Any

import matplotlib.pyplot as plt
import pandas as pd
import scipy.stats as stats

from isp_test.main_tools import bezier_curve


class compression:
    def __init__(self, organise_dct):
        self.organise_dct = organise_dct
        self.IP = self.organise_dct.get('IP')
        self.IL = self.organise_dct.get('IL')
        self.e = self.organise_dct.get('e')
        self.p = self.organise_dct.get('p')
        self.g = 9.80665
        self.depth = self.organise_dct.get('depth')
        self.press_rzg = self.organise_dct.get('press_rzg_comp')

        self.Eoed = self.organise_dct.get('Eoed')  # Основной одометрический
        self.Ecas = self.organise_dct.get('Ecas')  # Касательный
        self.Erzg = self.organise_dct.get('Erzg')  # Касательный

        logging.basicConfig(level=logging.INFO, filename="compression_isp.log", filemode="w",
                            format="%(asctime)s %(levelname)s %(message)s")

        if not self.IP or not self.IL or not self.e or not self.p or not self.depth:
            logging.warning(f"Multiple parameters without value")
        logging.info(
            f"Initialize successful: Depth: {self.depth}, IP: {self.IP}, IL: {self.IL}, e: {self.e}, p: {self.p}.")

    def coefficeients(self) -> (float, float):
        """
        Возвращает moed и beta исходя из типа грунта
        :return:
        """
        moed, beta = 1, 0.8

        if not self.IP:
            logging.info(f"Coefficients - Moed: {moed} and Beta: {beta}.")
            return moed, beta

        if 1 <= self.IP <= 7:
            beta = 0.7
            if 0.45 <= self.e <= 0.55:
                moed = 2.8

            if 0.55 < self.e <= 0.65:
                moed = ((0.65 - self.e) / 0.1) * 0.3 + 2.5

            if 0.65 < self.e <= 0.75:
                moed = ((0.75 - self.e) / 0.1) * 0.4 + 2.1

            if 0.75 < self.e <= 0.85:
                moed = ((0.85 - self.e) / 0.1) * 0.7 + 1.4

        if 7 < self.IP <= 17:
            beta = 0.6
            if 0.45 <= self.e <= 0.55:
                moed = 3

            if 0.55 < self.e <= 0.65:
                moed = ((0.65 - self.e) / 0.1) * 0.3 + 2.7

            if 0.65 < self.e <= 0.75:
                moed = ((0.75 - self.e) / 0.1) * 0.3 + 2.4

            if 0.75 < self.e <= 0.85:
                moed = ((0.85 - self.e) / 0.1) * 0.6 + 1.8

            if 0.85 < self.e <= 0.95:
                moed = ((0.95 - self.e) / 0.1) * 0.3 + 1.5

            if 0.95 < self.e <= 1.05:
                moed = ((1.05 - self.e) / 0.1) * 0.3 + 1.2

        if self.IP > 17:
            beta = 0.4
            if 0.65 < self.e <= 0.75:
                moed = 2.4

            if 0.75 < self.e <= 0.85:
                moed = ((0.85 - self.e) / 0.1) * 0.2 + 2.2

            if 0.85 < self.e <= 0.95:
                moed = ((0.95 - self.e) / 0.1) * 0.2 + 2

            if 0.95 < self.e <= 1.05:
                moed = ((1.05 - self.e) / 0.1) * 0.2 + 1.8

        logging.info(f"Coefficients - Moed: {moed} and Beta: {beta}.")
        return moed, beta

    def definition_press(self) -> list[float]:
        """
        Возвращает давление по типу грунта
        :return:
        """
        press_spd = [0, 0.05, 0.1, 0.2, 0.4, 0.8]

        # Для глинистых грунтов
        if self.IP:
            if self.IL >= 1:
                press_spd = [0, 0.0125, 0.025, 0.05, 0.1, 0.2]
            if 1 > self.IL >= 0.75:
                press_spd = [0, 0.0125, 0.025, 0.05, 0.1, 0.2]
            if 0.75 > self.IL >= 0.5:
                press_spd = [0, 0.025, 0.05, 0.1, 0.2, 0.4]
            if 0.5 > self.IL >= 0.25:
                press_spd = [0, 0.05, 0.1, 0.2, 0.4, 0.8]
            if self.IL < 0.25:
                press_spd = [0, 0.1, 0.2, 0.4, 0.8, 1.6]
        else:
            if self.e >= 1:
                press_spd = [0, 0.0125, 0.025, 0.05, 0.1, 0.2]
            if 1 > self.e >= 0.75:
                press_spd = [0, 0.0125, 0.025, 0.05, 0.1, 0.2]
            if 0.75 > self.e > 0.6:
                press_spd = [0, 0.025, 0.05, 0.1, 0.2, 0.4]
            if self.e <= 0.6:
                press_spd = [0, 0.05, 0.1, 0.2, 0.4, 0.8]

        logging.info(f"Press graph - {press_spd}.")

        return press_spd

    def definition_rzg(self):
        """
        Определляет петлю разгрузки и вставляет ее в график
        :return:
        """
        for count, val in enumerate(self.press_spd, 0):
            if self.press_spd[count] <= self.press_rzg < self.press_spd[count + 1]:
                index_1 = count
                index_2 = count + 1
                break

        logging.info(f"Index for RZG are taken: {index_1}, {index_2}.")

        res = stats.linregress(self.press_spd[index_1:index_2 + 1],
                               self.otn_vert_def[index_1:index_2 + 1])

        otn_vert_def_B_rzg = self.press_rzg * res.slope + res.intercept

        intercept_press = self.press_rzg * random.uniform(.9, .95)

        otn_vert_def_A_rzg = otn_vert_def_B_rzg - (intercept_press / self.Erzg)

        press_end_rzg = self.press_spd[0] + 0.005

        press_start_rzg = self.press_rzg

        # Нижняя кривая
        xpoints = [press_end_rzg, (press_start_rzg + press_end_rzg) / 2, press_start_rzg]
        ypoints = [otn_vert_def_A_rzg, otn_vert_def_B_rzg, otn_vert_def_B_rzg]

        count_step = 5
        if count_step < 4:
            count_step = 4

        control_points = [(x, y) for (x, y) in zip(xpoints, ypoints)]
        xvals, yvals = bezier_curve(control_points, nTimes=count_step)

        new_otn_def = self.otn_vert_def[:index_2]
        new_press = self.press_spd[:index_2]
        new_otn_def.extend(yvals)
        new_press.extend(xvals)

        if self.Erzg / self.Eoed < 2.5:
            coefficient = 7
        else:
            coefficient = 2

        # Верхняя кривая
        xpoints = [intercept_press, (press_end_rzg + press_start_rzg) / coefficient, press_end_rzg]
        ypoints = [otn_vert_def_B_rzg, otn_vert_def_A_rzg, otn_vert_def_A_rzg]

        control_points = [(x, y) for (x, y) in zip(xpoints, ypoints)]
        xvals, yvals = bezier_curve(control_points, nTimes=count_step)

        new_otn_def.extend(yvals)
        new_press.extend(xvals)

        new_otn_def.extend(self.otn_vert_def[index_2:])
        new_press.extend(self.press_spd[index_2:])

        self.otn_vert_def = new_otn_def
        self.press_spd = new_press

        logging.info(f"RZG created is successfully.")

    def definition_q_zg(self) -> float:
        """
        Определяет природное эффективное напряжение
        :return:
        """
        try:
            press_zg = (self.p * self.g * self.depth) / 1000
        except TypeError:
            logging.error(f"Calculation error. The standard pressure is taken.")
            press_zg = 0.05
        logging.info(f"Effective press - {press_zg}.")
        return press_zg

    def find_index_q_zg(self) -> (int, int):
        """
        Ищет индексы, которые соответствуют q_zg на компрессионной кривой
        :return:
        """
        index_1, index_2 = 0, 1

        for count, val in enumerate(self.press_spd, 0):
            if self.press_spd[count] < self.q_zg <= self.press_spd[count + 1]:
                index_1 = count
                index_2 = count + 1
                break
        logging.info(f"Index are taken: {index_1}, {index_2}.")
        return index_1, index_2

    def first_scenario(self) -> list[float]:
        """
        Когда q_zg меньше 0.1
        :return:
        """
        delta_h = (0.1 * 20) / self.Eoed
        degree_d = self.Ecas / self.Eoed
        a = delta_h / ((0.2 ** degree_d) - (0.1 ** degree_d))
        p_y = [a * x ** degree_d for x in self.press_spd]
        otn_vert_def = [(p_y[x] / 20) for x in range(len(p_y))]

        otn_vert_def[self.index_2] = (self.press_spd[self.index_2] - self.press_spd[self.index_1] + self.Ecas *
                                      otn_vert_def[self.index_1]) / self.Ecas

        otn_vert_def[self.press_spd.index(0.2)] = ((0.1) + self.Eoed * otn_vert_def[
            self.press_spd.index(0.1)]) / self.Eoed

        count = 2
        for val in self.press_spd:
            if val <= 0.2:
                continue
            otn_vert_def[self.press_spd.index(val)] = (val - (val / 2) + self.Eoed * count * otn_vert_def[
                self.press_spd.index(val) - 1]) / (self.Eoed * count)
            count *= 2

        return otn_vert_def

    def second_scenario(self) -> list[float]:
        """
        Когда q_zg находится в диапазоне от 0.1 до 0.2
        :return:
        """
        delta_h = (0.1 * 20) / self.Eoed
        degree_d = random.randint(5, 6) / 10  # Eoed_k_opr / Eoed01_02_MPa
        a = delta_h / ((0.2 ** degree_d) - (0.1 ** degree_d))
        p_y = [a * x ** degree_d for x in self.press_spd]
        otn_vert_def = [(p_y[x] / 20) for x in range(len(p_y))]
        return otn_vert_def

    def third_scenario(self) -> list[float]:
        """
        Когда q_zg больше 0.2
        :return:
        """
        delta_h = (0.1 * 20) / self.Eoed
        degree_d = self.Ecas / self.Eoed
        a = delta_h / ((0.2 ** degree_d) - (0.1 ** degree_d))
        p_y = [a * x ** degree_d for x in self.press_spd]
        otn_vert_def = [(p_y[x] / 20) for x in range(len(p_y))]

        otn_vert_def[self.press_spd.index(0.2)] = ((0.1) + self.Eoed * otn_vert_def[
            self.press_spd.index(0.1)]) / self.Eoed

        otn_vert_def[self.index_2] = ((self.press_spd[self.index_2] - self.press_spd[self.index_1]) + self.Ecas *
                                      otn_vert_def[self.index_1]) / self.Ecas

        count = 2
        for val in self.press_spd:
            if val <= self.press_spd[self.index_2]:
                continue
            otn_vert_def[self.press_spd.index(val)] = (val - (val / 2) + self.Ecas * count * otn_vert_def[
                self.press_spd.index(val) - 1]) / (self.Ecas * count)
            count *= 2

        return otn_vert_def

    def define_scenario(self) -> None:
        """
        Распределяет сценарии в зависимости от индекса
        :return:
        """
        index_02 = self.press_spd.index(0.2)

        if self.index_2 < index_02:
            logging.info(f"The value of the effective press is less than the value of the range odometric module.\n"
                         f"First scenario")
            otn_vert_def = self.first_scenario()

        if self.index_2 == index_02:
            logging.info(f"The value of the effective press is equal than the value of the range odometric module.\n"
                         f"Second scenario")
            otn_vert_def = self.second_scenario()

        if self.index_2 > index_02:
            logging.info(f"The value of the effective press is greater than the value of the range odometric module.\n"
                         f"Third scenario")
            otn_vert_def = self.third_scenario()

        logging.info(f"Relative vertical deformation is successfully calculated.")

        return otn_vert_def

    def create_por_list(self) -> list[float]:
        """
        Создает значения коэффициента пористости
        :return:
        """
        por_list = [(self.e - (otn * (1 + self.e))) for otn in self.otn_vert_def]
        logging.info(f"Calculate coefficient of porosity is done.")
        return por_list

    def create_mo_list(self) -> list[float | str | Any]:
        """
        Создает значения коэффициента сжимаемости
        :return:
        """
        koef_m0 = [(self.por_list[x] - self.por_list[x + 1]) / (self.press_spd[x + 1] - self.press_spd[x]) for x in
                   range(len(self.press_spd) - 1)]
        koef_m0.insert(0, '-')
        logging.info(f"Calculate coefficient of m0 is done.")
        return koef_m0

    def check_values(self):

        res = stats.linregress(self.press_spd[self.index_1:self.index_2 + 1],
                               self.otn_vert_def[self.index_1:self.index_2 + 1])
        otn_vert_def_ZG = self.q_zg * res.slope + res.intercept
        otn_END_A = 0 * res.slope + res.intercept

        res_max = stats.linregress([otn_END_A, otn_vert_def_ZG], [0, self.q_zg])
        press_MAX = (self.otn_vert_def[-1] * res_max.slope + res_max.intercept)

        res_max = stats.linregress([0, self.q_zg], [otn_END_A, otn_vert_def_ZG])
        otn_MAX = (self.press_spd[-1] * res_max.slope + res_max.intercept)

        # Oдометрический модуль по бете
        E_oed_beta = self.Eoed * self.beta

        # Одометрический модуль с учетом moed
        E_oed_moed = self.Eoed * self.moed

        # Текущий касательный модуль
        E_cas_now = self.q_zg / (otn_vert_def_ZG - otn_END_A)

        # Проверка секущего модуля
        E_oed_now = 0.1 / (self.otn_vert_def[self.press_spd.index(0.2)] - self.otn_vert_def[self.press_spd.index(0.1)])

        logging.info(f"Checking the set parameters now: Ecas - {E_cas_now}, Eoed - {E_oed_now}")

        return E_oed_beta, E_oed_moed, E_cas_now, E_oed_now, otn_vert_def_ZG, otn_END_A, otn_MAX, press_MAX

    def aggregation(self):
        """
        Собирает все воедино
        :return:
        """
        self.moed, self.beta = self.coefficeients()

        if not self.Ecas:
            logging.warning(f"Missing values Ecas. The tangent module is taken by beta.")
            self.Ecas = self.Eoed * self.beta

        self.press_spd = self.definition_press()

        self.q_zg = self.definition_q_zg()

        self.index_1, self.index_2 = self.find_index_q_zg()

        self.otn_vert_def = self.define_scenario()

        self.por_list = self.create_por_list()

        self.m0_list = self.create_mo_list()

        self.E_oed_beta, self.E_oed_moed, self.E_cas_now, self.E_oed_now, self.otn_vert_def_ZG, self.otn_END_A, self.otn_MAX, self.press_MAX = self.check_values()

        if self.Erzg:
            logging.info(f"The test with RZG.")

            if not self.press_rzg:
                self.press_rzg = 0.25

            logging.info(f"The pressure for RZG is {self.press_rzg}.")

            self.definition_rzg()
            self.por_list = self.create_por_list()
            self.m0_list = self.create_mo_list()

        self.plotting_graph()

    def ret_dataframe(self) -> pd.DataFrame:
        """
        Возвращает основные столбцы испытания
        :return:
        """
        lst = [self.press_spd, self.otn_vert_def, self.por_list, self.m0_list]
        names = ['press', 'otn', 'por', 'mo']
        prepare_df = {f'{name}': value for name, value in zip(names, lst)}

        df = pd.DataFrame.from_dict(prepare_df)
        df.reset_index(drop=True, inplace=True)

        logging.info(f"The data for graph is ready.")

        return df

    def ret_values_to_excel(self) -> dict:
        """
        Возвращает значения для вставки в эксель
        :return:
        """
        values_for_Excel = {"E_oed": self.E_oed_now,
                            "E_oed_k": self.E_cas_now,
                            "q_zg": self.q_zg,
                            "otn_zg": self.otn_vert_def_ZG,
                            "otn_END_A": self.otn_END_A,
                            'press_MAX': self.press_spd[-1],
                            'otn_MAX': self.otn_vert_def[-1],
                            'Erzg': self.Erzg,
                            }

        logging.info(f"The data for protocol is ready.")

        return values_for_Excel

    def plotting_graph(self) -> None:
        """
        Формирует график
        :return:f
        """
        # plt.yticks([0.01 * count for count in range(len(self.ef))])
        plt.xticks([0.1 * count for count in range(len(self.press_spd))])

        ax = plt.gca()
        ax.set_xlim((0, self.press_spd[-1] * 1.1))
        ax.set_ylim((self.otn_vert_def[-1] * 1.1, 0))

        plt.grid(color='gray')

        plt.xlabel('Вертикальное давление, МПа')
        plt.ylabel('Относительная вертикальная\n деформация, д.е.')

        # Значения кривой
        plt.plot(self.press_spd, self.otn_vert_def, color='red')
        plt.plot(self.press_spd, self.otn_vert_def, 'o', markerfacecolor='black', markeredgecolor='black')
        # Линия по Ea
        plt.plot([0, self.press_spd[-1]], [self.otn_END_A, self.otn_MAX], color='green')
        # Перпендикуляр к оси X
        plt.plot([self.q_zg, self.q_zg], [0, self.otn_vert_def_ZG], color='green', linestyle='dashed')
        # Перпендикуляр к оси Y
        plt.plot([0, self.q_zg], [self.otn_vert_def_ZG, self.otn_vert_def_ZG], color='green', linestyle='dashed')

        logging.info(f"A graph is built.")

        plt.show()


if __name__ == "__main__":
    organise_dct = {
        'Ecas': 20,
        'Eoed': 30,
        'Erzg': 80,
        'press_rzg_comp': 0.321,
        'depth': 10,
        'IP': 10,
        'IL': 0.3,
        'e': 0.7,
        'p': 2,
    }

    test = compression(organise_dct=organise_dct)
    test.aggregation()
    df = test.ret_dataframe()
    print(df)
