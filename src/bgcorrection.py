
def correctmcaLS(pathToFile):
    lambdaConst = 1e9
    dataFile = open(pathToFile)
    data = np.loadtxt(dataFile, delimiter = ",", dtype="float")
    intensities = []
    shifts = []
    origSize = len(data)
    for i in range(origSize):
        if data[i,0] <= 2950 and data[i,0]>= 2750:
            intensities.append(data[i, 1])
            shifts.append(data[i, 0])
    matrixSize = len(intensities)
    D = np.zeros((matrixSize - 2, matrixSize), dtype="float64")
    W = np.eye(matrixSize, dtype="float64")
    for index in range(matrixSize - 2):
        D[index][index] = 1
        D[index][index+1] = -2
        D[index][index+2] = 1
    Dtransposed = D.transpose()
    Deval = lambdaConst * np.matmul(Dtransposed, D, dtype = "float64")
    L = Deval + W
    Lprim = np.matmul(W, intensities, dtype = "float64")
    z = np.linalg.solve(L,Lprim)
    iterNum = 15
    d = intensities - z
    for k in range(iterNum):
        result = intensities - z
        d_ = []
        for j in range(matrixSize - 1):
            if d[j] < 0:
                d_.append(d[j])

        m = np.mean(d_)
#        print(d_)
        standardDev = np.std(d_)
        print(standardDev)
        const = -m + 2 * standardDev

        for z in range(matrixSize- 1):
            if d[z] > 0:
                W[z][z] = Decimal(1/(1 + math.exp( 2 * (d[z] - const) /(standardDev))))
                #W[k][k] = Decimal(1/(1 + ( 2 * d[k] - const /(1+ standardDev))))
            else:
                W[z][z] = 1
        L = Deval + W
        Lprim = np.matmul(W, intensities, dtype = "float64")
        z = np.linalg.solve(L, Lprim)
    mlt.use("SVG")
    plt.plot(shifts, intensities - z)
    plt.savefig("test.svg")


