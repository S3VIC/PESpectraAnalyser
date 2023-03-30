import params.parameters as par
import src.interface as inter
import numpy as np
import src.model as mod

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
            #SF - single file
            file = open(signalName + "_SF_shiftStab.txt", "a")
            spectraDict = mod.getDataFromFile(path + fileName)
            predictedShift = mod.searchForSignalIntensity(spectraDict, signalName)
            verifiedShift = mod.checkForMaximum(spectraDict, predictedShift)
#        checkShifts(predictedShift, verifiedShift)
            shiftDiff = signalShift - verifiedShift
#            differencesList.append(signalShift - verifiedShift)
            file.write(str(shiftDiff) + '\n')
        file.close()

def checkRamanShiftDiffForSpectraPairs(path1, path2, pairsDict):
    differencesList = []
    signals = par.SIGNAL_SHIFTS
    for key, value in pairsDict.items():
        spectra1Dict = mod.getDataFromFile(path1+key)
        spectra2Dict = mod.getDataFromFile(path2+value)
        for signalName, signalShift in signals.items():
            file = open(signalName + "_SF_shiftStabPaired.txt", "a")
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
    #print(pairFiles)
    return pairFiles

def getRamanShiftStats(path):
    fileList = inter.getFilenameList(path)

    for dataFileName in fileList:
        data = np.loadtxt(path + dataFileName)
        print(dataFileName + ":")
        print("min: " + str(min(data)))
        print("max: " + str(max(data)))
        print("\n")
