import ROOT as r
import numpy as np
import matplotlib.pyplot as plt
import scipy
import scipy.stats
import pandas as pd
from iminuit import Minuit
from sklearn.datasets import make_blobs
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import DBSCAN
from sklearn import metrics
import gc
r.gStyle.SetOptStat(0)


####################################################################################
'''Supprime toute les variables globals sauf keep_vars' 
#utilisation: clear_variables() '''
####################################################################################

def clear_variables(keep_vars):
    global_vars = globals().copy()
    for var_name in global_vars:
        if var_name not in keep_vars:
            del globals()[var_name]

####################################################################################
'''Sépare les particules dans les event'''
####################################################################################

def separation(liste):
    suites_croissantes = []
    suite_actuelle = [liste[0]]

    for i in range(1, len(liste)):
        if liste[i] >= liste[i-1]:
            suite_actuelle.append(liste[i])
        else:
            suites_croissantes.append(suite_actuelle)
            suite_actuelle = [liste[i]]

    suites_croissantes.append(suite_actuelle)
    return suites_croissantes

####################################################################################
'''On regarde si il y a au moins 2 event distinct par liste'''
####################################################################################

def DeuxElementsDistincts(liste):
    if len(set(liste)) >= 2:
        return True
    else:
        return False

####################################################################################
'''Structurer une deux liste en sous liste de même structure 
l1 = [[1, 2], [3, 4, 5], [6]]
l2 = [2, 3, 4, 5, 6, 2]
l2_new=[[2, 3], [4, 5, 6], [2]] '''
####################################################################################

def AjusterStructureListe(l1, l2):
    l2_new = []
    index_l2 = 0

    for sous_liste in l1:
        taille_sous_liste = len(sous_liste)
        nouvelle_sous_liste = l2[index_l2:index_l2+taille_sous_liste]
        l2_new.append(nouvelle_sous_liste)
        index_l2 += taille_sous_liste

    return l2_new


def StructureAll(x,y,z,t,R,index1):
    x3, y3, z3, t3, R3 = [],[],[],[],[]
    for i in range(len(index1)):
        x2 =  AjusterStructureListe(x[i],index1)
        y2 =  AjusterStructureListe(y[i],index1)
        z2 =  AjusterStructureListe(z[i],index1)
        t2 =  AjusterStructureListe(t[i],index1)
        R2 =  AjusterStructureListe(R[i],index1) 
        x3.append(x2)
        y3.append(y2)
        z3.append(z2)
        t3.append(t2)
        R3.append(R2)
    return x3, y3, z3, t3, R3
####################################################################################
'''Regarde si une liste de nombre est croissant ou decroissant'''
####################################################################################
def croissante(lst):
    return all(lst[i] <= lst[i+1] for i in range(len(lst)-1))

def decroissante(lst):
    return all(lst[i] >= lst[i+1] for i in range(len(lst)-1))


####################################################################################
'''Regarde si une liste de nombre est positif ou negatif'''
####################################################################################
def positif(lst):
    return all(element >= 0 for element in lst)

def negatif(lst):
    return all(element <= 0 for element in lst)


####################################################################################
'''Regarde si une liste de nombre a que des zero ou que des 1'''
####################################################################################
def ZeroBIB(lst):
    return all(element == 0 for element in lst)

def ZeroOrTwo(lst):
    return all((element == 0 and element == 2) for element in lst )

def OneTop(lst):
    return all(element == 1  or element == 2 for element in lst)

def TwoPileup(lst):
    return all(element == 2 and element == 0   for element in lst)

####################################################################################
'''Compter le nombre de hit dans une list'''
####################################################################################
def Comptage(Liste,nom_liste):
    a=0
    for hit in Liste:
        a+=1
    print("Nombre de Hit total pour",nom_liste,a)


####################################################################################
'''Compter le nombre de trace dans une liste de liste'''
####################################################################################
def Comptage2(Liste,nom_liste):
    a = 0
    for event in Liste:
        for hit in event:
            a += 1
    print("Nombre de Trace total:",nom_liste, a)


####################################################################################
'''Compter le nombre de hit dans une liste de liste de liste'''
####################################################################################
def Comptage3(Liste,nom_liste):
    a = 0
    for event in Liste:
        for hit in event:
            for nb in hit:
                a += 1
    print("Nombre de hit total:",nom_liste, a)


####################################################################################
'''Recherche le plus petit et le plus grand element dans une liste de liste'''
####################################################################################
def extremum(Liste):
    elements = [element for sous_liste in Liste for element in sous_liste]
    plus_petit = min(elements)
    plus_grand = max(elements)
    return plus_petit, plus_grand







