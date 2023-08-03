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
import pprint
vector = pytest.importorskip("vector")
import sys
#sys.exit()
tfile_BIB1 = r.TFile.Open("Global_index_s4038_309680_BeamGas_20MeV.HIT.root")
tree_BIB1= tfile_BIB1.Get("ntuples/SiHGTD")

tfile_top = r.TFile.Open("Global_Index_s4038_ttbar_10.HIT.root")
tree_top = tfile_top.Get("ntuples/SiHGTD")


x_BIB1, y_BIB1, z_BIB1, t_BIB1, RDB_BIB1, RFJ_BIB1,  pdg_BIB1, E_BIB1 = Lbr.Lbr_ImportDataBIB(tree_BIB1) #variable x,y,z,R pour le BIB


x_top, y_top, z_top, t_top, RDB_top, RFJ_top,  pdg_top, E_top = Lbr.Lbr_ImportDataTop(tree_top) #variable x,y,z,R pour le BIB





datatop=[]
for hit in RFJ_top[-1]:
# Créer un dictionnaire pour chaque élément
    dictionnaire = {"px": hit[0], "py": hit[1], "pz": hit[2], "E": hit[3], "ex": 0.0}
# Ajouter le dictionnaire à la liste finale
    datatop.append(dictionnaire)

# Convertir la liste finale en ak.Array
datatop = ak.Array(datatop)

print(datatop)

print(len(x_top[-1]))

rayon = 0.4


jetdef = fastjet.JetDefinition(fastjet.antikt_algorithm, rayon)

cluster = fastjet.ClusterSequence(datatop, jetdef)
jets = cluster.inclusive_jets()

constituent = cluster.constituents()

constituent_index = cluster.constituent_index()

constituent_index = constituent_index.to_list()

num_clusters = len(jets)

x_ind, y_ind, z_ind, t_ind, pdg_ind = [], [], [], [], []

for i in range(len(constituent_index)):
    x = [x_top[-1][constituent_index[i][j]] for j in range(len(constituent_index[i]))]
    y = [y_top[-1][constituent_index[i][j]] for j in range(len(constituent_index[i]))]
    z = [z_top[-1][constituent_index[i][j]] for j in range(len(constituent_index[i]))]
    t = [t_top[-1][constituent_index[i][j]] for j in range(len(constituent_index[i]))]
    true = [pdg_top[-1][constituent_index[i][j]] for j in range(len(constituent_index[i]))]
    x_ind.append(x)
    y_ind.append(y)
    z_ind.append(z)
    t_ind.append(t)
    pdg_ind.append(true)



A, A1 = Lbr.Lbr_MinuitFitFastJet( z_ind, t_ind)

B = []
non=0
oui=0
c=0
for i in range(len(z_ind)):
    if len(z_ind[i])<2:
        B.append("NaN")
    if len(z_ind[i]) > 1 and Tools.positif(z_ind[i]):
        B.append("P")
    if len(z_ind[i]) > 1 and Tools.negatif(z_ind[i]):
        B.append("N")
    if len(z_ind[i]) > 1 and not Tools.positif(z_ind[i]) and not Tools.negatif(z_ind[i]):
        B.append("NaN")

Validation = []

# print("a",A[44])
# print("b",B[44])
for i in range(len(A)):
    c+=1
    if B[i] == "NaN":
        Validation.append("NaN")
    if float(A[i]) > 0 and B[i] == "P":
        Validation.append("OUI")
        oui += 1
    if float(A[i]) < 0 and B[i] == "N":
        Validation.append("OUI")
        oui += 1
    if float(A[i]) > 0 and B[i] == "N" or float(A[i]) < 0 and B[i] == "P":
        Validation.append("NON")
        non += 1

Eff = (oui / (oui + non))*100


# for i in range(len(Validation)):
#     if Validation[i] == "NON":
#         print("###############################")
#         print(i)
#         print("a=",A[i])
#         print("t=",t_ind[i])
#         print("z=",z_ind[i])
#         print("pgd=",pdg_ind[i])
#         print("ind=",constituent_index[i])







#Graphe
colors = plt.cm.tab10(np.linspace(0, 1, 10)) 
markers = ['o', 's', '^', 'v', 'D', 'P', '*', 'X', 'h', 'd']
a=0
for i in range(len(x_ind)):
    plt.scatter(x_ind[i], y_ind[i], color=colors[i % 10], marker=markers[(i+a) % 10],label=f'{i} {Validation[i]} , {A1[i]}, {B[i]}' )
    if (i+1) % 10 == 0:
        a+=1
plt.xlabel("Axe des x")  # Légende de l'axe x
plt.ylabel("Axe des y")  # Légende de l'axe y
plt.text(0.5, -0.11,f"Rayon du clustering = {rayon}                    Total cluster: {num_clusters}              Efficacité: {Eff}", ha='center', va='center', transform=plt.gca().transAxes)

num_events = len(x_ind)

if num_events > 40:
    num_columns = math.ceil(num_events / 40)  # Calcul du nombre de colonnes en fonction du nombre d'événements
    num_rows = math.ceil(num_events / num_columns)
    
    handles, labels = plt.gca().get_legend_handles_labels()
    legend = plt.legend(handles, labels, ncol=num_columns, mode='expand', borderaxespad=0, fontsize='small', title='Éléments', framealpha=0)        
    # Réorganiser les étiquettes des éléments en plusieurs colonnes
    label_rows = []
    for row in range(num_rows):
        start_index = row * num_columns
        end_index = min(start_index + num_columns, num_events)
        label_rows.append(labels[start_index:end_index])
    
    # Créer une légende détachée
    legend_bbox = legend.get_bbox_to_anchor().transformed(plt.gca().transAxes)
    legend_x = legend_bbox.x0
    legend_y = legend_bbox.y1 + 0.05  # Ajuster la position verticale de la légende détachée
    legend_width = legend_bbox.width
    legend_height = legend_bbox.height * num_rows
    legend_ax = plt.gcf().add_axes([legend_x, legend_y, legend_width, legend_height])
    legend_ax.axis('off')  # Masquer les axes de la légende détachée
    
    # Afficher les étiquettes des éléments en plusieurs colonnes dans la légende détachée
    for row, row_labels in enumerate(label_rows):
        row_labels_str = ' '.join(row_labels)
        legend_ax.text(0, row, row_labels_str, fontsize='small', ha='left', va='bottom')
else:
    plt.legend()
plt.show()






# for cte in constituent_index:
#     print(cte)
#     for i in cte:
#         print(i)








sys.exit()
# Extraire les coordonnées des jets
x = ak.to_numpy(jets.px)
y = ak.to_numpy(jets.py)

# Obtenir le nombre de clusters
num_clusters = len(jets)

# Générer une liste de couleurs distinctes pour chaque cluster
colors = plt.cm.get_cmap('tab20', num_clusters)

# Tracer le graphe en attribuant une couleur différente à chaque cluster
for i in range(num_clusters):
    plt.scatter(x[i], y[i], color=colors(i), label=f"Cluster {i+1}")

plt.xlabel("px")
plt.ylabel("py")
plt.title("Clusters de particules")
plt.text(0.5, -0.11,f"Rayon du clustering = {rayon}                    Total cluster: {num_clusters}" , ha='center', va='center', transform=plt.gca().transAxes)
plt.legend()

plt.show()

rayon += 0.2











sys.exit()

data = []
# Parcourir chaque sous-liste
for event in RFJ_BIB1:
    data1 = []
    for hit in event:
    # Créer un dictionnaire pour chaque élément
        dictionnaire = {"px": hit[0], "py": hit[1], "pz": hit[2], "E": hit[3], "ex": 0.0}
    # Ajouter le dictionnaire à la liste finale
        data1.append(dictionnaire)
    data.append(data1)
# Convertir la liste finale en ak.Array
data = ak.Array(data)
a=0
for i in range(len(x_BIB1)):
    for j in range(len(x_BIB1[i])):
        a+=1
print(len(x_BIB1))






jetdef = fastjet.JetDefinition(fastjet.antikt_algorithm, 1000)

cluster = fastjet.ClusterSequence(data, jetdef)


jets = cluster.inclusive_jets()

# Extraire les coordonnées des jets

# Extraire les coordonnées des jets
x = ak.to_numpy(ak.flatten(jets.px))
y = ak.to_numpy(ak.flatten(jets.py))

# Obtenir le nombre de clusters
num_clusters = len(jets)

# Générer une liste de couleurs distinctes pour chaque cluster
colors = plt.cm.get_cmap('tab20', num_clusters)

# Tracer le graphe en attribuant une couleur différente à chaque cluster
for i in range(num_clusters):
    plt.scatter(x[i], y[i], color=colors(i), label=f"Cluster {i+1}")

plt.xlabel("px")
plt.ylabel("py")
plt.title("Clusters de particules")
plt.text(0.5, -0.11,f"Total cluster: {num_clusters}" , ha='center', va='center', transform=plt.gca().transAxes)
plt.legend()

plt.show()

sys.exit()

for i in range(len(jets)):
    print(jets[i])
    print(datatop[i])
    if i == 10: break
# Extraire les coordonnées des jets

print(len(jets))
for i in range(len(jets)):
    print(jets[i])
    print("#########################################")
