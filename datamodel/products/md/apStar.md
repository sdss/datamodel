# Data Model: apStar


APOGEE Redux combined spectrum file


## Contents
- [Basic Information](#basic-information)
- [Changelog](#changelog)
- [Example HDUS List](#example-hdus-list)
- [Notes](#notes)
- [Regrets](#regrets)
---

## Basic Information
apStar files contain the spectral data for a given star.  apStar files combine data from multiple visits, and combine the data from the three chips. Spectra are resampled onto a simple logarithmic wavelength scale. Both combined spectra as well as the resampled individual visit spectra are output.

### Naming Convention
<code>apStar-.+-[0-9]{5}\.fits</code>, where .+ (a.k.a. STARNAME) uniquely identifies each star and [0-9]{5} is the 5-digit MJD number of the last data included in the combined frames. There will also be a link, apStar-STARNAME.fits to the latest combined frame. apStar-STARNAME\.html

### Releases
DR12, DR13, DR14, DR15, DR16, DR17, DR19, WORK

### Enviroments
APOGEE_REDUX

### Approximate Size
1 MB

### File Type
FITS

### Generated by Product
apogeereduce (apstar_output)

### Is a VAC
False

### HDUS List for release WORK
  - [HDU0: PRIMARY](#hdu0-primary)
  - [HDU1](#hdu1)
  - [HDU2](#hdu2)
  - [HDU3](#hdu3)
  - [HDU4](#hdu4)
  - [HDU5](#hdu5)
  - [HDU6](#hdu6)
  - [HDU7](#hdu7)
  - [HDU8](#hdu8)
  - [HDU9](#hdu9)

---

## Changelog
Describes changes to the datamodel product and/or file structure from one release to another
 - WORK
   - from: DR19
   - note: No changes
 - DR19
   - from: DR17
   - primary_delta_nkeys: 13
   - added_primary_header_kwargs: ['PMRA', 'SVTARG0', 'SVAPTRG0', 'GMAG', 'BPMAG', 'JMAG', 'HEALPIX', 'CATEGORY', 'HMAG', 'EPMDEC', 'V_APRED', 'BPERR', 'KMAG', 'APTARG3', 'CADENCE', 'VRAD', 'APRED', 'CHISQ1', 'CHISQ2', 'PMDEC', 'CATID', 'KERR', 'CARTON1', 'HERR', 'JERR', 'GERR', 'FRSTCRTN', 'EPLX', 'PLX', 'EPMRA', 'PROGRAM', 'RPMAG', 'STARVER', 'RPERR']
   - removed_primary_header_kwargs: ['VERR1', 'AKTARG', 'H', 'FIELD', 'RMAX', 'ROVERMIN', 'VHELIO1', 'VERR_MED', 'K', 'K_ERR', 'BMAX', 'GOVERMIN', 'AKWISE', 'AUTOFWHM', 'BMIN', 'SFD_EBV', 'ROVERMAX', 'GMIN', 'AKMETHOD', 'WASH_M', 'VERR2', 'MAX_H', 'CCFWHM', 'WISE_4_5', 'IRAC_3_6', 'MIN_JK', 'IRAC_4_5', 'GMAX', 'WASH_T2', 'GOVERMAX', 'J', 'TARG_4_5', 'DDO51', 'NWAVE', 'H_ERR', 'BOVERMAX', 'VHELIO2', 'IRAC_5_8', 'J_ERR', 'BOVERMIN', 'SNREV', 'RV_CHI2', 'MAX_JK', 'MIN_H', 'RMIN', 'VHELIO']
 - DR17
   - from: DR16
   - primary_delta_nkeys: 48
   - added_primary_header_kwargs: ['K_ERR', 'RV_FEH', 'AP2TARG2', 'RV_TEFF', 'APTARG2', 'WASH_M', 'MAX_H', 'CCFWHM', 'MIN_JK', 'IRAC_3_6', 'AP2TARG4', 'WISE_4_5', 'IRAC_4_5', 'SRC_H', 'WASH_T2', 'TARG_4_5', 'APTARG1', 'NRES', 'DDO51', 'RV_LOGG', 'H_ERR', 'AP2TARG3', 'IRAC_5_8', 'N_COMP', 'J_ERR', 'AP2TARG1', 'RV_CHI2', 'MAX_JK', 'MIN_H', 'SNREV']
   - removed_primary_header_kwargs: ['RVTEFF3', 'RVCARB2', 'RVALPH1', 'RVTEFF1', 'RVTEFF2', 'RVLOGG2', 'FLAG3', 'SVERR', 'RVCARB1', 'SYNTHSCA', 'RVLOGG3', 'RVCARB3', 'CHISQ', 'VGSR', 'OVHELIO', 'TARG2', 'CHISQ3', 'RVFEH1', 'VERR3', 'TARG3', 'OVERR_ME', 'HJD3', 'SNRVIS3', 'LOCID', 'VLSR', 'HJD1', 'RVTEFF', 'SVHELIO', 'SVSCAT', 'VRAD', 'FIBER3', 'DATE', 'SVERR_ME', 'CHISQ1', 'CHISQ2', 'RVCARB', 'RVALPH2', 'COMBTYPE', 'VTYPE1', 'TARG1', 'RVFEH', 'BC3', 'RVALPH3', 'RVLOGG1', 'RVFEH2', 'VTYPE3', 'OVERR', 'DATE3', 'HJD2', 'OVSCAT', 'RVLOGG', 'SURVEY', 'CCPFWHM', 'TELESCOP', 'RVALPH', 'RVFEH3', 'VRAD3', 'SFILE3', 'VTYPE2', 'VHELIO3', 'JD3']
 - DR16
   - from: DR15
   - primary_delta_nkeys: 38
   - removed_primary_header_kwargs: ['FLAG5', 'JD4', 'BC4', 'SFILE4', 'SFILE5', 'FIBER5', 'FLAG4', 'DATE5', 'VERR5', 'HJD5', 'VHELIO5', 'RVTEFF5', 'JD5', 'RVTEFF4', 'VTYPE5', 'RVLOGG5', 'RVCARB5', 'VERR4', 'FIBER4', 'HJD4', 'RVCARB4', 'VHELIO4', 'SNRVIS5', 'RVALPH5', 'RVFEH5', 'SNRVIS4', 'DATE4', 'BC5', 'VRAD4', 'CHISQ4', 'RVALPH4', 'VTYPE4', 'CHISQ5', 'RVLOGG4', 'VRAD5', 'RVFEH4']
 - DR15
   - from: DR14
   - note: No changes
 - DR14
   - from: DR13
   - primary_delta_nkeys: 17
   - added_primary_header_kwargs: ['OVSCAT', 'AKTARG', 'CHISQ5', 'CHISQ1', 'CHISQ2', 'SFD_EBV', 'OVERR_ME', 'COMBTYPE', 'CHISQ', 'CHISQ4', 'VGSR', 'VLSR', 'AKMETHOD', 'OVHELIO', 'AKWISE', 'CHISQ3', 'OVERR']
 - DR13
   - from: DR12
   - primary_delta_nkeys: 2
   - added_primary_header_kwargs: ['SURVEY', 'TARG3']

---
## Example HDUS List

### HDU0: PRIMARY


#### HDU Type: IMAGE
#### HDU Size:  0 bytes

##### Header Table Caption for HDU0
Key | Value | Comment | |
| --- | --- | --- | --- |
| SIMPLE | True |  |
| BITPIX | 8 |  |
| NAXIS | 0 |  |
| EXTEND | True |  |
| CRVAL1 | 4.179 | Start log10(wavelength) |
| CDELT1 | 6e-06 | Dispersion in log10(wavelength) |
| CRPIX1 | 1 | Pixel of starting wavelength |
| CTYPE1 | LOG-LINEAR |  |
| DC-FLAG | 1 |  |
| OBJID | 2M13593121+6335074 | Object ID |
| V_APRED | e3d3e47d8cc59a8c6fe843286012406797e4265d |  |
| APRED | 1.0 |  |
| STARVER | 59380 |  |
| HEALPIX | 10105 |  |
| SNR | 55.79573596219787 | final median signal-to-noise ratio |
| RA | 209.88019 | right ascension, deg, J2000 |
| DEC | 63.585385 | declination, deg, J2000 |
| GLON | 110.7479855645902 | galactic longitude, deg, J2000 |
| GLAT | 51.90245725450458 | galactic latitude, deg, J2000 |
| JMAG | 99.98999786376953 | 2MASS J magnitude |
| JERR | -9999.990234375 | 2MASS J magnitude uncertainty |
| HMAG | 12.41699981689453 | 2MASS H magnitude |
| HERR | -9999.990234375 | 2MASS H magnitude uncertainty |
| KMAG | 99.98999786376953 | 2MASS K magnitude |
| KERR | -9999.990234375 | 2MASS K magnitude uncertainty |
| SRC_H |  |  |
| CATID | 4349650353 | Catalog ID |
| SVTARG0 | 0 |  |
| CARTON1 | ops_std_boss |  |
| CADENCE |  |  |
| PROGRAM |  |  |
| CATEGORY |  |  |
| PLX | -9999.990234375 |  |
| EPLX | -9999.990234375 |  |
| PMRA | -9999.990234375 |  |
| EPMRA | -9999.990234375 |  |
| PMDEC | -9999.990234375 |  |
| EPMDEC | -9999.990234375 |  |
| GMAG | -9999.990234375 | Gaia G-band magnitude |
| GERR | -9999.990234375 | Gaia G-band magnitude uncertainty |
| BPMAG | -9999.990234375 | Gaia BP-band magnitude |
| BPERR | -9999.990234375 | Gaia BP-band magnitude uncertainty |
| RPMAG | -9999.990234375 | Gaia RP-band magnitude |
| RPERR | -9999.990234375 | Gaia RP-band magnitude uncertainty |
| SVAPTRG0 | 0 |  |
| FRSTCRTN | 0 |  |
| APTARG1 | 0 |  |
| APTARG2 | 0 |  |
| APTARG3 | 0 |  |
| AP2TARG1 | 0 |  |
| AP2TARG2 | 0 |  |
| AP2TARG3 | 0 |  |
| AP2TARG4 | 0 |  |
| NVISITS | 2 |  |
| STARFLAG | 4 |  |
| ANDFLAG | 0 |  |
| N_COMP | 1 |  |
| VRAD | 15.53428683921353 |  |
| VSCATTER | 0.05736543274360906 |  |
| VERR | 0.0 |  |
| RV_TEFF | 6192.648320659712 |  |
| RV_LOGG | 4.764470879595443 |  |
| RV_FEH | -0.8657725795265059 |  |
| MEANFIB | 278.3546740070248 |  |
| SIGFIB | 7.778174593052023 |  |
| NRES |  5.00 4.25 3.50 |  |
| COMMENT | VISIT 1 INFORMATION |  |
| SFILE1 | apVisit-1.0-apo25m-15303-59280-271.fits |  |
| DATE1 | 2021-03-07T09:31:18.160 |  |
| JD1 | 2459280.91942 |  |
| FIBER1 | 271 |  |
| BC1 | -1.620521068572998 |  |
| CHISQ1 | 1.779343951621781 |  |
| VRAD1 | 15.48004525881579 |  |
| SNRVIS1 | 18.54220008850098 |  |
| FLAG1 | 4 |  |
| COMMENT | VISIT 2 INFORMATION |  |
| SFILE2 | apVisit-1.0-apo25m-15303-59380-282.fits |  |
| DATE2 | 2021-06-15T04:31:21.759 |  |
| JD2 | 2459380.71116 |  |
| FIBER2 | 282 |  |
| BC2 | -11.79683303833008 |  |
| CHISQ2 | 1.225171249772008 |  |
| VRAD2 | 15.5611722318132 |  |
| SNRVIS2 | 37.41019821166992 |  |
| FLAG2 | 4 |  |
| HISTORY | APOGEE Reduction Pipeline Version: 1.0 |  |
| HISTORY | HDU0 : header |  |
| HISTORY | HDU1 : flux |  |
| HISTORY | HDU2 : flux uncertainty |  |
| HISTORY | HDU3 : pixel bitmask |  |
| HISTORY | HDU4 : sky |  |
| HISTORY | HDU5 : sky uncertainty |  |
| HISTORY | HDU6 : telluric |  |
| HISTORY | HDU7 : telluric uncertainty |  |
| HISTORY | HDU8 : LSF table |  |
| HISTORY | HDU9 : RV table |  |



### HDU1: 


#### HDU Type: IMAGE
#### HDU Size:  267 KB

##### Header Table Caption for HDU1
Key | Value | Comment | |
| --- | --- | --- | --- |
| XTENSION | IMAGE |  |
| BITPIX | -64 |  |
| NAXIS | 2 |  |
| NAXIS1 | 8575 |  |
| NAXIS2 | 4 |  |
| PCOUNT | 0 |  |
| GCOUNT | 1 |  |
| CRVAL1 | 4.179 | Start log10(wavelength) |
| CDELT1 | 6e-06 | Dispersion in log10(wavelength) |
| CRPIX1 | 1 | Pixel of starting wavelength |
| CTYPE1 | LOG-LINEAR |  |
| BUNIT | Flux (10^-17 erg/s/cm^2/Ang) |  |



### HDU2: 


#### HDU Type: IMAGE
#### HDU Size:  267 KB

##### Header Table Caption for HDU2
Key | Value | Comment | |
| --- | --- | --- | --- |
| XTENSION | IMAGE |  |
| BITPIX | -64 |  |
| NAXIS | 2 |  |
| NAXIS1 | 8575 |  |
| NAXIS2 | 4 |  |
| PCOUNT | 0 |  |
| GCOUNT | 1 |  |
| CRVAL1 | 4.179 | Start log10(wavelength) |
| CDELT1 | 6e-06 | Dispersion in log10(wavelength) |
| CRPIX1 | 1 | Pixel of starting wavelength |
| CTYPE1 | LOG-LINEAR |  |
| BUNIT | Err (10^-17 erg/s/cm^2/Ang) |  |



### HDU3: 


#### HDU Type: IMAGE
#### HDU Size:  267 KB

##### Header Table Caption for HDU3
Key | Value | Comment | |
| --- | --- | --- | --- |
| XTENSION | IMAGE |  |
| BITPIX | 64 |  |
| NAXIS | 2 |  |
| NAXIS1 | 8575 |  |
| NAXIS2 | 4 |  |
| PCOUNT | 0 |  |
| GCOUNT | 1 |  |
| CRVAL1 | 4.179 | Start log10(wavelength) |
| CDELT1 | 6e-06 | Dispersion in log10(wavelength) |
| CRPIX1 | 1 | Pixel of starting wavelength |
| CTYPE1 | LOG-LINEAR |  |
| BUNIT | Pixel bitmask |  |



### HDU4: 


#### HDU Type: IMAGE
#### HDU Size:  267 KB

##### Header Table Caption for HDU4
Key | Value | Comment | |
| --- | --- | --- | --- |
| XTENSION | IMAGE |  |
| BITPIX | -64 |  |
| NAXIS | 2 |  |
| NAXIS1 | 8575 |  |
| NAXIS2 | 4 |  |
| PCOUNT | 0 |  |
| GCOUNT | 1 |  |
| CRVAL1 | 4.179 | Start log10(wavelength) |
| CDELT1 | 6e-06 | Dispersion in log10(wavelength) |
| CRPIX1 | 1 | Pixel of starting wavelength |
| CTYPE1 | LOG-LINEAR |  |
| BUNIT | Sky (10^-17 erg/s/cm^2/Ang) |  |



### HDU5: 


#### HDU Type: IMAGE
#### HDU Size:  267 KB

##### Header Table Caption for HDU5
Key | Value | Comment | |
| --- | --- | --- | --- |
| XTENSION | IMAGE |  |
| BITPIX | -64 |  |
| NAXIS | 2 |  |
| NAXIS1 | 8575 |  |
| NAXIS2 | 4 |  |
| PCOUNT | 0 |  |
| GCOUNT | 1 |  |
| CRVAL1 | 4.179 | Start log10(wavelength) |
| CDELT1 | 6e-06 | Dispersion in log10(wavelength) |
| CRPIX1 | 1 | Pixel of starting wavelength |
| CTYPE1 | LOG-LINEAR |  |
| BUNIT | Sky error (10^-17 erg/s/cm^2/Ang) |  |



### HDU6: 


#### HDU Type: IMAGE
#### HDU Size:  267 KB

##### Header Table Caption for HDU6
Key | Value | Comment | |
| --- | --- | --- | --- |
| XTENSION | IMAGE |  |
| BITPIX | -64 |  |
| NAXIS | 2 |  |
| NAXIS1 | 8575 |  |
| NAXIS2 | 4 |  |
| PCOUNT | 0 |  |
| GCOUNT | 1 |  |
| CRVAL1 | 4.179 | Start log10(wavelength) |
| CDELT1 | 6e-06 | Dispersion in log10(wavelength) |
| CRPIX1 | 1 | Pixel of starting wavelength |
| CTYPE1 | LOG-LINEAR |  |
| BUNIT | Telluric |  |



### HDU7: 


#### HDU Type: IMAGE
#### HDU Size:  267 KB

##### Header Table Caption for HDU7
Key | Value | Comment | |
| --- | --- | --- | --- |
| XTENSION | IMAGE |  |
| BITPIX | -64 |  |
| NAXIS | 2 |  |
| NAXIS1 | 8575 |  |
| NAXIS2 | 4 |  |
| PCOUNT | 0 |  |
| GCOUNT | 1 |  |
| CRVAL1 | 4.179 | Start log10(wavelength) |
| CDELT1 | 6e-06 | Dispersion in log10(wavelength) |
| CRPIX1 | 1 | Pixel of starting wavelength |
| CTYPE1 | LOG-LINEAR |  |
| BUNIT | Telluric error |  |



### HDU8: 


#### HDU Type: BINARY TABLE
#### HDU Size:  0 bytes

##### Header Table Caption for HDU8
Key | Value | Comment | |
| --- | --- | --- | --- |
| XTENSION | BINTABLE |  |
| BITPIX | 8 |  |
| NAXIS | 2 |  |
| NAXIS1 | 0 |  |
| NAXIS2 | 0 |  |
| PCOUNT | 0 |  |
| GCOUNT | 1 |  |
| TFIELDS | 0 |  |

##### Binary Table Caption for HDU8
Name | Type | Unit | Description |
| --- | --- | --- | --- |



### HDU9: 


#### HDU Type: BINARY TABLE
#### HDU Size:  38 KB

##### Header Table Caption for HDU9
Key | Value | Comment | |
| --- | --- | --- | --- |
| XTENSION | BINTABLE |  |
| BITPIX | 8 |  |
| NAXIS | 2 |  |
| NAXIS1 | 19644 |  |
| NAXIS2 | 2 |  |
| PCOUNT | 0 |  |
| GCOUNT | 1 |  |
| TFIELDS | 19 |  |
| TDIM14 | (801) |  |
| TDIM15 | (801) |  |
| TDIM16 | (801) |  |

##### Binary Table Caption for HDU9
Name | Type | Unit | Description |
| --- | --- | --- | --- |
 | FILENAME | char[300] |  |  |
 | SNR | float64 |  |  |
 | VHELIO | float64 | km/s | Heliocentric velocity derived from VREL |
 | VREL | float64 | km/s | RVs of all visits as determined by cross-correlation of reampled visit spectrum with combined spectrum, and cross-correlation of combined spectrum with best matching template |
 | VRELERR | float64 | km/s | Error estimate for VREL |
 | TEFF | float64 |  | Teff for template spectrum that best matches combined spectrum |
 | TEFFERR | float64 |  |  |
 | LOGG | float64 |  | log g for template spectrum that best matches combined spectrum |
 | LOGGERR | float64 |  |  |
 | FEH | float64 |  | [Fe/H] for template spectrum that best matches combined spectrum |
 | FEHERR | float64 |  |  |
 | CHISQ | float64 |  |  |
 | BC | float64 | km/s | Barycentric correction |
 | X_CCF | float64[801] |  |  |
 | CCF | float64[801] |  | Cross-correlation function of combined spectra and individual visits with best-matching template from mini-grid |
 | CCFERR | float64[801] |  | CCF error array |
 | XCORR_VREL | float64 |  |  |
 | XCORR_VRELERR | float64 |  |  |
 | XCORR_VHELIO | float64 |  |  |



---
## Notes
None

---
## Regrets
I have no regrets!