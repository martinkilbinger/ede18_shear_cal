def download_HST_images(dest_dir='data/HST'):
    """Download HST images from galsim repository
    
    Parameters
    ----------
    dest_dir: string, optional, default='data/HST'
        destination directory
        
    Returns
    -------
    None
    """

    from urllib import urlretrieve
    from shutil import move
    
    url = 'https://github.com/GalSim-developers/GalSim/tree/releases/2.0/examples/data'
    data_files = ['real_galaxy_catalog_23.5_example.fits', \
                  'acs_I_unrot_sci_20_cf.fits', \
                  'real_galaxy_images.fits', \
                  'real_galaxy_PSF_images.fits']

    if not os.path.exists(dest_dir):
        # TODO: Catch exception OSError if file exists, but is not dir
        os.makedirs(dest_dir)
        
    for d in data_files:
        target = '{}/{}'.format(dest_dir, d)
        if os.path.isfile(target):
            print('Data file {} already exists, skipping...'.format(target))
        else:
            print('Downloading data file {}.'.format(target))
            urlretrieve(url, d)
            move(d, target)

