import random
import pandas as pd

def random_time() -> float:
    """
    Создает примерные значения по времени одной точки в испытании одноплоскостного среза
    :return:
    """
    return random.randint(900, 1500) / 100

def SPS_time(quantity_point) -> list[float]:
    """
    Создает лист времени испытания одноплоскостного среза
    :param quantity_point:
    :return:
    """
    return [random_time() * count for count in range(quantity_point)]

def ISP_SPS(dataframe_isp, organise_dct) -> pd.DataFrame:
    """
    Создает исходник испытания одноплоскостного среза
    :param pressStart:
    :return:
    """
    pressStart = organise_dct.get("PressStart_unaxial_now")

    SHEAR_DEF = list(dataframe_isp[1])
    TANGENT_PRESS = list(dataframe_isp[0])

    count_point = len(SHEAR_DEF)

    TIME = SPS_time(count_point)

    action_list = [str('Stabilization') for x in range(count_point)]

    action_changed_list = [str(True) for x in range(count_point)]

    press_sps = [pressStart for x in range(count_point)]

    empty_list = [str('') for x in range(count_point)]

    name = [str('Срез') for x in range(count_point)]

    df = pd.DataFrame({'Time': TIME, 'Action': action_list, 'Action_Changed': action_changed_list,
                       'VerticalPress_kPa': empty_list, 'ShearDeformation_mm': SHEAR_DEF, 'ShearPress_kPa': empty_list,
                       'VerticalPress_MPa': press_sps, 'ShearPress_MPa': TANGENT_PRESS, 'ShearStrain': empty_list,
                       'Stage': name})
    return df
