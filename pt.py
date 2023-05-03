import random
import math
from collections import Counter


class Solution:
    def __init__(self, p, n, m, r):
        self.p = p
        self.n = n
        self.m = m
        self.r = r
        self.win = [1]*(r+1)
        self.cnt = {}
        
    def first(self):
        for i in range(self.r+1):
            rand_value = random.random()
            while rand_value < self.p:
                self.win[i] += 1
                rand_value = random.random()
        
        print(type(self.win))
        return self.win
    
    #  В лотерее среди N билетов M выигрышных. Игрок покупает r билетов.
    #     С.в. η — число выигрышных билетов среди купленных.
    
    def second(self):   
        # self.series = sorted(self.cnt.most_common()) # type: ignore
        math_expect = (self.r * self.m)/self.n
        dispersion = (self.r * self.m)/(self.n-1)*(1-self.m/self.n)*(1-self.r/self.n)
        
        average = 0
        for i in range(self.r):
            average += (i+1)*self.win[i]
        average /= self.n
        
        s2 = 0
        for i in range(self.r):
            s2 += ((i+1) - average)**2 * self.win[i]
        s2 /= self.n
        
        R = self.r - 1
        
        k = len(self.win) - 1
        median = 0
        if len(self.win) % 2 == 0:
            median = (k//2 + k//2 + 1) / 2
        else:
            median = k//2
            
        return math_expect, average, math.fabs(math_expect - average), dispersion, s2,  math.fabs(dispersion-s2), median, R
    
    def generate_plot_data(self):
        self.sums = [0] * len(self.win)
        self.sums[0] = 0
        
        probability = [0] * len(self.win)
        for i in range(self.r):
            probability[i] = ((math.comb(self.m, (i+1))*math.comb(self.n-self.m, self.r-(i+1)))/math.comb(self.n,self.r)) 
        
        # print(probability)    
            
        for i in range(1, len(self.win) - 1):
            self.sums[i] = self.sums[i - 1] + probability[i-1]
        self.sums[-1] = 1
         # print(f'\n\n{self.sums}')
         
        probability_selective = []
        for i in self.win:
            probability_selective.append(i / self.n)
            
        print(f'\n\probability:\n{probability}')      
        print(f'probability_selective:\n{probability_selective}\n')     
        print(f'sum_probability_selective:{sum(probability_selective)}\n\n')    
             
        self.prefix_sums = [0] * len(self.win)
        self.prefix_sums[0] = 0
        for i in range(1, len(self.win) - 1):
            self.prefix_sums[i] = self.prefix_sums[i - 1] + probability_selective[i-1]
            
        print(f'\n\sums:\n{self.sums}')      
        print(f'prefix_sums:\n{self.prefix_sums}') 
            
        self.diff = 0
        for a, b in zip(self.prefix_sums, self.sums):
            if math.fabs(a - b) > self.diff:
                self.diff = math.fabs(a - b)
        print(f'max_diff={self.diff}')        
    
        # print(f'\n\n{self.sums}')


if __name__ == '__main__':
    p = float(input("p = "))
    n = int(input("n = "))
    m = int(input("m = "))
    r = int(input("r = "))
    solution = Solution(p, n, m, r)
    answer = solution.first()
    solution.generate_plot_data()
    print(answer)
        