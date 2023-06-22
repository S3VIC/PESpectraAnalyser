import numpy as np
import scipy as sc
import matplotlib.pyplot as plt
import matplotlib as mlt
from enum import Enum
from scipy.optimize import curve_fit

#custom imports
import params.modelParams as mpar
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


def limitSpectra(limits, x, y):
    X = np.array([], dtype = 'float')
    Y = np.array([], dtype = 'float')
    for i in range(len(x)):
        if( limits[0] <= x[i] <= limits[1]):
            X = np.append(X, x[i])
            Y = np.append(Y, y[i])
    return X, Y            


def getSpectraDataFromFile(filePath, delim):
    data = np.loadtxt(filePath, delimiter = delim)
    x = np.array(data[:, 0], dtype = 'float')
    y = np.array(data[:, 1], dtype = 'float')
    return x, y


def findModelPeakShifts(X, Y, promin, signals):
    peaksIndexes = sc.signal.find_peaks(Y, prominence = promin)[0]
    peaksIntensities = np.array(Y[peaksIndexes[0]], dtype = 'float')
    peakShifts = findSpectraPeakShifts(X, peaksIndexes, signals)
    modelShifts = np.array([], dtype = 'float')
    for signal in signals:
        modelShifts = np.append(modelShifts, peakShifts[signal])

    return modelShifts

#crystr5 = 1416/(const * 1295 + 1303) do implementacji zwłaszcza do metod normalizacyjnych!!

def deconv1(promin):
    path = input("Path for CSV files: ")
    outputPath = input("Path for output files: ")
    fileList = inter.getFilenameList(path)
    crystFile = open("cryst1.csv", 'a')
    for file in fileList:
        x, y = getSpectraDataFromFile(path + file, ',')
        X, Y = limitSpectra([2815, 2960], x, y)
        popt, _ = curve_fit(fan.cryst1GaussModel, X, Y, p0 = mpar.c1_pInit, bounds = mpar.c1_bounds)
        Y_model = fan.cryst1GaussModel(X, popt[0], popt[1], popt[2], popt[3], popt[4], popt[5], popt[6], popt[7], popt[8], popt[9], popt[10], popt[11])
        fig, ax = plt.subplots()
        ax.set(yticklabels = [])
        ax.set_ylabel("Intensywność [j. u.]")
        ax.set_xlabel("Przesunięcie Ramana [cm$^{-1}]$")
        plt.gca().invert_xaxis()
        plt.plot(X, Y)
        plt.plot(X, Y_model)
        plt.legend(["widmo", "dopasowanie"])
        Y_model1 = fan.GaussModel(X, popt[0], popt[1], popt[2])
        Y_model2 = fan.GaussModel(X, popt[3], popt[4], popt[5])
        integralInten1 = fan.rectIntegRight(X, Y_model1)
        integralInten2 = fan.rectIntegRight(X, Y_model2)
        crystal = integralInten2 / integralInten1 
        print(file)
        crystFile.write(str(crystal) + '\n')
        #plt.show()
        plt.savefig(outputPath + file[:-4] + "_image.png", dpi=600)
        plt.close()
    crystFile.close()


def deconv2(promin):
    #path = input("Path for CSV files: ")    
    path = "output/dyneema/asLS/bend/"
    outputPath = input("Path for output files: ")
    fileList = inter.getFilenameList(path)
    crystFile = open(outputPath + "cryst2.csv", 'a')
    for file in fileList:
        x, y = getSpectraDataFromFile(path + file, ',')
        X, Y = limitSpectra([1400, 1500], x, y)
        popt, _ = curve_fit(fan.cryst2GaussModel, X, Y, p0 = mpar.c2_pInit, bounds = mpar.c2_bounds)
        print(popt)
        Y_Model = fan.cryst2GaussModel(X, popt[0], popt[1], popt[2], popt[3], popt[4], popt[5], popt[6], popt[7], popt[8], popt[9], popt[10], popt[11])
        fig, ax = plt.subplots()
        plt.plot(X,Y)
        plt.plot(X, Y_Model)
        plt.gca().invert_xaxis()
        plt.legend(("widmo", "dopasowanie"))
        YModel1 = fan.GaussModel(X, popt[0], popt[1], popt[2])
        YModel2 = fan.GaussModel(X, popt[3], popt[4], popt[5])
        integralInten1 = fan.rectIntegRight(X, YModel1)
        integralInten2 = fan.rectIntegRight(X, YModel2)
        crystal = integralInten1 / integralInten2 
        crystFile.write(str(crystal) + '\n')
        plt.savefig(outputPath + file[:-4] + ".png", dpi = 600)
        plt.close()
    crystFile.close() 


def deconv3(promin):
    #path = input("Path for CSV files: ")    
    path1 = "output/dyneema/asLS/bend/"
    path2 = "output/dyneema/asLS/twist/"
    outputPath = input("Path for output files: ")
    fileList1 = inter.getFilenameList(path1)
    fileList2 = inter.getFilenameList(path2)
    crystFile = open(outputPath + "cryst3.csv", 'a')
    for index, file in enumerate(fileList1):
        x1, y1, = getSpectraDataFromFile(path1 + fileList1[index], ',')
        x2, y2 = getSpectraDataFromFile(path2 + fileList2[index], ',')

        X1, Y1 = limitSpectra([1400, 1500], x1, y1)
        X2, Y2 = limitSpectra([1280, 1330], x2, y2)
        popt1, _ = curve_fit(fan.cryst2GaussModel, X1, Y1, p0 = mpar.c2_pInit, bounds = mpar.c2_bounds)
        popt2, _ = curve_fit(fan.cryst3GaussModel, X2, Y2, p0 = mpar.c3_pInit, bounds = mpar.c3_bounds)
        Y1_Model = fan.cryst2GaussModel(X1, popt1[0], popt1[1], popt1[2], popt1[3], popt1[4], popt1[5], popt1[6], popt1[7], popt1[8], popt1[9], popt1[10], popt1[11])
        Y2_Model = fan.cryst3GaussModel(X2, popt2[0], popt2[1], popt2[2], popt2[3], popt2[4], popt2[5])
        YModel1 = fan.GaussModel(X1, popt1[0], popt1[1], popt1[2])
        YModel2 = fan.GaussModel(X2, popt2[0], popt2[1], popt2[2])
        fig, ax = plt.subplots()
        plt.plot(X2,Y2)
        plt.plot(X2, Y2_Model)
        plt.gca().invert_xaxis()
        plt.legend(("widmo", "dopasowanie"))
        plt.savefig(outputPath + file[:-4] + ".png", dpi = 600)
        integralInten1 = fan.rectIntegRight(X1, YModel1)
        integralInten2 = fan.rectIntegRight(X2, YModel2)
        crystal = integralInten1 / integralInten2
        crystFile.write(str(crystal) + '\n')
    crystFile.close()


def deconv4():
    path1 = "output/dyneema/asLS/bend/"
    path2 = "output/dyneema/asLS/str_CC/"
    outputPath = input("Path for output files: ")
    fileList1 = inter.getFilenameList(path1)
    fileList2 = inter.getFilenameList(path2)
    crystFile = open(outputPath + "cryst4.csv", 'a')
    for index, file in enumerate(fileList1):
        x1, y1, = getSpectraDataFromFile(path1 + fileList1[index], ',')
        x2, y2 = getSpectraDataFromFile(path2 + fileList2[index], ',')

        X1, Y1 = limitSpectra([1400, 1500], x1, y1)
        X2, Y2 = limitSpectra([1000, 1100], x2, y2)
        popt1, _ = curve_fit(fan.cryst2GaussModel, X1, Y1, p0 = mpar.c2_pInit, bounds = mpar.c2_bounds)
        popt2, _ = curve_fit(fan.cryst3GaussModel, X2, Y2, p0 = mpar.c4_pInit, bounds = mpar.c4_bounds)
        Y1_Model = fan.cryst2GaussModel(X1, popt1[0], popt1[1], popt1[2], popt1[3], popt1[4], popt1[5], popt1[6], popt1[7], popt1[8], popt1[9], popt1[10], popt1[11])
        Y2_Model = fan.cryst3GaussModel(X2, popt2[0], popt2[1], popt2[2], popt2[3], popt2[4], popt2[5])
        YModel1 = fan.GaussModel(X1, popt1[0], popt1[1], popt1[2])
        YModel2 = fan.GaussModel(X2, popt2[0], popt2[1], popt2[2])
        fig, ax = plt.subplots()
        plt.plot(X2,Y2)
        plt.plot(X2, Y2_Model)
        plt.gca().invert_xaxis()
        plt.legend(("widmo", "dopasowanie"))
        plt.savefig(outputPath + file[:-4] + ".png", dpi = 600)
        integralInten1 = fan.rectIntegRight(X1, YModel1)
        integralInten2 = fan.rectIntegRight(X2, YModel2)
        crystal = integralInten1 / integralInten2
        crystFile.write(str(crystal) + '\n')
    crystFile.close()

def setUpDeconv():
    choice = inter.deconvChoice()
    match choice:
        case 1:
            print("Hello")
        case 2:
            print("Hello")
        case 3:
            print("Hello")
        case 4:
            print("Hello")
        case 5:
            print("Hello")
        case 6:
            print("Hello")

