import random

import numpy as np
from scipy.stats import stats
from scipy.special import comb
from scipy import interpolate

"""
Интерполяция значений исходя из настроек в интерактивной схеме
"""
def interpolation(x, y=None, count_point=None, method_interpolate="PchipInterpolator", parameters=None):
    if parameters:
        method_interpolate = parameters.get('method_interpolate')
        if not count_point:
            count_point = parameters.get('count_point')

    yfit = np.linspace(min(y), max(y), num=count_point)

    if method_interpolate == "interp1d":
        pchip = interpolate.interp1d(y, x, kind='linear')

    if method_interpolate == "CubicSpline":
        pchip = interpolate.CubicSpline(y, x)

    if method_interpolate == "PchipInterpolator":
        pchip = interpolate.PchipInterpolator(y, x)

    if method_interpolate == "Akima1DInterpolator":
        pchip = interpolate.Akima1DInterpolator(y, x)

    if method_interpolate == "BarycentricInterpolator":
        pchip = interpolate.BarycentricInterpolator(y, x)

    if method_interpolate == "KroghInterpolator":
        pchip = interpolate.KroghInterpolator(y, x)

    if method_interpolate == "make_interp_spline":
        pchip = interpolate.make_interp_spline(y, x)

    if method_interpolate == "nearest":
        pchip = interpolate.interp1d(y, x, kind='nearest')

    if method_interpolate == "quadratic":
        pchip = interpolate.interp1d(y, x, kind='quadratic')

    if method_interpolate == "cubic":
        pchip = interpolate.interp1d(y, x, kind='cubic')

    if method_interpolate == "nearest_volume":
        pchip = interpolate.PchipInterpolator(y, x)
        xnew = pchip(yfit)

        xnew = xnew.tolist()

        xnew = volume_random_values(points_x=xnew,
                         dont_touch_indexes=[0, ],
                         parameters_points=parameters)

        i = 0
        filtered_data_x = []
        filtered_data_y = []

        while i < len(xnew):
            if i + 3 <= len(xnew):
                filtered_data_x.append(xnew[i])
                filtered_data_y.append(yfit[i])
            i += 4

        filtered_data_x.append(xnew[-1])
        filtered_data_y.append(yfit[-1])

        filtered_data_x = np.asarray(filtered_data_x)
        filtered_data_y = np.asarray(filtered_data_y)

        pchip = interpolate.interp1d(filtered_data_y, filtered_data_x, kind='nearest')

    xnew = pchip(yfit)

    if type(yfit) != list:
        yfit = yfit.tolist()
    if type(xnew) != list:
        xnew = xnew.tolist()

    if type(xnew) == list:
        pass

    return xnew, yfit

"""
Нахождение ближайшей точки в массиве, исходя из заданного значения
"""
def nearest(lst, target):
    try:
        pressMAX = lst.tolist().index(max(lst))
    except:
        pressMAX = lst.index(max(lst))
    return min(lst[:pressMAX], key=lambda x: abs(x - target))


"""
Рассчёт процента исходя из заданного отхождения в интерактивной настройке
"""
def random_percent(random_percent_min, random_percent_max):
    """
    Функция рандомного процента
    :return:
    """
    perc_min = int((100 - float(random_percent_min)) * 100)
    perc_max = int((100 + float(random_percent_max)) * 100)
    return random.randint(perc_min, perc_max) / 10000

def random_values(points_x, dont_touch_indexes, parameters_points):
    random_percent_min = parameters_points.get('random_percent_min')
    random_percent_max = parameters_points.get('random_percent_max')
    points_x = [random_percent(random_percent_min, random_percent_max) * x_value if count not in dont_touch_indexes else x_value for count, x_value in enumerate(points_x, 0)]
    return points_x

def volume_random_values(points_x, dont_touch_indexes, parameters_points):
    random_percent_min = parameters_points.get('random_percent_min')
    random_percent_max = parameters_points.get('random_percent_max')
    points_x = [random_percent(random_percent_min, random_percent_max) * x_value if count not in dont_touch_indexes else x_value for count, x_value in enumerate(points_x, 0)]
    return points_x

"""
Еще одна версия кривой Безье
"""
class Bezier():
    def TwoPoints(t, P1, P2):
        """
        Returns a point between P1 and P2, parametised by t.
        INPUTS:
            t     float/int; a parameterisation.
            P1    numpy array; a point.
            P2    numpy array; a point.
        OUTPUTS:
            Q1    numpy array; a point.
        """
        Q1 = (1 - t) * P1 + t * P2
        return Q1

    def Points(t, points):
        """
        Returns a list of points interpolated by the Bezier process
        INPUTS:
            t            float/int; a parameterisation.
            points       list of numpy arrays; points.
        OUTPUTS:
            newpoints    list of numpy arrays; points.
        """
        newpoints = []
        for i1 in range(0, len(points) - 1):
            newpoints += [Bezier.TwoPoints(t, points[i1], points[i1 + 1])]
        return newpoints

    def Point(t, points):
        """
        Returns a point interpolated by the Bezier process
        INPUTS:
            t            float/int; a parameterisation.
            points       list of numpy arrays; points.
        OUTPUTS:
            newpoint     numpy array; a point.
        """
        newpoints = points
        while len(newpoints) > 1:
            newpoints = Bezier.Points(t, newpoints)

        return newpoints[0]

    def Curve(t_values, points):
        """
        Returns a point interpolated by the Bezier process
        INPUTS:
            t_values     list of floats/ints; a parameterisation.
            points       list of numpy arrays; points.
        OUTPUTS:
            curve        list of numpy arrays; points.
        """
        curve = np.array([[0.0] * len(points[0])])
        for t in t_values:
            curve = np.append(curve, [Bezier.Point(t, points)], axis=0)

        curve = np.delete(curve, 0, 0)
        return curve

"""
Кривая Безье
Используется для петель разгрузки
"""
def bernstein_poly(i, n, t):
    """
     The Bernstein polynomial of n, i as a function of t
    """

    return comb(n, i) * (t ** (n - i)) * (1 - t) ** i

def bezier_curve(points, nTimes=1000):
    """
       Given a set of control points, return the
       bezier curve defined by the control points.

       points should be a list of lists, or list of tuples
       such as [ [1,1],
                 [2,3],
                 [4,5], ..[Xn, Yn] ]
        nTimes is the number of time steps, defaults to 1000

        See http://processingjs.nihongoresources.com/bezierinfo/
    """

    nPoints = len(points)
    xPoints = np.array([p[0] for p in points])
    yPoints = np.array([p[1] for p in points])

    t = np.linspace(0.0, 1.0, nTimes)

    polynomial_array = np.array([bernstein_poly(i, nPoints - 1, t) for i in range(0, nPoints)])

    xvals = np.dot(xPoints, polynomial_array)
    yvals = np.dot(yPoints, polynomial_array)

    return xvals, yvals

def definition_type_grunt(IP=None, IL=None, e=None):
    pass
