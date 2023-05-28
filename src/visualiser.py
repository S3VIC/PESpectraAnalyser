import matplotlib.pyplot as plt
import matplotlib as mlt
import numpy as np
import src.interface as inter
from enum import Enum
import params.parameters as par
#### ENUM SECTION ####
class Color(Enum):
    RED = 0
    YELLOW = 1
    BLUE = 2
    GREEN = 3


class Markers(Enum):
    CROSS = 0
    SQUARE = 1
    TRIANGLE = 2
    DIAMOND = 3


def getBgType(fileName):
    bgType = fileName[fileName.index("_") + 1 : -4]
    match bgType:
        case "raw":
            return Markers.CROSS
        case "asLS":
            return Markers.SQUARE
        case "arLS":
            return Markers.TRIANGLE
        case "at":
            return Markers.DIAMOND
        case other:
            assert False, "Error, bgType not recognised!"


def getCrystType(fileName):
    crystType = int(fileName[5])
    match crystType:
        case 1:
            return Color.RED
        case 2:
            return Color.YELLOW
        case 3:
            return Color.BLUE
        case 4:
            return Color.GREEN 
        case other:
            assert False, "Error, index out of enum range!"


###################################################################


def plotRawCorrectedSpectra(fileName, shifts, x, z):
    mlt.use("SVG")
    plt.plot(shifts, x - z)
    plt.plot(shifts, z)
    plt.plot(shifts, x)
    plt.savefig(fileName)
    plt.close()


def plotBarChart(title, xTicks, counts):
    fig, ax = plt.subplots()
    fig.suptitle(title)
    ax.set_ylabel("Liczba")
    plt.bar(xTicks, counts)
    plt.savefig(title + ".png")
    plt.close()


def plotPartialSpectra(initialSpectra, spectra, path, fileName):
    mlt.use("Cairo")
    fig, ax = plt.subplots()
    ax.set_ylabel("Intensity [arb. units]")
    #ax.set(yticklabels = []) # removing ytick labels 
    ax.set_xlabel("Raman shift [cm$^{-1}]$")
    baseline = np.array([], dtype = 'float64')
    for i in range(len(initialSpectra[0])):
        for k in range(len(spectra[0])):
            if(initialSpectra[0][i] == spectra[0][k]):
                baseline = np.append(baseline, initialSpectra[1][i] - spectra[1][k])
    
    plt.xlim([spectra[0][0], spectra[0][-1]])
    plt.plot(spectra[0], spectra[1])
    plt.plot(initialSpectra[0], initialSpectra[1])
    plt.plot(spectra[0], baseline)
    plt.legend(["corrected", "raw", "baseline"])
    #plt.xlim([40, 3420]) #limitting xaxis range
    plt.gca().invert_xaxis() # inverting xaxis
    plt.savefig(path + fileName + ".png", dpi = 400)
    plt.close()



def plotCrysts(path):
    mlt.rcParams.update({'figure.autolayout': True})
    mlt.use("Cairo")
    fileList = inter.getFilenameList(path)
    ids = inter.createIDs()
    fig, ax = plt.subplots()
    ax.set_ylabel("Value")
    ax.set_xlabel("Probe ID")
    #plt.ylim([0, 2.2])

    for fileName in fileList:
        marker = getBgType(fileName)
        color = getCrystType(fileName)
        file = open(path + fileName, "r")
        data = np.loadtxt(file)
        plt.scatter(ids, data, c = par.colors[color.value], marker = par.markers[marker.value])
        file.close()

    plt.xticks(rotation=45)
    plt.savefig("fileName.png", dpi = 600)
    plt.close()
