import params.parameters as par
import src.model as mod
import sys
import os
import src.visualiser as vis
import src.statisticalAnalysis as stat
import src.bgcorrection as bg

def displayOptions():
    print(par.SIMPLE_PLOTTING_OPTION)
    print(par.GAL_PEAKS_PLOTTING)
    print(par.FULL_PLOTTING_OPTION)
    print(par.MODELLING_ACTIONS)
    print("5) statistical analysis")
    actionChoice(sys.argv[1])


def displayModelOptions():
    print(par.RAW_MODEL_OPT)
    print(par.RAW_MODEL_WITH_NORMALISATION)
    print(par.OMNIC_BACK_CORRECTED)
    print(par.FULL_PLOTTING_OPTION)
    print(par.MAIN_MENU)


def mainMenu():
    print(par.WELCOME_MESSAGE)
    print(par.CHOOSE_MESSAGE)
    displayOptions()


def actionChoice(path):
    number = int(input("Select option: "))
    match number:
        case 1:
            assert False, par.notImplemented
        case 2:
            assert False, par.notImplemented
        case 3:
            assert False, par.notImplemented
        case 4:
            displayModelOptions()
            modelChoice(path)
        case 5:
            #stat.getCrystalStatistics(path)
            #bg.correctmcaLS(path)
            #stat.checkRamanShiftDiff(path)
            #stat.checkForPairSpectras(path, sys.argv[2])
            stat.checkRamanShiftDiffForSpectraPairs(path, sys.argv[2], stat.checkForPairSpectras(path, sys.argv[2]))
        # test case
        case 6:
            stat.getRamanShiftStats(path)
        case other:
            assert False, "nope"


def modelChoice(path):
    choice = int(input("Select option: "))
    match choice:
        case 1:
            mod.rawModelling(path)
        case 2:
            mod.rawModelingWithNormalisation(path, 'CH2_str_sym')
        case 3:
            assert False, par.notImplemented
        case 4:
            assert False, par.notImplemented
        case 5:
            assert False, par.notImplemented
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

