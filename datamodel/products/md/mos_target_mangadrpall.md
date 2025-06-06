# Data Model: mos_target_mangadrpall


MOS Target table: mos_target_mangadrpall


## Contents
- [Basic Information](#basic-information)
- [Changelog](#changelog)
- [Example HDUS List](#example-hdus-list)
- [Notes](#notes)
- [Regrets](#regrets)
---

## Basic Information
Final summary file of the MaNGA Data Reduction Pipeline (DRP).

### Naming Convention
$MOS_TARGET/[V_TARG]/mos_mangadrpall.fits, where V_TARG=1.0.2 for DR19

### Releases
DR19

### Enviroments
MOS_TARGET

### Approximate Size
8 MB

### File Type
FITS

### Generated by Product
sdss5db> targetdb, operations database server

### Is a VAC
False

### Data Level
2.3.3

### HDUS List for release DR19
  - [HDU0: PRIMARY](#hdu0-primary)
  - [HDU1](#hdu1)

---

## Changelog
Describes changes to the datamodel product and/or file structure from one release to another

---
## Example HDUS List

### HDU0: PRIMARY
Primary header

#### HDU Type: IMAGE
#### HDU Size:  0 bytes

##### Header Table Caption for HDU0
Key | Value | Comment | |
| --- | --- | --- | --- |
| SIMPLE | True | conforms to FITS standard |
| BITPIX | 8 | array data type |
| NAXIS | 0 | number of array dimensions |
| EXTEND | True |  |



### HDU1: 
MOS Target table: mos_target_mangadrpall

#### HDU Type: BINARY TABLE
#### HDU Size:  8 MB

##### Header Table Caption for HDU1
Key | Value | Comment | |
| --- | --- | --- | --- |
| XTENSION | BINTABLE | binary table extension |
| BITPIX | 8 | array data type |
| NAXIS | 2 | number of array dimensions |
| NAXIS1 | 780 | length of dimension 1 |
| NAXIS2 | 11273 | length of dimension 2 |
| PCOUNT | 0 | number of group parameters |
| GCOUNT | 1 | number of groups |
| TFIELDS | 160 | number of table fields |
| TNULL1 | -2147483648 |  |
| TNULL19 | -2147483648 |  |
| TNULL21 | -2147483648 |  |
| TNULL25 | -2147483648 |  |
| TNULL27 | -2147483648 |  |
| TNULL39 | -2147483648 |  |
| TNULL40 | -2147483648 |  |
| TNULL41 | -2147483648 |  |
| TNULL46 | -9223372036854775808 |  |
| TNULL47 | -9223372036854775808 |  |
| TNULL48 | -9223372036854775808 |  |
| TNULL49 | -9223372036854775808 |  |
| TNULL51 | -2147483648 |  |
| TNULL53 | -2147483648 |  |
| TNULL54 | -2147483648 |  |
| TNULL55 | -2147483648 |  |
| TNULL72 | -2147483648 |  |
| TNULL73 | -2147483648 |  |
| TNULL74 | -2147483648 |  |
| TNULL76 | -2147483648 |  |
| TNULL77 | -2147483648 |  |
| TNULL160 | -9223372036854775808 |  |

##### Binary Table Caption for HDU1
Name | Type | Unit | Description |
| --- | --- | --- | --- |
 | plate | int32 |  | Plate ID |
 | ifudsgn | char[5] |  | IFU design id (e.g. 12701) |
 | plateifu | char[11] |  | Plate+ifudesign name for this object (e.g. 7443-12701) |
 | mangaid | char[9] |  | MaNGA ID for this object (e.g. 1-114145) |
 | versdrp2 | char[6] |  | Version of DRP used for 2d reductions |
 | versdrp3 | char[6] |  | Version of DRP used for 3d reductions |
 | verscore | char[6] |  | Version of mangacore used for reductions |
 | versutil | char[7] |  | Version of idlutils used for reductions |
 | versprim | char[4] |  | Version of mangapreim used for reductions |
 | platetyp | char[14] |  | Plate type (e.g. MANGA, APOGEE-2&amp;MANGA) |
 | srvymode | char[14] |  | Survey mode (e.g. MANGA dither, MANGA stare, APOGEE lead) |
 | objra | float64 |  | Right ascension of the science object in J2000 |
 | objdec | float64 | degrees | Declination of the science object in J2000 |
 | ifuglon | float64 | degrees | Galactic longitude corresponding to IFURA/DEC |
 | ifuglat | float64 | degrees | Galactic latitude corresponding to IFURA/DEC |
 | ifura | float64 | degrees | Right ascension of this IFU in J2000 |
 | ifudec | float64 | degrees | Declination of this IFU in J2000 |
 | ebvgal | float32 | degrees | E(B-V) value from SDSS dust routine for this IFUGLON, IFUGLAT |
 | nexp | int32 |  | Number of science exposures combined |
 | exptime | float32 |  | Total exposure time |
 | drp3qual | int32 | seconds | Quality bitmask |
 | bluesn2 | float32 |  | Total blue SN2 across all nexp exposures |
 | redsn2 | float32 |  | Total red SN2 across all nexp exposures |
 | harname | char[17] |  | IFU harness name |
 | frlplug | int32 |  | Frplug hardware code |
 | cartid | char[5] |  | Cartridge ID number |
 | designid | int32 |  | Design ID number |
 | cenra | float64 |  | Plate center right ascension in J2000 |
 | cendec | float64 | degrees | Plate center declination in J2000 |
 | airmsmin | float32 | degrees | Minimum airmass across all exposures |
 | airmsmed | float32 |  | Median airmass across all exposures |
 | airmsmax | float32 |  | Maximum airmass across all exposures |
 | seemin | float32 |  | Best guider seeing |
 | seemed | float32 | arcsec | Median guider seeing |
 | seemax | float32 | arcsec | Worst guider seeing |
 | transmin | float32 | arcsec | Worst transparency |
 | transmed | float32 |  | Median transparency |
 | transmax | float32 |  | Best transparency |
 | mjdmin | int32 |  | Minimum MJD across all exposures |
 | mjdmed | int32 |  | Median MJD across all exposures |
 | mjdmax | int32 |  | Maximum MJD across all exposures |
 | gfwhm | float32 |  | Reconstructed FWHM in g-band |
 | rfwhm | float32 | arcsec | Reconstructed FWHM in r-band |
 | ifwhm | float32 | arcsec | Reconstructed FWHM in i-band |
 | zfwhm | float32 | arcsec | Reconstructed FWHM in z-band |
 | mngtarg1 | int64 | arcsec | Manga-target1 maskbit for galaxy target catalog |
 | mngtarg2 | int64 |  | Manga-target2 maskbit for galaxy target catalog |
 | mngtarg3 | int64 |  | Manga-target3 maskbit for galaxy target catalog |
 | catidnum | int64 |  | Primary target input catalog (leading digits of mangaid) |
 | plttarg | char[19] |  | plateTarget reference file appropriate for this target |
 | manga_tileid | int32 |  | The ID of the tile to which this object has been allocated |
 | nsa_iauname | char[19] |  | IAU-style designation based on RA/Dec (NSA) |
 | ifutargetsize | int32 |  | The ideal IFU size for this object. The intended IFU size is equal to IFUTargetSize except if IFUTargetSize &gt; 127 when it is 127, or &lt; 19 when it is 19 |
 | ifudesignsize | int32 | fibers | The allocated IFU size (0 = "unallocated") |
 | ifudesignwrongsize | int32 | fibers | The allocated IFU size if the intended IFU size was not available |
 | z | float32 | fibers | The targeting redshift (identical to nsa_z for those targets in the NSA Catalog. For others, it is the redshift provided by the Ancillary programs) |
 | zmin | float32 |  | The minimum redshift at which the galaxy could still have been included in the Primary sample |
 | zmax | float32 |  | The maximum redshift at which the galaxy could still have been included in the Primary sample |
 | szmin | float32 |  | The minimum redshift at which the galaxy could still have been included in the Secondary sample |
 | szmax | float32 |  | The maximum redshift at which the galaxy could still have been included in the Secondary sample |
 | ezmin | float32 |  | The minimum redshift at which the galaxy could still have been included in the Primary+ sample |
 | ezmax | float32 |  | The minimum redshift at which the galaxy could still have been included in the Primary+ sample |
 | probs | float32 |  | The probability that a Secondary sample galaxy is included after down-sampling. For galaxies not in the Secondary sample PROBS is set to the mean down-sampling probability |
 | pweight | float32 |  | The volume weight for the Primary sample. Corrects the MaNGA selection to a volume limited sample. |
 | psweight | float32 |  | The volume weight for the combined Primary and full Secondary samples. Corrects the MaNGA selection to a volume limited sample. |
 | psrweight | float32 |  | The volume weight for the combined Primary and down-sampled Secondary samples. Corrects the MaNGA selection to a volume limited sample. |
 | sweight | float32 |  | The volume weight for the full Secondary sample. Corrects the MaNGA selection to a volume limited sample. |
 | srweight | float32 |  | The volume weight for the down-sampled Secondary sample. Corrects the MaNGA selection to a volume limited sample. |
 | eweight | float32 |  | The volume weight for the Primary+ sample. Corrects the MaNGA selection to a volume limited sample. |
 | esweight | float32 |  | The volume weight for the combined Primary+ and full Secondary samples. Corrects the MaNGA selection to a volume limited sample. |
 | esrweight | float32 |  | The volume weight for the combined Primary+ and down-sampled Secondary samples. Corrects the MaNGA selection to a volume limited sample. |
 | nsa_field | int32 |  | SDSS field ID covering the target |
 | nsa_run | int32 |  | SDSS run ID covering the target |
 | nsa_camcol | int32 |  | SDSS camcol ID covering the catalog position. |
 | nsa_version | char[6] |  | Version of NSA catalogue used to select these targets |
 | nsa_nsaid | int32 |  | The NSAID field in the NSA catalogue referenced in nsa_version. |
 | nsa_nsaid_v1b | int32 |  | The NSAID of the target in the NSA_v1b_0_0_v2 catalogue (if applicable). |
 | nsa_z | float32 |  | Heliocentric redshift (NSA) |
 | nsa_zdist | float32 |  | Distance estimate using peculiar velocity model of Willick et al. (1997), expressed as a redshift equivalent; multiply by c/H0 for Mpc (NSA) |
 | nsa_elpetro_mass | float32 |  | Stellar mass from K-correction fit (use with caution) for elliptical Petrosian fluxes (NSA) |
 | nsa_elpetro_absmag_f | float32 | solar masses | Absolute magnitude in rest-frame GALEX far-UV, from elliptical Petrosian fluxes (NSA) |
 | nsa_elpetro_absmag_n | float32 | mag | Absolute magnitude in rest-frame GALEX near-UV, from elliptical Petrosian fluxes (NSA) |
 | nsa_elpetro_absmag_u | float32 | mag | Absolute magnitude in rest-frame SDSS u-band, from elliptical Petrosian fluxes (NSA) |
 | nsa_elpetro_absmag_g | float32 | mag | Absolute magnitude in rest-frame SDSS g-band, from elliptical Petrosian fluxes (NSA) |
 | nsa_elpetro_absmag_r | float32 | mag | Absolute magnitude in rest-frame SDSS r-band, from elliptical Petrosian fluxes (NSA) |
 | nsa_elpetro_absmag_i | float32 | mag | Absolute magnitude in rest-frame SDSS i-band, from elliptical Petrosian fluxes (NSA) |
 | nsa_elpetro_absmag_z | float32 | mag | Absolute magnitude in rest-frame SDSS z-band, from elliptical Petrosian fluxes (NSA) |
 | nsa_elpetro_amivar_f | float32 | mag | Inverse variance of elpetro_absmag_f (NSA) |
 | nsa_elpetro_amivar_n | float32 | mag^{-2} | Inverse variance of elpetro_absmag_n (NSA) |
 | nsa_elpetro_amivar_u | float32 | mag^{-2} | Inverse variance of elpetro_absmag_u (NSA) |
 | nsa_elpetro_amivar_g | float32 | mag^{-2} | Inverse variance of elpetro_absmag_g (NSA) |
 | nsa_elpetro_amivar_r | float32 | mag^{-2} | Inverse variance of elpetro_absmag_r (NSA) |
 | nsa_elpetro_amivar_i | float32 | mag^{-2} | Inverse variance of elpetro_absmag_i (NSA) |
 | nsa_elpetro_amivar_z | float32 | mag^{-2} | Inverse variance of elpetro_absmag_z (NSA) |
 | nsa_elpetro_flux_f | float32 | mag^{-2} | Elliptical SDSS-style Petrosian flux in GALEX far-UV (using r-band aperture) (NSA) |
 | nsa_elpetro_flux_n | float32 | nanomaggies | Elliptical SDSS-style Petrosian flux in GALEX near-UV (using r-band aperture) (NSA) |
 | nsa_elpetro_flux_u | float32 | nanomaggies | Elliptical SDSS-style Petrosian flux in SDSS u-band (using r-band aperture) (NSA) |
 | nsa_elpetro_flux_g | float32 | nanomaggies | Elliptical SDSS-style Petrosian flux in SDSS g-band (using r-band aperture) (NSA) |
 | nsa_elpetro_flux_r | float32 | nanomaggies | Elliptical SDSS-style Petrosian flux in SDSS r-band (using r-band aperture) (NSA) |
 | nsa_elpetro_flux_i | float32 | nanomaggies | Elliptical SDSS-style Petrosian flux in SDSS i-band (using r-band aperture) (NSA) |
 | nsa_elpetro_flux_z | float32 | nanomaggies | Elliptical SDSS-style Petrosian flux in SDSS z-band (using r-band aperture) (NSA) |
 | nsa_elpetro_flux_ivar_f | float32 | nanomaggies | Inverse variance of elpetroflux_f (NSA) |
 | nsa_elpetro_flux_ivar_n | float32 | nanomaggies^{-2} | Inverse variance of elpetroflux_n (NSA) |
 | nsa_elpetro_flux_ivar_u | float32 | nanomaggies^{-2} | Inverse variance of elpetroflux_u (NSA) |
 | nsa_elpetro_flux_ivar_g | float32 | nanomaggies^{-2} | Inverse variance of elpetroflux_g (NSA) |
 | nsa_elpetro_flux_ivar_r | float32 | nanomaggies^{-2} | Inverse variance of elpetroflux_r (NSA) |
 | nsa_elpetro_flux_ivar_i | float32 | nanomaggies^{-2} | Inverse variance of elpetroflux_i (NSA) |
 | nsa_elpetro_flux_ivar_z | float32 | nanomaggies^{-2} | Inverse variance of elpetroflux_z (NSA) |
 | nsa_elpetro_th50_r | float32 | nanomaggies^{-2} | Elliptical Petrosian 50% light radius in SDSS r-band (NSA) |
 | nsa_elpetro_phi | float32 | arcsec | Position angle (east of north) used for elliptical apertures (for this version, same as ba90) (NSA) |
 | nsa_elpetro_ba | float32 | deg | Axis ratio used for elliptical apertures (for this version, same as ba90) (NSA) |
 | nsa_sersic_mass | float32 |  | Stellar mass from K-correction fit (use with caution) for Sersic fluxes (NSA) |
 | nsa_sersic_absmag_f | float32 | solar mass | Absolute magnitude in rest-frame GALEX near-UV, from Sersic fluxes (NSA) |
 | nsa_sersic_absmag_n | float32 | mag | Absolute magnitude in rest-frame GALEX far-UV, from Sersic fluxes (NSA) |
 | nsa_sersic_absmag_u | float32 | mag | Absolute magnitude in rest-frame SDSS u-band, from Sersic fluxes (NSA) |
 | nsa_sersic_absmag_g | float32 | mag | Absolute magnitude in rest-frame SDSS g-band, from Sersic fluxes (NSA) |
 | nsa_sersic_absmag_r | float32 | mag | Absolute magnitude in rest-frame SDSS r-band, from Sersic fluxes (NSA) |
 | nsa_sersic_absmag_i | float32 | mag | Absolute magnitude in rest-frame SDSS i-band, from Sersic fluxes (NSA) |
 | nsa_sersic_absmag_z | float32 | mag | Absolute magnitude in rest-frame SDSS z-band, from Sersic fluxes (NSA) |
 | nsa_sersic_flux_f | float32 | mag | Two-dimensional, single-component Sersic fit flux in GALEX far-UV (fit using r-band structural parameters) (NSA) |
 | nsa_sersic_flux_n | float32 | nanomaggies | Two-dimensional, single-component Sersic fit flux in GALEX near-UV (fit using r-band structural parameters) (NSA) |
 | nsa_sersic_flux_u | float32 | nanomaggies | Two-dimensional, single-component Sersic fit flux in SDSS u-band (fit using r-band structural parameters) (NSA) |
 | nsa_sersic_flux_g | float32 | nanomaggies | Two-dimensional, single-component Sersic fit flux in SDSS g-band (fit using r-band structural parameters) (NSA) |
 | nsa_sersic_flux_r | float32 | nanomaggies | Two-dimensional, single-component Sersic fit flux in SDSS r-band (fit using r-band structural parameters) (NSA) |
 | nsa_sersic_flux_i | float32 | nanomaggies | Two-dimensional, single-component Sersic fit flux in SDSS i-band (fit using r-band structural parameters) (NSA) |
 | nsa_sersic_flux_z | float32 | nanomaggies | Two-dimensional, single-component Sersic fit flux in SDSS z-band (fit using r-band structural parameters) (NSA) |
 | nsa_sersic_flux_ivar_f | float32 | nanomaggies | Inverse variance of sersic_flux_f (NSA) |
 | nsa_sersic_flux_ivar_n | float32 | nanomaggies^{-2} | Inverse variance of sersic_flux_n (NSA) |
 | nsa_sersic_flux_ivar_u | float32 | nanomaggies^{-2} | Inverse variance of sersic_flux_u (NSA) |
 | nsa_sersic_flux_ivar_g | float32 | nanomaggies^{-2} | Inverse variance of sersic_flux_g (NSA) |
 | nsa_sersic_flux_ivar_r | float32 | nanomaggies^{-2} | Inverse variance of sersic_flux_r (NSA) |
 | nsa_sersic_flux_ivar_i | float32 | nanomaggies^{-2} | Inverse variance of sersic_flux_i (NSA) |
 | nsa_sersic_flux_ivar_z | float32 | nanomaggies^{-2} | Inverse variance of sersic_flux_z (NSA) |
 | nsa_sersic_th50 | float32 | nanomaggies^{-2} | 50% light radius of two-dimensional, single-component Sersic fit to r-band (NSA) |
 | nsa_sersic_phi | float32 | arcsec | Angle (E of N) of major axis in two-dimensional, single-component Sersic fit in r-band (NSA) |
 | nsa_sersic_ba | float32 | deg | Axis ratio b/a from two-dimensional, single-component Sersic fit in r-band (NSA) |
 | nsa_sersic_n | float32 |  | Sersic index from two-dimensional, single-component Sersic fit in r-band (NSA) |
 | nsa_petro_flux_f | float32 |  | Azimuthally-averaged SDSS-style Petrosian flux in GALEX far-UV (using r-band aperture) (NSA) |
 | nsa_petro_flux_n | float32 | nanomaggies | Azimuthally-averaged SDSS-style Petrosian flux in GALEX far-UV (using r-band aperture) (NSA) |
 | nsa_petro_flux_u | float32 | nanomaggies | Azimuthally-averaged SDSS-style Petrosian flux in SDSS u-band (using r-band aperture) (NSA) |
 | nsa_petro_flux_g | float32 | nanomaggies | Azimuthally-averaged SDSS-style Petrosian flux in SDSS g-band (using r-band aperture) (NSA) |
 | nsa_petro_flux_r | float32 | nanomaggies | Azimuthally-averaged SDSS-style Petrosian flux in SDSS r-band (using r-band aperture) (NSA) |
 | nsa_petro_flux_i | float32 | nanomaggies | Azimuthally-averaged SDSS-style Petrosian flux in SDSS i-band (using r-band aperture) (NSA) |
 | nsa_petro_flux_z | float32 | nanomaggies | Azimuthally-averaged SDSS-style Petrosian flux in SDSS z-band (using r-band aperture) (NSA) |
 | nsa_petro_flux_ivar_f | float32 | nanomaggies | Inverse variance of petro_flux_f (NSA) |
 | nsa_petro_flux_ivar_n | float32 | nanomaggies^{-2} | Inverse variance of petro_flux_n (NSA) |
 | nsa_petro_flux_ivar_u | float32 | nanomaggies^{-2} | Inverse variance of petro_flux_u (NSA) |
 | nsa_petro_flux_ivar_g | float32 | nanomaggies^{-2} | Inverse variance of petro_flux_g (NSA) |
 | nsa_petro_flux_ivar_r | float32 | nanomaggies^{-2} | Inverse variance of petro_flux_r (NSA) |
 | nsa_petro_flux_ivar_i | float32 | nanomaggies^{-2} | Inverse variance of petro_flux_i (NSA) |
 | nsa_petro_flux_ivar_z | float32 | nanomaggies^{-2} | Inverse variance of petro_flux_z (NSA) |
 | nsa_petro_th50 | float32 | nanomaggies^{-2} | Azimuthally averaged SDSS-style Petrosian 50% light radius (derived from r band) (NSA) |
 | nsa_extinction_f | float32 | arcsec | Galactic extinction from Schlegel, Finkbeiner, and Davis (1997), in GALEX far-UV (NSA) |
 | nsa_extinction_n | float32 | mag | Galactic extinction from Schlegel, Finkbeiner, and Davis (1997), in GALEX near-UV (NSA) |
 | nsa_extinction_u | float32 | mag | Galactic extinction from Schlegel, Finkbeiner, and Davis (1997), in SDSS u-band (NSA) |
 | nsa_extinction_g | float32 | mag | Galactic extinction from Schlegel, Finkbeiner, and Davis (1997), in SDSS g-band (NSA) |
 | nsa_extinction_r | float32 | mag | Galactic extinction from Schlegel, Finkbeiner, and Davis (1997), in SDSS r-band (NSA) |
 | nsa_extinction_i | float32 | mag | Galactic extinction from Schlegel, Finkbeiner, and Davis (1997), in SDSS i-band (NSA) |
 | nsa_extinction_z | float32 | mag | Galactic extinction from Schlegel, Finkbeiner, and Davis (1997), in SDSS z-band (NSA) |
 | htmid | int64 | mag | 20-level deep Hierarchical Triangular Mesh ID |



---
## Notes
None

---
## Regrets
I  have no regrets!