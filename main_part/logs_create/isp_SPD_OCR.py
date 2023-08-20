import random
import pandas as pd

def random_time() -> float:
    """
    Создает примерные значения по времени одной точки в испытании компрессии
    :return:
    """
    return random.randint(900, 1500) / 100

def SPD_time(quantity_point) -> list[float]:
    """
    Создает лист времени испытания компрессии
    :param quantity_point:
    :return:
    """
    return [random_time() * count for count in range(quantity_point)]

def ISP_SPD(dataframe_isp, organise_dct) -> pd.DataFrame:

    press_spd = dataframe_isp[0]
    otn_vert_def = dataframe_isp[1]
    p_y = [otn * 20 for otn in otn_vert_def]
    por_list = dataframe_isp[2]
    try:
        koef_m0 = dataframe_isp[3]
    except:
        pass

    count_point = len(press_spd)

    TIME = SPD_time(count_point)

    action_list = [str('Stabilization') for x in range(count_point)]

    action_changed_list = [str(True) for x in range(count_point)]

    ePress_kPa = [int(0) for x in range(count_point)]

    empty_list = [str('') for x in range(count_point)]

    name = [str('Компрессия') for x in range(count_point)]

    df = pd.DataFrame({'Time': TIME, 'Action': action_list, 'Action_Changed': action_changed_list,
                       'VerticalPress_kPa': [press * 100 for press in press_spd], 'ePress_kPa': ePress_kPa, 'VerticalDeformation_mm': p_y,
                       'VerticalPress_MPa': press_spd, 'PorePress_MPa': p_y, 'VerticalStrain': ePress_kPa,
                       'Deformation_mm': [press * 0.1 for press in press_spd],
                       'Stage': ePress_kPa, '': name})
    return df