# Linearised-distflow

This repository provides a model of the IEEE 33-bus radial distribution network implemented using pandapower. It allows users to add custom-defined Distributed Energy Resources (DERs) such as photovoltaic (PV) systems, wind turbines, distributed generators (DG), and storage units at desired nodes. Users can perform power flow analyses utilizing various pandapower functions.​


## 1. Custom DER Integration
Easily add user-defined DERs, including PV systems, wind turbines, DGs, and storage units, to specific nodes within the network.​
## 2. Power Flow Analysis
Utilize general linearized distflow equations or pandapower's (https://www.pandapower.org) functions to conduct power flow analyses on the modified network.​

In detail, the key equations of linearized distflow equations are given by:

\begin{subequations}
\begin{align}
\textbf{Active power balance:}\quad
P_{i+1,t} &= P_{i,t} + P_{i+1,t}^{\mathrm{G}} - P_{i+1,t}^{\mathrm{LD}} - P_{i+1,t}^{\mathrm{Lat}}, \label{eq:activeBalance}\\[1mm]
\textbf{Reactive power balance:}\quad
Q_{i+1,t} &= Q_{i,t} - Q_{i+1,t}^{\mathrm{LD}} - Q_{i+1,t}^{\mathrm{Lat}}, \quad \forall\, i,t, \label{eq:reactiveBalance}\\[1mm]
\textbf{Voltage drop:}\quad
U_{i+1,t} &= U_{i,t} - \frac{R_i\,P_{i,t} + X_i\,Q_{i,t}}{U_0}, \quad \forall\, i,t, \label{eq:voltageDrop}
\end{align}
\end{subequations}

where:
\begin{itemize}
    \item \(P_{i,t}\) and \(Q_{i,t}\) denote the active and reactive power flowing through the main branch at bus \(i\) and time \(t\);
    \item \(P_{i,t}^{\mathrm{G}}\) represents the power injection from DERs at bus \(i\) (with \(P_{1,t}^{\mathrm{G}}\) including the grid power);
    \item \(P_{i,t}^{\mathrm{LD}}\) and \(Q_{i,t}^{\mathrm{LD}}\) are the local load demands;
    \item \(P_{i,t}^{\mathrm{Lat}}\) and \(Q_{i,t}^{\mathrm{Lat}}\) denote the power flows on the lateral branches;
    \item \(R_i\) and \(X_i\) are the resistance and reactance of the line segment between buses \(i\) and \(i+1\);
    \item \(U_{0}\) is the substation (reference) voltage.
\end{itemize}

Equations \eqref{eq:activeBalance}--\eqref{eq:voltageDrop} ensure that the power flow and voltage profiles along the feeder are maintained within their operational limits.

## 3. Simplified Network Data
Access an accompanying .xlsx file containing a simplified representation of the distribution network, detailing feeder connections and corresponding impedance parameters. You can decide change different networks based on your desires. 
