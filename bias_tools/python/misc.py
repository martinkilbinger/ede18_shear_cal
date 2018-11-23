# -*- coding: utf-8 -*-
  
"""

This module contains misc methods.

:Authors: Martin Kilbinger <martin.kilbinger@cea.fr>

:Version: 0.1

:Date: 23/11/2018

"""

from __future__ import print_function
import os


def run_command(cmd):
    print('Running command: {}'.format(cmd))
    ex = os.system(cmd)
    if ex:
        print('Last call returned error code {}'.format(ex))


def get_dir_name_shear(g):
    """Return name of directory with files corresponding to given shear.

    Parameters
    ----------
    g: array(2, double)
        shear/ellipticity

    Returns
    -------
    dir_name: string
        directory name
    """

    dir_name = 'g1_{}_g2_{}'.format(g[0], g[1])

    return dir_name

