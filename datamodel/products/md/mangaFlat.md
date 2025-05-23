# Data Model: mangaFlat


The extracted flatfield frame


## Contents
- [Basic Information](#basic-information)
- [Changelog](#changelog)
- [Example HDUS List](#example-hdus-list)
- [Notes](#notes)
- [Regrets](#regrets)
---

## Basic Information
This FITS file contains the reduce flat frames. The headers record the status of the telescope when the exposure is taken, and the software version that used to reduce this frame.

### Naming Convention
mgFlat-[camera]-[exposure].fits.gz, where [camera] is one of the four cameras on the instrument, b1, r1, or b2, r2, for the blue and red cameras on each SDSS spectrograph. [exposure] is the (zero-padded) 8-digit exposure number.

### Releases
DR13, DR14, DR15, DR16, DR17

### Enviroments
MANGA_SPECTRO_REDUX

### Approximate Size
14 MB

### File Type
FITS

### Generated by Product
mangadrp - mdrp_calib.pro

### Is a VAC
False

### Data Level
1.1.3

### HDUS List for release DR17
  - [HDU0: PRIMARY](#hdu0-primary)
  - [HDU1: FLUX](#hdu1-flux)
  - [HDU2: TSET](#hdu2-tset)
  - [HDU3: MASK](#hdu3-mask)
  - [HDU4: WIDTH](#hdu4-width)
  - [HDU5: SUPERFLATSET](#hdu5-superflatset)

---

## Changelog
Describes changes to the datamodel product and/or file structure from one release to another
 - DR17
   - from: DR16
   - note: No changes
 - DR16
   - from: DR15
   - note: No changes
 - DR15
   - from: DR14
   - note: No changes
 - DR14
   - from: DR13
   - note: No changes

---
## Example HDUS List

### HDU0: PRIMARY
primary header extension

#### HDU Type: IMAGE
#### HDU Size:  0 bytes

##### Header Table Caption for HDU0
Key | Value | Comment | |
| --- | --- | --- | --- |
| SIMPLE | True | Primary Header created by MWRFITS v1.11 |
| BITPIX | 8 |  |
| NAXIS | 0 |  |
| EXTEND | True |  |
| TELESCOP | SDSS 2.5-M | Sloan Digital Sky Survey |
| FILENAME | sdR-b1-00198579.fit |  |
| CAMERAS | b1 |  |
| EXPOSURE | 198579 |  |
| V_BOSS | v3_6 | Active version of the BOSS ICC |
| CAMDAQ | 1.5.0:38 |  |
| SUBFRAME |  | the subframe readout command |
| ERRCNT | NONE |  |
| SYNCERR | NONE |  |
| SLINES | NONE |  |
| PIXERR | NONE |  |
| PLINES | NONE |  |
| PFERR | NONE |  |
| DIDFLUSH | True | CCD was flushed before integration |
| FLAVOR | flat | exposure type, SDSS spectro style |
| MJD | 57132 | APO fMJD day at start of exposure |
| TAI-BEG | 4936241718.0 | MJD(TAI) seconds at start of integration |
| DATE-OBS | 2015-04-20T10:15:18 | TAI date at start of integration |
| V_GUIDER | v3_1 | version of the current guiderActor |
| V_SOP | v3_1 | version of the current sopActor |
| NAME | 8485-57132-01 | The name of the currently loaded plate |
| PLATEID | 8485 | The currently loaded plate |
| CARTID | 3 | The currently loaded cartridge |
| MAPID | 1 | The mapping version of the loaded plate |
| POINTING | A | The currently specified pointing |
| PLATETYP | APOGEE-2&MaNGA | Type of plate (e.g. BOSS, MANGA, APOGEE, APOGEE |
| SRVYMODE | MaNGA dither | Survey leading this observation and its mode |
| OBJSYS | ICRS | The TCC objSys |
| RA | 234.067561 | RA of telescope boresight (deg) |
| DEC | 48.589408 | Dec of telescope boresight (deg) |
| RADEG | 234.0643 | RA of telescope pointing(deg) |
| DECDEG | 48.5899 | Dec of telescope pointing (deg) |
| SPA | -125.7251068736687 | TCC SpiderInstAng |
| ROTPOS | 0.0 | Rotator request position (deg) |
| BOREOFFX | 0.0 | TCC Boresight offset, deg |
| BOREOFFY | 0.0 | TCC Boresight offset, deg |
| ARCOFFX | 0.002157 | TCC ObjArcOff, deg |
| ARCOFFY | -0.000492 | TCC ObjArcOff, deg |
| CALOFFX | 0.0 | TCC CalibOff, deg |
| CALOFFY | 0.0 | TCC CalibOff, deg |
| CALOFFR | 0.0 | TCC CalibOff, deg |
| GUIDOFFX | 0.0 | TCC GuideOff, deg |
| GUIDOFFY | 0.0 | TCC GuideOff, deg |
| GUIDOFFR | 0.034657 | TCC GuideOff, deg |
| AZ | 219.625142 | Azimuth axis pos. (approx, deg) |
| ALT | 67.301945 | Altitude axis pos. (approx, deg) |
| IPA | 54.018248 | Rotator axis pos. (approx, deg) |
| FOCUS | 417.3336 | User-specified focus offset (um) |
| M2PISTON | 208.02 | TCC SecOrient |
| M2XTILT | -3.81 | TCC SecOrient |
| M2YTILT | 0.01 | TCC SecOrient |
| M2XTRAN | 0.01 | TCC SecOrient |
| M2YTRAN | -171.8 | TCC SecOrient |
| M2ZROT | -0.05 | TCC SecOrient |
| M1PISTON | -1624.62 | TCC PrimOrient |
| M1XTILT | -0.0 | TCC PrimOrient |
| M1YTILT | -0.0 | TCC PrimOrient |
| M1XTRAN | 650.72 | TCC PrimOrient |
| M1YTRAN | 936.55 | TCC PrimOrient |
| M1ZROT | -0.0 | TCC PrimOrient |
| SCALE | 1.000165 | User-specified scale factor |
| V_APO | trunk+svn158476 | version of the current apoActor |
| PRESSURE | 21.402 | pressure: Barometric pressure |
| WINDD | 261.0 | windd: Average wind direction |
| WINDS | 8.1 | winds: Average wind speed |
| GUSTD | 227.0 | gustd: Average gust direction |
| GUSTS | 8.6 | gusts: Average gust speed |
| AIRTEMP | 4.5 | airTempPT: PT air temperature |
| DEWPOINT | -4.4 | dpTempPT: PT dewpoint temperature |
| TRUSTEMP | 2.7 | truss25m: 25m median truss temperature |
| HUMIDITY | 46.5 | humidity: Site humidity |
| DUSTA | 21399.0 | dusta: PT outside dust density, 0.3 microns |
| DUSTB | 976.0 | dustb: PT outside dust density, 1.0 micron |
| WINDD25M | 332.5 | windd25m: 25m wind direction |
| WINDS25M | 7.7 | winds25m: 25m wind speed |
| FF | 1 1 1 1 | FF lamps 1:on 0:0ff |
| NE | 0 0 0 0 | NE lamps 1:on 0:0ff |
| HGCD | 0 0 0 0 | HGCD lamps 1:on 0:0ff |
| FFS | 1 1 1 1 1 1 1 1 | Flatfield Screen 1:closed 0:open |
| MGDPOS | C | MaNGA dither position (C,N,S,E) |
| MGDRA | 0.0 | MaNGA decenter in RA, redundant with MGDPOS |
| MGDDEC | 0.0 | MaNGA decenter in Dec, redundant with MGDPOS |
| GUIDER1 | proc-gimg-0364.fits.gz | The first guider image |
| SLITID1 | 3 | Normalized slithead ID. sp1&2 should match. |
| SLITID2 | 3 | Normalized slithead ID. sp1&2 should match. |
| GUIDERN | proc-gimg-0364.fits.gz | The last guider image |
| COLLA | 3880 | The position of the A collimator motor |
| COLLB | 3980 | The position of the B collimator motor |
| COLLC | 3931 | The position of the C collimator motor |
| HARTMANN | Out | Hartmanns: Left,Right,Out |
| MC1HUMHT | 15.7 | sp1 mech Hartmann humidity, % |
| MC1HUMCO | 16.3 | sp1 mech Central optics humidity, % |
| MC1TEMDN | 5.5 | sp1 mech Median temp, C |
| MC1THT | 5.5 | sp1 mech Hartmann Top Temp, C |
| MC1TRCB | 5.3 | sp1 mech Red Cam Bottom Temp, C |
| MC1TRCT | 6.0 | sp1 mech Red Cam Top Temp, C |
| MC1TBCB | 5.3 | sp1 mech Blue Cam Bottom Temp, C |
| MC1TBCT | 5.5 | sp1 mech Blue Cam Top Temp, C |
| REQTIME | 30.0 | requested exposure time |
| EXPTIME | 30.11 | measured exposure time, s |
| SHOPETIM | 0.76 | open shutter transit time, s |
| SHCLOTIM | 0.57 | close shutter transit time, s |
| DARKTIME | 42.23271203041077 | time between flush end and readout start |
| LN2TEMP | 90.625 |  |
| CCDTEMP | -99.609 |  |
| IONPUMP | -6.65 |  |
| CAMROW | 0 |  |
| CAMCOL | 1 |  |
| AUTHOR | Brian Cherinka & David Law <bcherin1@jhu.edu, dlaw@stsci.edu> |  |
| VERSDRP2 | v1_5_4 | MaNGA DRP Version (2d processing) |
| VERSPLDS | v2_52 | Platedesign Version |
| VERSFLAT | v1_26 | Specflat Version |
| VERSCORE | v1_2_3 | MaNGAcore Version |
| VERSPRIM | v2_1 | MaNGA Preimaging Version |
| VERSUTIL | v5_5_23 | Version of idlutils |
| VERSIDL | x86_64 linux unix linux 7.1.1 Aug 21 2009 64 64 | Version of IDL |
| TWOPHASE | False |  |
| QUALITY | excellent |  |
| RDNOISE0 | 2.04621 | CCD read noise amp 0 [electrons] |
| RDNOISE1 | 1.98163 | CCD read noise amp 1 [electrons] |
| RDNOISE2 | 1.92539 | CCD read noise amp 2 [electrons] |
| RDNOISE3 | 1.8847 | CCD read noise amp 3 [electrons] |
| PIXFLAT | pixflatave-55056-b1.fits.gz |  |
| BADPIXEL | badpixels-56149-b1.fits.gz |  |
| DRP2QUAL | 513 | DRP-2d quality bitmask |
| NBRIGHT | 0 | Number of bright pixels (>10^5) in extracted fla |
| CHECKSUM | Af4BCc39Ac3AAc37 | HDU checksum created 2016-03-11T20:50:58 |



### HDU1: FLUX
Flat field vectors to remove relative flat-field variations as function of wavelength

#### HDU Type: IMAGE
#### HDU Size:  11 MB

##### Header Table Caption for HDU1
Key | Value | Comment | |
| --- | --- | --- | --- |
| XTENSION | IMAGE | IMAGE extension |
| BITPIX | -32 | Number of bits per data pixel |
| NAXIS | 2 | Number of data axes |
| NAXIS1 | 4112 |  |
| NAXIS2 | 709 |  |
| PCOUNT | 0 | No Group Parameters |
| GCOUNT | 1 | One Data Group |
| EXTNAME | FLUX |  |
| DATASUM | 1443432083 | data unit checksum created 2016-03-11T20:50:58 |
| CHECKSUM | 9ADFA49D2ACD939D | HDU checksum created 2016-03-11T20:50:58 |



### HDU2: TSET
Legendre polynomial traceset containing the x,y centers of the fiber traces

#### HDU Type: BINARY TABLE
#### HDU Size:  38 KB

##### Header Table Caption for HDU2
Key | Value | Comment | |
| --- | --- | --- | --- |
| XTENSION | BINTABLE | Written by IDL:  Fri Mar 11 13:50:57 2016 |
| BITPIX | 8 |  |
| NAXIS | 2 | Binary table |
| NAXIS1 | 39728 | Number of bytes per row |
| NAXIS2 | 1 | Number of rows |
| PCOUNT | 0 | Random parameter count |
| GCOUNT | 1 | Group count |
| TFIELDS | 4 | Number of columns |
| COMMENT |  |  |
| COMMENT |  *** End of mandatory fields *** |  |
| COMMENT |  |  |
| EXTNAME | TSET |  |
| COMMENT |  |  |
| COMMENT |  *** Column names *** |  |
| COMMENT |  |  |
| COMMENT |  |  |
| COMMENT |  *** Column formats *** |  |
| COMMENT |  |  |
| COMMENT |  |  |
| COMMENT |  *** Column dimensions (2 D or greater) *** |  |
| COMMENT |  |  |
| TDIM4 | ( 7, 709) |  |

##### Binary Table Caption for HDU2
Name | Type | Unit | Description |
| --- | --- | --- | --- |
 | FUNC | char[8] |  | function used to fit the Y-pixel positions on the CCD and corresponding X-centers are fitted to a functional form. Polynomial, Chebyshev, Legendre or Chebyshev_split functions are used. Default value is taken as Legendre function |
 | XMIN | float64 | minimum value of the independent variable used by fitting function. |  |
 | XMAX | float64 |  | maximum value of the independent variable which is used along with the fitting coefficients, in the fitting function to get the value of dependent variable, which is the X-center of fibers. |
 | COEFF | float64[4963] |  | fit coefficents |



### HDU3: MASK
Fiber bit mask

#### HDU Type: IMAGE
#### HDU Size:  709 bytes

##### Header Table Caption for HDU3
Key | Value | Comment | |
| --- | --- | --- | --- |
| XTENSION | IMAGE | IMAGE extension |
| BITPIX | 8 | Number of bits per data pixel |
| NAXIS | 1 | Number of data axes |
| NAXIS1 | 709 |  |
| PCOUNT | 0 | No Group Parameters |
| GCOUNT | 1 | One Data Group |
| EXTNAME | MASK |  |
| DATASUM | 50727936 | data unit checksum created 2016-03-11T20:50:58 |
| CHECKSUM | 4EQY69PX4CPX49PX | HDU checksum created 2016-03-11T20:50:58 |



### HDU4: WIDTH
Profile width of each fiber

#### HDU Type: IMAGE
#### HDU Size:  11 MB

##### Header Table Caption for HDU4
Key | Value | Comment | |
| --- | --- | --- | --- |
| XTENSION | IMAGE | IMAGE extension |
| BITPIX | -32 | Number of bits per data pixel |
| NAXIS | 2 | Number of data axes |
| NAXIS1 | 4112 |  |
| NAXIS2 | 709 |  |
| PCOUNT | 0 | No Group Parameters |
| GCOUNT | 1 | One Data Group |
| EXTNAME | WIDTH |  |
| DATASUM | 2907652064 | data unit checksum created 2016-03-11T20:50:58 |
| CHECKSUM | Wd26Xc26Wc26Wc26 | HDU checksum created 2016-03-11T20:50:58 |



### HDU5: SUPERFLATSET
Traceset describing superflat

#### HDU Type: BINARY TABLE
#### HDU Size:  35 KB

##### Header Table Caption for HDU5
Key | Value | Comment | |
| --- | --- | --- | --- |
| XTENSION | BINTABLE | Written by IDL:  Fri Mar 11 13:50:57 2016 |
| BITPIX | 8 |  |
| NAXIS | 2 | Binary table |
| NAXIS1 | 36722 | Number of bytes per row |
| NAXIS2 | 1 | Number of rows |
| PCOUNT | 0 | Random parameter count |
| GCOUNT | 1 | Group count |
| TFIELDS | 5 | Number of columns |
| COMMENT |  |  |
| COMMENT |  *** End of mandatory fields *** |  |
| COMMENT |  |  |
| EXTNAME | SUPERFLATSET |  |
| COMMENT |  |  |
| COMMENT |  *** Column names *** |  |
| COMMENT |  |  |
| COMMENT |  |  |
| COMMENT |  *** Column formats *** |  |
| COMMENT |  |  |

##### Binary Table Caption for HDU5
Name | Type | Unit | Description |
| --- | --- | --- | --- |
 | FULLBKPT | float32[2625] |  | The fullbkpt vector required by evaluations with bvalu |
 | BKMASK | int16[2625] |  | output mask vector |
 | NORD | int32 |  | order for spline fit |
 | COEFF | float32[2621] |  | fitting coefficients |
 | ICOEFF | float32[2621] |  | fitting coefficients |



---
## Notes
None

---
## Regrets
I  have no regrets!