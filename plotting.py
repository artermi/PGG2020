import matplotlib.pyplot as plt
import numpy as np

f = open("result.txt")
rG = []
lo = []

for line in f:
     rG.append("%.2f" % float(line.split()[0]) )
     lo.append(float(line.split()[1]))

plt.plot(rG,lo,'ks')
plt.show()
