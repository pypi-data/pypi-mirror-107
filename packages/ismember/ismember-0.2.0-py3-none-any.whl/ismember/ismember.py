# --------------------------------------------------------------------------
# Name        : ismember.py
# Author      : E.Taskesen
# Contact     : erdogan@gmail.com
# --------------------------------------------------------------------------

import numpy as np

# %% ismember
def ismember(a_vec, b_vec, method=None):
    """Ismember: MATLAB equivalent function

    Description
    -----------
    MATLAB equivalent ismember function
    [LIA, LOCB] = ISMEMBER(A,B) also returns an array LOCB containing the
    lowest absolute index in B for each element in A which is a member of
    B and 0 if there is no such index.

    Parameters
    ----------
    a_vec : list or array
    b_vec : list or array
    method : [None, 'rows', 'elementwise'] (default: None).
        'elementwise': Element wise matrice comparison
        'rows': Row-wise matrice comparison.

    Returns an array containing logical 1 (true) where the data in A is found 
    in B. Elsewhere, the array contains logical 0 (false)
    -------
    Tuple

    Example
    -------
    >>> a_vec = np.array([1,2,3,None])
    >>> b_vec = np.array([4,1,2])
    >>> Iloc, idx = ismember(a_vec,b_vec)
    >>> a_vec[Iloc] == b_vec[idx]
    >>>
    >>> # Row wise comparison
    >>> a_vec = np.array(((1, 2, 3), (4, 5, 6), (7, 8, 9), (10, 11, 12)))
    >>> b_vec = np.array(((4, 5, 6), (7, 8, 0)))
    >>> Iloc, idx = ismember(a_vec, b_vec, 'rows')
    >>>

    """

    # Append nan to b_vec to make shape similar
    if (method=='elementwise') and (a_vec.shape[0]>b_vec.shape[0]):
        nanrows = [[0]*b_vec.shape[1]] * (a_vec.shape[0] - b_vec.shape[0])
        b_vec = np.concatenate((b_vec, nanrows))

    # Set types
    a_vec, b_vec = _settypes(a_vec, b_vec)

    # Compute
    if method is None:
        Iloc, idx = _compute(a_vec, b_vec)
    elif method=='rows':
        Iloc, idx = _row_wise(a_vec, b_vec)
    elif method=='elementwise':
        # if a_vec.shape[0]!=b_vec.shape[0]: raise Exception('Error: Input matrices should have same number of rows.')
        # Compute row-wise over the matrices
        out = list(map(lambda x,y: _compute(x,y), a_vec, b_vec))
        # Unzipping
        Iloc, idx = list(zip(*out))
    else:
        Iloc, idx = None, None

    return(Iloc, idx)


# %% Typing
def _row_wise(a_vec, b_vec):
    Iloc = np.zeros(a_vec.shape[0]).astype(bool)
    idx = np.zeros(a_vec.shape[0])*np.nan
    for vec in enumerate(a_vec):
        I, _ = _compute(vec[1], b_vec)
        if np.all(I):
            Iloc[vec[0]]=True
            idx[vec[0]]=vec[0]

    return Iloc, idx

# %% Typing
def _settypes(a_vec, b_vec):
    if 'pandas' in str(type(a_vec)):
         a_vec.values[np.where(a_vec.values==None)]='NaN'
         a_vec = np.array(a_vec.values)
    if 'pandas' in str(type(b_vec)):
         b_vec.values[np.where(b_vec.values==None)]='NaN'
         b_vec = np.array(b_vec.values)
    if isinstance(a_vec, list):
        a_vec=np.array(a_vec)
        # a_vec[a_vec==None]='NaN'
    if isinstance(b_vec, list):
        b_vec=np.array(b_vec)
        # b_vec[b_vec==None]='NaN'

    return a_vec, b_vec


# %% Compute
def _compute(a_vec, b_vec):
    bool_ind = np.isin(a_vec,b_vec)
    common = a_vec[bool_ind]
    [common_unique, common_inv] = np.unique(common, return_inverse=True)
    [b_unique, b_ind] = np.unique(b_vec, return_index=True)
    common_ind = b_ind[np.isin(b_unique, common_unique, assume_unique=True)]
    return bool_ind, common_ind[common_inv]