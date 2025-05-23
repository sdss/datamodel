# Data Model: mos_target_opsdb_apo_camera_frame


MOS Target table: mos_target_opsdb_apo_camera_frame


## Contents
- [Basic Information](#basic-information)
- [Changelog](#changelog)
- [Example HDUS List](#example-hdus-list)
- [Notes](#notes)
- [Regrets](#regrets)
---

## Basic Information
The table contains signal-to-noise estimates for each 'camera', for each exposure. APOGEE is treated as one camera, while R1/2 and B1/2 are treated separately.

### Naming Convention
$MOS_TARGET/[V_TARG]/mos_opsdb_apo_camera_frame.fits, where V_TARG=1.0.2 for DR19

### Releases
DR19

### Enviroments
MOS_TARGET

### Approximate Size
3 MB

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
MOS Target table: mos_target_opsdb_apo_camera_frame

#### HDU Type: BINARY TABLE
#### HDU Size:  3 MB

##### Header Table Caption for HDU1
Key | Value | Comment | |
| --- | --- | --- | --- |
| XTENSION | BINTABLE | binary table extension |
| BITPIX | 8 | array data type |
| NAXIS | 2 | number of array dimensions |
| NAXIS1 | 118 | length of dimension 1 |
| NAXIS2 | 29792 | length of dimension 2 |
| PCOUNT | 0 | number of group parameters |
| GCOUNT | 1 | number of groups |
| TFIELDS | 5 | number of table fields |
| TNULL1 | -2147483648 |  |
| TNULL2 | -2147483648 |  |
| TNULL3 | -32768 |  |

##### Binary Table Caption for HDU1
Name | Type | Unit | Description |
| --- | --- | --- | --- |
 | pk | int32 |  | Unique identifier |
 | exposure_pk | int32 |  | Unique identifier in the exposure table |
 | camera_pk | int16 |  | Unique identifier in the camera table |
 | sn2 | float32 |  | Signal-to-noise squared estimate from on-mountain quick reduction pipelines |
 | comment | char[104] |  | An optional comment |



---
## Notes
None

---
## Regrets
I  have no regrets!