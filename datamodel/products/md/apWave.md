# Data Model: apWave


apWave contains calibration data relating to the wavelength calibration.


## Contents
- [Basic Information](#basic-information)
- [Changelog](#changelog)
- [Example HDUS List](#example-hdus-list)
- [Notes](#notes)
- [Regrets](#regrets)
---

## Basic Information
apWave contains calibration data relating to the wavelength calibration. For each fiber, 12 wavelength calibration coefficients relate the pixel number to the wavelength.

### Naming Convention
$APOGEE_REDUX/[APRED]/cal/[INSTRUMENT]/wave/apWave-[CHIP]-[NUM8].fits

### Releases
DR19, WORK

### Enviroments
APOGEE_REDUX

### Approximate Size
4 MB

### File Type
FITS

### Generated by Product
apogee_drp

### Is a VAC
False

### HDUS List for release WORK
  - [HDU0: PRIMARY](#hdu0-primary)
  - [HDU1](#hdu1)
  - [HDU2](#hdu2)
  - [HDU3](#hdu3)
  - [HDU4](#hdu4)
  - [HDU5](#hdu5)
  - [HDU6](#hdu6)
  - [HDU7](#hdu7)

---

## Changelog
Describes changes to the datamodel product and/or file structure from one release to another
 - WORK
   - from: DR19
   - note: No changes

---
## Example HDUS List

### HDU0: PRIMARY


#### HDU Type: IMAGE
#### HDU Size:  0 bytes

##### Header Table Caption for HDU0
Key | Value | Comment | |
| --- | --- | --- | --- |
| SIMPLE | True | conforms to FITS standard |
| BITPIX | 8 | array data type |
| NAXIS | 0 | number of array dimensions |
| EXTEND | True |  |
| NFRAMES | 1 | number of frames in fit |
| FRAME0 | 44950040 |  |
| NPOLY | 4 | polynomial order of fit |
| NGROUP | 1 | number of groups in fit |
| MEDRMS | 0.0258485337427728 | median rms |
| MEDSIG | 0.01433443261475986 | median sig |
| COMMENT | HDU#1 : wavelength calibration parameters [14,300] |  |
| COMMENT | HDU#2 : wavelength calibration array [300,2048] |  |
| COMMENT | HDU#3 : wavecal fit parameter array [npoly+3*ngroup,300] |  |
| COMMENT | HDU#4 : rms from fit [300,ngroup] |  |
| COMMENT | HDU#5 : sig from fit [300,ngroup] |  |
| COMMENT | HDU#6 : wavecal fit parameter array [npoly+3*ngroup,300] |  |
| COMMENT | HDU#7 : table with frames/group information |  |
| COMMENT | APOGEE_DRP_VER:daily |  |



### HDU1: 


#### HDU Type: IMAGE
#### HDU Size:  32 KB

##### Header Table Caption for HDU1
Key | Value | Comment | |
| --- | --- | --- | --- |
| XTENSION | IMAGE | Image extension |
| BITPIX | -64 | array data type |
| NAXIS | 2 | number of array dimensions |
| NAXIS1 | 300 |  |
| NAXIS2 | 14 |  |
| PCOUNT | 0 | number of parameters |
| GCOUNT | 1 | number of groups |



### HDU2: 


#### HDU Type: IMAGE
#### HDU Size:  4 MB

##### Header Table Caption for HDU2
Key | Value | Comment | |
| --- | --- | --- | --- |
| XTENSION | IMAGE | Image extension |
| BITPIX | -64 | array data type |
| NAXIS | 2 | number of array dimensions |
| NAXIS1 | 2048 |  |
| NAXIS2 | 300 |  |
| PCOUNT | 0 | number of parameters |
| GCOUNT | 1 | number of groups |



### HDU3: 


#### HDU Type: IMAGE
#### HDU Size:  16 KB

##### Header Table Caption for HDU3
Key | Value | Comment | |
| --- | --- | --- | --- |
| XTENSION | IMAGE | Image extension |
| BITPIX | -64 | array data type |
| NAXIS | 2 | number of array dimensions |
| NAXIS1 | 300 |  |
| NAXIS2 | 7 |  |
| PCOUNT | 0 | number of parameters |
| GCOUNT | 1 | number of groups |



### HDU4: 


#### HDU Type: IMAGE
#### HDU Size:  2 KB

##### Header Table Caption for HDU4
Key | Value | Comment | |
| --- | --- | --- | --- |
| XTENSION | IMAGE | Image extension |
| BITPIX | -64 | array data type |
| NAXIS | 2 | number of array dimensions |
| NAXIS1 | 1 |  |
| NAXIS2 | 300 |  |
| PCOUNT | 0 | number of parameters |
| GCOUNT | 1 | number of groups |



### HDU5: 


#### HDU Type: IMAGE
#### HDU Size:  2 KB

##### Header Table Caption for HDU5
Key | Value | Comment | |
| --- | --- | --- | --- |
| XTENSION | IMAGE | Image extension |
| BITPIX | -64 | array data type |
| NAXIS | 2 | number of array dimensions |
| NAXIS1 | 1 |  |
| NAXIS2 | 300 |  |
| PCOUNT | 0 | number of parameters |
| GCOUNT | 1 | number of groups |



### HDU6: 


#### HDU Type: IMAGE
#### HDU Size:  16 KB

##### Header Table Caption for HDU6
Key | Value | Comment | |
| --- | --- | --- | --- |
| XTENSION | IMAGE | Image extension |
| BITPIX | -64 | array data type |
| NAXIS | 2 | number of array dimensions |
| NAXIS1 | 300 |  |
| NAXIS2 | 7 |  |
| PCOUNT | 0 | number of parameters |
| GCOUNT | 1 | number of groups |



### HDU7: 


#### HDU Type: BINARY TABLE
#### HDU Size:  24 bytes

##### Header Table Caption for HDU7
Key | Value | Comment | |
| --- | --- | --- | --- |
| XTENSION | BINTABLE | binary table extension |
| BITPIX | 8 | array data type |
| NAXIS | 2 | number of array dimensions |
| NAXIS1 | 24 | length of dimension 1 |
| NAXIS2 | 1 | length of dimension 2 |
| PCOUNT | 0 | number of group parameters |
| GCOUNT | 1 | number of groups |
| TFIELDS | 3 | number of table fields |

##### Binary Table Caption for HDU7
Name | Type | Unit | Description |
| --- | --- | --- | --- |
 | FRAME | char[8] |  |  |
 | GROUP | int64 |  |  |
 | DITHPIX | float64 |  |  |



---
## Notes
None

---
## Regrets
I have no regrets!