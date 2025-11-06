import numpy as np
import os
from scipy.io import loadmat
from scipy.optimize import linprog
import matplotlib.pyplot as plt
import imageio.v2 as imageio

script_dir = os.path.dirname(os.path.abspath(__file__))  # marche pour un script .py
file_path = os.path.join(script_dir, "pedsX.mat")

print("Chemin complet :", file_path)

# --- Charger le fichier .mat ---
data = loadmat(file_path)

# --- Exemple : accéder à une variable ---
X = np.array(data["X"])  # converti en ndarray pour sécurité
m = np.array(data["m"])
n = np.array(data["n"])
#_________________________
#Ici, on a récupéré la big matrice avec les images vectorisées (X c'est la vidéo)
#m et n sont les dimensions (en pixel) des images

# Données
m = int(m)
n = int(n)
p = m * n  # Taille du vecteur image
t = 100

# Affichage d'une image
image = X[:,1].reshape((n,m)).T
image = 1 - image
plt.imshow(image, cmap = "grey")

# Vidéo initiale
frames = []
for i in range(X.shape[1]):
    frame = X[:,i].reshape((n,m)).T
    frame = 1 - frame
    frames.append(frame)

imageio.mimsave("video.mp4", frames, fps=10)

# Objectif
c = np.zeros(3*t + 2)
c[2:2+t] = 1

# Création de la matrice contraintes A 
A = np.zeros((2*t, 3*t + 2))
for j in range(t):
    # Première contrainte : u_j - X(i,j) + (b_i^+ - b_i^-) - s1_j = 0
    A[j, 0] = 1
    A[j, 1] = -1
    A[j, 1 + j] = 1
    A[j, 1 + t + j] = -1

    # Deuxième contrainte : u_j + X(i,j) - (b_i^+ - b_i^-) - s2_j = 0
    A[t + j, 0] = -1
    A[t + j, 1] = 1
    A[t + j, 2 + j] = 1
    A[t + j, 2 + 2*t + j] = -1


bounds = [[0,None] for _ in range(3*t + 2)] #Pas de bornes pour les n+1 variables

# Création de la vidéo optimale sous forme de vecteur
b_opt = np.zeros(p)
"""
for i in range(p):
    b_eq = np.concatenate([X[i, :], -X[i, :]])
    model = linprog(c=c, A_eq=A, b_eq = b_eq, bounds=bounds)
    print(i)

    if model.success:
        #print(model.x[0], " et ", model.x[1])
        b_opt[i] = model.x[0] - model.x[1]
    else:
        print(f"Pixel {i}: {model.message}")

background = b_opt.reshape((n, m)).T    
background = 1 - background
#plt.imsave("background.png", background, cmap='gray'). Sauvegarder le fichier !
plt.imshow(background, cmap='gray')
plt.title("Arrière-plan estimé")
plt.axis('off')
plt.show()
"""