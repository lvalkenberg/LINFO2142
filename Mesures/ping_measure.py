# -*- coding: utf-8 -*-
"""
Created on Fri Nov 12 12:33:07 2021

@author: louis
"""
import time
from datetime import *
import sys
import csv
import os
from ping3 import ping

#"iperf.par2.as49434.net"
destinations = [ "iperf.biznetnetworks.com", "iperf.scottlinux.com", "iperf.eenet.ee", 
                "speedtest.uztelecom.uz", "lille.testdebit.info", "speedtest.serverius.net" ] 

"""
    Send ping to dest and return none in case of timeout (20s default)
"""
def Ping(dest, to=None):

    if(to == None):
        return ping(dest) #¶return none in case of timeout
    else:
        return ping(dest, to)
    
def main(output_file, number):

    # Open type : happend if only one execution or create a new file
    if(os.path.isfile(output_file)):
        open_type = "a"
    else:
        open_type = "w"
    
    with open(output_file, open_type, newline='') as file:
        writer = csv.writer(file)
        if(open_type == "w"):
            writer.writerow(['Date', 'Destination', 'Ping', 'Lost', 'Measurment', 'Error'])

        for dest in destinations:
            global_delay = 0
            nb_mesures = 0
            lost = 0
            error = 0
            pings_tab = []
            for i in range(number):
                try:
                    ping_val= ping(dest)
                    if(ping_val != None and ping_val != False):
                        global_delay += ping_val
                        pings_tab.append(ping_val)
                        nb_mesures += 1
                    elif(ping_val == None): #timeout
                        pings_tab.append('NaN')
                        lost += 1
                    else:
                        error += 1
                except Exception as e:
                    print("PING ERROR")
                    print(e)

        
            now = datetime.now()
            writer.writerow([now, dest, pings_tab, lost/number, number, error])
            # if(nb_mesures != 0):
            #     writer.writerow([now, dest, global_delay/nb_mesures, lost/number])
            # else:
            #      writer.writerow([now, dest, 'NaN', lost/number])
        
        file.flush()

    

    return 0


if len(sys.argv) != 3:
    print("ERROR : wrong format !")
    print('You must enter : python3 ping_measure.py {output file.csv} {number of ping on each servers}')
else:
    main(sys.argv[1], int(sys.argv[2]))

    
