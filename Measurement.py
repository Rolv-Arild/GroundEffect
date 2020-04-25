import time


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
            raise ValueError  #
        values = [time.time(), dist] + voltages + weights
        values = [str(val) for val in values]
        self.file.write(",".join(values) + "\n")
