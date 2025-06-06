# Data Model: mos_target_skymapper_gaia


MOS Target table: mos_target_skymapper_gaia


## Contents
- [Basic Information](#basic-information)
- [Changelog](#changelog)
- [Example HDUS List](#example-hdus-list)
- [Notes](#notes)
- [Regrets](#regrets)
---

## Basic Information
This catalogue contains photometric stellar parameters for 9+ million stars in common between the SkyMapper survey and Gaia DR2. See https://skymapper.anu.edu.au/_data/sm-gaia/ for details.

### Naming Convention
$MOS_TARGET/[V_TARG]/mos_skymapper_gaia.fits, where V_TARG=1.0.2 for DR19

### Releases
DR19

### Enviroments
MOS_TARGET

### Approximate Size
61 MB

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
MOS Target table: mos_target_skymapper_gaia

#### HDU Type: BINARY TABLE
#### HDU Size:  61 MB

##### Header Table Caption for HDU1
Key | Value | Comment | |
| --- | --- | --- | --- |
| XTENSION | BINTABLE | binary table extension |
| BITPIX | 8 | array data type |
| NAXIS | 2 | number of array dimensions |
| NAXIS1 | 32 | length of dimension 1 |
| NAXIS2 | 2000000 | length of dimension 2 |
| PCOUNT | 0 | number of group parameters |
| GCOUNT | 1 | number of groups |
| TFIELDS | 6 | number of table fields |
| TNULL1 | -9223372036854775808 |  |
| TNULL2 | -9223372036854775808 |  |

##### Binary Table Caption for HDU1
Name | Type | Unit | Description |
| --- | --- | --- | --- |
 | skymapper_object_id | int64 |  | SkyMapper object_id |
 | gaia_source_id | int64 |  | Gaia DR2 source_id |
 | teff | float32 | K | Effective temperature |
 | e_teff | float32 | K | Effective temperature uncertainty |
 | feh | float32 | dex | Metallicity |
 | e_feh | float32 | dex | Metallicity uncertainty |



---
## Notes
None

---
## Regrets
I  have no regrets!