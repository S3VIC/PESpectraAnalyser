import sys

# custom imports
import src.noisered as noise
import src.visualiser as vis

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    vis.plot_spectra(sys.argv[1])
    noise.test_function("Hello world!")
