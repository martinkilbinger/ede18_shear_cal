g1=-0.02
g2=0.0

#dirname='/home/apujol/galsim/multishear/g1_'$g1'_g2_'$g2
#dirname='/dsm/cosmo02/sparseastro/apujol/galsim/multishear/g1_'$g1'_g2_'$g2
dirname='output/g1_'$g1'_g2_'$g2
galsim csc_multishear.yaml gal.shear.g1=$g1 gal.shear.g2=$g2 output.dir=$dirname


