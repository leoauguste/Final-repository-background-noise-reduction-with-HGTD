import awkward as ak  # noqa: F401
import numpy as np  # noqa: F401
import pytest  # noqa: F401
import pprint
import fastjet._pyjet  # noqa: F401
from sklearn.cluster import DBSCAN
import ROOT as r
from ROOT import TGraphErrors

TP = []
FP = []
TN = []
FN = []
STP = []
SFP = []
STN = []
SFN = []
abs = [0.,10., 25.,50.,100.,150.,200.]

data1 = np.loadtxt('0Pileup.txt')
TP1 = data1[:, 0].tolist()
FP1 = data1[:, 1].tolist()
TN1 = data1[:, 2].tolist()
FN1 = data1[:, 3].tolist()
VarTP1 = np.sqrt(np.var(TP1))
VarFP1 = np.sqrt(np.var(FP1))
VarTN1 = np.sqrt(np.var(TN1))
VarFN1 = np.sqrt(np.var(FN1))
MTP1 = np.mean(TP1)
MTN1 = np.mean(TN1)
MFP1 = np.mean(FP1)
MFN1 = np.mean(FN1)

data1_5 = np.loadtxt('10Pileup.txt')
TP1_5 = data1_5[:, 0].tolist()
FP1_5 = data1_5[:, 1].tolist()
TN1_5 = data1_5[:, 2].tolist()
FN1_5 = data1_5[:, 3].tolist()
VarTP1_5 = np.sqrt(np.var(TP1_5))
VarFP1_5 = np.sqrt(np.var(FP1_5))
VarTN1_5 = np.sqrt(np.var(TN1_5))
VarFN1_5 = np.sqrt(np.var(FN1_5))
MTP1_5 = np.mean(TP1_5)
MTN1_5 = np.mean(TN1_5)
MFP1_5 = np.mean(FP1_5)
MFN1_5 = np.mean(FN1_5)

data2 = np.loadtxt('25Pileup.txt')
TP2 = data2[:, 0].tolist()
FP2 = data2[:, 1].tolist()
TN2 = data2[:, 2].tolist()
FN2 = data2[:, 3].tolist()
VarTP2 = np.sqrt(np.var(TP2))
VarFP2 = np.sqrt(np.var(FP2))
VarTN2 = np.sqrt(np.var(TN2))
VarFN2 = np.sqrt(np.var(FN2))
MTP2 = np.mean(TP2)
MTN2 = np.mean(TN2)
MFP2 = np.mean(FP2)
MFN2 = np.mean(FN2)

data3 = np.loadtxt('50Pileup.txt')
TP3 = data3[:, 0].tolist()
FP3 = data3[:, 1].tolist()
TN3 = data3[:, 2].tolist()
FN3 = data3[:, 3].tolist()
VarTP3 = np.sqrt(np.var(TP3))
VarFP3 = np.sqrt(np.var(FP3))
VarTN3 = np.sqrt(np.var(TN3))
VarFN3 = np.sqrt(np.var(FN3))
MTP3 = np.mean(TP3)
MTN3 = np.mean(TN3)
MFP3 = np.mean(FP3)
MFN3 = np.mean(FN3)

data4 = np.loadtxt('100Pileup.txt')
TP4 = data4[:, 0].tolist()
FP4 = data4[:, 1].tolist()
TN4 = data4[:, 2].tolist()
FN4 = data4[:, 3].tolist()
VarTP4 = np.sqrt(np.var(TP4))
VarFP4 = np.sqrt(np.var(FP4))
VarTN4 = np.sqrt(np.var(TN4))
VarFN4 = np.sqrt(np.var(FN4))
MTP4 = np.mean(TP4)
MTN4 = np.mean(TN4)
MFP4 = np.mean(FP4)
MFN4 = np.mean(FN4)

data5 = np.loadtxt('150Pileup.txt')
TP5 = data5[:, 0].tolist()
FP5 = data5[:, 1].tolist()
TN5 = data5[:, 2].tolist()
FN5 = data5[:, 3].tolist()
VarTP5 = np.sqrt(np.var(TP5))
VarFP5 = np.sqrt(np.var(FP5))
VarTN5 = np.sqrt(np.var(TN5))
VarFN5 = np.sqrt(np.var(FN5))
MTP5 = np.mean(TP5)
MTN5 = np.mean(TN5)
MFP5 = np.mean(FP5)
MFN5 = np.mean(FN5)


data6 = np.loadtxt('200Pileup.txt')
TP6 = data6[:, 0].tolist()
FP6 = data6[:, 1].tolist()
TN6 = data6[:, 2].tolist()
FN6 = data6[:, 3].tolist()
VarTP6 = np.sqrt(np.var(TP6))
VarFP6 = np.sqrt(np.var(FP6))
VarTN6 = np.sqrt(np.var(TN6))
VarFN6 = np.sqrt(np.var(FN6))
MTP6 = np.mean(TP6)
MTN6 = np.mean(TN6)
MFP6 = np.mean(FP6)
MFN6 = np.mean(FN6)


TP.append(MTP1)
TP.append(MTP1_5)
TP.append(MTP2)
TP.append(MTP3)
TP.append(MTP4)
TP.append(MTP5)
TP.append(MTP6)
STP.append(VarTP1)
STP.append(VarTP1_5)
STP.append(VarTP2)
STP.append(VarTP3)
STP.append(VarTP4)
STP.append(VarTP5)
STP.append(VarTP6)

FP.append(MFP1)
FP.append(MFP1_5)
FP.append(MFP2)
FP.append(MFP3)
FP.append(MFP4)
FP.append(MFP5)
FP.append(MFP6)
SFP.append(VarFP1_5)
SFP.append(VarFP2)
SFP.append(VarFP3)
SFP.append(VarFP4)
SFP.append(VarFP5)
SFP.append(VarFP6)

TN.append(MTN1)
TN.append(MTN1_5)
TN.append(MTN2)
TN.append(MTN3)
TN.append(MTN4)
TN.append(MTN5)
TN.append(MTN6)
STN.append(VarTN1)
STN.append(VarTN1_5)
STN.append(VarTN2)
STN.append(VarTN3)
STN.append(VarTN4)
STN.append(VarTN5)
STN.append(VarTN6)

FN.append(MFN1)
FN.append(MFN1_5)
FN.append(MFN2)
FN.append(MFN3)
FN.append(MFN4)
FN.append(MFN5)
FN.append(MFN6)
SFN.append(VarFN1)
SFN.append(VarFN1_5)
SFN.append(VarFN2)
SFN.append(VarFN3)
SFN.append(VarFN4)
SFN.append(VarFN5)
SFN.append(VarFN6)



Dic = [TP, FP, TN, FN]
Incertitude = [STP, SFP, STN, SFN]
zz = [0., 0., 0., 0., 0., 0., 0.,]
x_min = 0
x_max = 210
y_min = 0
y_max = 100
def Lbr_plot_graph_root( abs, Dic):
	#Avec root
    c = r.TCanvas("c", "c", 800, 800)

    # TP
    gr1 = TGraphErrors(len(abs), np.array(abs), np.array(TP), np.array(zz), np.array(STP))
    gr1.SetTitle("Confusion matrix for different number of pileup")
    gr1.SetLineColor(r.kBlue)
    gr1.SetLineWidth(2)

    gr1.SetFillColorAlpha(r.kBlue-9, 0.5)  # Utilisez une couleur plus claire pour le remplissage
    gr1.SetFillStyle(1001)  # Utilisez le style de remplissage 1001 pour un remplissage uni
    gr1.SetMarkerStyle(20)  # Définissez le style de marqueur souhaité
    gr1.Draw("APL")

    gr1.GetYaxis().SetTitle("(%)")
    gr1.GetYaxis().SetTitleSize(0.05)
    gr1.GetYaxis().SetTitleOffset(1.2)

    gr1.GetXaxis().SetTitle("Pileup event")
    gr1.GetXaxis().SetTitleSize(0.05)
    gr1.GetXaxis().SetTitleOffset(1.2)
    gr1.SetMarkerStyle(20)
    gr1.GetXaxis().SetRangeUser(x_min, x_max)  #choisir le début et la fin des axe, si on le met pas le canevas choisi pour nous
    gr1.GetYaxis().SetRangeUser(y_min, y_max)

    # FP
    gr2 = TGraphErrors(len(abs), np.array(abs), np.array(FP), np.array(zz), np.array(SFP))
    gr2.SetLineColor(r.kRed)
    gr2.SetLineWidth(2)
    gr2.SetMarkerStyle(20)
    gr2.SetFillColorAlpha(r.kRed-9, 0.5)  # Utilisez une couleur plus claire pour le remplissage
    gr2.SetFillStyle(1001)  # Utilisez le style de remplissage 1001 pour un remplissage uni
    gr2.Draw("PL SAME")

    # TN
    gr3 = TGraphErrors(len(abs), np.array(abs), np.array(TN), np.array(zz), np.array(STN))    
    gr3.SetLineColor(r.kGreen+2)
    gr3.SetLineWidth(2)
    gr3.SetMarkerStyle(20)
    gr3.SetFillColorAlpha(r.kGreen-9, 0.5)  # Utilisez une couleur plus claire pour le remplissage
    gr3.SetFillStyle(1001)  # Utilisez le style de remplissage 1001 pour un remplissage uni
    gr3.Draw("PL SAME")

    # FN
    gr4 = TGraphErrors(len(abs), np.array(abs), np.array(FN), np.array(zz), np.array(SFN))  
    gr4.SetLineColor(r.kMagenta+2)
    gr4.SetLineWidth(2)
    gr4.SetMarkerStyle(20)
    gr4.SetFillColorAlpha(r.kMagenta-9, 0.5)  # Utilisez une couleur plus claire pour le remplissage
    gr4.SetFillStyle(1001)  # Utilisez le style de remplissage 1001 pour un remplissage uni
    gr4.Draw("PL SAME")


    leg = r.TLegend(0.2, 0.55, 0.45, 0.7) #coin inf gauch, sup droit
    leg.SetBorderSize(0)
    leg.SetFillColor(0)
    leg.AddEntry(gr1, "True positive", "l")
    leg.AddEntry(gr2, "False negative", "l")
    leg.AddEntry(gr3, "True negative", "l")
    leg.AddEntry(gr4, "False negative", "l")
    leg.Draw()

    #c.SetLogx()
    c.SetTitle("Efficiency")
    c.SetLeftMargin(0.15)
    c.SetRightMargin(0.05)
    c.SetTopMargin(0.05)
    c.SetBottomMargin(0.15)
    c.Update()

    c.SaveAs("Confusions2.pdf")




Lbr_plot_graph_root(abs, Dic)








