# -*- coding: utf-8 -*-
  
"""

This module contains misc methods.

:Authors: Martin Kilbinger <martin.kilbinger@cea.fr>

:Version: 0.1

:Date: 23/11/2018

"""

from __future__ import print_function
import os
import subprocess
import shlex


class param:
    """General class to store (default) variables
    """

    def __init__(self, **kwds):
        self.__dict__.update(kwds)

    def print(self, **kwds):
        print(self.__dict__)

    def var_list(self, **kwds):
        return vars(self)



def run_command(cmd, job=None, output_path=None):

    if job == None:
        job = param(re_run=True, dry_run=False)

    msg = ''
    run = True

    if output_path is not None and os.path.exists(output_path):

        if job.re_run:
            msg = 'overwriting'

        else:
            msg = 'keeping'
            run = False

        msg = '{} existing file {}, '.format(msg, output_path)

    if job.dry_run == True:
        msg = 'dry run, {}'.format(msg)
        run = False

    if run == True:
        msg = '{}running {}'.format(msg, cmd)
        print(msg)

        #ex = os.system(cmd)
        c = shlex.split(cmd)
        pipe = subprocess.Popen(c, stdout=subprocess.PIPE)
        ex = 0
        while True:
            output = pipe.stdout.readline()
            if output == '' and pipe.poll() is not None:
                break
            if output:
                print(output.strip())
            ex = pipe.poll()

        if ex:
            print('Last call returned error code {}'.format(ex))

    else:
        msg = '{}not running {}'.format(msg, cmd)
        print(msg)


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

