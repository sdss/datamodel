# Data Model: mos_target_field


MOS Target table: mos_target_field


## Contents
- [Basic Information](#basic-information)
- [Changelog](#changelog)
- [Example HDUS List](#example-hdus-list)
- [Notes](#notes)
- [Regrets](#regrets)
---

## Basic Information
The table includes the field information, where a field is a unique pointing of the telescope on the sky.

### Naming Convention
$MOS_TARGET/[V_TARG]/mos_field.fits, where V_TARG=1.0.2 for DR19

### Releases
DR19

### Enviroments
MOS_TARGET

### Approximate Size
7 MB

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
MOS Target table: mos_target_field

#### HDU Type: BINARY TABLE
#### HDU Size:  7 MB

##### Header Table Caption for HDU1
Key | Value | Comment | |
| --- | --- | --- | --- |
| XTENSION | BINTABLE | binary table extension |
| BITPIX | 8 | array data type |
| NAXIS | 2 | number of array dimensions |
| NAXIS1 | 193 | length of dimension 1 |
| NAXIS2 | 38919 | length of dimension 2 |
| PCOUNT | 0 | number of group parameters |
| GCOUNT | 1 | number of groups |
| TFIELDS | 9 | number of table fields |
| TNULL1 | -2147483648 |  |
| TNULL4 | -2147483648 |  |
| TNULL5 | -2147483648 |  |
| TNULL6 | -2147483648 |  |
| TNULL9 | -2147483648 |  |

##### Binary Table Caption for HDU1
Name | Type | Unit | Description |
| --- | --- | --- | --- |
 | pk | int32 |  | The primary key. A sequential identifier. |
 | racen | float64 |  | The Right Ascension of the center of the field. |
 | deccen | float64 |  | The Declination of the center of the field. |
 | version_pk | int32 |  | The primary key of the version in the dr19_version table. |
 | cadence_pk | int32 |  | The primary key of the cadence in the dr19_cadence table. |
 | observatory_pk | int32 |  | The primary key of the observatory in the dr19_observatory table. |
 | position_angle | float32 |  | The position angle of the field E of N in degrees. |
 | slots_exposures | char[153] |  | Exposures assigned to each LST and sky brightness slot |
 | field_id | int32 |  | The idenifier of a field within a version of the survey plan. |



---
## Notes
None

---
## Regrets
I  have no regrets!