"""
PyMotifCounter utility functions.

:author: Athanasios Anastasiou
:date: Nov 2021
"""
import numpy


def adj_mat_to_motif_id(adj_mat):
    """
    Returns the motif-id given an adjacency matrix.

    Notes:
        * As a convention, nodes are numbered clockwise from the top-left. So, if you were trying to get the motif
          ID of some motif in a size 4 Motif class, then the "motif nodes" are assumed to be 0,1,2,3. Anything else is
          simply a transposition of the values of that matrix.

    :param adj_mat: A square adjacency matrix.
    :type adj_mat: numpy.array
    :returns: The motif id
    :rtype: int
    :raises: TypeError of the adjacency matrix is not square or of integer data type.
    """
    # Check that the matrix is square
    mat_shape = adj_mat.shape
    if not isinstance(adj_mat.dtype, type(numpy.dtype('int'))):
        raise TypeError("The adjacency matrix must be of integer data type.")

    if mat_shape[0] != mat_shape[1]:
        raise TypeError("The adjacency matrix must be square.")

    return int("".join([str(k) for k in adj_mat.reshape((mat_shape[0]**2,))]), base=2)


def motif_id_to_adj_mat(a_motif_id, motif_size):
    """
    Returns the adjacency matrix associated with a particular motif id.

    Notes:
        * In this function it is assumed that the motif id is the number that is formed by flattening its adjacency
          matrix in row major form.
        * See `this link <https://www.weizmann.ac.il/mcb/UriAlon/sites/mcb.UriAlon/files/uploads/NetworkMotifsSW/mfinder/motifdictionary.pdf>`_
          for a comprehensive set of examples.
        * This function always returns a **directed** network. To re-create the motif that
          results from an ID of an enumeration over undirected networks, call the function
          with the ID and then call ``.to_undirected()`` (``networkx`` function) on the resulting motif.

    :param a_motif_id: An integer number representing a given motif id.
    :type a_motif_id: int
    :param motif_size: The motif size "class" this id is part of.
    :type motif_size: int
    :return: An adjacency matrix that can be used to create a ``<<networkx.Graph>>`` object.
    :rtype: numpy.array
    """
    bin_rep_size = motif_size ** 2
    adj_mat_str = format(a_motif_id, f"0{bin_rep_size}b")
    adj_mat = []
    for m in range(0, motif_size):
        adj_mat.append(list(map(int, adj_mat_str[(m*motif_size):(m*motif_size)+motif_size])))
    return numpy.array(adj_mat)
    

