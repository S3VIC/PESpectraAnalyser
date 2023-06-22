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
c1_min_p1 = np.array([1, SIGNAL_SHIFTS['CH2_str_sym'] - 4, 1], dtype = 'float')
c1_min_p2 = np.array([1, SIGNAL_SHIFTS['CH2_str_asym'] - 4, 1], dtype = 'float')
c1_min_p3 = np.array([1, 2898, 1], dtype = 'float')
c1_min_p4 = np.array([1, 2925, 1], dtype = 'float')

c1_max_p1 = np.array([4.5e3, SIGNAL_SHIFTS['CH2_str_sym'] + 6, 25], dtype = 'float')
c1_max_p2 = np.array([4.5e3, SIGNAL_SHIFTS['CH2_str_asym'] + 6, 25], dtype = 'float')
c1_max_p3 = np.array([1.5e3, 2912, 30], dtype = 'float')
c1_max_p4 = np.array([1.5e3, 2939, 30], dtype = 'float')


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
c2_min_p1 = np.array([1, SIGNAL_SHIFTS['CH2_ben_cryst'] - 7, 1], dtype = 'float')
c2_min_p2 = np.array([1, SIGNAL_SHIFTS['CH2_ben_amorf'] - 12, 1], dtype = 'float')
c2_min_p3 = np.array([0, 1459, 1], dtype = 'float')
c2_min_p4 = np.array([1, 1470, 1], dtype = 'float')

c2_max_p1 = np.array([4.5e3, SIGNAL_SHIFTS['CH2_ben_cryst'] + 12, 15], dtype = 'float')
c2_max_p2 = np.array([4.5e3, SIGNAL_SHIFTS['CH2_ben_amorf'] + 12, 4], dtype = 'float')
c2_max_p3 = np.array([4.5e3, 1464, 20], dtype = 'float')
c2_max_p4 = np.array([4.5e3, 1480, 20], dtype = 'float')


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
c3_min_p1 = np.array([1, SIGNAL_SHIFTS['CH2_twist_amorf'] - 4, 1], dtype = 'float')
c3_min_p2 = np.array([1, 1310, 1], dtype = 'float')

c3_max_p1 = np.array([4.5e3, SIGNAL_SHIFTS['CH2_twist_amorf'] + 4, 15], dtype = 'float')
c3_max_p2 = np.array([4.5e3, 1319, 4], dtype = 'float')


c3_bounds_low = np.concatenate((c3_min_p1, c3_min_p2), axis = None)
c3_bounds_high = np.concatenate((c3_max_p1, c3_max_p2), axis = None)

#init values
c3_init_p1 = np.array([1, SIGNAL_SHIFTS['CH2_twist_amorf'], 1], dtype = 'float')
c3_init_p2 = np.array([1, 1315, 1], dtype = 'float')

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


#Params for cryst 2-3
#min c23_bounds model
c23_min_p1 = np.array([1, SIGNAL_SHIFTS['CH2_ben_amorf']  - 8, 1], dtype = 'float')
c23_min_p2 = np.array([1, SIGNAL_SHIFTS['CH2_ben_cryst']  - 8, 1], dtype = 'float')
c23_min_p3 = np.array([1, SIGNAL_SHIFTS['CH2_twist_amorf']  - 10, 1], dtype = 'float')

#max c23_bounds model
c23_max_p1 = np.array([3.5e3, SIGNAL_SHIFTS['CH2_ben_amorf'] + 8, 30], dtype = 'float')
c23_max_p2 = np.array([3.5e3, SIGNAL_SHIFTS['CH2_ben_cryst'] + 8, 30], dtype = 'float')
c23_max_p3 = np.array([3.5e3, SIGNAL_SHIFTS['CH2_twist_amorf'] + 10, 30], dtype = 'float')

#min c23_bounds additional
c23_min_p4 = np.array([1, 1460, 1], dtype = 'float')
c23_min_p5 = np.array([1, 1365, 1], dtype = 'float')
c23_min_p6 = np.array([1, 1345, 1], dtype = 'float')
c23_min_p7 = np.array([1, 1310, 1], dtype = 'float')
#max c23_bounds additional
c23_max_p4 = np.array([3.5e3, 1477, 30], dtype = 'float')
c23_max_p5 = np.array([3.5e3, 1375, 30], dtype = 'float')
c23_max_p6 = np.array([3.5e3, 1355, 30], dtype = 'float')
c23_max_p7 = np.array([3.5e3, 1318, 30], dtype = 'float')
c23_bounds_low = np.concatenate((c23_min_p1, c23_min_p2, c23_min_p3, c23_min_p4, c23_min_p5, c23_min_p6, c23_min_p7), axis = None) #axis = None for creating 1D array
c23_bounds_high = np.concatenate((c23_max_p1, c23_max_p2, c23_max_p3, c23_max_p4, c23_max_p5, c23_max_p6, c23_max_p7), axis = None) #axis = None for creating 1D array
#init values
c23_init_p1 = np.array([1, SIGNAL_SHIFTS['CH2_ben_amorf'], 5], dtype = 'float')
c23_init_p2 = np.array([1, SIGNAL_SHIFTS['CH2_ben_cryst'], 5], dtype = 'float')
c23_init_p3 = np.array([1, SIGNAL_SHIFTS['CH2_twist_amorf'], 5], dtype = 'float')
c23_init_p4 = np.array([1, 1470, 1], dtype = 'float')
c23_init_p5 = np.array([1, 1370, 1], dtype = 'float')
c23_init_p6 = np.array([1, 1350, 1], dtype = 'float')
c23_init_p7 = np.array([1, 1314, 1], dtype = 'float')

c23_bounds = (c23_bounds_low, c23_bounds_high)
c23_pInit = np.concatenate((c23_init_p1, c23_init_p2, c23_init_p3, c23_init_p4, c23_init_p5, c23_init_p6, c23_init_p7), axis = None)
#############################################################################################################################################
