import random
import math
from collections import Counter

class Solution:
    def __init__(self, p, n, m, r):
        self.p = p
        self.n = n
        self.m = m
        self.r = r
        self.win = [1]*r
        self.cnt = {}
        
    def first(self):
        for i in range(self.r):
            rand_value = random.random()
            while rand_value > self.p:
                self.win[i] += 1
                rand_value = random.random()

        self.cnt = Counter(self.win)
        return sorted(self.cnt.most_common())
    
    def second(self):
        self.series = sorted(self.cnt.most_common())
        math_expect = (self.r * self.m)/self.n
        dispersion = (self.r * self.m)/(self.n-1)*(1-self.m/self.n)*(1-self.r/self.n)
        
        average = 0
        for x_i, n_i in self.series:
            average += x_i * n_i
        average /= self.n
        
        s2 = 0
        for x_i, n_i in self.series:
            s2 += (x_i - average)**2 * n_i
        s2 /= self.n
        
        R = self.series[-1][0] - self.series[0][0]
        
        k = len(self.series) - 1
        median = 0
        if len(self.series) % 2 == 0:
            median = (self.series[k//2][0] + self.series[k//2 + 1][0]) / 2
        else:
            median = self.series[k//2][0]
            
        return math_expect, average, math.fabs(math_expect - average), dispersion, s2,  math.fabs(dispersion-s2), median, R
    
    def generate_plot_data(self):     
        self.sums = [0] * len(self.series)
        probability = [0] * len(self.series)
        self.sums[0] = self.p
        
        for x_i, n_i in self.series:
            probability.append((math.comb(self.m, x_i)*math.comb(self.n-self.m, self.r-x_i))/math.comb(self.n,self.r))
        
        for i in range(1, len(self.series) - 1):
            self.sums[i] = self.sums[i - 1] + probability[i - 1]
        self.sums[-1] = 1
        
        print(self.sums)

        self.probability_selective  = []
        for _, n_i in self.series:
            self.probability_selective .append(n_i / self.n)
        self.prefix_sums = [0] * len(self.series)
        self.prefix_sums[0] = self.probability_selective[0]
        for i in range(1, len(self.series)):
            self.prefix_sums[i] = self.prefix_sums[i - 1] + self.probability_selective[i - 1]
        self.diff = 0
        for a, b in zip(self.prefix_sums, self.sums):
            if math.fabs(a - b) > self.diff:
                self.diff = math.fabs(a - b)
    
    

if __name__ == '__main__':
    p = float(input("p = "))
    n = int(input("n = "))
    m = int(input("m = "))
    r = int(input("r = "))
    solution = Solution(p, n, m, r)
    answer = solution.first()
    print(answer)
        