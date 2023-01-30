import matplotlib.pyplot as plt
import matplotlib as mlt
import numpy as np

# mlt.use('SVG')

def getCrystalData(filePath):
  mlt.use('SVG')
  dataFile = np.loadtxt(filePath, delimiter = '\t')
  cryst_1 = np.array(dataFile[:, 0], dtype = 'float')
  cryst_2 = np.array(dataFile[:, 1], dtype = 'float')
  cryst_3 = np.array(dataFile[:, 2], dtype = 'float')
  cryst_4 = np.array(dataFile[:, 3], dtype = 'float')

  fig, ax = plt.subplots(1, 1)
  bin_num = 50
  n, bins, patches = ax.hist(cryst_1, bin_num, density = False, histtype = 'stepfilled', cumulative = False)

  plt.savefig('test.svg')
