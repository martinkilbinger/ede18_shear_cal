# -*- coding: utf-8 -*-

"""

This module contains methods to compute errors
of shear biases.

:Authors: Martin Kilbinger <martin.kilbinger@cea.fr>
          Arnaud Pujol

:Version: 0.1

:Date: 23/11/2018

"""

from __future__ import print_function

import numpy as np
from misc import *



def mean_over_shear(results):
    """Return mean of measured galaxy properties over different sheared images.

    Parameters
    ----------
    results: dictionary of class misc.gal_par
        galaxy properties

    Returns
    -------
    res_mean: class misc.gal_par
        mean galaxy properties
    """

    res_mean = None

    for step in results:

        if res_mean is None:
            pass
            res_mean = gal_par.from_gal_par(results[step])
            # TODO coding


    return res_mean


def get_jk_indices_1d(n, jk_num, rand_order=True):
    """Create list of indices 0 .. jk_num-1, filling up an array with length n with distribution
       of indices as equal as possible.
       for a Jackknife error analysis.

    Parameters
    ---------
    n: int
        length of array
    jk_num: int
        number of jackknife samples
    rand_order: bool, optional, default=True
        if True, the indices are returned in random order. 
    
    Returns
    -------
    jk_indices: array of int
        array assigning an index (from 0 to jk_num - 1) to
        each of the data elements. 
    """

    if jk_num > n:
        print('Jackknife number cannot be larger than data length'.format(jk_num, n))

    ratio = n / jk_num + int(n % jk_num > 0)

    jk_indices = np.arange(n, dtype = int)/ratio

    if rand_order:
        np.random.shuffle(jk_indices)

    return jk_indices


def jackknife_err(var, jk_var):
    """Return Jackknife error of var from jk_var subsamples.

    Parameters
    ----------
    var: double or array(double)
        mean value of the variable or length nbins, a constant
    jk_var: np.ndarray(double, jk_dim, nbins))
        2D array of jackknife samples with 0-axis = samples, 1-axis = bins.

    Parameters
    ----------
    jk_err: double or array(double)
        jackknife error of var
    """

    if type(var) == np.ndarray:
        jk_dim = jk_var.shape[0]
        err    = (jk_dim - 1.0) / jk_dim * (jk_var - var)**2
	jk_err = np.sqrt(np.sum(err, axis = 0))
    else:
        jk_dim = len(jk_var)
        err = (jk_dim - 1.0) / jk_dim * (jk_var - var)**2
        jk_err = np.sqrt(np.sum(err))

    return jk_err



def get_bin_edges(array, nbins, equal_bins=True):
    """Return bin edges corresponding to an input array.

    Parameters
    ----------
    array: array(double)
        input values.
    nbins: int
        number of bins.
    equal_bins: bool, optional, default=True
        bins of equal number of elements if True. Otherwise,
        the bin separation is linear

    Returns
    -------
    bin_edges: array(double)
        array of nbins+1 elements.
    """    

    if equal_bins:
        lims = np.linspace(0, len(array[(array < np.inf)]) - 1, nbins + 1)
        lims = np.array(lims, dtype = int)
        bin_edges = np.sort(array[(array < np.inf)])[lims]

        return np.unique(bin_edges)

    else:

        return np.linspace(min(array), max(array), nbins + 1)


