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

"""
    Lance les diff�rentes mesures
"""
def main(hours, output_file, one_time=0):

    launch()  #launch web-scrapping

    end =  datetime.now() + timedelta(hours=hours)
    
    # Open type : happend if only one execution or create a new file
    if(one_time != 0):
        open_type = "a"
    else:
        open_type = "w"
    
    with open(output_file, open_type, newline='') as file:
        writer = csv.writer(file)
        if(open_type == "w"):
            writer.writerow(['Date', 'Destination', 'Ping'])

        while datetime.now() < end :
            
            dic = {}
            for j in range(10):
                res = Measurement(destinations)
                
                for a,b in res:

                    if a in dic and b != None:
                        dic[a] = (dic[a][0] + b, dic[a][1] +1)    
                    elif a not in dic and b != None:
                        dic[a] = (b, 1)
                    else:
                        continue #cas ou b (le ping) est None
            
            now = datetime.now()

            for key, value in dic.items():
                writer.writerow([now, key, value[0]/value[1]])
            
            file.flush()
            
            if(one_time != 0): # Exectute the script only one time
                return 0
            
            time.sleep(6*60)

    

    return 0


if len(sys.argv) != 3 and len(sys.argv) != 4:
    print("ERROR : wrong format !")
    print('You must enter : python3 MySCript.py {number of hours} {output file.csv} {execute only one time si != 0, default=0}')

else:
    if len(sys.argv) == 3:
        main(int(sys.argv[1]), sys.argv[2])
    if len(sys.argv) == 4:
        main(int(sys.argv[1]), sys.argv[2], sys.argv[3])
    