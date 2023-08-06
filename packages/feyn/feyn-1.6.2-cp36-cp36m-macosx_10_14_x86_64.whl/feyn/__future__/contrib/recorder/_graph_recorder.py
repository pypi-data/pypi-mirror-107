from collections import Counter
from ._feat_occ import _update_feat_occ_mat, _plot_matrix_heatmap
from ._barcode import _convert_record_to_barcode, _plot_barcode

import numpy as np
import matplotlib.pyplot as plt

class GraphRecorder:
    """The Graph Recorder object allows you to collect information during each fitting loop.
       This is used typically to record the information in the best graphs within the fitting loop:
       >>> gr = GraphRecorder(feature_occurrence = True)
       >>> for _ in range(10):
       >>>     qgraph.fit(data)
       >>>     gr.add_graphs(qgraph.best())
       >>>     ql.update(qgraph.best())
       Arguments:
           feature_occurrence {bool} -- Records feature occurrence on the recorder object. This enables the methods plot_feature_occurrence, plot_barcode
    """

    def __init__(self, feature_occurrence = True):
        """Constructs a new GraphRecorder object

        Keyword Arguments:
            feature_occurrence {bool} --  Records feature occurrence on the recorder object. This enables the methods plot_feature_occurrence, plot_barcode (default: {True})
        """
        self._record_feature_occurrence = feature_occurrence
        self._feature_occurrence = []

    def record_graphs(self, graphs):
        """This records relevant information from the graphs to the internal state based on the choice of the init function.

        Arguments:
            graphs {List(feyn.Graph)} -- List of feyn.Graphs to record information for
        """
        if self._record_feature_occurrence:
            if len(self._feature_occurrence) == 0:
                matrix = []
                column_names = []
            else:
                matrix = self._feature_occurrence[-1][0]
                column_names = self._feature_occurrence[-1][1]

            ls_of_feat_by_graph = []
            for graph in graphs:
                ls_of_feat_by_graph.append(graph.features)

            self._feature_occurrence.append(_update_feat_occ_mat(matrix, column_names, ls_of_feat_by_graph))

    def plot_feature_occurrence(self, show = 10, figsize = (10,10), ax=None):
        """This plots a heatmap of features occuring in the graphs recorded.

        Keyword Arguments:
            show {int} -- Only show the top <show> occurring features (default: {10})
            figsize {tuple} -- matplotlib figsize (default: {(10,10)})
            ax {matplotlib.axes.Axes} -- Matplotlib axes (default: {None})

        Raises:
            Exception: If GraphRecorder has not recorded the feature occurrence

        Returns:
            {matplotlib.axes.Axes} -- Matplotlib axes
        """
        if not self._record_feature_occurrence:
            raise Exception('Only suitable for "feature occurrence" recording types.')

        ax = _plot_matrix_heatmap(self._feature_occurrence[-1][0], self._feature_occurrence[-1][1], show, figsize, ax)
        return ax

    def plot_barcode(self, show = 10, figsize = (6,6), ax=None):
        """This plots the barcode of features occuring throughout the fitting loop of the graphs recorded

        Keyword Arguments:
            show {int} -- Only show the top <show> occurring features (default: {10})
            figsize {tuple} -- matplotlib figsize (default: {(10,10)})
            ax {matplotlib.axes.Axes} -- Matplotlib axes (default: {None})

        Raises:
            Exception: If GraphRecorder has not recorded the feature occurrence

        Returns:
            {matplotlib.axes.Axes} -- Matplotlib axes
        """
        if not self._record_feature_occurrence:
            raise Exception('This is only suitable for a "feature occurrence" recorder.')

        barcode_array = _convert_record_to_barcode(self._feature_occurrence)
        column_names = self._feature_occurrence[-1][1]
        return _plot_barcode(barcode_array, column_names, show, figsize, ax)

    @staticmethod
    def _unravel_list(ls):
        return [item for subitem in ls for item in subitem]