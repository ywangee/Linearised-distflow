import pandas as pd
import numpy as np
import pandapower as pa
import pandapower.networks as pn
import copy
# -----------------------------------------------------------------------------
# -----------------------------------------------------------------------------



'Current network topology is imported from Pandapower, the first bus 1 is numbered as bus 0'
'The Sbase = 10MVA on basis of pypower instead of 100'
# --------------------------------------------------------------------------
# Self-defined generators which are modeled as voltage controlled PV buses
# if considering a generator as a PQ bus, use "static generator" instead.
# --------------------------------------------------------------------------
net = pn.case33bw()
net.sn_mva = 100 # unit is MWA
Vbase = 12.6 * (10 ** 3)  # in V
Sbase = net.sn_mva * (10 ** 6) # in W
Ibase = Sbase/Vbase

# predefine the DDER and NonDDER; manual input bus NO. should minus 1 to keep consistent with real number.
net.gen['1'] = pa.create_gen(net, 6, p_mw=-0.050, vm_pu=1.00, name='MT', max_p_mw=0, min_p_mw=-0.100)
net.gen['2'] = pa.create_gen(net, 9, p_mw=-0.050, vm_pu=1.00, name='MT', max_p_mw=0, min_p_mw=-0.100)
net.gen['3'] = pa.create_gen(net, 12, p_mw=-0.060, vm_pu=1.02, name='MT', max_p_mw=0, min_p_mw=-0.100) # PV
net.gen['4'] = pa.create_gen(net, 19, p_mw=-0.070, vm_pu=1.02, name='MT', max_p_mw=0, min_p_mw=-0.100)
net.gen['5'] = pa.create_gen(net, 21, p_mw=-0.080, vm_pu=1.02, name='MT', max_p_mw=0, min_p_mw=-0.100) # PV
net.gen['6'] = pa.create_gen(net, 21, p_mw=-0.080, vm_pu=1.02, name='PV', max_p_mw=0, min_p_mw=-0.100) # PV
net.gen['7'] = pa.create_gen(net, 21, p_mw=-0.080, vm_pu=1.02, name='PV', max_p_mw=0, min_p_mw=-0.100) # PV
# # -------------------------------------------------------------------------------------------------------------------------------------------
# Self-defined storage (EV). The EV should be coupled with traffic flow model,
# or further considering the GIS in the future
# ---------------------------------------------------------------------------------------------------------------------------------------------
net.storage['1'] = pa.create_storage(net, 5, p_mw=0.030, max_e_mwh=0.060, min_e_mwh=0.005, max_p_mw= 0.030, min_p_mw=-0.030, controllable=True)
net.storage['2'] = pa.create_storage(net, 11, p_mw=0.030, max_e_mwh=0.060, min_e_mwh=0.005, max_p_mw= 0.030, min_p_mw=-0.030, controllable=True)
net.storage['3'] = pa.create_storage(net, 17, p_mw=0.030, max_e_mwh=0.060, min_e_mwh=0.005, max_p_mw= 0.030, min_p_mw=-0.030, controllable=True)
net.storage['4'] = pa.create_storage(net, 24, p_mw=0.030, max_e_mwh=0.060, min_e_mwh=0.005, max_p_mw= 0.030, min_p_mw=-0.030, controllable=True)
net.storage['5'] = pa.create_storage(net, 28, p_mw=0.030, max_e_mwh=0.060, min_e_mwh=0.005, max_p_mw= 0.030, min_p_mw=-0.030, controllable=True)

net.line.to_excel("./Line.xlsx", index=False)  # net.Line contains extra branches which should be further modified
net.gen.to_excel("./Generator.xlsx", index=False)
# net.storage.to_excel("./Storage_EV.xlsx", index=False)
net.load.to_excel("./Load.xlsx", index=False)

net.PV = net.gen.loc[(net.gen['name']=='PV')]
net.MT = net.gen.loc[(net.gen['name']=='MT')]

line = pd.read_excel("./modified_Line.xlsx", engine='openpyxl')

# ngen_MT =net.gen.count('MT')
nline = line.shape[0]
nbus = net.bus.shape[0]
ngen = net.gen.shape[0]

ngen_PV = net.PV.shape[0]
ngen_MT = net.MT.shape[0]
nstorage = net.storage.shape[0]

# # ----Create bus_bus matrix ------
con_bus_bus = np.zeros([nbus, nbus])
fbus = pd.DataFrame(line, columns={'from_bus'}).values
tbus = pd.DataFrame(line, columns={'to_bus'}).values

nbranch = 32

for i in range(nbranch): # convert to branch number
    con_bus_bus[fbus[i], tbus[i]] = 1
    con_bus_bus[tbus[i], fbus[i]] = -1

# # ----Create bus_generation matrix ------
con_bus_gen = np.zeros([nbus, ngen])
genbus = pd.DataFrame(net.gen, columns={'bus'}).values

for i in range(nbus):
    for j in range(ngen):
        if i == genbus[j]:
            con_bus_gen[i, j] = 1

# ----Create bus_generation matrix with detailed generator types------
con_bus_genMT = np.zeros([nbus, ngen_MT])
gen_MTbus = pd.DataFrame(net.MT, columns={'bus'}).values

for i in range(nbus):
    for j in range(ngen_MT):
        if i == genbus[j]:
            con_bus_genMT[i, j] = 1

con_bus_genPV = np.zeros([nbus, ngen_PV])
gen_PVbus = pd.DataFrame(net.PV, columns={'bus'}).values

for i in range(nbus):
    for j in range(ngen_PV):
        if i == genbus[j]:
            con_bus_genPV[i, j] = 1

# # ----Create bus_EV matrix ------
con_bus_storage = np.zeros([nbus, nstorage])
storagebus = pd.DataFrame(net.storage, columns={'bus'}).values
#
for i in range(nbus):
    for j in range(nstorage):
        if i == storagebus[j]:
            con_bus_storage[i, j] = 1

# --------------------------------------------Call Pandapower to run power flow-----------------------------------------------
pa.runpp(net, algorithm='nr', calculate_voltage_angles='auto', init='auto', max_iteration='auto', tolerance_mva=1e-08,
         trafo_model='t', trafo_loading='current', enforce_q_lims=False, check_connectivity=True, voltage_depend_loads=True,
         consider_line_temperature=False)

#----------------------Ybus which is calcualted with the result of per_unit (baseMVA 100)---------------------
ppc = net._ppc
# print(ppc)

Ybus = net._ppc["internal"]["Ybus"].todense()
Y_bus = pd.DataFrame(Ybus)
Y_bus.to_excel("./Ybus.xlsx", index=False)
ybus = -Ybus
row, col = np.diag_indices_from(ybus)
ybus[row, col] = 0
zbus = 1./ ybus
zbus[~ np.isfinite(zbus)] = 0

r_phy = np.real(zbus)
x_phy = np.imag(zbus)
'''We converter the physical units to per unit'''
r = r_phy / (Vbase ** 2 / Sbase)
x = x_phy / (Vbase ** 2 / Sbase)


X = pd.DataFrame(x)
R = pd.DataFrame(r)
X.to_excel("./X.xlsx", index=False)
R.to_excel("./R.xlsx", index=False)

# # ----Create auxiliary_matrix to calculation ------
# ----------------------------dist_bus matrix ------------------------------------
dist_bus_matrix = np.eye(nbus)  # It is formulate based on the lin-distflow equation
for i in range(nbranch):
    dist_bus_matrix[fbus[i], tbus[i]] = -1
cbb = pd.DataFrame(dist_bus_matrix)
cbb.to_excel("./cbb.xlsx", index=False)
'''dist_bus is as same as bus_branch matrix'''

# nbranch = fbus.shape[0]
con_bus_branch = np.zeros([nbus, nbranch])
# This matrix is for SOCP distflow calculation
for i in range(nbus):
    for j in range(nbranch):
        if i == fbus[j]:
            con_bus_branch[i, j] = 1
        if i == tbus[j]:
            con_bus_branch[i, j] = -1

Con_bus_branch = pd.DataFrame(con_bus_branch)
Con_bus_branch.to_excel("./bus_branch.xlsx", index=False)

# ----Modify the R and X matrix to match the SOCP calculation------
aux_matrix = con_bus_branch
for i in range(nbus):
    for j in range(nbranch):
        if aux_matrix[i, j] == 1:
            aux_matrix[i, j] = 0
# no matter choosing departure or arrival nodes would not change the r_dist
# If converting lower triangle of r, there would be error even with same shape of r and r_triu

r_dist = -1 * r * aux_matrix
x_dist = -1 * x * aux_matrix

rdist = pd.DataFrame(r_dist)
rdist.to_excel("./r_dist.xlsx", index=False)


R_dist = np.triu(r_dist)
X_dist = np.triu(x_dist)

Rdist = pd.DataFrame(R_dist)
Rdist.to_excel("./Rdist.xlsx", index=False)

# single vector of r and x with branch number column
r_single = R_dist.T @ np.ones([nbus, 1])
x_single = X_dist.T @ np.ones([nbus, 1])
'''Have to convert the matrix to single vector to keep each bus corresponding to its relevant position'''
R_single = pd.DataFrame(r_single)
R_single.to_excel("./R_single.xlsx", index=False)
X_single = pd.DataFrame(x_single)
X_single.to_excel("./X_single.xlsx", index=False)

Trans = np.eye(nbranch)
R_Trans = Trans * r_single
X_Trans = Trans * x_single

# To convert bus_branch match
add_0 = np.array([0])
R_final = np.insert(R_Trans, 0, values=add_0, axis=0)
X_final = np.insert(X_Trans, 0, values=add_0, axis=0)


