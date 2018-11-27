# -*- coding: utf-8 -*-
  
"""

This module contains methods for plotting
shear bias results.

:Authors: Martin Kilbinger <martin.kilbinger@cea.fr>
          Arnaud Pujol

:Version: 0.1

:Date: 23/11/2018

"""

import matplotlib
matplotlib.use('Agg')

import pylab as plt

from errors import *


def get_item(x, i):

    if isinstance(x, list):
        try:
            return x[i]
        except IndexError:
            print('List has less than {} items'.format(i))
            #raise
    else:
        return x



def plot_mean_per_bin_several(xvar, xname, yvar, yname, nbins, filter_arr=None, jk_num=50, color='k', marker='s', \
                      ylims=None, leg_loc='upper center', equal_bins=True, linestyle='-', lw=3, leg_ncol=1, \
                      error_mode='jk', out_name=None):
    """Plots various curves of mean and error bars of input data.

    Parameters
    ----------
    xvar: array(float)
        x-values
    xname: string
        x-label
    yvar: [array of] array(float)
        [array of] y-value distributions
    yname: [array of] string
       [array of] name of y, shown in legend
    nbins: int
        number of x bins
    filter_array: array(bool), optional, default=None
         selection in xvar and yvar. If None, use all objects
    jk_num: int, optional, default=50
        number of jackknife subsamples for error bars
    c: [array of] char, optional, default='k'
        [array of] color
    marker: [array of] char, optional, default='s'
        [array of] marker of points
    ylims: array(float, 2)
        y-axis limits
    leg_loc: string, optional, default='upper center'
        position of legend 
    equal_bins: bool, optional, default=True
        if True, each bin has the same number of elements. Otherwise, 
        bins are defined linearly according to the min and max values. 
    linestyle: string, linestyle of the plot. 
    lw: float, optional, default=3
        line width
    leg_ncol: int, optional, default=1
        number of columns in legend
    error_mode: string, optional, default='jk'
        error type, one in 'jk' (jackknife) or 'std' (standard deviation)
    out_name: string, optional, default=None
        if not None, save plot to file out_name.

    Returns
    -------
    x_mean: array of array(float)
        mean x for each bin and sample
    y_mean: array of array(float)
        mean y for each bin and sample
    y_std: array of array(float)
        std y for each bin and sample
    """

    if not filter_arr:
        filter_arr = np.arange(len(xvar))

    xvar_f = xvar[filter_arr]

    nxi = len(yvar)

    x_mean = []
    y_mean = []
    y_std  = []

    for i, yv in enumerate(yvar):

        yv_f = yv[filter_arr]
        yn   = get_item(yname, i)
        c    = get_item(color, i)
        m    = get_item(marker, i)
        ls   = get_item(linestyle, i)

        dxi = (i - (nxi-1)/2)

        xm, ym, ys = plot_mean_per_bin_one(xvar_f, xname, yv_f, yn, nbins, dxi=dxi, jk_num=jk_num, c=c, \
                              marker=m, ylims=ylims, equal_bins=equal_bins, linestyle=ls, lw=lw, \
                              error_mode=error_mode)
        x_mean.append(xm)
        y_mean.append(ym)
        y_std.append(ys)

    plt.legend(loc = leg_loc, frameon = False, fontsize = 10, ncol = leg_ncol)
    plt.savefig(out_name)
    print('Plot saved to {}'.format(out_name))
    plt.show()

    return x_mean, y_mean, y_std



def plot_mean_per_bin_one(xvar, xname, yvar, yname, nbins, filter_arr=None, dxi=0, jk_num=50, c='k', marker='s', \
                      ylims=None, equal_bins=True, linestyle='-', lw=3, error_mode='jk'):
    """Plots mean and error bars of input data.

    Parameters
    ----------
    xvar: array(float)
        x-values
    xname: string
        x-label
    yvar: array(float)
        y-value distributions
    yname: string
       name of y, shown in legend
    nbins: int
        number of x bins
    dxi: int, optional, default=0
        additive x-offset step
    jk_num: int, optional, default=50
        number of jackknife subsamples for error bars
    c: char, optional, default='k'
        color
    marker: char, optional, default='s'
        marker of points
    ylims: array(float, 2)
        y-axis limits
    equal_bins: bool, optional, default=True
        if True, each bin has the same number of elements. Otherwise, 
        bins are defined linearly according to the min and max values. 
    linestyle: string, linestyle of the plot. 
    lw: float, optional, default=3
        line width
    error_mode: string, optional, default='jk'
        error type, one in 'jk' (jackknife) or 'std' (standard deviation)

    Returns
    -------
    x_mean: array(float)
        mean x for each bin
    y_mean, y_std: array(float)
        mean and error of y for each bin
    """

    bin_edges = get_bin_edges(xvar, nbins, equal_bins = equal_bins)
    dx        = (bin_edges[1] - bin_edges[0]) / 20 * dxi

    x_plot = []
    y_plot = []
    err_plot = []

    for i in range(nbins):
        filter_bin = (xvar >= bin_edges[i])*(xvar < bin_edges[i+1])
        if error_mode == 'jk':
            jk_indices = get_jk_indices_1d(xvar[filter_bin], jk_num, rand_order=True)
            sub_mean   = [np.mean(yvar[filter_bin][jk_indeces != j]) for j in range(jk_num)]
            mean       = np.mean(sub_mean)
            err        = jackknife_err(mean, sub_mean)
        elif error_mode == 'std':
            mean = np.mean(yvar[filter_bin])
            err  = np.std(yvar[filter_bin])
        else:
            print("WRONG error_model in plot_mean_per_bin")

        x_plot.append(np.mean(xvar[filter_bin]) + dx)
        y_plot.append(mean)
        err_plot.append(err)

    plt.errorbar(x_plot, y_plot, err_plot, c = c, marker = marker, markersize = 5, label = yname, \
                 linestyle = linestyle, lw = lw)

    if ylims is not None:
        plt.ylim(ylims[0], ylims[1])
    plt.xlabel(xname)
    #plt.ylabel(yname)
    plt.axhline(0, c = 'k', lw = 1)

    return x_plot, y_plot, err_plot

