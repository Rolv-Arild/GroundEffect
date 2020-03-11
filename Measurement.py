import time
import pandas as pd
import numpy as np


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


def read_measurements(fname):
    return pd.read_csv(fname)


def get_forces(w1, w2, w3, w4, a=0.14, b=0.08):
    f1 = (-w3 * a + w1 * (a + 2 * b)) / (2 * b)
    f2 = (-w4 * a + w2 * (a + 2 * b)) / (2 * b)
    f3 = (-w1 * a + w3 * (a + 2 * b)) / (2 * b)
    f4 = (-w2 * a + w4 * (a + 2 * b)) / (2 * b)

    return f1, f2, f3, f4


if __name__ == '__main__':
    m_file = MeasurementWriter("write_test.csv")
    m_file.write(1, [2, 3, 4, 5], [6, 7, 8, 9])
    m_file.write(10, [11, 12, 13, 14], [15, 16, 17, 18])
    print(get_forces(2000, 1000, 1000, 1000))
