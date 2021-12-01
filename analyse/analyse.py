# -*- coding: utf-8 -*-
from os import write
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


def process_path(path, serveur):

    answer = ""
    ip = serveur.split()[1][1:-1]

    if path[len(path)-1 -len(ip) -2: -3]!= ip:

        return answer

    for hop in path.split(","):
        if '*' not in hop:
            answer += hop
            answer += ","  #We add the "," back
    
    return answer[0:-1] #To delete the last ","

def get_hop_number(path):

    return path.count("(")


def traceroute_analyse(file="../data2/measure_traceroute.csv", outputfile="traceroute_analyse.txt"):  
    """
    1. We process the path :
        - We take only the paths who reach the server
        - We delete the ("*", "*") in the path
    """


    with open(outputfile, "a") as output:

        total_discarded_path = 0

        serv2path = {}  #<Serveurs, <path, [date]>>         => To compare all the different path
        serv2path_hour = {}  #<Serveurs, <hour, [path]>>    => To find pattern in the path according to the hours
        serv2length = {}     #<Serveurs, <length, [path]>>  => To compare the length

        trace_csv = pd.read_csv(file)
        
        date = trace_csv["Date"]
        serveurs =trace_csv["Serveur"]
        traceroute = trace_csv["Traceroute"]


        ######################################
        #          ANALYSE THE RESULTS       #
        ######################################
        
        for i in range(len(date)):

            d = date[i]
            hour = d.split()[1].split(":")[0]
            serv = serveurs[i]
            path = process_path(traceroute[i], serv)

            if path == "":
                total_discarded_path += 1
                continue


            # ACCORDING TO THE DATE
            if serv in serv2path:

                if path in serv2path[serv]:
                    serv2path[serv][path].append(d)
                else:
                    serv2path[serv][path] = [d]

            else:

                serv2path[serv] = {}
                serv2path[serv][path] = [d]
            

            #   ACCORDING TO THE HOUR
            if serv in serv2path_hour:

                if hour in serv2path_hour[serv]:
                    
                    if path not in serv2path_hour[serv][hour]:
                        serv2path_hour[serv][hour].append(path)

                else:
                    serv2path_hour[serv][hour] = [path]

            else:

                serv2path_hour[serv] = {}
                serv2path_hour[serv][hour] = [path]
        

            #   ACCORDING TO THE LENGTH
            if serv in serv2length:

                if get_hop_number(path) in serv2length[serv]:
                    serv2length[serv][get_hop_number(path)].append(path)
                
                else:
                    serv2length[serv][get_hop_number(path)] = [path]
            
            else:
                serv2length[serv] = {}
                serv2length[serv][get_hop_number(path)] = [path]






        print("Total number of discarded path : {0}".format(total_discarded_path))
        for s in serveurs.unique():
            if s not in serv2path:
                print("Server {0} is never reached !".format(s))          


        #######################################
        #           PRINT RESULTS             #
        #######################################

        output.write("="*250+"\n")
        output.write("DIFFERENT PATH IN FUNCTION OF THE DATE\n")
        output.write("="*250+"\n\n")

        for serv in serv2path.keys():

            output.write("-"*250+"\n")
            output.write("For server {0}, there are {1} different paths :\n".format(serv, len(serv2path[serv].keys())))

            for path in serv2path[serv].keys():
                
                output.write("{0} with {1} occurences.\n".format(path, len(serv2path[serv][path])))
        print("\n")
        
        output.write("="*250+"\n")
        output.write("DIFFERENT PATH IN FUNCTION OF THE HOUR\n")
        output.write("="*250+"\n")

        for serv in serv2path_hour.keys():

            output.write("-"*250+"\n")
            output.write("For server {0}:\n".format(serv))

            hours = ["00", "01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12", "13", "14", "15", "16", "17", "18", "19", "20", "21", "22", "23"]
            for h in hours:
                output.write("At {0}:00 there are {1} different paths:\n".format(h, len(serv2path_hour[serv][h]) ))
                
                #for p in serv2path_hour[serv][h]:
                #    output.write(p + "\n")
        
        output.write("="*250+"\n")
        output.write("DIFFERENT PATH IN FUNCTION OF THEIR LENGTH\n")
        output.write("="*250+"\n")
    
        for serv in serv2length.keys():

            output.write("-"*250+"\n")
            output.write("For server {0}:\n".format(serv))

            for length in serv2length[serv].keys():
                output.write("There are {0} paths of length {1}\n".format(len(serv2length[serv][length]), length ))
        
        

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
