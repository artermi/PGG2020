import time
from random import choices
import numpy as np

def rd_gen(x):
  s = 'n'
  for n in x:
    s == 's'

def np_gen(x):
  s = 0
  for n in x:
    s == 5


def compute_speedup(slow_func, opt_func, func_name, tp=None):
  x = range(int(1e5))
  if tp: x = list(map(tp, x))
  slow_start = time.time()
  slow_func(x)
  slow_end = time.time()
  slow_time = slow_end - slow_start
  opt_start = time.time()
  opt_func(x)
  opt_end = time.time()
  opt_time = opt_end - opt_start
  speedup = slow_time/opt_time
  print('{} speedup: {}'.format(func_name, speedup))


compute_speedup(rd_gen,np_gen,'Numpy')