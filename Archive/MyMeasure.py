from ping3 import ping
import dns.resolver
import speedtest #https://www.speedtest.net/fr

#destination = ["www.starlink.be", "www.starlink.fr", "www.starlink.com"]
#localisation = [Ile de france, Indonesie, (Nouvelle Zelande#"speedtest-iperf-akl.vetta.online" => TJS none ...), USA, Estonie, Uzbekistan]
destinations = ["iperf.par2.as49434.net", "iperf.biznetnetworks.com", "iperf.scottlinux.com", "iperf.eenet.ee", 
                "speedtest.uztelecom.uz" ] 

"""
    Send ping to dest and return none in case of timeout (20s default)
"""
def MyPing(dest, to=4):
    try:
        return ping(dest, timeout=to) #¶return none in case of timeout
    
    except:
        print("PING ERROR")
        return "PING ERROR"

"""
    Make DNS request to dest and return a string
"""
def MyDns(dest):

    try: 
        result = dns.resolver.query(dest, 'A')
        ans = ""
        for ipval in result:
            ans += "DNS " + dest + " : " + ipval.to_text()
        
        return ans
                    
    except:
        return "DNS ERROR"

"""
    Run bandwith mesurement with speedtest on the closest (distance (km)) available server
    
    return exemple :
        {'download': 45203916.74099848, 'upload': 0, 'ping': 41.488, 'server': {'url': 'http://ookla2.ictvanloon.nl:8080/speedtest/upload.php', 'lat': '51.4381', 'lon': '5.4752', 'name': 'Eindhoven', 'country': 'Netherlands', 'cc': 'NL', 'sponsor': 'ICTvanLoon', 'id': '45519', 'host': 'ookla2.ictvanloon.nl:8080', 'd': 107.95631998641474, 'latency': 41.488}, 'timestamp': '2021-11-11T09:35:42.333814Z', 'bytes_sent': 0, 'bytes_received': 56774196, 'share': None, 'client': {'ip': '81.246.166.119', 'lat': '50.6361', 'lon': '4.605', 'isp': 'Proximus', 'isprating': '3.7', 'rating': '0', 'ispdlavg': '0', 'ispulavg': '0', 'loggedin': '0', 'country': 'BE'}}
"""    
def bw_speedtest():
    # utility
    def get_lower_key(dic):
        min_key = None
        for key in dic.keys():
            if(min_key == None or key < min_key):
                min_key = key
        return min_key

    s = speedtest.Speedtest()
    servers = s.get_servers()
    opt = get_lower_key(servers)
    s.servers = {}
    s.servers[opt] = servers[opt]
    s.download() #b/s
    s.upload() #b/s
    return s.results

def Measurement(destinations):
    
    res = []
    for dest in destinations:
        a  = (dest,MyPing(dest))  #Comment traiter les "None" ? -> timeout, packet lost
        res.append(a)

    return res
