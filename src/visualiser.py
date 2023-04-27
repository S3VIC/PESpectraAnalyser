import matplotlib.pyplot as plt
import matplotlib as mlt
import numpy as np
import src.interface as inter


def plotRawCorrectedSpectra(fileName, shifts, x, z):
    mlt.use("SVG")
    plt.plot(shifts, x - z)
    plt.plot(shifts, z)
    plt.plot(shifts, x)
    plt.savefig(fileName)
    plt.close()



def getCrystalData(filePath):
  mlt.use('SVG')
  dataFile = np.loadtxt(filePath, delimiter = '\t')
  cryst_1 = np.array(dataFile[:, 0], dtype = 'float')
  cryst_2 = np.array(dataFile[:, 1], dtype = 'float')
  cryst_3 = np.array(dataFile[:, 2], dtype = 'float')
  cryst_4 = np.array(dataFile[:, 3], dtype = 'float')

  fig, ax = plt.subplots(1, 1)
  bin_num = 100
  n, bins, patches = ax.hist(cryst_1, bin_num, density = False, histtype = 'stepfilled', cumulative = False)

  plt.savefig('cryst_1_raw_n2.svg')
  plt.close()


      
def plotBarChart(title, xTicks, counts):
    fig, ax = plt.subplots()
    fig.suptitle(title)
    ax.set_ylabel("Liczba")
    plt.bar(xTicks, counts)
    plt.savefig(title + ".png")
    plt.close()



def plotPartialSpectra(spectra, path, fileName):
    mlt.use("Cairo")
    fig, ax = plt.subplots()
    ax.set_ylabel("Intensity [arb. units]")
    ax.set(yticklabels = []) # removing ytick labels 
    ax.set_xlabel("Raman shift [cm$^{-1}]$")
    plt.plot(spectra[0], spectra[1])
    #plt.xlim([40, 3420]) #limitting xaxis range
    plt.gca().invert_xaxis() # inverting xaxis
    plt.savefig(path + fileName + ".png", dpi = 400)
    plt.close()


def plotCrystScatter(path1, path2, path3, path4):
    print("Nothing")

