# LINFO2142

## Pings Measures

Run ping_measure from /Mesures with ```python3 ping_measure.py destination.csv (numbre of measures)```

## Bandwidth Measures

Run bw_measure from /Mesures with ```python3 bw_measure.py destination.csv ```

## Weather scrapping

Run scrapping from /Mesures with ```python3 scrapping.py destination.csv```

## Traceroute

To launch the traceroute analysis, first you need to run in Mesures ```python3 traceroute.py "../data2/traceroute.txt" "../data2/measure_traceroute.csv"``` and then in analyse ```python3 analyse.py```. The text analysis will be in "traceroute_analyse.txt" and the code will plot the 4 graphs of the report.

## Packages

pip3 install ping3 dnspython speedtest-cli

## Data

The data directory contains the data we used, mainly data_fusion (all the measure done with the satellite) and data_home (measure done with Proximus).

## Analyse

/analyse contains the script used for the analyse of the data.
