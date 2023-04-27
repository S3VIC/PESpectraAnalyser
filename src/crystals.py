import numpy as np
import params.parameters as par
import src.interface as inter
import scipy as sc
import matplotlib.pyplot as plt
import matplotlib as mlt


#returns array containing shift and intensity respectively of the signal searched based on the first prediction
# old peak searching method
def checkForMaximum(spectraDict, foundSignalShift):
    maxInt = spectraDict[foundSignalShift]
    spectraShifts = list(spectraDict.keys())
    shiftIndex = spectraShifts.index(foundSignalShift)
    realShift = spectraShifts.index(foundSignalShift)
    for i in range(10):
        if spectraDict[spectraShifts[shiftIndex - i]] > maxInt:
          maxInt = spectraDict[spectraShifts[shiftIndex - i]]
          realShift = spectraShifts[shiftIndex - i]
    
    for i in range(10):
        if spectraDict[spectraShifts[shiftIndex + i]] > maxInt:
          maxInt = spectraDict[spectraShifts[shiftIndex - i]]
          realShift = spectraShifts[shiftIndex - i]
    signalParams = np.array([realShift, maxInt], dtype = 'float')

    return signalParams

#returns signal params array - corrected shift and intensity respectively
def searchForSignalIntensity(spectraDict, signalName):
  
    keys = np.array(list(spectraDict.keys()))
    signalShift = par.SIGNAL_SHIFTS[signalName]
    minDistance = abs(signalShift - keys[0])
    predictedShift = keys[0]

    for i in range(1, len(keys)):
        distance = abs(signalShift - keys[i])
        if distance < minDistance:
            minDistance = distance
            predictedShift = keys[i]
        predictedInten= spectraDict[predictedShift]
        signalParams = checkForMaximum(spectraDict, predictedShift)

    return np.array(signalParams, dtype='float')


def searchForSignal(peaksShifts, peakName):
    foundShifts = np.array([], dtype = 'float')
    signalNames = np.array(par.SIGNAL_SHIFTS.keys())
    
    for signal in signalNames:
        shift = par.SIGNAL_SHIFTS[signal]


    return foundShifts

#########################################################################


def calculateSimpleCryst(signal1, signal2, outputFileName):
    cryst1 = signal1 / signal2
    writeCrystToFile(outputFileName + ".csv", cryst1)

def plotCrysts(path):
    fileList = inter.getFilenameList(path)
    mlt.use("Cairo")
    fig, ax = plt.subplots()
    ax.set_ylabel("Value")
    ax.set_xlabel("Probe ID")
    plt.ylim([-1, 2]) #limitting yaxis range
    ids = np.linspace(1, 16, 16)
    print(ids)
    for i in range(len(fileList)):
        if("cryst1" in fileList[i]):
            if("raw" in fileList[i]):
                file = open(path + fileList[i], "r")
                data = np.loadtxt(file)
                plt.scatter(ids, data, c = 'red', marker = 'X')
            if("asLS" in fileList[i]):
                file = open(path + fileList[i], "r")
                data = np.loadtxt(file)
                plt.scatter(ids, data, c = 'red', marker = 's')
            if("arLS" in fileList[i]):
                file = open(path + fileList[i], "r")
                data = np.loadtxt(file)
                print("data: " + str(len(ids)))
                plt.scatter(ids, data, c = 'red', marker = 'v')

        if("cryst2" in fileList[i]):
            if("raw" in fileList[i]):
                file = open(path + fileList[i], "r")
                data = np.loadtxt(file)
                plt.scatter(ids, data, c = 'yellow', marker = 'X')
            if("asLS" in fileList[i]):
                file = open(path + fileList[i], "r")
                data = np.loadtxt(file)
                plt.scatter(ids, data, c = 'yellow', marker = 's')
            if("arLS" in fileList[i]):
                file = open(path + fileList[i], "r")
                data = np.loadtxt(file)
                plt.scatter(ids, data, c = 'yellow', marker = 'v')
        if("cryst3" in fileList[i]):
            if("raw" in fileList[i]):
                file = open(path + fileList[i], "r")
                data = np.loadtxt(file)
                plt.scatter(ids, data, c = 'blue', marker = 'X')
            if("asLS" in fileList[i]):
                file = open(path + fileList[i], "r")
                data = np.loadtxt(file)
                plt.scatter(ids, data, c = 'blue', marker = 's')
            if("arLS" in fileList[i]):
                file = open(path + fileList[i], "r")
                data = np.loadtxt(file)
                plt.scatter(ids, data, c = 'blue', marker = 'v')
        if("cryst4" in fileList[i]):
            if("raw" in fileList[i]):
                file = open(path + fileList[i], "r")
                data = np.loadtxt(file)
                plt.scatter(ids, data, c = 'green', marker = 'X')
            if("asLS" in fileList[i]):
                file = open(path + fileList[i], "r")
                data = np.loadtxt(file)
                plt.scatter(ids, data, c = 'green', marker = 's')
            if("arLS" in fileList[i]):
                file = open(path + fileList[i], "r")
                data = np.loadtxt(file)
                plt.scatter(ids, data, c = 'green', marker = 'v')
    plt.savefig("fig2.png", dpi = 400)
    plt.close()

# returns dict of pairs SIGNAL_NAME : SIGNAL_SHIFT 
def getPeaks(path, promin):
    cryst1_raw = np.array([], dtype = 'float')
    cryst2_raw = np.array([], dtype = 'float')
    cryst3_raw = np.array([], dtype = 'float')
    cryst4_raw = np.array([], dtype = 'float')


    cryst1_asLS = np.array([], dtype = 'float')
    cryst2_asLS= np.array([], dtype = 'float')
    cryst3_asLS = np.array([], dtype = 'float')
    cryst4_asLS = np.array([], dtype = 'float')


    cryst1_arLS = np.array([], dtype = 'float')
    cryst2_arLS = np.array([], dtype = 'float')
    cryst3_arLS = np.array([], dtype = 'float')
    cryst4_arLS = np.array([], dtype = 'float')
    
    pathRaw = path + "raw/"
    pathasLS = path + "asLS/"
    patharLS = path + "arLS/"

    #cryst_path = "ben-twist-str/"
    cryst_path = "str_CH2/"
    raw_List = inter.getFilenameList(pathRaw)
    asLS_List = inter.getFilenameList(pathasLS + cryst_path)
    arLS_List = inter.getFilenameList(patharLS + cryst_path)

    for i in range(len(raw_List)):
        data_raw = np.loadtxt(pathRaw + raw_List[i], delimiter=',')
        data_asLS = np.loadtxt(pathasLS + cryst_path +  asLS_List[i], delimiter=',')
        data_arLS = np.loadtxt(patharLS + cryst_path +  arLS_List[i], delimiter=',')

        intensities_raw = np.array(data_raw[:, 1], dtype ='float')
        ramanshifts_raw = np.array(data_raw[:, 0], dtype ='float')
         
        intensities_asLS = np.array(data_asLS[:, 1], dtype ='float')
        ramanshifts_asLS= np.array(data_asLS[:, 0], dtype ='float')
        intensities_arLS = np.array(data_arLS[:, 1], dtype ='float')
        ramanshifts_arLS = np.array(data_arLS[:, 0], dtype ='float')

        peaksIndexes_raw = sc.signal.find_peaks(intensities_raw, prominence = promin)
        peaksShifts_raw = np.array(ramanshifts_raw[peaksIndexes_raw[0]], dtype = 'float')
        peaksIntensities_raw = np.array(intensities_raw[peaksIndexes_raw[0]], dtype = 'float')
        
        peaksIndexes_asLS = sc.signal.find_peaks(intensities_asLS, prominence = promin)
        peaksShifts_asLS = np.array(ramanshifts_asLS[peaksIndexes_asLS[0]], dtype = 'float')
        peaksIntensities_asLS = np.array(intensities_asLS[peaksIndexes_asLS[0]], dtype = 'float')
        
        #print(peaksShifts_raw)   
        peaksIndexes_arLS = sc.signal.find_peaks(intensities_arLS, prominence = promin)
        peaksShifts_arLS = np.array(ramanshifts_arLS[peaksIndexes_arLS[0]], dtype = 'float')
        peaksIntensities_arLS = np.array(intensities_arLS[peaksIndexes_arLS[0]], dtype = 'float')
       
        signalNames = np.array(list(par.SIGNAL_SHIFTS.keys()))
        
        peak_shifts_raw = {}
        peak_data_raw = {}

        peak_shifts_asLS = {}
        peak_data_asLS = {}
        
        peak_shifts_arLS = {}
        peak_data_arLS = {}

        for signal in signalNames:
            referenceShift = par.SIGNAL_SHIFTS[signal]
            spectraShift_raw = peaksShifts_raw[0]
            spectraInten_raw = peaksIntensities_raw[0]
            spectraShift_asLS = peaksShifts_asLS[0]
            spectraInten_asLS = peaksIntensities_asLS[0]
            spectraShift_arLS = peaksShifts_arLS[0]
            spectraInten_arLS = peaksIntensities_arLS[0]

            for i in range(1, len(peaksShifts_raw)):
                diff_raw = abs(peaksShifts_raw[i] - referenceShift)
                refDiff_raw = abs(spectraShift_raw - referenceShift)
                if(diff_raw <= refDiff_raw):
                    spectraShift_raw = peaksShifts_raw[i]
                    spectraInten_raw = peaksIntensities_raw[i]
            
            for i in range(1, len(peaksShifts_asLS)): 
                diff_asLS = abs(peaksShifts_asLS[i] - referenceShift)
                refDiff_asLS = abs(spectraShift_asLS - referenceShift)
                if(diff_asLS <= refDiff_asLS):
                    spectraShift_asLS = peaksShifts_asLS[i]
                    spectraInten_asLS = peaksIntensities_asLS[i]
            for i in range(1, len(peaksShifts_arLS)):
                diff_arLS = abs(peaksShifts_arLS[i] - referenceShift)
                refDiff_arLS = abs(spectraShift_arLS - referenceShift)
                if(diff_arLS <= refDiff_arLS):
                    spectraShift_arLS = peaksShifts_arLS[i]
                    spectraInten_arLS = peaksIntensities_arLS[i]
                    
            peak_shifts_raw[signal] = spectraShift_raw
            peak_data_raw[spectraShift_raw] = spectraInten_raw
            
            peak_shifts_asLS[signal] = spectraShift_asLS
            peak_data_asLS[spectraShift_asLS] = spectraInten_asLS
           
            peak_shifts_arLS[signal] = spectraShift_arLS
            peak_data_arLS[spectraShift_arLS] = spectraInten_arLS

        peaks_raw = np.array([peak_shifts_raw, peak_data_raw])
        peaks_asLS = np.array([peak_shifts_asLS, peak_data_asLS])
        peaks_arLS = np.array([peak_shifts_arLS, peak_data_arLS])
        #calculate crysts and save them to file
        #c1
        calculateSimpleCryst(peaks_raw[1][peaks_raw[0]['CH2_str_sym']], peaks_raw[1][peaks_raw[0]['CH3_str_asym']], "cryst1_raw")
        calculateSimpleCryst(peaks_asLS[1][peaks_asLS[0]['CH2_str_sym']], peaks_asLS[1][peaks_asLS[0]['CH3_str_asym']], "cryst1_asLS")
        calculateSimpleCryst(peaks_arLS[1][peaks_arLS[0]['CH2_str_sym']], peaks_arLS[1][peaks_arLS[0]['CH3_str_asym']], "cryst1_arLS")
       # ##c2
       # calculateSimpleCryst(peaks_raw[1][peaks_raw[0]['CH2_ben_cryst']], peaks_raw[1][peaks_raw[0]['CH2_ben_amorf']], "cryst2_raw")
       # calculateSimpleCryst(peaks_asLS[1][peaks_asLS[0]['CH2_ben_cryst']], peaks_asLS[1][peaks_asLS[0]['CH2_ben_amorf']], "cryst2_asLS")
       # calculateSimpleCryst(peaks_arLS[1][peaks_arLS[0]['CH2_ben_cryst']], peaks_arLS[1][peaks_arLS[0]['CH2_ben_amorf']], "cryst2_arLS")
       ####c3
       # calculateSimpleCryst(peaks_raw[1][peaks_raw[0]['CH2_ben_cryst']], peaks_raw[1][peaks_raw[0]['CH2_twist_amorf']], "cryst3_raw")
       # calculateSimpleCryst(peaks_asLS[1][peaks_asLS[0]['CH2_ben_cryst']], peaks_asLS[1][peaks_asLS[0]['CH2_twist_amorf']], "cryst3_asLS")
       # calculateSimpleCryst(peaks_arLS[1][peaks_arLS[0]['CH2_ben_cryst']], peaks_arLS[1][peaks_arLS[0]['CH2_twist_amorf']], "cryst3_arLS")
       # ###c4
       # calculateSimpleCryst(peaks_raw[1][peaks_raw[0]['CH2_ben_cryst']], peaks_raw[1][peaks_raw[0]['CC_str_amorf']], "cryst4_raw")
       # calculateSimpleCryst(peaks_asLS[1][peaks_asLS[0]['CH2_ben_cryst']], peaks_asLS[1][peaks_asLS[0]['CC_str_amorf']], "cryst4_asLS")
       # calculateSimpleCryst(peaks_arLS[1][peaks_arLS[0]['CH2_ben_cryst']], peaks_arLS[1][peaks_arLS[0]['CC_str_amorf']], "cryst4_arLS")


#saves data to file from an array
def writeCrystToFile(filename, crystValue):
    file = open(filename, "a")
    file.write(str(crystValue) + "\n")
    file.close()




#reads data from file and returns it in form of dictionary {RAMAN SHIFT : INTENSITY} 
def getDataFromFile(filePath):
    dataFile = np.loadtxt(filePath, delimiter=',')
    xCoordinates = np.array(dataFile[:, 0], dtype='float')
    yCoordinates = np.array(dataFile[:, 1], dtype='float')
    spectraData = {}

    for i in range(xCoordinates.size):
        spectraData[xCoordinates[i]] = yCoordinates[i]

    return spectraData


#series of functions calculating particular cryst param


#
#def calculateSingleCryst(path, fileNamesList, choice):
#    fileName = input("File Name for cryst{0}: ".format(choice))
#    for file in fileNamesList:
#        peaks = getPeaks(path + file, 140)
#        #print("File : " + file + " PROCESSING")
#        match choice:
#            case 1:
#            case 2:
#            case 3:
#            case 4:
#            case other:
#                assert False, "Wrong option"
#        calculateSimpleCryst(signal1, signal2, fileName)
#        print("File : " + file + " DONE")


def calculateAllCryst(path, fileNamesList):
    outputFileNames = np.array([], dtype='string')
    for i in range(4):
        fileName = input("File name for cryst{0}: ".format(i + 1))
        outputFileNames = np.append(outputFileNames, fileName)
    for file in fileNamesList:
        calculateCryst1(path + file, outputFileNames[0])
        calculateCryst2(path + file, outputFileNames[1])
        calculateCryst3(path + file, outputFileNames[2])
        calculateCryst4(path + file, outputFileNames[3])
        print("File : " + file + " DONE")


def calculateCrysts(path):    
    fileNamesList = inter.getFilenameList(path)
    inter.displayCrystParamsInfo()
    choice = int(input("Which cryst params to calculate: "))
    match choice:
        case 1 | 2 | 3 | 4:
            calculateSingleCryst(path, fileNamesList, choice)
        case 5:
            calculateAllCryst(path, fileNamesList)
        case other:
            assert False, "Wrong option" 



def getIntensityList(spectraData):
    intensityList = np.array([], dtype='float')
    choice = int(input("Which cryst params to calculate: ")) 
    match choice:
        case 1:
            intensityList = np.append(intensityList, searchForSignalIntensity(spectraData, 'CH2_str_sym'))
            intensityList = np.append(intensityList, searchForSignalIntensity(spectraData, 'CH3_str_asym'))
        case 2:
            intensityList = np.append(intensityList, searchForSignalIntensity(spectraData, 'CH2_ben_cryst'))
            intensityList = np.append(intensityList, searchForSignalIntensity(spectraData, 'CH2_ben_amorf'))
        case 3:
            intensityList = np.append(intensityList, searchForSignalIntensity(spectraData, 'CH2_ben_cryst'))
            intensityList = np.append(intensityList, searchForSignalIntensity(spectraData, 'CH2_twist_amorf'))
        case 4:
            intensityList = np.append(intensityList, searchForSignalIntensity(spectraData, 'CH2_ben_cryst'))
            intensityList = np.append(intensityList, searchForSignalIntensity(spectraData, 'CC_str_amorf'))
        case 5:
            signalNameList = list(par.SIGNAL_SHIFTS.keys())
            for i in signalNameList:
                intensityList = np.append(intensityList, searchForSignalIntensity(spectraData, i))
        case other:
            assert False, "Wrong option"

    return intensityList


def rawModelingWithNormalisation(path, normIntensity):
  filelist = inter.getfilenamelist(path)
  crystlist = np.array([], dtype='float')

  for filename in filelist:
    spectradatanorm = getdatafromfile(path + filename)

    normalisationintensity = searchforsignalintensity(spectradatanorm, par.signal_shifts[normIntensity])

    xcoordinates = list(spectradatanorm.keys())

    for i in xcoordinates:
      spectradatanorm[i] = spectradatanorm[i] / normalisationintensity

    intensitylist = getintensitylist(spectradatanorm)

    crystparams = calculatecrystparams(intensitylist)

    crystlist = np.append(crystlist, crystparams)

  writetofile("raw_normalised" + normIntensity + ".csv", crystlist)


def calculateCrystParams(intensityList):
  cryst1 = intensityList[0] / intensityList[1]  # I1 / I2
  cryst2 = intensityList[2] / intensityList[3]  # I3 / I4
  cryst3 = intensityList[2] / intensityList[4]  # I3 / I5
  cryst4 = intensityList[2] / intensityList[5]  # I3 / I6
  #crystr5 = 1416/(const * 1295 + 1303) do implementacji zwłaszcza do metod normalizacyjnych!!

  crystParams = np.array([
    cryst1,
    cryst2,
    cryst3,
    cryst4
  ], dtype='float')

  return crystParams
