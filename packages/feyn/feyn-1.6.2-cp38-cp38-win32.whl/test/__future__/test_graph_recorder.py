from typing import Collection
import unittest
from unittest.case import TestCase
import pytest

import numpy as np

from feyn.__future__.contrib.recorder import GraphRecorder
from feyn.__future__.contrib.recorder._feat_occ import _update_feat_occ_mat
from feyn.__future__.contrib.recorder._barcode import _convert_record_to_barcode

class Test_update_feat_freq_mat(unittest.TestCase):
    def setUp(self):
        self.ls_of_feat_by_graph = [['x1', 'x2'], ['x2', 'x3']]

    def test_empty_matrix_empty_columns(self):
        matrix = []
        column_names = []
        update_matrix = _update_feat_occ_mat(matrix, column_names, self.ls_of_feat_by_graph)
        actual_mat = np.array([
            [1,1,0],
            [1,2,1],
            [0,1,1]
        ])
        actual_col_names = np.array(['x1', 'x2', 'x3'])
        assert (update_matrix[0] == actual_mat).all()
        assert (update_matrix[1] == actual_col_names).all()

    def test_update_of_empty_matrix_empty_columns_three_graphs(self):
        matrix = []
        column_names = []
        ls_of_feat_by_graph = [['x1', 'x2'],['x3', 'x4', 'x1'], ['x5', 'x1']]
        update_matrix = _update_feat_occ_mat(matrix, column_names, ls_of_feat_by_graph)

        actual_mat = np.array([
            [3, 1, 1, 1, 1],
            [1, 1, 0, 0, 0],
            [1, 0, 1, 1, 0],
            [1, 0, 1, 1, 0],
            [1, 0, 0, 0, 1]
            ])
        actual_column_names = np.array(['x1', 'x2', 'x3', 'x4', 'x5'])
        assert (update_matrix[0] == actual_mat).all()
        assert (update_matrix[1] == actual_column_names).all()

    def test_update_of_empty_matrix_empty_columns_sing_feat_graphs(self):
        matrix = []
        column_names = []
        ls_of_feats_by_graph = [['x1']]
        update_matrix = _update_feat_occ_mat(matrix, column_names, ls_of_feats_by_graph)
        actual_mat = np.array([
            [1]
        ])
        actual_column_names = np.array(['x1'])
        assert (update_matrix[0] == actual_mat).all()
        assert (update_matrix[1] == actual_column_names).all()

    def test_update_matrix_no_new_feats(self):
        matrix = np.array([
            [1,0,0],
            [0,2,1],
            [0,1,1]
        ])
        column_names = np.array(['x1', 'x2', 'x3'])
        update_matrix = _update_feat_occ_mat(matrix, column_names, self.ls_of_feat_by_graph)
        actual_mat = np.array([
            [2,1,0],
            [1,4,2],
            [0,2,2]
        ])
        actual_col_names = np.array(['x1', 'x2', 'x3'])
        assert (update_matrix[0] == actual_mat).all()
        assert (update_matrix[1] == actual_col_names).all()

    def test_update_matrix_new_feats(self):
        matrix = np.array([
            [1,1],
            [1,2]
        ])
        column_names = np.array(['x1', 'x2'])
        update_matrix = _update_feat_occ_mat(matrix, column_names, self.ls_of_feat_by_graph)
        actual_mat = np.array([
            [2,2,0],
            [2,4,1],
            [0,1,1]
        ])
        actual_col_names = np.array(['x1', 'x2', 'x3'])

        assert (update_matrix[0] == actual_mat).all()
        assert (update_matrix[1] == actual_col_names).all()

    def test_conver_record_to_barcode_single_record(self):
        record = [(np.arange(9).reshape((3,3)), np.array(['x1', 'x2', 'x3']))]
        barcode_array = _convert_record_to_barcode(record)
        assert (barcode_array == np.array([0,4,8])).all()

    def test_conver_record_to_barcode_multiple_record_same_feats(self):
        record = [(np.arange(9).reshape((3,3)), np.array(['x1', 'x2', 'x3'])), (np.arange(10,19).reshape((3,3)), np.array(['x1', 'x2', 'x3']))]
        barcode_array = _convert_record_to_barcode(record)
        actuals = np.array([[0,4,8],[10,10,10]])
        assert (barcode_array == actuals).all()

    def test_conver_record_to_barcode_multiple_record_diff_feats(self):
        record = [
            (np.arange(9).reshape((3,3)), np.array(['x1', 'x2', 'x3'])),
            (np.arange(1,26).reshape((5,5)), np.array(['x1', 'x2', 'x3', 'x4', 'x5'])),
            ]
        barcode_array = _convert_record_to_barcode(record)
        actuals = np.array([
            [0,4,8,0,0],
            [1,3,5,19,25]
        ])
        assert (barcode_array == actuals).all()

    def test_record_graphs_to_empty_record(self):
        gr = GraphRecorder(feature_occurrence= True)
        graph1 = FakeGraph(['x1', 'x2', 'x3'])
        graph2 = FakeGraph(['x2', 'x3', 'x4'])
        gr.record_graphs([graph1, graph2])

        actual_record = [(np.array([
            [1, 1, 1, 0],
            [1, 2, 2, 1],
            [1, 2, 2, 1],
            [0, 1, 1, 1]
        ]), np.array(['x1', 'x2', 'x3', 'x4']))]

        assert (gr._feature_occurrence[0][0] == actual_record[0][0]).all()
        assert (gr._feature_occurrence[0][1] == actual_record[0][1]).all()

class FakeGraph:
    def __init__(self, features):
        self.features = features
