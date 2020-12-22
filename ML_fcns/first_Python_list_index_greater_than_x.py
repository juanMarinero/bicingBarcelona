import numpy as np


def first_Python_list_index_greater_than_x(L, v_min=0.9, n_components_min=0):
    L = list(L)
    try:
        index = next(i for i, v in enumerate(L) if v > v_min)
    except StopIteration:
        #  print(f"No element greater than {v_min} !!")
        return (None, None)

    i_max = len(L) - 1
    if i_max < (n_components_min - 1):
        n_components_min = i_max + 1  # n_components_min too high corrected

    n_components = np.max([index + 1, n_components_min])

    float_formatter = "{:.1f}".format
    np.set_printoptions(formatter={"float_kind": float_formatter})
    #  print(f"explained_variance_ratio__cum (till {v_min*100}%): ", end=" ")
    #  print(np.array(L[:n_components]) * 100)

    return (index, n_components)
