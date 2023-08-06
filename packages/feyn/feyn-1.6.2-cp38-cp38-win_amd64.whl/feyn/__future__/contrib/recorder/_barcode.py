import numpy as np
import matplotlib.pyplot as plt

def _plot_barcode(array, column_names, show = 10, figsize = (6,6), ax=None):
    array_copy = np.copy(array)
    column_names_copy = np.copy(column_names)

    array_sum = array_copy.sum(axis=0)
    sort = np.argsort(array_sum)[-show:]
    idx_to_show = np.sort(sort)
    array_copy = array_copy[:,idx_to_show]
    column_names_copy = column_names_copy[idx_to_show]

    if ax is None:
        fig, ax = plt.subplots(figsize = figsize)

    for ix in range(len(column_names_copy)):
        for jx, amount in enumerate(array_copy[:, ix]):
            ax.plot([jx, jx+1], [ix,ix], c='k', lw = amount)

    ax.set_title('Barcode plot of feature occurrence')
    ax.set_yticks(range(len(column_names_copy)))
    ax.set_xticks(range(1, array_copy.shape[0]+1))
    ax.set_yticklabels(column_names_copy)
    ax.set_xlabel('Epochs')
    ax.set_ylabel('Features')
    fig.tight_layout()

    return ax

def _convert_record_to_barcode(record):
    columns_names = np.copy(record[-1][1])
    barcode_array = np.copy(record[0][0].diagonal())

    if len(record[0][1]) < len(columns_names):
        no_missing_feats = len(columns_names) - len(record[0][1])
        barcode_array = np.r_[barcode_array,np.zeros(no_missing_feats)]

    for ix in range(1,len(record)):
        occ_cum_sum_epoch = record[ix][0].diagonal()
        no_missing_feats = len(columns_names) - len(occ_cum_sum_epoch)
        occ_cum_sum_epoch = np.r_[occ_cum_sum_epoch, np.zeros(no_missing_feats)]

        occ_cum_sum_prev_epoch = record[ix-1][0].diagonal()
        no_missing_feats = len(columns_names) - len(occ_cum_sum_prev_epoch)
        occ_cum_sum_prev_epoch = np.r_[occ_cum_sum_prev_epoch, np.zeros(no_missing_feats)]

        row = np.subtract(occ_cum_sum_epoch, occ_cum_sum_prev_epoch)
        barcode_array = np.r_['0,2', barcode_array, row]

    return barcode_array