import numpy as np
import params.parameters as par
import src.interface as inter


def checkForMaximum(spectraDict, foundSignalShift):
    maxInt = foundSignalShift
    spectraShifts = list(spectraDict.keys())
    shiftIndex = spectraShifts.index(foundSignalShift)
    for i in range(5):
        if spectraDict[spectraShifts[shiftIndex - i]] > maxInt:
          maxInt = spectraShifts[shiftIndex - i]
    
    for i in range(5):
        if spectraDict[spectraShifts[shiftIndex + i]] > maxInt:
          maxInt = spectraShifts[shiftIndex + i]
    return maxInt
    

def writeToFile(filename, crystValues):
  file = open(filename, "a")
  for value in crystValues:
    file.write(str(value))
    file.write('\n')
  file.close()


def searchForSignalIntensity(spectraDict, signalName):
  keys = np.array(list(spectraDict.keys()))
  signalShift = par.SIGNAL_SHIFTS[signalName]
  minDistance = abs(signalShift - keys[0])
  realShift = keys[0]

  for i in range(1, len(keys)):
      distance = abs(signalShift - keys[i])
      if distance < minDistance:
          minDistance = distance
          realShift = keys[i]
  signalInten = spectraDict[realShift]

  return signalInten
  #return realShift


def getDataFromFile(filePath):
  dataFile = np.loadtxt(filePath, delimiter=',')
  xCoordinates = np.array(dataFile[:, 0], dtype='float')
  yCoordinates = np.array(dataFile[:, 1], dtype='float')
  spectraData = {}

  for i in range(xCoordinates.size):
    spectraData[xCoordinates[i]] = yCoordinates[i]

  return spectraData


def rawModelling(path):
  filenamesList = inter.getFilenameList(path)
  cryst1 = np.array([] ,dtype='float')
  cryst2 = np.array([] ,dtype='float')
  cryst3 = np.array([] ,dtype='float')
  cryst4 = np.array([] ,dtype='float')

  for filename in filenamesList:
    spectraData = getDataFromFile(path + filename)

    intensityList = getIntensityList(spectraData)
    #print(intensityList)
#    Calculating cryst parameters
    crystParams = calculateCrystParams(intensityList)
    cryst1 = np.append(cryst1, crystParams[0])
    cryst2 = np.append(cryst2, crystParams[1])
    cryst3 = np.append(cryst3, crystParams[2])
    cryst4 = np.append(cryst4, crystParams[3])
    
  fileName1 = input("File Name for cryst1: ")
  fileName2 = input("File Name for cryst2: ")
  fileName3 = input("File Name for cryst3: ")
  fileName4 = input("File Name for cryst4: ")
  
  writeToFile(fileName1 + ".csv", cryst1)
  writeToFile(fileName2 + ".csv", cryst2)
  writeToFile(fileName3 + ".csv", cryst3)
  writeToFile(fileName4 + ".csv", cryst4)


def getIntensityList(spectraData):
  signalNameList = list(par.SIGNAL_SHIFTS.keys())
  intensityList = np.array([], dtype='float')

  for i in signalNameList:
    intensityList = np.append(intensityList, searchForSignalIntensity(spectraData, i))

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
