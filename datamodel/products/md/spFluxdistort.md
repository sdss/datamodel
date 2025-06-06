# Data Model: spFluxdistort


This file contains the flux distortion image.


## Contents
- [Basic Information](#basic-information)
- [Changelog](#changelog)
- [Example HDUS List](#example-hdus-list)
- [Notes](#notes)

---

## Basic Information
This file contains the flux distortion image.

### Naming Convention
$BOSS_SPECTRO_REDUX/[RUN2D]/[FIELD]/spFluxdistort-[FIELD]-[MJD]-[FRAME].fits

### Releases
IPL3, DR19

### Enviroments
BOSS_SPECTRO_REDUX

### Approximate Size
8 MB

### File Type
FITS

### Generated by Product
idlspec2d - rm_spcoadd_v5.pro

### Is a VAC
False

### HDUS List for release DR19
  - [HDU0: PRIMARY](#hdu0-primary)

---

## Changelog
Describes changes to the datamodel product and/or file structure from one release to another
 - DR19
   - from: IPL3
   - note: No changes

---
## Example HDUS List

### HDU0: PRIMARY
Image with the flux distortion vector for each fiber.

#### HDU Type: IMAGE
#### HDU Size:  8 MB

##### Header Table Caption for HDU0
Key | Value | Comment | |
| --- | --- | --- | --- |
| SIMPLE | True | Written by IDL:  Wed Apr  3 02:01:41 2024 |
| BITPIX | -32 | Number of bits per data pixel |
| NAXIS | 2 | Number of data axes |
| NAXIS1 | 4648 |  |
| NAXIS2 | 500 |  |
| EXTEND | True |  |
|  |  |  |
|  | INSTRUMENT INFO |  |
| TELESCOP | SDSS 2.5-M | Telescope |
| OBSERVAT | APO | Observatory |
| SPEC |  | Spectrograph name |
| NGUIDE | 15 | Number of guider frames during exposure |
| SEEING20 | 1.141 | 20% seeing during exposure (arcsec) |
| SEEING50 | 1.261 | 50% seeing during exposure (arcsec) |
| SEEING80 | 1.508 | 80% seeing during exposure (arcsec) |
| RMSOFF20 | 0.128035 | 20% RMS offset of guide fibers (arcsec) |
| RMSOFF50 | 0.167586 | 50% RMS offset of guide fibers (arcsec) |
| RMSOFF80 | 0.255783 | 80% RMS offset of guide fibers (arcsec) |
|  |  |  |
|  | EXPOSURE INFO |  |
| EXPOSURE | 353048 | Exposure number |
| FLAVOR | science | exposure type, SDSS spectro style |
| QUALITY | excellent | Exposure Quality |
| MJD | 60000 | Modified Julian Date at start of exposure |
| TAI-BEG | 5184019757.0 | MJD(TAI) seconds at start of integration |
| DATE-OBS | 2023-02-25T05:29:17 | TAI date at start of integration |
| INTSTART |  | Start of the integration |
| INTEND |  | End of the integration |
| REQTIME | 900.0 | requested exposure time |
| EXPTIME | 900.09 | requested exposure time |
| DARKTIME | 916.907684326 | time between flush end and readout start |
| SHOPETIM | 0.75 | open shutter transit time (s) |
| SHCLOTIM | 0.54 | close shutter transit time (s) |
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
| CARTID | FPS-N | Cartridge used in this plugging |
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
| RA | 150.013468 | RA of telescope boresight (deg) |
| DEC | 2.183181 | Dec of telescope boresight (deg) |
| RADEG | 150.01675 | RA of telescope pointing(deg) |
| DECDEG | 2.18325 | Dec of telescope pointing (deg) |
| EQUINOX | 2000.0 | Equinox of celestial coordinate system |
| RADECSYS | FK5 |  |
| OFFRA | 0.0 | Absolute guider offset in RA |
| OFFDEC | -0.1 | Absolute guider offset in DEC |
| OFFPA | -432.0 | Absolute guider offset in PA |
| GSEEING | 1.19 | Seeing from the guider (arcsec) |
| AIRMASS | 1.21229 | AIRMASS |
| HA |  | HA axis pos. (approx, deg) |
| SPA | 41.822992 | TCC SpiderInstAng |
| ROTPOS | 13.5 | Rotator request position (deg) |
| AZ | 34.274411 | Azimuth axis pos. (approx, deg) |
| ALT | 54.475041 | Altitude axis pos. (approx, deg) |
| IPA | 221.633737 | Rotator axis pos. (approx, deg) |
| FOCUS | 205.0 | User-specified focus offset (um) |
| SCALE | 1.0 | User-specified scale factor |
| OBJSYS | ICRS | The TCC objSys |
| BOREOFFX | 0.0 | TCC Boresight offset (deg) |
| BOREOFFY | 0.0 | TCC Boresight offset (deg) |
| ARCOFFX | -0.003279 | TCC ObjArcOff (deg) |
| ARCOFFY | -6.9e-05 | TCC ObjArcOff (deg) |
| CALOFFX | 0.0 | TCC CalibOff (deg) |
| CALOFFY | 0.0 | TCC CalibOff (deg) |
| CALOFFR | 0.0 | TCC CalibOff (deg) |
| GUIDOFFX | 0.0 | TCC GuideOff (deg) |
| GUIDOFFY | 0.0 | TCC GuideOff (deg) |
| GUIDOFFR | 0.164006 | TCC GuideOff (deg) |
| M2PISTON | 3972.29 | TCC SecOrient |
| M2XTILT | -0.01 | TCC SecOrient |
| M2YTILT | -0.01 | TCC SecOrient |
| M2XTRAN | -0.01 | TCC SecOrient |
| M2YTRAN | -66.18 | TCC SecOrient |
| M2ZROT | -11.12 | TCC SecOrient |
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
| MCHUMHT | 3.9 | spec mech Hartmann humidity (%) |
| MCHUMCO | 2.4 | spec mech Central optics humidity (%) |
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
| COLLA | 1742 | The position of the A collimator motor |
| COLLB | 1740 | The position of the B collimator motor |
| COLLC | 1759 | The position of the C collimator motor |
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
| VERS2D | v6_1_3 | Version of idlspec2d for 2D reduction |
|  |  |  |
|  | APO WEATHER |  |
| PRESSURE | 21.549 | APO SDSS 2.5m Air Pressure (inch Hg) |
| WINDD | 198.1 | APO SDSS 2.5m Wind Direction (deg) |
| WINDS | 19.3 | APO SDSS 2.5m Wind Speed (mph) |
| GUSTD | 204.1 | APO SDSS 2.5m Wind Gust Direction (deg) |
| GUSTS | 22.0 | APO SDSS 2.5m Wind Gust Speed (mph) |
| AIRTEMP | 0.0 | APO SDSS 2.5m Outside temperature (deg C) |
| DEWPOINT | 0.0 | APO SDSS 2.5m Dewpoint (deg C) |
| TRUSTEMP | 3.0 | APO SDSS 2.5m Truss Temperature (deg C) |
| HUMIDITY | NaN | APO SDSS 2.5m Humidity (percent) |
| DUSTA | 13818.0 | APO SDSS 2.5m dust (count of 0.3mu/particles/vol |
| DUSTB | 1480.0 | APO SDSS 2.5m dust (count of 1mu/particles/vol/t |
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
| FF | 0 0 0 0 | Flat Field lamps 1:on 0:off |
| FFS | 0 0 0 0 0 0 0 0 | Flatfield Screen 1:closed 0:open |
| HARTMANN | Out | Hartmanns: Left,Right,Out,Closed |
|  |  |  |
|  | REDUCTION |  |
| RDNOISE0 | 2.05857 | CCD read noise amp 0 [electrons] |
| RDNOISE1 | 1.91756 | CCD read noise amp 1 [electrons] |
| RDNOISE2 | 1.88385 | CCD read noise amp 2 [electrons] |
| RDNOISE3 | 2.00696 | CCD read noise amp 3 [electrons] |
| PIXFLAT | pixflatave-59768-b1.fits.gz | Name of Pixel Flat used |
| BADPIXEL | badpixels-59747-b1.fits.gz | Name of Badpixel mask used |
|  |  |  |
|  | PIPELINE OUTPUTS |  |
| RUN2D | v6_1_3 | Spectro-2D reduction name |
| TAI-END | 5184020657.09 |  |
| FRAMESN2 | 0.637019265761 | (S/N)^2 at fidicial magnitude |
| DEREDSN2 | 0.637019265761 | Extinction corrected (S/N)^2 (like quick redux) |
| REDDEN01 | 0.0 | Median extinction in u-band |
| REDDEN02 | 0.0 | Median extinction in g-band |
| REDDEN03 | 0.0 | Median extinction in r-band |
| REDDEN04 | 0.0 | Median extinction in i-band |
| REDDEN05 | 0.0 | Median extinction in z-band |
| XSIGMA | 1.06889 |  |
| WSIGMA | 1.08981 |  |
| WDISPR | 3.10333 |  |
| CONFSFIL | confSummaryF-8872.par |  |
| FLATFILE | sdR-b1-00353044.fit |  |
| ARCFILE | sdR-b1-00353047.fit |  |
| OBJFILE | sdR-b1-00353048.fit |  |
| LAMPLIST | lamphgcdne.dat |  |
| SKYLIST | skylines.dat |  |
| OBSMODE | dark_rm |  |
| SIGBS0 | 0.034 | 5577.3 line gaussian fit sigma position before |
| CENBS0 | -0.272 | 5577.3 line gaussian fit center position before |
| AVGBS0 | -0.289 | 5577.3 line average position before shift (pixe |
| STDBS0 | 0.042 | 5577.3 line std position before shift (pixels) |
| AVGAS0 | -0.001 | 5577.3 line average position after shift (pixel |
| STDAS0 | 0.018 | 5577.3 line std position after shift (pixels) |
| HELIO_RV | 1.95078733724 | V_RAD for backwards compatibility |
| V_RAD | 1.95078733724 | radial velocity relative to the barycenter (add |
| VACUUM | True | Wavelengths are in vacuum |
| SFLATTEN | True | Superflat has been applied |
| PSFSKY | 3 | Order of PSF skysubtraction |
| SKYCHI2 | 0.900314249399 | Mean chi^2 of sky-subtraction |
| PREJECT | 0.2 | Profile area rejection threshold |
| LOWREJ | 4 | Extraction: low rejection |
| HIGHREJ | 50 | Extraction: high rejection |
| SCATPOLY | 0 | Extraction: Order of scattered light polynomial |
| PROFTYPE | 1 | Extraction profile: 1=Gaussian |
| NFITPOLY | 1 | Extraction: Number of parameters in each profil |
| XCHI2 | 0.0 | Extraction: Mean chi^2 |



---
## Notes
None