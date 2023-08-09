import random

class GruntNormative:
    def __init__(self, organise_values):
        self.organise_values = organise_values

        # Параметры пробы для включения схем
        self.We = self.organise_values.get('We')
        self.p = self.organise_values.get('p')
        self.ps = self.organise_values.get('ps')
        self.e = self.organise_values.get('e')
        self.IL = self.organise_values.get('IL')
        self.IP = self.organise_values.get('IP')

        self.normative_parameters = {
            'E_0': None,
            'E_50': None,
            'F_traxial':None,
            'C_traxial':None,
            'E_rzg': None,
            'CD_v_rzg': None,
            'Dilatanci': None,
            'CD_v': None,
            'CD_u1': None,
            'CD_u2': None,
            'CD_u3': None,
            #None,
            'CU_E50': None,
            'CU_fi': None,
            'CU_c': None,
            #None,
            'UU_c': None,
            #None,
            'OCR': None,
            #None,
            'Eoed01_02_MPa': None,
            'Eobs01_02_Mpa': None,
            #None,
            'F_unaxial': None,
            'C_unaxial': None,
        }

        self.get_type_grunt()
        self.angle_dilatanci()
        self.first_koef_puasson()
        self.rzg_koef_puasson()

    def get_type_grunt(self):
        """
        Поменяй на нормальный обработчик
        :return:
        """
        if str(self.IP) in ['nan', 'None'] or str(self.IL) in ['nan', 'None']:
            self.grunt = 'sand'
        else:
            if self.IP < 7:
                self.grunt = 'sandy_loam'
            elif self.IP < 17:
                self.grunt = 'loam'
            elif self.IP < 27:
                self.grunt = 'clay'

    def angle_dilatanci(self):
        if self.grunt == 'gravel':
            self.dilatanci = random.randint(400, 900) / 100

        if self.grunt == 'sand':
            self.dilatanci = random.randint(300, 600) / 100

        if self.grunt == 'sandy_loam':
            self.dilatanci = random.randint(10, 200) / 100

        if self.grunt == 'loam':
            self.dilatanci = random.randint(50, 100) / 100

        if self.grunt == 'clay':
            self.dilatanci = random.randint(0, 50) / 100

        self.normative_parameters.update({'Dilatanci': self.dilatanci})

    def first_koef_puasson(self):
        """
        Исправить полностью класс с точки зрения получения грунта и его параметров
        :return:
        """
        if self.grunt == 'gravel':
            self.first_puasson = random.randint(30, 35) / 100

        if self.grunt == 'sand':
            self.first_puasson = random.randint(30, 35) / 100

        if self.grunt == 'sandy_loam':
            self.first_puasson = random.randint(30, 35) / 100

        if self.grunt == 'loam':
            self.first_puasson = random.randint(35, 37) / 100

        if self.grunt == 'clay':
            self.first_puasson = random.randint(30, 45) / 100

        self.normative_parameters.update({'CD_v': self.first_puasson})

    def second_koef_puasson(self):
        pass

    def rzg_koef_puasson(self):
        self.koef_rzg = random.randint(14, 16) / 100
        self.normative_parameters.update({'CD_v_rzg': self.koef_rzg})

    def C_F_normative(self):
        pass

    def E_normative(self):
        pass

    def return_parameters(self):
        return self.normative_parameters
