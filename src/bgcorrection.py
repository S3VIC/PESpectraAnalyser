import scipy as sc
import numpy as np
import math
import matplotlib.pyplot as plt
import matplotlib as mlt
import src.interface as inter

def correctmcaLS(pathToFile):
    lambdaConst = 1e8
    p = 1e-5
    dataFile = open(pathToFile)
    data = np.loadtxt(dataFile, delimiter = ",", dtype="float")
    #Filling arrays with spectra data
    intensities = np.array([], dtype='float')
    shifts = np.array([], dtype='float')
    origSize = len(data) # spectra size
    
    print("1) 2700 - 3000")
    print("2) 950 - 1500")
    spectraRangeChoice = int(input("Choose spectra range to correct: "))
    match spectraRangeChoice:
        case 1:
            spectraRange = np.array([3000, 2700], dtype='int')
        case 2:
            spectraRange = np.array([1500, 950], dtype='int')
        case other:
            assert False, "Wrong option"

    for i in range(origSize):
        if data[i,0] <= spectraRange[0] and data[i,0]>= spectraRange[1]:
            intensities = np.append(intensities, (data[i, 1]))
            shifts = np.append(shifts, (data[i, 0]))
   #Cropped matrix size to the size of spectra "frame" we are considering for bg correction
    matrixSize = len(intensities)
    diags = np.array([0, 1, 2])
    e = np.ones(matrixSize, dtype='float64')
    values = np.array([e, -2*e, e])
    #differential matrix D
    D = sc.sparse.spdiags(values, diags, matrixSize - 2, matrixSize).toarray()
    Dtr= D.transpose()
    w = np.ones(matrixSize)
    lambdaConst2 = 20
    E = np.eye(matrixSize, dtype='int')
    H = lambdaConst * np.matmul(Dtr, D, dtype='float64')
    S = lambdaConst2 * np.matmul(E.transpose(), E, dtype='float64')
    iterNum = 20
    for k in range(iterNum):
        W = sc.sparse.spdiags(w, 0, matrixSize, matrixSize)
        #cholesky decomposition
        C = sc.linalg.cholesky(W + H + S)
        z = sc.linalg.solve(C, sc.linalg.solve(C.transpose(), np.multiply(w, intensities) + np.matmul(S, intensities, dtype='float64')))
        d = intensities - z;
        dNegative = d[d < 0]
        m = np.mean(dNegative)
        stDev = np.std(dNegative)
        wt = np.ones(matrixSize)
        for i in range(matrixSize):
            if d[i] > 0:
                wt[i] = 1./(1 + math.exp(2*(d[i] - (2 * stDev - m))/stDev))
            else:
                wt[i] = 1
                continue
        #if (np.linalg.norm(w - wt) / np.linalg.norm(w)) < p:
        #    break
        w = wt

    mlt.use("SVG")
    plt.plot(shifts, intensities - z)
    plt.plot(shifts, z)
    plt.plot(shifts, intensities)
    plt.savefig("testMcaLS.svg")
    plt.close()


def correctAsLS(pathToFile):
    lambdaConst = 1e7
    #assymetric coefficient
    p = 0.05
    dataFile = open(pathToFile)
    data = np.loadtxt(dataFile, delimiter = ",", dtype="float")
    #Filling arrays with spectra data
    x = np.array([], dtype='float')
    shifts = np.array([], dtype='float')
    origSize = len(data) # spectra size
    print("1) 2700 - 3000")
    print("2) 950 - 1500")
    spectraRangeChoice = int(input("Choose spectra range to correct: "))
    match spectraRangeChoice:
        case 1:
            spectraRange = np.array([3000, 2700], dtype='int')
        case 2:
            spectraRange = np.array([1500, 950], dtype='int')
        case other:
            assert False, "Wrong option"

    for i in range(origSize):
        if data[i,0] <= spectraRange[0] and data[i,0]>= spectraRange[1]:
            intensities = np.append(intensities, (data[i, 1]))
            shifts = np.append(shifts, (data[i, 0]))
 
    m = len(x)
    e = np.ones(m, dtype='float64')
    values = np.array([e, -2*e, e])
    diags = np.array([0, 1, 2])
    #differential matrix D
    D = sc.sparse.spdiags(values, diags, m- 2, m).toarray()
    w = np.ones(m)
    iterNum = 50
    for i in range(iterNum):
        W = sc.sparse.spdiags(w, 0, m, m)
        C = sc.linalg.cholesky(W + lambdaConst * np.matmul(D.transpose(), D))
        z = sc.linalg.solve(C, sc.linalg.solve(C.transpose(), np.multiply(w,x)))
        for i in range(m):
            if x[i] > z[i]:
                w[i] = p
            else:
                w[i] = 1 - p
    mlt.use("SVG")
    plt.plot(shifts, x - z)
    plt.plot(shifts, z)
    plt.plot(shifts, x)
    plt.savefig("testAsLS.svg")
    plt.close()


def arLS(pathToInputFiles, pathToOutputFiles):
    fileNamesList = inter.getFilenameList(pathToInputFiles)
    print("1) 2700 - 3000")
    print("2) 950 - 1500")
    spectraRangeChoice = int(input("Choose spectra range to correct: "))
    match spectraRangeChoice:
        case 1:
            spectraRange = np.array([3000, 2700], dtype='int')
        case 2:
            spectraRange = np.array([1500, 950], dtype='int')
        case other:
            assert False, "Wrong option"
    for file in fileNamesList:
        lambdaConst = 1e8
        #termination precission
        p = 0.28
        dataFile = open(pathToInputFiles + file)
        data = np.loadtxt(dataFile, delimiter = ",", dtype="float")
        #Filling arrays with spectra data
        x = np.array([], dtype='float')
        shifts = np.array([], dtype='float')
        origSize = len(data) # spectra size
        for i in range(origSize):
            if data[i,0] <= spectraRange[0] and data[i,0]>= spectraRange[1]:
                x = np.append(x, (data[i, 1]))
                shifts = np.append(shifts, (data[i, 0]))
        N = len(x)
        e = np.ones(N, dtype='float64')
        values = np.array([e, -2*e, e])
        diags = np.array([0, 1, 2])
        #differential matrix D
        D = sc.sparse.spdiags(values, diags, N - 2, N).toarray()
        w = np.ones(N)
        H = lambdaConst * np.matmul(D.transpose(), D)

        for i in range(4):
            W = sc.sparse.spdiags(w, 0, N, N)
            C = sc.linalg.cholesky(W + H)
            z = sc.linalg.solve(C, sc.linalg.solve(C.transpose(), np.multiply(w, x)))
            d = x - z

            dn = d[d < 0]
            m = np.mean(dn)
            stDev = np.std(dn)
            wt = np.zeros(N, dtype='float64')
            for i in range(N):
                #wt[i] = 1. / (1 + math.exp(2 * (d[i] - (2*s-m))/s))
                wt[i] = 1./(1 + math.exp(2*(d[i] - (2 * stDev - m))/stDev))
            finishParam = (np.linalg.norm(w - wt) / np.linalg.norm(w))
            w = wt
        outputFile = open(pathToOutputFiles + "corr_" + file, "w")
        for i in range(N):
            outputFile.write(str(shifts[i]) + "," + str(x[i]) + "\n")
        outputFile.close()
        print("File : " + file + " DONE")
        #mlt.use("SVG")
        #plt.plot(shifts, x - z)
        #plt.plot(shifts, z)
        #plt.plot(shifts, x)
        #plt.savefig(pathToOutputFiles + file[:-3] + ".svg")
        #plt.close()
        
