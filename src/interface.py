import params.parameters as par
import src.model as mod
import sys
import os
import src.visualiser as vis
import src.statisticalAnalysis as stat
import src.bgcorrection as bg


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
            pathToFiles="data/input/raw/"
            pathToOutputFiles="data/output/"
            #bg.correctmcaLS(pathToFile)
            #bg.correctAsLS(pathToFile)
            bg.arLS(pathToFiles, pathToOutputFiles)
        case 5:
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
            mod.calculateCrysts(path)
        case 2:
            assert False, par.notImplemented
        case 3:
            assert False, par.notImplemented
        #    stat.searchForPeaks()
        case 4:
            mainMenu()
        case other:
            assert False, "Wrong option"



def getFilenameList(path):
    fileList = []
    for filename in os.listdir(path):
        if filename[-3:].upper() == par.FILENAME_EXTENSION:
            temp_file = os.path.join(path, filename)
        if os.path.isfile(temp_file):
            fileList.append(filename)
    return fileList

def displayCrystParamsInfo():
    print(par.cryst1Prompt)
    print(par.cryst2Prompt)
    print(par.cryst3Prompt)
    print(par.cryst4Prompt)
    print(par.crystPrompt)
    
