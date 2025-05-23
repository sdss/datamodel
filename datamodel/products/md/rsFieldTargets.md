# Data Model: rsFieldTargets


Targets for a particular field


## Contents
- [Basic Information](#basic-information)
- [Changelog](#changelog)
- [Example HDUS List](#example-hdus-list)

---

## Basic Information
Targets in the area around a particular field. Produced by robostrategy's rs_field_targets, using the tofits() method of the Field class. No cadence set or assignments performed.

### Naming Convention
$ROBOSTRATEGY_DATA/allocations/[PLAN]/targets/rsFieldTargets-[PLAN]-[OBSERVATORY]-[FIELDID].fits

### Releases
WORK

### Enviroments
ROBOSTRATEGY_DATA

### Approximate Size
5 MB

### File Type
FITS

### Generated by Product
robostrategy

### HDUS List for release WORK
  - [HDU0: PRIMARY](#hdu0-primary)
  - [HDU1: TARGETS](#hdu1-targets)
  - [HDU2: DESMODE](#hdu2-desmode)

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
| SIMPLE | True | file does conform to FITS standard |
| BITPIX | 16 | number of bits per data pixel |
| NAXIS | 0 | number of data axes |
| EXTEND | True | FITS dataset may contain extensions |
| COMMENT |   FITS (Flexible Image Transport System) format is defined in 'Astronomy |  |
| COMMENT |   and Astrophysics', volume 376, page 359; bibcode: 2001A&A...376..359H |  |
| STRATVER | 1.0.6dev | robostrategy version |
| SCHEDVER | 0.9.1 | roboscheduler version |
| MUGATVER | 0.1.0alpha | mugatu version |
| KAIJUVER | 1.0.0 | kaiju version |
| RACEN | 292.128118909909 | RA J2000 center of field (deg) |
| DECCEN | 25.2620206919673 | Dec J2000 center of field (deg) |
| OBS | apo | observatory used for field |
| PA | 54.7425765991211 | position angle (deg E of N) |
| FCADENCE | none | field cadence |
| CBUFFER | 2.0 | kaiju collision buffer |
| NOCALIB | False | True if this field ignores calibrations |
| RCNAME0 | sky_boss | required calibration category |
| RCNUM0 |  | number required per exposure |
| RCNAME1 | standard_boss | required calibration category |
| RCNUM1 |  | number required per exposure |
| RCNAME2 | sky_apogee | required calibration category |
| RCNUM2 |  | number required per exposure |
| RCNAME3 | standard_apogee | required calibration category |
| RCNUM3 |  | number required per exposure |



### HDU1: TARGETS
Targets in field

#### HDU Type: BINARY TABLE
#### HDU Size:  10 MB

##### Binary Table Caption for HDU1
Name | Type | Unit | Description |
| --- | --- | --- | --- |
 | RSASSIGN | int32 |  | Set to 0 if not to be assigned, 1 if to be assigned, 2 if an open target assignment |
 | RSID | int64 |  | robostrategy unique ID |
 | CARTON_TO_TARGET_PK | int64 |  | primary key for carton_to_target table |
 | PRIORITY | int32 |  | priority for assignment (lower numbers assigned first) |
 | VALUE | float32 |  | value to be used for cadence allocation to fields |
 | LAMBDA_EFF | float32 | Angstrom | effective wavelength for observation |
 | DELTA_RA | float64 | arcsec | RA offset of observation from nominal object position |
 | DELTA_DEC | float64 | arcsec | Dec offset of observation from nominal object position |
 | RA | float64 | deg | Object position in RA J2000 |
 | DEC | float64 | deg | Object position in Dec J2000 |
 | EPOCH | float32 | years | Epoch of RA/Dec |
 | PMRA | float32 | mas/year | Proper motion in RA |
 | PMDEC | float32 | mas/year | Proper motion in Dec |
 | PARALLAX | float32 | arcsec | Parallax |
 | CATALOGID | int64 |  | Unique id in catalog table of catalogdb |
 | TARGET_PK | int64 |  | Primary key in target table in targetdb |
 | MAGNITUDE | float32[7] | mag | Array of magnitudes (g, r, i, BP, G, RP, H) |
 | CARTON | char[50] |  | Name of carton for this target |
 | CARTON_PK | int32 |  | Primary key of carton for this target's carton |
 | PROGRAM | char[15] |  | Name of program for this target |
 | MAPPER | char[3] |  | Name of mapper for this target |
 | CATEGORY | char[15] |  | Category of target, one of 'science', 'sky_boss', 'standard_boss', 'sky_apogee', and 'standard_apogee' |
 | CADENCE | char[22] |  | Desired cadence of target |
 | FIBERTYPE | char[6] |  | Fiber type desired |
 | PLAN | char[8] |  | Plan associated with targeting version |
 | TAG | char[8] |  | Tag associated with targeting version |
 | X | float64 | mm | X position in focal plane |
 | Y | float64 | mm | Y position in focal plane |
 | WITHIN | int32 |  | target is covered by a robot with right fiber type |
 | INCADENCE | int32 |  | target is observable in field cadence (all 0 in this file) |



### HDU2: DESMODE
Available design modes

#### HDU Type: BINARY TABLE
#### HDU Size:  6 KB

##### Binary Table Caption for HDU2
Name | Type | Unit | Description |
| --- | --- | --- | --- |
 | LABEL | char[30] |  | name of design mode |
 | BOSS_N_SKIES_MIN | float64 |  | Minimum number of skies for BOSS |
 | APOGEE_N_SKIES_MIN | float64 |  | Minimum number of skies for APOGEE |
 | BOSS_MIN_SKIES_FOVMETRIC | float64[3] |  | Minimum FOV metric for BOSS skies |
 | APOGEE_MIN_SKIES_FOVMETRIC | float64[3] |  | Minimum FOV metric for APOGEE skies |
 | BOSS_N_STDS_MIN | float64 |  | Minimum number of standards for BOSS |
 | APOGEE_N_STDS_MIN | float64 |  | Minimum number of standards for APOGEE |
 | BOSS_MIN_STDS_FOVMETRIC | float64[3] |  | Minimum FOV metric for BOSS standards |
 | APOGEE_MIN_STDS_FOVMETRIC | float64[3] |  | Minimum FOV metric for APOGEE standards |
 | BOSS_STDS_MAGS | float64[7, 2] | mag | Minimum and maximum magnitude for BOSS standard in (g, r, i, BP, G, RP, H) |
 | APOGEE_STDS_MAGS | float64[7, 2] | mag | Minimum and maximum magnitude for APOGEE standard in (g, r, i, BP, G, RP, H) |
 | BOSS_BRIGHT_LIMIT_TARGETS | float64[7, 2] | mag | Minimum and maximum magnitude for BOSS target in (g, r, i, BP, G, RP, H) |
 | APOGEE_BRIGHT_LIMIT_TARGETS | float64[7, 2] | mag | Minimum and maximum magnitude for APOGEE target in (g, r, i, BP, G, RP, H) |
 | BOSS_SKY_NEIGHBORS_TARGETS | float64 |  | ??? |
 | APOGEE_SKY_NEIGHBORS_TARGETS | float64 |  | ??? |
 | APOGEE_TRACE_DIFF_TARGETS | float64 | mag | maximum difference in H mag for targets neighboring on slit |


