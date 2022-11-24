import matplotlib.pyplot as plt
import src.params.parameters as par
import numpy as np
import src.analyzer as an
import src.params.parameters as par


def set_plotting_params(graph, plotRange):
    plt.grid(par.GRID_VISIBILITY)
    plt.xlim(plotRange)
    graph.invert_xaxis()
    plt.ylabel(par.Y_LABEL)
    plt.xlabel(par.X_LABEL)
    ax = plt.gca()  # Gets available axes from figure matching the given keyword args, or creates a new one.
    ax.axes.yaxis.set_ticklabels([])    # Sets tick-labels blank


def set_derivative_params(graph):
    #   plt.grid(gridVisibility)
    plt.xlim(par.X_RANGE)
    graph.invert_xaxis()
    plt.ylabel(par.DERIVATIVE_Y_LABEL)
    plt.xlabel(par.X_LABEL)


def single_plot(file):
    data = np.loadtxt(file, delimiter=',')
    figure, ax = plt.subplots()
    #print(data[:, 0])
    x = data[:, 0]
    y = data[:, 1]
    set_plotting_params(ax, par.X_RANGE_full)
    ax.plot(x, y, linewidth=1.5)
    #ax.plot(par.PEAK_1, (np.amax(y) -1500, np.amax(y) - 1840), linewidth=2)
    #ax.plot(par.PEAK_2, (np.amax(y) - 1500, np.amax(y) - 1840), linewidth=2)
    #ax.plot(par.PEAK_3, (np.amax(y) - 1500, np.amax(y) - 1840), linewidth=2)
    #ax.plot(par.PEAK_4, (np.amax(y) - 1200, np.amax(y) - 1340), linewidth=2)
    #ax.plot(par.PEAK_5, (np.amax(y) - 1200, np.amax(y) - 1340), linewidth=2)
    #ax.plot(par.PEAK_6, (np.amax(y) - 1200, np.amax(y) - 1340), linewidth=2)
    #ax.plot(par.PEAK_7, (np.amax(y) - 1200, np.amax(y) - 1340), linewidth=2)
    #ax.plot(par.PEAK_8, (np.amax(y) - 1600, np.amax(y) - 1940), linewidth=2)
    #ax.plot(par.PEAK_9, (np.amax(y) - 1600, np.amax(y) - 1940), linewidth=2)
    #ax.plot(par.PEAK_10, (np.amax(y) - 1600, np.amax(y) - 1940), linewidth=2)
    plt.legend(['Raman spectra', '1', '2', '3', '4', '5', '6', '7', '8', '9'], prop={'size': 6})
    #plt.legend(['Raman spectra'])
    plt.savefig(file[:-3], dpi=300)  # saving figure to png file with certain dpi and closing plot
    #set_plotting_params(ax, par.X_RANGE_check_1)
    #plt.savefig(file[:-4] + "check_1.", dpi=300)  # saving figure to png file with certain dpi and closing plot
    #set_plotting_params(ax, par.X_RANGE_check_2)
    #plt.savefig(file[:-4] + "check_2.", dpi=300)  # saving figure to png file with certain dpi and closing plot
    plt.close()


def plot_spectra(path):
    file_list = an.get_file_names(path)
    for file in file_list:
        single_plot(path + file)
