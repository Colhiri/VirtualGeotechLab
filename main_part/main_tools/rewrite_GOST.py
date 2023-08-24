class IdentifySoil:
    def __init__(self, organise_dct):
        self.organise_dct = organise_dct

        self.depth = self.organise_dct.get('depth')
        self.g = 9.80665

        self.IP = organise_dct.get('IP')
        self.IL = organise_dct.get('IL')
        self.p = organise_dct.get('p')
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

    def definition_gransostav(self) -> str:

        grunt_type = None

        if (self.G5_2 + self.G10_5 + self.GGR10) > 25:
            grunt_type = 'Гравелистый'
        elif (self.G1_05 + self.G2_1 + self.G5_2 + self.G10_5 + self.GGR10) > 50:
            grunt_type = 'Крупный'
        elif (self.G05_025 + self.G1_05 + self.G2_1 + self.G5_2 + self.G10_5 + self.GGR10) > 50:
            grunt_type = 'Средней крупности'
        elif (self.G025_01 + self.G05_025 + self.G1_05 + self.G2_1 + self.G5_2 + self.G10_5 + self.GGR10) >= 75:
            grunt_type = 'Мелкий'
        elif (self.G025_01 + self.G05_025 + self.G1_05 + self.G2_1 + self.G5_2 + self.G10_5 + self.GGR10) < 75:
            grunt_type = 'Пылеватый'

        return grunt_type

    def definition_density(self) -> str:

        density = None

        match self.grunt_type:
            case 'Гравелистый' | 'Крупный' | 'Средней крупности':
                if self.e:
                    if self.e <= 0.55:
                        density = 'Плотный'
                    if 0.55 < self.e <= 0.7:
                        density = 'Средней плотности'
                    if self.e > 0.7:
                        density = 'Рыхлый'

            case 'Мелкий':
                if self.e:
                    if self.e <= 0.6:
                        density = 'Плотный'
                    if 0.6 < self.e <= 0.75:
                        density = 'Средней плотности'
                    if self.e > 0.75:
                        density = 'Рыхлый'

            case 'Пылеватый':
                if self.e:
                    if self.e <= 0.6:
                        density = 'Плотный'
                    if 0.6 < self.e <= 0.8:
                        density = 'Средней плотности'
                    if self.e > 0.8:
                        density = 'Рыхлый'

        return density

    def definition_water_saturation(self) -> str | None:

        water_saturation = None

        if self.Sr:
            if self.Sr <= 0.8:
                water_saturation = True
            else:
                water_saturation = False

        return water_saturation

    def definition_constistenci(self) -> (str, str):

        consistency = None

        grunt_type = None

        if self.IP <= 7:
            grunt_type = 'Супесь'
            if self.IL < 0:
                consistency = 'Твердая'
            if 0 <= self.IL <= 1:
                consistency = 'Пластичная'
            if 1 < self.IL:
                consistency = 'Текучая'

        if 7 < self.IP <= 17:
            grunt_type = 'Суглинок'
            if self.IL < 0:
                consistency = 'Твердый'
            if 0 <= self.IL <= 0.25:
                consistency = 'Полутвердый'
            if 0.25 < self.IL <= 0.5:
                consistency = 'Тугопластичный'
            if 0.5 < self.IL <= 0.75:
                consistency = 'Мягкопластичный'
            if 0.75 < self.IL <= 1:
                consistency = 'Текучепластичный'
            if 1 < self.IL:
                consistency = 'Текучий'

        if self.IP > 17:
            grunt_type = 'Глина'
            if self.IL < 0:
                consistency = 'Твердая'
            if 0 <= self.IL <= 0.25:
                consistency = 'Полутвердая'
            if 0.25 < self.IL <= 0.5:
                consistency = 'Тугопластичная'
            if 0.5 < self.IL <= 0.75:
                consistency = 'Мягкопластичная'
            if 0.75 < self.IL <= 1:
                consistency = 'Текучепластичная'
            if 1 < self.IL:
                consistency = 'Текучая'

        return consistency, grunt_type

    def aggregation_parameters(self):

        if self.IP:
            self.consistency, self.grunt_type = self.definition_constistenci()
        else:
            self.grunt_type = self.definition_gransostav()
            self.density = self.definition_density()

        self.water_saturation = self.definition_water_saturation()

    def GOST_SPS(self) -> (float, float, float):
        press_1, press_2, press_3 = (self.organise_dct.get('pressStart1_unaxial'),
                                     self.organise_dct.get('pressStart1_unaxial'),
                                     self.organise_dct.get('pressStart1_unaxial'))
        F, C = self.organise_dct.get('F_unaxial'), self.organise_dct.get('C_unaxial')

        if press_1 and press_2 and press_3:
            return press_1, press_2, press_3
        if F and C:
            if self.grunt_type in ['Гравелистый', 'Крупный', 'Средний', 'Глина']:
                if self.density in ['Плотный'] or self.consistency in ['Твердая', 'Полутвердая']:
                    press_1 = 0.100
                    press_2 = 0.300
                    press_3 = 0.500
            if self.grunt_type in ['Гравелистый', 'Крупный', 'Средний', 'Суглинок', 'Глина']:
                if self.density in ['Средней плотности'] or self.consistency in ['Тугопластичная', 'Тугопластичный', 'Полутвердый']:
                    press_1 = 0.100
                    press_2 = 0.200
                    press_3 = 0.300
            if self.grunt_type in ['Супесь', 'Мелкий', 'Пылеватый']:
                if self.density in ['Плотный', 'Средней плотности'] or self.IL <= 0.5:
                    press_1 = 0.100
                    press_2 = 0.200
                    press_3 = 0.300
            if self.grunt_type in ['Гравелистый', 'Крупный', 'Средний', 'Мелкий', 'Пылеватый', 'Суглинок', 'Глина']:
                if self.density in ['Рыхлый'] or 0.5 < self.IL <= 1.0:
                    press_1 = 0.100
                    press_2 = 0.150
                    press_3 = 0.200
                else:
                    press_1 = 0.025
                    press_2 = 0.075
                    press_3 = 0.125
        else:
            press_1, press_2, press_3 = None, None, None

        return press_1, press_2, press_3

    def GOST_TP(self, mode) -> (float, float, float):
        press_1, press_2, press_3 = (self.organise_dct.get(f'pressStart1_traxial_{mode}'),
                                     self.organise_dct.get(f'pressStart1_traxial_{mode}'),
                                     self.organise_dct.get(f'pressStart1_traxial_{mode}'))

        F, C = self.organise_dct.get(f'F_traxial_{mode}'), self.organise_dct.get(f'C_traxial_{mode}')

        if press_1 and press_2 and press_3:
            return press_1, press_2, press_3
        if F and C:
            press_1 = (self.p * self.g * self.depth) / 1000
            if press_1 < 0.05:
                press_1 = 0.05
            if 0.15 < press_1 < 0.25:
                press_1 -= 0.1
            if press_1 > 0.25:
                press_1 -= 0.2
            press_2 = press_1 + 0.1
            press_3 = press_2 + 0.1
        else:
            press_1, press_2, press_3 = None, None, None

        return press_1, press_2, press_3
