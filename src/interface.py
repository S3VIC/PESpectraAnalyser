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
    print("1) Plotting")
    print("2) Statistical analysis")
    print("3) Modelling")
    print("4) Exit")
    actionChoice(sys.argv[1])


def plottingOptions():
    print("1) Raw plotting")
    print("2) Plotting with Gal peaks")
    print("3) Raw and Gal plotting")
    print("4) Maine menu")
    plottingActions()


def plottingActions():
    action = int(input("Select option: "))
    match action:
        case 1:
            plottingOptions()
        case 2:
            assert False, par.notImplemented
        case 3:
            assert False, par.notImplemented
        case 4:
            mainMenu()
            

def statisticalAnalysisOptions():
    print("1) Raman shift stability (raw)")
    print("2) Raman shift stabilility for paired spectras (OMNIC bg correction)")
    print("2) Raman shift stability (after bg correction)")
    print("4) Main menu")
    statisticalAnalysisActions()


def statisticalAnalysisActions():
    action = int(input("Select option: "))

    match action:
        case 1:
            assert False, par.notImplemented
        case 2:
            assert False, par.notImplemented
        case 3:
            assert False, par.notImplemented
        case 4:
            mainMenu()


def modellingOptions():
    print("1) Raw modelling (based on raw intensities)")
    print("2) Modelling bg corrected spectras")
    print("3) Main menu")
    modellingActions()


def modellingActions():
    action = int(input("Select option: "))
    match action:
        case 1:
            assert False, par.notImplemented
        case 2:
            assert False, par.notImplemented
        case 3:
            mainMenu()
        case other:
            assert False, "Wrong option"


def displayModelOptions():
    print(par.RAW_MODEL_OPT)
    print(par.RAW_MODEL_WITH_NORMALISATION)
    print(par.OMNIC_BACK_CORRECTED)
    print(par.FULL_PLOTTING_OPTION)
    print(par.MAIN_MENU)


def actionChoice(path):
    number = int(input("Select option: "))
    match number:
        case 1:
            plottingOptions()
        case 2:
            statisticalAnalysisOptions()
        case 3:
            displayModelOptions()
            modelChoice(path)
        case 4:
            exit()
        case other:
            assert False, "nope"


def getFilenameList(path):
  fileList = []
  for filename in os.listdir(path):
    if filename[-3:].upper() == par.FILENAME_EXTENSION:
      temp_file = os.path.join(path, filename)
      if os.path.isfile(temp_file):
        fileList.append(filename)
  return fileList

