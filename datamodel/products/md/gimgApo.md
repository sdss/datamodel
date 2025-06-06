# Data Model: gimgApo


APO Guide Focus Acquisition Camera raw image


## Contents
- [Basic Information](#basic-information)
- [Changelog](#changelog)
- [Example HDUS List](#example-hdus-list)
- [Notes](#notes)
- [Regrets](#regrets)
---

## Basic Information
Guide Focus Acquisition Camera raw image from one of six cameras located around the periphery of the robotic array.  Used for telescope guiding and focus.

### Naming Convention
$GCAM_DATA_N/[MJD]/gimg-gfa[CAMNUM]n-[EXPNUM].fits

### Releases
DR19, WORK

### Enviroments
GCAM_DATA_N

### Approximate Size
3 MB

### File Type
FITS

### Generated by Product
fliswarm

### Is a VAC
False

### Data Level
0.1.1

### HDUS List for release WORK
  - [HDU0: PRIMARY](#hdu0-primary)
  - [HDU1: RAW](#hdu1-raw)

---

## Changelog
Describes changes to the datamodel product and/or file structure from one release to another
 - WORK
   - from: DR19
   - note: No changes

---
## Example HDUS List

### HDU0: PRIMARY
empty

#### HDU Type: IMAGE
#### HDU Size:  0 bytes

##### Header Table Caption for HDU0
Key | Value | Comment | |
| --- | --- | --- | --- |
| SIMPLE | True | conforms to FITS standard |
| BITPIX | 8 | array data type |
| NAXIS | 0 | number of array dimensions |
| EXTEND | True |  |
| CHECKSUM | B5fHE5Z9B5dEB5Z9 | HDU checksum updated 2024-12-04T01:34:49 |
| DATASUM | 0 | data unit checksum updated 2024-12-04T01:34:49 |



### HDU1: RAW
raw image data

#### HDU Type: IMAGE
#### HDU Size:  8 MB

##### Header Table Caption for HDU1
Key | Value | Comment | |
| --- | --- | --- | --- |
| XTENSION | IMAGE | Image extension |
| BITPIX | 16 | data type of original image |
| NAXIS | 2 | dimension of original image |
| NAXIS1 | 2048 | length of original image axis |
| NAXIS2 | 2048 | length of original image axis |
| PCOUNT | 0 | number of parameters |
| GCOUNT | 1 | number of groups |
| EXTNAME | RAW | extension name |
| CAMNAME | gfa2n | Camera name |
| VCAM | 0.6.1a0 | Version of the camera library |
| IMAGETYP | object | The image type of the file |
| EXPTIME | 15.0 | Exposure time of single integration [s] |
| EXPTIMEN | 15.0 | Total exposure time [s] |
| STACK | 1 | Number of stacked frames |
| STACKFUN | median | Function used for stacking |
| TIMESYS | TAI | Time reference system |
| SJD | 60648 | SDSS custom Julian Day |
| DATE-OBS | 2024-12-04 01:35:06.421088 | Time of the start of the exposure [TAI] |
| CCDTEMP | -20.0 | Degrees C |
| BEGX | 0 | Window start pixel in X |
| BEGY | 0 | Window start pixel in Y |
| ENDX | 2048 | Window end pixel in X |
| EDNY | 2048 | Window end pixel in Y |
| BINX | 1 | Binning in X |
| BINY | 1 | Binning in Y |
| GAIN | 1.48 | The CCD gain [e-/ADUs] |
| READNOIS | 15.2 | The CCD read noise [ADUs] |
| PIXELSC | 0.2214 | Scale of unbinned pixel on sky [arcsec/pix] |
| WCSAXES | 2 | Number of coordinate axes |
| CRPIX1 | 0.0 | Pixel coordinate of reference point |
| CRPIX2 | 0.0 | Pixel coordinate of reference point |
| CDELT1 | 1.0 | Coordinate increment at reference point |
| CDELT2 | 1.0 | Coordinate increment at reference point |
| CRVAL1 | 0.0 | Coordinate value at reference point |
| CRVAL2 | 0.0 | Coordinate value at reference point |
| LATPOLE | 90.0 | [deg] Native latitude of celestial pole |
| MJDREF | 0.0 | [d] MJD of fiducial time |
| OBSERVAT | APO | Observatory |
| OBJSYS | ICRS | The TCC objSys |
| RA | 299.474394 | RA of telescope boresight (deg) |
| DEC | 29.169265 | Dec of telescope boresight (deg) |
| RADEG | 299.477391 | RA of telescope pointing (deg) |
| DECDEG | 29.17005 | Dec of telescope pointing (deg) |
| SPA | -14.36210698614883 | TCC SpiderInstAng |
| ROTPOS | 57.5446 | Rotator request type |
| BOREOFFX | 0.0 | TCC Boresight offset, deg |
| BOREOFFY | 0.0 | TCC Boresight offset, deg |
| ARCOFFX | -0.002617 | TCC ObjArcOff, deg |
| ARCOFFY | -0.000785 | TCC ObjArcOff, deg |
| CALOFFX | 0.0 | TCC CalibOff, deg |
| CALOFFY | 0.0 | TCC CalibOff, deg |
| CALOFFR | 0.0 | TCC CalibOff, deg |
| GUIDOFFX | 0.0 | TCC GuideOff, deg |
| GUIDOFFY | 0.0 | TCC GuideOff, deg |
| GUIDOFFR | -0.076706 | TCC GuideOff, deg |
| AZ | 260.288779 | Azimuth axis pos. (approx, deg) |
| ALT | 46.198008 | Altitude axis pos. (approx, deg) |
| IPA | 165.652447 | Rotator axis pos. (approx, deg) |
| FOCUS | 135.39 | User-specified focus offset (um) |
| M1PISTON | 0.0 | TCC PrimOrient |
| M1XTILT | -18.23 | TCC PrimOrient |
| M1YTILT | -7.9 | TCC PrimOrient |
| M1XTRAN | -427.17 | TCC PrimOrient |
| M1YTRAN | -999.0 | TCC PrimOrient |
| M1ZROT | 0.0 | TCC PrimOrient |
| M2PISTON | 4728.79 | SecOrient |
| M2XTILT | -24.58 | SecOrient |
| M2YTILT | -17.47 | SecOrient |
| M2XTRAN | 18.41 | SecOrient |
| M2YTRAN | 47.37 | SecOrient |
| M2ZROT | -32.42 | SecOrient |
| SCALE | 1.0 | User-specified scale factor |
| FF | 0 0 0 0 | FF lamps 1:on 0:0ff |
| NE | 0 0 0 0 | NE lamps 1:on 0:0ff |
| HGCD | 0 0 0 0 | HGCD lamps 1:on 0:0ff |
| FFS | 0 0 0 0 0 0 0 0 | Flatfield Screen 1:closed 0:open |
| V_APO | 4.1.0 | Version of the current apoActor |
| PRESSURE | 21.574 |  |
| WINDD | 183.9 |  |
| WINDS | 10.2 |  |
| GUSTD | 200.1 |  |
| GUSTS | 12.0 |  |
| AIRTEMP | 0.0 |  |
| DEWPOINT | 0.0 |  |
| TRUSTEMP | -26.18 |  |
| HUMIDITY | 80.4 |  |
| DUSTA | -999.0 |  |
| DUSTB | -999.0 |  |
| WINDD25M | -999.0 |  |
| WINDS25M | -999.0 |  |
| CARTID | FPS-N | Cart ID |
| CONFIGID | 17592 | Configuration ID |
| DESIGNID | 672687 | Design ID associated with CONFIGID |
| FIELDID | 102404 | Field ID associated with CONFIGID |
| RAFIELD | 299.477390623955 | Field right ascension |
| DECFIELD | 29.1700500129573 | Field declination |
| FIELDPA | 57.544647 | Field position angle |
| BIASFILE |  | Bias file associated with this image |
| BSCALE | 1 |  |
| BZERO | 32768 |  |
| CHECKSUM | UFCcV99bUECbU99b | HDU checksum updated 2024-12-04T01:34:48 |
| DATASUM | 956385174 | data unit checksum updated 2024-12-04T01:34:48 |



---
## Notes
None

---
## Regrets
I  have no regrets!