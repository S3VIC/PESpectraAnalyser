#python imports
import sys
import os
import numpy as np

#custom imports
import src.prompts as pr
import params.parameters as par
import src.crystals as cr
import src.visualiser as vis
import src.stats as stat
import src.correction as cor


def mainMenu():
    print(par.WELCOME_MESSAGE)
    print(par.CHOOSE_MESSAGE)
    pr.displayOptions(par.INITIAL_PROMPTS)
    initialActionChoice()


def initialActionChoice():
    number = int(input(par.SELECT_PROMPT))
    match number:
        case 1:
            pr.displayOptions(par.BGCORRECTION_OPTIONS)
            bgCorrectionActions()
        case 2:
            pr.displayOptions(par.CRYST_CALCULATION)
            crystCalculationActions()
        case 3:
            pr.displayOptions(par.PLOTTING_OPTIONS)
            plottingActions()
        case 4:
            exit()
        case 5:
            path = input("Path: ")
            #cr.integratePeaks(path, 10, 'CH3_str_asym', 'CH2_str_sym')
            #cr.integratePeaks(path, 10, 'CH2_ben_amorf', 'CH2_ben_cryst')
            #cr.integratePeaks(path, 10, 'CH2_ben_amorf', 'CH2_twist_amorf')
            cr.integratePeaks(path, 10, 'CH2_ben_amorf', 'CC_str_amorf')
        case 6:
            cr.deconv1(2) 

        case 7:
            stat.findRSshifts()
        case 8:
            cr.deconv2(2)
        case 9:
            cr.deconv3(2)
        case 10:
            cr.deconv4()

        case other:
            assert False, "nope"


def plottingActions():
    action = int(input(par.SELECT_PROMPT))
    match action:
        case 1:
            path = input("Path for CSV files: ")
        case 2:
            assert False, par.notImplemented
        case 3:
            path = input("Path for CSV files: ")
            vis.plotCrysts(path)
        case 4:
            mainMenu()
        case 5:
            pathRaw = input("Path for raw files: ")
            pathOmnic = input("Path for omnic files: ")
            vis.plotOmnicPartialSpectra(pathRaw, pathOmnic)


def crystCalculationActions():
    action = int(input(par.SELECT_PROMPT))
    match action:
        case 1:
            path = input("Path to .CSV files: ")
            #cr.saveRawCrysts(path)
            cr.saveRawCrysts(path, 2, "raw/", "", 1, ['CH2_str_sym', 'CH3_str_asym'])
            cr.saveRawCrysts(path, 2, "raw/", "", 2, ['CH2_ben_cryst', 'CH2_ben_amorf'])
            cr.saveRawCrysts(path, 2, "raw/", "", 3, ['CH2_ben_cryst', 'CH2_twist_amorf'])
            cr.saveRawCrysts(path, 2, "raw/", "", 4, ['CH2_ben_cryst', 'CC_str_amorf'])
            cr.saveRawCrysts(path, 2, "asLS/", "str_CH2/", 1, ['CH2_str_sym', 'CH3_str_asym'])
            cr.saveRawCrysts(path, 2, "asLS/", "ben-twist-str/", 2, ['CH2_ben_cryst', 'CH2_ben_amorf'])
            cr.saveRawCrysts(path, 2, "asLS/", "ben-twist-str/", 3, ['CH2_ben_cryst', 'CH2_twist_amorf'])
            cr.saveRawCrysts(path, 2, "asLS/", "ben-twist-str/", 4, ['CH2_ben_cryst', 'CC_str_amorf'])
            cr.saveRawCrysts(path, 2, "arLS/", "str_CH2/", 1, ['CH2_str_sym', 'CH3_str_asym'])
            cr.saveRawCrysts(path, 2, "arLS/", "ben-twist-str/", 2, ['CH2_ben_cryst', 'CH2_ben_amorf'])
            cr.saveRawCrysts(path, 2, "arLS/", "ben-twist-str/", 3, ['CH2_ben_cryst', 'CH2_twist_amorf'])
            cr.saveRawCrysts(path, 2, "arLS/", "ben-twist-str/", 4, ['CH2_ben_cryst', 'CC_str_amorf'])
            if(os.path.exists(path + "at/")):
                cr.saveRawCrysts(path, 2, "at/", "", 1, ['CH2_str_sym', 'CH3_str_asym'])
                cr.saveRawCrysts(path, 2, "at/", "", 2, ['CH2_ben_cryst', 'CH2_ben_amorf'])
                cr.saveRawCrysts(path, 2, "at/", "", 3, ['CH2_ben_cryst', 'CH2_twist_amorf'])
                cr.saveRawCrysts(path, 2, "at/", "", 4, ['CH2_ben_cryst', 'CC_str_amorf'])
        case 2:
            assert False, par.notImplemented
        case 3:
            assert False, par.notImplemented
        #    stat.searchForPeaks()
        case 4:
            mainMenu()
        case other:
            assert False, "Wrong option"


def bgCorrectionActions():
    action = int(input(par.SELECT_PROMPT))
    match action:
        case 1:
            cor.setParams(1)
        case 2:
            cor.setParams(2)
        case other:
            assert False, "Wrong option"



def getFilenameList(path):
    fileList = np.array([])
    for filename in os.listdir(path):
        if filename[-3:].upper() == par.FILENAME_EXTENSION:
            temp_file = os.path.join(path, filename)
            if os.path.isfile(temp_file):
                fileList = np.append(fileList, filename)
    
    fileList = np.sort(fileList)
    return fileList



def displayCrystParamsInfo():
    print(par.cryst1Prompt)
    print(par.cryst2Prompt)
    print(par.cryst3Prompt)
    print(par.cryst4Prompt)
    print(par.crystPrompt)
    
def logStatus(maxNum, counter, fileName):
    print(fileName + " " + str(counter) + " out of " + str(maxNum) + " [DONE]") 



#reads data from file and returns it in form of dictionary {RAMAN SHIFT : INTENSITY} 
def getDataFromFile(filePath):
    dataFile = np.loadtxt(filePath, delimiter=',')
    xCoordinates = np.array(dataFile[:, 0], dtype='float')
    yCoordinates = np.array(dataFile[:, 1], dtype='float')
    spectraData = {}

    for i in range(xCoordinates.size):
        spectraData[xCoordinates[i]] = yCoordinates[i]

    return spectraData


def writeCrystToFile(filename, crystValue):
    file = open(filename, "a")
    file.write(str(crystValue) + "\n")
    file.close()

def writeCrystsToFile(fileName, crystsArr):
    file = open(fileName, 'a')
    for cryst in crystsArr:
        file.write(str(cryst) + '\n')
    file.close()



def createIDs():
    pathForIDs = input("Path for renamed files: ")
    fileNames = getFilenameList(pathForIDs)
    ids = np.array([])
    for file in fileNames:
        ids = np.append(ids, file[:file.find('_')])
    print(ids)
    return ids


def deconvChoice():
    for prompt in par.deconvChoicePrompts:
        print(prompt)
    choice = input("Choose parameter to calculate: ")
    return choice
