import funcAnalysis as fan
import numpy as np


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
