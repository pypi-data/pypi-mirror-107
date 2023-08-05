import numpy as np


def gini_coefficient(list_, precision: int = None):
    """
    This function calculates gini coefficient (index) for a list, series,
    array or an analogous collections of numbers.

    Parameters:
        list_ : list
            List, series or array of numerical values
        precision : int
            Number of digits after decimal separator which are to be returned
    Returns:
        gini : float
            Values of gini coefficient

    Examples:
        >>> gini_coefficient([1, 3, 5])
        0.2962962962962963

        >>> gini_coefficient([1, 3, 5], 3)
        0.296
    """
    list_ = list(list_)

    if not (type(list_) == list and
            all([is_numeric(item) for item in list_])):
        raise TypeError("Parameter 'list_' should be a list of numeric values")

    if precision is not None and not type(precision) == int:
        raise TypeError("Parameter 'precision' should be an integer")

    mean_absolute_difference = np.abs(np.subtract.outer(list_, list_)).mean()
    relative_mean_absolute_difference = mean_absolute_difference / np.mean(list_)
    gini = 0.5 * relative_mean_absolute_difference
    if precision is not None:
        gini = round(gini, precision)

    return gini


def is_numeric(x):
    """
    This function checks if the input value is a numerical value such as:
    int, float, np.int, np.float

    Examples:
         >>> is_numeric(2.1)
         True

         >>> is_numeric("abc")
         False
    """
    if isinstance(x, (int, float, np.integer, np.float)):
        return True
    else:
        return False
