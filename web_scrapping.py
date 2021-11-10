from bs4 import BeautifulSoup
from datetime import datetime
from Hour import *
import requests
import csv


#url = "https://www.buienradar.be/weer/Louvain-la-Neuve/BE/2792073"
url = "https://www.meteobelgique.be/previsions-meteo-belgique/heure-par-heure/1348/louvain-la-neuve"


dic_nuage = {"sun.png" : 6, "lightcloudy.png" : 5, "lightsun.png" : 4, "cloudyshower.png" : 3, "cloudy.png" : 3, 
             "mostcloudy.png" : 2, "cover.png" : 1, "lightrain.png" : 1, "lightshower.png" : 2, "rain.png" : 1,
             "thundershower.png" : 1, "shower.png" : 1, "thunderrain.png" : 1, "moon" : 0}

dic_date = {"janvier" : 1, "février" : 2, "mars" : 3, "avril" : 4, "mai" : 5, "juin" : 6, "juillet" : 7, "août" : 8,
            "septembre" : 9, "octobre" : 10, "novembre" : 11, "décembre" : 12}

def get_data(url):
    """
    @pre: url est le lien vers un site météo
    @post retourne une liste d'objet Hour(@date, @ensoleimment, @vent, @precipitation, @temperature)
    """
    
    temperature = 0
    vent = 0 
    precipitation = 0
    hours = []

    content = requests.get(url).content
    soup = BeautifulSoup(content, features="lxml")
    data = soup.findAll('tr')
    size = len(data)-1
    
    year = datetime.now().year
    
    for i in range(1,size+1):
        
        word = data[i].text.split()
        if word == [] :
            size-=1
            continue
        
        info = word[3].split(":00")

        jour = datetime(year, dic_date[str.lower(word[2])], int(word[1]), int(info[0]))        
    
        info = info[1].split("°C")
        temperature = float(info[0])
    
        if len(word) == 6:  #No rain
            vent = int(info[1])
            precipitation = 0.0
        
        elif len(word) == 7: #Rain [mm]
            vent = int(word[4][2:])
            precipitation = float(info[1])

        else:
            print("ERREUR : taille inconnue")
            return
    
    
        pic = str(data[i].find('img')).split()  #1e image is the sunshine
        pic = pic[2].strip('"').split("/")
        if pic[-2] == "night":
            pic[-1] = "moon"
        pic = pic[-1]
        
        if pic in dic_nuage:
            hours.append(Hour(jour, dic_nuage[pic], vent, precipitation, temperature))
        else:
            print("ERREUR WEBSCRAPING : IMAGE {0} NON RECONNUE".format(pic))

    return hours


def launch():

    data = get_data(url)

    with open("data.csv", 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Date', 'Sunshine', 'Wind', 'Rain', 'Temperature'])
        for i in data:
            row = str(i).split(",")
            writer.writerow([row[0], row[1], row[2], row[3], row[4]])
