import numpy as np
import random
import matplotlib.colors as mcolors
import matplotlib.pyplot as plt


from random import randint


def affiche_resultat(data_norm,les_centres,l_affectation): 
    nb_centre= len(les_centres)
    colors = list(mcolors.cnames.values())
    np.random.shuffle(colors)
    for i in range(nb_centre):
        colors.append('#%06X' % randint(0, 0xFFFFFF))


    for i in range(nb_centre): 
        plt.scatter(data_norm[l_affectation[i]][:,0],data_norm[l_affectation[i]][:,1],color=colors[i])

    x= [ l[0]for l in les_centres ]
    y = [ l[1]for l in les_centres ]
    plt.scatter(x,y,color='r',marker='x')
    plt.savefig("res_custer_final")
    plt.show()

def normalisation(A: np.ndarray) -> np.ndarray:
    """Transforme les caractéristiques en mettant chaque caractéristique sur l'échelle [0, 1].

    Args:
        A (np.ndarray): les données d'entrée.

    Returns:
        np.ndarray: Tableau transformé
    """
    assert isinstance(A, np.ndarray), f"A doit etre un {np.ndarray} et non un {type(A)}"
    return (A-A.min(axis=0))/(A.max(axis=0)-A.min(axis=0))


def dist_vect(A: np.ndarray, B: np.ndarray) -> float:
    """Calcule la distance euclidian entre A et B

    Args:
        A (np.ndarray): Vecteur 1
        B (np.ndarray): Vecteur 2

    Returns:
        float: la distance entre A et B
    """
    assert isinstance(A, np.ndarray), f"A doit etre un {np.ndarray} et non un {type(A)}"
    assert isinstance(B, np.ndarray), "B doit etre un numpy array"
    return np.sqrt(np.power(A-B, 2).sum(0))


def centroide(X: np.ndarray) -> np.ndarray:
    """Prend en entrée un ensemble d'éxemples contenant au moins 2 observation et rend leur centroide.

    Args:
        X (np.ndarray): Les données d'entrée

    Returns:
        ndarray: Le centroide de l'ensemble
    """
    assert isinstance(X, np.ndarray), f"X doit etre un {np.ndarray} et non un {type(X)}"
    # assert len(X) > 1, "X doit contenir au moins 2 exemples"

    return X.mean(axis=0)


def inertie_cluster(X:np.ndarray)->float:
    """Calculer l'inertie de cluster X

    Args:
        X (np.ndarray): Cluster

    Returns:
        float: inertie.
    """
    assert isinstance(X, np.ndarray), f"X doit etre un {np.ndarray} et non un {type(X)}"

    # l'inertie d'un cluster est la somme des distances des enxemples de ce cluster au centre

    # centre = centroide(X)  # on calcule le centre du cluster
    # some_distance = 0
    # for i in range(X.shape[0]):  # pour tous les exemples
    #     distance_au_centre = (dist_vect(X[i, :], centre))**2
    #     some_distance += distance_au_centre
        #print(f"centre : {centre}   Exemple:{ X[i,:]} distance= {distance_au_centre}")
    return (dist_vect(X, centroide(X))**2).sum()


def initialisation(k:int, X:np.ndarray)->np.ndarray:  # rend k centre de cluster 
    """
    Étant donné un entier 𝐾>1 et une base d'apprentissage X de 𝑛 exemples 
    rend un array contenant 𝐾 exemples tirés aléatoirement dans la base. 
    On fait l'hypothèse que K<=n.

    Args:
        k (int): k centre de cluster
        X (np.ndarray): base d'apprentissage.

    Returns:
        np.ndarray: échantillon de n exemples tirés aléatoirement
    """
    assert isinstance(X, np.ndarray), f"A doit etre un {np.ndarray} et non un {type(X)}"
    #assert k <= len(X), f"k={k} doit étre <= n={len(X)}"

    return np.array(random.sample(list(X), k))



def plus_proche(x:np.ndarray, centroides:np.ndarray)->int:
    """
    Rend l'indice du array correspondant au centroide dont l'exemple est le plus proche.
    En cas d'égalité de distance, le centroide de plus petit indice est choisi.

    Args:
        x (np.ndarray): un exemple
        centroides (np.ndarray): centroides

    Returns:
        int: l'indice de centroide le plus proche a l'exemple x.
    """
    assert isinstance(x, np.ndarray), f"x doit etre un {np.ndarray} et non un {type(x)}"
    assert isinstance(centroides, np.ndarray), f"centroides doit etre un {np.ndarray} et non un {type(centroides)}"


    return dist_vect(x.reshape(-1, 1), centroides.T).argmin()

def affecte_cluster(X:dict, centroides:np.ndarray)->dict:
    """
    Étant donné une base d'apprentissage et un ensemble de K centroïdes, 
    rend la matrice d'affectation des exemples de la base aux clusters représentés par chaque centroïde.

    Args:
        X (dict): base d'apprentissage.
        centroides (np.ndarray): centroïdes.

    Returns:
        dict: affectation des exemples
    """
    assert isinstance(X, np.ndarray), f"X doit etre un {np.ndarray} et non un {type(X)}"
    assert isinstance(centroides, np.ndarray), f"centroides doit etre un {np.ndarray} et non un {type(centroides)}"


    aff = np.apply_along_axis(plus_proche, 1, X, centroides)
    dic = {
        centroide:np.where(aff==centroide)[0] for centroide in range(len(centroides))
    }
    return dict(dic)


def nouveaux_centroides(X:np.ndarray, affectation:dict)->np.ndarray:
    """
    Étant donné une base d'apprentissage et une matrice d'affectation,
    rend l'ensemble des nouveaux centroides obtenus.

    Args:
        X (np.ndarray): base d'apprentissage
        affectation (dict): matrice d'affectation

    Returns:
        np.ndarray: nouveau centroides
    """
    assert isinstance(X, np.ndarray), f"X doit etre un {np.ndarray} et non un {type(X)}"
    assert isinstance(affectation, dict), f"affectation doit etre un {np.ndarray} et non un {type(affectation)}"

    # renvoie l'ensemble des nouveau centroides
    return np.array([ centroide(X[index]) for _, index in affectation.items()])


def inertie_globale(X:np.ndarray, affectation:dict)->np.ndarray:
    """étant donné une base d'apprentissage et une matrice d'affectation, rend la valeur de l'inertie globale du partitionnement correspondant.

    Args:
        X (np.ndarray): [description]
        affectation (dict): [description]

    Returns:
        np.ndarray: [description]
    """
    assert isinstance(X, np.ndarray), f"X doit etre un {np.ndarray} et non un {type(X)}"
    assert isinstance(affectation, dict), f"affectation doit etre un {dict} et non un {type(affectation)}"

    return sum([ inertie_cluster(X[index]) for _, index in affectation.items()])



def kmoyennes(k:int, X:np.ndarray, epsilon:float, iter_max:int)->tuple:
    """Cette fonction est une imlimentation de l'algorithme de Kmeans.

    Args:
        k (int): Nombre de clusters, K>1.
        X (np.ndarray): base d'apprentissage.
        epsilon (float): epsilon est un critère de convergence, epsilon > 0.
        iter_max (int): iter_max est utilisé pour fixer un nombre d'itérations maximal, iter_max>1

    Returns:
        tuple: ensemble de centroides, la matrice d'affectation.
    """
    assert k>1, f"k doit etre > 1 et pas {k}"
    assert isinstance(X, np.ndarray), f"X doit etre un {np.ndarray} et non un {type(X)}"
    assert epsilon>0, f"epsilon doit etre > 0 et pas {epsilon}"
    assert iter_max>1, f"iter_max doit etre > 1 et pas {iter_max}"

    X = normalisation(X)
    centroides = initialisation(k, X)  # initialisation des centroides au hasard
    matrix= affecte_cluster(X,centroides) # on effecte les données aux centroides 
    inertie = inertie_globale(X, matrix)
    nb_iter = 0
    while((nb_iter< iter_max) and (inertie>epsilon)): 
        centroides = nouveaux_centroides(X, matrix)
        matrix= affecte_cluster(X, centroides)
        inertie = abs(inertie - inertie_globale(X, matrix))
        nb_iter+=1
    return centroides, matrix



def calculate_WSS(data, kmax):
    sse = []
    for k in range(1, kmax+1):
        centroides, matrix = kmoyennes(
                                k=10, 
                                X=data, 
                                epsilon=0.3, 
                                iter_max=int(1e1)
                            )
        curr_sse = 0

        # calculate square of Euclidean distance of each point from its cluster center and add to current WSS
        for c_name, index in matrix.items():
            curr_sse = dist_vect(data[index], centroides[c_name]).sum()
            # curr_center = centroids[pred_clusters[i]]
            # curr_sse += (data[i, 0] - curr_center[0]) ** 2 + (data[i, 1] - curr_center[1]) ** 2

        sse.append(curr_sse)
    return sse