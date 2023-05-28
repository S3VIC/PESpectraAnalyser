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

#########################################################################
def findSpectraPeakShifts(X, peaksIndexes, signals):
    spectraPeakShifts = {}
    foundPeaksShifts = np.array(X[peaksIndexes], dtype = 'float')

    for signal in signals:
        referenceShift = par.SIGNAL_SHIFTS[signal]
        spectraShift = foundPeaksShifts[0]
        for j in range(1 , len(foundPeaksShifts)):
            actualRefDiff = abs(foundPeaksShifts[j] - referenceShift)
            refDiff = abs(spectraShift - referenceShift)
            if( actualRefDiff <= refDiff ):
                spectraShift = foundPeaksShifts[j]
        spectraPeakShifts[signal] = spectraShift

    return spectraPeakShifts


def findSpectraPeakIntensities(X, Y, peaks):
    spectraPeakIntensities = {}
    for peak in peaks:
        for i in range(len(X)):
            if(X[i] == peak):
                spectraPeakIntensities[X[i]] = Y[i] 

    return spectraPeakIntensities


def calcCryst(signal1, signal2, outputFileName):
    cryst1 = signal1 / signal2
    inter.writeCrystToFile(outputFileName + ".csv", cryst1)


def saveRawCrysts(path, promin, signalType, addPath, crystNum, signals):
    fullPath = path + signalType + addPath
    fileNamesList = inter.getFilenameList(fullPath)

    for i in range(len(fileNamesList)):
        data = np.loadtxt(fullPath + fileNamesList[i], delimiter = ',')
        X = np.array(data[:, 0], dtype ='float')
        Y = np.array(data[:, 1], dtype ='float')

        foundPeakIndexes = sc.signal.find_peaks(Y, prominence = promin)[0]
        foundPeaksShifts = np.array(X[foundPeakIndexes], dtype = 'float')
        foundPeaksIntensities = np.array(Y[foundPeakIndexes], dtype = 'float')
    
        signalsShifts = findSpectraPeakShifts(X, foundPeakIndexes, signals)
        signalsSpectraData = findSpectraPeakIntensities(X, Y, list(signalsShifts.values()))

        peaks = np.array([signalsShifts, signalsSpectraData])
        
        signal1 = peaks[1][peaks[0][signals[0]]]
        signal2 = peaks[1][peaks[0][signals[1]]]
        outputFileName = "cryst" + str(crystNum) + "_" + signalType[:-1]

        calcCryst(signal1, signal2, outputFileName)



def integratePeaks(path, promin, peak1Name, peak2Name):
    fileList = inter.getFilenameList(path)
    for fileName in fileList:
        data = np.loadtxt(path + fileName, delimiter = ',')
        x = data[:, 0]
        y = data[:, 1]
        foundPeakIndexes = sc.signal.find_peaks(y, prominence = promin)[0]
        foundPeakShifts = np.array(x[foundPeakIndexes], dtype = 'float')
        foundPeakIntensities = np.array(y[foundPeakIndexes], dtype = 'float')
        refShifts = np.array([par.SIGNAL_SHIFTS[peak1Name], par.SIGNAL_SHIFTS[peak2Name]], dtype = 'float')

        signalsSpectraShifts = findSpectraPeakShifts(x, doundPeakIndexes, signals)
        signalsSpectraIntensities = findSpectraPeakIntensities(x, y, list(signalsSpectraShifts.values()))

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
        x = np.array(data[:, 0], dtype = 'float')
        y = np.array(data[:, 1], dtype = 'float')
        X = np.array([], dtype = 'float')
        Y = np.array([], dtype = 'float')
        for i in range(len(x)):
            if( 2750 <= x[i] <= 3000 ):
                X = np.append(X, x[i])
                Y = np.append(Y, y[i])
                
        peaksIndexes = sc.signal.find_peaks(Y, prominence = promin)
        peaksShifts = np.array(X[peaksIndexes[0]], dtype = 'float')
        peaksIntensities = np.array(Y[peaksIndexes[0]], dtype = 'float')
        
        peakShifts = findSpectraPeakShifts(X, peaksIndexes[0], signals)
        
        modelShifts = np.array([peakShifts[signals[0]], peakShifts[signals[1]]], dtype = 'float')
        boundaries1 = [ 1, modelShifts[0], 1, 1, modelShifts[1], 1, 1, 2898, 1, 1, 2925, 1 ]
        boundaries2 = [ 9e3, modelShifts[0] + 7, 9e3, 9e3, modelShifts[1] + 8, 9e3, 9e3, 2912, 1.5e1, 9e3, 2939, 9e3 ]
        boundaries = (boundaries1, boundaries2)
        pInit = [1, modelShifts[0], 1, 1, modelShifts[1], 5, 1, 2905, 1, 1, 2932, 1]
        #popt, pcov = curve_fit(fan.cryst1GaussModel, X, Y, p0 = [1, modelShifts[0], 1, 1, modelShifts[1], 5, 1, 2905, 1, 1, 2932, 1], bounds = boundaries)
        popt, pcov = curve_fit(fan.cryst1GaussModel, X, Y, p0 = pInit, bounds = boundaries)
        Y_model = fan.cryst1GaussModel(X, popt[0], popt[1], popt[2], popt[3], popt[4], popt[5], popt[6], popt[7], popt[8], popt[9], popt[10], popt[11])

        print(popt)
        #print(modelShifts)
        plt.plot(X, Y)
        plt.plot(X, Y_model)
        Y_Model1 = fan.GaussModel(X, popt[0], popt[1], popt[2])
        Y_Model2 = fan.GaussModel(X, popt[3], popt[4], popt[5])
        Y_Model3 = fan.GaussModel(X, popt[6], popt[7], popt[8])
        Y_Model4 = fan.GaussModel(X, popt[9], popt[10], popt[11])
        #plt.plot(X, Y_Model1)
        #plt.plot(X, Y_Model2)
        #plt.plot(X, Y_Model3)
        #plt.plot(X, Y_Model4)
        plt.legend(["main", "asym", "sym", "2905", "2932"])
        integralInten1 = fan.rectIntegRight(X, Y_Model1)
        integralInten2 = fan.rectIntegRight(X, Y_Model2)
        crystal = integralInten1 / integralInten2 
        print(file)
        print(crystal)
        plt.show()
        plt.close()

  # alSS
  # arPLS
  # airPLS
