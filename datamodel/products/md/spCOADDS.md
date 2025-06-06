# Data Model: spCOADDS


Custom Coadd Schema Plans


## Contents
- [Basic Information](#basic-information)
- [Changelog](#changelog)
- [Example PAR List](#example-par-list)
- [Notes](#notes)

---

## Basic Information
Contains the Schema used to defined the Custom target level Coadding schema

### Naming Convention
$BOSS_SPECTRO_REDUX/[RUN2D]/[PHASE]_[SURVEY]_COADDS.par

### Releases
IPL3, DR19

### Enviroments
BOSS_SPECTRO_REDUX

### Approximate Size
895 bytes

### File Type
PAR

### Generated by Product
idlspec2d - manage_coadd_Schema.py

### Is a VAC
False

### PAR List for release DR19
  - [SCHEMA](#SCHEMA)

---

## Changelog
Describes changes to the datamodel product and/or file structure from one release to another
 - DR19
   - from: IPL3
   - note: No changes

---
## Example PAR List
### Comments
```
#%yanny
# Table
#
# Schema Description for custom BOSS Coadds
#
# Last Updated Fri Apr 06 22:37:45 2023
# Written by manage_coadd_Schema.py
#
#    Legacy is a currently unutilized, but there for future versions to include tags from SDSS-IV,-III etc in addition to current tag
#
```

### Header

Key | Value | Comment | |
| --- | --- | --- | --- |
| SDSS_GEN | SDSS-V | The associated SDSS Generation (or phase) |
| SURVEY | BHM | The associated survey |
| Filename | /uufs/chpc.utah.edu/common/home/sdss50/sdsswork/bhm/boss/spectro/redux/v6_1_3/SDSSV_BHM_COADDS.par | the filename (and path) of this file |


### Tables


#### SCHEMA
- Description: The Coadding Schema
- Number of Rows: 1

#### Structure
Name | Type | Unit | Description | Is Array | Example |
| --- | --- | --- | --- | --- | --- |
 | NAME | char[8] | ;; | Name of the Custom Coadd Schema | False | allepoch |
 | CARTON | char[5][25] |  | List of Cartons to include (can include wild cards) | True | ['*spiders*', '*bhm_gua*', '*bhm_csc*', '*mwm_erosita*', '*bhm_colr_galaxies*'] |
 | SDSS_ID | char[1][1] |  | List of SDSS_IDs to select (or CatalogIDs if use_catid is set) | True | [''] |
 | LEGACY | char[1][1] |  | Not used at present, but designed for legacy coadding | True | [''] |
 | CADENCE | double | days | Coadding Cadence (0.0 for open-ended) | False | 0.0 |
 | MJD | char[1][1] |  | list of MJDs to include | True | [''] |
 | PROGRAM | char[1][1] |  | List of Programs to select | True | [''] |
 | DR | long |  | DR/IPL Coadding (1:True, 2:False) | False | 1 |
 | RERUN1D | long |  | Rerun 1D analysis of custom coadd  (1:True, 2:False) | False | 1 |
 | ACTIVE | long |  | Is this an active Schema (1:True, 2:False) | False | 1 |
 | USE_CATID | long |  | Use CatalogIDs rather than SDSS_IDs  (1:True, 2:False) | False | 1 |
 | USE_FIRSTCARTON | long |  | Use Firstcarton only for carton match (dont look at db)   (1:True, 2:False) | False | 0 |


---
## Notes
None