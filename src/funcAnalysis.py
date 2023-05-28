#library containt functional analysis methods


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mlt
from scipy.optimize import curve_fit


def rectIntegLeft(x, y):
    if(len(x) != len(y)):
        assert False, "Size of x and y do not match"

    else:
        area = 0
        for i in range(len(x) - 1):
            a = x[i + 1] - x[i]
            b = y[i]
            area = area + a * b 
        
        return area

 

def rectIntegRight(x, y):
    if(len(x) != len(y)):
        assert False, "Size of x and y do not match"

    else:
        area = 0
        for i in range(len(x) - 1):
            a = x[i + 1] - x[i]
            b = y[i + 1]
            area = area + a * b 
        
        return area


def trapInteg(x, y):
    if(len(x) != len(y)):
        assert False, "Size of x and y do not match"

    else:
        area = 0
        for i in range(len(x) - 1):
            h = x[i + 1] - x[i]
            a = y[i + 1]
            b = y[i]
            area = area + h * (a + b)
        return area / 2




def cryst1GaussModel(x, a1, b1, c1, a2, b2, c2, a3, b3, c3, a4, b4, c4):
    return a1 * np.exp( - (x - b1)**2 / 2 / c1**2) + a2 * np.exp( - (x - b2)**2 / 2 /c2**2) + a3 * np.exp(- (x - b3)**2 / 2 / c3**2) + a4 * np.exp(- (x - b4)**2 / 2 / c4**2)


def cryst134GaussModel1(x, a1, b1, c1, a2, b2, c2, a3, c3, a4, b4, c4):
    return a1 * np.exp( - (x - b1)**2 / 2 / c1**2) + a2 * np.exp( - (x - b2)**2 / 2 /c2**2) + a3 * np.exp(- (x - 2905)**2 / 2 / c3**2) + a4 * np.exp(- (x - b4)**2 / 2 / c4**2)


def cryst2GaussModel(x, a1, b1, c1, a2, b2, c2, a3, b3):
    return a1 * np.exp( - (x - b1)**2 / 2 / c1**2) + a2 * np.exp( - (x - b2)**2 / 2 /c2**2) + a3 * np.exp(- (x - b3)**2 / 2 / c3**2)

def GaussModel(x, a, b, c):
    return a * np.exp( - (x - b)**2 / 2 / c**2)


