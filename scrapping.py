import requests
from bs4 import BeautifulSoup
import csv

f = open('weather.csv', 'a')

url = "https://www.meteobelgique.be/previsions-meteo-belgique/heure-par-heure/1348/louvain-la-neuve"

source = requests.get(url)

datas = []

# Ajoute les donnée de la prochaine heur dans le fichier f
if(source.ok):
    soup = BeautifulSoup(source.text, 'lxml')
    next_hour = soup.find_all('tr')[1]
    next_hour = next_hour.find_all('td')
    for td in next_hour:
        if(td.find('img') != None):
            datas.append(td.find('img')['src'])
            # print(td.find('img')['src'])
        else:
            datas.append(td.text)
            # print(td.text)
            
writer = csv.writer(f)
writer.writerow(datas)

f.close() 