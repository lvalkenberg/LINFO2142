from ping3 import ping
import dns.resolver

#destination = ["www.starlink.be", "www.starlink.fr", "www.starlink.com"]
destinations = ["iperf.par2.as49434.net", "iperf.biznetnetworks.com", "speedtest-iperf-akl.vetta.online", "iperf.scottlinux.com" ] 
                 #Ile de France,                 Indonesia,                  Nouvelle-Zélande,                    USA

def MyPing(dest):

    try:
        result = ping(dest)
        
        print("Ping {0} : {1} ms".format(dest, result))
        return 0
    
    except:
        print("PING ERROR")
        return -1


def MyDns(dest):

    try: 
        result = dns.resolver.query(dest, 'A')

        for ipval in result:
            print("DNS ", dest, " : ", ipval.to_text())
        return 0
                    
    except:
        print("DNS ERROR")
        return -1


def Measurement(destinations):
    
    for dest in destinations:
        MyPing(dest)
        MyDns(dest)
        print("\n")

Measurement(destinations)