import numpy as np
import scipy as sc
import matplotlib.pyplot as plt
import matplotlib as mlt
from enum import Enum
from scipy.optimize import curve_fit

#custom imports
import params.parameters as par
import src.interface as inter
import src.funcAnalysis as fan
import src.visualiser as vis


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

#########################################################################

def calculateSimpleCryst(signal1, signal2, outputFileName):
    cryst1 = signal1 / signal2
    inter.writeCrystToFile(outputFileName + ".csv", cryst1)


def findRealPeakShifts(X, peaksIndexes, signals):
    realPeakShifts = {}
    foundPeaksShifts = np.array(X[peaksIndexes], dtype = 'float')

    for signal in signals:
        referenceShift = par.SIGNAL_SHIFTS[signal]
        spectraShift = foundPeaksShifts[0]
        for j in range(1 , len(foundPeaksShifts)):
            actualRefDiff = abs(foundPeaksShifts[j] - referenceShift)
            refDiff = abs(spectraShift - referenceShift)
            if( actualRefDiff <= refDiff ):
                spectraShift = foundPeaksShifts[j]
        realPeakShifts[signal] = spectraShift

    return realPeakShifts


def findRealPeakIntensities(X, Y, peaks):
    realPeakIntensities = {}
    for peak in peaks:
        for i in range(len(X)):
            if(X[i] == peak):
                realPeakIntensities[X[i]] = Y[i] 

    return realPeakIntensities


#Calculates crystals based on given signals (cryst type) and type of bg correction that was applied on spectra
def calculateCrysts(path, promin, signalType, addPath, crystNum, signals):
    fullPath = path + signalType + addPath
    fileNamesList = inter.getFilenameList(fullPath)

    for i in range(len(fileNamesList)):
        data = np.loadtxt(fullPath + fileNamesList[i], delimiter = ',')
        Y = np.array(data[:, 1], dtype ='float')
        X = np.array(data[:, 0], dtype ='float')

        foundPeakIndexes = sc.signal.find_peaks(Y, prominence = promin)[0]
        foundPeaksShifts = np.array(X[foundPeakIndexes], dtype = 'float')
#        print(foundPeaksShifts)
        foundPeaksIntensities = np.array(Y[foundPeakIndexes], dtype = 'float')
        signalsShifts = {}
        signalsSpectraData = {}
        
    
        signalsShifts = findRealPeakShifts(X, foundPeakIndexes, signals)
        signalsSpectraData = findRealPeakIntensities(X, Y, list(signalsShifts.values()))

        #print(signalsShifts)
        peaks = np.array([signalsShifts, signalsSpectraData])
        calculateSimpleCryst(peaks[1][peaks[0][signals[0]]], peaks[1][peaks[0][signals[1]]], "cryst" + str(crystNum) + "_" + signalType[:-1])



def integratePeaks(path, promin, peak1Name, peak2Name):

    fileList = inter.getFilenameList(path)
    for fileName in fileList:
        file = open(path + fileName, 'r')

        data = np.loadtxt(file, delimiter = ',')
        x = data[:, 0]
        y = data[:, 1]
        file.close()
        peakIndex = sc.signal.find_peaks(y, prominence = promin)
        peakShifts = np.array(x[peakIndex[0]], dtype = 'float')
        peakInten = np.array(y[peakIndex[0]], dtype = 'float')
        referenceShift1 = par.SIGNAL_SHIFTS[peak1Name]
        referenceShift2 = par.SIGNAL_SHIFTS[peak2Name]

        shift1 = peakShifts[0]
        shift2 = peakShifts[0]
        inten1 = peakInten[0]
        inten2 = peakInten[0]

        for i in range(1, len(peakShifts)):
            diff_raw1 = abs(peakShifts[i] - referenceShift1)
            refDiff1 = abs(shift1 - referenceShift1)
            if(diff_raw1 <= refDiff1):
                shift1 = peakShifts[i]
                inten1 = peakInten[i]

            diff_raw2 = abs(peakShifts[i] - referenceShift2)
            refDiff2 = abs(shift2 - referenceShift2)
            if(diff_raw2 <= refDiff2):
                shift2 = peakShifts[i]
                inten2 = peakInten[i]

        indexOfPeak1 = np.where( x == shift1 ) 
        indexOfPeak2 = np.where( x == shift2 )
        index1 = int(indexOfPeak1[0]) 
        index2 = int(indexOfPeak2[0])
        offset = 30

        area1 = fan.rectIntegLeft(x[index1 - offset : index1 + offset], y[index1 - offset : index1 + offset])
        area2 = fan.rectIntegLeft(x[index2 - offset : index2 + offset], y[index2 - offset : index2 + offset])
        
        cryst = area1 / area2
        inter.writeCrystToFile("cryst4_raw_intRectLeft.CSV", cryst)

        area3 = fan.rectIntegRight(x[index1 - offset : index1 + offset], y[index1 - offset : index1 + offset])
        area4 = fan.rectIntegRight(x[index2 - offset : index2 + offset], y[index2 - offset : index2 + offset])
        cryst = area3 / area4
        inter.writeCrystToFile("cryst4_raw_intRectRight.CSV", cryst)

        area5 = fan.trapInteg(x[index1 - offset : index1 + offset], y[index1 - offset : index1 + offset])
        area6 = fan.trapInteg(x[index2 - offset : index2 + offset], y[index2 - offset : index2 + offset])
        cryst = area5 / area6
        inter.writeCrystToFile("cryst4_raw_intTrap.CSV", cryst)
        print(fileName + " finished")




#crystr5 = 1416/(const * 1295 + 1303) do implementacji zwłaszcza do metod normalizacyjnych!!


def deconvolutionTest(promin, signals):
    path = input("Path for CSV files: ")
    fileList = inter.getFilenameList(path)
    for file in fileList:
        data = np.loadtxt(path + file, delimiter = ',')
        X = np.array(data[:, 0], dtype = 'float')
        Y = np.array(data[:, 1], dtype = 'float')

        peaksIndexes = sc.signal.find_peaks(Y, prominence = promin)
        peaksShifts = np.array(X[peaksIndexes[0]], dtype = 'float')
        peaksIntensities = np.array(Y[peaksIndexes[0]], dtype = 'float')
        #peakData = {}
        
    
        peakShifts = findRealPeakShifts(X, peaksIndexes[0], signals)
#        peakData[spectraShift] = spectraInten
        
        modelShifts = np.array([peakShifts[signals[0]], peakShifts[signals[1]]], dtype = 'float')
        popt1, pcov1 = curve_fit(fan.strCH2GaussModel, X, Y, p0 = [1, modelShifts[0], 1, 1, modelShifts[1], 1, 1, 2905, 1, 1, 2932, 1])
        Y_model = fan.strCH2GaussModel(X, popt1[0], popt1[1], popt1[2], popt1[3], popt1[4], popt1[5], popt1[6], popt1[7], popt1[8], popt1[9], popt1[10], popt1[11])

        print(popt1)
        print(modelShifts)
        plt.plot(X, Y)
        plt.plot(X, Y_model)
        
        plt.show()
        plt.close()

  # alSS
  # arPLS
  # airPLS
