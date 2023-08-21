import random
import pandas as pd
import numpy as np

from GEOF.main_part.graphic.consolidation import traxial_consolidation

class Traxial_ISP:
    def __init__(self, organise_dct):
        self.organise_dct = organise_dct

    def idle_speed_stage(self):
        """
        Создает холостой ход испытания
        :return:
        """
        time_start = [randint(2, 9) / 100]
        for x in range(5):
            time_start.append(time_start[x] + randint(2, 9) / 100)

        action_none_value = [str('') for x in range(6)]
        action_none_value[3] = 'Start'
        action_none_value[4] = 'Start'
        action_none_value[5] = 'LoadStage'

        action_changed_none_value = [str('') for x in range(6)]
        action_changed_none_value[0] = True
        action_changed_none_value[2] = True
        action_changed_none_value[4] = True

        value_none_cell_press = randint(10, 500) / 100
        CellPress_kPa_none_value = [float(0) for x in range(6)]
        CellPress_kPa_none_value[0] = value_none_cell_press
        CellPress_kPa_none_value[1] = value_none_cell_press

        VerticalPress_kPa_none_value = [float(0) for x in range(6)]
        VerticalPress_kPa_none_value[0] = value_none_cell_press
        VerticalPress_kPa_none_value[1] = value_none_cell_press

        value_none = randint(10, 20) / 10
        VerticalDeformation_mm_none_value = [float(0) for x in range(6)]
        VerticalDeformation_mm_none_value[0] = value_none
        VerticalDeformation_mm_none_value[1] = value_none

        VerticalStrain_none_value = [float(0) for x in range(6)]
        VerticalStrain_none_value[0] = str('')
        VerticalStrain_none_value[1] = str('')

        value_noneVolumeStrain = randint(1000, 11000) / 10000
        VolumeStrain_none_value = [float(0) for x in range(6)]
        VolumeStrain_none_value[0] = value_noneVolumeStrain
        VolumeStrain_none_value[1] = value_noneVolumeStrain

        value_noneVolumeDeformation_cm3_none_value = randint(4000, 50000) / 1000
        VolumeDeformation_cm3_none_value = [float(0) for x in range(6)]
        VolumeDeformation_cm3_none_value[0] = value_noneVolumeDeformation_cm3_none_value
        VolumeDeformation_cm3_none_value[1] = value_noneVolumeDeformation_cm3_none_value

        Trajectory_none_value = [str('') for x in range(6)]
        Trajectory_none_value[-1] = 'ReconsolidationWoDrain'


    def load_stage(self):
        """
        Создает стадию загрузки испытания
        :return:
        """
        count_point_loadstage = randint(10, 25)
        step_time_loadstage = (30 + time_start[-1]) / (count_point_loadstage - 1)
        time_loadstage = [time_start[-1]]
        for x in range(count_point_loadstage - 1):
            time_loadstage.append(time_loadstage[x] + step_time_loadstage + randint(0, 50) / 100)

        action_loadstage = [str('LoadStage') for x in range(count_point_loadstage)]

        action_changed_loadstage = [str('') for x in range(count_point_loadstage)]
        action_changed_loadstage[-1] = True

        list_1000 = [float(1000) for x in range(count_point_loadstage)]

        Deviator_kPa_loadstage = [float(0) for x in range(count_point_loadstage)]

        value_loadstage_start = randint(5, 20) / 10000
        CellPress_kPa_loadstage = [value_loadstage_start]
        step_press = (press * 1000 - randint(1, 20) / 100) / (count_point_loadstage - 1)
        for x in range(count_point_loadstage - 1):
            CellPress_kPa_loadstage.append(CellPress_kPa_loadstage[x] + step_press)

        VerticalPress_kPa_loadstage = CellPress_kPa_loadstage

        VerticalDeformation_mm_loadstage = [float(e1_array[0]) for x in range(count_point_loadstage)]

        value_loadstage_start_volume = randint(5, 50) / 10000
        VolumeDeformation_cm3_loadstage = [value_loadstage_start_volume]
        step_volume = (ev_array_1[0] + randint(10, 20) / 10) / (count_point_loadstage - 1)
        for x in range(count_point_loadstage - 1):
            VolumeDeformation_cm3_loadstage.append(VolumeDeformation_cm3_loadstage[x] + step_volume)

        Deviator_MPa_loadstage = [float(0) for x in range(count_point_loadstage)]

        CellPress_MPa_loadstage = [x / 1000 for x in CellPress_kPa_loadstage]

        VerticalPress_MPa_loadstage = [x / 1000 for x in VerticalPress_kPa_loadstage]

        Trajectory_loadstage = [str('ReconsolidationWoDrain') for x in range(count_point_loadstage)]

        # otn_vert_def
        definirion_e1_array = np.asarray([float(0) for x in range(count_point_loadstage)])
        volume_76 = np.asarray([float(76) for x in range(count_point_loadstage)])
        first_cell_e1 = np.asarray([float(0) for x in range(count_point_loadstage)])
        VerticalStrain_loadstage = (VerticalPress_MPa_loadstage - first_cell_e1) / (volume_76 - (definirion_e1_array))

        # otn_vol_def
        definirion_ev_array = np.asarray([float(0) for x in range(count_point_loadstage)])
        volume = np.asarray([float(86149) for x in range(count_point_loadstage)])
        first_cell_ev = np.asarray([float(0) for x in range(count_point_loadstage)])
        VolumeStrain_loadstage = (VolumeDeformation_cm3_loadstage - first_cell_ev) / (volume - (definirion_ev_array))


    def stabilization_stage(self):
        """
        Создает стабилизацию испытания
        :return:
        """
        df = traxial_consolidation(self.organise_dct)
        print(df)


    def wait_stage(self):
        """
        Создает стадию ожидания испытания
        :return:
        """
        time_wait = np.arange(time_loadstage[-1], time_loadstage[-1] + parametr_d.get('reconsolidation_def'),
                              randint(290, 310) / 100)
        time_wait = time_wait.tolist()
        time_wait.append(time_wait[-1])
        time_wait.append(time_wait[-1] + randint(90, 100) / 100)

        count_point_wait = len(time_wait)

        action_wait = [str('Wait') for x in range(count_point_wait)]
        action_wait[-1] = 'LoadStage'
        action_wait[-2] = 'LoadStage'

        action_changed_wait = [str('') for x in range(count_point_wait)]
        action_changed_wait[-3] = True
        action_changed_wait[-1] = True

        Deviator_kPa_wait = [float(0) for x in range(count_point_wait)]

        Deviator_MPa_wait = [float(0) for x in range(count_point_wait)]

        list_1000 = [float(1000) for x in range(count_point_wait)]

        CellPress_kPa_wait = np.asarray(
            [float(CellPress_kPa_loadstage[-1]) for x in range(count_point_wait)]) - np.asarray(
            [float(randint(0, 10) / 1000) for x in range(count_point_wait)])

        VerticalPress_kPa_wait = CellPress_kPa_wait

        VerticalDeformation_mm_wait = [float(VerticalDeformation_mm_loadstage[-1]) for x in range(count_point_wait)]

        VolumeDeformation_cm3_wait = [VolumeDeformation_cm3_loadstage[-1]]
        step_volume = ((ev_array_1[0] + randint(10, 20) / 10) - (ev_array_1[0])) / (count_point_wait - 1)
        for x in range(count_point_wait - 1):
            VolumeDeformation_cm3_wait.append(VolumeDeformation_cm3_wait[x] + step_volume)

        CellPress_MPa_wait = [x / 1000 for x in CellPress_kPa_wait]

        VerticalPress_MPa_wait = [x / 1000 for x in VerticalPress_kPa_wait]

        Trajectory_wait = [str('ReconsolidationWoDrain') for x in range(count_point_wait)]
        Trajectory_wait[-1] = 'Consolidation'
        Trajectory_wait[-2] = 'Consolidation'
        Trajectory_wait[-2] = 'Consolidation'

        # otn_vert_def
        definirion_e1_array = np.asarray([float(0) for x in range(count_point_wait)])
        volume_76 = np.asarray([float(76) for x in range(count_point_wait)])
        first_cell_e1 = np.asarray([float(0) for x in range(count_point_wait)])
        VerticalStrain_wait = (VerticalPress_MPa_wait - first_cell_e1) / (volume_76 - (definirion_e1_array))

        # otn_vol_def
        definirion_ev_array = np.asarray([float(0) for x in range(count_point_wait)])
        volume = np.asarray([float(86149) for x in range(count_point_wait)])
        first_cell_ev = np.asarray([float(0) for x in range(count_point_wait)])
        VolumeStrain_wait = (VolumeDeformation_cm3_wait - first_cell_ev) / (volume - (definirion_ev_array))



    def ISP_TPs(self, dataframe_isp, organise_dct) -> pd.DataFrame:
        """
        Создает исходный файл испытания трехосного сжатия
        :param dataframe_isp:
        :param organise_dct:
        :return:
        """

if __name__ == "__main__":
    test = Traxial_ISP(organise_dct={'PressStart_traxial_now': 0.1,
                                     'IP': 25,
                                     't_100': 700,
                                     })
    test.stabilization_stage()