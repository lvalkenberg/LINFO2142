from matplotlib import colors
import matplotlib.pyplot as plt
import numpy as np
import random

def get_tot_index_occ(dic):
    # dic = <path, occurence>

    tot = 0
    for key in dic.keys():
        tot += dic[key]
    
    return tot


def plot_traceroute_path_by_hop(dic):
    #dic = <Serveur, <Index, <path, occurence>>>

    for serv in dic.keys():

        dic_Y = {}      #<hop, Y>

        X = [i for i in range(len(dic[serv].keys())+1)]          # Hop index
        Y = [0 for i in range(len(dic[serv].keys())+1)]          # % of each different hop

        dic_Y["others"] = Y #Add "others" parametre for rare hop
    
        
        plt.title("Traceroute analysis for server "+serv)
        OTHERS = np.array([0 for i in range(len(dic[serv].keys()))])
        for index in dic[serv].keys():

            for hop in dic[serv][index].keys():

                if (dic[serv][index][hop] < get_tot_index_occ(dic[serv][index]) * 0.15):     # if less than 25% of total occurence then consider it as "others"
                    new_OTHERS = Y
                    new_OTHERS[index] = dic[serv][index][hop]
                    dic_Y["others"] = np.array(dic_Y["others"]) + np.array(new_OTHERS)

                else:
                    if hop not in dic_Y:
                        dic_Y[hop] = Y
                    
                    thisY = Y
                    thisY[index] =  dic[serv][index][hop]
                    dic_Y[hop] =  np.array(dic_Y[hop]) + np.array(thisY)
        
        #plot_colors = ["red", "yellow", "green", "blue", "orange", "grey", "pink"]
        plot_colors = ["dimgray", "silver", "indianred", "maroon", "red", "coral", "sienna", "sandybrown", "orange", "gold", "olive", "yellow", "lawngreen", 
                        "green", "forestgreen", "lime", "turquoise", "deepskyblue", "blue", "indigo", "fuchsia", "hotpink"]
        random.shuffle(plot_colors)
        plt.bar(X, np.array(dic_Y["others"]), label="others", color="black")
        i = 0
        for key in dic_Y.keys():
            if key != "others":
                thisY = []
                for val in  dic_Y[key]:
                    if val > 10:
                        thisY.append(val)
                    else:
                        thisY.append(0)

                plt.bar(X, np.array(thisY), label=key, color=plot_colors[i%len(plot_colors)])
                i+=1

        print(dic_Y.items())
        plt.legend()
        plt.xlim(0.5)
        plt.show()

        

"""
Remarques:

On a pas des diagrammes en batonnet de la même hauteur partout car on a preprocesser les paths retiré (*,*)
"""