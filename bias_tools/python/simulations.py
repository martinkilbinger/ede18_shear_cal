# -*- coding: utf-8 -*-
  
"""

This module contains methods for creating image simulations
using galsim

:Authors: Martin Kilbinger <martin.kilbinger@cea.fr>
          Arnaud Pujol

:Version: 0.1

:Date: 23/11/2018

"""


from __future__ import print_function
import os
import sys

import misc


#### great3-like simulations with galsim ###


def count_missing_files(path_format, n):
    """Return the number of missing files i=0..n-1 following file format

    path_format: string including format
        file format
    n: int
        number of files

    Returns
    n_missing: int
        number of missing files
    """

    n_missing = 0
    for i in range(n):
        output_path = path_format % (i, 0)
        if not os.path.exists(output_path):
            n_missing = n_missing + 1

    return n_missing


def create_all_sims_great3(g_list, config_path, config_psf_path, input_dir, output_base_dir, \
                           output_gal_fname_format, output_psf_fname_format, nxy_tiles=None, nfiles=None, job=None):
    """Create great3-like image and PSF simulations using galsim for a list of shears.
    
    g_list: list of array(2, double)
        shear value list
    config_path: string
        path to galsim config file
    config_pst_path: string
        path to galsim PSF config file
    input_dir: string
        base input directory
    output_dir: string
        base output directory
    output_gal_fname_format: string
        output galaxy image file name format
    output_psf_fname_format: string
        output PSF image file name format
    nxy_tiles: int, optional, default=None
        number of postage stamps per direction, if None use default number
        from galsim config file
    nfiles: int, optional, default=None
        number of files, if None use default number from galsim
        config file
    job: class misc.param, optional, default=
        job control

    Returns
    -------
    None
    """

    print('*** Start create_all_sims_great3 ***')

    extra_str = ''
    if nfiles is not None:
        extra_str = '{} output.nfiles={}'.format(extra_str, nfiles)
        
    for g in g_list:
        output_dir = '{}/{}'.format(output_base_dir, misc.get_dir_name_shear(g))
        if not os.path.isdir(output_dir):
            os.makedirs(output_dir)
        
        n_out_missing = count_missing_files('{}/{}'.format(output_dir, output_gal_fname_format), nfiles)
        if n_out_missing > 0:
            print('For shear ({},{}), {} images are missing, running galsim'.format(g[0], g[1], n_out_missing))
            create_sim_one_shear_great3(g, config_path, input_dir, output_dir, \
                                        extra_str, output_gal_fname_format, nxy_tiles=nxy_tiles, job=job)
        else:
            print('For shear ({},{}), all images already exist, skipping galsim call'.format(g[0], g[1]))

    
    # Create PSF
    outdir_psf = '{}/psf'.format(output_base_dir)
    n_out_missing = count_missing_files('{}/{}'.format(outdir_psf, output_psf_fname_format), nfiles)
    if n_out_missing > 0:
        print('{} PSF images are missing, running galsim'.format(n_out_missing))
        galsim_command = 'galsim {0} input.catalog.dir={1} input.dict.dir={1} output.dir={2} output.file_name.format={3}{4}'. \
            format(config_psf_path, input_dir, outdir_psf, output_psf_fname_format, extra_str)
        misc.run_command(galsim_command, job=job)
    else:
        print('All PSF images already exist, skipping galsim call')
    
    print('*** End create_all_sims_great3 ***')
    
    
def create_sim_one_shear_great3(g, config_path, input_dir, output_dir, \
                                extra_str, output_fname_format, nxy_tiles=None, job=None):
    """Create great3-like image simulations for given constant shear by calling galsim.
    
    Parameters
    ----------
    g: array(2, double)
        shear
    config_path: string
        path to galsim config file
    input_dir: string
        base output directory
    output_dir: string
        base output directory
    extra_str: string
        extra options for galsim
    output_fname_format: string
        output file name format
    nxy_tiles: int, optional, default=None
        number of tiles per direction, if None use default number
        from galsim config file
    job: class misc.param, optional, default=
        job control

    Returns
    -------
    None
    """

    if nxy_tiles is not None:
        extra_str = '{0} image.nx_tiles={1} image.ny_tiles={1}'.format(extra_str, nxy_tiles)

    galsim_command = 'galsim {0} gal.shear.g1={1} gal.shear.g2={2} input.catalog.dir={3} input.dict.dir={3} output.dir={4} output.file_name.format={5}{6}'. \
        format(config_path, g[0], g[1], input_dir, output_dir, output_fname_format, extra_str)
    misc.run_command(galsim_command, job=job)



