from ping3 import ping
import dns.resolver

#destination = ["www.starlink.be", "www.starlink.fr", "www.starlink.com"]
#localisation = [Ile de france, Indonesie, (Nouvelle Zelande#"speedtest-iperf-akl.vetta.online" => TJS none ...), USA, Estonie, Uzbekistan]
destinations = ["iperf.par2.as49434.net", "iperf.biznetnetworks.com", "iperf.scottlinux.com", "iperf.eenet.ee", 
                "speedtest.uztelecom.uz" ] 

def MyPing(dest):

    try:
        return ping(dest, timeout=10) #¶return none in case of timeout
    
    except:
        return "PING ERROR"


def MyDns(dest):

    try: 
        result = dns.resolver.query(dest, 'A')
        ans = ""
        for ipval in result:
            ans += "DNS " + dest + " : " + ipval.to_text()
        
        return ans
                    
    except:
        return "DNS ERROR"


def Measurement(destinations):
    
    res = []
    for dest in destinations:
        a  = (dest,MyPing(dest))  #Comment traiter les "None" ?
        res.append(a)

    return res

