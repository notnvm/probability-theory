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
        self.win = [1]*(r+1)
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
                if u < mm/nn:
                    count += 1
                    nn = nn - 1
                    mm = mm - 1
                else:
                    nn = nn - 1
            ar.append(count)

        self.cnt = Counter(ar)
        self.series = sorted(self.cnt.most_common())
        print(self.series)
        # for yj, nj in sorted(self.cnt.most_common()):
        #     print(f'\nyj = {yj}, nj = {nj}, nj/n = {nj/self.n}\n')
        # print(f'\n\nself.m = {self.m}, self.n = {self.n}')
        # self.series = sorted(self.cnt.most_common())
        # print(self.series)
        return self.series #! sorted(self.cnt.most_common())
          
    def average(self):
        """compute sample mean"""
        
        avg = 0
        for xi, ni in self.series:
            avg += xi * ni
        avg /= self.p
        return avg
    
    def mean(self):
        """compute math expectation"""
        
        return (self.r * self.m)/self.n
    
    def variance(self):
        """compute dispersion"""
        
        return ((self.r*self.m)/(self.n-1))*(1-self.m/self.n)*(1-self.r/self.n)   
    
    def sample_variance(self):
        """compute sample dispersion"""
        
        sv = 0
        avg = self.average()
        for xi, ni in self.series:
            sv += ((xi - avg)**2)*ni
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
        for xi,_ in self.series:
            probability.append((math.comb(self.m, xi)*math.comb(self.n-self.m, self.r-xi))/math.comb(self.n,self.r))
        # print(probability)
        # print(sum(probability))
        return probability
    
    def max_deviation(self):
        """
             compute max deviation between relative frequency and probability\n
             max|nj/n - P(ξ = xi)|
        """
        probability = self.probability()
        relative_frequency = [i/self.p for _, i in self.series]
        max_deviation = -100
        for i in range(len(probability)):
            if max_deviation < abs(relative_frequency[i] - probability[i]):
                max_deviation = abs(relative_frequency[i] - probability[i])
        return max_deviation
        
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
        
        # print(f'prob = {probability}')
        # print(f'tdf = {tdf}')
        return tdf


    def sample_distribution_function(self):
        """
             compute sample distribution function\n
             F = [0, n1/n, n1/n+n2/n, ... , n1/n+n2/n+...+nk/n, 1]
        """
        sdf = [0]
        for _, ni in self.series:
            sdf.append(sdf[self.series.index((_, ni))] + ni/self.p)
            
        # print(f'rel_freq = {[i for _,i in self.series]}')
        # print(f'sdf = {sdf}')
        return sdf

    def measure_of_discrepancy(self):
        sdf = self.sample_distribution_function()
        tdf = self.theoretical_distribution_function()
        discrepancy = max([abs(sdf[i] - tdf[i]) for i in range(len(tdf))])
        return discrepancy


if __name__ == '__main__':
    p=int(input('p='))
    n=int(input('n='))    
    m=int(input('m='))
    r=int(input('r='))
    s = Solution(p, n, m, r)
    s.first()
    # print(f's.first() = {s.first()}')
    # print(f's.first()[0][0] = {s.first()[0][0]}')
    # tdf = s.theoretical_distribution_function()
    # sdf = s.sample_distribution_function()
    # print(f'series.len = {len(s.series)}')
    # print(f'tdf.len = {len(tdf)}')
    # print(f'sdf.len = {len(sdf)}')
    # print('\n', sum(s.probability()))