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
                if value <= 1 and value >= 0:
                    count = count + 1
            percentTable.append(count/len(crystData))
        for element in range(4):
            print("Cryst " + str(element) + " " + str(percentTable[element]))
        print("\n")
        file.close()


def checkRamanShiftDiff(path, signalName):
    fileList = inter.getFilenameList(path)
    #print(len(fileList))
    differencesList = []
    for fileName in fileList:
        spectraDict = mod.getDataFromFile(path + fileName)
        predictedShift = mod.searchForSignalIntensity(spectraDict, signalName)
        verifiedShift = mod.checkForMaximum(spectraDict, predictedShift)
        #if abs(verifiedShift - predictedShift) > 1e-4:
            #print("Different")
        #else:
            #print("The same")
        differencesList.append(par.SIGNAL_SHIFTS[signalName] - verifiedShift)
    standarddev = np.std(differencesList) 
    average = np.average(differencesList)
    print(standarddev)
    print(average)
    print(min(differencesList))
    #sortedList = sdifferencesList.sort()

def checkRamanShiftDiffForSpectraPairs(path1, path2, pairsDict, signalName):
    differencesList = []
    for key, value in pairsDict.items():
        spectra1Dict = mod.getDataFromFile(path1+key)
        spectra2Dict = mod.getDataFromFile(path2+value)
        predictedShift1 = mod.searchForSignalIntensity(spectra1Dict, signalName)
        predictedShift2 = mod.searchForSignalIntensity(spectra2Dict, signalName)
        verifiedShift1 = mod.checkForMaximum(spectra1Dict, predictedShift1)
        verifiedShift2 = mod.checkForMaximum(spectra2Dict, predictedShift2)

        differencesList.append(verifiedShift1 - verifiedShift2)
    standardDev = np.std(differencesList)
    average = np.average(differencesList)
    print(standardDev)
    print(average)
    print(max(differencesList))

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