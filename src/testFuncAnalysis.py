import funcAnalysis as fan
import numpy as np
import os

def getFileList(path):
    fileList = np.array([])
    for filename in os.listdir(path):
        if filename[-3:].upper() == "CSV":
            temp_file = os.path.join(path, filename)
            if os.path.isfile(temp_file):
                fileList = np.append(fileList, filename)
    fileList = np.sort(fileList)
    return fileList



if __name__=='__main__':
    print("Hello")
    x = np.linspace(0, np.pi, 5000)
    y = np.sin(x)
    area = fan.rectIntegLeft(x, y)
    area2 = fan.rectIntegRight(x, y)
    area3 = fan.trapInteg(x, y)
    print(area)
    print(area2)
    print(area3)
    path = input("Path: ")
    fileList = getFileList(path)
    for fileName in fileList:
        file = open(path + fileName, 'r')
        data = np.loadtxt(file, delimiter = ',')
        x = data[:, 0]
        y = data[:, 1]
        area4 = fan.rectIntegLeft(x, y)
        area5 = fan.rectIntegRight(x, y)
        area6 = fan.trapInteg(x, y)

        print(area4)
        print(area5)
        print(area6)
    
