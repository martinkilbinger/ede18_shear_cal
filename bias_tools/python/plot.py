# -*- coding: utf-8 -*-
  
"""

This module contains methods for plotting
shear bias results.

:Authors: Martin Kilbinger <martin.kilbinger@cea.fr>
          Arnaud Pujol

:Version: 0.1

:Date: 23/11/2018

"""


def plot_mean_per_bin(xvar, xname, yvar, yname, nbins, filter_arr, jk_num=50, c='k', show=True, marker='s', ylims=None, leg_loc='upper center', \
    equal_bins=True, linestyle= '-', lw=3, leg_ncol=1, error_mode='jk', save=False, out_name='/tmp/plot.pdf', get_out=False):
    """Plots mean and error bars of input data.

    Parameters
    ----------
    xvar: array(double)
        x-values
    xname: string
        x-label
    yvar: array, variable which mean is calculated in each x bin. 
    yname: string, name of the variable, shown in the legend. 
    nbins: integer, specifies the number of x bins used. 
    filter_array: boolean array which defines a selection of the objects in 
    xvar and yvar. 
    jk_num: integer, number of Jack-Knife subsamples used to calculate the error bars.
    c: colour of the error bars and points used.
    show: if True, it shows the plot.
    marker: marker of plotted points.
    ylims: None or [a,b], defining (if not None0 the y axes limits.
    leg_loc: position of legend. 
    equal_bins: if True, each bin has the same number of elements. Otherwise, 
        bins are defined linearly according to the min and max values. 
    linestyle: string, linestyle of the plot. 
    lw: float, line width of the plot.
    leg_ncol: integer, number of columns in the legend.
    error_mode: 'jk' or 'std', specifies if the errors are JK or the standard deviation. 
    save: if True, it saves the plots. 
    out_name: name of the output plot file. 
    get_out: if True, it returns the mean xvar, mean yvar and its error.
    Output:
    It generates a plot that can be saved and/or shown if specified. 
    x_plot: mean x for each bin. 
    y_plot, err_plot: mean y for each bin and its error.
    """
    xvar_f = xvar[filter_arr]
    yvar_f = yvar[filter_arr]
    bin_edges = get_bin_edges(xvar_f, nbins, equal_bins = equal_bins)
    nbins = len(bin_edges) - 1
    random_amplitude = (bin_edges[1] - bin_edges[0])/20.
    x_plot = []
    y_plot = []
    err_plot = []
    for i in range(nbins):
        filter_bin = (xvar_f >= bin_edges[i])*(xvar_f < bin_edges[i+1])
        jk_indeces = get_jk_indeces_1d(xvar_f[filter_bin], jk_num)
        np.random.shuffle(jk_indeces)
        if error_mode == 'jk':
            sub_mean = [np.mean(yvar_f[filter_bin][jk_indeces != j]) for j in range(jk_num)]
            mean = np.mean(sub_mean)
            err = jack_knife(mean, sub_mean)
        elif error_mode == 'std':
            mean = np.mean(yvar_f[filter_bin])
            err = np.std(yvar_f[filter_bin])
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
    if get_out:
        return x_plot, y_plot, err_plot
