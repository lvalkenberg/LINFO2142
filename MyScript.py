"""
Script qui run en continu pendant un certain nombre d'heure X donné en argument
Toutes les 6 minutes il va réaliser une séance de mesures.
Une séance de mesure consiste à mesurer la latence (PING) en prenant une moyenne sur 10 valeurs.
Après avoir effectué la séance de mesure, le script écrit le résultat dans le fichier "mesures.csv" en ajoutant le moment de la mesure
"""
from web_scrapping import *
from MyMeasure import *
from datetime import *
from Hour import *
import time
import sys
import csv


def main(hours, output_file):

    end =  datetime.now() + timedelta(hours=hours)
    
    with open(output_file, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Date', 'Destination', 'Ping'])

        i = 0
        while datetime.now() != end and i < 2:
            
            dic = {}
            for j in range(10):
                res = Measurement(destinations)
                
                for a,b in res:
                    if a == None or b == None:
                        print("UNEXPECTED NONE")
                        continue

                    if a in dic:
                        dic[a] += b
                    else:
                        dic[a] = b
            
            now = datetime.now()
            for key, value in dic.items():
                writer.writerow([now, key, value/10])
            
            time.sleep(6+60)
            
            
            i+=1 #enlever le i 

    

    return 0


if len(sys.argv) != 3 :
    print("ERROR : wrong format !")
    print('You must enter : python3 MySCript.py {number of hours} {output file.csv}')

else:
    main(int(sys.argv[1]), sys.argv[2])
    