import math

class IdentifySoil:
    def __init__(self, organise_dct):
        self.organise_dct = organise_dct

        self.IP = organise_dct.get('IP')
        self.IL = organise_dct.get('IL')
        self.e = organise_dct.get('e')
        self.Sr = organise_dct.get('Sr')

        self.GGR10 = organise_dct.get('GGR10')
        self.G10_5 = organise_dct.get('G10_5')
        self.G5_2 = organise_dct.get('G5_2')
        self.G2_1 = organise_dct.get('G2_1')
        self.G1_05 = organise_dct.get('G1_05')
        self.G05_025 = organise_dct.get('G05_025')
        self.G025_01 = organise_dct.get('G025_01')
        self.G01_005 = organise_dct.get('G01_005')

        self.type_soil = {
            'grunt_type': None,
            'consistency': None,
            'water_saturation': None,
            'density': None,

        }

    def definition_gransostav(self):

        self.grunt_type = None

        if (self.G5_2 + self.G10_5 + self.GGR10) > 25:
            self.grunt_type = 'Гравелистый'
        elif (self.G1_05 + self.G2_1 + self.G5_2 + self.G10_5 + self.GGR10) > 50:
            self.grunt_type = 'Крупный'
        elif (self.G05_025 + self.G1_05 + self.G2_1 + self.G5_2 + self.G10_5 + self.GGR10) > 50:
            self.grunt_type = 'Средней крупности'
        elif (self.G025_01 + self.G05_025 + self.G1_05 + self.G2_1 + self.G5_2 + self.G10_5 + self.GGR10) >= 75:
            self.grunt_type = 'Мелкий'
        elif (self.G025_01 + self.G05_025 + self.G1_05 + self.G2_1 + self.G5_2 + self.G10_5 + self.GGR10) < 75:
            self.grunt_type = 'Пылеватый'

        return self.grunt_type

    def definition_density(self):

        self.density = None

        match self.grunt_type:
            case 'Гравелистый' | 'Крупный' | 'Средней крупности':
                if self.e:
                    if self.e <= 0.55:
                        self.density = 'Плотный'
                    if 0.55 < self.e <= 0.7:
                        self.density = 'Средней плотности'
                    if self.e > 0.7:
                        self.density = 'Рыхлый'

            case 'Мелкий':
                if self.e:
                    if self.e <= 0.6:
                        self.density = 'Плотный'
                    if 0.6 < self.e <= 0.75:
                        self.density = 'Средней плотности'
                    if self.e > 0.75:
                        self.density = 'Рыхлый'

            case 'Пылеватый':
                if self.e:
                    if self.e <= 0.6:
                        self.density = 'Плотный'
                    if 0.6 < self.e <= 0.8:
                        self.density = 'Средней плотности'
                    if self.e > 0.8:
                        self.density = 'Рыхлый'

        return self.density

    def definition_water_saturation(self):

        self.water_saturation = None



