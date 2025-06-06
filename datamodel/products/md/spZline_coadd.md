# Data Model: spZline_coadd


Contains a summary of the Spectro-1D spZline output for custom coadded spectra.


## Contents
- [Basic Information](#basic-information)
- [Changelog](#changelog)
- [Example HDUS List](#example-hdus-list)
- [Notes](#notes)

---

## Basic Information
Contains a summary of the Spectro-1D spZline output for custom coadded spectra with line measurements

### Naming Convention
$BOSS_SPECTRO_REDUX/[RUN2D]/[COADD]/[RUN1D]/spZline-[COADD]-[MJD].fits

### Releases
IPL3, DR19

### Enviroments
BOSS_SPECTRO_REDUX

### Approximate Size
8 MB

### File Type
FITS

### Generated by Product
idlspec2d

### Is a VAC
False

### HDUS List for release DR19
  - [HDU0: PRIMARY](#hdu0-primary)
  - [HDU1: ](#hdu1-)
  - [HDU2: ](#hdu2-)

---

## Changelog
Describes changes to the datamodel product and/or file structure from one release to another
 - DR19
   - from: IPL3
   - note: No changes

---
## Example HDUS List

### HDU0: PRIMARY


#### HDU Type: IMAGE
#### HDU Size:  0 bytes

##### Header Table Caption for HDU0
Key | Value | Comment | |
| --- | --- | --- | --- |
| SIMPLE | True | Primary Header created by MWRFITS v1.13 |
| BITPIX | 16 |  |
| NAXIS | 0 |  |
| EXTEND | True | Extensions may be present |
| COEFF0 | 3.5523 | Central wavelength (log10) of first pixel |
| COEFF1 | 0.0001 | Log10 dispersion per pixel |
| CRVAL1 | 3.5523 | Central wavelength (log10) of first pixel |
| CD1_1 | 0.0001 | Log10 dispersion per pixel |
| CRPIX1 | 1 | Starting pixel (1-indexed) |
| CTYPE1 | LINEAR |  |
| MJD | 60000 | Modified Julian Date |
| RUNMJD | 60407 | Modified Julian Date of RUN |
| RUN2D | v6_1_3 | IDLSpec2D Run2d |
| RUN1D | v6_1_3 | Spectro-1D reduction name |
| VERS1D | v6_1_3 | Version of idlspec2d for 1D reduction |
| VERSLINE | v6_1_3 | Version of idlspec2d for line fitting |
| TILEID |  | Tile ID for SDSS BOSS plates (-1 for SDSS) |
| MOON_FRA | 0.270368403284 | Moon Phase |
| SPEC1_G | 6.62995 | (S/N)^2 for spec  1 at mag 21.20 |
| SN2EXT1G | 6.62995 | Extinction corrected (S/N)^2 |
| SPEC1_R | 21.791 | (S/N)^2 for spec  1 at mag 20.20 |
| SN2EXT1R | 21.791 | Extinction corrected (S/N)^2 |
| SPEC1_I | 16.2032 | (S/N)^2 for spec  1 at mag 20.20 |
| SN2EXT1I | 16.2032 | Extinction corrected (S/N)^2 |
| NGAL | 359 | Number of (good) main galaxies |
| GOFFGAL | 0.0602238311768 | Spectrophoto offset for main galaxies in G-band |
| GRMSGAL | 0.358758642181 | Spectrophoto RMS for main galaxies in G-band |
| ROFFGAL | 0.0581752210299 | Spectrophoto offset for main galaxies in R-band |
| RRMSGAL | 0.339271579636 | Spectrophoto RMS for main galaxies in R-band |
| IOFFGAL | 0.10673924994 | Spectrophoto offset for main galaxies in I-band |
| IRMSGAL | 0.382877112938 | Spectrophoto RMS for main galaxies in I-band |
| GROFFGAL | 0.00221052551269 | Spectrophoto offset for main galaxies in (GR) |
| GRRMSGAL | 0.230922157945 | Spectrophoto RMS for main galaxies in (GR) |
| RIOFFGAL | -0.0356044439901 | Spectrophoto offset for main galaxies in (RI) |
| RIRMSGAL | 0.161101424416 | Spectrophoto RMS for main galaxies in (RI) |
| UNAME | notch283 |  |
| CHOP_MIN | 3600.0 |  |
| CHOP_MAX | 10400.0 |  |
| DIMS0 | 32 | Number of emission lines |
| DIMS1 | 413 | Number of objects |



### HDU1: 
Line fitting metadata

#### HDU Type: BINARY TABLE
#### HDU Size:  1 MB

##### Header Table Caption for HDU1
Key | Value | Comment | |
| --- | --- | --- | --- |
| XTENSION | BINTABLE | Binary table written by MWRFITS v1.13 |
| BITPIX | 8 | Required value |
| NAXIS | 2 | Required value |
| NAXIS1 | 105 | Number of bytes per row |
| NAXIS2 | 13216 | Number of rows |
| PCOUNT | 0 | Normally 0 (no varying arrays) |
| GCOUNT | 1 | Required value |
| TFIELDS | 21 | Number of columns in table |
| COMMENT |  |  |
| COMMENT |  *** End of mandatory fields *** |  |
| COMMENT |  |  |
| COMMENT |  |  |
| COMMENT |  *** Column formats *** |  |
| COMMENT |  |  |
| COMMENT |  |  |
| COMMENT |  *** Column names *** |  |
| COMMENT |  |  |

##### Binary Table Caption for HDU1
Name | Type | Unit | Description |
| --- | --- | --- | --- |
 | FIELD | int64 |  | SDSS FieldID (plateID for plate era data) |
 | MJD | int64 |  | Modified Julian date of observation |
 | TARGET_INDEX | int64 |  | Target Index (1 to number of targets) |
 | CATALOGID | int64 |  | SDSS-V CatalogID used in naming |
 | SDSS_ID | int64 |  | Unified SDSS Target Identifier |
 | LINENAME | char[13] |  | Line name |
 | LINEWAVE | float64 |  | Catalog wavelength of line in vacuum Angstroms |
 | LINEZ | float32 |  | Redshift |
 | LINEZ_ERR | float32 |  | Redshift error (negative for invalid fit) |
 | LINESIGMA | float32 | km/s | Gaussian width in km/sec |
 | LINESIGMA_ERR | float32 |  | Gaussian width error (<0 for invalid fit) |
 | LINEAREA | float32 | nanomaggy*AA | Area in gaussian fit [(flux-units) * Ang] |
 | LINEAREA_ERR | float32 | nanomaggy*AA | Flux error (negative for invalid fit) |
 | LINEEW | float32 | AA | equivalent width |
 | LINEEW_ERR | float32 | AA | Equivalent width error (<0 for invalid fit) |
 | LINECONTLEVEL | float32 |  | Continuum level at line center |
 | LINECONTLEVEL_ERR | float32 |  | Error in continuum level at line center |
 | LINENPIXLEFT | int32 |  | Npixels to -3 sigma with INVVAR > 0 |
 | LINENPIXRIGHT | int32 |  | Npixels to +3 sigma with INVVAR > 0 |
 | LINEDOF | float32 |  | DOF in fit |
 | LINECHI2 | float32 |  | chi2 for all points in 3 sigma of line center |



### HDU2: 
Best-fit absorption-line spectrum, with line fits added in.

#### HDU Type: IMAGE
#### HDU Size:  7 MB

##### Header Table Caption for HDU2
Key | Value | Comment | |
| --- | --- | --- | --- |
| XTENSION | IMAGE | Image Extension created by MWRFITS v1.13 |
| BITPIX | -32 |  |
| NAXIS | 2 |  |
| NAXIS1 | 4648 |  |
| NAXIS2 | 413 |  |
| PCOUNT | 0 |  |
| GCOUNT | 1 |  |



---
## Notes
None