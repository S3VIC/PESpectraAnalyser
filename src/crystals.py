import numpy as np
import scipy as sc
import matplotlib.pyplot as plt
import matplotlib as mlt
from enum import Enum
from scipy.optimize import curve_fit

#custom imports
import params.lorentzModelParams as lor
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
def setModelParams(model, cryst):
    match(model):
        case 'g':
            match cryst:
                case 1:
                    return fan.cryst1GaussModel, fan.GaussModel, mpar.c1_pInit, mpar.c1_bounds
                case 2:
                    return fan.cryst2GaussModel, fan.GaussModel, mpar.c2_pInit, mpar.c2_bounds
                case 3:
                    return fan.cryst2GaussModel, fan.GaussModel, mpar.c2_pInit, mpar.c2_bounds, fan.cryst3GaussModel, mpar.c3_pInit, mpar.c3_bounds
                case 4:
                    return fan.cryst2GaussModel, fan.GaussModel, mpar.c2_pInit, mpar.c2_bounds, fan.cryst3GaussModel, mpar.c4_pInit, mpar.c4_bounds

        case 'l':
            match cryst:
                case 1:
                    return fan.cryst1LorentzModel, fan.LorentzModel, lor.c1_pInit, lor.c1_bounds
                case 2:
                    return fan.cryst2LorentzModel, fan.LorentzModel, lor.c2_pInit, lor.c2_bounds
                case 3:
                    return fan.cryst2LorentzModel, fan.LorentzModel, lor.c2_pInit, lor.c2_bounds, fan.cryst3LorentzModel, lor.c3_pInit, lor.c3_bounds
                case 4:
                    return fan.cryst2LorentzModel, fan.LorentzModel, lor.c2_pInit, lor.c2_bounds, fan.cryst3LorentzModel, lor.c4_pInit, lor.c4_bounds


def setInitialParams(paramFileName, paramNum):
    if(paramNum > 2):
        path = np.array([], dtype = 'str')
        fileList = np.array([], dtype = 'str')
        for index in range(2):
            p = input("Path {0} for CSV files: ".format(index + 1))
            path = np.append(path, p)
            fileList = np.append(fileList, inter.getFilenameList(p), axis = 0)
        fileList = np.reshape(fileList, (2, int(len(fileList)/2)))
        #print(fileList)
    
    else:
        path = input("Path for CSV files: ")
        fileList = inter.getFilenameList(path)
    
    outputPath = input("Path for output files: ")
    paramFile = open(outputPath + paramFileName, 'a')
    
    return path, outputPath, fileList, paramFile


def deconv1(model):
    path, outputPath, fileList, crystFile = setInitialParams("cryst1.csv", 1)
    func, modelFunc, inits, boundaries = setModelParams(model, 1)
    for file in fileList:
        x, y = getSpectraDataFromFile(path + file, ',')
        X, Y = limitSpectra([2800, 2990], x, y)
        popt, _ = curve_fit(func, X, Y, p0 = inits, bounds = boundaries)
        Y_model = func(X, popt[0], popt[1], popt[2], popt[3], popt[4], popt[5], popt[6], popt[7], popt[8], popt[9], popt[10], popt[11])
        vis.plotDeconvFit(X, Y, Y_model, outputPath, file, save = False)
        Y_model1 = modelFunc(X, popt[0], popt[1], popt[2])
        Y_model2 = modelFunc(X, popt[3], popt[4], popt[5])
        integralInten1 = fan.rectIntegRight(X, Y_model1)
        integralInten2 = fan.rectIntegRight(X, Y_model2)
        crystal = integralInten2 / integralInten1 
        print(file)
        crystFile.write(str(crystal) + '\n')
    crystFile.close()


def deconv2(model):
    path, outputPath, fileList, crystFile = setInitialParams("cryst2.csv")
    func, modelFunc, inits, boundaries = setModelParams(model, 2)
    for file in fileList:
        x, y = getSpectraDataFromFile(path + file, ',')
        X, Y = limitSpectra([1400, 1500], x, y)
        popt, _ = curve_fit(func, X, Y, p0 = inits, bounds = boundaries)
        Y_Model = func(X, popt[0], popt[1], popt[2], popt[3], popt[4], popt[5], popt[6], popt[7], popt[8], popt[9], popt[10], popt[11])
        vis.plotDeconvFit(X, Y, Y_model, outputPath, file, save = False)
        YModel1 = modelFunc(X, popt[0], popt[1], popt[2])
        YModel2 = modelFunc(X, popt[3], popt[4], popt[5])
        integralInten1 = fan.rectIntegRight(X, YModel1)
        integralInten2 = fan.rectIntegRight(X, YModel2)
        crystal = integralInten1 / integralInten2 
        crystFile.write(str(crystal) + '\n')
        plt.close()
    crystFile.close() 


def deconv3(model):
    path, outputPath, fList, crystFile = setInitialParams("cryst3.csv", 3)
    func1, modelFunc, inits1, boundaries1, func2, inits2, boundaries2 = setModelParams(model, 3)
    for index, file in enumerate(fList[0]):
        x1, y1, = getSpectraDataFromFile(path[0] + fList[0][index], ',')
        x2, y2 = getSpectraDataFromFile(path[1] + fList[1][index], ',')
        X1, Y1 = limitSpectra([1400, 1500], x1, y1)
        X2, Y2 = limitSpectra([1280, 1330], x2, y2)
        popt1, _ = curve_fit(func1, X1, Y1, p0 = inits1, bounds = boundaries1)
        popt2, _ = curve_fit(func2, X2, Y2, p0 = inits2, bounds = boundaries2)
        Y1_Model = func1(X1, popt1[0], popt1[1], popt1[2], popt1[3], popt1[4], popt1[5], popt1[6], popt1[7], popt1[8], popt1[9], popt1[10], popt1[11])
        Y2_Model = func2(X2, popt2[0], popt2[1], popt2[2], popt2[3], popt2[4], popt2[5])
        YModel1 = modelFunc(X1, popt1[0], popt1[1], popt1[2])
        YModel2 = modelFunc(X2, popt2[0], popt2[1], popt2[2])
        vis.plotDeconvFit(X2, Y2, Y2_Model, outputPath, file, save = True)
        integralInten1 = fan.rectIntegRight(X1, YModel1)
        integralInten2 = fan.rectIntegRight(X2, YModel2)
        crystal = integralInten1 / integralInten2
        crystFile.write(str(crystal) + '\n')
    crystFile.close()


def deconv4(model):
    path, outputPath, fList, crystFile = setInitialParams("cryst4.csv", 4)
    func1, modelFunc, inits1, boundaries1, func2, inits2, boundaries2 = setModelParams(model, 4)
    for index, file in enumerate(fList[0]):
        x1, y1 = getSpectraDataFromFile(path[0] + fList[0][index], ',')
        x2, y2 = getSpectraDataFromFile(path[1] + fList[1][index], ',')
        X1, Y1 = limitSpectra([1400, 1500], x1, y1)
        X2, Y2 = limitSpectra([1000, 1100], x2, y2)
        popt1, _ = curve_fit(func1, X1, Y1, p0 = mpar.c2_pInit, bounds = mpar.c2_bounds)
        popt2, _ = curve_fit(func2, X2, Y2, p0 = mpar.c4_pInit, bounds = mpar.c4_bounds)
        Y1_Model = func1(X1, popt1[0], popt1[1], popt1[2], popt1[3], popt1[4], popt1[5], popt1[6], popt1[7], popt1[8], popt1[9], popt1[10], popt1[11])
        Y2_Model = func2(X2, popt2[0], popt2[1], popt2[2], popt2[3], popt2[4], popt2[5])
        YModel1 = modelFunc(X1, popt1[0], popt1[1], popt1[2])
        YModel2 = modelFunc(X2, popt2[0], popt2[1], popt2[2])
        vis.plotDeconvFit(X2, Y2, Y2_Model, outputPath, file, save = True)
        integralInten1 = fan.rectIntegRight(X1, YModel1)
        integralInten2 = fan.rectIntegRight(X2, YModel2)
        crystal = integralInten1 / integralInten2
        crystFile.write(str(crystal) + '\n')
    crystFile.close()
