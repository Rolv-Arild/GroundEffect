import numpy as np
import pandas as pd
from sklearn.metrics import mean_squared_error
from sklearn.neural_network import MLPRegressor

from Regression import CurveRegression, exponential_model


def f(x, y, z):
    return x + y + z


def linear(x, a):
    return a * x


class Drone:
    def __init__(self, dist_cutoff, f_0: CurveRegression, f_ge: CurveRegression, f_u: MLPRegressor, n=4):
        self.n = n
        self.dist_cutoff = dist_cutoff
        self.f_0 = f_0
        self.f_ge = f_ge
        self.f_u = f_u

    def fit(self, df: pd.DataFrame):
        distances = df["distance"]
        voltages = df.filter(regex="^voltage_\\d+$")
        weights = df.filter(regex="^weight_\\d+$")
        forces = self.get_forces(weights)

        off_ground = distances > self.dist_cutoff

        self.f_0.fit(voltages[off_ground].values.reshape((-1,)), forces[off_ground].values.reshape((-1,)))
        base_pred = self.f_0.predict(voltages.values.reshape(-1, )).reshape((-1, self.n))
        ground_factor = (forces.values / base_pred).mean(axis=1)  # F = F0 * Fge -> Fge = F / F0
        valid = np.isfinite(ground_factor)  # Filter out invalid values (nan, inf, -inf)
        ground_factor = ground_factor[valid]
        dists = distances.values[valid]

        self.f_ge.fit(dists, ground_factor)
        ge = self.f_ge.predict(distances.values).reshape((-1, 1))

        unknown = forces.values - base_pred * ge  # F = F0 * Fge + Fu -> Fu = F - F0 * Fge

        self.f_u.fit(pd.concat((voltages, distances), axis=1).values, unknown)

    def score_predict(self, df):
        distances = df["distance"]
        voltages = df.filter(regex="^voltage_\\d+$")
        weights = df.filter(regex="^weight_\\d+$")
        forces = self.get_forces(weights)

        scores = []
        base_pred = self.f_0.predict(voltages.values.reshape(-1, )).reshape((-1, self.n))
        res = base_pred
        scores.append(mean_squared_error(forces.values, res))
        ge = self.f_ge.predict(distances.values).reshape((-1, 1))
        res *= ge
        scores.append(mean_squared_error(forces.values, res))
        unk = self.f_u.predict(pd.concat((voltages, distances), axis=1).values)
        res += unk
        scores.append(mean_squared_error(forces.values, res))

        return res, scores

    def predict(self, df):
        distances = df["distance"]
        voltages = df.filter(regex="^voltage_\\d+$")

        base_pred = self.f_0.predict(voltages.values.reshape(-1, )).reshape((-1, self.n))
        ge = self.f_ge.predict(distances.values).reshape((-1, 1))
        unk = self.f_u.predict(pd.concat((voltages, distances), axis=1).values)

        return base_pred * ge + unk

    def get_forces(self, df, a=0.2, b=0.2):
        forces = pd.DataFrame(columns=[f"force_{i}" for i in range(self.n)])
        for i in range(self.n):
            opposite = (i + self.n // 2) % self.n
            forces[f"force_{i}"] = (-df[f"weight_{opposite}"] * a + df[f"weight_{i}"] * (a + 2 * b)) / (2 * b)

        return forces


if __name__ == '__main__':
    d = Drone(25, CurveRegression(linear), CurveRegression(exponential_model),
              MLPRegressor((64, 64, 64, 64, 64), max_iter=1000))
    data = pd.read_csv("write_test.csv")
    d.fit(data[:8000])
    pred, scores = d.score_predict(data[8000:])
