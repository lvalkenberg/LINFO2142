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


def traceroute_analyse(file="../Mesures/traceroute_measure.csv"):
    
    dic = {}

    trace_csv = pd.read_csv(file)
    
    date = trace_csv["Date"]
    serveurs =trace_csv["Serveur"]
    traceroute = trace_csv["Traceroute"]
    

    for serv in serveurs:
        if serv not in dic:
            dic[serv] = {}
    
    for i in range(len(traceroute)):
        serv = serveurs[i]
        d = date[i]

        if d not in dic[serv]:
            dic[serv][d] = traceroute[i]

        else:
            print("Deux traceroutes pour un meme serveur et une meme date")   

    occurence = {}  #Dictionnaire< serveur, different_traceroute> où different_traceroute est un resume de toutes les tracroute du serveur
    for serv in dic.keys():
        for d in dic[serv].keys():

        #    if dic[serv][d] not in occurence:
        #        occurence[serv] = (dic[serv][d], 1)
            
        #    else:
        #        occurence[serv] = (dic[serv][d], occurence[serv][1] + 1)
        
        #print("Pour le serveur {0} il y a {1} chemins différents".format(serv, len(occurence[serv]))) 

            

    

traceroute_analyse()



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
