from datetime import *
import time
import os
import sys
import requests
from bs4 import BeautifulSoup
import csv

from urllib.request import Request, urlopen

url = "https://www.meteobelgique.be/previsions-meteo-belgique/heure-par-heure/1348/louvain-la-neuve"
headers = {
    'User-Agent': 'Mozilla/5.0',
}

"""
    Mesure weather condition for the next hour from https://www.accuweather.com/en/be/ottignies/27242/hourly-weather-forecast/27242
"""
def main(output_file):
    
    # Open type : happend if only one execution or create a new file
    if(os.path.isfile(output_file)):
        open_type = "a"
    else:
        open_type = "w"
    
    # source = req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    
    with open(output_file, open_type, newline='') as file:
        writer = csv.writer(file)
        if(open_type == "w"):
            writer.writerow(['Date', 'Condition', 'T', 'Pluie', 'Pression'])
    
        
        source = requests.get(url, headers=headers)
        
        # if couldn't get the html retry multiple times
        counter = 0
        while not source.ok:
            time.sleep(5 + counter*2) 
            counter += 1
            source = requests.get(url)
            if(counter == 1):
                print("UNABLE TO REACH THE SERVER")
                return 0;
        
        # Ajoute les donnée de la prochaine heure dans le fichier f
        if(source.ok):
            soup = BeautifulSoup(source.text, 'lxml')
            next_hour = soup.find_all('tr')[1]
            next_hour = next_hour.find_all('td')
            now = datetime.now()
            datas = [now, next_hour[1].find('img')['src'], next_hour[2].text, next_hour[3].text, next_hour[6].text]
                    
                    
        writer.writerow(datas)
        
        file.flush()
    

if len(sys.argv) != 2:
    print("ERROR : wrong format !")
    print('You must enter : python3 scrapping.py {output file.csv}')
else:
    main(sys.argv[1])