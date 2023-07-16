"""
Сюда передаются значения по C, F, E
Они обрабатываются и распределяются по графикам в механике


"""

def distribution(dct: dict):
    pressStart1 = 0.1
    pressStart2 = pressStart1 + 0.1
    pressStart3 = pressStart2 + 0.1
    press16 = pressStart1 * 1.6

    # Выбор значений механики
    E_0 = 90
    E_50 = 70
    F = 20
    C = 0.006
    countPoint = 500
    endE1 = 11.4
    stepE1 = endE1 / countPoint