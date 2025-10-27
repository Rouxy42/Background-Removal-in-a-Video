import numpy as np
from scipy.optimize import linprog
from concurrent.futures import ProcessPoolExecutor

data = np.load("data.npz", allow_pickle=True)
A2_sparse = csr_matrix(data["A2_sparse"].item())  # si c’est sparse LIL, utiliser .item()
c2 = data["c2"]
bounds2 = data["bounds2"]
X = data["X"]

# Définir ici A2_sparse, c2, bounds2, X, p, t

def solve_one_problem(j):
    b_eq = np.concatenate([X[:, j], -X[:, j]])
    model = linprog(c=c2, A_eq=A2_sparse, b_eq=b_eq, bounds=bounds2, method='highs')
    if model.success:
        return model.x[0]
    else:
        print(f"Pixel {j}: {model.message}")
        return np.nan

if __name__ == "__main__":
    import os
    num_cores = min(4, os.cpu_count())  # par exemple 4 coeurs
    t = X.shape[1]

    with ProcessPoolExecutor(max_workers=num_cores) as executor:
        a_opt = list(executor.map(solve_one_problem, range(t)))

    a_opt = np.array(a_opt)
