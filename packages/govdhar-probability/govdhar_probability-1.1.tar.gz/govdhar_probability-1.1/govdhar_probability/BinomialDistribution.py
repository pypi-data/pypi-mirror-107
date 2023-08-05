import math
import matplotlib.pyplot as plt
from .GeneralDistributions import Distribution

class Binomial(Distribution):
    def __init__(self, prob=.5, size=20):
        self.p = prob
        self.n = size
        Distribution.__init__(self, self.calculate_mean(), self.calculate_stdev())

    def calculate_mean(self):
        self.mean = self.p * self.n
        return self.mean

    def calculate_stdev(self):
        self.stdev = math.sqrt(self.mean * (1 - self.p))
        return self.stdev

    def replace_stats_with_data(self):
        self.n = len(self.data)
        self.p = sum(self.data) / self.n
        self.mean = self.calculate_mean()
        self.stdev = self.calculate_stdev()
        return self.p, self.n

    def plot_bar(self):
        fig = plt.figure()
        ax = fig.add_axes([0, 0, 1, 1])
        outcome = ['0', '1']
        result = [1 - sum(self.data), sum(self.data)]
        ax.bar(outcome, result)
        plt.title('Binomial Distribution')
        plt.xlabel("Outcome")
        plt.ylabel("Count")
        plt.show()

    def pdf(self, k):
        a = math.factorial(self.n) / (math.factorial(k) * (math.factorial(self.n - k)))
        b = (self.p ** k) * (1 - self.p) ** (self.n - k)
        return a * b

    def plot_bar_pdf(self):
        xval, yval = []
        n = len(self.data)
        for k in range(n + 1):
            xval.append(k)
            yval.append(self.pdf(k))
        return xval, yval

        plt.bar(xval, yval)
        plt.title('Binomial Distribution')
        plt.xlabel('# of Successes')
        plt.ylabel('Binomial pdf')

    def __add__(self, other):
        try:
            assert self.p == other.p, 'p values are not equal'
        except AssertionError as error:
            raise
        sum_bin = Binomial()
        sum_bin.n = self.n + other.n
        sum_bin.p = self.p
        sum_bin.calculate_mean()
        sum_bin.calculate_stdev()
        return sum_bin

    def __repr__(self):
        return "mean {}, standard deviation {}, p {}, n {}".format(self.mean, self.stdev, self.p, self.n)
