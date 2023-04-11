import scipy as sc
import numpy as np
import math
import matplotlib.pyplot as plt
import matplotlib as mlt

def correctmcaLS(pathToFile):
    lambdaConst = 1e10
    p = 1e-9
    dataFile = open(pathToFile)
    data = np.loadtxt(dataFile, delimiter = ",", dtype="float")
#Filling arrays with spectra data
    intensities = np.array([], dtype='float')
    shifts = np.array([], dtype='float')
    origSize = len(data) # spectra size
    for i in range(origSize):
        if data[i,0] <= 2950 and data[i,0]>= 2750:
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
    lambdaConst2 = 100
    E = np.eye(matrixSize, dtype='int')
    H = lambdaConst * np.matmul(Dtr, D, dtype='float64')
    S = lambdaConst2 * np.matmul(E.transpose(), E, dtype='float64')
    iterNum = 150
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
                wt = 1./(1 + math.exp(2*(d[i] - (2 * stDev - m))/stDev))
            else:
                continue
        if np.linalg.norm(w - wt) / np.linalg.norm(w) < p:
            break
        w = wt
        
    

    mlt.use("SVG")
    plt.plot(shifts, intensities - z)
    plt.savefig("test.svg")


