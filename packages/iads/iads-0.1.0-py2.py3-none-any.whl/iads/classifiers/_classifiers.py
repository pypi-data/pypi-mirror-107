# -*- coding: utf-8 -*-

"""
Package: iads
File: Classifiers.py
Année: LU3IN026 - semestre 2 - 2020-2021, Sorbonne Université
"""

# Classfieurs implémentés en LU3IN026
# Version de départ : Février 2021

# Import de packages externes
import numpy as np
import copy
from abc import abstractmethod, ABC

# ---------------------------
# ------------------------ A COMPLETER :


class Kernel(ABC):
    """ Classe pour représenter des fonctions noyau
    """

    def __init__(self, dim_in, dim_out):
        """ Constructeur de Kernel
            Argument:
                - dim_in : dimension de l'espace de départ (entrée du noyau)
                - dim_out: dimension de l'espace de d'arrivée (sortie du noyau)
        """
        self.input_dim = dim_in
        self.output_dim = dim_out

    def get_input_dim(self):
        """ rend la dimension de l'espace de départ
        """
        return self.input_dim

    def get_output_dim(self):
        """ rend la dimension de l'espace d'arrivée
        """
        return self.output_dim

    @abstractmethod
    def transform(self, V: np.ndarray) -> np.ndarray:
        """fonction pour transformer un vecteur vers un nouvel espace de représentation

        Args:
            V (np.ndarray): Vecteur à transformer

        Returns:
            np.ndarray: le vecteur obetnu aprés la transformation
        """
        raise NotImplementedError("Please Implement this method")


class KernelBias(Kernel):
    """ Classe pour un noyau simple 2D -> 3D
    """

    def __init__(self, dim_in):
        super().__init__(dim_in, dim_in+1)

    def transform(self, V) -> np.ndarray:
        """ndarray de dim 2 -> ndarray de dim 3

        >>> from iads import KernelBias
        >>> import numpy as np
        >>> kernel = KernelBias(dim_in=3)
        >>> v = np.random.randint(2, 8, size=9).reshape(3,3)
        >>> v
        array([[2, 5, 2],
               [2, 4, 5],
               [7, 6, 6]])
        >>> kernel.transform(v)
        array([[1, 2, 5, 2],
               [1, 2, 4, 5],
               [1, 7, 6, 6]])
        """

        return np.insert(np.array(V), 0, 1, axis=1)


class KernelPoly(Kernel):
    def __init__(self, dim_in):
        super().__init__(dim_in, 6)

    def transform(self, V):
        """ ndarray de dim 2 -> ndarray de dim 6
            ...
        """
        table1 = np.ones((len(V), 1))
        res_1_V = np.hstack((table1, V))
        table_x1 = (V[:, 0]*V[:, 0]).reshape((V[:, 0].shape[0], 1))
        res_1_V_x1 = np.hstack((res_1_V, table_x1))
        table_x2 = (V[:, 1]*V[:, 1]).reshape((V[:, 1].shape[0], 1))
        res_1_V_x1_x2 = np.hstack((res_1_V_x1, table_x2))
        table_x1_x2 = (V[:, 0]*V[:, 1]).reshape((V[:, 0].shape[0], 1))
        res_tous = np.hstack((res_1_V_x1_x2, table_x1_x2))
        return res_tous


class Classifier(ABC):
    """ Classe pour représenter un classifieur
        Attention: cette classe est une classe abstraite, elle ne peut pas être
        instanciée.
    """

    def __init__(self, input_dimension, kernel: str = None, seed: int = 42):
        """ Constructeur de Classifier
            Argument:
                - intput_dimension (int) : dimension de la description des exemples
            Hypothèse : input_dimension > 0
        """
        assert input_dimension > 0, f"input_dimension: {input_dimension} <= 0"

        if kernel is not None and kernel == "bias":
            self.kernel = KernelBias(input_dimension)
        elif kernel is not None and kernel == "poly":
            self.kernel = KernelPoly(input_dimension)
        else:
            self.kernel = None

        self.input_dimension = input_dimension if self.kernel is None else self.kernel.get_output_dim()
        self.rand_generator = np.random.RandomState(seed)
        self.is_trained = False

    def train(self, X, y):
        """ Permet d'entrainer le modele sur l'ensemble donné
            X: ndarray avec des descriptions
            Y: ndarray avec les labels correspondants
            Hypothèse: X et Y ont le même nombre de lignes
        """
        assert X.ndim == 2, "X  is not 2 dimension"
        assert len(X) == len(
            y), "Number of observations does not equal the number of targets."

        if self.kernel is not None:
            X = self.kernel.transform(X)

        assert X.shape[1] == self.input_dimension, "input_dimension is diffrent to X"

        self._train(X, y)
        self.is_trained = True

    def score(self, x):
        """ rend le score de prédiction sur x (valeur réelle)
            x: une description
        """
        assert self.is_trained, "Model is Not trained"
        if x.shape[1] != self.input_dimension and self.kernel is not None:
            x = self.kernel.transform(x)
        return self._score(x)

    def predict(self, x):
        """ rend la prediction sur x (soit -1 ou soit +1)
            x: une description
        """
        assert self.is_trained, "Model is Not trained"
        if x.shape[1] != self.input_dimension and self.kernel is not None:
            x = self.kernel.transform(x)
        return self._predict(x)

    @abstractmethod
    def _train(self, desc_set, label_set):
        """ Permet d'entrainer le modele sur l'ensemble donné
            desc_set: ndarray avec des descriptions
            label_set: ndarray avec les labels correspondants
            Hypothèse: desc_set et label_set ont le même nombre de lignes
        """
        raise NotImplementedError("Please Implement this method")

    @abstractmethod
    def _score(self, x):
        """ rend le score de prédiction sur x (valeur réelle)
            x: une description
        """
        raise NotImplementedError("Please Implement this method")

    @abstractmethod
    def _predict(self, x):
        """ rend la prediction sur x (soit -1 ou soit +1)
            x: une description
        """
        raise NotImplementedError("Please Implement this method")

    def accuracy(self, desc_set, label_set):
        """ Permet de calculer la qualité du système sur un dataset donné
            desc_set: ndarray avec des descriptions
            label_set: ndarray avec les labels correspondants
            Hypothèse: desc_set et label_set ont le même nombre de lignes
        """
        pred = self.predict(desc_set)
        return (pred == label_set).mean()


class ClassifierLineaireRandom(Classifier):
    """ Classe pour représenter un classifieur linéaire aléatoire
        Cette classe hérite de la classe Classifier
    """

    def __init__(self, input_dimension, kernel: str = None, seed: int = 42):
        """ Constructeur de Classifier
            Argument:
                - intput_dimension (int) : dimension de la description des exemples
            Hypothèse : input_dimension > 0
        """
        super().__init__(input_dimension, kernel, seed)

    def _train(self, desc_set, label_set):
        """ Permet d'entrainer le modele sur l'ensemble donné
            desc_set: ndarray avec des descriptions
            label_set: ndarray avec les labels correspondants
            Hypothèse: desc_set et label_set ont le même nombre de lignes
        """
        #  dans ce classifieur aléatoir on se contante de mettre des valeurs aléatoire
        # un vecteur (input_dimension,1) : donc un vecteur colonne
        self.w = self.rand_generator.randn(self.input_dimension, 1)

    def _score(self, x):
        """ rend le score de prédiction sur x (valeur réelle)
            x: une description
        """
        x1 = x.reshape(-1,
                       self.input_dimension)  #  pour tjr avoir un vecteur ligne
        res = x1@self.w  #  le produit mat
        return res.reshape(-1)

    def _predict(self, X):
        """ rend la prediction sur x (soit -1 ou soit +1)
            x: une description
        """
        if X.ndim == 1:
            return -1 if self.score(X)[0] < 0 else 1
        else:
            scores = self.score(X)
            return np.where(scores < 0, -1, 1)


class ClassifierKNN(Classifier):
    """ Classe pour représenter un classifieur par K plus proches voisins.
        Cette classe hérite de la classe Classifier
    """

    # TODO: A Compléter

    def __init__(self, input_dimension, kernel: str = None, k: int = 5, normalise: bool = False, seed: int = 42):
        """ Constructeur de Classifier
            Argument:
                - intput_dimension (int) : dimension d'entrée des exemples
                - k (int) : nombre de voisins à considérer
            Hypothèse : input_dimension > 0
        """
        super().__init__(input_dimension, kernel, seed)
        self.k = k
        self.to_normalise = normalise

    def _score(self, X):
        """ rend la proportion de +1 parmi les k ppv de x (valeur réelle)
            x: une description : un ndarray
        """
        X = X.reshape(-1, self.input_dimension)
        dists = -2 * np.dot(X, self.desc_set.T) + np.sum(self.desc_set **2,    axis=1) + np.sum(X**2, axis=1)[:, np.newaxis]
        indice_plus_proche = dists.argsort(axis=1)[:, :self.k]
        scores = self.label_set[indice_plus_proche].sum(axis=1)/self.k
        return scores

    def _predict(self, X):
        """ rend la prediction sur x (-1 ou +1)
            x: une description : un ndarray
        """
        if X.ndim == 1:
            score = self.score(X)
            return -1 if score[0] < 0 else 1
        else:
            scores = self.score(X)
            return np.where(scores < 0, -1, 1)

    def _train(self, desc_set, label_set):
        """ Permet d'entrainer le modele sur l'ensemble donné
            desc_set: ndarray avec des descriptions
            label_set: ndarray avec les labels correspondants
            Hypothèse: desc_set et label_set ont le même nombre de lignes
        """
        self.desc_set = desc_set
        self.label_set = label_set
        if self.to_normalise:
            self.desc_set = self.normalise(desc_set)

    def normalise(self, desc_set):
        """
        """
        desc_set = desc_set / np.linalg.norm(desc_set)
        return desc_set

    # def repartition_data(self, desc_set, label_set):
    #     self.desc_set_test = desc_set[:len(desc_set)//3][:]
    #     self.desc_set_train = desc_set[len(desc_set)//3:][:]
    #     self.label_set_test = label_set[:len(label_set)//3][:]
    #     self.label_set_train = label_set[len(label_set)//3:][:]

        # return desc_set_test, desc_set_train, label_set_test, label_set_train

# ---------------------------

# ------------------------ A COMPLETER :


class ClassifierPerceptron(Classifier):
    """ Perceptron de Rosenblatt
    """

    def __init__(self, input_dimension: int, kernel: str = None, learning_rate: float = 1e-3, batch_size: int = 16, epochs: int = 1, history: bool = False, seed: int = 42):
        """ Constructeur de Classifier
            Argument:
                - input_dimension (int) : dimension de la description des exemples
                - learning_rate : epsilon
                - batch_size (int, optional): La taille de lot pour chaque pas dde gradient. Defaults to 16.
                - epochs (int, optional): Le nombre de fois à passer sur toute la base de données. Defaults to 1.
            Hypothèse : input_dimension > 0
        """
        super().__init__(input_dimension, kernel, seed)

        self.__w = np.zeros((self.input_dimension, 1))
        self.learning_rate = learning_rate
        self.batch_size = batch_size
        self.epochs = epochs
        self.history = history
        self.allw = []

    def _train(self, X: np.ndarray, y: np.ndarray) -> None:
        """Entraine le model

        Args:
            X (np.ndarray): Matrice X (la matrice des descriptions)
            y (np.ndarray): Le vecteur des target
        """
        self.is_trained = True
        idxbatchs = np.array_split(range(len(X)), len(X)//self.batch_size)

        for _ in range(self.epochs):
            np.random.shuffle(idxbatchs)
            for idxbatch in idxbatchs:
                x = X[idxbatch, :]
                N, _ = x.shape

                y_true = y[idxbatch]

                y_hat = self.predict(x)

                mask = np.where(y_true != y_hat, 1, 0).astype(bool)

                err = np.sum(y_true[mask, np.newaxis] *
                             x[mask, :], axis=0, keepdims=True).T

                self.__w += self.learning_rate*err/N

    def _score(self, X):
        """ rend le score de prédiction sur x (valeur réelle)
            x: une description
        """
        """x1= x.reshape(-1,self.input_dimension) # pour tjr avoir un vecteur ligne
        res= x1.dot(self.__w)  #x1@self.__w  # le produit mat
        return res[0][0]"""
        X = X.reshape(-1, self.input_dimension)
        return np.dot(X, self.__w)

    def _predict(self, X):
        """ rend la prediction sur x (soit -1 ou soit +1)
            x: une description
        """
        if X.ndim == 1:
            score = self.score(X)
            return -1 if score[0] < 0 else 1
        else:
            scores = self.score(X).reshape(-1)
            return np.where(scores < 0, -1, 1)

    def getW(self):
        return self.__w


class ClassifierPerceptronBiais(Classifier):
    """ Perceptron de ClassifierPerceptronBiais
    """

    def __init__(self, input_dimension: int, kernel: str = None, learning_rate: float = 1e-3, batch_size: int = 16, epochs: int = 1, strict: bool = False, history: bool = False, seed: int = 42):
        """ Constructeur de Classifier
            Argument:
                - input_dimension (int) : dimension de la description des exemples
                - learning_rate : epsilon
                - batch_size (int, optional): La taille de lot pour chaque pas dde gradient. Defaults to 16.
                - epochs (int, optional): Le nombre de fois à passer sur toute la base de données. Defaults to 1.
            Hypothèse : input_dimension > 0
        """
        super().__init__(input_dimension, kernel, seed)

        self.__w = np.zeros((self.input_dimension, 1))
        self.learning_rate = learning_rate
        self.batch_size = batch_size
        self.epochs = epochs
        self.history = history
        self.strict = strict

        self.allw = []
        self.cout_w = []

    def _train(self, X: np.ndarray, y: np.ndarray) -> None:
        """Entraine le model

        Args:
            X (np.ndarray): Matrice X (la matrice des descriptions)
            y (np.ndarray): Le vecteur des target
        """
        self.is_trained = True

        idxbatchs = np.array_split(range(len(X)), len(X)//self.batch_size)

        for _ in range(self.epochs):
            np.random.shuffle(idxbatchs)
            for idxbatch in idxbatchs:
                x = X[idxbatch, :]
                N, _ = x.shape

                y_true = y[idxbatch]

                y_hat = self.score(x).reshape(-1)

                if self.strict:
                    mask = np.where(y_true*y_hat <= 1, 1, 0).astype(bool)
                else:
                    mask = np.where(y_true*y_hat < 1, 1, 0).astype(bool)

                err = np.sum(y_true[mask, np.newaxis] *
                             x[mask, :], axis=0, keepdims=True).T

                self.__w += self.learning_rate*err/N

    def _score(self, X):
        """ rend le score de prédiction sur x (valeur réelle)
            x: une description
        """
        """x1= x.reshape(-1,self.input_dimension) # pour tjr avoir un vecteur ligne   
        res= x1.dot(self.__w)  #x1@self.__w  # le produit mat
        return res[0][0]"""
        X = X.reshape(-1, self.input_dimension)
        return np.dot(X, self.__w)

    def _predict(self, X):
        """ rend la prediction sur x (soit -1 ou soit +1)
            x: une description
        """
        if X.ndim == 1:
            score = self.score(X)
            return -1 if score[0] < 0 else 1
        else:
            scores = self.score(X).reshape(-1)
            return np.where(scores < 0, -1, 1)

    def getW(self):
        return self.__w


# ------------------
# code de la classe pour le classifieur ADALINE
class ClassifierADALINE(Classifier):
    """ Perceptron de ClassifierPerceptronBiais
    """

    def __init__(self, input_dimension: int, kernel: str = None, learning_rate: float = 1e-3, batch_size: int = 16, epochs: int = 1, history: bool = False, seed: int = 42):
        """ Constructeur de Classifier
            Argument:
                - input_dimension (int) : dimension de la description des exemples
                - learning_rate : epsilon
                - batch_size (int, optional): La taille de lot pour chaque pas dde gradient. Defaults to 16.
                - epochs (int, optional): Le nombre de fois à passer sur toute la base de données. Defaults to 1.
            Hypothèse : input_dimension > 0
        """
        super().__init__(input_dimension, kernel, seed)

        self.__w = np.zeros((self.input_dimension, 1))
        self.learning_rate = learning_rate
        self.batch_size = batch_size
        self.epochs = epochs
        self.history = history

        self.allw = []
        self.cout_w = []

    def _train(self, X: np.ndarray, y: np.ndarray) -> None:
        """Entraine le model

        Args:
            X (np.ndarray): Matrice X (la matrice des descriptions)
            y (np.ndarray): Le vecteur des target
        """
        self.is_trained = True

        idxbatchs = np.array_split(range(len(X)), len(X)//self.batch_size)

        for _ in range(self.epochs):
            np.random.shuffle(idxbatchs)
            for idxbatch in idxbatchs:
                x = X[idxbatch, :]
                N, _ = x.shape
                y_true = y[idxbatch].reshape(-1, 1)

                y_hat = self.score(x)

                err = x.T@(y_hat-y_true)

                self.__w -= self.learning_rate*err/N

    def _score(self, X):
        """ rend le score de prédiction sur x (valeur réelle)
            x: une description
        """
        """x1= x.reshape(-1,self.input_dimension) # pour tjr avoir un vecteur ligne
        res= x1.dot(self.__w)  #x1@self.__w  # le produit mat
        return res[0][0]"""
        X = X.reshape(-1, self.input_dimension)
        return np.dot(X, self.__w)

    def _predict(self, X):
        """ rend la prediction sur x (soit -1 ou soit +1)
            x: une description
        """
        if X.ndim == 1:
            score = self.score(X)
            return -1 if score[0] < 0 else 1
        else:
            scores = self.score(X).reshape(-1)
            return np.where(scores < 0, -1, 1)

    def getW(self):
        return self.__w


class ClassifierMultiOAA(Classifier):
    def __init__(self, classifieur: Classifier, input_dimension: int, kernel: str = None, seed: int = 42):
        super().__init__(input_dimension, kernel, seed)

        self.classif_ref = classifieur
        self.liste_classifieurs = dict()

    def _train(self, X: np.ndarray, y: np.ndarray) -> None:
        """Entraine le model

        Args:
            X (np.ndarray): Matrice X (la matrice des descriptions)
            y (np.ndarray): Le vecteur des target
        """
        self.classes = np.unique(y)
        for classe in self.classes:
            y_true = np.where(y == classe, 1, -1)
            clf = copy.deepcopy(self.classif_ref)
            clf.train(X, y_true)
            self.liste_classifieurs[classe] = clf

    def _score(self, x):
        """ rend le score de prédiction sur x (valeur réelle)
            x: une description
        """
        sss = [clf.score(x).reshape(-1, 1) for _, clf in self.liste_classifieurs.items()]
        scores = np.hstack(sss)
        return scores

    def _predict(self, x):
        scores = self.score(x)
        return np.argmax(scores, axis=1)


class NoeudCategoriel:
    """ Classe pour représenter des noeuds d'un arbre de décision
    """

    def __init__(self, num_att=-1, nom=''):
        """ 
        Constructeur: il prend en argument
            - num_att (int) : le numéro de l'attribut auquel il se rapporte: de 0 à ...
              si le noeud se rapporte à la classe, le numéro est -1, on n'a pas besoin
              de le préciser
            - nom (str) : une chaîne de caractères donnant le nom de l'attribut si
              il est connu (sinon, on ne met rien et le nom sera donné de façon 
              générique: "att_Numéro")
        """
        self.attribut = num_att    # numéro de l'attribut
        if (nom == ''):            # son nom si connu
            self.nom_attribut = 'att_'+str(num_att)
        else:
            self.nom_attribut = nom
        self.Les_fils = None       # aucun fils à la création, ils seront ajoutés
        self.classe = None       # valeur de la classe si c'est une feuille

    def est_feuille(self):
        """ rend True si l'arbre est une feuille 
            c'est une feuille s'il n'a aucun fils
        """
        return self.Les_fils == None

    def ajoute_fils(self, valeur, Fils):
        """ 
        valeur : 
        valeur de l'attribut de ce noeud qui doit être associée à Fils
                     le type de cette valeur dépend de la base
            Fils (NoeudCategoriel) : un nouveau fils pour ce noeud
            Les fils sont stockés sous la forme d'un dictionnaire:
            Dictionnaire {valeur_attribut : NoeudCategoriel}
        """
        if self.Les_fils == None:
            self.Les_fils = dict()
        self.Les_fils[valeur] = Fils
        # Rem: attention, on ne fait aucun contrôle, la nouvelle association peut
        # écraser une association existante.

    def ajoute_feuille(self, classe):
        """ 
        classe: valeur de la classe
            Ce noeud devient un noeud feuille
        """
        self.classe = classe
        self.Les_fils = None   # normalement, pas obligatoire ici, c'est pour être sûr

    def classifie(self, exemple):
        """ 
        exemple : numpy.array
            rend la classe de l'exemple (pour nous, soit +1, soit -1 en général)
            on rend la valeur 0 si l'exemple ne peut pas être classé (cf. les questions
            posées en fin de ce notebook)
        """
        if self.est_feuille():
            return self.classe
        if exemple[self.attribut] in self.Les_fils:
            # descente récursive dans le noeud associé à la valeur de l'attribut
            # pour cet exemple:
            return self.Les_fils[exemple[self.attribut]].classifie(exemple)
        else:
            # Cas particulier : on ne trouve pas la valeur de l'exemple dans la liste des
            # fils du noeud... Voir la fin de ce notebook pour essayer de résoudre ce mystère...
            print('\t*** Warning: attribut ', self.nom_attribut, ' -> Valeur inconnue: ', exemple[self.attribut])
            return 0

    def to_graph(self, g, prefixe='A'):
        """ construit une représentation de l'arbre pour pouvoir l'afficher graphiquement
            Cette fonction ne nous intéressera pas plus que ça, elle ne sera donc pas expliquée            
        """
        if self.est_feuille():
            g.node(prefixe, str(self.classe), shape='box')
        else:
            g.node(prefixe, self.nom_attribut)
            i = 0
            for (valeur, sous_arbre) in self.Les_fils.items():
                sous_arbre.to_graph(g, prefixe+str(i))
                g.edge(prefixe, prefixe+str(i), valeur)
                i = i+1
        return g


def construit_AD(X, Y, epsilon, LNoms=[]):
    """ X,Y : dataset
        epsilon : seuil d'entropie pour le critère d'arrêt 
        LNoms : liste des noms de features (colonnes) de description 
    """

    entropie_ens = entropie(Y)  # l'entropie de tous le dataset
    if (entropie_ens <= epsilon):
        # ARRET : on crée une feuille
        noeud = NoeudCategoriel(-1, "Label")
        noeud.ajoute_feuille(classe_majoritaire(Y))
    else:
        min_entropie = 1.1
        i_best = -1
        Xbest_valeurs = None
        for indice, attr in enumerate(LNoms):
            entropi_attr = 0
            # on calcule l'entropie de la classe pour chaque attribut
            # la liste des valeurs que peut prendre l'attributs attr
            val_unique, occur = np.unique(X[:, indice], return_counts=True)
            for i in range(0, len(val_unique)):
                v = val_unique[i]  # la valeur actuelle
                lab = Y[np.where(X[:, indice] == v)]
                p_v = occur[i]/len(X[:, indice])
                entropi_attr = entropi_attr + p_v * entropie(lab)  # P(Y|attr)

            if(entropi_attr < min_entropie):
                min_entropie = entropi_attr
                i_best = indice
                Xbest_valeurs = val_unique

        if len(LNoms) > 0:  # si on a des noms de features
            noeud = NoeudCategoriel(i_best, LNoms[i_best])
        else:
            noeud = NoeudCategoriel(i_best)
        for v in Xbest_valeurs:
            noeud.ajoute_fils(v, construit_AD(
                X[X[:, i_best] == v], Y[X[:, i_best] == v], epsilon, LNoms))
    return noeud


class ClassifierArbreDecision(Classifier):
    """ Classe pour représenter un classifieur par arbre de décision
    """

    def __init__(self, input_dimension, epsilon, LNoms=[]):
        """ Constructeur
            Argument:
                - intput_dimension (int) : dimension de la description des exemples
                - epsilon (float) : paramètre de l'algorithme (cf. explications précédentes)
                - LNoms : Liste des noms de dimensions (si connues)
            Hypothèse : input_dimension > 0
        """
        self.dimension = input_dimension
        self.epsilon = epsilon
        self.LNoms = LNoms
        # l'arbre est manipulé par sa racine qui sera un Noeud
        self.racine = None

    def toString(self):
        """  -> str
            rend le nom du classifieur avec ses paramètres
        """
        return 'ClassifierArbreDecision ['+str(self.dimension) + '] eps='+str(self.epsilon)

    def _train(self, desc_set, label_set):
        """ Permet d'entrainer le modele sur l'ensemble donné
            desc_set: ndarray avec des descriptions
            label_set: ndarray avec les labels correspondants
            Hypothèse: desc_set et label_set ont le même nombre de lignes
        """
        self.racine = construit_AD(
            desc_set, label_set, self.epsilon, self.LNoms)

    def _score(self, x):
        """ rend le score de prédiction sur x (valeur réelle)
            x: une description
        """
        # cette méthode ne fait rien dans notre implémentation :
        pass

    def _predict(self, x):
        """ x (array): une description d'exemple
            rend la prediction sur x             
        """
        courant = NoeudCategoriel()  # on declare un noeud  pour parcourir l'arbre
        courant = self.racine  # la racine de l'arbre de decision
        return self.racine.classifie(x)

    def affiche(self, GTree):
        """ affichage de l'arbre sous forme graphique
            Cette fonction modifie GTree par effet de bord
        """
        self.racine.to_graph(GTree)
