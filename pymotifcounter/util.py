"""
PyMotifCounter utility functions.

:author: Athanasios Anastasiou
:date: Nov 2021
"""
from functools import reduce


def motif_id_to_adj_mat(a_motif_id, motif_size):
    """
    Returns the adjacency matrix associated with a particular motif id.

    Notes:
        * In this function it is assumed that the motif id is the number that is formed by flatenning its adjacency
          matrix in row major form.

    :param a_motif_id: An integer number representing a given motif id.
    :type a_motif_id: int
    :param motif_size: The motif size "class" this id is part of.
    :type motif_size: int
    :return:
    """
    bin_rep_size = motif_size ** 2
    adj_mat_str = format(a_motif_id, f"0{bin_rep_size}b")
    adj_mat = []
    for m in range(0, motif_size):
        adj_mat.append(list(map(int, adj_mat_str[(m*motif_size):(m*motif_size)+motif_size])))
    return adj_mat