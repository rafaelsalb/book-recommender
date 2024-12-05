import numpy as np

def personalized_pagerank(A: np.ndarray, e: np.ndarray, alpha: float = 0.85, max_iter: int = 100, tol: float = 0.001):
    n = A.shape[0]

    # Matriz grau
    D = np.sum(A, axis=1) * np.identity(n)
    D_inv = np.linalg.pinv(D)

    # Matriz de transição
    P = np.dot(A.T, D_inv)

    # Vetor de personalização
    e = e / np.sum(e)

    pr = np.ones(n) / n
    for _ in range(max_iter):
        new_pr = (1.0 - alpha) * np.dot(P, pr) + alpha * e # no PageRank convencional, 'e' seria apenas um vetor uniforme de 1/n
        l1_err = np.linalg.norm(new_pr - pr, ord=1) # norma L1
        if l1_err < tol:
            break
        pr = new_pr

    return pr, l1_err
