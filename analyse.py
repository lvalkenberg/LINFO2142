# -*- coding: utf-8 -*-
"""
Created on Wed Nov 24 08:29:25 2021

@author: louis
"""

import pandas as pd
import numpy as np
from ast import literal_eval
import matplotlib.pyplot as plt

"""
    Return mean for each measurement.
    Pings : a NUMPY array of string containing an array
"""
def mean_ping(pings):
    mean_ping = []
    for i in range(len(pings)):
        array = literal_eval(pings[i])
        measures = np.array(array).astype(np.double)
        mean_ping.append(np.sum(measures)/len(measures))
    return mean_ping
        

ping_csv = pd.read_csv("../data/measure_ping.csv")

mask = ping_csv["Destination"]=="speedtest.uztelecom.uz"
uztelecom_ping = ping_csv.loc[mask, ["Ping"]]
mean_uztelecom_ping = mean_ping(np.array(uztelecom_ping["Ping"]))

plt.plot(mean_uztelecom_ping)
plt.ylabel('Mean ping to speedtest.uztelecom.uz')
plt.show()
