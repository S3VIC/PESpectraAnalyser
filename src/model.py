import numpy as np
import params.parameters as par
import src.interface as inter

#Writing cryst calculated cryst parameters to a file (each time this function is evaluated
# the output is appended to file

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
    

def writeToFile(filename, crystList):
  file = open(filename, "a")
  for dataSet in crystList:
    for k in range(4):
      file.write(str(dataSet[k]))
      if k != 3:
        file.write(',')
    file.write('\n')
  file.close()


def searchForSignalIntensity(spectraDict, signalName):
  keys = list(spectraDict.keys())
  signalShift = par.SIGNAL_SHIFTS[signalName]
  minDistance = abs(signalShift - keys[0])
  realShift = keys[0]

  for i in range(1, len(keys)):
      distance = abs(signalShift - keys[i])
      if distance < minDistance:
          minDistance = distance
          realShift = keys[i]
  signalInten = spectraDict[realShift]

#  return signalInten
  return realShift

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
  crystList = []
  for filename in filenamesList:
    spectraData = getDataFromFile(path + filename)

    intensityList = getIntensityList(spectraData)

#    Calculating cryst parameters
    crystParams = calculateCrystParams(intensityList)
    crystList.append(crystParams)

  writeToFile("test.csv", crystList)


def getIntensityList(spectraData):
  signalNameList = list(par.SIGNAL_SHIFTS.keys())

  intensityList = []

  for i in signalNameList:
    intensityList.append(searchForSignalIntensity(spectraData, par.SIGNAL_SHIFTS[i]))

  return intensityList


def rawModelingWithNormalisation(path, normalisationCoeff):
  fileList = inter.getFilenameList(path)
  crystList = []

  for filename in fileList:
    spectraDataNorm = getDataFromFile(path + filename)

    normalisationIntensity = searchForSignalIntensity(spectraDataNorm, par.SIGNAL_SHIFTS[normalisationCoeff])

    xCoordinates = list(spectraDataNorm.keys())

    for i in xCoordinates:
      spectraDataNorm[i] = spectraDataNorm[i] / normalisationIntensity

    intensityList = getIntensityList(spectraDataNorm)

    crystParams = calculateCrystParams(intensityList)

    crystList.append(crystParams)

  writeToFile("raw_normalised" + normalisationCoeff + ".csv", crystList)


def calculateCrystParams(intensityList):
  cryst1 = intensityList[0] / intensityList[1]  # I1 / I2
  cryst2 = intensityList[2] / intensityList[3]  # I3 / I4
  cryst3 = intensityList[2] / intensityList[4]  # I3 / I5
  cryst4 = intensityList[2] / intensityList[5]  # I3 / I6

  crystParams = [
    cryst1,
    cryst2,
    cryst3,
    cryst4
  ]

  return crystParams


