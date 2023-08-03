import ROOT as r
import fast_library as Lbr
import Tools_library as Tools
from pyjet import ClusterSequenceArea
import awkward as ak
import matplotlib.pyplot as plt
import numpy as np
from pyjet import cluster, DTYPE_PTEPM
import fastjet
import pytest
import math
from tqdm import tqdm
vector = pytest.importorskip("vector")
import sys
#sys.exit()

####################################################################################
#Importation des data
####################################################################################

#BIB
tfile_BIB1 = r.TFile.Open("All_BIB_global_index.HIT.root")
tree_BIB1= tfile_BIB1.Get("ntuples/SiHGTD")
x_BIB, y_BIB, z_BIB, t_BIB, RDB_BIB, RFJ_BIB,  pdg_BIB, E_BIB = Lbr.Lbr_ImportDataBIB(tree_BIB1) #variable x,y,z,R pour le BIB
#x_BIB, y_BIB, z_BIB, t_BIB, RDB_BIB, RFJ_BIB,  pdg_BIB, E_BIB = x_BIB[:10], y_BIB[:10], z_BIB[:10], t_BIB[:10], RDB_BIB[:10], RFJ_BIB[:10],  pdg_BIB[:10], E_BIB[:10]

#Top
tfile_top = r.TFile.Open("Global_Index_s4038_ttbar_400.HIT.root")
tree_top = tfile_top.Get("ntuples/SiHGTD")
x_top, y_top, z_top, t_top, RDB_top, RFJ_top,  pdg_top, E_top = Lbr.Lbr_ImportDataTop(tree_top) #variable x,y,z,R pour le BIB
#x_top, y_top, z_top, t_top, RDB_top, RFJ_top,  pdg_top, E_top = x_top[:10], y_top[:10], z_top[:10], t_top[:10], RDB_top[:10], RFJ_top[:10],  pdg_top[:10], E_top[:10]

#Pileup low
tfile_lowP = r.TFile.Open("All_global_low_minbias.HIT.root")
tree_lowP = tfile_lowP.Get("ntuples/SiHGTD")
x_lowP, y_lowP, z_lowP, t_lowP, RDB_lowP, RFJ_lowP,  pdg_lowP, E_lowP = Lbr.Lbr_Importminbias(tree_lowP)

#Pileup high
tfile_highP = r.TFile.Open("Global_000001_high_minbias_HIT.root")
tree_highP = tfile_highP.Get("ntuples/SiHGTD")
x_highP, y_highP, z_highP, t_highP, RDB_highP, RFJ_highP,  pdg_highP, E_highP = Lbr.Lbr_Importminbias(tree_highP)



####################################################################################
#On fais une liste pour reconnaitre le BIB et le top une fois les evenement ensemble
####################################################################################
TrueBIB = Lbr.Lbr_BIB(x_BIB)
Truetop = Lbr.Lbr_top(x_top)
TruelowP = Lbr.Lbr_lowP(x_lowP)
TruehighP = Lbr.Lbr_lowP(x_highP)
####################################################################################

EventSize = 200
NbPileup = 25
TruePositif = []
FasePositif = []
Truenegative = []
FalseNegative = []
for iteration in range(500):

    x, y, z, t, RFJ_tot, index_part1, pdg = Lbr.finalsample(EventSize,NbPileup, x_BIB, y_BIB, z_BIB, t_BIB, RFJ_BIB,x_top, y_top, z_top, t_top, RFJ_top, x_lowP, y_lowP, z_lowP, 
                                            t_lowP, RFJ_lowP,TrueBIB, Truetop,TruelowP,  pdg_BIB, pdg_top, pdg_lowP, x_highP, y_highP, z_highP, t_highP, RFJ_highP,TruehighP,pdg_highP)

    RFJ = Lbr.akarray(RFJ_tot)
    index1 = Lbr.Lbr_IndexLayerZLDL(z)
    rayon = 0.4
    constituent_index = Lbr.FastJetCluster(RFJ,rayon)
    X2, Y2, Z2, T2, PDG2, index_part2,index_layer2 = Lbr.indexage(constituent_index,x, y, z, t, pdg,index_part1,index1)

    parametre = 0.15
    MaxHit = 2
    labelsi, n_clustersi, n_noisei,  Index_cluster, Index_layer, T, Z, X, Y, index_part, PDG = Lbr.DBSCANClustering(parametre,MaxHit,index_layer2,T2,Z2,X2, Y2, index_part2, PDG2)

    Coef, Cov = Lbr.Lbr_MinuitFitFastJet(Z, T)
    G_B1, G_B2, G_B3, G_B4, G_T1, G_T2, G_T3, G_T4, G_TruePositif, G_FalsePositif, G_TrueNegative, G_FalseNegative,Nombre_Cluster, Nombre_Cluster_Bon, N = Lbr.Lbr_AnalyseTrace3(Coef, Index_layer, index_part,PDG,T) #avec DBSCAN
    TruePositif.append(G_TruePositif)
    FasePositif.append(G_FalsePositif)
    Truenegative.append(G_TrueNegative)
    FalseNegative.append(G_FalseNegative)
    print(iteration)


TP = np.array(TruePositif, dtype=float)
FP = np.array(FasePositif, dtype=float)
TN = np.array(Truenegative, dtype=float)
FN = np.array(FalseNegative, dtype=float)
data = np.column_stack((TP, FP, TN, FN))
np.savetxt('25Pileup.txt', data)
