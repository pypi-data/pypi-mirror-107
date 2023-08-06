from numpy import ndarray
def check_not_2D(X):
    """
    X: ndarray
    """
    if len(X.shape) == 2:
        return False
    else:
        return True
def check_is_1D(X):
    """
    X: ndarray
    """
    if len(X.shape) == 1:
        return True
    else:
        return False
def check_2D(X):
    """
    X: ndarray
    """
    if len(X.shape) == 2:
        return True
    else:
        return False
def is_regressor(X):
    if len(set(X)) > 8:
        return True
def ensure_ndarray(X):
    if isinstance(X, ndarray):
        return X
    elif isinstance(X, list):
        return ndarray(X)
    elif X is None:
        return X
    else:
        try:
            return X.values
        except:
            print("Unknown data type")
def ensure_1d(X):
    if isinstance(X, ndarray):
        if len(X.shape) == 1:
            return X
        else:
            return X.reshape(-1, )
    elif X is None:
        return X