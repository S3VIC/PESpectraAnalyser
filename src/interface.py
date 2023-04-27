import params.parameters as par
import src.crystals as cr
import sys
import os
import src.visualiser as vis
import src.statisticalAnalysis as stat
import src.bg_algorithms as bg
import numpy as np


def mainMenu():
    print(par.WELCOME_MESSAGE)
    print(par.CHOOSE_MESSAGE)
    displayOptions()



def displayOptions():
    for prompt in par.INITIAL_PROMPTS:
        print(prompt)
    initialActionChoice()



def plottingOptions():
    for prompt in par.PLOTTING_OPTIONS:
        print(prompt)
    plottingActions()



def statisticalAnalysisOptions():
    for prompt in par.STATISTICAL_ANALYSIS_OPTIONS:
        print(prompt)
    statisticalAnalysisActions()



def modellingOptions():
    for prompt in par.MODELLING_OPTIONS:
        print(prompt)
    modellingActions()



def bgCorrectionOptions():
    for prompt in par.BGCORRECTION_OPTIONS:
        print(prompt)
    bgCorrectionActions()


def initialActionChoice():
    number = int(input(par.SELECT_PROMPT))
    match number:
        case 1:
            plottingOptions()
        case 2:
            statisticalAnalysisOptions()
        case 3:
            modellingOptions()
        case 4:
            bgCorrectionOptions()
        case 5:
            path = input("Path: ")
            cr.getPeaks(path, 10)
        case 6:
            path = input("Path: ")
            cr.plotCrysts(path)
        case 7:
            exit()
        case other:
            assert False, "nope"


def plottingActions():
    action = int(input(par.SELECT_PROMPT))
    match action:
        case 1:
            plottingOptions()
        case 2:
            assert False, par.notImplemented
        case 3:
            assert False, par.notImplemented
        case 4:
            vis.barCharts()
        case 5:
            mainMenu()
            

def statisticalAnalysisActions():
    action = int(input(par.SELECT_PROMPT))

    match action:
        case 1:
            stat.checkRamanShiftDiff()
        case 2:
            path1 = input("Directory 1 path: ")
            path2 = input("Directory 2 path: ")
            pairDict = stat.checkForPairSpectras(path1, path2)
            stat.checkRamanShiftDiffForSpectraPairs(path1, path2, pairDict)
        case 3:
            assert False, par.notImplemented
        case 4: 
            file1 = input("Path for 1st file with cryst params: ")
            file2 = input("Path for 2nd file with cryst params: ")
            stat.compareCrystParams(file1, file2)
        case 5:
            mainMenu()


def modellingActions():
    action = int(input(par.SELECT_PROMPT))
    match action:
        case 1:
            path = input("Path to .CSV files: ")
            cr.calculateCrysts(path)
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
            bg.setParams(1)
#            pathToInputFiles = input("Path to .CSV files: ")
#            pathToOutputFiles = input("Path to output files: ")
#            bg.correctAsLS(pathToInputFiles, pathToOutputFiles)
        case 2:
            bg.setParams(2)
           # pathToInputFiles = input("Path to .CSV files: ")
           # pathToOutputFiles = input("Path to output files: ")
           # bg.arLS(pathToInputFiles, pathToOutputFiles)
        case 3:
            pathToFile = input("(TESTING ALGORITHM VERSION) Path to file:") 
            bg.correctmcaLS(pathToFile)
        #case 4:
            #bg.setParams()
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
