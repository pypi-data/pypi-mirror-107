from scipy.sparse import coo_matrix
import numpy as np

def is_symmetric(m):
    """Check if a sparse matrix is symmetric

    Parameters
    ----------
    m : array or sparse matrix
        A square matrix.

    Returns
    -------
    check : bool
        The check result.

    """
    if m.shape[0] != m.shape[1]:
        raise ValueError('m must be a square matrix')

    if not isinstance(m, coo_matrix):
        m = coo_matrix(m)

    r, c, v = m.row, m.col, m.data
    tril_no_diag = r > c
    triu_no_diag = c > r

    if triu_no_diag.sum() != tril_no_diag.sum():
        return False

    rl = r[tril_no_diag]
    cl = c[tril_no_diag]
    vl = v[tril_no_diag]
    ru = r[triu_no_diag]
    cu = c[triu_no_diag]
    vu = v[triu_no_diag]

    sortl = np.lexsort((cl, rl))
    sortu = np.lexsort((ru, cu))
    vl = vl[sortl]
    vu = vu[sortu]

    check = np.allclose(vl, vu)

    return check

def eigen(A):
    from scipy.sparse.linalg import eigs
    matrix = A.transpose(copy=False)
    evals_large, evecs_large = eigs(matrix, 1, which='LM')
    evals_small, evecs_small = eigs(matrix, 1, sigma=0, which='LM')
    print('largest evalue:', evals_large[0], ', smallest evalue:', evals_small[0], ', condition number:', evals_large[0]/evals_small[0])
    #try:
    #    evals_small, evecs_small = eigs(matrix, 1, which='SM')
    #    print("      ", evals_large, evals_small, evals_large[0]/evals_small[0])
    #except:
    #    print("non transposed version failed!")

def compare(scheme1, scheme2, uh):
    # print(m1.todense())
    # print(m2.todense())
    m1 = scheme1.assemble(uh)
    m2 = scheme2.assemble(uh)

    if not isinstance(m1, coo_matrix):
        m1 = coo_matrix(m1)
    if not isinstance(m2, coo_matrix):
        m2 = coo_matrix(m2)

    #for row, col, value in zip(m1.row, m1.col, m1.data):
    #    print( "({0}, {1}) {2}".format(row, col, value) )
    #for row, col, value in zip(m2.row, m2.col, m2.data):
    #    print( "({0}, {1}) {2}".format(row, col, value) )
    m12 = coo_matrix(m1 - m2)
    #for row, col, value in zip(m12.row, m12.col, m12.data):
    #    print( "({0}, {1}) {2}".format(row, col, value) )
    print(m12)
