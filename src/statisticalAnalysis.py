import params.parameters as par
import src.interface as inter
import numpy as np
import src.model as mod
from scipy.signal import find_peaks


def getCrystalStatistics(path):
    fileList = inter.getFilenameList(path)
    for fileName in fileList:
        file = open(fileName, "r")
        fileData = np.loadtxt(file, delimiter = ',')
        percentTable = []
        print("For file" + fileName + ":")
        for column in range(4):
            crystData = np.array(fileData[:, column], dtype = 'float')
            count = 0
            for value in crystData:
                if 1 >= value >= 0:
                    count = count + 1
            percentTable.append(count/len(crystData))
        for element in range(4):
            print("Cryst " + str(element) + " " + str(percentTable[element]))
        print("\n")
        file.close()


def checkShifts(predictedShift, verifiedShift):
    if abs(verifiedShift - predictedShift) > 1e-4:
        print("Different")
    else:
        print("The same")


def checkRamanShiftDiff():
    path = input("Directory path: ")
    signals = par.SIGNAL_SHIFTS
    fileList = inter.getFilenameList(path)
    
    for fileName in fileList:
        for signalName, signalShift in signals.items():
            differencesList = []
            file = open(signalName + "_SF_shiftStab.csv", "a")
            spectraDict = mod.getDataFromFile(path + fileName)
            predictedShift = mod.searchForSignalIntensity(spectraDict, signalName)
            verifiedShift = mod.checkForMaximum(spectraDict, predictedShift)
            shiftDiff = signalShift - verifiedShift
            file.write(str(shiftDiff) + '\n')
        file.close()


def checkRamanShiftDiffForSpectraPairs(path1, path2, pairsDict):
    differencesList = []
    signals = par.SIGNAL_SHIFTS

    for key, value in pairsDict.items():
        spectra1Dict = mod.getDataFromFile(path1+key)
        spectra2Dict = mod.getDataFromFile(path2+value)
    
        for signalName, signalShift in signals.items():
            file = open(signalName + "_SF_shiftStabPaired.csv", "a")
            predictedShift1 = mod.searchForSignalIntensity(spectra1Dict, signalName)
            predictedShift2 = mod.searchForSignalIntensity(spectra2Dict, signalName)
            verifiedShift1 = mod.checkForMaximum(spectra1Dict, predictedShift1)
            verifiedShift2 = mod.checkForMaximum(spectra2Dict, predictedShift2)
            shiftDiff = verifiedShift1 - verifiedShift2
            file.write(str(shiftDiff) + '\n')
        
        file.close()


def checkForPairSpectras(path1, path2):
    fileList1 = inter.getFilenameList(path1)
    fileList2 = inter.getFilenameList(path2)
    pairFiles = {}

    for fileName in fileList1:
        for fileName2 in fileList2:
            if fileName in fileName2:
                pairFiles[fileName] = fileName2
    return pairFiles


def searchForPeaks():
    path1 = input("Directory path: ")
    fileList = inter.getFilenameList(path1)
    
    for fileName in fileList:
        file = open(fileName, "r")
        data = np.loadtxt(path1 + fileName, delimiter=',')
        yCoordinates = np.array(data[:, 1], dtype = 'float')
        peakIndices = find_peaks(yCoordinates, width = 1)
        print(len(peakIndices[0]))
        print(peakIndices[0])
            
