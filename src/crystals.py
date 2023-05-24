import numpy as np
import scipy as sc
import matplotlib.pyplot as plt
import matplotlib as mlt
from enum import Enum

#custom imports
import params.parameters as par
import src.interface as inter
import src.funcAnalysis as fan
import src.visualiser as vis


class Color(Enum):
    RED = 0
    YELLOW = 1
    BLUE = 2
    GREEN = 3


class Markers(Enum):
    CROSS = 0
    SQUARE = 1
    TRIANGLE = 2
    DIAMOND = 3





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

def createIDs():
    pathForIDs = input("Path for renamed files: ")
    fileNames = inter.getFilenameList(pathForIDs)
    ids = np.array([])
    for file in fileNames:
        ids = np.append(ids, file[:file.find('_')])
    print(ids)
    return ids
        

def getBgType(fileName):
    bgType = fileName[fileName.index("_") + 1 : -4]
    match bgType:
        case "raw":
            return Markers.CROSS
        case "asLS":
            return Markers.SQUARE
        case "arLS":
            return Markers.TRIANGLE
        case "at":
            return Markers.DIAMOND
        case other:
            assert False, "Error, bgType not recognised!"


def getCrystType(fileName):
    crystType = int(fileName[5])
    match crystType:
        case 1:
            return Color.RED
        case 2:
            return Color.YELLOW
        case 3:
            return Color.BLUE
        case 4:
            return Color.GREEN 
        case other:
            assert False, "Error, index out of enum range!"


def plotCrysts(path):
    mlt.rcParams.update({'figure.autolayout': True})
    mlt.use("Cairo")
    fileList = inter.getFilenameList(path)
    ids = createIDs()
    fig, ax = plt.subplots()
    ax.set_ylabel("Value")
    ax.set_xlabel("Probe ID")
    plt.ylim([0, 2.2])

    for fileName in fileList:
        marker = getBgType(fileName)
        color = getCrystType(fileName)
        file = open(path + fileName, "r")
        data = np.loadtxt(file)
        plt.scatter(ids, data, c = par.colors[color.value], marker = par.markers[marker.value])
        file.close()

    plt.xticks(rotation=45)
    plt.savefig("test2.png", dpi = 400)
    plt.close()


#Calculates crystals based on given signals (cryst type) and type of bg correction that was applied on spectra
def getPeaks(path, promin, signalType, addPath, crystNum, signals):
    fullPath = path + signalType + addPath
    
    fileNamesList = inter.getFilenameList(fullPath)
    for i in range(len(fileNamesList)):
        data = np.loadtxt(fullPath + fileNamesList[i], delimiter = ',')
        intensities = np.array(data[:, 1], dtype ='float')
        ramanshifts = np.array(data[:, 0], dtype ='float')

        peaksIndexes = sc.signal.find_peaks(intensities, prominence = promin)
        peaksShifts = np.array(ramanshifts[peaksIndexes[0]], dtype = 'float')
#        print(peaksShifts)
        peaksIntensities = np.array(intensities[peaksIndexes[0]], dtype = 'float')
        peakShifts = {}
        peakData = {}
        
        for signal in signals:
            referenceShift = par.SIGNAL_SHIFTS[signal]
            spectraShift = peaksShifts[0]
            spectraIntensities = peaksIntensities[0]

            for j in range(1, len(peaksShifts)):
                diff = abs(peaksShifts[j] - referenceShift)
                refDiff = abs(spectraShift - referenceShift)
                if(diff <= refDiff):
                    spectraShift = peaksShifts[j]
                    spectraInten = peaksIntensities[j]
    
            peakShifts[signal] = spectraShift
            peakData[spectraShift] = spectraInten

        #print(peakShifts)
        peaks = np.array([peakShifts, peakData])
        calculateSimpleCryst(peaks[1][peaks[0][signals[0]]], peaks[1][peaks[0][signals[1]]], "cryst" + str(crystNum) + "_" + signalType[:-1])


#saves data to file from an array
def writeCrystToFile(filename, crystValue):
    file = open(filename, "a")
    file.write(str(crystValue) + "\n")
    file.close()

def integratePeaks(path, promin, peak1Name, peak2Name):

    fileList = inter.getFilenameList(path)
    for fileName in fileList:
        file = open(path + fileName, 'r')

        data = np.loadtxt(file, delimiter = ',')
        x = data[:, 0]
        y = data[:, 1]
        file.close()
        peakIndex = sc.signal.find_peaks(y, prominence = promin)
        peakShifts = np.array(x[peakIndex[0]], dtype = 'float')
        peakInten = np.array(y[peakIndex[0]], dtype = 'float')
        referenceShift1 = par.SIGNAL_SHIFTS[peak1Name]
        referenceShift2 = par.SIGNAL_SHIFTS[peak2Name]

        shift1 = peakShifts[0]
        shift2 = peakShifts[0]
        inten1 = peakInten[0]
        inten2 = peakInten[0]

        for i in range(1, len(peakShifts)):
            diff_raw1 = abs(peakShifts[i] - referenceShift1)
            refDiff1 = abs(shift1 - referenceShift1)
            if(diff_raw1 <= refDiff1):
                shift1 = peakShifts[i]
                inten1 = peakInten[i]

            diff_raw2 = abs(peakShifts[i] - referenceShift2)
            refDiff2 = abs(shift2 - referenceShift2)
            if(diff_raw2 <= refDiff2):
                shift2 = peakShifts[i]
                inten2 = peakInten[i]

        indexOfPeak1 = np.where( x == shift1 ) 
        indexOfPeak2 = np.where( x == shift2 )
        index1 = int(indexOfPeak1[0]) 
        index2 = int(indexOfPeak2[0])
        offset = 30

        area1 = fan.rectIntegLeft(x[index1 - offset : index1 + offset], y[index1 - offset : index1 + offset])
        area2 = fan.rectIntegLeft(x[index2 - offset : index2 + offset], y[index2 - offset : index2 + offset])
        
        cryst = area1 / area2
        writeCrystToFile("cryst4_raw_intRectLeft.CSV", cryst)

        area3 = fan.rectIntegRight(x[index1 - offset : index1 + offset], y[index1 - offset : index1 + offset])
        area4 = fan.rectIntegRight(x[index2 - offset : index2 + offset], y[index2 - offset : index2 + offset])
        cryst = area3 / area4
        writeCrystToFile("cryst4_raw_intRectRight.CSV", cryst)

        area5 = fan.trapInteg(x[index1 - offset : index1 + offset], y[index1 - offset : index1 + offset])
        area6 = fan.trapInteg(x[index2 - offset : index2 + offset], y[index2 - offset : index2 + offset])
        cryst = area5 / area6
        writeCrystToFile("cryst4_raw_intTrap.CSV", cryst)
        print(fileName + " finished")


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



  # alSS
  # arPLS
  # airPLS
