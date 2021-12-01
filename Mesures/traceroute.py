import csv
import sys
import os


def process(input, output_writer):

    date = ""    
    path = []
    values = []

    index = 0
    for string_line in input:
        
        if string_line[0:4] == "2021":
            
            if index != 0:
                output_writer.writerow([date[0:-1], serveur, path, values]) #Write the last line of the preceding date
            
            date = string_line
            index = -1      # To avoid that the next line (beginning with "traceroute ...") is written in the output file
            
        
        else:
            line = string_line.split()

            if line == []:
                continue
            
            if line[0] == "traceroute":
                
                if index != 0:          #Pour éviter d'écrire le 1e traceroute sans son chemin
                    output_writer.writerow([date[0:-1], serveur, path, values])
                
                serveur = line[2] + " " + line[3][0:-1]
                ip_serv = line[3][1:-2]
                path = []
                values = []
            

            elif line[1] == "*" and line[2] == "*" and line[3] == "*":        #serveur injoignibale
                path.append(("*", "*"))
                values.append(("-1", "-1", "-1"))
            
            elif line[1] == "*" and line[2] == "*" and line[3] != "*":
                path.append((line[4][1:-1], line[3]))
                values.append(("-1", "-1", line[5]))

            elif line[1] == "*" and line[2] != "*":
                path.append(( line[3][1:-1], line[2]))
                values.append(("-1", line[4], line[6] ))

            else:
                
                if ip_serv in string_line:      
                    path.append((ip_serv, ip_serv))
                else:
                    path.append((line[2][1:-1], line[1])) #(IP, Hostname) with IP without '(' & ')'
                
                #Different possible cases :
                # 1. "*", "*", mesures1, "ms"
                # 2. "*", mesures1, "ms", mesures2, "ms"
                # 3. mesures1, "ms", mesures2, "ms", mesures3, "ms"
                # 4. mesures1, "ms", mesures2, "ms", source2, (IP2), mesures3, "ms"
                # 5. mesures1, "ms", {special symbol: X!, S!, etc..}, mesures2, "ms"   (=> special symbols can be anywhere)
                # 6. mesures1, "ms", "*", "*"
                # 7. mesures1, "ms", mesures2, "ms", "*"
                # 8. mesures1, "ms", "*", mesures2, "ms"
                #   .   .   .
                #   .   .   .
                # We conserv only case 3

                # A value of -1 means that a problem occured : no mesure, *, source2, special symbol, etc ..


                l = []
                try:
                    float(line[3])
                    l.append(line[3])
                    try:
                        float(line[5])
                        l.append(line[5])
                        try:
                            float(line[7])
                            l.append(line[7])   # Si on fait 3 probes / adresse IP

                        except:
                            l.append("-1")
                    
                    except:
                        l.append("-1")
                        l.append("-1")
                
                except:
                    for number in line[1:]:

                        try:
                            float(number)
                            l.append(number)
                        
                        except:
                            continue
                
                    while len(l) != 3:
                        l.append("-1")  #Demande trop de travail pour pas grand chose => -1 = erreur

            
                if (len(l) != 3):
                    print(l)
                    return
                
                values.append((l[0], l[1], l[2]))
        
        index +=1
    
    output_writer.writerow([date[0:-1], serveur, path, values])


def main(input, output):
    """
        @input = input file, with all the traceroute measure
        @output = output file (of type .csv)
    """
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