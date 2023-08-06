import numpy as np

matrix = np.array(
    [
        [0, 1, 1, 0],
        [0, 0, 1, 0],
        [2, 1, 1, 1],
    ])


for i in range(matrix.shape[1]):
    for j in range(matrix.shape[1]):
        if i != j:
            inner_product = np.inner(matrix[:, i], matrix[:, j])
            norm_i = np.linalg.norm(matrix[:, i])
            norm_j = np.linalg.norm(matrix[:, j])
            if np.abs(inner_product - norm_j * norm_i) < 1E-5:
                print(i, j, 'Dependent')
            else:
                print(i, j, 'Independent')


