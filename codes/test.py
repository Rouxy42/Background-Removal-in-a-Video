import numpy as np
import os
from scipy.io import loadmat
from scipy.optimize import linprog

script_dir = os.path.dirname(os.path.abspath(__file__))  # marche pour un script .py
file_path = os.path.join(script_dir, "pedsX.mat")

print("Chemin complet :", file_path)

# --- Charger le fichier .mat ---
data = loadmat(file_path)

# --- Exemple : accéder à une variable ---
X = np.array(data["X"])  # converti en ndarray pour sécurité
m = np.array(data["m"])
n = np.array(data["n"])
print(X)

#Ici, on a récupéré la big matrice avec les images vectorisées (X c'est la vidéo)
#m et n sont les dimensions (en pixel) des images

# Données
m = int(m)
n = int(n)
p = m * n  # Taille du vecteur image
t = 100


# Objectif
c = [1, -1, -1]

# Création de la matrice contraintes A 
A = np.zeros((2*t, 3*t +1))
for j in range(t):
    # Première contrainte pour les 100 itérations
    A[j, 0] = 1
    A[j, j + 1] = 1
    A[j, j + 101] = -1
    # Deuxième contrainte pour les 100 itérations
    A[100 + j, 0] = -1
    A[100 + j, j + 1] = 1
    A[100 + j, j + 201] = -1
