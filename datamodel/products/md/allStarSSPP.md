# Data Model: allStarSSPP


SSPP stellar parameters


## Contents
- [Basic Information](#basic-information)
- [Changelog](#changelog)
- [Example HDUS List](#example-hdus-list)
- [Notes](#notes)

---

## Basic Information
This is a value added catalog, and contains Teff, logg, [Fe/H], [C/Fe], and [alpha/Fe] derived by SEGUE Stellar Parameter Pipeline (SSPP) for stars with S/N > 10 and the temperature range 4400 - 7000 K.

### Naming Convention
allStar-SSPP-BOSS_pipeline.fits

### Releases
WORK

### Enviroments
MWM_SSPP

### Approximate Size
13 MB

### File Type
FITS

### Generated by Product
SSPP

### Is a VAC
False

### HDUS List for release WORK
  - [HDU0: PRIMARY](#hdu0-primary)
  - [HDU1: ](#hdu1)

---

## Changelog
This is a value added catalog specifically generated for IPL-1.

---
## Example HDUS List

### HDU0: PRIMARY
Null extension

#### HDU Type: IMAGE
#### HDU Size:  0 bytes

##### Header Table Caption for HDU0
Key | Value | Comment | |
| --- | --- | --- | --- |
| SIMPLE | True | Dummy Created by MWRFITS v1.11 |
| BITPIX | 8 | Dummy primary header created by MWRFITS |
| NAXIS | 0 | No data is associated with this header |
| EXTEND | True | Extensions may (will!) be present |



### HDU1:
HDU1 contains the stellar parameters.

#### HDU Type: BINARY TABLE
#### HDU Size:  13 MB

##### Header Table Caption for HDU1
Key | Value | Comment | |
| --- | --- | --- | --- |
| XTENSION | BINTABLE | Written by IDL:  Fri Oct 28 03:17:55 2022 |
| BITPIX | 8 |  |
| NAXIS | 2 | Binary table |
| NAXIS1 | 104 | Number of bytes per row |
| NAXIS2 | 131393 | Number of rows |
| PCOUNT | 0 | Random parameter count |
| GCOUNT | 1 | Group count |
| TFIELDS | 18 | Number of columns |
| SSPP_VER | v22_02 | Version of the SSPP |
| CREATION | Thu Oct 27 18:17:55 2022 | Creation Date |

##### Binary Table Caption for HDU1
Name | Type | Unit | Description |
| --- | --- | --- | --- |
 | FIELD | int32 |  | Field number |
 | MJD | int32 |  | Modified Julian Date |
 | TARGET_INDEX | int16 |  | Target index |
 | SPSPEC | char[17] |  | Field-MJD-Target_index |
 | TEFF | int16 | K | Estimated Teff |
 | TEFF_ERR | float32 | K | Error in Teff |
 | LOGG | float32 |  | Estimated log g |
 | LOGG_ERR | float32 | dex | Error in log g |
 | FEH | float32 |  | Estimated [Fe/H] |
 | FEH_ERR | float32 | dex | Error in [Fe/H] |
 | AFE | float32 |  | Estimated [alpha/Fe] |
 | AFE_ERR | float32 | dex | Error in [alpha/Fe] |
 | CFE | float32 |  | Estimated [C/Fe] |
 | CFE_ERR | float32 | dex | Error in [C/Fe] |
 | SNR | float32 |  | Average S/N per pixel over 4000 - 8000 A |
 | RA | float64 | degree | RA in degree |
 | DEC | float64 | degree | DEC in degree |
 | CATALOGID | char[19] |  | Catalog ID |



---
## Notes
None