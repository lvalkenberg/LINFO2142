# -*- coding: utf-8 -*-
"""
Created on Wed Nov 24 08:29:25 2021

@author: louis
"""

import pandas as pd
import numpy as np
from ast import literal_eval
import matplotlib.pyplot as plt
from datetime import *

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
        
def fusion_with_weather(csv1, csv2):
    fusion = []
    index2 = 0
    for i in range(len(csv1)):
        if(index2 >= len(csv2)):
            return fusion;
        date1 = datetime.strptime(csv1[i][0][0:13], "%Y-%m-%d %H")
        date2 = datetime.strptime(csv2[index2][0][0:13], "%Y-%m-%d %H") + timedelta(hours=1)
        if(date1 == date2):
            # print(np.ndarray.tolist(csv1[i]) + np.ndarray.tolist(csv2[index2][1:]))
            fusion.append(np.ndarray.tolist(csv1[i]) + np.ndarray.tolist(csv2[index2][1:]))
        elif(date1 > date2):
            i -= 1
            index2 +=1
    return fusion

ping_csv = pd.read_csv("../data/measure_ping.csv")
bw_csv = pd.read_csv("../data/measure_bw.csv")
weather_csv = pd.read_csv("../data/measure_weather.csv")

ping_array = np.array(ping_csv)
weather_array = np.array(weather_csv)
ping_weather_array = fusion_with_weather(np.array(ping_csv), np.array(weather_csv))
print(np.unique(weather_array[:,1]))

# print(datetime.strptime(ping_array[0][0][0:13], "%Y-%m-%d %H") + timedelta(hours=8))

# mask = ping_csv["Destination"]=="speedtest.uztelecom.uz"
# uztelecom_ping = ping_csv.loc[mask, ["Ping"]]
# mean_uztelecom_ping = mean_ping(np.array(uztelecom_ping["Ping"]))

# plt.plot(mean_uztelecom_ping)
# plt.ylabel('Mean ping to speedtest.uztelecom.uz')
# plt.show()
