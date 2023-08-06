# -*- coding: utf-8 -*-

"""
Package: iads
File: evaluation.py
Année: LU3IN026 - semestre 2 - 2020-2021, Sorbonne Université
"""

# ---------------------------
# Fonctions d'évaluation de classifieurs

# import externe
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns



def matrix_confusion(y_true, y_hat):
    assert y_true.shape == y_hat.shape, "shape is not the same"
    if len(np.unique(y_true)) == 2:
        y_true = np.where(y_true == -1, 0, 1)
        y_hat = np.where(y_hat == -1, 0, 1)

    x = zip(y_true, y_hat)
    cf = np.zeros((len(np.unique(y_true)), len(np.unique(y_true))))
    for true, pred in x:
        cf[true][pred] += 1

    blanks = ['' for i in range(cf.size)]
    group_labels = ['True Neg', 'False Pos', 'False Neg', 'True Pos'] if len(np.unique(y_true)) == 2 else blanks

    group_counts = ["{0:0.0f}\n".format(value) for value in cf.flatten()]

    group_percentages = ["{0:.2%}".format(value) for value in cf.flatten()/np.sum(cf)]

    box_labels = [f"{v1}{v2}{v3}".strip() for v1, v2, v3 in zip(group_labels, group_counts,group_percentages)]
    box_labels = np.asarray(box_labels).reshape(cf.shape[0],cf.shape[1])

    accuracy  = np.trace(cf) / float(np.sum(cf))

    if len(cf)==2:
        precision = cf[1,1] / sum(cf[:,1])
        recall    = cf[1,1] / sum(cf[1,:])
        f1_score  = 2*precision*recall / (precision + recall)
        stats_text = "\n\nAccuracy={:0.3f}\nPrecision={:0.3f}\nRecall={:0.3f}\nF1 Score={:0.3f}".format(
            accuracy,precision,recall,f1_score)
    else:
        stats_text = "\n\nAccuracy={:0.3f}".format(accuracy)



    figsize = plt.rcParams.get('figure.figsize')


    plt.figure(figsize=figsize)
    sns.heatmap(cf,annot=box_labels, fmt="",cmap="Blues", cbar=True, xticklabels="auto",yticklabels="auto")

    plt.ylabel('True label')
    plt.xlabel('Predicted label' + stats_text)

