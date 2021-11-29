# -*- coding: utf-8 -*-
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


#def traceroute_analyse(file="../Mesures/traceroute_measure.csv"):
def traceroute_analyse(file="../Mesures/training.csv", outputfile="traceroute_analyse.txt"):  

    with open(outputfile, "a") as output:

        serv2path_date = {}  #<Serveurs, <path, [date]>>
        serv2path_hour = {}  #<Serveurs, <path, [hour]>>     => To find pattern in the path according to the hours
        
        trace_csv = pd.read_csv(file)
        
        date = trace_csv["Date"]
        serveurs =trace_csv["Serveur"]
        traceroute = trace_csv["Traceroute"]


        # ACCORDING TO THE DATE
        for i in range(len(date)):
            
            d = date[i]
            serv = serveurs[i]
            path = traceroute[i]

            if serv in serv2path_date:

                if path in serv2path_date[serv]:
                    serv2path_date[serv][path].append(d)
                else:
                    serv2path_date[serv][path] = [d]

            else:

                serv2path_date[serv] = {}
                serv2path_date[serv][path] = [d]
        
        # ACCORDING TO THE HOUR
        for i in range(len(date)):
            
            d = date[i]
            hour = d.split()[1].split(":")[0]
            serv = serveurs[i]
            path = traceroute[i]

            if serv in serv2path_hour:

                if path in serv2path_hour[serv]:
                    serv2path_hour[serv][path].append(hour)
                else:
                    serv2path_hour[serv][path] = [hour]

            else:

                serv2path_hour[serv] = {}
                serv2path_hour[serv][path] = [hour]


        # DIFFERENT PATH IN FUNCTION OF THE DATE
        output.write("="*250+"\n")
        output.write("DIFFERENT PATH IN FUNCTION OF THE DATE\n")
        for serv in serv2path_date.keys():

            output.write("="*250+"\n")
            output.write("Pour le serveur {0}, il y a {1} chemins différents :\n".format(serv, len(serv2path_date[serv].keys())))

            for path in serv2path_date[serv].keys():
                
                output.write("{0} with {1} occurences.\n".format(path, len(serv2path_date[serv][path])))
        

        # DIFFERENT PATH IN FUNCTION OF THE HOUR
        output.write("="*250+"\n")
        output.write("DIFFERENT PATH IN FUNCTION OF THE HOUR\n")
        for serv in serv2path_hour.keys():

            output.write("="*250+"\n")
            output.write("Pour le serveur {0}, il y a {1} chemins différents :\n".format(serv, len(serv2path_hour[serv].keys())))

            for path in serv2path_hour[serv].keys():
                
                output.write("{0} with {1} occurences.\n".format(path, len(serv2path_hour[serv][path])))
        

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
