import numpy as np

def personalized_pagerank(adj_matrix, personalization, alpha=0.85, max_iter=100, tol=1e-6):
    N = adj_matrix.shape[0]

    out_degree = adj_matrix.sum(axis=1)
    transition_matrix = adj_matrix / out_degree[:, None]
    transition_matrix = np.nan_to_num(transition_matrix)

    pr = np.ones(N) / N

    for _ in range(max_iter):
        pr_new = alpha * np.dot(transition_matrix.T, pr) + (1 - alpha) * personalization
        if np.linalg.norm(pr_new - pr, ord=1) < tol:
            break
        pr = pr_new

    return pr
