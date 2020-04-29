import numpy as np
from scipy.optimize import curve_fit


class CurveRegression:
    def __init__(self, model, init_param=None):
        self.model = model
        self.param = init_param
        self.covar = None

    def predict(self, x):
        return self.model(x, *self.param)

    def fit(self, x, y):
        solution = curve_fit(self.model, x, y, p0=self.param)
        self.param = solution[0]
        self.covar = solution[1]

    def __str__(self):
        return f"F_G:{self.model}Parameters:{self.param}"


def cheeseman_model(x, rho):
    return 1 / (1 - rho / (x ** 2))


def exponential_model(x, a, b):
    return a * np.exp(-x / b) + 1


def piecewise_linear_model(x, y_intersect, cutoff):
    def linear(xn):
        slope = (1 - y_intersect) / cutoff
        return slope * xn + y_intersect

    return np.piecewise(x, [x < cutoff, x >= cutoff], [linear, 1])


def log_model(x, a, b):
    return a * np.log(b * x + 1)
