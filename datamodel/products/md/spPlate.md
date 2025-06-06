# Data Model: spPlate


The spPlate files contain the combined spectra for all exposures of a given plate.


## Contents
- [Basic Information](#basic-information)
- [Changelog](#changelog)
- [Example HDUS List](#example-hdus-list)
- [Notes](#notes)
- [Regrets](#regrets)
---

## Basic Information
The spPlate files contain the combined spectra for all exposures of a given plate. There are typically four 900s exposures which may have been taken in a single night, or over multiple nights. This file is superceded in SDSS-V by the spField files.

### Naming Convention
$BOSS_SPECTRO_REDUX/[RUN2D]/[FIELD]/spPlate-[FIELD]-[MJD].fits

### Releases
DR9, DR10, DR12, DR11, DR13, DR14, DR15, DR16, DR17

### Enviroments
BOSS_SPECTRO_REDUX

### Approximate Size
63 MB

### File Type
FITS

### Generated by Product
idlspec2d

### Is a VAC
False

### Data Level
0.0.0

### HDUS List for release DR17
  - [HDU0: PRIMARY](#hdu0-primary)
  - [HDU1: IVAR](#hdu1-ivar)
  - [HDU2: ANDMASK](#hdu2-andmask)
  - [HDU3: ORMASK](#hdu3-ormask)
  - [HDU4: WAVEDISP](#hdu4-wavedisp)
  - [HDU5: PLUGMAP](#hdu5-plugmap)
  - [HDU6: SKY](#hdu6-sky)

---

## Changelog
Describes changes to the datamodel product and/or file structure from one release to another
 - DR17
   - from: DR16
   - note: No changes
 - DR16
   - from: DR15
   - added_primary_header_kwargs: ['EXPID004', 'EXPID005', 'EXPID030', 'EXPID011', 'EXPID010', 'EXPID014', 'EXPID040', 'EXPID013', 'EXPID024', 'EXPID035', 'EXPID022', 'EXPID020', 'EXPID021', 'EXPID029', 'EXPID031', 'EXPID032', 'EXPID016', 'EXPID034', 'EXPID008', 'EXPID018', 'EXPID007', 'EXPID037', 'EXPID028', 'EXPID017', 'EXPID039', 'EXPID006', 'EXPID002', 'EXPID023', 'EXPID019', 'EXPID009', 'EXPID001', 'EXPID003', 'EXPID015', 'EXPID012', 'EXPID027', 'EXPID026', 'EXPID038', 'EXPID036', 'EXPID025', 'EXPID033']
   - removed_primary_header_kwargs: ['EXPID15', 'EXPID07', 'EXPID36', 'EXPID16', 'EXPID08', 'EXPID32', 'EXPID34', 'EXPID04', 'EXPID19', 'EXPID22', 'EXPID05', 'EXPID26', 'EXPID38', 'EXPID18', 'EXPID03', 'EXPID10', 'EXPID02', 'EXPID13', 'EXPID20', 'EXPID09', 'EXPID01', 'EXPID40', 'EXPID11', 'EXPID39', 'EXPID37', 'EXPID24', 'EXPID35', 'EXPID28', 'EXPID23', 'EXPID30', 'EXPID14', 'EXPID25', 'EXPID06', 'EXPID27', 'EXPID12', 'EXPID31', 'EXPID33', 'EXPID17', 'EXPID29', 'EXPID21']
 - DR15
   - from: DR14
   - note: No changes
 - DR14
   - from: DR13
   - note: No changes
 - DR13
   - from: DR11
   - primary_delta_nkeys: 2
   - removed_primary_header_kwargs: ['XCHI2MIN', 'XCHI2MAX']
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

### HDU0: PRIMARY
coadded calibrated flux

#### HDU Type: IMAGE
#### HDU Size:  17 MB

##### Header Table Caption for HDU0
Key | Value | Comment | |
| --- | --- | --- | --- |
| SIMPLE | True | conforms to FITS standard |
| BITPIX | -32 | array data type |
| NAXIS | 2 | number of array dimensions |
| NAXIS1 | 4646 |  |
| NAXIS2 | 1000 |  |
| EXTEND | True |  |
| TELESCOP | SDSS 2.5-M | Sloan Digital Sky Survey |
| NGUIDE | 0 | Number of guider frames during exposure |
| SEEING20 | 0.0 | 20% seeing during exposure (arcsec) |
| SEEING50 | 0.0 | 50% seeing during exposure (arcsec) |
| SEEING80 | 0.0 | 80% seeing during exposure (arcsec) |
| RMSOFF20 | 0.0 | 20% RMS offset of guide fibers (arcsec) |
| RMSOFF50 | 0.0 | 50% RMS offset of guide fibers (arcsec) |
| RMSOFF80 | 0.0 | 80% RMS offset of guide fibers (arcsec) |
| DAQVER | 1.2.8 |  |
| CAMDAQ | 1.4.1:31 |  |
| ERRCNT | NONE |  |
| SYNCERR | NONE |  |
| SLINES | NONE |  |
| PIXERR | NONE |  |
| PLINES | NONE |  |
| FLAVOR | science | exposure type, SDSS spectro style |
| BOSSVER | branch_jme-rewrite+svn105958 | ICC version |
| MJD | 55182 | APO MJD day at start of exposure |
| MJDLIST | 55181 55182 |  |
| TAI-BEG | 4767651797.0 | MJD(TAI) seconds at start of exposure |
| DATE-OBS | 2009-12-16T03:43:17 | TAI date at start of exposure |
| OBJSYS | ICRS | The TCC objSys |
| RA | 28.001011 | RA of telescope boresight (deg) |
| DEC | 0.000273 | Dec of telescope boresight (deg) |
| EQUINOX | 2000.0 |  |
| RADECSYS | FK5 |  |
| RADEG | 28.0 | RA of telescope pointing(deg) |
| DECDEG | 0.0 | Dec of telescope pointing (deg) |
| ROTPOS | 0.0 | Rotator request position (deg) |
| BOREOFFX | 0.0 | TCC Boresight offset, deg |
| BOREOFFY | 0.0 | TCC Boresight offset, deg |
| ARCOFFX | 0.001011 | TCC ObjArcOff, deg |
| ARCOFFY | 0.000273 | TCC ObjArcOff, deg |
| OBJOFFX | 0.0 | TCC ObjOff, deg |
| OBJOFFY | 0.0 | TCC ObjOff, deg |
| CALOFFX | 0.0 | TCC CalibOff, deg |
| CALOFFY | 0.0 | TCC CalibOff, deg |
| CALOFFR | 0.0 | TCC CalibOff, deg |
| GUIDOFFX | 0.0 | TCC GuideOff, deg |
| GUIDOFFY | 0.0 | TCC GuideOff, deg |
| GUIDOFFR | 0.025747 | TCC GuideOff, deg |
| AZ | -27.8383 | Azimuth axis pos. (approx, deg) |
| ALT | 53.1857 | Altitude axis pos. (approx, deg) |
| AIRMASS | 1.20358 |  |
| FOCUS | 489.22 | User-specified focus offset (um) |
| M2PISTON | 2377.59 | TCC SecOrient |
| M2XTILT | -3.99 | TCC SecOrient |
| M2YTILT | -9.02 | TCC SecOrient |
| M2XTRAN | 10.04 | TCC SecOrient |
| M2YTRAN | 81.54 | TCC SecOrient |
| M1PISTON | 878.14 | TCC PrimOrient |
| M1XTILT | -3.55 | TCC PrimOrient |
| M1YTILT | 5.26 | TCC PrimOrient |
| M1XTRAN | 277.92 | TCC PrimOrient |
| M1YTRAN | 177.48 | TCC PrimOrient |
| SCALE | 0.999911 | User-specified scale factor |
| NAME | 3606-55180-01 | The name of the currently loaded plate |
| PLATEID | 3606 | The currently loaded plate |
| TILEID | 10070 | Cartridge used in this plugging |
| CARTID | 14 | Cartridge used in this plugging |
| MAPID | 1 | The mapping version of the loaded plate |
| POINTING | A | The currently specified pointing |
| GUIDER1 | proc-gimg-0258.fits | The first guider image |
| COLLA | 11677 | The position of the A collimator motor |
| COLLB | 12284 | The position of the B collimator motor |
| COLLC | 12953 | The position of the C collimator motor |
| HARTMANN | Out | Hartmanns: Left,Right,Out |
| MC1HUMHT | 45.7 | sp1 mech Hartmann humidity, % |
| MC1HUMCO | 34.9 | sp1 mech Central optics humidity, % |
| MC1TEMDN | 1.1 | sp1 mech Median temp, C |
| MC1THT | 0.3 | sp1 mech Hartmann Top Temp, C |
| MC1TRCB | 1.1 | sp1 mech Red Cam Bottom Temp, C |
| MC1TRCT | 2.2 | sp1 mech Red Cam Top Temp, C |
| MC1TBCB | 1.0 | sp1 mech Blue Cam Bottom Temp, C |
| MC1TBCT | 1.4 | sp1 mech Blue Cam Top Temp, C |
| MC2HUMHT | 46.2 | sp2 mech Hartmann humidity, % |
| MC2HUMCO | 39.6 | sp2 mech Central optics humidity, % |
| MC2TEMDN | 0.2 | sp2 mech Median temp, C |
| MC2THT | -0.1 | sp2 mech Hartmann Top Temp, C |
| MC2TRCB | 0.6 | sp2 mech Red Cam Bottom Temp, C |
| MC2TRCT | 0.2 | sp2 mech Red Cam Top Temp, C |
| MC2TBCB | 0.0 | sp2 mech Blue Cam Bottom Temp, C |
| MC2TBCT | 0.6 | sp2 mech Blue Cam Top Temp, C |
| GUIDERN | proc-gimg-0284.fits | The last guider image |
| NEXP | 40 | Number of exposures in this file |
| BESTEXP | 104940 |  |
| EXPID001 | b1-00104940-00104944-00104945 | ID string for exposure 1 |
| EXPID002 | b1-00104941-00104944-00104945 | ID string for exposure 2 |
| EXPID003 | b1-00104942-00104944-00104945 | ID string for exposure 3 |
| EXPID004 | b1-00104943-00104944-00104945 | ID string for exposure 4 |
| EXPID005 | b1-00105003-00105010-00105011 | ID string for exposure 5 |
| EXPID006 | b1-00105004-00105010-00105011 | ID string for exposure 6 |
| EXPID007 | b1-00105006-00105010-00105011 | ID string for exposure 7 |
| EXPID008 | b1-00105007-00105010-00105011 | ID string for exposure 8 |
| EXPID009 | b1-00105008-00105010-00105011 | ID string for exposure 9 |
| EXPID010 | b1-00105009-00105010-00105011 | ID string for exposure 10 |
| EXPID011 | b2-00104940-00104944-00104945 | ID string for exposure 11 |
| EXPID012 | b2-00104941-00104944-00104945 | ID string for exposure 12 |
| EXPID013 | b2-00104942-00104944-00104945 | ID string for exposure 13 |
| EXPID014 | b2-00104943-00104944-00104945 | ID string for exposure 14 |
| EXPID015 | b2-00105003-00105010-00105011 | ID string for exposure 15 |
| EXPID016 | b2-00105004-00105010-00105011 | ID string for exposure 16 |
| EXPID017 | b2-00105006-00105010-00105011 | ID string for exposure 17 |
| EXPID018 | b2-00105007-00105010-00105011 | ID string for exposure 18 |
| EXPID019 | b2-00105008-00105010-00105011 | ID string for exposure 19 |
| EXPID020 | b2-00105009-00105010-00105011 | ID string for exposure 20 |
| EXPID021 | r1-00104940-00104944-00104945 | ID string for exposure 21 |
| EXPID022 | r1-00104941-00104944-00104945 | ID string for exposure 22 |
| EXPID023 | r1-00104942-00104944-00104945 | ID string for exposure 23 |
| EXPID024 | r1-00104943-00104944-00104945 | ID string for exposure 24 |
| EXPID025 | r1-00105003-00105010-00105011 | ID string for exposure 25 |
| EXPID026 | r1-00105004-00105010-00105011 | ID string for exposure 26 |
| EXPID027 | r1-00105006-00105010-00105011 | ID string for exposure 27 |
| EXPID028 | r1-00105007-00105010-00105011 | ID string for exposure 28 |
| EXPID029 | r1-00105008-00105010-00105011 | ID string for exposure 29 |
| EXPID030 | r1-00105009-00105010-00105011 | ID string for exposure 30 |
| EXPID031 | r2-00104940-00104944-00104945 | ID string for exposure 31 |
| EXPID032 | r2-00104941-00104944-00104945 | ID string for exposure 32 |
| EXPID033 | r2-00104942-00104944-00104945 | ID string for exposure 33 |
| EXPID034 | r2-00104943-00104944-00104945 | ID string for exposure 34 |
| EXPID035 | r2-00105003-00105010-00105011 | ID string for exposure 35 |
| EXPID036 | r2-00105004-00105010-00105011 | ID string for exposure 36 |
| EXPID037 | r2-00105006-00105010-00105011 | ID string for exposure 37 |
| EXPID038 | r2-00105007-00105010-00105011 | ID string for exposure 38 |
| EXPID039 | r2-00105008-00105010-00105011 | ID string for exposure 39 |
| EXPID040 | r2-00105009-00105010-00105011 | ID string for exposure 40 |
| NEXP_B1 | 10 | b1 camera number of exposures |
| NEXP_B2 | 10 | b2 camera number of exposures |
| NEXP_R1 | 10 | r1 camera number of exposures |
| NEXP_R2 | 10 | r2 camera number of exposures |
| EXPT_B1 | 9004.0 | b1 camera exposure time (seconds) |
| EXPT_B2 | 9003.0 | b2 camera exposure time (seconds) |
| EXPT_R1 | 9004.0 | r1 camera exposure time (seconds) |
| EXPT_R2 | 9003.0 | r2 camera exposure time (seconds) |
| EXPTIME | 9003.0 | Minimum of exposure times for all cameras |
| SPCOADD | Tue May 12 07:16:52 2020 | SPCOADD finished |
| SHOPETIM | 0.735 | open shutter transit time, s |
| SHCLOTIM | 0.55 | close shutter transit time, s |
| AUTHOR | Scott Burles & David Schlegel |  |
| VERSIDL | 7.1.1 | Version of IDL |
| VERSUTIL | v5_5_17 | Version of idlutils |
| VERSREAD | v5_13_2 | Version of idlspec2d for pre-processing raw dat |
| VERS2D | v5_13_2 | Version of idlspec2d for 2D reduction |
| VERSCOMB | v5_13_2 | Version of idlspec2d for combining multiple spe |
| VERSLOG | trunk 26892 | Version of SPECLOG product |
| VERSFLAT | v1_32 | Version of SPECFLAT product |
| TWOPHASE | False |  |
| RDNOISE0 | 2.02617 | CCD read noise amp 0 [electrons] |
| BADPIXEL | badpixels-55056-b1.fits.gz |  |
| RUN2D | v5_13_2 | Spectro-2D reduction name |
| TAI-END | 4767744569.0 |  |
| REDDEN01 | 0.1615 | Median extinction in u-band |
| REDDEN02 | 0.1188 | Median extinction in g-band |
| REDDEN03 | 0.0862 | Median extinction in r-band |
| REDDEN04 | 0.0653 | Median extinction in i-band |
| REDDEN05 | 0.0463 | Median extinction in z-band |
| XSIGMA | 1.24718 |  |
| XSIGMIN | 1.04837 |  |
| XSIGMAX | 1.33269 |  |
| WSIGMA | 1.23172 |  |
| WSIGMIN | 1.11223 |  |
| WSIGMAX | 1.30906 |  |
| PLUGFILE | plPlugMapM-3606-55180-01.par |  |
| LAMPLIST | lamphgcdne.dat |  |
| SKYLIST | skylines.dat |  |
| HELIO_RV | 25.651407139 | Heliocentric correction (added to velocities) |
| VACUUM | True | Wavelengths are in vacuum |
| SFLATTEN | True | Superflat has been applied |
| PSFSKY | 3 | Order of PSF skysubtraction |
| SKYCHI2 | 1.12456156354 | Mean chi^2 of sky-subtraction |
| SCHI2MIN | 0.96159253806 |  |
| SCHI2MAX | 1.35154027834 |  |
| PREJECT | 0.2 | Profile area rejection threshold |
| SPEC1_G | 23.4987 | (S/N)^2 for spec  1 at mag 21.20 |
| SN2EXT1G | 23.4987 | Extinction corrected (S/N)^2 |
| SPEC1_R | 56.5887 | (S/N)^2 for spec  1 at mag 20.20 |
| SN2EXT1R | 56.5887 | Extinction corrected (S/N)^2 |
| SPEC1_I | 42.3044 | (S/N)^2 for spec  1 at mag 20.20 |
| SN2EXT1I | 42.3044 | Extinction corrected (S/N)^2 |
| SPEC2_G | 17.8264 | (S/N)^2 for spec  2 at mag 21.20 |
| SN2EXT2G | 17.8264 | Extinction corrected (S/N)^2 |
| SPEC2_R | 48.7679 | (S/N)^2 for spec  2 at mag 20.20 |
| SN2EXT2R | 48.7679 | Extinction corrected (S/N)^2 |
| SPEC2_I | 39.813 | (S/N)^2 for spec  2 at mag 20.20 |
| SN2EXT2I | 39.813 | Extinction corrected (S/N)^2 |
| NSTD | 20 | Number of (good) std stars |
| GOFFSTD | 0.00389767 | Spectrophoto offset for std stars in G-band |
| GRMSSTD | 0.0587422 | Spectrophoto RMS for std stars in G-band |
| ROFFSTD | -0.0083313 | Spectrophoto offset for std stars in R-band |
| RRMSSTD | 0.0406629 | Spectrophoto RMS for std stars in R-band |
| IOFFSTD | 0.00646877 | Spectrophoto offset for std stars in I-band |
| IRMSSTD | 0.0573644 | Spectrophoto RMS for std stars in I-band |
| GROFFSTD | 0.00730133 | Spectrophoto offset for std stars in (GR) |
| GRRMSSTD | 0.05883 | Spectrophoto RMS for std stars in (GR) |
| RIOFFSTD | -0.00788879 | Spectrophoto offset for std stars in (RI) |
| RIRMSSTD | 0.0370529 | Spectrophoto RMS for std stars in (RI) |
| LOWREJ | 4 | Extraction: low rejection |
| HIGHREJ | 4 | Extraction: high rejection |
| SCATPOLY | 0 | Extraction: Order of scattered light polynomial |
| PROFTYPE | 1 | Extraction profile: 1=Gaussian |
| NFITPOLY | 1 | Extraction: Number of parameters in each profil |
| XCHI2 | 0.0 | Extraction: Mean chi^2 |
| NWORDER | 2 | Linear-log10 coefficients |
| COEFF0 | 3.5513 | Central wavelength (log10) of first pixel |
| COEFF1 | 0.0001 | Log10 dispersion per pixel |
| UNAME | kp139 |  |
| FBADPIX | 0.0396756 | Fraction of bad pixels |
| FBADPIX1 | 0.036316 | Fraction of bad pixels on spectro-1 |
| FBADPIX2 | 0.0430486 | Fraction of bad pixels on spectro-2 |
| WAT0_001 | system=linear |  |
| WAT1_001 | wtype=linear label=Wavelength units=Angstroms |  |
| CRVAL1 | 3.5513 | Central wavelength (log10) of first pixel |
| CD1_1 | 0.0001 | Log10 dispersion per pixel |
| CRPIX1 | 1 | Starting pixel (1-indexed) |
| CTYPE1 | LINEAR |  |
| DC-FLAG | 1 | Log-linear flag |
| BUNIT | 1E-17 erg/cm^2/s/Ang |  |



### HDU1: IVAR
inverse variance of flux

#### HDU Type: IMAGE
#### HDU Size:  17 MB

##### Header Table Caption for HDU1
Key | Value | Comment | |
| --- | --- | --- | --- |
| XTENSION | IMAGE | IMAGE extension |
| BITPIX | -32 | Number of bits per data pixel |
| NAXIS | 2 | Number of data axes |
| NAXIS1 | 4646 |  |
| NAXIS2 | 1000 |  |
| PCOUNT | 0 | No Group Parameters |
| GCOUNT | 1 | One Data Group |
| WAT0_001 | system=linear |  |
| WAT1_001 | wtype=linear label=Wavelength units=Angstroms |  |
| CRVAL1 | 3.5513 | Central wavelength (log10) of first pixel |
| CD1_1 | 0.0001 | Log10 dispersion per pixel |
| CRPIX1 | 1 | Starting pixel (1-indexed) |
| CTYPE1 | LINEAR |  |
| DC-FLAG | 1 | Log-linear flag |
| BUNIT | 1/(1E-17 erg/cm^2/s/Ang)^2 |  |
| EXTNAME | IVAR | Inverse variance |



### HDU2: ANDMASK
AND Mask

#### HDU Type: IMAGE
#### HDU Size:  17 MB

##### Header Table Caption for HDU2
Key | Value | Comment | |
| --- | --- | --- | --- |
| XTENSION | IMAGE | IMAGE extension |
| BITPIX | 32 | Number of bits per data pixel |
| NAXIS | 2 | Number of data axes |
| NAXIS1 | 4646 |  |
| NAXIS2 | 1000 |  |
| PCOUNT | 0 | No Group Parameters |
| GCOUNT | 1 | One Data Group |
| WAT0_001 | system=linear |  |
| WAT1_001 | wtype=linear label=Wavelength units=Angstroms |  |
| CRVAL1 | 3.5513 | Central wavelength (log10) of first pixel |
| CD1_1 | 0.0001 | Log10 dispersion per pixel |
| CRPIX1 | 1 | Starting pixel (1-indexed) |
| CTYPE1 | LINEAR |  |
| DC-FLAG | 1 | Log-linear flag |
| EXTNAME | ANDMASK | AND Mask |



### HDU3: ORMASK
OR Mask

#### HDU Type: IMAGE
#### HDU Size:  17 MB

##### Header Table Caption for HDU3
Key | Value | Comment | |
| --- | --- | --- | --- |
| XTENSION | IMAGE | IMAGE extension |
| BITPIX | 32 | Number of bits per data pixel |
| NAXIS | 2 | Number of data axes |
| NAXIS1 | 4646 |  |
| NAXIS2 | 1000 |  |
| PCOUNT | 0 | No Group Parameters |
| GCOUNT | 1 | One Data Group |
| WAT0_001 | system=linear |  |
| WAT1_001 | wtype=linear label=Wavelength units=Angstroms |  |
| CRVAL1 | 3.5513 | Central wavelength (log10) of first pixel |
| CD1_1 | 0.0001 | Log10 dispersion per pixel |
| CRPIX1 | 1 | Starting pixel (1-indexed) |
| CTYPE1 | LINEAR |  |
| DC-FLAG | 1 | Log-linear flag |
| EXTNAME | ORMASK | OR Mask |



### HDU4: WAVEDISP
Wavelength dispersion in number of pixel

#### HDU Type: IMAGE
#### HDU Size:  17 MB

##### Header Table Caption for HDU4
Key | Value | Comment | |
| --- | --- | --- | --- |
| XTENSION | IMAGE | IMAGE extension |
| BITPIX | -32 | Number of bits per data pixel |
| NAXIS | 2 | Number of data axes |
| NAXIS1 | 4646 |  |
| NAXIS2 | 1000 |  |
| PCOUNT | 0 | No Group Parameters |
| GCOUNT | 1 | One Data Group |
| WAT0_001 | system=linear |  |
| WAT1_001 | wtype=linear label=Wavelength units=Angstroms |  |
| CRVAL1 | 3.5513 | Central wavelength (log10) of first pixel |
| CD1_1 | 0.0001 | Log10 dispersion per pixel |
| CRPIX1 | 1 | Starting pixel (1-indexed) |
| CTYPE1 | LINEAR |  |
| DC-FLAG | 1 | Log-linear flag |
| BUNIT | pixels |  |
| EXTNAME | WAVEDISP | Wavelength dispersion |



### HDU5: PLUGMAP
Target level metadata

#### HDU Type: BINARY TABLE
#### HDU Size:  276 KB

##### Header Table Caption for HDU5
Key | Value | Comment | |
| --- | --- | --- | --- |
| XTENSION | BINTABLE | Binary table written by MWRFITS v1.11 |
| BITPIX | 8 | Required value |
| NAXIS | 2 | Required value |
| NAXIS1 | 283 | Number of bytes per row |
| NAXIS2 | 1000 | Number of rows |
| PCOUNT | 0 | Normally 0 (no varying arrays) |
| GCOUNT | 1 | Required value |
| TFIELDS | 35 | Number of columns in table |
| COMMENT |  |  |
| COMMENT |  *** End of mandatory fields *** |  |
| COMMENT |  |  |
| EXTNAME | PLUGMAP | Plugmap structure |
| COMMENT |  |  |
| COMMENT |  *** Column names *** |  |
| COMMENT |  |  |
| COMMENT |  |  |
| COMMENT |  *** Column formats *** |  |
| COMMENT |  |  |

##### Binary Table Caption for HDU5
Name | Type | Unit | Description |
| --- | --- | --- | --- |
 | OBJID | int32[5] |  | Unique object id from SDSS imaging (run,rerun,camCol,field,id) |
 | HOLETYPE | char[6] |  | Hole ID in which the positioner is sitting |
 | RA | float64 | deg | Calculated on sky fiber RA including delta_RA |
 | DEC | float64 | deg | Calculated on sky fiber Dec including delta_DEC |
 | MAG | float32[5] |  | [u, g, r, i, z] optical magnitudes |
 | STARL | float32 |  | likelihood object is star (0-1, Plate OBJECT holes only) |
 | EXPL | float32 |  | likelihood object is exponential disk (0-1, Plate OBJECT holes only) |
 | DEVAUCL | float32 |  | likelihood object is deVaucouleurs profile (0-1, Plate OBJECT holes only) |
 | OBJTYPE | char[16] |  | Why object was targetted (QSO = Science Target) |
 | XFOCAL | float64 |  | Hole x-axis position in focal plane per exposure |
 | YFOCAL | float64 |  | Hole y-axis position in focal plane per exposure |
 | SPECTROGRAPHID | int32 |  | Spectrograph to which the fibre is assigned. (SDSS-V: 1 = BOSS, 2 = APOGEE) or (SDSS-IV: 1=BOSS SP1, 2=BOSS SP2) |
 | FIBERID | int32 |  | Fiber ID of target |
 | THROUGHPUT | int32 |  | Plate Fiber throughput (0-65535, 0=no light) |
 | PRIMTARGET | int32 |  | Plate Primary target flags |
 | SECTARGET | int32 |  | Plate Secondary target flags |
 | OFFSETID | int32 |  | plate offset associated; 0 = primary pointing |
 | SCI_EXPTIME | float32 | s | Rescaled Science Exposure Time for offset plate |
 | SOURCETYPE | char[21] |  | indicate the nature of the source, one of STAR, QSO, GALAXY, or NA |
 | LAMBDA_EFF | float32 | AA | Wavelength used for coordinate transformations |
 | ZOFFSET | float32 | micron | backstopping offset distance (from washers) |
 | BLUEFIBER | int32 |  | BOSS to assign this target a 'blue' fiber |
 | BOSS_TARGET1 | int64 |  | Targeting bitmask for SDSS-III BOSS |
 | BOSS_TARGET2 | int64 |  | Targeting bitmask for SDSS-III BOSS |
 | ANCILLARY_TARGET1 | int64 |  | Targeting bitmask for SDSS-III BOSS Ancillary |
 | ANCILLARY_TARGET2 | int64 |  | Targeting bitmask for SDSS-III BOSS Ancillary |
 | RUN | int32 |  | SDSS imaging run, for SDSS imaging targets |
 | RERUN | char[4] |  | SDSS imaging rerun, for SDSS imaging targets |
 | CAMCOL | int32 |  | SDSS imaging camcol, for SDSS imaging targets |
 | FIELD | int32 |  | SDSS imaging field, for SDSS imaging targets |
 | ID | int32 |  | SDSS imaging id, for SDSS imaging targets |
 | CALIBFLUX | float32[5] |  | SDSS band [u,g,r,i,z] target calibration flux |
 | CALIBFLUX_IVAR | float32[5] |  | target calibration flux inverse variance |
 | CALIB_STATUS | int32[5] |  | target calibration status flag |
 | SFD_EBV | float32 |  | SFD reddening |



### HDU6: SKY
subtracted sky flux

#### HDU Type: IMAGE
#### HDU Size:  17 MB

##### Header Table Caption for HDU6
Key | Value | Comment | |
| --- | --- | --- | --- |
| XTENSION | IMAGE | Image Extension created by MWRFITS v1.11 |
| BITPIX | -32 |  |
| NAXIS | 2 |  |
| NAXIS1 | 4646 |  |
| NAXIS2 | 1000 |  |
| EXTNAME | SKY | Subtracted sky flux |
| PCOUNT | 0 |  |
| GCOUNT | 1 |  |



---
## Notes
None

---
## Regrets
I have no regrets!