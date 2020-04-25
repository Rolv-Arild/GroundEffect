import numpy as np
import pandas as pd

from Measurement import MeasurementWriter
from Regression import exponential_model, cheeseman_model


def gen_data(writer, force_per_volt=3, a=0.2, b=0.2, n=10000, dist_min=5, dist_max=50, volt_min=-10, volt_max=70):
    def f0(v):
        return force_per_volt * v

    def sim_f(voltages, distance):
        avg_volt = np.mean(voltages)
        mult = cheeseman_model(distance, 15)
        # mult = exponential_model(distance, 10, 3)
        base_weight = f0(avg_volt) * mult
        forces = [base_weight * v / (avg_volt or 1) for v in voltages]
        # w1 = (2 * b * f1 + a * (f1 + f3))/(2 * (a + b))
        weights = []
        for i, f in enumerate(forces):
            opposite = forces[(i + 2) % 4]
            w = (2 * b * f + a * (f + opposite)) / (2 * (a + b))
            if np.isnan(w):
                print("Hei")
            weights.append(w)

        return weights

    volts = (volt_max - volt_min) * np.random.random((n, 4)) + volt_min
    np.maximum(volts, 0, volts)
    dists = (dist_max - dist_min) * np.random.random((n,)) + dist_min
    np.maximum(dists, 0, dists)

    for volt, dist in zip(volts, dists):
        m_file.write(dist, list(volt), sim_f(volt, dist))


if __name__ == '__main__':
    m_file = MeasurementWriter("write_test.csv")

    gen_data(m_file)

    df = pd.read_csv("write_test.csv")
    corr = df.corr()
