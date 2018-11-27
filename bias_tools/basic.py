
# coding: utf-8

# # Basic jupyter notebook for shear bias computations

# In[19]:


#get_ipython().magic(u'run python/misc.py')
#get_ipython().magic(u'run python/simulations.py')
#get_ipython().magic(u'run python/shapes.py')

from misc import *
from simulations import *
from shapes import *
from errors import *
from plot import *


# In[2]:


#% run python/data.py
#download_HST_images()


# In[3]:


# Job control:
job = param()

# Re-run job if output file already exists?
job.re_run = False

# Set dry_run to True for test run
job.dry_run = False


# In[4]:


# Small shear change for numerical derivative
dg = 0.02


# In[5]:


# List of signs for shear change
# Five steps (one in each direction + (0, 0)
g_steps = [(-1, 0), (0, -1), (1, 0), (0, 1), (0, 0)]

# Three steps, requires randomly changing signs
#g_step_list = [(-1, 0), (0, -1), (1, 1)]


# In[6]:


# Dictionary and list of shears
g_dict = {}
for step in g_steps:
    g_dict[step] = (step[0] * dg, step[1] * dg)
g_values = g_dict.values()


# ### Setup

# #### Image sizes and numbers

# In[7]:


# Number of postage stamps is nxy_tiles^2
nxy_tiles = 4
#nxy_tiles = 100

# Number of files with different constant shear and PSF
nfiles    =  10
#nfiles   = 200


# #### Galsim

# In[8]:


# Files and directories
galsim_config_fname        = 'csc_multishear.yaml'
galsim_config_psf_fname    = 'csc_psf.yaml'
galsim_config_dir          = 'config/galsim'
galsim_input_dir           = 'data/galsim/great3/control/space/constant'
galsim_output_base_dir     = 'output/galsim'
galsim_output_gal_fname_format = 'image-%03d-%1d.fits'
galsim_output_psf_fname_format = 'starfield_image-%03d-%1d.fits'


# In[9]:


# Set paths
galsim_config_path     = '{}/{}'.format(galsim_config_dir, galsim_config_fname)
galsim_config_psf_path = '{}/{}'.format(galsim_config_dir, galsim_config_psf_fname)


# ### Create image simulations by calling galsim

# In[ ]:


# TODO: Only run if output file does not exist
create_all_sims_great3(g_values, galsim_config_path, galsim_config_psf_path, galsim_input_dir, galsim_output_base_dir, \
        galsim_output_gal_fname_format, galsim_output_psf_fname_format, nxy_tiles=nxy_tiles, nfiles=nfiles, job=job)


# ### Measure shapes

# In[10]:


ksb_input_base_dir  = galsim_output_base_dir
ksb_output_base_dir = 'output/shapelens'
all_shapes_shapelens(g_values, ksb_input_base_dir, ksb_output_base_dir, nfiles, nxy_tiles, job=job)


# ### Get shear estimate results

# In[20]:


results_input_base_dir  = ksb_output_base_dir
psf_input_dir           = '{}/psf/'.format(galsim_output_base_dir)
results = all_read_shapelens(g_dict, results_input_base_dir, psf_input_dir, nfiles)


# In[ ]:


R_output_dir = 'output/R'
R = shear_response(results, dg, output_dir=R_output_dir)


###

R = read_R(R_output_dir)
print('mean(R)')
print(R.mean(axis=2))

print('std(R)')
print(R.std(axis=2))

mean_over_shear(results)


# ### Plot shear response

nbins = 3
xvar  = results[(0, 0)].sn
xname = 'SNR'

yvar   = [shear_bias_m(R, i) for i in [0, 1]]
yvar.append(R[0,1])
yname  = ['$m_1$', '$m_2$', '$R_{12}$']
color  = ['g', 'r', 'b']
marker = ['o', 's', 'd']
x_mean, y_mean, y_std = plot_mean_per_bin_several(xvar, xname, yvar, yname, nbins, error_mode='std', \
        color=color, lw=2, marker=marker, out_name='snr_m1.pdf')


