import numpy as np
import params.parameters as par
import src.interface as inter

#returns array containing shift and intensity respectively of the signal searched based on the first prediction
def checkForMaximum(spectraDict, foundSignalShift):
    maxInt = spectraDict[foundSignalShift]
    spectraShifts = list(spectraDict.keys())
    shiftIndex = spectraShifts.index(foundSignalShift)
    realShift = spectraShifts.index(foundSignalShift)
    for i in range(5):
        if spectraDict[spectraShifts[shiftIndex - i]] > maxInt:
          maxInt = spectraDict[spectraShifts[shiftIndex - i]]
          realShift = spectraShifts[shiftIndex - i]
    
    for i in range(5):
        if spectraDict[spectraShifts[shiftIndex + i]] > maxInt:
          maxInt = spectraDict[spectraShifts[shiftIndex - i]]
          realShift = spectraShifts[shiftIndex - i]
    signalParams = np.array([realShift, maxInt], dtype = 'float')

    return signalParams


#saves data to file from an array
def writeToFile(filename, crystValues):
  file = open(filename, "a")
  for value in crystValues:
    file.write(str(value) + "\n")
  file.close()


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
def calculateCryst1(path, outputFileName):
    cryst1 = np.array([], dtype='float')
    
    spectraData = getDataFromFile(path)
    ramanInt = np.array([], dtype='float')
    ramanInt = np.append(ramanInt, searchForSignalIntensity(spectraData, 'CH2_str_sym'))
    ramanInt = np.append(ramanInt, searchForSignalIntensity(spectraData, 'CH2_str_asym'))
    cryst1 = np.append(cryst1, ramanInt[1] / ramanInt[3])
    
    writeToFile(outputFileName + ".csv", cryst1)


def calculateCryst2(path, outputFileName):
    cryst2 = np.array([], dtype='float')
    spectraData = getDataFromFile(path)
    ramanInt = np.array([], dtype='float')
    ramanInt = np.append(ramanInt, searchForSignalIntensity(spectraData, 'CH2_ben_cryst'))
    ramanInt = np.append(ramanInt, searchForSignalIntensity(spectraData, 'CH2_ben_amorf'))
    cryst2 = np.append(cryst2, ramanInt[1] / ramanInt[3])
    
    writeToFile(outputFileName + ".csv", cryst2)


def calculateCryst3(path, outputFileName):
    cryst3 = np.array([], dtype='float')
    
    spectraData = getDataFromFile(path)
    ramanInt = np.array([], dtype='float')
    ramanInt = np.append(ramanInt, searchForSignalIntensity(spectraData, 'CH2_ben_cryst'))
    ramanInt = np.append(ramanInt, searchForSignalIntensity(spectraData, 'CH2_twist_amorf'))
    cryst3 = np.append(cryst3, ramanInt[1] / ramanInt[3])
    
    writeToFile(outputFileName + ".csv", cryst3)


def calculateCryst4(path, outputFileName):
    cryst4 = np.array([], dtype='float')

    spectraData = getDataFromFile(path)
    ramanInt = np.array([], dtype='float')
    ramanInt = np.append(ramanInt, searchForSignalIntensity(spectraData, 'CH2_ben_cryst'))
    ramanInt = np.append(ramanInt, searchForSignalIntensity(spectraData, 'CC_str_amorf'))
    cryst4 = np.append(cryst4, ramanInt[1] / ramanInt[3])
    
    writeToFile(outputFileName + ".csv", cryst4)

#
def calculateSingleCryst(path, fileNamesList, choice):
    fileName = input("File Name for cryst{0}: ".format(choice))
    for file in fileNamesList:
        match choice:
            case 1:
                calculateCryst1(path + file, fileName)
            case 2:
                calculateCryst2(path + file, fileName)
            case 3:
                calculateCryst3(path + file, fileName)
            case 4:
                calculateCryst4(path + file, fileName)
            case other:
                assert False, "Wrong option"
        print("File : " + file + " DONE")


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
            intensityList = np.append(intensityList, searchForSignalIntensity(spectraData, 'CH2_str_asym'))
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
