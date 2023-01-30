import params.parameters as par
import src.model as mod
import sys
import src.visualiser as vis

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
            vis.getCrystalData(sys.argv[1])
        case other:
            assert False, "nope"


def modelChoice(path):
    choice = int(input("Select option: "))
    match choice:
        case 1:
            mod.rawModelling(path)
        case 2:
            mod.rawModelingWithNormalisation(path)
        case 3:
            assert False, par.notImplemented
        case 4:
            assert False, par.notImplemented
        case 5:
            assert False, par.notImplemented
        case other:
            assert False, "nope"
