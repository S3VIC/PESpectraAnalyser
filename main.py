#!/usr/bin/python3
import sys
# custom imports
# import src.visualiser as vis
import matplotlib as mlt
import matplotlib.pyplot as plt
import numpy as np
import src.interface as inter
            
def justPlot(fileName):
    dataFile = open(fileName, "r")
    data = np.loadtxt(dataFile, delimiter=",", dtype="float")
    x = data[:,0]
    y = data[:,1]
    plt.plot(x,y)
    plt.savefig("test2.svg")


if __name__ == '__main__':
    inter.mainMenu()
#    inter.actionChoice(sys.argv[1])
#  print("Hello world!")/A
#    justPlot(sys.argv[1])
