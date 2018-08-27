#Here I show an example of how I run KSB with shapelens. 

#Shear values
g1=0.0
g2=-0.02

#Input galaxy images path
gal_path='/dsm/cosmo02/sparseastro/apujol/galsim/multishear/g1_'$g1'_g2_'$g2'/'
#Input PSF images path
psf_path='/dsm/cosmo02/sparseastro2/apujol/galsim_runs/control/space/constant/'
#Output KSB path
out_path='/dsm/cosmo02/sparseastro2/apujol/shapelens/output/ksbtt/multishear/g1_'$g1'_g2_'$g2'/'

#I have 200 images (for both galaxies and PSFs), I run KSB in a loop over the images.
for i in {0..199}
do
	while [[ $(echo -n ${i} | wc -c) -lt 3 ]] ; 
	do
	    i="0${i}"
	done
    #PSF image file name
	psf_name=$psf_path'starfield_image-'$i'-0.fits'
    #galaxy image file name
	gal_name=$gal_path'image-'$i'-0.fits'
    #output KSB file name
	out_name=$out_path'result-'$i'.txt'

	echo running image $gal_name
    #run KSB
	get_shapes -T -p $psf_name $gal_name > $out_name 
done
