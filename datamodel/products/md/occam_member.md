# Data Model: occam_member


The OCCAM member summary table provides positional, identification, and membership information for 1196 candidate open cluster member stars.



## Contents
- [Basic Information](#basic-information)
- [Changelog](#changelog)
- [Example HDUS List](#example-hdus-list)
- [Notes](#notes)
- [Regrets](#regrets)
---

## Basic Information
The OCCAM member summary table provides the proper motion membership probabilities from Cantat-Gaudin et al. 2020 and Hunt and Reffert 2023 alongside the radial velocity and [Fe/H] membership probabilities from MWM/APOGEE. Basic postional information is included with source IDs from Gaia DR2/3 and SDSS-V DR19 for each star in the table.


### Naming Convention
$APOGEE_OCCAM/occam_member-[VERS].fits where VERS is DR19 in the latest version

### Releases
DR19

### Enviroments
APOGEE_OCCAM

### Approximate Size
216 KB

### File Type
FITS

### Generated by Product
OCCAM

### Is a VAC
True

### Data Level
3.3.0

### HDUS List for release DR19
  - [HDU0: PRIMARY](#hdu0-primary)
  - [HDU1: OCCAM data](#hdu1-occam data)

---

## Changelog
Describes changes to the datamodel product and/or file structure from one release to another

---
## Example HDUS List

### HDU0: PRIMARY
The primary HDU, in accordance with the FITS file standard. No useful information is stored here

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



### HDU1: OCCAM data
The data reported are as follows:


#### HDU Type: BINARY TABLE
#### HDU Size:  206 KB

##### Header Table Caption for HDU1
Key | Value | Comment | |
| --- | --- | --- | --- |
| XTENSION | BINTABLE | binary table extension |
| BITPIX | 8 | 8-bit bytes |
| NAXIS | 2 | 2-dimensional binary table |
| NAXIS1 | 177 | width of table in bytes |
| NAXIS2 | 1196 | number of rows in table |
| PCOUNT | 0 | size of special data area |
| GCOUNT | 1 | one data group (required keyword) |
| TFIELDS | 23 | number of fields in each row |

##### Binary Table Caption for HDU1
Name | Type | Unit | Description |
| --- | --- | --- | --- |
 | Cluster | char[20] | --- | Open cluster name   1 |
 | SDSS_ID | int64 | --- | Internal SDSS-V source ID   2 |
 | GaiaDR3_ID | int64 | --- | Gaia DR3 source ID   3 |
 | GaiaDR2_ID | int64 | --- | Gaia DR2 source ID   4 |
 | OBJ_ID | char[32] | --- | DR17 APOGEE ID 5 |
 | GLON | float32 | deg | Galactic longitude   6 |
 | GLAT | float32 | deg | Galactic latitude   7 |
 | RAdeg | float64 | deg | Right ascencion   8 |
 | DEdeg | float64 | deg | Declination   9 |
 | V_RAD | float32 | km/s | Average radial velocity  10 |
 | E_V_RAD | float32 | km/s | Standard error in radial velocity measurements 11 |
 | STD_V_RAD | float32 | km/s | 1-sigma radial velocity scatter  12 |
 | PMRA | float32 | mas/yr | Proper motion in RA  13 |
 | E_PMRA | float32 | mas/yr | Standard error of proper motion in RA  14 |
 | PMDE | float32 | mas/yr | Proper motion in declination 15 |
 | E_PMDE | float32 | mas/yr | Standard error of proper motion in declination  16 |
 | FeH_ASPCAP | float64 | dex | [Fe/H] from the ASPCAP pipeline  17
 |
 | E_FeH_ASPCAP | float64 | dex | 1-sigma [Fe/H] dispersion  18 |
 | CG_Prob | float64 | --- | Membership probability from Cantat-Gaudin et. al 2020  19 |
 | RV_Prob | float64 | --- | OCCAM RV membership probability  20 |
 | FeH_Prob_ASPCAP | float64 | --- | OCCAM ASPCAP [Fe/H] membership probability 21 |
 | EH_Prob | float64 | --- | Membership probability from Hunt & Reffert 2023 22 |
 | XMatch | uint8 | --- | An unsigned integer to indicate whether a individual star has been observed by Galah, GaiaESO or OCCASO. The first bit corresponds to Galah, second to GaiaESO, and the thrid to OCCASO.  23 |



---
## Notes
None

---
## Regrets
I  have no regrets!