import numpy as np
import os
from scipy.io import loadmat

# --- Obtenir le dossier du script actuel ---
script_dir = os.path.dirname(os.path.abspath(__file__))

# --- Construire le chemin vers le fichier .mat dans le même dossier ---
file_path = os.path.join(script_dir, "pedsX.mat")

# --- Vérifier que le fichier existe ---
if not os.path.isfile(file_path):
    raise FileNotFoundError(f"Fichier non trouvé : {file_path}")

# --- Charger le fichier .mat ---
data = loadmat(file_path)

# --- Exemple : accéder à une variable ---
X = np.array(data["X"])  # converti en ndarray pour sécurité
m = np.array(data["m"])
n = np.array(data["n"])

#Ici, on a récupéré la big matrice avec les images vectorisées (X c'est la vidéo)
#m et n sont les dimensions (en pixel) des images

F = np.array