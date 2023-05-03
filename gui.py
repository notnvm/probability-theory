import tkinter as tk
from tkinter import ttk
import pt as task
import math

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

class Gui:
    def __init__(self, master):
        master.title("Моделирование случайной величины")
        master.geometry('1680x960')
        master["bg"] = "#252526" 
        self.master = master
        
        self.label_p = tk.Label(master, text='Введите значение p:', foreground="white",background='#252526', font='Arial 12')
        self.label_p.place(x=0, y=0)
        self.label_n = tk.Label(master, text='Введите значение N:', foreground="white",background='#252526', font='Arial 12')
        self.label_n.place(x=0, y=40)
        self.label_m = tk.Label(master, text='Введите значение M:', foreground="white",background='#252526', font='Arial 12')
        self.label_m.place(x=0, y=80)
        self.label_r = tk.Label(master, text='Введите значение r:', foreground="white",background='#252526', font='Arial 12')
        self.label_r.place(x=0, y=120)
        
        
        self.p_val = tk.Entry(master, font='Arial 12', width=16, foreground='white',background='#252526')
        self.p_val.place(x=160, y=3)
        
        self.n_val = tk.Entry(master, font='Arial 12', width=16, foreground='white',background='#252526')
        self.n_val.place(x=160, y=43)
        
        self.m_val = tk.Entry(master, font='Arial 12', width=16, foreground='white',background='#252526')
        self.m_val.place(x=160, y=83)
        
        self.r_val = tk.Entry(master, font='Arial 12', width=16, foreground='white',background='#252526')
        self.r_val.place(x=160, y=123)
        
        self.solve_btn = tk.Button(master, text='Решить', font='Arial 12', width=33, foreground='white', background='#252526', command=self.solve_callback)
        self.solve_btn.place(x=0, y=150)
        
        self.fig, self.ax = plt.subplots(1, 1)
        self.fig.set_facecolor('#252526')
        self.fig.set_size_inches(5, 5)
        self.ax.grid(True)
        self.ax.set_facecolor("white")
        self.ax.set_title("График функции распределения", color='white')
        self.ax.tick_params(axis='x', colors='white')
        self.ax.tick_params(axis='y', colors='white')
        chart = FigureCanvasTkAgg(self.fig, master)
        chart.get_tk_widget().place(x=680, y=350)
        
    def solve_callback(self):
        self.ax.clear()
        self.ax.grid(True)
        self.ax.set_title("График функции распределения", color='white')
        
        
        p = float(self.p_val.get())
        n = int(self.n_val.get())
        m = int(self.m_val.get())
        r = int(self.r_val.get())
        solution = task.Solution(p, n, m, r)
        first_task = solution.first()
        print(first_task)
        math_expect, average, diff_avg, dispersion, s2,  diff_disp, median, R = solution.second()

        heads = ["y_i", "n_i", "n_i / n"]
        self.table_ft = ttk.Treeview(self.master, show='headings', columns=heads, height=4)
        for header in heads:
            self.table_ft.heading(header, text=header, anchor='center')
            self.table_ft.column(header, anchor='center', width=455)
        for i in range(r+1):
            self.table_ft.insert("", tk.END, values=(i, first_task[i], first_task[i]/n))
        self.scrollbary = tk.Scrollbar(self.master, orient=tk.VERTICAL)
        self.table_ft.configure(yscrollcommand=self.scrollbary.set)
        self.scrollbary.configure(command=self.table_ft.yview)
        
        topics = ["Mn", "x̂", "|Mn - x̂|", "Dn", "S^2", "|Dn - S^2|", "Me", "R"]
        self.table_sd = ttk.Treeview(self.master, show='headings', columns=topics, height=2)
        for topic in topics:
            self.table_sd.heading(topic, text=topic, anchor='center')
            self.table_sd.column(topic, anchor='center', width=175)
        self.table_sd.insert("", tk.END, values=(math_expect, average, diff_avg, dispersion, s2,  diff_disp, median, R))
        
        parts = ['y_j', 'P(n = y_j)', 'n_j / n']
        self.probs_table = ttk.Treeview(self.master, show='headings', columns=parts, height=4)
        for part in parts:
            self.probs_table.heading(part, text=part, anchor='center')
            self.probs_table.column(part, anchor='center', width=455)
        max_deviation = 0
        # prob_res = []
        for i in range(r+1):
            probability = (math.comb(m, (i))*math.comb(n-m, r-(i)))/math.comb(n,r)
            # prob_res.append(probability)
            if math.fabs(first_task[i]/n - probability) > max_deviation:
                max_deviation = first_task[i]/n - probability
            self.probs_table.insert("", tk.END, values=((i), probability, first_task[i]/n))
        
        self.label_max_deviation = tk.Label(self.master, text=f'Величина max|n_j / n - P(n = y_j)| = {round(max_deviation, 4)}', foreground="white",background='#252526', font='Arial 12')
        self.label_max_deviation.place(x=0, y=180)  
         
        # print(sum(prob_res))        
        self.scrollbar = ttk.Scrollbar(self.master, orient=tk.VERTICAL)
        self.table_ft.configure(yscrollcommand=self.scrollbar.set)
        self.scrollbar.configure(command=self.probs_table.yview)
        self.table_ft.place(x=320, y=0)
        self.table_sd.place(x=320, y=110)
        self.probs_table.place(x=320, y=180)
        
        solution.generate_plot_data()
        
        for i in range(r-1):
            self.ax.plot((i, i+1), (solution.sums[i], solution.sums[i]),
                         color='red', linewidth=2)
            self.ax.plot((i, i+1), (solution.prefix_sums[i], solution.prefix_sums[i]),
                         color='blue', linewidth=2)
            
        self.ax.plot((r-1, r), (1, 1), color='red', linewidth=2, label='F(x)')
        self.ax.plot((r-1, r), (1, 1), color='blue', linewidth=2, label='F^(x)')

        self.ax.grid(True)
        self.ax.legend()
        chart = FigureCanvasTkAgg(self.fig, self.master)
        chart.get_tk_widget().place(x=680, y=350)
        
        self.label_max_diff_f = tk.Label(self.master, text=f'Мера расхождения D = {round(solution.diff, 4)}', foreground="white",background='#252526', font='Arial 12')
        self.label_max_diff_f.place(x=0, y=200)  
        
        
window = tk.Tk()
gui = Gui(window)
window.mainloop()