# ede18_shear_cal
École d'été Euclid 2018: Projet "table ronde": shear calibration

## Files

* `make_simu.py`
  Crée des galaxies simulées (basée sur HST), applique shear, mesure biais.
* `data`
  Répertoire avec des données.
  * `constant/space/control`
    branche great3, information (.fits, .yaml) des shears appliqués aux galaxies
 * `scripts_for_shear_bias`
    Scripts d'Arnau pour son papier Pujol et al. (2018)
    * `galsim`
      Pour tourner galsim
    * `notebook`
      Mesure de biais, erreurs de jackknife
    * `shapelens`
      Pour tourner shapelens (mesure de forme KSB)
* `bias_tools`
  Scriptes et notebooks de Martin

