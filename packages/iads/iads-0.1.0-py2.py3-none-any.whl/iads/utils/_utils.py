# -*- coding: utf-8 -*-

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import math
"""
Package: iads
Fichier: utils.py
Année: semestre 2 - 2019-2020, Sorbonne Université
"""

# ---------------------------
# -*- coding: utf-8 -*-

"""
Package: iads
File: utils.py
Année: LU3IN026 - semestre 2 - 2020-2021, Sorbonne Université
"""


# Fonctions utiles pour les TDTME de LU3IN026
# Version de départ : Février 2021

# import externe

# ------------------------


def plot2DSet(descriptions, labels):
    """
    cette fonction permet d'afficher la représentation graphique des deux ndarray passés
    en paramètre
    contrainte : on considère que la taille des deux vecteurs est la même
    """
    data_negatifs = descriptions[labels == -1]  # Extraction des exemples de classe -1:
    # Extraction des exemples de classe +1
    data_positifs = descriptions[labels == +1]
    # 'o' rouge pour la classe -1
    plt.scatter(data_negatifs[:, 0],
                data_negatifs[:, 1], marker='o', color='red')
    # 'x' bleu pour la classe +1
    plt.scatter(data_positifs[:, 0],
                data_positifs[:, 1], marker='x', color='blue')

    plt.grid(True)

def plot_frontiere(desc_set, label_set, classifier, step=30):
    """ desc_set * label_set * Classifier * int -> NoneType
        Remarque: le 4e argument est optionnel et donne la "résolution" du tracé
        affiche la frontière de décision associée au classifieur
    """
    mmax = desc_set.max(0)
    mmin = desc_set.min(0)
    x1grid, x2grid = np.meshgrid(np.linspace(
        mmin[0], mmax[0], step), np.linspace(mmin[1], mmax[1], step))
    grid = np.hstack((x1grid.reshape(x1grid.size, 1),
                      x2grid.reshape(x2grid.size, 1)))

    # calcul de la prediction pour chaque point de la grille
    res = np.array([classifier.predict(grid[i, :]) for i in range(len(grid))])
    res = res.reshape(x1grid.shape)
    # tracer des frontieres
    # colors[0] est la couleur des -1 et colors[1] est la couleur des +1
    plt.contourf(x1grid, x2grid, res, colors=[
                 "darksalmon", "skyblue"], levels=[-1000, 0, 1000])
# ------------------------


def genere_dataset_uniform(p, n, inf, sup):
    if(n % 2 == 0):  # on test si on a un nombre pair d'observations
        res = (np.random.uniform(inf, sup, (n, p)), np.asarray(
            [-1 for i in range(0, n//2)] + [+1 for i in range(0, n//2)]))
    else:
        res = (np.random.uniform(inf, sup, (n, p)), np.asarray(
            [-1 for i in range(0, n//2)] + [+1 for i in range(0, n//2+1)]))
    return res

# genere_dataset_gaussian:


def genere_dataset_gaussian(positive_center, positive_sigma, negative_center, negative_sigma, nb_points):
    np.random.seed(42)
    tab_positif = np.random.multivariate_normal(
        positive_center, positive_sigma, nb_points)
    tab_negatif = np.random.multivariate_normal(
        negative_center, negative_sigma, nb_points)
    label = np.asarray([-1 for i in range(0, nb_points)] +
                       [+1 for i in range(0, nb_points)])
    return (np.vstack((tab_negatif, tab_positif)), label)


# ------------------------
def create_XOR(n, sigma):
    d_desc_gauss, d_lab_gauss = genere_dataset_gaussian(
        np.array([10, 0]), np.array([[sigma*100, 0], [0, sigma*100]]),
        np.array([0, 0]), np.array([[sigma*100, 0], [0, sigma*100]]), n)

    d_desc_gauss1, d_lab_gauss1 = genere_dataset_gaussian(
        np.array([0, 10]), np.array([[sigma*100, 0], [0, sigma*100]]),
        np.array([10, 10]), np.array([[sigma*100, 0], [0, sigma*100]]), n)

    return np.concatenate((d_desc_gauss, d_desc_gauss1)), np.concatenate((d_lab_gauss, d_lab_gauss1))


def crossval(X, Y, n_iterations, iteration):
    index_debut_test = (len(X)//n_iterations)*(iteration)
    index_fin_test= (len(X)//n_iterations)*(iteration+1)
    indexs = np.arange(index_debut_test, index_fin_test)
    index_app = np.setdiff1d(np.arange(0, len(X)), indexs)

    return X[index_app],Y[index_app],X[indexs], Y[indexs] 


def plot2DSetMulticlass(X,Y): 
    """
    cette fonction permet d'afficher la représentation graphique des deux ndarray rerésentant plus de deux classe 
    passés en paramètre 
    contrainte : on considère que la taille des deux vecteurs est la même
    """ 
    classes = np.unique(Y)
    colors = list(mcolors.BASE_COLORS)    
    assert len(classes)<=len(colors), "non"
    for i, cl in enumerate(classes): 
        x1, x2 = X[Y == cl].T
        plt.scatter(x1, x2, c=colors[i])
        plt.xlabel('0')
        plt.ylabel(i)
    plt.show()
    
    
def conf_matric(y_true, y_pred):
    y_true = np.where(y_true==-1, 0, 1)
    y_pred = np.where(y_pred==-1, 0, 1)
    mc = np.zeros((2,2))
    for x, y in zip(y_true, y_pred):
        mc[x][y] += 1
    return mc

def shannon(P):
    """ list[Number] -> float
        Hypothèse: la somme des nombres de P vaut 1
        P correspond à une distribution de probabilité
        rend la valeur de l'entropie de Shannon correspondante
    """
    k = len(P)
    if(k<2): 
        return 0.0
    return (-1)*np.sum(list([P[i]*math.log(P[i],k) for i in range(0,k) if(P[i]!=0)]))
    
    

def entropie(Y):
    """ Y : (array) : ensemble de labels de classe
        rend l'entropie de l'ensemble Y
    """
    valeurs, nb_fois = np.unique(Y,return_counts=True)
    k = len(Y)
    P = [x/k for x in nb_fois] # la proba des classe de Y
    return shannon(P)
    
    
    
def discretise(desc, labels, col):
    """ array * array * int -> tuple[float, float]
        Hypothèse: les 2 arrays sont de même taille et contiennent au moins 2 éléments
        col est le numéro de colonne à discrétiser
        rend la valeur de coupure qui minimise l'entropie ainsi que son entropie.
    """
    # initialisation: (import sys doit avoir été fait)
    min_entropie = sys.float_info.max  # on met à une valeur max car on veut minimiser 
    min_seuil = 0.0     
    
    # trie des valeurs: ind contient les indices dans l'ordre croissant des valeurs pour chaque colonne
    ind= np.argsort(desc,axis=0)
    
    # pour voir ce qui se passe, on va sauver les entropies trouvées et les points de coupures:
    liste_entropies = []
    liste_coupures = []
    
    # Dictionnaire pour compter les valeurs de classes qui restera à voir
    Avenir_nb_class = dict()
    # et son initialisation: 
    for j in range(0,len(desc)):
        if labels[j] in Avenir_nb_class:
            Avenir_nb_class[labels[j]] += 1
        else:
            Avenir_nb_class[labels[j]] = 1
    
    # Dictionnaire pour compter les valeurs de classes que l'on a déjà vues
    Vues_nb_class = dict()
    
    # Nombre total d'exemples à traiter:
    nb_total = 0  
    for c in Avenir_nb_class:
        nb_total += Avenir_nb_class[c]
    
    # parcours pour trouver le meilleur seuil:
    for i in range(len(desc)-1):
        v_ind_i = ind[i]   # vecteur d'indices de la valeur courante à traiter
        courant = desc[v_ind_i[col]][col]  # valeur courante de la colonne
        lookahead = desc[ind[i+1][col]][col] # valeur suivante de la valeur courante
        val_seuil = (courant + lookahead) / 2.0; # Seuil de coupure: entre les 2 valeurs
        
        # M-A-J de la distrib. des classes:
        # pour réduire les traitements: on retire un exemple de E2 et on le place
        # dans E1, c'est ainsi que l'on déplace donc le seuil de coupure.
        if labels[v_ind_i[col]] in Vues_nb_class:
            Vues_nb_class[labels[v_ind_i[col]]] += 1
            
        else:
            Vues_nb_class[labels[v_ind_i[col]]] = 1
        # on retire de l'avenir:
        Avenir_nb_class[labels[v_ind_i[col]]] -= 1
        
        # construction de 2 listes: ordonnées sur les mêmes valeurs de classes
        # contenant le nb d'éléments de chaque classe
        nb_inf = [] 
        nb_sup = []
        tot_inf = 0
        tot_sup = 0
        for (c, nb_c) in Avenir_nb_class.items():
            nb_sup.append(nb_c)
            tot_sup += nb_c
            if (c in Vues_nb_class):
                nb_inf.append(Vues_nb_class[c])
                tot_inf += Vues_nb_class[c]
            else:
                nb_inf.append(0)
        
        # calcul de la distribution des classes de chaque côté du seuil:
        freq_inf = [nb/float(tot_inf) for nb in nb_inf]
        freq_sup = [nb/float(tot_sup) for nb in nb_sup]
        # calcul de l'entropie de la coupure
        val_entropie_inf = ut.shannon(freq_inf)
        val_entropie_sup = ut.shannon(freq_sup)
        
        val_entropie = (tot_inf / float(tot_inf+tot_sup)) * val_entropie_inf \
                       + (tot_sup / float(tot_inf+tot_sup)) * val_entropie_sup
        # Ajout de la valeur trouvée pour l'historique:
        liste_entropies.append(val_entropie)
        liste_coupures.append(val_seuil)
        
        # si cette coupure minimise l'entropie, on mémorise ce seuil et son entropie:
        if (min_entropie > val_entropie):
            min_entropie = val_entropie
            min_seuil = val_seuil
    return (min_seuil, min_entropie), (liste_coupures,liste_entropies,)


def leave_one_out(C, DS):
    """ Classifieur * tuple[array, array] -> float
    """ 
    nb = 0 
    for i in range(DS[0].shape[0]): # le nombre de lignes 
        
        classe = DS[1][i] 
        test = DS[0][i]  # l'individu qui sert pour test 
        index = np.setdiff1d(np.arange(0,DS[0].shape[0]),i) # les autres index 
        
        train_label = DS[1][index] # les label du train 
        train_set = DS[0][index] # les exemples du train 
        
        model = copy.deepcopy(C) 
        model.train(train_set,train_label)
        prediction = model.predict(test)
        if(prediction==classe):
            nb=nb+1
    return nb/DS[0].shape[0]  # l'accuracy       


def standard_normalization(X: np.ndarray) -> np.ndarray:
    """Transforme les caractéristiques en soustrayant la moyenne
        puis divise sur l'écart-type..

        $z = \frac{x_{i}-\mu(x)}{\sigma(x)}$

    Args:
        X (np.ndarray): les données d'entrée.

    Returns:
        np.ndarray: Tableau transformé
    """
    assert isinstance(X, np.ndarray), f"A doit etre un {np.ndarray} et non un {type(X)}"
    return (X-X.mean(axis=0))/X.std(0)



def pca(X:np.ndarray, n_components:int=2):
    """[summary]

    Args:
        X (np.ndarray): [description]
        n_components (int, optional): [description]. Defaults to 2.
    """
    assert isinstance(X, np.ndarray), f"X doit etre un {np.ndarray} et non un {type(X)}"
    assert isinstance(n_components, int), f"n_components doit etre un {int} et non un {type(n_components)}"
    assert n_components<=X.shape[1], f"n_components doit etre < {X.shape[0]}"

    X = standard_normalization(X)

    #Calculer les vecteurs propres et les valeurs propres
    covariance_matrix = np.cov(X.T) #Calculer d'abord la matrice de covariance
    _, eigen_vectors = np.linalg.eig(covariance_matrix) #Décomposition propre de la covariance
    projection_matrix = (eigen_vectors.T[:][:n_components]).T
    X_pca = X.dot(projection_matrix)
    return X_pca


def plot_coefficients(coef, feature_names, top_features=20):
    top_positive_coefficients = np.argsort(coef)[-top_features:]
    top_negative_coefficients = np.argsort(coef)[:top_features]
    top_coefficients = np.hstack([top_negative_coefficients, top_positive_coefficients])
    # create plot
    fig = plt.figure(figsize=(15, 5))
    plt.title('Les valeur des w pour les différents mot du vocabulair')
    colors = ['red' if c < 0 else 'blue' for c in coef[top_coefficients]]
    plt.bar(np.arange(2 * top_features), coef[top_coefficients], color=colors)
    feature_names = np.array(feature_names)
    plt.xticks(np.arange(1, 1 + 2 * top_features), feature_names[top_coefficients], rotation=60, ha='right')
    return fig


