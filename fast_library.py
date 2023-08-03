import ROOT as r
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import scipy
import scipy.stats
from iminuit import Minuit
from sklearn.datasets import make_blobs
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import DBSCAN
from sklearn import metrics
from tqdm import tqdm
import awkward as ak
import fastjet
import random
r.gStyle.SetOptStat(0)

import Tools_library as Tools

####################################################################################
'''INFORMATION VALABLE POUR SAMPLE s4038
Espacement des layers du HGTD avec les sample s4038_..._.HIT
Si pour chaque HGTD le layer le plus proche du PI est noté 0 et le plus éloigné est 
noté 3 (donc 0 1 2 3), on a comme distance entre chaque layer:
Entre 0 et 1: 10mm  Temps de parcour pour c : 0.033 nanoseconde
Entre 1 et 2: 15mm  Temps de parcour pour c : 0.050 nanoseconde
Entre 2 et 3: 10mm  Temps de parcour pour c : 0.033 nanoseconde
En valeur absolue:
Layer 0 = 3443mm
Layer 1 = 3453mm
Layer 2 = 3468mm
Layer 3 = 3478mm
 '''
####################################################################################





####################################################################################
'''LDL Importation des data event par event avec creation du vecteur R et en 
eliminant les hit isole et les bug 
On separe BIB et top car dans les event BIB j'ai 8 event top qui se sont glisse 
et il faut que je les supprime '''
####################################################################################


########################## Pour BIB ###############################
def Lbr_ImportDataBIB(NomTree):
	x,y,z,t,pdg,E=[],[],[],[],[],[]
	x2,y2,z2,t2,pdg2,E2=[],[],[],[],[],[]
	
	R_DB=[]
	R_FJ=[]
	for event in NomTree:
		x2.append(list(event.HGTD_x))
		y2.append(list(event.HGTD_y))
		z2.append(list(event.HGTD_z))
		t2.append(list(event.HGTD_time))
		pdg2.append(list(event.HGTD_pdgId))
		E2.append(list(event.HGTD_eloss))
#pour enlever les event avec 1 hit et parce que certain hit sont en double ce qui fait bug le clustering  (meme valeurs pour toute les variable à la dernière decimal près) 
	for x1,y1,z1,t1,pdg1,E1 in zip(x2,y2,z2,t2,pdg2,E2):
		x4,y4,z4,t4,pdg4,E4=[],[],[],[],[],[]
		for i in range(len(x1)):
			if x1[i] not in x4 and t1[i] not in t4 and t1[i] < 20 and z1[i]> 0:
				y4.append(y1[i])
				x4.append(x1[i])
				z4.append(z1[i])
				t4.append(t1[i])
				pdg4.append(pdg1[i])
				E4.append(E1[i])
		if len(x4)>1 and len(x4)<700: #Il y a des evenement top glisser dans mes samples BIB, ou du moins des evenement cheloux. je les supprimes comme ça
			y.append(y4)
			x.append(x4)
			z.append(z4)
			t.append(t4)	
			pdg.append(pdg4)	
			E.append(E4)
	for i in range(len(x)):
		X1=[]
		X1_FJ=[]
		for j in range(len(x[i])):
			if z[i][j] > 0:
				X=[]
				X_FJ=[]
				X.append(x[i][j])
				X.append(y[i][j])
				#X.append(t[i][j]) 
				X1.append(X)
				X_FJ.append((x[i][j]/t[i][j]))
				X_FJ.append((y[i][j]/t[i][j]))
				X_FJ.append((z[i][j]/t[i][j]))
				X_FJ.append(E[i][j])
				X1_FJ.append(X_FJ)
		R_DB.append(X1)
		R_FJ.append(X1_FJ)
	return x,y,z,t,R_DB,R_FJ,pdg,E



######################### Pour top #################################
def Lbr_ImportDataTop(NomTree):
	x,y,z,t,pdg,E=[],[],[],[],[],[]
	x2,y2,z2,t2,pdg2,E2=[],[],[],[],[],[]
	
	R_DB=[]
	R_FJ=[]
	for event in NomTree:
		x2.append(list(event.HGTD_x))
		y2.append(list(event.HGTD_y))
		z2.append(list(event.HGTD_z))
		t2.append(list(event.HGTD_time))
		pdg2.append(list(event.HGTD_pdgId))
		E2.append(list(event.HGTD_eloss))
#pour enlever les event avec 1 hit et parce que certain hit sont en double ce qui fait bug le clustering
	for x1,y1,z1,t1,pdg1,E1 in zip(x2,y2,z2,t2,pdg2,E2):
		x4,y4,z4,t4,pdg4,E4=[],[],[],[],[],[]
		for i in range(len(x1)):
			if x1[i] not in x4 and t1[i] not in t4 and z1[i] > 0  and t1[i] < 20 :
				y4.append(y1[i])
				x4.append(x1[i])
				z4.append(z1[i])
				t4.append(t1[i])
				pdg4.append(pdg1[i])
				E4.append(E1[i])
		if len(x4)>1: 
			y.append(y4)
			x.append(x4)
			z.append(z4)
			t.append(t4)	
			pdg.append(pdg4)	
			E.append(E4)

	for i in range(len(x)):
		X1=[]
		X1_FJ=[]
		for j in range(len(x[i])):
			if z[i][j] > 0:
				X=[]
				X_FJ=[]
				X.append(x[i][j])
				X.append(y[i][j])
				#X.append(t[i][j]) 
				X1.append(X)
				X_FJ.append((x[i][j]/t[i][j]))
				X_FJ.append((y[i][j]/t[i][j]))
				X_FJ.append((z[i][j]/t[i][j]))
				X_FJ.append(E[i][j])
				X1_FJ.append(X_FJ)
		R_DB.append(X1)
		R_FJ.append(X1_FJ)

	return x,y,z,t,R_DB,R_FJ,pdg,E


############################ Pour Pileup ###################################
def Lbr_Importminbias(NomTree):
	x,y,z,t,pdg,E=[],[],[],[],[],[]
	x2,y2,z2,t2,pdg2,E2=[],[],[],[],[],[]
	
	R_DB=[]
	R_FJ=[]
	for event in NomTree:
		x2.append(list(event.HGTD_x))
		y2.append(list(event.HGTD_y))
		z2.append(list(event.HGTD_z))
		t2.append(list(event.HGTD_time))
		pdg2.append(list(event.HGTD_pdgId))
		E2.append(list(event.HGTD_eloss))
#pour enlever les event avec 1 hit et parce que certain hit sont en double ce qui fait bug le clustering
	for x1,y1,z1,t1,pdg1,E1 in zip(x2,y2,z2,t2,pdg2,E2):
		x4,y4,z4,t4,pdg4,E4=[],[],[],[],[],[]
		for i in range(len(x1)):
			if x1[i] not in x4 and y1[i] not in y4 and z1[i] not in z4 and t1[i] not in t4 and z1[i] > 0:
				y4.append(y1[i])
				x4.append(x1[i])
				z4.append(z1[i])
				t4.append(t1[i])
				pdg4.append(pdg1[i])
				E4.append(E1[i])
		y.append(y4)
		x.append(x4)
		z.append(z4)
		t.append(t4)	
		pdg.append(pdg4)	
		E.append(E4)

	for i in range(len(x)):
		X1=[]
		X1_FJ=[]
		for j in range(len(x[i])):
			if z[i][j] > 0:
				X=[]
				X_FJ=[]
				X.append(x[i][j])
				X.append(y[i][j])
				#X.append(t[i][j]) 
				X1.append(X)
				X_FJ.append((x[i][j]/t[i][j]))
				X_FJ.append((y[i][j]/t[i][j]))
				X_FJ.append((z[i][j]/t[i][j]))
				X_FJ.append(E[i][j])
				X1_FJ.append(X_FJ)
		R_DB.append(X1)
		R_FJ.append(X1_FJ)

	return x,y,z,t,R_DB,R_FJ,pdg,E


####################################################################################
'''Melange BIB et top + rajout pileup '''
####################################################################################
# x_highP, y_highP, z_highP, t_highP, R_highP, TruehighP, pdg_highP
def finalsample(EventSize,NbPileup, x_BIB, y_BIB, z_BIB, t_BIB, R_BIB,x_top, y_top, z_top, t_top, R_top, x_lowP, y_lowP, z_lowP, t_lowP, R_lowP,TrueBIB, Truetop,True_lowP,  pdg_BIB, pdg_top, pdg_lowP, x_highP, y_highP, z_highP, t_highP, R_highP, True_highP, pdg_highP):
	x, y, z, t, R, TruePart, pdg = [], [] , [], [], [], [], []
	for i in range(EventSize):
		BIBUse = []
		TopUse = []
		EventBIB = random.randint(0,len(x_BIB)-1)
		EventTop = random.randint(0,len(x_top)-1)
		while EventBIB in BIBUse:
			EventBIB = random.randint(0,len(x_BIB)-1)
		while EventTop in TopUse:
			EventTop = random.randint(0,len(x_top)-1)
		BIBUse.append(EventBIB)
		TopUse.append(EventTop)
		x1, y1, z1, t1, R1, TruePart1, pdg1 = [], [] , [], [], [], [], []
		x1.extend(x_BIB[EventBIB])
		x1.extend(x_top[EventTop])
		y1.extend(y_BIB[EventBIB])
		y1.extend(y_top[EventTop])
		z1.extend(z_BIB[EventBIB])
		z1.extend(z_top[EventTop])
		t1.extend(t_BIB[EventBIB])
		t1.extend(t_top[EventTop])
		R1.extend(R_BIB[EventBIB])
		R1.extend(R_top[EventTop])
		pdg1.extend(pdg_BIB[EventBIB])
		pdg1.extend(pdg_top[EventTop])
		TruePart1.extend(TrueBIB[EventBIB])
		TruePart1.extend(Truetop[EventTop])

		low = 209.2692
		high = 0.725172
		for i in range(NbPileup):
			PileupUseLow = []
			PileupUseHigh = []
			low_high = random.uniform(0, low + high)
			if low_high < high:
				EventPileupHigh = random.randint(0,len(x_highP)-1)
				while EventPileupHigh in PileupUseHigh:
					EventPileupHigh = random.randint(0,len(x_highP)-1)
				x1.extend(x_highP[EventPileupHigh])
				y1.extend(y_highP[EventPileupHigh])
				z1.extend(z_highP[EventPileupHigh])
				t1.extend(t_highP[EventPileupHigh])
				R1.extend(R_highP[EventPileupHigh])
				TruePart1.extend(True_highP[EventPileupHigh])
				pdg1.extend(pdg_highP[EventPileupHigh])
				PileupUseHigh.append(EventPileupHigh)
			else:
				EventPileupLow = random.randint(0,len(x_lowP)-1)
				while EventPileupLow in PileupUseLow:
					EventPileupLow = random.randint(0,len(x_lowP)-1)
				x1.extend(x_lowP[EventPileupLow])
				y1.extend(y_lowP[EventPileupLow])
				z1.extend(z_lowP[EventPileupLow])
				t1.extend(t_lowP[EventPileupLow])
				R1.extend(R_lowP[EventPileupLow])
				TruePart1.extend(True_lowP[EventPileupLow])
				pdg1.extend(pdg_lowP[EventPileupLow])
				PileupUseLow.append(EventPileupLow)
		x.append(x1)
		y.append(y1)
		z.append(z1)
		t.append(t1)
		R.append(R1)
		pdg.append(pdg1)
		TruePart.append(TruePart1)
	return x, y, z, t, R, TruePart, pdg
####################################################################################
'''Création du  ak.array '''
####################################################################################

def akarray(RFJ):
	datatop2=[]
	for i in range(len(RFJ)):
		datatop=[]
		for hit in RFJ[i]:
			dictionnaire = {"px": hit[0], "py": hit[1], "pz": hit[2], "E": hit[3], "ex": 0.0}
			datatop.append(dictionnaire)
		datatop2.append(datatop)
	datatop2 = ak.Array(datatop2)
	return datatop2

####################################################################################
'''Compter le nombre de pdg particule'''
####################################################################################
def Numberpdg(pdg):
	numberhit = 0
	numberhitpdg = 0
	for event in pdg:
		for hit in event:
			numberhit += 1
			if hit != -9999.0:
				numberhitpdg += 1
	return numberhit, numberhitpdg

####################################################################################
'''LDL: Creation de l'indexage des layers pour une liste de liste -4 -3 -2 -1 0 1 2 3
pour HGTD droit (z negatif) du PI -> exterieur: 0 1 2 3
pour HGTD gauche (z positif) du PI -> exterieur: -1 -2 -3 -4  '''
####################################################################################
def Lbr_IndexLayerZLDL(VarZ):
	index1i=[]
	for j in range(len(VarZ)):
		index1=[]
		for i in range(len(VarZ[j])):
			if int(VarZ[j][i])== -3478:
				index2 = 3
				index1.append(index2)
			if int(VarZ[j][i])== -3468:
				index2 = 2
				index1.append(index2)
			if int(VarZ[j][i])== -3453:
				index2 = 1
				index1.append(index2)
			if int(VarZ[j][i])== -3443:
				index2 = 0
				index1.append(index2)
			if int(VarZ[j][i])== 3443:
				index2 = -1
				index1.append(index2)
			if int(VarZ[j][i])== 3453:
				index2 = -2
				index1.append(index2)
			if int(VarZ[j][i])== 3468:
				index2 = -3
				index1.append(index2)
			if int(VarZ[j][i])== 3478:
				index2 = -4
				index1.append(index2)
		index1i.append(index1)
	return index1i




####################################################################################
'''LDL Indexage du BIB et top pour différencier les deux
0 -> BIB
1 -> top
2 -> lowP
'''
####################################################################################

def Lbr_BIB(x_BIB):
	TrueBIB=[]
	for event in x_BIB:
		x=[]
		for hit in event:
			x.append(0)
		TrueBIB.append(x)
	return TrueBIB

def Lbr_top(x_top):
	Truetop=[]
	for event in x_top:
		x=[]
		for hit in event:
			x.append(1)
		Truetop.append(x)
	return Truetop

def Lbr_lowP(x_lowP):
	TruelowP=[]
	for event in x_lowP:
		x=[]
		for hit in event:
			x.append(2)
		TruelowP.append(x)
	return TruelowP



####################################################################################
'''Creation du clustering avec fastjet'''
####################################################################################
def FastJetCluster(vector,radius):
	constituent_index = []
	for event in vector:
		jetdef = fastjet.JetDefinition(fastjet.antikt_algorithm, radius)
		cluster = fastjet.ClusterSequence(event, jetdef)
		constituent_index1 = cluster.constituent_index()
		constituent_index1 = constituent_index1.to_list()
		constituent_index.append(constituent_index1)
	return constituent_index




####################################################################################
'''Creation de l'indexage pour FastJet'''
####################################################################################
def indexage(constituent_index1,VarX, VarY, VarZ, VarT, Varpdg, BiBorTop, index):
	X1,Y1,Z1,T1,PDG,BiBorTop1,index1 = [], [], [], [], [], [], []
	
	for m,constituent_index in enumerate(constituent_index1):
		for i in range(len(constituent_index)):
			x = [VarX[m][constituent_index[i][j]] for j in range(len(constituent_index[i]))] #m -> eveny, i -> Cluster dans event, j -> hit dans cluster
			y = [VarY[m][constituent_index[i][j]] for j in range(len(constituent_index[i]))]
			z = [VarZ[m][constituent_index[i][j]] for j in range(len(constituent_index[i]))]
			t = [VarT[m][constituent_index[i][j]] for j in range(len(constituent_index[i]))]
			pdg = [Varpdg[m][constituent_index[i][j]] for j in range(len(constituent_index[i]))]
			BiB = [BiBorTop[m][constituent_index[i][j]] for j in range(len(constituent_index[i]))]
			Ind = [index[m][constituent_index[i][j]] for j in range(len(constituent_index[i]))]
			X1.append(x)
			Y1.append(y)
			Z1.append(z)
			T1.append(t)
			PDG.append(pdg)
			BiBorTop1.append(BiB)
			index1.append(Ind)

	return X1, Y1, Z1, T1, PDG, BiBorTop1, index1






####################################################################################
'''LDL: Creation du clustering avec DBSCAN
Creation de l'indexage '''
####################################################################################

def DBSCANClustering(parametre,MaxHit,index1,VarT,VarZ,VarX, VarY, BIB, Varpdg):
	labelsi, n_clustersi, n_noisei = [], [], []
	Cluster, Index_cluster, Index_layer, t_index, z_index, x_index, y_index,  BIBorTop, pdg_ind = [], [], [], [], [], [], [], [], []
	for i in tqdm(range(len(VarT))):
		R1 = np.array(VarT[i]).reshape(-1, 1)

		db = DBSCAN(eps=parametre, min_samples=MaxHit) #esp= distance entre chaque hit, min_samples -> nombre minimum de hit pour faire un cluster 
		db.fit(R1) 
		labels = db.labels_  #etiquettes les hit dans les clusers -> labels[i] contient l'etiquette du i-eme point de donnees. 
		n_clusters = len(set(labels)) - (1 if -1 in labels else 0) #compte le nombre de cluster
		n_noise = list(labels).count(-1) #compte le nombre de point sans cluster
		labelsi.append(labels)
		n_clustersi.append(n_clusters)
		n_noisei.append(n_noise)		
	#Indexage des cluster
		Cluster1 = []



		for b in range(n_clusters):
			T,K,B,Z,P, X, Y = [], [], [], [], [], [], []
			M=[]
			Cluster1.append(R1[labels == b])
			cluster_hits = R1[labels == b]
			for j in range(len(cluster_hits)):
				hit_indices = np.where((R1 == cluster_hits[j]).all(axis=1))[0]
				# print("iiiii=",i)
				# print(hit_indices)
				M.append(hit_indices)
				if len(hit_indices) == 1: #expliquer ici
					a=int(hit_indices)
				if len(hit_indices) > 1:
					a=int(hit_indices[0])
				K.append(index1[i][a])
				T.append(VarT[i][a])
				B.append(BIB[i][a])
				Z.append(VarZ[i][a])
				P.append(Varpdg[i][a])
				X.append(VarX[i][a])
				Y.append(VarY[i][a])
			pdg_ind.append(P)
			Index_layer.append(K)
			t_index.append(T)
			z_index.append(Z)
			x_index.append(X)
			y_index.append(Y)
			BIBorTop.append(B)
	print("Ici", len(Index_layer))
	return labelsi, n_clustersi, n_noisei, Index_cluster, Index_layer, t_index, z_index, x_index, y_index, BIBorTop, pdg_ind



####################################################################################
'''Creation d'un fit sur les trajectoire avec minuit pour fastjet'''
####################################################################################
def fonction(z1, a, b):
	return a*z1 + b

def Lbr_MinuitFitFastJet( VarZ, VarT):
	Coef=[]
	covariances = []
	for i in tqdm(range(len(VarZ))): #cluster
		if len(VarZ[i])>1: 
			def least_squares( a, b):
				return np.sum((np.array(VarT[i]) - fonction(np.array(VarZ[i]), a, b))**2)
			init_a = 0.01
			init_b = 0.0
			m = Minuit(least_squares, a=init_a, b=init_b)
			m.migrad()
			Coef.append(m.values['a'])
			covariances.append(m.covariance)
		else: 
			Coef.append(0)
			covariances.append(None)
	return Coef, covariances



####################################################################################
'''Comptage des bon fit pour evenement top seulement (pour la recherche d'un rayon
optimum).'''
####################################################################################

def comptage(VarZ,A):
	B = []
	non=0
	oui=0
	c=0
	for i in range(len(VarZ)): #event
		B1 = []
		for j in range(len(VarZ[i])): #cluster
			if len(VarZ[i][j])<2:
				B1.append("NaN")
			if len(VarZ[i][j]) > 1 and Tools.positif(VarZ[i][j]):
				B1.append("P")
			if len(VarZ[i][j]) > 1 and Tools.negatif(VarZ[i][j]):
				B1.append("N")
			if len(VarZ[i][j]) > 1 and not Tools.positif(VarZ[i][j]) and not Tools.negatif(VarZ[i][j]):
				B1.append("NaN")
		B.append(B1)

	Validation = []

	for i in range(len(A)): #event
		for j in range(len(A[i])): #cluster
			if B[i][j] == "NaN":
				Validation.append("NaN")
				c+=1
			if float(A[i][j]) > 0 and B[i][j] == "P":
				Validation.append("OUI")
				oui += 1
			if float(A[i][j]) < 0 and B[i][j] == "N":
				Validation.append("OUI")
				oui += 1
			if float(A[i][j]) > 0 and B[i][j] == "N" or float(A[i][j]) < 0 and B[i][j] == "P":
				Validation.append("NON")
				non += 1
	
	return oui, non, c





####################################################################################
'''On regarde le nombre de cluster valide'''
####################################################################################

def Lbr_BIB_Top(BIB_true3):
	a=0
	for event in BIB_true3:
		for cluster in event:
			if Tools.ZeroBIB(cluster) or Tools.OneTop(cluster):
				a+=1
	print("Le nombre de cluster bon est:",a)


####################################################################################
'''Création graph avec root'''
####################################################################################

def Lbr_Graph(VarAbs, VarOrd, AbsTitre, OrdTitre, Titre ):
	canvas = r.TCanvas("canvas", Titre, 1200, 600)
	graph = r.TGraph(len(VarAbs), np.array(VarAbs), np.array(VarOrd))
	graph.SetLineColor(r.kMagenta+2)
	graph.SetLineWidth(2)
	graph.GetXaxis().SetTitle(AbsTitre)
	graph.GetYaxis().SetTitle(OrdTitre)

	canvas.SetLeftMargin(0.15)
	canvas.SetRightMargin(0.05)
	canvas.SetTopMargin(0.05)
	canvas.SetBottomMargin(0.15)
	canvas.Update()

	graph.Draw()
	r.gPad.SetLogx()

	legend = r.TLegend(0.25, 0.65, 0.35, 0.85)
	legend.SetBorderSize(0)
	legend.SetTextSize(0.03)
	legend.SetFillColor(0)
	legend.AddEntry(graph,'Eff', "l")
	legend.Draw()

	canvas.Draw()
	canvas.Show()
	canvas.SaveAs("Efficiency.pdf")



####################################################################################
'''On regarde les traces qui sont valide pour different coef de clustering
Utiliser les indices T et B pour y comprendre quelque chose. 
G pour HGTD Gauche.
Le BIB va dans le sens inverse à z (a < 0) dans nos samples.
+----------------------+-------------+
| 				 HGTD       	   |
+----------------------+-------------+
|  Sample     |  BIB  |   Top      |
+----------------------+-------------+
|  a > 0      |   B1  |   T1       |
+----------------------+-------------+
|  a < 0      |   B2  |   T2       |
+----------------------+-------------+
|  NaN        |   B3  |   T3       |
+----------------------+-------------+
|  total      |   B4  |   T4       |
+----------------------+-------------+ 
####################################################################################
#####################
+-------------------+
| True positive %   |
| 100 * (B2 / B4)   |
+-------------------+
| False positive %  |
| 100 * (T2 / T4)   |
+-------------------+
| True negative %   |
| 100 * (B1 / B4)   |
+-------------------+
| False negative %  |
| 100 * (T1 / T4)   |
+-------------------+
'''
####################################################################################

def Lbr_AnalyseTrace3(Coef, Index_layer, BIB_true,PDG,T):

	Nombre_Cluster=0

	#HGTD gauche -> HGTD_G
	G_B1 = 0
	G_B2 = 0
	G_B3 = 0
	G_T1 = 0 
	G_T2 = 0
	G_T3 = 0

	N = 0

	for i in range(len(Coef)):
		Nombre_Cluster += 1
####################  HGTD GAUCHE  ###########################################
		if Tools.negatif(Index_layer[i]): # On se place dans HGTD gauche
			if Coef[i] > 0:  #event qu'on assimile a du top
				if Tools.OneTop(BIB_true[i]): #assumption correct, top est bien top
#On regarde si la valeur du coef a "diverge" pas, sinon on envoie dans NaN
						G_T1 += 1
				if Tools.ZeroBIB(BIB_true[i]) or Tools.ZeroOrTwo(BIB_true[i]): # assumption fausse, c'est du BIB que notre methode detecte comme du top
						G_B1 += 1
						# print("##################")
						# print(Coef[i])
						# print(BIB_true[i])
						# print(T[i])
						for hit in PDG[i]:
							if hit != -9999.0:
								N += 1

			if Coef[i] < 0: # event qu'on assimile a du BIB
				if Tools.ZeroBIB(BIB_true[i]): #assumption correct, BIB est bien BIB
						G_B2 += 1 
				if Tools.TwoPileup(BIB_true[i]):
						G_B2 += 1
				if Tools.OneTop(BIB_true[i]): # assumption fausse, c'est du top que notre methode detecte comme du BIB
						G_T2 += 1
						for hit in PDG[i]:
							if hit != -9999.0:
								N += 1
						# print("##################################")
						# print(PDG[i])
						# print(T[i])

	G_B4 = G_B1 +  G_B2 + G_B3
	G_T4 = G_T1 + G_T2  + G_T3

	Nombre_Cluster_Bon = G_B2 + G_T1 
	G_TruePositif = 100 * (G_B2/G_B4) 
	G_TrueNegative = 100 *((G_B1+G_B3)/G_B4)
	G_FalsePositif = 100 * ((G_T2+G_T3)/G_T4)
	G_FalseNegative =100 * (G_T1/G_T4)

	return	 G_B1, G_B2, G_B3, G_B4, G_T1, G_T2, G_T3, G_T4, G_TruePositif, G_FalsePositif, G_TrueNegative, G_FalseNegative, \
		     Nombre_Cluster, Nombre_Cluster_Bon, N





####################################################################################
'''Pour faire un graphe des clusters'''
####################################################################################




def GraphCluster(Varx, Vary, NbCluster, Eff):
	colors = plt.cm.tab10(np.linspace(0, 1, 10)) 
	markers = ['o', 's', '^', 'v', 'D', 'P', '*', 'X', 'h', 'd']
	a=0
	for i in range(len(Varx)):
		plt.scatter(Varx[i], Vary[i], color=colors[i % 10], marker=markers[(i+a) % 10])
		if (i+1) % 10 == 0:
			a+=1
	plt.xlabel("Axe des x")  # Légende de l'axe x
	plt.ylabel("Axe des y")  # Légende de l'axe y
	plt.text(0.5, -0.11,f"             Total cluster: {NbCluster}              Efficacité: {Eff}", ha='center', va='center', transform=plt.gca().transAxes)

	plt.show()






