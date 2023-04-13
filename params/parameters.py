# interface params
WELCOME_MESSAGE = "WELCOME TO PE-SPECTRA ANALYSER"
CHOOSE_MESSAGE = "Choose an option:"
SIMPLE_PLOTTING_OPTION = "1) Plot raw spectra"
GAL_PEAKS_PLOTTING = "2) Plot spectra with gal_peaks grid"
FULL_PLOTTING_OPTION = "3) Plot both: raw spectra and with gal_peaks"
MODELLING_ACTIONS = "4) Modelling options"

# general params
FILENAME_EXTENSION = "CSV"

#model options (for interface)
RAW_MODEL_OPT = "1) Raw modelling (based on raw spectra)"
RAW_MODEL_WITH_NORMALISATION = "2) Raw modelling with normalisation"
OMNIC_BACK_CORRECTED = "3) Modelling with corrected baseline (using OMNIC software)"
RAW_WITH_BASELINE_CORRECTION = "4) Modelling with baseline correction"
MAIN_MENU = "5) Back to main menu"

FILENAME_RAW_MODEL = "rawCryst.csv"
# model params
SIGNAL_SHIFTS = {
    'CH2_str_sym' : 2848,
    'CH2_str_asym' : 2882,
    'CH2_ben_cryst' : 1416,
    'CH2_ben_amorf' : 1440,
    'CH2_twist_amorf' : 1303,
    'CC_str_amorf' : 1080
}

cryst1Prompt = "Calculate cryst1"
cryst2Prompt = "Calculate cryst2"
cryst3Prompt = "Calculate cryst3"
cryst4Prompt = "Calculate cryst4"
crystPrompt = "Calculate all cryst params"
# SIGNAL_SHIFTS_KEY_LIST = list(SIGNAL_SHIFTS.keys())

# plotting parameters

notImplemented = "Not implemented yet"
