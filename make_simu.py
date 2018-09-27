# -*- coding: utf-8 -*-

"""
From GalSim demo6.py
Create simulated images to measure the bias using A. Pujol technics.
Make a simple verification on the shear apllied using KSB from galsim.hsm.

Warning :
It's not an usual executable script
Best way is to run it through a Python environment (like IPython)

Note :
Can be run from GalSim "example/" directory
Otherwise one will need to copy the "example/data" directory at this file location or change "dir" variable.
"""


import galsim
import numpy as np


#############
# Make simu #
#############

print "Make simulation.."

cat_file_name = 'real_galaxy_catalog_23.5_example.fits'
dir = 'data'

random_seed = 1512413
sky_level = 1.e6        # ADU / arcsec^2
pixel_scale = 0.16      # arcsec
gal_flux = 1.e5         # arbitrary choice, makes nice (not too) noisy images
gal_g1 = [0.02, 0., -0.02]         #
gal_g2 = [0., 0.02, -0.02]         #
gal_mu = 1.082          # mu = ( (1-kappa)^2 - g1^2 - g2^2 )^-1
psf_inner_fwhm = 0.6    # arcsec
psf_outer_fwhm = 2.3    # arcsec
psf_inner_fraction = 0.8  # fraction of total PSF flux in the inner Gaussian
psf_outer_fraction = 0.2  # fraction of total PSF flux in the inner Gaussian
ngal = 100

if len(gal_g1) != len(gal_g2):
    raise Exception("gal_g1 and gal_g2 must have the same size")

# Read in galaxy catalog
# Note: dir is the directory both for the catalog itself and also the directory prefix
# for the image files listed in the catalog.
# If the images are in a different directory, you may also specify image_dir, which gives
# the relative path from dir to wherever the images are located.
real_galaxy_catalog = galsim.RealGalaxyCatalog(cat_file_name, dir=dir)

# Make the double Gaussian PSF
psf1 = galsim.Gaussian(fwhm = psf_inner_fwhm, flux = psf_inner_fraction)
psf2 = galsim.Gaussian(fwhm = psf_outer_fwhm, flux = psf_outer_fraction)
psf = psf1+psf2

# Draw the PSF with no noise.
psf_image = psf.drawImage(scale = pixel_scale)
# write to file
# psf_image.write(psf_file_name)


# Build the images
all_images = []
for k in range(ngal):

    #print k
    gal_shear_tmp = []
    for g1_tmp, g2_tmp in zip(gal_g1, gal_g2):

        #print g1_tmp, g2_tmp

        # Initialize the random number generator we will be using.
        rng = galsim.UniformDeviate(random_seed+k+1)

        gal_1 = galsim.RealGalaxy(real_galaxy_catalog, index = k, flux=gal_flux)
        gal_2 = galsim.RealGalaxy(real_galaxy_catalog, index = k, flux=gal_flux)

        # Rotate by an angle of 90° to get <e_int> = 0
        theta = np.pi/2. * galsim.radians
        gal_2 = gal_2.rotate(theta)

        # Apply the desired shear
        gal_1 = gal_1.shear(g1=g1_tmp, g2=g2_tmp)
        gal_2 = gal_2.shear(g1=g1_tmp, g2=g2_tmp)

        # Also apply a magnification mu = ( (1-kappa)^2 - |gamma|^2 )^-1
        # This conserves surface brightness, so it scales both the area and flux.
        gal_1 = gal_1.magnify(gal_mu)
        gal_2 = gal_2.magnify(gal_mu)

        # Make the combined profile
        final_1 = galsim.Convolve([psf, gal_1])
        final_2 = galsim.Convolve([psf, gal_2])

        # Offset by up to 1/2 pixel in each direction
        # We had previously (in demo4 and demo5) used shift(dx,dy) as a way to shift the center of
        # the image.  Since that is applied to the galaxy, the units are arcsec (since the galaxy
        # profile itself doesn't know about the pixel scale).  Here, the offset applies to the
        # drawn image, which does know about the pixel scale, so the units of offset are pixels,
        # not arcsec.  Here, we apply an offset of up to half a pixel in each direction.
        dx = rng() - 0.5
        dy = rng() - 0.5

        # Draw the profile
        if k == 0:
            # Note that the offset argument may be a galsim.PositionD object or a tuple (dx,dy).
            im_1 = final_1.drawImage(scale=pixel_scale, offset=(dx,dy))
            im_2 = final_2.drawImage(scale=pixel_scale, offset=(dx,dy))
            xsize, ysize = im_1.array.shape
        else:
            im_1 = galsim.ImageF(xsize,ysize)
            im_2 = galsim.ImageF(xsize,ysize)
            final_1.drawImage(im_1, scale=pixel_scale, offset=(dx,dy))
            final_2.drawImage(im_2, scale=pixel_scale, offset=(dx,dy))

        # Add a constant background level
        # Note :
        # The background make the shear measurement impossible
        background = sky_level * pixel_scale**2
        #im_1 += background
        #im_2 += background

        # Add Poisson noise.  This time, we don't give a sky_level, since we have already
        # added it to the image, so we don't want any more added.  The sky_level parameter
        # really defines how much _extra_ sky should be added above what is already in the image.
        im_1.addNoise(galsim.PoissonNoise(rng))
        im_2.addNoise(galsim.PoissonNoise(rng))

        # Store that into the list of all images
        gal_shear_tmp.append(np.array([im_1, im_2]))
    all_images += [gal_shear_tmp]

# Format :
# all_images = [gal_index(100), shear_apply(3), rotation(2)]
all_images = np.array(all_images)


###############
# Verif shear #
###############

print "Compute shear for verification.."

all_shear_1 = []
all_shear_2 = []
for i in range(ngal):
    diff_shear_1 = []
    diff_shear_2 = []
    for j in range(len(gal_g1)):

        # Estimate the shear using KSB
        ss_1 = galsim.hsm.EstimateShear(all_images[i,j,0], psf_image, shear_est="KSB", strict=False)
        ss_2 = galsim.hsm.EstimateShear(all_images[i,j,1], psf_image, shear_est="KSB", strict=False)

        diff_shear_1.append(np.array([ss_1.corrected_g1, ss_2.corrected_g1]))
        diff_shear_2.append(np.array([ss_1.corrected_g2, ss_2.corrected_g2]))
    all_shear_1 += [diff_shear_1]
    all_shear_2 += [diff_shear_2]

all_shear_1 = np.array(all_shear_1)
all_shear_2 = np.array(all_shear_2)

mean_g = []
for i in range(len(gal_g2)):

    # Mean shear on gal and gal_90 to get <e_int> = 0
    g1_tmp = np.mean(np.concatenate((all_shear_1[:,i,0], all_shear_1[:,i,1])))
    g2_tmp = np.mean(np.concatenate((all_shear_2[:,i,0], all_shear_2[:,i,1])))
    mean_g.append(np.array([g1_tmp, g2_tmp]))

mean_g = np.array(mean_g)
# absolute error from input
g_err = np.abs(mean_g - np.array([gal_g1,gal_g2]).T)

print
print "Shear measured"
print mean_g
print "Error from expected"
print g_err
