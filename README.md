# LINFO2142

Mesure délai (netperf): DNS, PING, HTTP
Essayer de voir quand on change de station de base (traceroute). Base dépend de la destination
Essayer de voir si on peut pas employer les centres de Mlab comme cible.

buienradar
# Script de mesures
Le script va commencer par récupérer les données météo sur le site https://www.meteobelgique.be/previsions-meteo-belgique/heure-par-heure/1348/louvain-la-neuve. Ensuite, il va faire des mesures de ping pour différents serveurs dans le monde. Toutes les 6 minutes, 10 mesures de ping sont faites pour chaque serveur. Il va ensuite écrire dans le fichier de sortie la date de la mesure, le serveur correspondant et la moyenne de ces mesures.

## Compilation

Pour lancer le script il faut entrer la commande suivante : `python3 MyScript.py {heure} {fichier}` où `{heure}` est le nombre d'heure durant lesquelles le script va faire des mesures et `{fichier}` le nom du fichier .csv de sortie.

