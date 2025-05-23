# Data Model: mos_target_mastar_goodvisits


MOS Target table: mos_target_mastar_goodvisits


## Contents
- [Basic Information](#basic-information)
- [Changelog](#changelog)
- [Example HDUS List](#example-hdus-list)
- [Notes](#notes)
- [Regrets](#regrets)
---

## Basic Information
Summary file of all visits of stars included in MaNGA Stellar Libary.

### Naming Convention
$MOS_TARGET/[V_TARG]/mos_mastar_goodvisits.fits, where V_TARG=1.0.2 for DR19

### Releases
DR19

### Enviroments
MOS_TARGET

### Approximate Size
10 MB

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
MOS Target table: mos_target_mastar_goodvisits

#### HDU Type: BINARY TABLE
#### HDU Size:  10 MB

##### Header Table Caption for HDU1
Key | Value | Comment | |
| --- | --- | --- | --- |
| XTENSION | BINTABLE | binary table extension |
| BITPIX | 8 | array data type |
| NAXIS | 2 | number of array dimensions |
| NAXIS1 | 189 | length of dimension 1 |
| NAXIS2 | 59266 | length of dimension 2 |
| PCOUNT | 0 | number of group parameters |
| GCOUNT | 1 | number of groups |
| TFIELDS | 37 | number of table fields |
| TNULL4 | -2147483648 |  |
| TNULL6 | -2147483648 |  |
| TNULL17 | -2147483648 |  |
| TNULL19 | -32768 |  |
| TNULL20 | -32768 |  |
| TNULL23 | -32768 |  |
| TNULL26 | -32768 |  |
| TNULL27 | -32768 |  |
| TNULL29 | -2147483648 |  |
| TNULL31 | -32768 |  |
| TNULL37 | -9223372036854775808 |  |

##### Binary Table Caption for HDU1
Name | Type | Unit | Description |
| --- | --- | --- | --- |
 | drpver | char[6] |  | Version of mangadrp. |
 | mprocver | char[6] |  | Version of mastarproc. |
 | mangaid | char[22] |  | MaNGA-ID for the object. |
 | plate | int32 |  | Plate ID. |
 | ifudesign | char[5] |  | IFUDESIGN for the fiber bundle. |
 | mjd | int32 |  | Modified Julian Date for this visit. |
 | ifura | float64 | deg | Right Ascension of the center of the IFU. |
 | ifudec | float64 | deg | Declination of the center of the IFU. |
 | ra | float64 | deg | Right Ascension for this object at the time given by the EPOCH column (Equinox J2000). |
 | dec | float64 | deg | Declination for this object at the time given by the EPOCH column (Equinox J2000). |
 | epoch | float32 |  | Epoch of the astrometry (which is approximate for some catalogs). |
 | psfmag_1 | float32 | mag | PSF magnitude in the first band with the filter correspondence depending on PHOTOCAT. |
 | psfmag_2 | float32 | mag | PSF magnitude in the second band with the filter correspondence depending on PHOTOCAT. |
 | psfmag_3 | float32 | mag | PSF magnitude in the third band with the filter correspondence depending on PHOTOCAT. |
 | psfmag_4 | float32 | mag | PSF magnitude in the fourth band with the filter correspondence depending on PHOTOCAT. |
 | psfmag_5 | float32 | mag | PSF magnitude in the fifth band with the filter correspondence depending on PHOTOCAT. |
 | mngtarg2 | int32 |  | MANGA_TARGET2 targeting bitmask. |
 | exptime | float32 | sec | Median exposure time for all exposures on this visit. |
 | nexp_visit | int16 |  | Total number of exposures during this visit. This column was named 'NEXP' in DR15/16. |
 | nvelgood | int16 |  | Number of exposures (from all visits of this PLATE-IFUDESIGN) with good velocity measurements. |
 | heliov | float32 | km/s | Median heliocentric velocity of all exposures on all visits that yield good velocity measurements. This is used to shift the spectra to the rest frame. |
 | verr | float32 | km/s | 1-sigma uncertainty of the heliocentric velocity |
 | v_errcode | int16 |  | Error code for HELIOV. Zero is good, nonzero is bad. |
 | heliov_visit | float32 | km/s | Median heliocentric velocity of good exposures from only this visit, rather than from all visits. |
 | verr_visit | float32 | km/s | 1-sigma uncertainty of HELIOV_VISIT. |
 | v_errcode_visit | int16 |  | Error code for HELIOV_VISIT. Zero is good, nonzero is bad. |
 | velvarflag | int16 |  | Flag indicating the significant variation of the heliocentric velocity from visit to visit. A value of 1 means the variation is beyond 3-sigma between at least two of the visits. A value of 0 means all variations between pairs of visits are less than 3-sigma. |
 | dv_maxsig | float32 |  | Maximum significance in velocity variation between pairs of visits. |
 | mjdqual | int32 |  | Spectral quality bitmask (MASTAR_QUAL). |
 | bprperr_sp | float32 |  | Uncertainty in the synthetic Bp-Rp color derived from the spectra. |
 | nexp_used | int16 |  | Number of exposures used in constructing the visit spectrum. |
 | s2n | float32 |  | Median signal-to-noise ratio per pixel of this visit spectrum. |
 | s2n10 | float32 |  | Top 10-th percentile signal-to-noise ratio per pixel of this visit spectrum. |
 | badpixfrac | float32 |  | Fraction of bad pixels (those with inverse variance being zero.) |
 | coord_source | char[9] |  | Source of astrometry. |
 | photocat | char[9] |  | Source of photometry. |
 | pk | int64 |  | Primary key. Sequential identifier for this table. |



---
## Notes
None

---
## Regrets
I  have no regrets!