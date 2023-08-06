#!/usr/bin/env python
# -*- coding: latin-1 -*-
'''
Created on 5 sept. 2016

@author: SL
'''

import re
import string
import numpy as np


from ._porter import stem
from collections import Counter
from nltk.corpus import stopwords
from typing import Iterable, Callable
from tqdm import tqdm

STOP_WORDS = set(stopwords.words('english'))


def get_text_words(text: str) -> dict:
    """Permet de traiter le text:
        - Enlever la ponctuation
        - Separer le text vers une liste de mots
        - Stemming
        - Supprimer les stopwords
        - Calculer le nombre d'occurence de chaque mots.

        returner un dictionnaire contenant le token comme clé et le nombre d'occurence comme valeur.

    >>> text = "I like eat delicious food."
    >>> get_text_words(text=text)
    {'like': 1, 'eat': 1, 'delici': 1, 'food': 1}

    Args:
        text (str): Le text d'entrée.

    Returns:
        dict: Dictionnaire contenant comme clé le token et comme valeur le nombre d'occurence de token dans le text.
    """
    # On supprime la ponctuation de notre text pour ne pas avoir boucoup de bruit
    text = text.translate(str.maketrans('', '', string.punctuation))
    # Un expression reguliere pour spliter le text vers une list de mots
    tab = re.findall(r"\w+", text, re.UNICODE)
    # On mis les mot en miniscule pour les normalizer
    tab = [i.lower() for i in tab]
    # Pour vectoriser notre text donc on a besoin de nombre d'occurence de chaque mot dans notre text
    ret = Counter(tab)
    # On stem (enlever les traiminaison) les token (effacer les terminaison pour normaliser les mots) en gardant le nombre d'occurence
    # On supprimes les stopwords pour garger que les mots qui sont informatif
    ret = {stem(a): b for (a, b) in ret.items() if a not in STOP_WORDS}
    return ret


class CountVectorizer:
    def __init__(self, preprocessor: Callable = get_text_words, vocabulary: Iterable = None, max_df: int = None, min_df: int = 0, binary: bool = False):
        """
        Args:
            preprocessor (Callable, optional): TheFonction qui nous permer de processer le text. Defaults to get_text_words.
            vocabulary (Iterable, optional): Un vocabulaire deja connue. Defaults to None.
            max_df (int, optional): Eliminer les mots qui ont un nombre d'occurence plus de max_df. Defaults to None.
            min_df (int, optional): Eliminer les mots qui ont un nombre d'occurence inferieur à min_df. Defaults to 0.
            binary (bool, optional): Si c'est True on construit des repersentation binaire 1 si le mot exist 0 sinon. Defaults to False.
        """
        self.preprocessor = preprocessor
        self.vocabulary = vocabulary
        self.max_df = max_df if max_df is not None else np.iinfo(np.int32).max
        self.min_df = min_df
        self.binary = binary
        self.is_trained = False

    def __get_vocabulary(self, occurs):
        occur = dict()
        for text_rpr in occurs:
            for w, oc in text_rpr.items():
                occur[w] = occur.get(w, 0) + oc

        if self.vocabulary is None:
            occur = filter(
                lambda x: x[1] < self.max_df and x[1] > self.min_df, occur.items())
        else:
            occur = filter(lambda x: x[1] < self.max_df and x[1] >
                           self.min_df and x[0] in self.vocabulary, occur.items())
        return Counter(dict(occur))

    def __vectorize(self, occur):
        vect = np.zeros(len(self.vocabulary))
        for w, o in occur.items():
            idx = self.vocabulary.get(w, self.vocabulary['<oov>'])
            if self.binary:
                vect[idx] = 1
            else:
                vect[idx] = o

        return vect

    def fit(self, documents: Iterable) -> None:
        """
        Entraine le Vectorizer
        Args:
            documents (Iterable): list des document c'est à dire une liste des phrase à encoder et pour entrainer le vectorizer.
        """
        documents = np.array(documents)
        # On calcule le precessing de chaque document
        vfunc = np.vectorize(self.preprocessor)
        occurs = vfunc(documents)
        # On calcule les occurences global
        tf = self.__get_vocabulary(occurs)
        # On calcule le vocabulaire
        self.vocabulary = {k: i for i, k in enumerate(
            tf.keys(), 1)}
        # on ajoute un token qui repersente le out of vocab dans le cas ou le mot n'est pas dans le train
        self.vocabulary['<oov>'] = 0
        self.is_trained = True

    def transform(self, documents) -> np.ndarray:
        """
        Vectorize les document et retourn une matrix X
        Args:
            documents (Iterable): list des document c'est à liste des phrase à encoder.
        """
        assert self.is_trained, "Le vectorize n'est pas entrainer encore, il faut d'abord l'entrainer avec la fonction train"
        documents = np.array(documents)
        # On calcule le precessing de chaque document
        vfunc = np.vectorize(self.preprocessor)
        occurs = vfunc(documents)
        X = []
        for occur in tqdm(occurs, total=len(occurs)):
            X.append(self.__vectorize(occur=occur))
        return np.array(X)

    def fit_transform(self, documents) -> np.ndarray:
        """
        Entraine et Vectorize les document et retourn une matrix X
        Args:
            documents (Iterable): list des document c'est à liste des phrase à encoder.
        """
        documents = np.array(documents)
        # On calcule le precessing de chaque document
        vfunc = np.vectorize(self.preprocessor)
        occurs = vfunc(documents)
        # On calcule les occurences global
        tf = self.__get_vocabulary(occurs)
        # On calcule le vocabulaire
        self.vocabulary = {k: i for i, k in enumerate(
            tf.keys(), 1)}
        # on ajoute un token qui repersente le out of vocab dans le cas ou le mot n'est pas dans le train
        self.vocabulary['<oov>'] = 0
        self.is_trained = True

        X = []
        for occur in tqdm(occurs, total=len(occurs)):
            X.append(self.__vectorize(occur=occur))
        return np.array(X)







class TFIDFVectorizer:
    def __init__(self, preprocessor: Callable = get_text_words, vocabulary: Iterable = None, max_df: int = None, min_df: int = 0):
        """
        Args:
            preprocessor (Callable, optional): TheFonction qui nous permer de processer le text. Defaults to get_text_words.
            vocabulary (Iterable, optional): Un vocabulaire deja connue. Defaults to None.
            max_df (int, optional): Eliminer les mots qui ont un nombre d'occurence plus de max_df. Defaults to None.
            min_df (int, optional): Eliminer les mots qui ont un nombre d'occurence inferieur à min_df. Defaults to 0.
        """
        self.preprocessor = preprocessor
        self.vocabulary = vocabulary
        self.max_df = max_df if max_df is not None else np.iinfo(np.int32).max
        self.min_df = min_df
        self.is_trained = False


    def __get_vocabulary(self, occurs):
        occur = dict()
        for text_rpr in occurs:
            for w, oc in text_rpr.items():
                occur[w] = occur.get(w, 0) + oc

        if self.vocabulary is None:
            occur = filter(
                lambda x: x[1] < self.max_df and x[1] > self.min_df, occur.items())
        else:
            occur = filter(lambda x: x[1] < self.max_df and x[1] >
                           self.min_df and x[0] in self.vocabulary, occur.items())
        return Counter(dict(occur))

    def __vectorize(self, occur, idf):
        vect = np.zeros(len(self.vocabulary))
        for w, tf in occur.items():
            idx = self.vocabulary.get(w, self.vocabulary['<oov>'])
            vect[idx] = tf*idf[idx]
        return vect

    def _get_idf(self, documents):
        idx, df = zip(*[(idx, sum(map(lambda x: 1 if w in x else 0, documents))) for w, idx in self.vocabulary.items()])
        df = np.array(df)
        idf = np.log((1+len(documents))/(1+df))
        r =  np.zeros_like(idf)
        r[list(idx)] = idf
        return r

    def fit(self, documents: Iterable) -> None:
        """
        Entraine le Vectorizer
        Args:
            documents (Iterable): list des document c'est à dire une liste des phrase à encoder et pour entrainer le vectorizer.
        """
        documents = np.array(documents)
        # On calcule le precessing de chaque document
        vfunc = np.vectorize(self.preprocessor)
        occurs = vfunc(documents)
        # On calcule les occurences global
        tf = self.__get_vocabulary(occurs)
        # On calcule le vocabulaire
        self.vocabulary = {k: i for i, k in enumerate(
            tf.keys(), 1)}
        # on ajoute un token qui repersente le out of vocab dans le cas ou le mot n'est pas dans le train
        self.vocabulary['<oov>'] = 0
        #On calcule l'idf
        self.is_trained = True

    def transform(self, documents) -> np.ndarray:
        """
        Vectorize les document et retourn une matrix X
        Args:
            documents (Iterable): list des document c'est à liste des phrase à encoder.
        """
        assert self.is_trained, "Le vectorize n'est pas entrainer encore, il faut d'abord l'entrainer avec la fonction train"
        documents = np.array(documents)
        # On calcule le precessing de chaque document
        vfunc = np.vectorize(self.preprocessor)
        occurs = vfunc(documents)

        idf = self._get_idf(documents)

        X = []
        for occur in tqdm(occurs, total=len(occurs)):
            X.append(self.__vectorize(occur=occur, idf=idf))
        return np.array(X)

    def fit_transform(self, documents) -> np.ndarray:
        """
        Entraine et Vectorize les document et retourn une matrix X
        Args:
            documents (Iterable): list des document c'est à liste des phrase à encoder.
        """
        documents = np.array(documents)
        # On calcule le precessing de chaque document
        vfunc = np.vectorize(self.preprocessor)
        occurs = vfunc(documents)
        # On calcule les occurences global
        tf = self.__get_vocabulary(occurs)
        # On calcule le vocabulaire
        self.vocabulary = {k: i for i, k in enumerate(
            tf.keys(), 1)}
        # on ajoute un token qui repersente le out of vocab dans le cas ou le mot n'est pas dans le train
        self.vocabulary['<oov>'] = 0
        #On calcule l'idf
        idf = self._get_idf(documents)
        self.is_trained = True
        X = []
        for occur in tqdm(occurs, total=len(occurs)):
            X.append(self.__vectorize(occur=occur, idf=idf))
        return np.array(X)