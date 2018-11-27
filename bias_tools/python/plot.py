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


def plot_mean_per_bin(xvar, xname, yvar, yname, nbins, filter_arr=None, jk_num=50, c='k', show=True, marker='s', \
                      ylims=None, leg_loc='upper center', equal_bins=True, linestyle= '-', lw=3, leg_ncol=1, \
                      error_mode='jk', save=False, out_name='/tmp/plot.pdf'):
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
    filter_array: array(bool), optional, default=None
         selection in xvar and yvar. If None, use all objects
    jk_num: int, optional, default=50
        number of jackknife subsamples for error bars
    c: char, optional, default='k'
        color
    show: bool, optional, default=True
        show plot if True
    marker: char, optional, default='s'
        marker of points
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
    save: bool, optional, default=False
        save the plot to file if True
    out_name: string, optional, default='/tmp/plot.pdf'
        output plot file name

    Returns
    -------
    x_plot: array(float)
        mean x for each bin
    y_plot, err_plot: array(float)
        mean and error of y for each bin
    """

    if filter_arr:
        xvar_f = xvar[filter_arr]
        yvar_f = yvar[filter_arr]
    else:
        xvar_f = xvar
        yvar_f = yvar

    bin_edges = get_bin_edges(xvar_f, nbins, equal_bins = equal_bins)
    nbins = len(bin_edges) - 1
    random_amplitude = (bin_edges[1] - bin_edges[0])/20.

    x_plot = []
    y_plot = []
    err_plot = []

    for i in range(nbins):
        filter_bin = (xvar_f >= bin_edges[i])*(xvar_f < bin_edges[i+1])
        if error_mode == 'jk':
            jk_indices = get_jk_indices_1d(xvar_f[filter_bin], jk_num, rand_order=True)
            sub_mean   = [np.mean(yvar_f[filter_bin][jk_indeces != j]) for j in range(jk_num)]
            mean       = np.mean(sub_mean)
            err        = jackknife_err(mean, sub_mean)
        elif error_mode == 'std':
            mean = np.mean(yvar_f[filter_bin])
            err  = np.std(yvar_f[filter_bin])
        else:
            print("WRONG error_model in plot_mean_per_bin")

        rand =  np.random.random()*random_amplitude
        x_plot.append(np.mean(xvar_f[filter_bin]) + rand)
        y_plot.append(mean)
        err_plot.append(err)

    plt.errorbar(x_plot, y_plot, err_plot, c = c, marker = marker, markersize = 5, label = yname, linestyle = linestyle, lw = lw)

    if ylims is not None:
        plt.ylim(ylims[0], ylims[1])
    plt.xlabel(xname)
    #plt.ylabel(yname)
    plt.axhline(0, c = 'k', lw = 1)

    if show:
        plt.legend(loc = leg_loc, frameon = False, fontsize = 10, ncol = leg_ncol)
        if save:
            plt.savefig(out_name)
            print("Plot saved in " + out_name)
        plt.show()

    return x_plot, y_plot, err_plot
