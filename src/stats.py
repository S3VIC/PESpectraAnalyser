import params.parameters as par
import src.interface as inter
import numpy as np
import src.crystals as cr 
import src.visualiser as vis
from scipy.signal import find_peaks


def saveRSData(data):
    signalNames = list(par.SIGNAL_SHIFTS.keys())
    for i in range(len(data)):
        file = open(signalNames[i] + "_shifts.csv", "a")
        file.write(str(data[i]) + "\n")
        file.close()


def findRSshifts():
    path = input("Path for CSV files: ")
    fileNameList = inter.getFilenameList(path)

    for fileName in fileNameList:
        data = np.loadtxt(path + fileName, delimiter = ',')
        X = np.array(data[:, 0], dtype = 'float')
        Y = np.array(data[:, 1], dtype = 'float')
        peaksIndexes = find_peaks(Y, prominence = 2)[0]
        peaksSpectraShifts = np.array(X[peaksIndexes], dtype = 'float')
        filteredPeaksShifts = np.array([], dtype = 'float')
        
        for signal in list(par.SIGNAL_SHIFTS.keys()):
            peakShift = peaksSpectraShifts[0]
            peakRefShift = par.SIGNAL_SHIFTS[signal] 
            for peak in peaksSpectraShifts:
                shiftDiff = peak - peakRefShift
                refShiftDiff = peakShift - peakRefShift
                if(abs(shiftDiff) <= abs(refShiftDiff)):
                    peakShift = peak
            filteredPeaksShifts = np.append(filteredPeaksShifts, peakShift - peakRefShift)
        saveRSData(filteredPeaksShifts)
        print(fileName)
        print(filteredPeaksShifts)


