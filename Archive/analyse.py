# -*- coding: utf-8 -*-
"""
Created on Wed Nov 24 08:29:25 2021

@author: louis
"""

from typing import Counter
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
        

def traceroute_analyse(file="Mesures/traceroute_measure.csv"):
    
    dic = {}

    trace_csv = pd.read_csv(file)
    
    serveurs =trace_csv["Serveur"]
    traceroute = trace_csv["Traceroute"]
    date = trace_csv["Date"]

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

            if dic[serv][d] not in occurence:
                occurence[serv] = (dic[serv][d], 1)
            
            else:
                occurence[serv] = (dic[serv][d], occurence[serv][1] + 1)
        
        print("Pour le serveur {0} il y a {1} chemins différents".format(serv, len(occurence[serv]))) 

            

    

traceroute_analyse()


ping_csv = pd.read_csv("../data/measure_ping.csv")

mask = ping_csv["Destination"]=="speedtest.uztelecom.uz"
uztelecom_ping = ping_csv.loc[mask, ["Ping"]]
mean_uztelecom_ping = mean_ping(np.array(uztelecom_ping["Ping"]))

plt.plot(mean_uztelecom_ping)
plt.ylabel('Mean ping to speedtest.uztelecom.uz')
plt.show()
