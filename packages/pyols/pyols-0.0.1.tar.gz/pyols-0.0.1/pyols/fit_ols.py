import numpy

def fit_ols(x, y):
  m, n = x.shape
  x1 = numpy.hstack((numpy.ones((m,1)), x))
  sol = numpy.linalg.solve(numpy.dot(x1.T,x1), numpy.dot(x1.T,y))
  return sol
