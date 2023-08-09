словарь из МЕХАНИКИ

organise_dct = {
            "LAB_NO": LAB_NO,
            "N_IG": N_IG,
            "boreHole": boreHole,
            "depth": depth,
            "nameSoil": nameSoil,
            "date_isp_object": date_isp_object,
            "date_isp": date_isp,
            "date_protocol": date_protocol,
            "number_protocol": number_protocol,
            "nameClient": nameClient,
            "nameObject": nameObject,
            'pathSave': pathSave,

            # Физические параметры для протокола
            'We': We,
            'p': p,
            'ps': ps,
            'e': e,
            'IP': IP,
            'IL': IL,
            'Sr': Sr,
            'WL': WL,
            'WP': WP,
            'Ir': Ir,

            # Грансостав
            'GGR10': GGR10,
            'G10_5': G10_5,
            'G5_2': G5_2,
            'G2_1': G2_1,
            'G1_05': G1_05,
            'G05_025': G05_025,
            'G025_01': G025_01,
            'G01_005': G01_005,
            'G005_001': G005_001,
            'G001_0002': G001_0002,
            'G0002': G0002,

            # Трехосники КД
            'pressStart1_traxial': pressStart1_traxial,
            'pressStart2_traxial': pressStart2_traxial,
            'pressStart3_traxial': pressStart3_traxial,
            'E_0': E_0,
            'E_50': E_50,
            'F_traxial': F_traxial,
            'C_traxial': C_traxial,
            'E_rzg': E_rzg,
            'CD_v_rzg': CD_v_rzg,
            'Dilatanci': Dilatanci,
            'CD_v': CD_v,

            # Трехосники КН
            pressStart1_traxial_CU = worksheet_journal['CU_sigma1'][row]
            pressStart2_traxial_CU = worksheet_journal['CU_sigma2'][row]
            pressStart3_traxial_CU = worksheet_journal['CU_sigma3'][row]
            CU_E50 = worksheet_journal['CU_E50'][row]
            CU_fi = worksheet_journal['CU_fi'][row]
            CU_c = worksheet_journal['CU_c'][row]

            # Трехосники НН
            pressStart1_traxial_UU = worksheet_journal['UU_sigma1'][row]
            pressStart2_traxial_UU = worksheet_journal['UU_sigma2'][row]
            pressStart3_traxial_UU = worksheet_journal['UU_sigma3'][row]
            UU_c = worksheet_journal['UU_c'][row]

            # OCR и компрессия
            'OCR': OCR,
            'effective_press': effective_press,
            'Eoed01_02_MPa': Eoed01_02_MPa,
            'Eobs01_02_Mpa': Eobs01_02_Mpa,

            # Одноплоскостной срез
            'F_unaxial': F_unaxial,
            'C_unaxial': C_unaxial,

            ### Текущие давления на срезах, трехосниках
            'name_traxial_now': None,
            'name_unaxial_now': None,

            'PressStart_traxial_now': None,
            'PressStart_unaxial_now': None,

            'PressEnd_traxial_now': None,
            'PressEnd_unaxial_now': None,
        }