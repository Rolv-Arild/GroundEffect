from pandas import DataFrame

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
    polynomial_regression = PolynomialRegression(3, bias=False)
    average_voltages = df.filter(regex="^voltage_\\d+$").mean(axis=1)
    average_weights = df.filter(regex="^weight_\\d+$").mean(axis=1)
    polynomial_regression.fit(average_voltages.values, average_weights.values)
    return polynomial_regression


if __name__ == '__main__':
    df = read_measurements("example_measurements.csv")
    f0 = find_f0(df[df["distance"] >= 20])
    print(f0)
