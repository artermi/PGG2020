import matplotlib.pyplot as plt
import numpy as np
import os
import statistics

rG = []
lo = []

for fi in os.listdir("sim"):
    num = float(fi[4:8])/5000
    rG.append(num)
    with open('sim/' + fi,'r') as f:
        all_num = []
        for line in f:
            rnd, per = int(line.split()[0]), float(line.split()[1])
            if rnd < 5000:
                continue
            all_num.append(per)
        lo.append(statistics.mean(all_num))


plt.plot(rG,lo,'ks')
plt.show()

