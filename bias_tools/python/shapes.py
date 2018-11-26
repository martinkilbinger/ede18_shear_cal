# -*- coding: utf-8 -*-
  
"""

This module contains methods for measuring shapes
of galaxy images using shapelens.

:Authors: Martin Kilbinger <martin.kilbinger@cea.fr>
          Arnaud Pujol

:Version: 0.1

:Date: 23/11/2018

"""


from __future__ import print_function

import os
import numpy as np

import misc



class gal_par:
    """Measured parameters of a galaxy sample.
    """

    def __init__(self, idn, e1, e2, scale, sn, beta, q, ep, ex):

        self.idn   = idn
        self.e1    = e1
        self.e2    = e2
        self.scale = scale
        self.sn    = sn
        self.beta  = beta
        self.q     = q
        self.ep    = ep
        self.ex    = ex



def get_slope(x, y):
    return y/x


def all_shapes_shapelens(g_values, input_base_dir, output_base_path, nfiles, job=None):
    """Measure galaxy shapes in simulated images with various shear by
       calling shapelens (get-shapes).

    Parameters
    ----------
    g_values: list of array(2, double)
        shear value list
    input_base_dir: string
        base input directory
    output_base_path: string
        output base directory name 
    nfiles: int, optional, default=None
        number of files, if None use default number from galsim
        config file
    job: class misc.param, optional, default=
        job control

    Returns
    -------
    None
    """

    for i in range(nfiles):
    
        input_psf_path = '{}/psf/starfield_image-{:03d}-0.fits'.format(input_base_dir, i)

        for g in g_values:

            dir_name_shear = misc.get_dir_name_shear(g)
            input_gal_path = '{}/{}/image-{:03d}-0.fits'.format(input_base_dir, dir_name_shear, i)
            output_dir    = '{}/{}'.format(output_base_path, dir_name_shear)
            if not os.path.isdir(output_dir):
                os.makedirs(output_dir)

            output_path = '{}/result-{:03d}.txt'.format(output_dir, i)
            shapes_one_image(input_gal_path, input_psf_path, output_path, job)



def shapes_one_image(input_gal_path, input_psf_path, output_path, job):
    """Measure galaxy shapes in simulated image.

    Parameters
    ----------
    input_gal_path: string
        input file name with galaxy images
    input_psf_path: string
        input psf file name
    output_path: string
        output path
    job: class misc.param, optional, default=
        job control

    Returns
    -------
    None
    """

    ksb_command = 'get_shapes -T -p {} {} > {}'.format(input_psf_path, input_gal_path, output_path)
    misc.run_command(ksb_command, job=job, output_path=output_path)



def get_ksb(file_list, psf_path):
    """Read and return KSB results from files.
    
    Parameters
    ----------
    file_list: list of strings
        image files with measured shapes and other quantities.
    psf_path: string
        directory where PSE output of the PSF is saved.
    
    Returns
    -------
    results: class gal_par
        galaxy parameters
    """
    
    final_gal_id = np.array([])
    final_e1 = np.array([])
    final_e2 = np.array([])
    out_scale = np.array([])
    out_sn = np.array([])
    psf_theta = np.array([])

    for filename in file_list:

        # Galaxy parameters
        data = np.loadtxt(filename, usecols = (0,3,4,5,6))
        final_gal_id = np.append(final_gal_id, data[:,0])
        final_e1 = np.append(final_e1, data[:,1])
        final_e2 = np.append(final_e2, data[:,2])
        out_scale = np.append(out_scale, data[:,3])
        out_sn = np.append(out_sn, data[:,4])

        # PSF parameters
        pse_file = psf_path + 'starfield_image-' + file_list[0][-7:-4] + '-0.cat' #TODO change to subfield_image
        psf_theta = np.append(psf_theta, np.loadtxt(pse_file)[:,10]/360.*2*np.pi)

    out_beta, out_q = g2bq(final_e1, final_e2)
    out_beta = correct_radians(out_beta)
    final_ep, final_ex = e12_2_epx(final_e1, final_e2, psf_theta)

    results = gal_par(final_gal_id, final_e1, final_e2, out_scale, out_sn, out_beta, out_q, final_ep, final_ex)

    return results



def e12_2_epx(e1, e2, beta):
    """Rotate ellipticity into the PSF orientation reference frame.

    Parameters
    ----------
    e1, e2: double
        ellipticy/shear Cartesian components
    beta: double
        orientation of the PSF.

    Returns
    -------
    ep, ex: double
        ellipticity/shear tangential and radial components
    """

    in_beta, in_q = g2bq(e1, e2)
    out_beta = correct_radians(in_beta - beta)
    ep, ex = bq2g(correct_radians(out_beta), in_q)

    return ep, ex



def g2bq(g1, g2):
    """Translate the ellipticities from g1, g2 to beta, q terms.
    
    Parameters
    ----------
    g1, g2: double
        components of the ellipticity/shear
    
    Returns
    -------
    beta, q: double
        ellipticity in beta, q terms
    """
    
    beta = np.arctan2(g2,g1)/2.
    g = np.sqrt(g1**2. + g2**2.)
    q = (1 - g)/(1 + g)

    return beta, q



def correct_radians(angular_array):
    """
    Map array of angules in radians to [0; pi]. Iterative calls.
    
    Parameters
    ----------
    angular_array: array of float
        angles [rad]
        
    Returns
    -------
    corrected_radians: array of float
        angles [rad] within [0; pi]
    """
    
    corrected_radians = np.copy(angular_array)
    while np.sum(corrected_radians > np.pi) > 0:
        corrected_radians[corrected_radians > np.pi] = corrected_radians[corrected_radians > np.pi] - np.pi
    while np.sum(corrected_radians < 0) > 0:
        corrected_radians[corrected_radians < 0] = corrected_radians[corrected_radians < 0] + np.pi
    return corrected_radians



def shear_response(results, dg, output_dir=None):
    """Return shear response matrix.

    Parameters
    ----------
    results: dictionary of lists
        results for different shear values
    output_dir: string, optional, default=None
        output_dir, if None, do not write response to file

    Returns
    -------
    R: matrix(2, 2) of double
        shear response matrix
    """

    R = np.zeros((2,2))

    if len(results) == 4:

        R[0,0] = get_slope(2 * dg, results[(+1, 0)].e1 - results[(-1, 0)].e1)
        R[1,1] = get_slope(2 * dg, results[(0, +1)].e2 - results[(0, -1)].e2)
        R[0,1] = get_slope(2 * dg, results[(0, +1)].e1 - results[(0, -1)].e2)
        R[1,0] = get_slope(2 * dg, results[(+1, 0)].e2 - results[(-1, 0)].e2)

    elif len(results) == 3:

        # TODO
        pass

    else:
        print('Length of results dictionary is {}, not possible to obtain response matrix'.format(len(results)))

    if output_dir:
        for i in range(2):
            for j in range(2):
                out_name = '{}/R_{}_{}'.format(output_dir, i, j)
                np.save(out_name, R[i][j])

    return R


def shear_bias_m(R, i):
    """Return multiplicative shear bias for component i given shear the response matrix R

    Parameters
    ----------
    R: matrix(2, 2) of double
        shear response matrix
    i: int
        component, 0 or 1

    Returns
    -------
    m: double
        multiplicative shear bias
    """

    assert(i==0 or i==1)

    return R[i][i] - 1.0

