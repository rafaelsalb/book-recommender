import numpy as np

def colors_from_ranking(ranking: np.ndarray, liked: bool) -> np.ndarray:
    colors = np.ones((len(ranking), 2))
    colors[:, 0] = ranking / np.max(ranking)
    colors[:, 1] = 1.0 if liked else 0.0
    return colors
