#! /usr/bin/env python3
import matplotlib
matplotlib.use('Agg')
from pylab import *
from fit_ols import *

if __name__ == '__main__':
  x = rand(3,3)
  y = rand(3)
  sol = fit_ols(x,y)
  print(sol)
