import scipy as sc
import numpy as np
import math
import decimal
import matplotlib.pyplot as plt
import matplotlib as mlt
import src.interface as inter
import src.visualiser as vis

# airPLS  - A
# arPLS - B
# alss - C
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
    print("1) 2500 - 3150")
    print("2) 900 - 1550")
    
    spectraRangeChoice = int(input("Choose spectra range to correct: "))
    match spectraRangeChoice:
        case 1:
            spectraLimits = np.array([2500, 3150], dtype='int')
        case 2:
            spectraLimits = np.array([900, 1650], dtype='int')
        case other:
            assert False, "Wrong option"

    return spectraLimits



def asLS(spectra, lam, asymWeight):
    spectraSize = len(spectra)
    #creating 2nd degree differential matrix D
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
    
    #creating 2nd degree differential matrix D
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
            wt[i] = 1. / (1 + math.exp(2 * ( d[i] - (2 * dstdDev - dNegMean))/ dstdDev))
        
        if (np.linalg.norm(w - wt) / np.linalg.norm(w)) < termPrecision:
            break
    
        w = wt
    
    newSignal = spectra - estBaseline
    return newSignal


#def correctmcaLS(pathToFile):
#    lambdaConst = 1e8
#    p = 1e-5
#    dataFile = open(pathToFile)
#    data = np.loadtxt(dataFile, delimiter = ",", dtype="float")
#    #Filling arrays with spectra data
#    intensities = np.array([], dtype='float')
#    shifts = np.array([], dtype='float')
#    origSize = len(data) # spectra size
#    
#    print("1) 2700 - 3000")
#    print("2) 950 - 1500")
#    spectraRangeChoice = int(input("Choose spectra range to correct: "))
#    match spectraRangeChoice:
#        case 1:
#            spectraRange = np.array([3000, 2700], dtype='int')
#        case 2:
#            spectraRange = np.array([1500, 950], dtype='int')
#        case other:
#            assert False, "Wrong option"
#
#    for i in range(origSize):
#        if data[i,0] <= spectraRange[0] and data[i,0]>= spectraRange[1]:
#            intensities = np.append(intensities, (data[i, 1]))
#            shifts = np.append(shifts, (data[i, 0]))
#   #Cropped matrix size to the size of spectra "frame" we are considering for bg correction
#    matrixSize = len(intensities)
#    diags = np.array([0, 1, 2])
#    e = np.ones(matrixSize, dtype='float64')
#    values = np.array([e, -2*e, e])
#    #differential matrix D
#    D = sc.sparse.spdiags(values, diags, matrixSize - 2, matrixSize).toarray()
#    Dtr= D.transpose()
#    w = np.ones(matrixSize)
#    lambdaConst2 = 20
#    E = np.eye(matrixSize, dtype='int')
#    H = lambdaConst * np.matmul(Dtr, D, dtype='float64')
#    S = lambdaConst2 * np.matmul(E.transpose(), E, dtype='float64')
#    iterNum = 20
#    for k in range(iterNum):
#        W = sc.sparse.spdiags(w, 0, matrixSize, matrixSize)
#        #cholesky decomposition
#        C = sc.linalg.cholesky(W + H + S)
#        z = sc.linalg.solve(C, sc.linalg.solve(C.transpose(), np.multiply(w, intensities) + np.matmul(S, intensities, dtype='float64')))
#        d = intensities - z;
#        dNegative = d[d < 0]
#        m = np.mean(dNegative)
#        stDev = np.std(dNegative)
#        wt = np.ones(matrixSize)
#        for i in range(matrixSize):
#            if d[i] > 0:
#                wt[i] = 1./(1 + math.exp(2*(d[i] - (2 * stDev - m))/stDev))
#            else:
#                wt[i] = 1
#                continue
#        #if (np.linalg.norm(w - wt) / np.linalg.norm(w)) < p:
#        #    break
#        w = wt
#
#    mlt.use("SVG")
#    plt.plot(shifts, intensities - z)
#    plt.plot(shifts, z)
#    plt.plot(shifts, intensities)
#    plt.savefig("testMcaLS.svg")
#    plt.close()

def saveSpectraToCSV(spectra, path, fileName):
    file = open(path + fileName, "w")

    for i in range(len(spectra[0])):
        file.write(str(spectra[0, i]) + "," + str(spectra[1, i]) + "\n")

    file.close()

def plotSpectra(spectra, path, fileName):
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


def logStatus(maxNum, counter, fileName):
    print(fileName + " " + str(maxNum) + " out of " + str(counter) + " [DONE]") 

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
                newSignal = asLS(croppedSpectra[1], 5e7, 0.05)
                fileNamePrefix = "asLS_"
            case 2:
                newSignal = arLS(croppedSpectra[1], 1e7, 0.05)
                fileNamePrefix = "arLS_"
            case other:
                assert False, "Wrong option"
    
        newSpectra = np.array([croppedSpectra[0], newSignal], dtype = 'float')
        saveSpectraToCSV(newSpectra, outputPath, fileNamePrefix + file)
        plotSpectra(newSpectra, outputPath, fileNamePrefix + file[:-4])
        logStatus(filesNum, counter, file)
        counter = counter + 1







