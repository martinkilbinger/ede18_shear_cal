In this directory you can find 2 files:

csc_multishear.yaml
———————————————————
This is a config file to simulate the GREAT3-CSC images from parameter files. The parameter files specify all the parameters from the file. I used to run this code in the cluster, at: /dsm/cosmo02/sparseastro2/apujol/galsim_runs
The code inputs the parameter files from the directory control/space/constant from where the script was. The output goes to the directory multishear from where the script is. Everything is specified in the yams file. 


run_multishear.sh
————————————————— 

In this script I show an example of how to run galsim specifying some parameters on the command. Here I show how to force g1 and g2 to some values. No matter what the parameter files specify, here I’m overwriting the shear values. I’m also defining the output directory. This is what I did to ru the sheared versions of the images, basically changing the shear values in the script and running again (in bash). 