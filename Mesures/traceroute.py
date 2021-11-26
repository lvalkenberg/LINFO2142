import csv
import sys
import os

def process(input, output_writer):

    date = input.readline()

    path = []
    values = []

    index = 0
    for line in input:
        try:

            line = line.split()

            if line[0] == "traceroute":
                
                if index != 0:          #Pour éviter d'écrire le 1e traceroute sans son chemin
                    output_writer.writerow([date[0:-1], serveur, path, values])
                
                serveur = line[2]
                path = []
                values = []

            elif line[1] == "*" and line[2] == "*" and line[3] == "*":        #serveur injoignibale
                path.append(("*", "*"))
                values.append(("*", "*", "*"))
            
            elif line[1] == "*" and line[2] == "*" and line[3] != "*":
                path.append((line[3], line[4][1:-1]))
                values.append(("*", "*", line[5].replace(",", ".")[0:-2]))

            elif line[1] == "*" and line[2] != "*":
                path.append((line[2], line[3][1:-1]))
                values.append(("*", line[4].replace(",", ".")[0:-2], line[5].replace(",",".")[0:-2] ))

            else:
                path.append((line[1], line[2][1:-1])) #pour pas avoir les ( )
                values.append((line[3].replace(",", ".")[0:-2], line[4].replace(",",".")[0:-2], line[5].replace(",", ".")[0:-2]))   # Si on fait 3 probes / adresse IP
        
        
        except Exception as e:
            print(e)
            continue

        index +=1
    
    output_writer.writerow([date[0:-1], serveur, path, values])


def main(input, output):
    try:
        with open(input, "r") as input_file:

            if(os.path.isfile(output)):
                open_type = "a"
            else:
                open_type = "w"
                        
            with open(output, open_type, newline='') as output_file:
                
                writer = csv.writer(output_file)
                
                if(open_type == "w"):
                    writer.writerow(["Date", "Serveur", "Traceroute", "Values"]) #Traceroute = [(adresse ip, hostname)]; Values = [time in [ms] ] !!
                

                process(input_file, writer)

            

    except Exception as e:
        print(e)
        return -1;

    return 0

if len(sys.argv) != 3:
    print("ERROR : wrong format !")
    print('You must enter : python3 traceroute.py {inpute file} {output .csv file}')
else:
    main(sys.argv[1], sys.argv[2])