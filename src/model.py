import numpy as np
import params.parameters as par
import os

#Writing cryst calculated cryst parameters to a file (each time this function is evaluated
# the output is appended to file


def writeToFile(filename, crystList):
  file = open(filename, "a")
  for i in crystList:
    file.write(str(i[0]))
    file.write('\t')
    file.write(str(i[1]))
    file.write('\t')
    file.write(str(i[2]))
    file.write('\t')
    file.write(str(i[3]))
    file.write('\n')
  file.close()


def searchForSignalIntensity(spectraDict, signalShift):
  keys = list(spectraDict.keys())
  minDistance = abs(signalShift - keys[0])
  realShift = keys[0]

  for i in range(1, len(keys)):
      distance = abs(signalShift - keys[i])
      if distance < minDistance:
          minDistance = distance
          realShift = keys[i]
  signalInten = spectraDict[realShift]

  return signalInten


def getFilenames(path):
  fileList = []
  for filename in os.listdir(path):
    if filename[-3:].upper() == par.FILENAME_EXTENSION:
      temp_file = os.path.join(path, filename)
      if os.path.isfile(temp_file):
        fileList.append(filename)
  return fileList


def getDataFromFile(filePath):
  dataFile = np.loadtxt(filePath, delimiter=',')
  xCoordinates = np.array(dataFile[:, 0], dtype='float')
  yCoordinates = np.array(dataFile[:, 1], dtype='float')
  spectraData = {}

  for i in range(xCoordinates.size):
    spectraData[xCoordinates[i]] = yCoordinates[i]

  return spectraData


def rawModelling(path):
  filenamesList = getFilenames(path)
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


def rawModelingWithNormalisation(path):
  fileList = getFilenames(path)
  crystList_1 = []
  crystList_2 = []

  for filename in fileList:
    spectraDataNorm1 = getDataFromFile(path + filename)
    spectraDataNorm2 = getDataFromFile(path + filename)

    normalisationIntensities = [
      searchForSignalIntensity(spectraDataNorm1, par.SIGNAL_SHIFTS['CH2_str_sym']),
      searchForSignalIntensity(spectraDataNorm1, par.SIGNAL_SHIFTS['CH2_str_asym'])
    ]

    xCoordinates = list(spectraDataNorm1.keys())

    for i in xCoordinates:
      spectraDataNorm1[i] = spectraDataNorm1[i] / normalisationIntensities[0]
      spectraDataNorm2[i] = spectraDataNorm2[i] / normalisationIntensities[1]

    intensityList_1 = getIntensityList(spectraDataNorm1)
    intensityList_2 = getIntensityList(spectraDataNorm2)

    crystParams_1 = calculateCrystParams(intensityList_1)
    crystParams_2 = calculateCrystParams(intensityList_2)

    crystList_1.append(crystParams_1)
    crystList_2.append(crystParams_2)

  writeToFile("raw_normalised_1.csv", crystList_1)
  writeToFile("raw_normalised_2.csv", crystList_2)


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
