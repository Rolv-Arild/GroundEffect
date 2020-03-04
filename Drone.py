from pandas import DataFrame, Series
from sklearn.linear_model import LinearRegression
import numpy as np

from Measurement import read_measurements
from PolynomialRegression import PolynomialRegression
from scipy.optimize import curve_fit


class Drone:
    def f0(self, voltages):
        avg_voltage = sum(voltages) / len(voltages)
        return 0.01 * avg_voltage ** 3 + 0.1 * avg_voltage ** 2 + avg_voltage

    def f_ground_effect(self, dist, voltages):
        # avg_voltage = sum(voltages) / len(voltages)
        return self.f0(voltages)

    def f_unknown(self, dist, voltages):
        pass


def model1(x, rho):
    return 1 / (1 - rho * (1 / x) ** 2)


def model2(x, a, b):
    return a * np.exp(-x / b) + 1


class F_geRegression:
    def __init__(self, model):
        if model == "model1":
            self.param = [1]
            self.covar = np.zeros(1)
        elif model == "model2":
            self.param = [1, 1]
            self.covar = np.zeros((2, 2))
        else:
            print("No model chosen")

        self.model = model

    def predict(self, distances):
        if self.model == "model1":
            return model1(distances, self.param[0])
        elif self.model == "model2":
            return model2(distances, self.param[0], self.param[1])
        else:
            print("Missing model")
            return []

    def fit(self, x, y):
        print(x.values, y.values)
        if self.model == "model1":
            solution = curve_fit(model1, x.values, y.values)
        elif self.model == "model2":
            solution = curve_fit(model2, x.values, y.values)
        else:
            print("Missing model")
            return []

        self.param = solution[0]
        self.covar = solution[1]

    def __str__(self):
        return f"Model:{self.model}\nParameters:{self.param}"

def find_f0(df: DataFrame):
    polynomial_regression = PolynomialRegression(3, bias=True)
    average_voltages = df.filter(regex="^voltage_\\d+$").mean(axis=1)
    average_weights = df.filter(regex="^weight_\\d+$").mean(axis=1)
    polynomial_regression.fit(average_voltages.values, average_weights.values)
    return polynomial_regression


def find_fge(df: DataFrame, f0, model):
    curve_regression = F_geRegression(model)
    average_voltages = df.filter(regex="^voltage_\\d+$").mean(axis=1)
    calc_weights = f0.predict(average_voltages.values)
    average_weights = df.filter(regex="^weight_\\d+$").mean(axis=1)
    error_weights = average_weights / calc_weights
    distances = df["distance"]
    curve_regression.fit(distances, error_weights)
    return curve_regression


def find_fu(df: DataFrame, f0, fge):
    df = df.drop(["time"], axis=1)
    lr = LinearRegression()  # Most basic model
    voltages = df.filter(regex="^voltage_\\d+$")
    average_voltages = voltages.mean(axis=1)
    weights = df.filter(regex="^weight_\\d+$")
    distances = df["distance"]
    pred_weights = f0.predict(average_voltages.values) * fge.predict(distances.values)
    error_weights = weights.values - np.repeat(np.reshape(pred_weights, (-1, 1)), 4, axis=1)
    lr.fit(df.values, error_weights)
    return lr


if __name__ == '__main__':
    import matplotlib.pyplot as plt

    df = read_measurements("example_measurements.csv")
    f0 = find_f0(df[df["distance"] >= 20])
    fge = find_fge(df, f0, "model1")
    fu = find_fu(df, f0, fge)
    print(f0)
    print(fge)
    print(fu)

    plt.figure(1)
    plt.scatter(df["voltage_1"], df['weight_1'])
    plt.plot(np.arange(0,5,0.1), f0.predict(np.arange(0,5,0.1))*fge.predict(np.array([20])), color = "blue")
    plt.plot(np.arange(0,5,0.1), f0.predict(np.arange(0,5,0.1)), color = "orange")
    plt.show()
