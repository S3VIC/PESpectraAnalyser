#python libs imports
import scipy as sc
import numpy as np
import math
import decimal
import matplotlib.pyplot as plt
import matplotlib as mlt

#custom imports
import src.interface as inter
import src.visualiser as vis

# airPLS  - A
# arPLS - B
# alss - C (to samo co aslss)
# SNIP - S


def importData(pathToFile):
    data = np.loadtxt(pathToFile, delimiter=',')
    x = np.array(data[:, 0], dtype='float')
    y = np.array(data[:, 1], dtype='float')
    spectra = np.array([x, y], dtype='float')

    return spectra


def cropSpectra(spectra, spectraLimits):
    croppedX = np.array([], dtype = 'float')
    croppedY = np.array([], dtype = 'float')

    for i in range(len(spectra[0])):
        if spectraLimits[0] <= spectra[0, i] <= spectraLimits[1]:
            croppedX = np.append(croppedX, spectra[0, i])
            croppedY = np.append(croppedY, spectra[1, i])
    croppedSpectra = np.array([croppedX, croppedY], dtype = 'float')
    
    return croppedSpectra


def chooseSpectraLimits():
    print("1) 2800 - 2990 -> CH2 stretch")
    print("2) 1400 - 1500 -> CH2 bend")
    print("3) 1280 - 1330 -> CH2 twist")
    print("4) 1000 - 1100 -> CC stretch")
    
    spectraRangeChoice = int(input("Choose spectra range to correct: "))
    match spectraRangeChoice:
        case 1:
            spectraLimits = np.array([2800, 2990], dtype='int')
        case 2:
            spectraLimits = np.array([1400, 1500], dtype='int')
        case 3:
            spectraLimits = np.array([1290, 1330], dtype = 'int')
        case 4:
            spectraLimits = np.array([1000, 1100], dtype = 'int')
        case other:
            assert False, "Wrong option"

    return spectraLimits



def asLS(spectra, lam, asymWeight):
    spectraSize = len(spectra)
    e = np.ones(spectraSize, dtype='float64')
    values = np.array([e, -2*e, e])
    diags = np.array([0, 1, 2])
    D = sc.sparse.spdiags(values, diags, spectraSize - 2, spectraSize).toarray()
    w = np.ones(spectraSize)
    for i in range(10):
        W = sc.sparse.spdiags(w, 0, spectraSize, spectraSize)
        C = sc.linalg.cholesky(W + lam * np.matmul(D.transpose(), D))
        estBaseline = sc.linalg.solve(C, sc.linalg.solve(C.transpose(), np.multiply(w, spectra)))
        for i in range(spectraSize):
            if spectra[i] > estBaseline[i]:
                w[i] = asymWeight
            else:
                w[i] = 1 - asymWeight

    newSignal = spectra - estBaseline

    return newSignal 



def arLS(spectra, lamb, termPrecision):
    spectraSize = len(spectra)
    e = np.ones(spectraSize, dtype='float64')
    values = np.array([e, -2*e, e])
    diags = np.array([0, 1, 2])
    D = sc.sparse.spdiags(values, diags, spectraSize - 2, spectraSize).toarray()
    H = lamb * np.matmul(D.transpose(), D)
    w = np.ones(spectraSize)

    while(True):
        W = sc.sparse.spdiags(w, 0, spectraSize, spectraSize)
        C = sc.linalg.cholesky(W + H)
        estBaseline = sc.linalg.solve(C, sc.linalg.solve(C.transpose(), np.multiply(w, spectra)))
        d = spectra - estBaseline
        dNegativeElems = d[ d < 0 ]
        dNegMean = np.mean(dNegativeElems)
        dstdDev = np.std(dNegativeElems)
        wt = np.zeros(spectraSize, dtype = 'float64')
        
        for i in range(spectraSize):
            wt[i] = 1. / (1 + np.exp(2 * ( d[i] - (2 * dstdDev - dNegMean))/ dstdDev))
        
        if (np.linalg.norm(w - wt) / np.linalg.norm(w)) < termPrecision:
            break
    
        w = wt
    newSignal = spectra - estBaseline
    return newSignal


def saveSpectraToCSV(spectra, path, fileName):
    file = open(path + fileName, "w")

    for i in range(len(spectra[0])):
        file.write(str(spectra[0, i]) + "," + str(spectra[1, i]) + "\n")

    file.close()




def logStatus(maxNum, counter, fileName):
    print(fileName + " " + str(counter) + " out of " + str(maxNum) + " [DONE]") 



def setParams(algorithmNum):
    inputPath = input("Path to input .CSV files: ")
    outputPath = input("Set output path (default: ./): ")
    
    if outputPath == "":
        outputPath = "./"
    
    fileNamesList = inter.getFilenameList(inputPath)
    spectraLimits = chooseSpectraLimits()
    filesNum = len(fileNamesList)
    counter = 1

    for file in fileNamesList:
        spectra = importData(inputPath + file)
        croppedSpectra = cropSpectra(spectra, spectraLimits)

        match algorithmNum:
            case 1:
                newSignal = asLS(croppedSpectra[1], 1e8, 0.01)
            case 2:
                newSignal = arLS(croppedSpectra[1], 3e8, 0.001)
            case other:
                assert False, "Wrong option"
    
        newSpectra = np.array([croppedSpectra[0], newSignal], dtype = 'float')
        saveSpectraToCSV(newSpectra, outputPath, file)
        vis.plotPartialSpectra(spectra, newSpectra, outputPath,  file[:-4])
        logStatus(filesNum, counter, file)
        counter = counter + 1







