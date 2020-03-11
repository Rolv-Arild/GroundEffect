import numpy as np
from pandas import DataFrame, read_csv
from scipy.optimize import curve_fit
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


class FgRegression:
    def __init__(self, model, init_param=None):
        self.model = model
        self.param = init_param
        self.covar = None

    def predict(self, distances):
        return self.model(distances, *self.param)

    def fit(self, x, y):
        solution = curve_fit(self.model, x.values, y.values, p0=self.param)

        self.param = solution[0]
        self.covar = solution[1]

    def __str__(self):
        return f"F_G:{self.model}Parameters:{self.param}"


def cheeseman_model(x, rho):
    return 1 / (1 - rho * (1 / x) ** 2)


def exponential_model(x, a, b):
    return a * np.exp(-x / b) + 1


def piecewise_linear_model(x, y_intersect, cutoff):
    def linear(xn):
        slope = (1 - y_intersect) / cutoff
        return slope * xn + y_intersect

    return np.piecewise(x, [x < cutoff, x >= cutoff], [linear, 1])


def log_model(x, a, b):
    return a * np.log(b * x + 1)


def find_f0(df: DataFrame):
    polynomial_regression = PolynomialRegression(2, bias=False)
    # polynomial_regression = FgRegression(log_model)
    average_voltages = df.filter(regex="^voltage_\\d+$").mean(axis=1)
    average_weights = df.filter(regex="^weight_\\d+$").mean(axis=1)
    polynomial_regression.fit(average_voltages.values, average_weights.values)
    return polynomial_regression


def find_fge(df: DataFrame, f0, model):
    average_voltages = df.filter(regex="^voltage_\\d+$").mean(axis=1)
    calc_weights = f0.predict(average_voltages.values)
    average_weights = df.filter(regex="^weight_\\d+$").mean(axis=1)
    error_weights = average_weights / calc_weights
    distances = df["distance"]
    model.fit(distances, error_weights)
    return model


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
    from mpl_toolkits.mplot3d import Axes3D

    df = read_csv("write_test.csv")
    f0 = find_f0(df[df["distance"] >= 40])
    fge = find_fge(df, f0, FgRegression(exponential_model))
    fu = find_fu(df, f0, fge)
    print(f0)
    print(fge)
    print(fu)
    # print(f0.predict(np.ones(300)) * fge.predict(np.arange(0, 30, 0.1)))

    fig = plt.figure(1)
    ax = fig.add_subplot(111, projection='3d')
    avg_voltages = df.filter(regex="^voltage_\\d+$").mean(axis=1)
    avg_weights = df.filter(regex="^weight_\\d+$").mean(axis=1)
    ax.scatter(xs=avg_voltages, ys=df["distance"], zs=avg_weights)
    plt.show()

    exit(0)
    df = df[(df["distance"] - 30).abs() < 3]
    plt.scatter(df["voltage_1"], df['weight_1'])
    plt.plot(np.arange(0, 10, 0.1), f0.predict(np.arange(0, 10, 0.1)) * fge.predict(np.array([30])), color="blue")
    plt.plot(np.arange(0, 10, 0.1), f0.predict(np.arange(0, 10, 0.1)), color="orange")
    plt.show()

