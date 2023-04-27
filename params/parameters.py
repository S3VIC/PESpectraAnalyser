# interface params
WELCOME_MESSAGE = "WELCOME TO PE-SPECTRA ANALYSER"
CHOOSE_MESSAGE = "Choose an option:"
SIMPLE_PLOTTING_OPTION = "1) Plot raw spectra"
GAL_PEAKS_PLOTTING = "2) Plot spectra with gal_peaks grid"
FULL_PLOTTING_OPTION = "3) Plot both: raw spectra and with gal_peaks"
MODELLING_ACTIONS = "4) Modelling options"

#interface prompts
SELECT_PROMPT = "Select option: "
INITIAL_PROMPTS = [
    "1) Plotting",
    "2) Statistical analysis",
    "3) Modelling",
    "4) Background correction",
    "5) Exit"
    ]

PLOTTING_OPTIONS = [
    "1) Raw plotting",
    "2) Plotting with Gal peaks",
    "3) Raw and Gal plotting",
    "4) Bar chart",
    "5) Maine menu",
    ]

STATISTICAL_ANALYSIS_OPTIONS = [
    "1) Raman shift stability (raw)",
    "2) Raman shift stabilility for paired spectras (OMNIC bg correction)",
    "3) Raman shift stability (after bg correction)",
    "4) Compare cryst params",
    "5) Main menu"
    ]
MODELLING_OPTIONS = [
    "1) Raw modelling (based on raw intensities)",
    "2) Modelling bg corrected spectras",
    "3) Search for peaks",
    "4) Main menu",
    ]
BGCORRECTION_OPTIONS = [
    "1) asLS",
    "2) arLS"
    ]
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
    'CH3_str_asym' : 2882,
    'CH2_str_sym' : 2848,
    'CH2_ben_amorf' : 1440,
    'CH2_ben_cryst' : 1416,
    'CH2_twist_amorf' : 1303,
    'CH2_twist_cryst_int' : 1295,
    'CC_str_amorf' : 1080
}


cryst1Prompt = "1) Calculate cryst1"
cryst2Prompt = "2) Calculate cryst2"
cryst3Prompt = "3) Calculate cryst3"
cryst4Prompt = "4) Calculate cryst4"
crystPrompt = "5) Calculate all cryst params"

# SIGNAL_SHIFTS_KEY_LIST = list(SIGNAL_SHIFTS.keys())

# plotting parameters
notImplemented = "Not implemented yet"
