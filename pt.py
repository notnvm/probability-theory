import random
import math
from collections import Counter


class Solution:
    def __init__(self, p: int, n: int, m: int, r: int):
        """
            В лотерее среди N билетов M выигрышных. Игрок покупает r билетов.
            С.в. η — число выигрышных билетов среди купленных.

            p: int - Число экспериментов
            n: int - Общее число билетов
            m: int - Число выигрышных билетов
            r: int - Число купленных билетов
        """

        self.p = p
        self.n = n
        self.m = m
        self.r = r
        self.win = [1] * (r + 1)
        self.cnt = {}

    def first(self):
        """Simulation of an experiment\n
            Hypergeometric distribution"""
        ar = []
        for j in range(self.p):
            count = 0
            nn = self.n
            mm = self.m
            for i in range(self.r):
                u = random.random()
                if u < mm / nn:
                    count += 1
                    nn = nn - 1
                    mm = mm - 1
                else:
                    nn = nn - 1
            ar.append(count)

        self.cnt = Counter(ar)
        self.series = sorted(self.cnt.most_common())

        return self.series  

    def average(self):
        """compute sample mean"""
        avg = 0
        for xi, ni in self.series:
            avg += xi * ni
        avg /= self.p
        
        return avg

    def mean(self):
        """compute math expectation"""

        return (self.r * self.m) / self.n

    def variance(self):
        """compute dispersion"""

        return ((self.r * self.m) / (self.n - 1)) * (1 - self.m / self.n) * (1 - self.r / self.n)

    def sample_variance(self):
        """compute sample dispersion"""
        sv = 0
        avg = self.average()
        for xi, ni in self.series:
            sv += ((xi - avg) ** 2) * ni
        sv /= self.p
        
        return sv

    def sample_size(self):
        return self.series[-1][0] - self.series[0][0]

    def sample_median(self):
        x = [i for i, _ in self.series]
        return (x[len(x) // 2] + x[len(x) // 2 - 1]) / 2 if len(x) % 2 == 0 else x[len(x) // 2]

    def probability(self):
        """
            compute theoretical probability\n
            C(n, k)\n
            P(ξ = xi) = C(m, xi) * C(n-m, r-xi) / C(n, r)
        """
        probability = []
        for i in range(self.r+1):
            probability.append(
                (math.comb(self.m, i) * math.comb(self.n - self.m, self.r - i)) / math.comb(self.n, self.r))

        return probability

    def second(self):
        """ compute all numerical characteristics\n
            return [E, sample_mean_x, abs_diff_mean, D, SS, abs_diff_variance, self.sample_median(), self.sample_size()]
        """
        E = self.mean()
        sample_mean_x = self.average()
        abs_diff_mean = abs(E - sample_mean_x)
        D = self.variance()
        SS = self.sample_variance()
        abs_diff_variance = abs(D - SS)
        
        return [E, sample_mean_x, abs_diff_mean, D, SS, abs_diff_variance, self.sample_median(), self.sample_size()]

    def theoretical_distribution_function(self):
        """
             compute theoretical distribution function\n
             F = [0, p1, p1+p2, ... , p1+p2+...+pk, 1]
        """
        probability = self.probability()
        tdf = [0]
        for i in range(len(probability)):
            tdf.append(tdf[i] + probability[i])

        return tdf

    def get_tdf_intervals(self):
        """
             compute theoretical distribution function intervals\n
             exmpl: (x_min, x_max, probability)
        """
        tdf = self.theoretical_distribution_function()
        tdf_intervals = [(-2, 0, 0)]
        for i in range(self.r):
            tdf_intervals.append((i, i+1, tdf[i+1]))
        tdf_intervals.append((self.r, self.r+2, 1))

        return tdf_intervals
          
    def sample_distribution_function(self):
        """
             compute sample distribution function\n
             F = [0, n1/n, n1/n+n2/n, ... , n1/n+n2/n+...+nk/n, 1]
        """
        sdf = [0]
        for _, ni in self.series:
            sdf.append(sdf[self.series.index((_, ni))] + ni / self.p)

        return sdf
    
    def get_sdf_intervals(self):
        """
             compute sample distribution function intervals\n
             exmpl: (x_min, x_max, probability)
        """   
        sdf = self.sample_distribution_function()
        sdf_intervals = [(-2, self.series[0][0], 0)]
        for i in range(len(self.series) - 1):
            sdf_intervals.append((self.series[i][0], self.series[i+1][0], sdf[i+1]))
        sdf_intervals.append((self.series[-1][0], self.r+2, 1))

        return sdf_intervals

    def measure_of_discrepancy(self):
        """
             compute discrepancy of sdf and tdf\n
             D = max|nj/n - P(ξ = xj)|
        """
        discrepancy = 0
        sdfi = self.get_sdf_intervals()
        tdfi = self.get_tdf_intervals()
        
        for xmin, xmax, probability in sdfi:
            for i in range(len(tdfi)):
                if (xmin == tdfi[i][0] or xmax == tdfi[i][1]) and abs(probability - tdfi[i][2]) > discrepancy:
                    discrepancy = abs(probability - tdfi[i][2])

        return discrepancy