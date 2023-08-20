import os
import shutil

def write_log(row, dataframe, organise_dct):
    LAB_NO = str(organise_dct.get("LAB_NO"))
    if LAB_NO in ['NAN', "None", "nAn"]:
        LAB_NO = str(row)

    pathSave = organise_dct.get('pathSave_spd')

    pathSave = os.path.join(pathSave, 'Испытания')
    if not os.path.exists(pathSave):
        os.mkdir(pathSave)

    pathSave = os.path.join(pathSave, LAB_NO)
    if not os.path.exists(pathSave):
        os.mkdir(pathSave)


    """
    Нужно доработать под ГТ 7.1.4
    Нужно придумать что делать с временем
    """
    pathSave_Execute = os.path.join(pathSave, 'Execute')
    if not os.path.exists(pathSave_Execute):
        os.mkdir(pathSave_Execute)
        my_file = open(f"{pathSave_Execute}\\Execute.1.log", "w+")
        my_file.write('Just simple test')
        my_file.close()
    pathSave_General = os.path.join(pathSave, 'General')
    if not os.path.exists(pathSave_General):
        os.mkdir(pathSave_General)
        my_file = open(f"{pathSave_General}\\General.1.log", "w+")
        my_file.write('SampleHeight_mm	SampleDiameter_mm	\n'
                      '20	87')
        my_file.close()
    pathSave_Test = os.path.join(pathSave, 'Test')
    if not os.path.exists(pathSave_Test):
        os.mkdir(pathSave_Test)

    # 20230627 143100 ГТ 7.2.6.xml Дата, время, тип
    shutil.copy('..\\GEOF\\main_part\\XML_LOG\\SPD_ГТ_7.1.4.xml'
                , f'{pathSave}\\SPD_ГТ_7.1.4.xml')

    dataframe.to_csv(f"{pathSave_Test}\\Test.1.log", sep='\t', index=False, encoding="ANSI")
