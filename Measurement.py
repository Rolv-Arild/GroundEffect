import time

import numpy as np
import pandas as pd

from Regression import FgRegression, exponential_model, cheeseman_model


class MeasurementWriter:
    def __init__(self, fname, n_measurements=4):
        self.file = open(fname, "w")
        self.n_measurements = n_measurements
        columns = ["time", "distance"] + \
                  [f"voltage_{n}" for n in range(n_measurements)] + \
                  [f"weight_{n}" for n in range(n_measurements)]
        self.file.write(",".join(columns) + "\n")

    def write(self, dist, voltages, weights):
        if not len(voltages) == len(weights) == self.n_measurements:
            raise ValueError
        values = [time.time(), dist] + voltages + weights
        values = [str(val) for val in values]
        self.file.write(",".join(values) + "\n")


def get_forces(w1, w2, w3, w4, a=0.2, b=0.2):
    f1 = (-w3 * a + w1 * (a + 2 * b)) / (2 * b)
    f2 = (-w4 * a + w2 * (a + 2 * b)) / (2 * b)
    f3 = (-w1 * a + w3 * (a + 2 * b)) / (2 * b)
    f4 = (-w2 * a + w4 * (a + 2 * b)) / (2 * b)

    return f1, f2, f3, f4


if __name__ == '__main__':
    m_file = MeasurementWriter("write_test.csv")


    def f0(v):
        return 10 * v


    def sim_f(voltages, distance):
        avg_volt = np.mean(voltages)
        # mult = cheeseman_model(distance, 15)
        mult = exponential_model(distance, 10, 3)
        base_weight = f0(avg_volt) * mult
        weights = [base_weight * (v / avg_volt + np.random.normal(scale=0.1)) for v in voltages]
        return weights


    volts = 10 * np.random.random((1000, 4))
    dists = 45 * np.random.random((1000,)) + 5

    for volt, dist in zip(volts, dists):
        m_file.write(dist, list(volt), sim_f(volt, dist))

    df = pd.read_csv("write_test.csv")
    corr = df.corr()
    print("Hei")
