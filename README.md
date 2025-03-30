# Linearised-distflow

This repository provides a model of the IEEE 33-bus radial distribution network implemented using pandapower. It allows users to add custom-defined Distributed Energy Resources (DERs) such as photovoltaic (PV) systems, wind turbines, distributed generators (DG), and storage units at desired nodes. Users can perform power flow analyses utilizing various pandapower functions.​


## 1. Custom DER Integration
Easily add user-defined DERs, including PV systems, wind turbines, DGs, and storage units, to specific nodes within the network.​
## 2. Power Flow Analysis
Utilize general linearized distflow equations or pandapower's (https://www.pandapower.org) functions to conduct power flow analyses on the modified network.​

In detail, the key equations of linearized distflow equations are given by:

P(i+1, t) = P(i, t) + P(i+1, t)^G - P(i+1, t)^LD - P(i+1, t)^Lat
Q(i+1, t) = Q(i, t) - Q(i+1, t)^LD - Q(i+1, t)^Lat     for all i, t
U(i+1, t) = U(i, t) - [R_i * P(i, t) + X_i * Q(i, t)] / U0    for all i, t



## 3. Simplified Network Data
Access an accompanying .xlsx file containing a simplified representation of the distribution network, detailing feeder connections and corresponding impedance parameters. You can decide change different networks based on your desires. 
