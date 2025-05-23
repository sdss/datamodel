# Data Model: mos_target_zari18pms


MOS Target Table: zari18pms


## Contents
- [Basic Information](#basic-information)
- [Changelog](#changelog)
- [Example HDUS List](#example-hdus-list)
- [Notes](#notes)
- [Regrets](#regrets)
---

## Basic Information
Pre-main sequence (PMS) catalogue from Zari+2018.

### Naming Convention
$MOS_TARGET/[V_TARG]/mos_zari18pms-[NUM].fits, where V_TARG=1.0.1 for DR18; and NUM = 1..1 to partition the file into parts

### Releases
DR18, DR19

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
 - DR19
   - from: DR18
   - note: No changes

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
MOS Target Table: zari18pms

#### HDU Type: BINARY TABLE
#### HDU Size:  3 MB

##### Header Table Caption for HDU1
Key | Value | Comment | |
| --- | --- | --- | --- |
| XTENSION | BINTABLE | binary table extension |
| BITPIX | 8 | array data type |
| NAXIS | 2 | number of array dimensions |
| NAXIS1 | 96 | length of dimension 1 |
| NAXIS2 | 43151 | length of dimension 2 |
| PCOUNT | 0 | number of group parameters |
| GCOUNT | 1 | number of groups |
| TFIELDS | 21 | number of table fields |
| TNULL1 | -9223372036854775808 |  |
| TNULL18 | -2147483648 |  |

##### Binary Table Caption for HDU1
Name | Type | Unit | Description |
| --- | --- | --- | --- |
 | source | int64 |  | Unique source identifier (Gaia DR2 source_id) |
 | glon | float64 | deg | Galactic longitude |
 | glat | float64 | deg | Galactic latitude |
 | plx | float32 | mas | Parallax |
 | e_plx | float32 | mas | Standard error of parallax (parallax_error) |
 | pmglon | float32 | mas/yr | Proper motion in galactic longitude |
 | e_pmglon | float32 | mas/yr | Standard error of proper motion in galactic longitude |
 | pmglat | float32 | mas/yr | Proper motion in galactic latitude |
 | e_pmglat | float32 | mas/yr | Standard error of proper motion in galactic latitude |
 | pmlbcorr | float32 |  | Correlation between proper motion in galactic longitude and proper motion in galactic latitude |
 | rv | float32 | km/s | radial velocity |
 | e_rv | float32 | km/s | radial velocity error |
 | gmag | float32 | mag | G-band mean magnitude (phot_g_mean_mag) |
 | bpmag | float32 | mag | BP-band mean magnitude (phot_bp_mean_mag) |
 | rpmag | float32 | mag | RP-band mean magnitude (phot_g_mean_mag) |
 | bp_over_rp | float32 |  | BP/RP excess factor |
 | chi2al | float32 |  | AL chi-square value (astrometric_chi2_al) |
 | ngal | int32 |  | Number of good observation AL (astrometric_n_good_obs_al) |
 | ag | float32 | mag | Extinction in G-band (A_G) |
 | bp_rp | float32 | mag | Colour excess in BP-RP |
 | uwe | float32 |  | Unit Weight Error, as defined in Lindegren et al., 2018A&A...616A...2L |



---
## Notes
None

---
## Regrets
I have no regrets!