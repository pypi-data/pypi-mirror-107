import numpy as np
import matplotlib.pyplot as plt
from itertools import combinations

def _update_feat_occ_mat(matrix, column_names, ls_of_feats_by_graph):

    ls_of_feats_in_graphs = _unravel_list(ls_of_feats_by_graph)
    unique_feats_in_graphs = np.unique(ls_of_feats_in_graphs)

    # add to the columns names features that have not occured before
    idx_of_new_feats = [feature not in column_names for feature in unique_feats_in_graphs]
    new_feats = unique_feats_in_graphs[idx_of_new_feats]
    column_names_new = np.r_[column_names, new_feats]

    if len(matrix) == 0:
        # Initialise a new matrix if this is the first record
        matrix_new = np.zeros(shape = (len(unique_feats_in_graphs), len(unique_feats_in_graphs)))
    else:
        # Add new zero rows and columns for the new features
        zero_columns = np.zeros(shape = (matrix.shape[0], len(new_feats)))
        matrix_new = np.c_[matrix, zero_columns]
        zero_rows = np.zeros(shape = (len(new_feats), matrix_new.shape[1]))
        matrix_new = np.r_[matrix_new, zero_rows]

    # In each entry add the value of one to the matrix if the features at this index occur in the same graph
    for graph_features in ls_of_feats_by_graph:
        # Find all tuples of two features from a list of features from the graph
        comb_of_pairs = list(combinations(graph_features, 2))
        # Add the repeated tuples for each feature in the graph for the diagonal of the matrix
        tuple_of_repeated_feats = [(feature, feature) for feature in graph_features]
        comb_of_pairs += tuple_of_repeated_feats
        comb_of_pairs = np.array(comb_of_pairs)

        idx1 = [np.where(column_names_new == feat)[0][0] for feat in comb_of_pairs[:,0]]
        idx2 = [np.where(column_names_new == feat)[0][0] for feat in comb_of_pairs[:,1]]

        # Add one to each entry if the features occur in the graph
        matrix_new[idx1, idx2] += 1
        matrix_new[idx2, idx1] += 1
        # Remove the repeated diagonal
        matrix_new[idx1+idx2, idx1+idx2] -= 1

    return matrix_new, column_names_new

def _plot_matrix_heatmap(matrix, column_names, show = 10, figsize = (10,10), ax=None):
    matrix_copy = np.copy(matrix)
    column_names_copy = np.copy(column_names)

    if type(show).__name__ == 'int':
        sort = np.sort(np.argsort(matrix_copy.diagonal())[-show:])
        matrix_copy = matrix_copy[:,sort][sort]
        column_names_copy = np.array(column_names_copy)[sort]

    else:
        raise Exception(f'Can only show an integer amount of features. {show} was passed which has type {type(show).__name__}')

    if ax is None:
        fig, ax = plt.subplots(figsize = figsize)
        fig.tight_layout()


    im = ax.imshow(matrix_copy, cmap = 'feyn-primary')
    ax.figure.colorbar(im, ax=ax)

    ax.set_xticks(range(len(column_names_copy)))
    ax.set_yticks(range(len(column_names_copy)))

    ax.set_xticklabels(column_names_copy)
    ax.set_yticklabels(column_names_copy)
    plt.setp(ax.get_xticklabels(), rotation=45, ha="right",
            rotation_mode="anchor")

    for i in range(len(column_names_copy)):
        for j in range(len(column_names_copy)):
            ax.text(j, i, round(matrix_copy[i, j],2),
                        ha="center", va="center")

    ax.set_title("Frequence of features")
    return ax

def _unravel_list(ls):
    return [item for subitem in ls for item in subitem]