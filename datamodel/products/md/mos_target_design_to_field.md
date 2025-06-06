# Data Model: mos_target_design_to_field


MOS Target table: mos_target_design_to_field


## Contents
- [Basic Information](#basic-information)
- [Changelog](#changelog)
- [Example HDUS List](#example-hdus-list)
- [Notes](#notes)
- [Regrets](#regrets)
---

## Basic Information
Connects a design to a given field within a version of the survey. Sets the placement of the design in the overall exposure sequence for that field.

### Naming Convention
$MOS_TARGET/[V_TARG]/mos_design_to_field.fits, where V_TARG=1.0.2 for DR19

### Releases
DR19

### Enviroments
MOS_TARGET

### Approximate Size
5 MB

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
MOS Target table: mos_target_design_to_field

#### HDU Type: BINARY TABLE
#### HDU Size:  5 MB

##### Header Table Caption for HDU1
Key | Value | Comment | |
| --- | --- | --- | --- |
| XTENSION | BINTABLE | binary table extension |
| BITPIX | 8 | array data type |
| NAXIS | 2 | number of array dimensions |
| NAXIS1 | 28 | length of dimension 1 |
| NAXIS2 | 218694 | length of dimension 2 |
| PCOUNT | 0 | number of group parameters |
| GCOUNT | 1 | number of groups |
| TFIELDS | 5 | number of table fields |
| TNULL1 | -2147483648 |  |
| TNULL2 | -2147483648 |  |
| TNULL3 | -2147483648 |  |
| TNULL4 | -9223372036854775808 |  |
| TNULL5 | -9223372036854775808 |  |

##### Binary Table Caption for HDU1
Name | Type | Unit | Description |
| --- | --- | --- | --- |
 | pk | int32 |  | The primary key. A sequential identifier. |
 | design_id | int32 |  | The primary key of the design in the dr19_design table. |
 | field_pk | int32 |  | The primary key of the field in the dr19_field table. |
 | exposure | int64 |  | The 0-indexed exposure number in the lunation sequence for the field. |
 | field_exposure | int64 |  | The 0-indexed overall exposure number in the sequence for the field. |



---
## Notes
None

---
## Regrets
I  have no regrets!