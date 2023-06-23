import numpy as np

#reference shifts
SIGNAL_SHIFTS = {
    'CH2_str_asym' : 2882,
    'CH2_str_sym' : 2848,
    'CH2_ben_amorf' : 1440,
    'CH2_ben_cryst' : 1416,
    'CH2_twist_amorf' : 1303,
    'CC_str_amorf' : 1080
}

#Params for cryst 1
c1_min_p1 = np.array([1, SIGNAL_SHIFTS['CH2_str_sym'] - 4, 0.5], dtype = 'float')
c1_min_p2 = np.array([1, SIGNAL_SHIFTS['CH2_str_asym'] - 4, 0.5], dtype = 'float')
c1_min_p3 = np.array([1, 2898, 0.5], dtype = 'float')
c1_min_p4 = np.array([1, 2925, 0.5], dtype = 'float')

c1_max_p1 = np.array([np.inf, SIGNAL_SHIFTS['CH2_str_sym'] + 6, np.inf], dtype = 'float')
c1_max_p2 = np.array([np.inf, SIGNAL_SHIFTS['CH2_str_asym'] + 6, np.inf], dtype = 'float')
c1_max_p3 = np.array([np.inf, 2912, np.inf], dtype = 'float')
c1_max_p4 = np.array([np.inf, 2939, np.inf], dtype = 'float')


c1_bounds_low = np.concatenate((c1_min_p1, c1_min_p2, c1_min_p3, c1_min_p4), axis = None)
c1_bounds_high = np.concatenate((c1_max_p1, c1_max_p2, c1_max_p3, c1_max_p4), axis = None)

#init values
c1_init_p1 = np.array([1, SIGNAL_SHIFTS['CH2_str_sym'], 1], dtype = 'float')
c1_init_p2 = np.array([1, SIGNAL_SHIFTS['CH2_str_asym'], 1], dtype = 'float')
c1_init_p3 = np.array([1, 2905, 1], dtype = 'float')
c1_init_p4 = np.array([1, 2932, 1], dtype = 'float')

c1_bounds = (c1_bounds_low, c1_bounds_high)
c1_pInit = np.concatenate((c1_init_p1, c1_init_p2, c1_init_p3, c1_init_p4), axis = None)
###############################################################################

#Params for cryst 2
c2_min_p1 = np.array([1, SIGNAL_SHIFTS['CH2_ben_cryst'] - 7, 0.1], dtype = 'float')
c2_min_p2 = np.array([1, SIGNAL_SHIFTS['CH2_ben_amorf'] - 12, 0.1], dtype = 'float')
c2_min_p3 = np.array([1, 1459, 1], dtype = 'float')
c2_min_p4 = np.array([1, 1470, 1], dtype = 'float')

c2_max_p1 = np.array([5e3, SIGNAL_SHIFTS['CH2_ben_cryst'] + 12, np.inf], dtype = 'float')
c2_max_p2 = np.array([5e3, SIGNAL_SHIFTS['CH2_ben_amorf'] + 12, np.inf], dtype = 'float')
c2_max_p3 = np.array([5e3, 1464, np.inf], dtype = 'float')
c2_max_p4 = np.array([5e3, 1480, np.inf], dtype = 'float')


c2_bounds_low = np.concatenate((c2_min_p1, c2_min_p2, c2_min_p3, c2_min_p4), axis = None)
c2_bounds_high = np.concatenate((c2_max_p1, c2_max_p2, c2_max_p3, c2_max_p4), axis = None)

#init values
c2_init_p1 = np.array([1, SIGNAL_SHIFTS['CH2_ben_cryst'], 1], dtype = 'float')
c2_init_p2 = np.array([1, SIGNAL_SHIFTS['CH2_ben_amorf'], 1], dtype = 'float')
c2_init_p3 = np.array([1, 1460, 1], dtype = 'float')
c2_init_p4 = np.array([1, 1475, 1], dtype = 'float')

c2_bounds = (c2_bounds_low, c2_bounds_high)
c2_pInit = np.concatenate((c2_init_p1, c2_init_p2, c2_init_p3, c2_init_p4), axis = None)



#Params for cryst 3 (uses also params for cryst 2)
c3_min_p1 = np.array([0.01, SIGNAL_SHIFTS['CH2_twist_amorf'] - 15, 1], dtype = 'float')
c3_min_p2 = np.array([0.01, 1310, 1], dtype = 'float')

c3_max_p1 = np.array([2e5, SIGNAL_SHIFTS['CH2_twist_amorf'] + 1, np.inf], dtype = 'float')
c3_max_p2 = np.array([2e5, 1319, np.inf], dtype = 'float')


c3_bounds_low = np.concatenate((c3_min_p1, c3_min_p2), axis = None)
c3_bounds_high = np.concatenate((c3_max_p1, c3_max_p2), axis = None)

#init values
c3_init_p1 = np.array([1, SIGNAL_SHIFTS['CH2_twist_amorf'], 3], dtype = 'float')
c3_init_p2 = np.array([1, 1315, 3], dtype = 'float')

c3_bounds = (c3_bounds_low, c3_bounds_high)
c3_pInit = np.concatenate((c3_init_p1, c3_init_p2), axis = None)


#Params for cryst 4 (uses also params for cryst 2)
c4_min_p1 = np.array([1, SIGNAL_SHIFTS['CC_str_amorf'] - 5, 1], dtype = 'float')
c4_min_p2 = np.array([1, 1065, 1], dtype = 'float')

c4_max_p1 = np.array([4.5e3, SIGNAL_SHIFTS['CC_str_amorf'] + 5, 15], dtype = 'float')
c4_max_p2 = np.array([4.5e3, 1075, 4], dtype = 'float')


c4_bounds_low = np.concatenate((c4_min_p1, c4_min_p2), axis = None)
c4_bounds_high = np.concatenate((c4_max_p1, c4_max_p2), axis = None)

#init values
c4_init_p1 = np.array([1, SIGNAL_SHIFTS['CC_str_amorf'], 1], dtype = 'float')
c4_init_p2 = np.array([1, 1070, 1], dtype = 'float')

c4_bounds = (c4_bounds_low, c4_bounds_high)
c4_pInit = np.concatenate((c4_init_p1, c4_init_p2), axis = None)
#############################################################################################################################################
