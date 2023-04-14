import matplotlib.pyplot as plt
import matplotlib as mlt
import numpy as np
import src.interface as inter
# mlt.use('SVG')

def getCrystalData(filePath):
  mlt.use('SVG')
  dataFile = np.loadtxt(filePath, delimiter = '\t')
  cryst_1 = np.array(dataFile[:, 0], dtype = 'float')
  cryst_2 = np.array(dataFile[:, 1], dtype = 'float')
  cryst_3 = np.array(dataFile[:, 2], dtype = 'float')
  cryst_4 = np.array(dataFile[:, 3], dtype = 'float')

  fig, ax = plt.subplots(1, 1)
  bin_num = 100
  n, bins, patches = ax.hist(cryst_1, bin_num, density = False, histtype = 'stepfilled', cumulative = False)

  plt.savefig('cryst_1_raw_n2.svg')
  plt.close()

def barCharts():
    path = input("Directory path: ")
    fileList = inter.getFilenameList(path)
    data = [] 
    for fileName in fileList:
        file = open(path + fileName, "r")
        data = np.loadtxt(file)
        file.close()
        minData = min(data)
        maxData = max(data)
        if(abs(minData) > abs(maxData)):
            maxRange = minData
        else:
            maxRange = maxData
        ranges = []
        rangesNum = 4
        differences = abs(maxRange) / rangesNum
        for i in range(0,rangesNum):
            ranges.append([i*differences, (i+1) * differences])
        bars = []
        for i in range(rangesNum):
            bars.append([])

        for record in data:
            for i in range(len(ranges)):
                if((abs(record) > ranges[i][0]) and (abs(record) <= ranges[i][1])):
                    bars[i].append(abs(record))
                else:
                    continue
        barCounts = []
        for bar in bars:
            barCounts.append(len(bar))
        rangesStrings = []
        for diff in ranges:
            rangesStrings.append("{:.2f}".format(diff[0]) + " - " + str("{:.2f}".format(diff[1])))
        print(barCounts)
        plt.figure()
        plt.bar(rangesStrings, barCounts)
        plt.savefig(fileName + "_barChart.png")
        plt.close()

      
def plotBarChart(title, xTicks, counts):
    fig, ax = plt.subplots()
    fig.suptitle(title)
    ax.set_ylabel("Liczba")
    plt.bar(xTicks, counts)
    plt.savefig(title + ".png")
    plt.close()
    
