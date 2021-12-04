from datetime import *
import sys
import csv
import os
import speedtest #https://www.speedtest.net/fr
import os
import time
import random

"""
    Run bandwith mesurement with speedtest on the closest (distance (km)) available server
    
    return exemple :
        {'download': 45203916.74099848, 'upload': 0, 'ping': 41.488, 'server': {'url': 'http://ookla2.ictvanloon.nl:8080/speedtest/upload.php', 'lat': '51.4381', 'lon': '5.4752', 'name': 'Eindhoven', 'country': 'Netherlands', 'cc': 'NL', 'sponsor': 'ICTvanLoon', 'id': '45519', 'host': 'ookla2.ictvanloon.nl:8080', 'd': 107.95631998641474, 'latency': 41.488}, 'timestamp': '2021-11-11T09:35:42.333814Z', 'bytes_sent': 0, 'bytes_received': 56774196, 'share': None, 'client': {'ip': '81.246.166.119', 'lat': '50.6361', 'lon': '4.605', 'isp': 'Proximus', 'isprating': '3.7', 'rating': '0', 'ispdlavg': '0', 'ispulavg': '0', 'loggedin': '0', 'country': 'BE'}}
"""    
def bw_speedtest(t):
    # utility
    def get_lower_key(dic):
        min_key = None
        for key in dic.keys():
            if(min_key == None or key < min_key):
                min_key = key
        return min_key

    s = speedtest.Speedtest()
    if(t == 1):
        servers = s.get_servers()
        opt = get_lower_key(servers)
        s.servers = {}
        s.servers[opt] = servers[opt]
    s.download() #b/s
    s.upload() #b/s
    return s.results

def main(output_file):
    
    #time.sleep(random.randrange(90)) #wait random time betwenn 10s

    # Open type : happend if only one execution or create a new file
    if(os.path.isfile(output_file)):
        open_type = "a"
    else:
        open_type = "w"
    
    with open(output_file, open_type, newline='') as file:
        writer = csv.writer(file)
        if(open_type == "w"):
            writer.writerow(['date','country','name','host','id','download', 'upload', 'ping', 'd'])
        
        now = datetime.now()
        try:
            res = bw_speedtest(0)
            writer.writerow([now,res.server["country"],res.server["name"],res.server["host"],res.server["id"], res.download, res.upload, res.ping, res.server["d"]])
        except:
             writer.writerow([now,'NaN'])
            
        file.flush()  

    return 0


if len(sys.argv) != 2:
    print("ERROR : wrong format !")
    print('You must enter : python3 bw_measure.py {output file.csv}')
else:
    main(sys.argv[1])

    