# Data Model: apFlux


apFlux contains calibration data about the relative response of the system at different wavelengths.


## Contents
- [Basic Information](#basic-information)
- [Changelog](#changelog)
- [Example HDUS List](#example-hdus-list)
- [Notes](#notes)
- [Regrets](#regrets)
---

## Basic Information
apFlux contains calibration data about the relative response of the system at different wavelengths. It is derived from a combination of observations of a spectrophotometric standard and flat fields. The format is a response curve for each fiber, on a wavelength scale that corresponds to 0.5 pixel spacing.

### Naming Convention
$APOGEE_REDUX/[APRED]/cal/[INSTRUMENT]/flux/apFlux-[CHIP]-[NUM8].fits

### Releases
DR19, WORK

### Enviroments
APOGEE_REDUX

### Approximate Size
2 MB

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
| SIMPLE | True | image conforms to FITS standard |
| BITPIX | 16 | bits per data value |
| NAXIS | 0 | number of axes |
| EXTEND | True | file may contain extensions |
| INTDELAY | 0.1 | Integration Delay(S) |
| DATE-OBS | 2020-11-11T03:18:13.342 | Date at start of integration |
| TIMESYS | UTC | Time Zone of Date |
| NFRAMES | 5 | Num of SUTR/Fow reads |
| INTOFF | 10647 | Single read duration in mSec |
| EXPTIME | 53.335 | Actual Integration Time |
| FILENAME | /data-ql/data/59164/apRaw-36020029-001.fits | Fits file name root |
| IMAGETYP | DomeFlat | Object type for EXP |
| FULLX | 8192 | Camera Full Frame X DIM |
| FULLY | 2048 | Camera Full Frame X DIM |
| BEGX | 1 | IRAF 1-indexed Value |
| BEGY | 1 | IRAF 1-indexed Value |
| BINX | 1 | in pixels |
| BINY | 1 | in pixels |
| ACAMREV | UVA-Astrocam v1.2r55 | Camera Software revision |
| OBSCMNT | None | Observer comment |
| LKSHPWR | 0.0 | LS-PWR1-% |
| TDETTOP | 74.41 | T_DETPOLE_TOP in Degrees K |
| TDETBASE | 74.405 | T_DETPOLE_BASE in Degrees K |
| COLPITCH | 0.0 | Collimator Pitch(pix) |
| TTENTTOP | 83.204 | T_TENT_TOP in Degrees K |
| COLLM3 | 0.0 | Collimator M3(um) |
| TCLDPMID | 77.658 | T_CP_MIDDLE in Degrees K |
| COLLM2 | 0.0 | Collimator M2(um) |
| COLLM1 | 0.0 | Collimator M1(um) |
| TGETTER | 75.943 | T_GETTER in Degrees K |
| TTLMBRD | 295.113 | T_TempBrd in Degrees K |
| TLSOUTH | 75.983 | T_L_SOUTH in Degrees K |
| TLNORTH | 76.54 | T_L_NORTH in Degrees K |
| TLSCAM2 | 78.905 | T_LS-Camera2 in Degrees K |
| TLSCAM1 | 78.893 | T_LS-Camera1 in Degrees K |
| TLSDETC | 74.751 | T_LS-DetectorC in Degrees K |
| TLSDETB | 73.789 | T_LS-DetectorB in Degrees K |
| TPGVAC | 1.05e-06 | Pfeiffer-Vacuum in Torr |
| LN2CNTRL | 0.0 | LN2(%) |
| TCAMAFT | 77.712 | T_CAM_AFT in Degrees K |
| TCAMMID | 78.473 | T_CAM_MIDDLE in Degrees K |
| COLLYAW | 0.0 | Collimator Yaw(pix) |
| TCAMFWD | 78.474 | T_CAM_FWD in Degrees K |
| TEMPVPH | 77.838 | T_VPH in Degrees K |
| TRADSHLD | 88.437 | T_RADSHIELD_E in Degrees K |
| TCOLLIM | 78.551 | T_COLLIMATOR in Degrees K |
| TCPCORN | 79.629 | T_CP_CORNER in Degrees K |
| TCLDPHNG | 79.117 | T_CP_HANGERS in Degrees K |
| COLLPIST | 0.0 | Collimator Piston(um) |
| DITHPIX | 12.994 | Dither Position(pix) |
| RELHUM | 13.562 | RH_T(%) |
| LN2LEVEL | 91.886 | LN2_T(%) |
| MKSVAC | 9.1378e-07 | MKS-Vacuum in Torr |
| OBJECT | ObjName |  |
| FILTER1 | FILTER |  |
| ICSREV | APOGEE ICS2.0r033 |  |
| DSPFILE | UNKNOWN |  |
| TELESCOP | SDSS 2-5m |  |
| EXPTYPE | DOMEFLAT |  |
| LAMPQRTZ | False | CalBox Quartz Lamp Status |
| LAMPUNE | False | CalBox UNe Lamp Status |
| LAMPTHAR | False | CalBox ThArNe Lamp Status |
| LAMPSHTR | False | CalBox Shutter Lamp Status |
| LAMPCNTL | True | CalBox Controller Status |
| SEEING | 1.13324 | RMS seeing from guide fibers |
| FF | 0 0 0 0 | FF lamps 1:on 0:0ff |
| NE | 0 0 0 0 | NE lamps 1:on 0:0ff |
| HGCD | 0 0 0 0 | HGCD lamps 1:on 0:0ff |
| FFS | 1 1 1 1 1 1 1 1 | Flatfield Screen 1:closed 0:open |
| OBJSYS | ICRS | The TCC objSys |
| RA | 354.466379 | RA of telescope boresight (deg) |
| DEC | -0.450599 | Dec of telescope boresight (deg) |
| RADEG | 354.4629 | RA of telescope pointing(deg) |
| DECDEG | -0.4476 | Dec of telescope pointing (deg) |
| SPA | 0.3302035598793031 | TCC SpiderInstAng |
| ROTPOS | 0.0 | Rotator request position (deg) |
| BOREOFFX | 0.0 | TCC Boresight offset, deg |
| BOREOFFY | 0.0 | TCC Boresight offset, deg |
| ARCOFFX | 0.003479 | TCC ObjArcOff, deg |
| ARCOFFY | -0.002999 | TCC ObjArcOff, deg |
| CALOFFX | 0.0 | TCC CalibOff, deg |
| CALOFFY | 0.0 | TCC CalibOff, deg |
| CALOFFR | 0.0 | TCC CalibOff, deg |
| GUIDOFFX | 0.0 | TCC GuideOff, deg |
| GUIDOFFY | 0.0 | TCC GuideOff, deg |
| GUIDOFFR | 0.006488 | TCC GuideOff, deg |
| AZ | 0.616542 | Azimuth axis pos. (approx, deg) |
| ALT | 56.890156 | Altitude axis pos. (approx, deg) |
| IPA | 180.429894 | Rotator axis pos. (approx, deg) |
| FOCUS | 109.8659 | User-specified focus offset (um) |
| M2PISTON | 5282.99 | TCC SecOrient |
| M2XTILT | -10.38 | TCC SecOrient |
| M2YTILT | -4.8 | TCC SecOrient |
| M2XTRAN | 17.04 | TCC SecOrient |
| M2YTRAN | -37.28 | TCC SecOrient |
| M2ZROT | -29.93 | TCC SecOrient |
| M1PISTON | 1946.4 | TCC PrimOrient |
| M1XTILT | 69.89 | TCC PrimOrient |
| M1YTILT | 100.0 | TCC PrimOrient |
| M1XTRAN | 372.59 | TCC PrimOrient |
| M1YTRAN | 622.11 | TCC PrimOrient |
| M1ZROT | 0.24 | TCC PrimOrient |
| SCALE | 0.999803 | User-specified scale factor |
| V_GUIDER | 3.8.1 | version of the current guiderActor |
| V_SOP | 4.0.2 | version of the current sopActor |
| NAME | 15033-59158-01 | The name of the currently loaded plate |
| PLATEID | 15033 | The currently loaded plate |
| CARTID | 7 | The currently loaded cartridge |
| MAPID | 1 | The mapping version of the loaded plate |
| POINTING | A | The currently specified pointing |
| PLATETYP | BHM&MWM | Type of plate (e.g. BOSS, MANGA, APOGEE, APOGEE |
| SRVYMODE | BHM lead | Survey leading this observation and its mode |
| CHIP | a |  |
| NREAD | 5 |  |
| V_APRED | daily |  |
| HISTORY | AP3D: Wed Nov 11 22:36:20 2020 |  |
| HISTORY | AP3D: u0914350 on kp117 |  |
| HISTORY | AP3D: IDL 8.5.1 linux x86_64 |  |
| HISTORY | AP3D:  APOGEE Reduction Pipeline Version: daily |  |
| HISTORY | AP3D: Output File: |  |
| HISTORY | AP3D:  HDU1 - image (ADU) |  |
| HISTORY | AP3D:  HDU2 - error (ADU) |  |
| HISTORY | AP3D:  HDU3 - flag mask |  |
| HISTORY | AP3D:         1 - bad pixels |  |
| HISTORY | AP3D:         2 - cosmic ray |  |
| HISTORY | AP3D:         4 - saturated |  |
| HISTORY | AP3D:         8 - unfixable |  |
| HISTORY | AP3D: Global fractional variability = 0.000 |  |
| HISTORY | AP3D: BAD PIXEL MASK file="/uufs/chpc.utah.edu/common/home/sdss50/sdsswo |  |
| HISTORY | AP3D: rk/mwm/apogee/spectro/redux/daily/cal/apogee-n/bpm/apBPM-a-1564000 |  |
| HISTORY | AP3D: Dark Current Correction file="/uufs/chpc.utah.edu/common/home/sdss |  |
| HISTORY | AP3D: 50/sdsswork/mwm/apogee/spectro/redux/daily/cal/apogee-n/darkcorr/a |  |
| HISTORY | AP3D: Flat Field Correction file="/uufs/chpc.utah.edu/common/home/sdss50 |  |
| HISTORY | AP3D: /sdsswork/mwm/apogee/spectro/redux/daily/cal/apogee-n/flatcorr/apF |  |
| HISTORY | AP3D: 74267 pixels are bad |  |
| HISTORY | AP3D: 0 pixels have cosmic rays |  |
| HISTORY | AP3D: Cosmic Rays FIXED |  |
| HISTORY | AP3D: 18 pixels are saturated |  |
| HISTORY | AP3D: 18 saturated pixels FIXED |  |
| HISTORY | AP3D: 0 pixels are unfixable |  |
| HISTORY | AP3D: Fowler Sampling, Nfowler=1 |  |
| UT-MID | 2020-11-11T03:18:40.0 | Date at midpoint of exposure |
| JD-MID | 2459164.63796 | JD at midpoint of exposure |
| PSFFILE | /uufs/chpc.utah.edu/common/home/sdss50/sdsswork/mwm/apogee/spectro/r |  |
| HISTORY | AP2D: Wed Nov 11 22:48:40 2020 |  |
| HISTORY | AP2D: u0914350 on kp117 |  |
| HISTORY | AP2D: IDL 8.5.1 linux x86_64 |  |
| HISTORY | AP2D:  APOGEE Reduction Pipeline Version: daily |  |
| HISTORY | AP2D: Output File: |  |
| HISTORY | AP2D:  HDU1 - image (ADU) |  |
| HISTORY | AP2D:  HDU2 - error (ADU) |  |
| HISTORY | AP2D:  HDU3 - flag mask |  |
| HISTORY | AP2D:         0 - good pixels |  |
| HISTORY | AP2D:         1 - bad pixels |  |
| HISTORY | AP2D:  HDU4 - wavelengths (Ang) |  |
| HISTORY | AP2D:  HDU5 - wavelength coefficients |  |
| HISTORY | AP2D: Extract_type=4 - Using Empirical PSF Extraction |  |
| EXTRTYPE | 4 | Extraction type |
| OBSTYPE | FLUXCORR |  |
| HISTORY | APMKFLUXCAL: Wed Nov 11 22:49:36 2020 |  |
| HISTORY | APMKFLUXCAL: u0914350 on kp117 |  |
| HISTORY | APMKFLUXCAL: IDL 8.5.1 linux x86_64 |  |
| HISTORY | APMKFLUXCAL:  APOGEE Reduction Pipeline Version: daily |  |
| HISTORY | APMKFLUXCAL: Output File: |  |
| HISTORY | APMKFLUXCAL:  HDU1 - Relative Flux Calibration [Npix,Nfibers,3] |  |
| HISTORY | APMKFLUXCAL:  HDU2 - Throughput [Nfibers,3] |  |
| HISTORY | APMKFLUXCAL: File="/uufs/chpc.utah.edu/common/home/sdss50/sdsswork/mwm/a |  |
| HISTORY | APMKFLUXCAL: pogee/spectro/redux/daily/exposures/apogee-n/59164/36020029 |  |
| HISTORY | LAMPTYPE=DOMEFLAT |  |



### HDU1: 


#### HDU Type: IMAGE
#### HDU Size:  2 MB

##### Header Table Caption for HDU1
Key | Value | Comment | |
| --- | --- | --- | --- |
| XTENSION | IMAGE | IMAGE extension |
| BITPIX | -32 | Number of bits per data pixel |
| NAXIS | 2 | Number of data axes |
| NAXIS1 | 2048 |  |
| NAXIS2 | 300 |  |
| PCOUNT | 0 | No Group Parameters |
| GCOUNT | 1 | One Data Group |
| CTYPE1 | Pixel |  |
| CTYPE2 | Fiber |  |
| CTYPE3 | Chip |  |
| BUNIT | Relative Flux |  |



### HDU2: 


#### HDU Type: IMAGE
#### HDU Size:  1 KB

##### Header Table Caption for HDU2
Key | Value | Comment | |
| --- | --- | --- | --- |
| XTENSION | IMAGE | IMAGE extension |
| BITPIX | -32 | Number of bits per data pixel |
| NAXIS | 1 | Number of data axes |
| NAXIS1 | 300 |  |
| PCOUNT | 0 | No Group Parameters |
| GCOUNT | 1 | One Data Group |
| CTYPE1 | Fiber |  |
| CTYPE2 | Chip |  |
| BUNIT | Throughput |  |



### HDU3: 


#### HDU Type: IMAGE
#### HDU Size:  8 KB

##### Header Table Caption for HDU3
Key | Value | Comment | |
| --- | --- | --- | --- |
| XTENSION | IMAGE | IMAGE extension |
| BITPIX | -32 | Number of bits per data pixel |
| NAXIS | 1 | Number of data axes |
| NAXIS1 | 2048 |  |
| PCOUNT | 0 | No Group Parameters |
| GCOUNT | 1 | One Data Group |
| CTYPE1 | Pixel |  |
| CTYPE3 | Chip |  |
| BUNIT | Relative Flux |  |



### HDU4: 


#### HDU Type: IMAGE
#### HDU Size:  8 KB

##### Header Table Caption for HDU4
Key | Value | Comment | |
| --- | --- | --- | --- |
| XTENSION | IMAGE | IMAGE extension |
| BITPIX | -32 | Number of bits per data pixel |
| NAXIS | 1 | Number of data axes |
| NAXIS1 | 2048 |  |
| PCOUNT | 0 | No Group Parameters |
| GCOUNT | 1 | One Data Group |
| CTYPE1 | Pixel |  |
| CTYPE3 | Chip |  |
| BUNIT | Relative Flux |  |



---
## Notes
None

---
## Regrets
I have no regrets!