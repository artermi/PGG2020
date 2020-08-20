import numpy as np 
import statistics

alp = 1/1.230
x = []
for i in range(100000):
	 y = np.random.exponential(scale = alp)
	 y = y - int(y)

	 x.append(y)

print(statistics.mean(x))