# Data Model: mos_target_bhm_spiders_agn_superset


MOS Target table: mos_target_bhm_spiders_agn_superset


## Contents
- [Basic Information](#basic-information)
- [Changelog](#changelog)
- [Example HDUS List](#example-hdus-list)
- [Notes](#notes)
- [Regrets](#regrets)
---

## Basic Information
One of several tables describing optical/IR counterparts to eROSITA X-ray sources identified via various methods.  These tables contain a superset of potential targets from which the SDSS-V spectroscopic targets were drawn.  The dr19_bhm_spiders_agn_superset table includes is expected to be dominated by Active Galactic Nuclei (AGN) but should also include a significant minority of galaxies, stars and other Galactic sources. Each row corresponds to one possible match between an X-ray source and a potential optical/IR counterpart.  The X-ray columns (ero_*) record the eROSITA information known at the time of target selection and may differ from publicly available eROSITA catalogs. The dr19_bhm_spiders_*_superset tables are derived from eROSITA observations of the eROSITA Final Equatorial Depth performance verification field ('eFEDS').

### Naming Convention
$MOS_TARGET/[V_TARG]/mos_bhm_spiders_agn_superset.fits, where V_TARG=1.0.2 for DR19

### Releases
DR19

### Enviroments
MOS_TARGET

### Approximate Size
4 MB

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
MOS Target table: mos_target_bhm_spiders_agn_superset

#### HDU Type: BINARY TABLE
#### HDU Size:  4 MB

##### Header Table Caption for HDU1
Key | Value | Comment | |
| --- | --- | --- | --- |
| XTENSION | BINTABLE | binary table extension |
| BITPIX | 8 | array data type |
| NAXIS | 2 | number of array dimensions |
| NAXIS1 | 258 | length of dimension 1 |
| NAXIS2 | 18079 | length of dimension 2 |
| PCOUNT | 0 | number of group parameters |
| GCOUNT | 1 | number of groups |
| TFIELDS | 40 | number of table fields |
| TNULL1 | -9223372036854775808 |  |
| TNULL17 | -9223372036854775808 |  |
| TNULL19 | -2147483648 |  |
| TNULL20 | -2147483648 |  |
| TNULL22 | -9223372036854775808 |  |
| TNULL23 | -9223372036854775808 |  |
| TNULL24 | -9223372036854775808 |  |
| TNULL26 | -9223372036854775808 |  |
| TNULL27 | -9223372036854775808 |  |

##### Binary Table Caption for HDU1
Name | Type | Unit | Description |
| --- | --- | --- | --- |
 | pk | int64 |  | primary key of table entry |
 | ero_version | char[14] |  | Identifier giving the eROSITA dataset and processing version e.g. 'eFEDS_c940', 'em01_c946_201008_poscorr' etc |
 | ero_detuid | char[28] |  | The standard official eROSITA unique detection identifier, e.g. 'em01_123456_020_ML12345_001_c946' etc |
 | ero_flux | float32 | erg/cm2/s | X-ray flux, usually in the main eROSITA detection band (0.2-2.3keV). |
 | ero_flux_err | float32 | erg/cm2/s | Uncertainty on X-ray flux |
 | ero_ext | float32 | arcsec | X-ray extent parameter |
 | ero_ext_err | float32 | arcsec | Uncertainty on X-ray extent parameter |
 | ero_ext_like | float32 |  | Likelihood of X-ray source being extended |
 | ero_det_like | float32 |  | X-ray detection likelihood |
 | ero_ra | float64 | deg | Best determination of X-ray position, J2000 |
 | ero_dec | float64 | deg | Best determination of X-ray position, J2000 |
 | ero_radec_err | float32 | arcsec | Best estimate of X-ray position uncertainty |
 | xmatch_method | char[11] |  | The X-ray-to-optical/IR cross-match method that was used in this case e.g. 'XPS-ML/NWAY', 'CLUSTERS_EFEDS_MULTIPLE' etc |
 | xmatch_version | char[15] |  | The cross-match software version and OIR catalog used e.g. 'LSdr8-JWMS_v2.1LSdr8-JWMS_v2.1', 'LSdr8-AG_v1,JC_16032020', 'eromapper_2020-10-12', 'CW20ps1dr2-v011220' etc |
 | xmatch_dist | float32 | arcsec | Distance between X-ray position and optical counterpart |
 | xmatch_metric | float32 |  | Metric giving quality of cross-match. Meaning is dependent on xmatch_method, e.g. p_any for NWAY |
 | xmatch_flags | int64 |  | Flags indicating cross-match properties (e.g. status flags), xmatch_method dependent |
 | target_class | char[7] |  | Best guess of source classification at time of xmatch e.g. 'GALAXY','STAR','QSO','UNKNOWN',.... |
 | target_priority | int32 |  | Relative to other targets in this catalog, interpreted/adapted later to derive a final target priority |
 | target_has_spec | int32 |  | Flags used to indicate if target has good quality archival spectroscopy available |
 | best_opt | char[6] |  | Describes which OIR survey provided the optical counterpart for this row of the table, i.e. which OIR cat gives the entries in fields opt_ra, opt_dec, opt_pmra, opt_pmdec, opt_epoch, and which OIR identifier is given in the *_id columns |
 | ls_id | int64 |  | Identifier of counterpart (if any) in dr19_legacy_survey_dr8 ('ls_id' field). Arithmetically derived from legacysurvey sweep file columns: release, brickid and objid:  ls_id = objid + (brickid * 2**16) + (release * 2**40) |
 | ps1_dr2_objid | int64 |  | Identifier of counterpart (if any) in dr19_panstarrs1 (catid_objid field). Identical to MAST 'ippObjID' identifier |
 | gaia_dr2_source_id | int64 |  | Identifier of counterpart (if any) in dr19_gaia_dr2_source ('source_id' field) |
 | unwise_dr1_objid | char[1] |  | Identifier of counterpart (if any) in dr19_unwise (not used) |
 | des_dr1_coadd_object_id | int64 |  | Identifier of counterpart (if any) in DES/dr1 coadd catalogg (not used) |
 | sdss_dr16_objid | int64 |  | Identifier of counterpart (if any) in SDSS dr16 photobj table (not used) |
 | opt_ra | float64 | deg | Sky coordinate of optical/IR counterpart, included for validity checks only |
 | opt_dec | float64 | deg | Sky coordinate of optical/IR counterpart, included for validity checks only |
 | opt_pmra | float32 | mas/yr | Proper motion of optical/IR counterpart, included for validity checks only |
 | opt_pmdec | float32 | mas/yr | Proper motion of optical/IR counterpart, included for validity checks only |
 | opt_epoch | float32 | decimal year | Epoch of opt_ra,opt_dec |
 | opt_modelflux_g | float32 | nanomaggy | optical magnitude of counterpart, included for validity checks only |
 | opt_modelflux_ivar_g | float32 | 1/nanomaggy^2 | uncertainty on optical magnitude of counterpart, included for validity checks only |
 | opt_modelflux_r | float32 | nanomaggy | optical magnitude of counterpart, included for validity checks only |
 | opt_modelflux_ivar_r | float32 | 1/nanomaggy^2 | uncertainty on optical magnitude of counterpart, included for validity checks only |
 | opt_modelflux_i | float32 | nanomaggy | optical magnitude of counterpart, included for validity checks only |
 | opt_modelflux_ivar_i | float32 | 1/nanomaggy^2 | uncertainty on optical magnitude of counterpart, included for validity checks only |
 | opt_modelflux_z | float32 | nanomaggy | optical magnitude of counterpart, included for validity checks only |
 | opt_modelflux_ivar_z | float32 | 1/nanomaggy^2 | uncertainty on optical magnitude of counterpart, included for validity checks only |



---
## Notes
None

---
## Regrets
I  have no regrets!