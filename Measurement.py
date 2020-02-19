import time
import pandas as pd


class MeasurementWriter:
    def __init__(self, fname, n_measurements=4):
        self.file = open(fname, "w")
        self.n_measurements = n_measurements
        columns = ["time", "dist"] + \
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


if __name__ == '__main__':
    m_file = MeasurementWriter("write_test.csv")
    m_file.write(1, [2, 3, 4, 5], [6, 7, 8, 9])
    m_file.write(10, [11, 12, 13, 14], [15, 16, 17, 18])
