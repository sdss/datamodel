# Data Model: mos_target_targeting_generation_to_carton


MOS Target table: mos_target_targeting_generation_to_carton


## Contents
- [Basic Information](#basic-information)
- [Changelog](#changelog)
- [Example HDUS List](#example-hdus-list)
- [Notes](#notes)
- [Regrets](#regrets)
---

## Basic Information
A 'targeting_generation' describes a collection of versioned cartons, together with their robostrategy control parameters. This is a convenient way to describe the specific set of carton-versions that were used (and the way that they were treated) within any particular run of robostrategy.  The dr19_targeting_generation_to_carton table describes a many-to-many relationship, connecting each targeting_generation to a set of entries in the dr19_carton table, as well as recording how those carton-versions were treated in the robostrategy code (i.e. the rs_stage and rs_active parameters).  Taken together, the dr19_targeting_generation, dr19_targeting_generation_to_carton and dr19_targeting_generation_to_version tables duplicate, in a database form, the robostrategy carton configuration information available via the rsconfig product (https://github.com/sdss/rsconfig).

### Naming Convention
$MOS_TARGET/[V_TARG]/mos_targeting_generation_to_carton.fits, where V_TARG=1.0.2 for DR19

### Releases
DR19

### Enviroments
MOS_TARGET

### Approximate Size
19 KB

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
MOS Target table: mos_target_targeting_generation_to_carton

#### HDU Type: BINARY TABLE
#### HDU Size:  11 KB

##### Header Table Caption for HDU1
Key | Value | Comment | |
| --- | --- | --- | --- |
| XTENSION | BINTABLE | binary table extension |
| BITPIX | 8 | array data type |
| NAXIS | 2 | number of array dimensions |
| NAXIS1 | 19 | length of dimension 1 |
| NAXIS2 | 640 | length of dimension 2 |
| PCOUNT | 0 | number of group parameters |
| GCOUNT | 1 | number of groups |
| TFIELDS | 5 | number of table fields |
| TNULL1 | -2147483648 |  |
| TNULL2 | -2147483648 |  |
| TNULL3 | -2147483648 |  |

##### Binary Table Caption for HDU1
Name | Type | Unit | Description |
| --- | --- | --- | --- |
 | pk | int32 |  | primary key for this table entry |
 | generation_pk | int32 |  | primary key of an entry in the dr19_targeting_generation table |
 | carton_pk | int32 |  | primary key of an entry in the dr19_carton table, i.e. a carton-version |
 | rs_stage | char[6] |  | the algorithimic stage of robostrategy in which targets from this carton-version are considered for assignment. Options: 'none', 'plates', 'srd', 'filler', or 'open'. See the robostrategy documentation for further information. |
 | rs_active | bool |  | a Boolean column describing whether the carton-version is considered within robostrategy |



---
## Notes
None

---
## Regrets
I  have no regrets!