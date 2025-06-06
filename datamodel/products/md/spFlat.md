# Data Model: spFlat


Extracted fiber flats, and associated data


## Contents
- [Basic Information](#basic-information)
- [Changelog](#changelog)
- [Example HDUS List](#example-hdus-list)
- [Notes](#notes)
- [Regrets](#regrets)
---

## Basic Information
This file contains information about fiberflats, X-centers of fibers, fibermask, profile width and superflat obtained from extracted flat calibration frames.

### Naming Convention
$BOSS_SPECTRO_REDUX/[RUN2D]/[FIELD]/spFlat-[BR][ID]-[FRAME].fits.gz

### Releases
DR9, DR10, DR12, DR11, DR13, DR14, DR15, DR16, DR17, DR18, IPL3, DR19

### Enviroments
BOSS_SPECTRO_REDUX

### Approximate Size
9 MB

### File Type
FITS

### Generated by Product
idlspec2d - spcalib.pro

### Is a VAC
False

### Data Level
0.0.0

### HDUS List for release DR19
  - [HDU0: fflat](#hdu0-fflat)
  - [HDU1: tset](#hdu1-tset)
  - [HDU2: fibermask](#hdu2-fibermask)
  - [HDU3: widthset](#hdu3-widthset)
  - [HDU4: superflatset](#hdu4-superflatset)
  - [HDU5: xsol](#hdu5-xsol)

---

## Changelog
Describes changes to the datamodel product and/or file structure from one release to another
 - DR19
   - from: IPL3
   - note: No changes
 - IPL3
   - from: DR18
   - added_hdus: ['xsol']
   - primary_delta_nkeys: 73
   - added_primary_header_kwargs: ['SPECMT', 'MEDWIDT2', 'B2CAMH', 'VERS2D', 'OFFDEC', 'T_OUT', 'MECHORIZ', 'ARCHTEMP', 'MEDWIDT3', 'COLLH', 'COLLT', 'EXTNAME', 'ARCHACF', 'R2CAMT', 'HA', 'T_FLOOR', 'MCHUMHT', 'T_CELL', 'FIELDID', 'SPEC', 'MECHORIX', 'INTSTART', 'CCDTYPE', 'OFFPA', 'R2CAMH', 'MCTBCB', 'T_PRIM', 'MCTEMDN', 'BOSSVER', 'DESIGNID', 'GSEEING', 'CONFID', 'ARCNAME', 'B2CAMT', 'BUFFER', 'CCD', 'AIRMASS', 'HEAR', 'CCDSUM', 'DAQVER', 'VKAIJU', 'EQUINOX', 'MEDWIDT0', 'MCHUMCO', 'PROFTYPE', 'INTEND', 'VJAEGER', 'T_IN', 'CCDID', 'ARCHBACK', 'MCTRCT', 'MCTHT', 'MEDWIDT1', 'V_ARCHON', 'VCOORDIO', 'ARCHBVER', 'VCALIBS', 'MECHORIY', 'SLITID', 'T_TRUSS', 'MCTBCT', 'OBSERVAT', 'MCTRCB', 'FLATNAME', 'OFFRA']
   - removed_primary_header_kwargs: ['AUTHOR', 'MGDPOS', 'MC1HUMCO', 'MGDRA', 'TWOPHASE', 'MC1TRCB', 'MGDDEC', 'MC1TEMDN', 'MC1HUMHT', 'MC1TRCT', 'CAMROW', 'MC1TBCB', 'MC1THT', 'CAMCOL', 'MC1TBCT', 'SLITID1']
 - DR18
   - from: DR17
   - primary_delta_nkeys: 38
   - added_primary_header_kwargs: ['M1ZROT', 'V_APO', 'MGDRA', 'GUSTD', 'PLATETYP', 'DUSTA', 'V_GUIDER', 'MC1HUMHT', 'PRESSURE', 'SHCLOTIM', 'IONPUMP', 'MC1TBCT', 'SUBFRAME', 'V_SOP', 'DUSTB', 'WINDD25M', 'MC1TRCB', 'MGDDEC', 'MC1THT', 'V_BOSS', 'DARKTIME', 'MC1HUMCO', 'GUSTS', 'CCDTEMP', 'HUMIDITY', 'MC1TEMDN', 'MC1TRCT', 'PFERR', 'SRVYMODE', 'SLITID1', 'WINDD', 'MGDPOS', 'LN2TEMP', 'AIRTEMP', 'WINDS25M', 'M2ZROT', 'DEWPOINT', 'REQTIME', 'DIDFLUSH', 'MC1TBCB', 'WINDS', 'SHOPETIM', 'TRUSTEMP']
   - removed_primary_header_kwargs: ['PIXBIAS', 'OBJOFFY', 'OBJOFFX', 'DAQVER', 'BOSSVER']
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
 - DR13
   - from: DR11
   - note: No changes
 - DR11
   - from: DR12
   - note: No changes
 - DR12
   - from: DR10
   - note: No changes
 - DR10
   - from: DR9
   - note: No changes

---
## Example HDUS List

### HDU0: fflat
The primary HDU data is an array of flat-field vectors for each fiber that removes relative flat-field variations as a function of wavelength between fibers. These are referred as fiberflats.

#### HDU Type: IMAGE
#### HDU Size:  7 MB

##### Header Table Caption for HDU0
Key | Value | Comment | |
| --- | --- | --- | --- |
| SIMPLE | True | Written by IDL:  Wed Apr  3 01:53:45 2024 |
| BITPIX | -32 | Number of bits per data pixel |
| NAXIS | 2 | Number of data axes |
| NAXIS1 | 4112 |  |
| NAXIS2 | 500 |  |
| EXTEND | True |  |
|  |  |  |
|  | INSTRUMENT INFO |  |
| TELESCOP | SDSS 2.5-M | Telescope |
| OBSERVAT | APO | Observatory |
| SPEC |  | Spectrograph name |
| CAMERAS | b1 | BOSS CAMERA |
| CCD |  | CCD name |
| CCDID |  | Unique identifier of the CCD |
| CCDTYPE |  | CCD type |
|  |  |  |
|  | EXPOSURE INFO |  |
| FILENAME | sdR-b1-00353044.fit | File basename |
| EXPOSURE | 353044 | Exposure number |
| FLAVOR | flat | exposure type, SDSS spectro style |
| QUALITY | excellent | Exposure Quality |
| MJD | 60000 | Modified Julian Date at start of exposure |
| TAI-BEG | 5184019362.0 | MJD(TAI) seconds at start of integration |
| DATE-OBS | 2023-02-25T05:22:42 | TAI date at start of integration |
| INTSTART |  | Start of the integration |
| INTEND |  | End of the integration |
| REQTIME | 25.0 | requested exposure time |
| EXPTIME | 25.08 | requested exposure time |
| DARKTIME | 46.6504614353 | time between flush end and readout start |
| SHOPETIM | 0.74 | open shutter transit time (s) |
| SHCLOTIM | 0.57 | close shutter transit time (s) |
| GUIDER1 |  | The first guider image for plates |
| GUIDERN |  | The last guider image for plates |
|  |  |  |
|  | EXPOSURE SETTINGS |  |
| DIDFLUSH | True | CCD was flushed before integration |
| SUBFRAME |  | the subframe readout command |
| CCDSUM |  | Horizontal and vertical binning |
| ARCHACF |  | Archon ACF file loaded |
| BUFFER |  | The buffer number read |
| ERRCNT | NONE | BOSSDAQ Error Count |
| SYNCERR | NONE | BOSSDAQ Sync Error Count |
| SLINES | NONE | BOSSDAQ Sync Error Lines |
| PIXERR | NONE | BOSSDAQ Pixel Error Count |
| PLINES | NONE | Pixel Error Lines |
| PFERR | NONE | Pixel Frame Error |
|  |  |  |
|  | FIELD/PLATE INFO |  |
| NAME |  | The name of the currently loaded plate |
| PLATEID |  | The currently loaded plate |
| CARTID | FPS-N | The currently loaded cartridge/instrument |
| MAPID |  | The mapping version of the loaded plate |
| POINTING |  | The currently specified pointing |
| PLATETYP | BHM&MWM | Type of plate (e.g. BOSS, MANGA, APOGEE, APOGEE) |
| SRVYMODE |  | Survey leading this observation and its mode |
| CONFID | 8872 | FPS configuration |
| DESIGNID | 108452 | FPS design |
| FIELDID | 112360 | FPS field |
| SLITID | 0 | spectrograph Normalized slithead ID. |
|  |  |  |
|  | TELESCOPE INFO |  |
| RA | 150.013708 | RA of telescope boresight (deg) |
| DEC | 2.183954 | Dec of telescope boresight (deg) |
| RADEG | 150.01675 | RA of telescope pointing(deg) |
| DECDEG | 2.18325 | Dec of telescope pointing (deg) |
| EQUINOX |  | Equinox of celestial coordinate system |
| OFFRA | 0.0 | Absolute guider offset in RA |
| OFFDEC | -0.1 | Absolute guider offset in DEC |
| OFFPA | -432.0 | Absolute guider offset in PA |
| GSEEING | 1.16 | Seeing from the guider (arcsec) |
| AIRMASS |  | AIRMASS |
| HA |  | HA axis pos. (approx, deg) |
| SPA | 43.758573 | TCC SpiderInstAng |
| ROTPOS | 13.5 | Rotator request position (deg) |
| AZ | 36.737714 | Azimuth axis pos. (approx, deg) |
| ALT | 53.665387 | Altitude axis pos. (approx, deg) |
| IPA | 223.555133 | Rotator axis pos. (approx, deg) |
| FOCUS | 205.0 | User-specified focus offset (um) |
| SCALE | 1.0 | User-specified scale factor |
| OBJSYS | ICRS | The TCC objSys |
| BOREOFFX | 0.0 | TCC Boresight offset (deg) |
| BOREOFFY | 0.0 | TCC Boresight offset (deg) |
| ARCOFFX | -0.00304 | TCC ObjArcOff (deg) |
| ARCOFFY | 0.000704 | TCC ObjArcOff (deg) |
| CALOFFX | 0.0 | TCC CalibOff (deg) |
| CALOFFY | 0.0 | TCC CalibOff (deg) |
| CALOFFR | 0.0 | TCC CalibOff (deg) |
| GUIDOFFX | 0.0 | TCC GuideOff (deg) |
| GUIDOFFY | 0.0 | TCC GuideOff (deg) |
| GUIDOFFR | 0.153533 | TCC GuideOff (deg) |
| M2PISTON | 3974.65 | TCC SecOrient |
| M2XTILT | 0.01 | TCC SecOrient |
| M2YTILT | -0.03 | TCC SecOrient |
| M2XTRAN | -0.02 | TCC SecOrient |
| M2YTRAN | -61.29 | TCC SecOrient |
| M2ZROT | -11.13 | TCC SecOrient |
| M1PISTON | 1.07 | TCC PrimOrient |
| M1XTILT | -59.51 | TCC PrimOrient |
| M1YTILT | -9.21 | TCC PrimOrient |
| M1XTRAN | -512.13 | TCC PrimOrient |
| M1YTRAN | 1906.31 | TCC PrimOrient |
| M1ZROT | 0.03 | TCC PrimOrient |
|  |  |  |
|  | SPECTROGRAPH STATUS |  |
| MECHORIX |  | Orientation in X axis (cm/s2) |
| MECHORIY |  | Orientation in Y axis (cm/s2) |
| MECHORIZ |  | Orientation in Z axis (cm/s2) |
| MCHUMHT | 2.9 | spec mech Hartmann humidity (%) |
| MCHUMCO | 2.5 | spec mech Central optics humidity (%) |
| MCTEMDN | 3.1 | spec mech Median temp (deg C) |
| MCTHT | 3.1 | spec mech Hartmann Top Temp (deg C) |
| MCTRCB | 3.1 | spec mech Red Cam Bottom Temp (deg C) |
| MCTRCT | 3.4 | spec mech Red Cam Top Temp (deg C) |
| MCTBCB | 3.1 | spec mech Blue Cam Bottom Temp (deg C) |
| MCTBCT | 3.1 | spec mech Blue Cam Top Temp (deg C) |
| B2CAMT |  | B2 camera temperature (deg C) |
| B2CAMH |  | B2 camera RH (%) |
| R2CAMT |  | R2 camera temperature (deg C) |
| R2CAMH |  | R2 camera RH (%) |
| COLLT |  | Collimator temperature (deg C) |
| COLLH |  | Collimator RH (%) |
| SPECMT |  | specMech temperature (deg C) |
| ARCHTEMP |  | Archon backplane temperature (deg C) |
| LN2TEMP | 94.922 | LN2 can temperature |
| CCDTEMP | -99.609 | Temperature of the sensor |
| IONPUMP | -7.76 | log10(Ion_Pump_pressure/torr) |
| COLLA | 3489 | The position of the A collimator motor |
| COLLB | 3487 | The position of the B collimator motor |
| COLLC | 3507 | The position of the C collimator motor |
|  |  |  |
|  | VERSIONS |  |
| VJAEGER | 1.3.4a0 | Version of Jaeger |
| VKAIJU | 1.2.4-alpha.0 | Version of Kaiju |
| VCOORDIO | 1.6.2a0 | Version of coordIO |
| VCALIBS | 2023.01.05 | Version of FPS calibrations |
| V_APO | 3.0.1 | Version of the current apoActor |
| V_BOSS | 6.0.2-alpha.0 | Active version of the BOSS ICC |
| V_ARCHON |  | Active version of the BOSS ARCHON Controller |
| ARCHBACK |  | Archon backplane ID |
| ARCHBVER |  | Archon backplane version |
| V_GUIDER |  | version of the current guiderActor |
| V_SOP |  | version of the current sopActor |
| DAQVER |  | BOSS Data Acquisition Version |
| CAMDAQ | 1.5.0:37 | Camera Data Acquisition Version |
| BOSSVER |  | ICC version |
| VERSIDL | 8.8.0 | Version of IDL |
| VERSUTIL | 6.0.0dev | Version of idlutils |
| VERSREAD | v6_1_3 | Version of idlspec2d for pre-processing raw data |
| VERSLOG | trunk 27531 | Version of SPECLOG product |
| VERSFLAT | v1_35 | SPECFLAT version |
| VERS2D |  | Version of idlspec2d for 2D reduction |
|  |  |  |
|  | APO WEATHER |  |
| PRESSURE | 21.546 | APO SDSS 2.5m Air Pressure (inch Hg) |
| WINDD | 191.3 | APO SDSS 2.5m Wind Direction (deg) |
| WINDS | 14.0 | APO SDSS 2.5m Wind Speed (mph) |
| GUSTD | 212.6 | APO SDSS 2.5m Wind Gust Direction (deg) |
| GUSTS | 22.0 | APO SDSS 2.5m Wind Gust Speed (mph) |
| AIRTEMP | 0.0 | APO SDSS 2.5m Outside temperature (deg C) |
| DEWPOINT | 0.0 | APO SDSS 2.5m Dewpoint (deg C) |
| TRUSTEMP | 2.9 | APO SDSS 2.5m Truss Temperature (deg C) |
| HUMIDITY | NaN | APO SDSS 2.5m Humidity (percent) |
| DUSTA | 14147.0 | APO SDSS 2.5m dust (count of 0.3mu/particles/vol |
| DUSTB | 1431.0 | APO SDSS 2.5m dust (count of 1mu/particles/vol/t |
| WINDD25M | -999.0 | Wind Direction at APO SDSS 2.5m (deg) |
| WINDS25M | -999.0 | Wind Speed at APO SDSS 2.5m (deg) |
|  |  |  |
|  | LCO WEATHER |  |
| T_OUT |  | LCO du Pont Outside temperature (deg C) |
| T_IN |  | LCO du Pont Inside temperature (deg C) |
| T_PRIM |  | LCO du Pont Primary mirror temperature (deg C) |
| T_CELL |  | LCO du Pont Cell temperature (deg C) |
| T_FLOOR |  | LCO du Pont Floor temperature (deg C) |
| T_TRUSS |  | LCO du Pont Truss temperature (deg C) |
|  |  |  |
|  | CALIBRATION SETTINGS |  |
| NE | 0 0 0 0 | Ne Arc lamps 1:on 0:off |
| HGCD | 0 0 0 0 | HgCd Arc lamps 1:on 0:off |
| HEAR | 0 0 0 0 | HeAr Arc lamps 1:On 0:off |
| FF | 1 1 1 1 | Flat Field lamps 1:on 0:off |
| FFS | 1 1 1 1 1 1 1 1 | Flatfield Screen 1:closed 0:open |
| HARTMANN | Out | Hartmanns: Left,Right,Out,Closed |
|  |  |  |
|  | REDUCTION |  |
| RDNOISE0 | 2.06291 | CCD read noise amp 0 [electrons] |
| RDNOISE1 | 1.95168 | CCD read noise amp 1 [electrons] |
| RDNOISE2 | 1.89922 | CCD read noise amp 2 [electrons] |
| RDNOISE3 | 2.01212 | CCD read noise amp 3 [electrons] |
| PIXFLAT | pixflatave-59768-b1.fits.gz | Name of Pixel Flat used |
| BADPIXEL | badpixels-59747-b1.fits.gz | Name of Badpixel mask used |
|  |  |  |
|  | PIPELINE OUTPUTS |  |
| NBRIGHT | 0 | Number of bright pixels (>10^5) in extracted fla |
| FLATNAME | sdR-b1-00353044.fit | Name of flat |
| ARCNAME | sdR-b1-00353047.fit | Name of associated arc |
| PROFTYPE | 1 | Extract Profile (1:guass 2:ExpCubic 3:DoubleGaus |
| MEDWIDT0 | 0.970656 | Median spatial dispersion widths in LL quadrant |
| MEDWIDT1 | 1.0265 | Median spatial dispersion widths in LR quadrant |
| MEDWIDT2 | 1.03808 | Median spatial dispersion widths in UL quadrant |
| MEDWIDT3 | 1.06889 | Median spatial dispersion widths in UR quadrant |
| EXTNAME | fflat |  |



### HDU1: tset
The HDU 1 data is a binary table whose fields are used to calculate the X-centers, for all fibers in the flat-field calibration frames. The Y-pixel positions on the CCD, which is the independent variable and the corresponding X-centers, which is the dependent variable are fitted to a functional form and the resulting coefficients are stored in the binary table.

#### HDU Type: BINARY TABLE
#### HDU Size:  27 KB

##### Header Table Caption for HDU1
Key | Value | Comment | |
| --- | --- | --- | --- |
| XTENSION | BINTABLE | Binary table written by MWRFITS v1.13 |
| BITPIX | 8 | Required value |
| NAXIS | 2 | Required value |
| NAXIS1 | 28024 | Number of bytes per row |
| NAXIS2 | 1 | Number of rows |
| PCOUNT | 0 | Normally 0 (no varying arrays) |
| GCOUNT | 1 | Required value |
| TFIELDS | 4 | Number of columns in table |
| COMMENT |  |  |
| COMMENT |  *** End of mandatory fields *** |  |
| COMMENT |  |  |
| EXTNAME | tset |  |
| COMMENT |  |  |
| COMMENT |  *** Column formats *** |  |
| COMMENT |  |  |
| COMMENT |  |  |
| COMMENT |  *** Column dimensions (2 D or greater) *** |  |
| COMMENT |  |  |
| TDIM4 | ( 7, 500) |  |
| COMMENT |  |  |
| COMMENT |  *** Column names *** |  |
| COMMENT |  |  |

##### Binary Table Caption for HDU1
Name | Type | Unit | Description |
| --- | --- | --- | --- |
 | FUNC | char[8] |  | function used to fit the Y-pixel positions on the CCD and corresponding X-centers are fitted to a functional form. Polynomial, Chebyshev, Legendre or Chebyshev_split functions are used. Default value is taken as Legendre function |
 | XMIN | float64 |  | minimum value of the independent variable which is used along with the fitting coefficients, in the fitting function to get the value of dependent variable, which is the X-center of fibers. |
 | XMAX | float64 |  | maximum value of the independent variable used by fitting function. |
 | COEFF | float64[3500] |  | fit coefficients |



### HDU2: fibermask
The HDU 2 data stores the fibermask. These are fiber status bits and are set to non-zero to indicate bad status. The status bits used for masking are documented in $IDLUTILS/$IDLUTILS_VER/data/sdss/sdssMaskbits.par.

#### HDU Type: IMAGE
#### HDU Size:  3 KB

##### Header Table Caption for HDU2
Key | Value | Comment | |
| --- | --- | --- | --- |
| XTENSION | IMAGE | Binary table written by MWRFITS v1.13 |
| BITPIX | 64 | Required value |
| NAXIS | 1 | Required value |
| NAXIS1 | 500 | Number of bytes per row |
| NAXIS2 | 1 | Number of rows |
| PCOUNT | 0 | Normally 0 (no varying arrays) |
| GCOUNT | 1 | Required value |
| TFIELDS | 4 | Number of columns in table |
| COMMENT |  |  |
| COMMENT |  *** End of mandatory fields *** |  |
| COMMENT |  |  |
| EXTNAME | fibermask |  |
| COMMENT |  |  |
| COMMENT |  *** Column formats *** |  |
| COMMENT |  |  |
| COMMENT |  |  |
| COMMENT |  *** Column dimensions (2 D or greater) *** |  |
| COMMENT |  |  |
| TDIM4 | ( 7, 500) |  |
| COMMENT |  |  |
| COMMENT |  *** Column names *** |  |
| COMMENT |  |  |



### HDU3: widthset
The data attribute of HDU 3 gives the first-order corrected profile width for each fiber bundle. This Gaussian sigma is in units of pixels. The X-positions on the CCD and their corresponding profile width are fitted to a functional form and the resulting coefficients are stored in a binary table. The X-position is the independent variable and the width is the dependent variable for the fitting function.

#### HDU Type: BINARY TABLE
#### HDU Size:  11 KB

##### Header Table Caption for HDU3
Key | Value | Comment | |
| --- | --- | --- | --- |
| XTENSION | BINTABLE | Binary table written by MWRFITS v1.13 |
| BITPIX | 8 | Required value |
| NAXIS | 2 | Required value |
| NAXIS1 | 12024 | Number of bytes per row |
| NAXIS2 | 1 | Number of rows |
| PCOUNT | 0 | Normally 0 (no varying arrays) |
| GCOUNT | 1 | Required value |
| TFIELDS | 4 | Number of columns in table |
| COMMENT |  |  |
| COMMENT |  *** End of mandatory fields *** |  |
| COMMENT |  |  |
| COMMENT |  |  |
| COMMENT |  *** End of mandatory fields *** |  |
| COMMENT |  |  |
| EXTNAME | widthset |  |
| COMMENT |  |  |
| COMMENT |  *** Column formats *** |  |
| COMMENT |  |  |
| COMMENT |  |  |
| COMMENT |  *** Column formats *** |  |
| COMMENT |  |  |
| COMMENT |  |  |
| COMMENT |  *** Column dimensions (2 D or greater) *** |  |
| COMMENT |  |  |
| COMMENT |  |  |
| COMMENT |  *** Column dimensions (2 D or greater) *** |  |
| COMMENT |  |  |
| TDIM4 | ( 3, 500) |  |
| COMMENT |  |  |
| COMMENT |  *** Column names *** |  |
| COMMENT |  |  |
| COMMENT |  |  |
| COMMENT |  *** Column names *** |  |
| COMMENT |  |  |

##### Binary Table Caption for HDU3
Name | Type | Unit | Description |
| --- | --- | --- | --- |
 | FUNC | char[8] |  | function used to fit the X-positions on CCD and the correspoding profile widths to a functional form. Polynomial, Chebyshev, Legendre or Chebyshev_split functions are used. Default value is taken as Legendre function. |
 | XMIN | float64 |  | minimum value of the independent variable which is used along with the fitting coefficients, in the fitting function to get the value of dependent variable, which is the profile width of fibers. |
 | XMAX | float64 |  | maximum value of the independent variable used by fitting function. |
 | COEFF | float64[1500] |  | fit coefficients |



### HDU4: superflatset
The data attribute of HDU 4 contains superflat which is constructed from extracted flat-field image and is stored in a bspline set structure form. A superflat is a bspline average across all fibers of the flat spectrum in raw counts as a function of wavelength.

#### HDU Type: BINARY TABLE
#### HDU Size:  24 KB

##### Header Table Caption for HDU4
Key | Value | Comment | |
| --- | --- | --- | --- |
| XTENSION | BINTABLE | Binary table written by MWRFITS v1.13 |
| BITPIX | 8 | Required value |
| NAXIS | 2 | Required value |
| NAXIS1 | 25396 | Number of bytes per row |
| NAXIS2 | 1 | Number of rows |
| PCOUNT | 0 | Normally 0 (no varying arrays) |
| GCOUNT | 1 | Required value |
| TFIELDS | 5 | Number of columns in table |
| COMMENT |  |  |
| COMMENT |  *** End of mandatory fields *** |  |
| COMMENT |  |  |
| COMMENT |  |  |
| COMMENT |  *** End of mandatory fields *** |  |
| COMMENT |  |  |
| COMMENT |  |  |
| COMMENT |  *** End of mandatory fields *** |  |
| COMMENT |  |  |
| EXTNAME | superflatset |  |
| COMMENT |  |  |
| COMMENT |  *** Column formats *** |  |
| COMMENT |  |  |
| COMMENT |  |  |
| COMMENT |  *** Column formats *** |  |
| COMMENT |  |  |
| COMMENT |  |  |
| COMMENT |  *** Column formats *** |  |
| COMMENT |  |  |
| COMMENT |  |  |
| COMMENT |  *** Column dimensions (2 D or greater) *** |  |
| COMMENT |  |  |
| COMMENT |  |  |
| COMMENT |  *** Column dimensions (2 D or greater) *** |  |
| COMMENT |  |  |
| TDIM4 | ( 3, 500) |  |
| COMMENT |  |  |
| COMMENT |  *** Column names *** |  |
| COMMENT |  |  |
| COMMENT |  |  |
| COMMENT |  *** Column names *** |  |
| COMMENT |  |  |
| COMMENT |  |  |
| COMMENT |  *** Column names *** |  |
| COMMENT |  |  |

##### Binary Table Caption for HDU4
Name | Type | Unit | Description |
| --- | --- | --- | --- |
 | FULLBKPT | float32[1816] |  | Breakpoint vector |
 | BKMASK | int16[1816] |  | mask of the breakpoint vector |
 | NORD | int32 |  | Number of orders for Bspline fit |
 | COEFF | float32[1812] |  | The bspline coefficients |
 | ICOEFF | float32[1812] |  | inversion bspline coefficients |



### HDU5: xsol
X centers for all traces

#### HDU Type: IMAGE
#### HDU Size:  7 MB

##### Header Table Caption for HDU5
Key | Value | Comment | |
| --- | --- | --- | --- |
| XTENSION | IMAGE | Binary table written by MWRFITS v1.13 |
| BITPIX | -32 | Required value |
| NAXIS | 2 | Required value |
| NAXIS1 | 4112 | Number of bytes per row |
| NAXIS2 | 500 | Number of rows |
| PCOUNT | 0 | Normally 0 (no varying arrays) |
| GCOUNT | 1 | Required value |
| TFIELDS | 5 | Number of columns in table |
| COMMENT |  |  |
| COMMENT |  *** End of mandatory fields *** |  |
| COMMENT |  |  |
| COMMENT |  |  |
| COMMENT |  *** End of mandatory fields *** |  |
| COMMENT |  |  |
| COMMENT |  |  |
| COMMENT |  *** End of mandatory fields *** |  |
| COMMENT |  |  |
| EXTNAME | xsol |  |
| COMMENT |  |  |
| COMMENT |  *** Column formats *** |  |
| COMMENT |  |  |
| COMMENT |  |  |
| COMMENT |  *** Column formats *** |  |
| COMMENT |  |  |
| COMMENT |  |  |
| COMMENT |  *** Column formats *** |  |
| COMMENT |  |  |
| COMMENT |  |  |
| COMMENT |  *** Column dimensions (2 D or greater) *** |  |
| COMMENT |  |  |
| COMMENT |  |  |
| COMMENT |  *** Column dimensions (2 D or greater) *** |  |
| COMMENT |  |  |
| TDIM4 | ( 3, 500) |  |
| COMMENT |  |  |
| COMMENT |  *** Column names *** |  |
| COMMENT |  |  |
| COMMENT |  |  |
| COMMENT |  *** Column names *** |  |
| COMMENT |  |  |
| COMMENT |  |  |
| COMMENT |  *** Column names *** |  |
| COMMENT |  |  |



---
## Notes
None

---
## Regrets
I have no regrets!