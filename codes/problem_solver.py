import numpy as np
from scipy.optimize import linprog

def one_problem_solve(j, c, A2_sparse, bounds, X):
    print(f"----- Début du calcul {j+1} -----")
    b_eq = np.concatenate([X[:, j], -X[:, j]])
    model2 = linprog(
        c = c,
        A_eq=A2_sparse,
        b_eq=b_eq,
        bounds=bounds,
        method='highs-ipm'
    )

    if model2.success:
        return model2.x[0]
    else:
        print(f"Erreur dans le problème {j}")
