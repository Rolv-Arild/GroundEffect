import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import PolynomialFeatures


class PolynomialRegression:
    def __init__(self, degree, bias=True):
        self.polynomial_features = PolynomialFeatures(degree=degree, include_bias=bias)
        self.linear_regression = LinearRegression(fit_intercept=bias)
        self.pipeline = make_pipeline(self.polynomial_features, self.linear_regression)

    def fit(self, x: list, y: list):
        self.pipeline.fit(np.reshape(x, (-1, 1)), y)

    def predict(self, x: list):
        return self.pipeline.predict(np.reshape(x, (-1, 1)))

    def score(self, x, y):
        return self.pipeline.score(np.reshape(x, (-1, 1)), y)

    def __str__(self):
        parts = []
        deg = 0 if self.linear_regression.intercept_ else 1
        for coef in self.linear_regression.coef_:
            if abs(coef) > 1.0e-15:
                if deg == 0:
                    s = f"{round(coef, 5)}"
                elif deg == 1:
                    s = f"{round(coef, 5)}*x"
                else:
                    s = f"{round(coef, 5)}*x^{deg}"
                parts.append(s)
            deg += 1
        return "+".join(reversed(parts))


class Drone:
    def f0(self, voltages):
        avg_voltage = sum(voltages) / len(voltages)
        return 0.01 * avg_voltage ** 3 + 0.1 * avg_voltage ** 2 + avg_voltage

    def f_ground_effect(self, dist, voltages):
        # avg_voltage = sum(voltages) / len(voltages)
        return self.f0(voltages)

    def f_unknown(self, dist, voltages):
        pass


if __name__ == '__main__':
    def f(x):
        return 0.01 * x ** 3 + 0.1 * x ** 2 + x


    voltage_forces = [(v, f(v)) for v in range(10)]

    voltages, forces = zip(*voltage_forces)

    x_train, y_train = voltages[::2], forces[::2]
    x_test, y_test = voltages[1::2], forces[1::2]

    pr = PolynomialRegression(3, False)

    pr.fit(x_train, y_train)
    print(pr.score(x_test, y_test))
    print(pr)
    print(max(abs(pred - actual) for actual, pred in zip(y_test, pr.predict(x_test))))
