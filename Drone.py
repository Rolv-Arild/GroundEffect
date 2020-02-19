from pandas import DataFrame, Series
from sklearn.linear_model import LinearRegression
import numpy as np

from Measurement import read_measurements
from PolynomialRegression import PolynomialRegression


class Drone:
    def f0(self, voltages):
        avg_voltage = sum(voltages) / len(voltages)
        return 0.01 * avg_voltage ** 3 + 0.1 * avg_voltage ** 2 + avg_voltage

    def f_ground_effect(self, dist, voltages):
        # avg_voltage = sum(voltages) / len(voltages)
        return self.f0(voltages)

    def f_unknown(self, dist, voltages):
        pass


def find_f0(df: DataFrame):
    polynomial_regression = PolynomialRegression(3, bias=True)
    average_voltages = df.filter(regex="^voltage_\\d+$").mean(axis=1)
    average_weights = df.filter(regex="^weight_\\d+$").mean(axis=1)
    polynomial_regression.fit(average_voltages.values, average_weights.values)
    return polynomial_regression


def find_fge(df: DataFrame, f0):
    polynomial_regression = PolynomialRegression(3, bias=True)
    average_voltages = df.filter(regex="^voltage_\\d+$").mean(axis=1)
    calc_weights = f0.predict(average_voltages.values)
    average_weights = df.filter(regex="^weight_\\d+$").mean(axis=1)
    error_weights = average_weights / calc_weights
    distances = df["distance"]
    polynomial_regression.fit(distances.values, error_weights.values)
    return polynomial_regression


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
    df = read_measurements("example_measurements.csv")
    f0 = find_f0(df[df["distance"] >= 20])
    fge = find_fge(df, f0)
    fu = find_fu(df, f0, fge)
    print(f0)
    print(fge)
    print(fu)
