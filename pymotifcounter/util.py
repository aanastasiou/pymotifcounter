"""
PyMotifCounter utility functions.

:author: Athanasios Anastasiou
:date: Nov 2021
"""
import numpy
import copy


def adj_mat_to_motif_id_perm(adj_mat):
    """
    Returns all motif-ids that result from permutations of the adjacency matrix.

    """
    master_adj_mat_copy =
    pass


def adj_mat_to_motif_id(adj_mat):
    """

    """
    # Check that the matrix is square
    mat_shape = adj_mat.shape
    if mat_shape[0]!=mat_shape[1]:
        # Raise exception
        pass
    else:
        return int("".join([str(k) for k in adj_mat.reshape((mat_shape[0]**2,))]), base=2)


def motif_id_to_adj_mat(a_motif_id, motif_size):
    """
    Returns the adjacency matrix associated with a particular motif id.

    Notes:
        * In this function it is assumed that the motif id is the number that is formed by flatenning its adjacency
          matrix in row major form.
        * See `this link <https://www.weizmann.ac.il/mcb/UriAlon/sites/mcb.UriAlon/files/uploads/NetworkMotifsSW/mfinder/motifdictionary.pdf>`_
          for a comprehensive set of examples.
        * This function returns a **directed** network. To re-create the motif that 
          results from an ID of an enumeration over undirected networks, call the function
          with the ID and then call ``.to_undirected()`` on the resulting motif.

    :param a_motif_id: An integer number representing a given motif id.
    :type a_motif_id: int
    :param motif_size: The motif size "class" this id is part of.
    :type motif_size: int
    :return: An adjacency matrix that can be used to create a ``<<networkx.Graph>>`` object.
    :rtype: numpy.ndarray
    """
    bin_rep_size = motif_size ** 2
    adj_mat_str = format(a_motif_id, f"0{bin_rep_size}b")
    adj_mat = []
    for m in range(0, motif_size):
        adj_mat.append(list(map(int, adj_mat_str[(m*motif_size):(m*motif_size)+motif_size])))
    return numpy.array(adj_mat)
    

