from matplotlib import colors
import matplotlib.pyplot as plt
import numpy as np

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

        X = [i+1 for i in range(len(dic[serv].keys()))]          # Hop index
        Y = [0 for i in range(len(dic[serv].keys()))]          # % of each different hop

        dic_Y["others"] = Y #Add "others" parametre for rare hop
    
        plt.figure(figsize=(9,7))
        plt.title("Traceroute analysis for server "+serv)
        OTHERS = np.array([0 for i in range(len(dic[serv].keys()))])
        for index in dic[serv].keys():
            
            for hop in dic[serv][index].keys():

                if (dic[serv][index][hop] < get_tot_index_occ(dic[serv][index]) * 0.15):     # if less than 25% of total occurence then consider it as "others"
                    new_OTHERS = Y
                    new_OTHERS[index] = dic[serv][index][hop]
                    dic_Y["others"] += np.array(new_OTHERS)

                else:
                    if hop not in dic_Y:
                        dic_Y[hop] = Y
                    
                    thisY = Y
                    thisY[index] =  dic[serv][index][hop]
                    dic_Y[hop] += np.array(thisY)
        

        plt.bar(X, np.array(dic_Y["others"]), label="others", color="black")
        for key in dic_Y.keys():
            if key != "others":
                plt.bar(X, np.array(dic_Y[key]), label=key)

        plt.legend()
        plt.ylim(4)
        plt.show()

        

"""
Remarques:

On a pas des diagrammes en batonnet de la même hauteur partout car on a preprocesser les paths retiré (*,*)
"""