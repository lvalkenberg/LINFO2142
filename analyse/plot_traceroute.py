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
        dic_Y["others"] = np.zeros(len(dic[serv].keys())+1)
        
        plt.title("Traceroute analysis for server "+serv)
        for index in dic[serv].keys():

            for hop in dic[serv][index].keys():

                if (dic[serv][index][hop] < (get_tot_index_occ(dic[serv][index]) * 0.10)):     # if less than 15% of total occurence then consider it as "others"
                    new_OTHERS = np.zeros(len(dic[serv].keys())+1)
                    new_OTHERS[index] = dic[serv][index][hop] #/ get_tot_index_occ(dic[serv][index])
                    dic_Y["others"] = np.array(dic_Y["others"]) + np.array(new_OTHERS)

                else:
                    if hop not in dic_Y:
                        dic_Y[hop] = np.zeros(len(dic[serv].keys())+1)
                    
                    thisY = np.zeros(len(dic[serv].keys())+1)
                    thisY[index] =  dic[serv][index][hop] #/ get_tot_index_occ(dic[serv][index])
                    dic_Y[hop] =  np.array(dic_Y[hop]) + np.array(thisY)
        
        plot_colors = ["dimgray", "silver", "indianred", "maroon", "red", "coral", "sienna", "sandybrown", "orange", "gold", "olive", "yellow", 
                        "green", "forestgreen", "lime", "turquoise", "deepskyblue", "blue", "indigo", "fuchsia", "hotpink", "lightgreen", "darkred"]
        
        random.shuffle(plot_colors)
        i = random.randint(0,len(plot_colors)-1)
        old_bottom = np.zeros(len(dic[serv].keys())+1)
        for key in dic_Y.keys():

            if key=="others":
                plt.bar(X, np.array(dic_Y[key]), label=key, bottom=old_bottom, color="black")
            else:
                plt.bar(X, np.array(dic_Y[key]), label=key, bottom=old_bottom, color=plot_colors[i%len(plot_colors)])
            i+=1

            old_bottom+=np.array(dic_Y[key])

        plt.legend(title="IP adress of the routers")
        plt.xlabel("Hop index")
        plt.ylabel("Occurence of the router")
        plt.xlim(0.5)
        plt.show()

        

"""
Remarques:

On a pas des diagrammes en batonnet de la même hauteur partout car on a preprocesser les paths retiré (*,*)
"""