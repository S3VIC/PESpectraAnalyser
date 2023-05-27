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
            cr.deconvolutionTest(2, ['CH3_str_asym', 'CH2_str_sym'])
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
            cr.plotCrysts(path)
        case 4:
            mainMenu()


def crystCalculationActions():
    action = int(input(par.SELECT_PROMPT))
    match action:
        case 1:
            path = input("Path to .CSV files: ")
            #cr.calculateCrysts(path)
            cr.getPeaks(path, 2, "raw/", "", 1, ['CH2_str_sym', 'CH3_str_asym'])
            cr.getPeaks(path, 2, "raw/", "", 2, ['CH2_ben_cryst', 'CH2_ben_amorf'])
            cr.getPeaks(path, 2, "raw/", "", 3, ['CH2_ben_cryst', 'CH2_twist_amorf'])
            cr.getPeaks(path, 2, "raw/", "", 4, ['CH2_ben_cryst', 'CC_str_amorf'])
            cr.getPeaks(path, 2, "asLS/", "str_CH2/", 1, ['CH2_str_sym', 'CH3_str_asym'])
            cr.getPeaks(path, 2, "asLS/", "ben-twist-str/", 2, ['CH2_ben_cryst', 'CH2_ben_amorf'])
            cr.getPeaks(path, 2, "asLS/", "ben-twist-str/", 3, ['CH2_ben_cryst', 'CH2_twist_amorf'])
            cr.getPeaks(path, 2, "asLS/", "ben-twist-str/", 4, ['CH2_ben_cryst', 'CC_str_amorf'])
            cr.getPeaks(path, 2, "arLS/", "str_CH2/", 1, ['CH2_str_sym', 'CH3_str_asym'])
            cr.getPeaks(path, 2, "arLS/", "ben-twist-str/", 2, ['CH2_ben_cryst', 'CH2_ben_amorf'])
            cr.getPeaks(path, 2, "arLS/", "ben-twist-str/", 3, ['CH2_ben_cryst', 'CH2_twist_amorf'])
            cr.getPeaks(path, 2, "arLS/", "ben-twist-str/", 4, ['CH2_ben_cryst', 'CC_str_amorf'])
            cr.getPeaks(path, 2, "at/", "", 1, ['CH2_str_sym', 'CH3_str_asym'])
            cr.getPeaks(path, 2, "at/", "", 2, ['CH2_ben_cryst', 'CH2_ben_amorf'])
            cr.getPeaks(path, 2, "at/", "", 3, ['CH2_ben_cryst', 'CH2_twist_amorf'])
            cr.getPeaks(path, 2, "at/", "", 4, ['CH2_ben_cryst', 'CC_str_amorf'])
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
