# Data Model: apMADGICS_out_flux


Independent combinations of flux or fluxerr from APOGEE exposures used as visit input for apMADGICS


## Contents
- [Basic Information](#basic-information)
- [Changelog](#changelog)
- [Example HDFS List](#example-hdfs-list)
- [Notes](#notes)
- [Regrets](#regrets)
---

## Basic Information
Independent combinations of flux or fluxerr from APOGEE exposures used as visit input for apMADGICS. Uses a Lanczos interpolation kernel the switches to linear around masked pixels.

### Naming Convention
$APMADGICS/[VERS]/outdir_wu_[STAR_PRIOR_TYPE]/apMADGICS_out_flux[FLUX_TYPE].h5 where VERS = "v2024_03_16" for DR19, STAR_PRIOR_TYPE has one of the values ["th", "dd"], and FLUX_TYPE is either empty of "err2".

### Releases
DR19

### Enviroments
APMADGICS

### Approximate Size
171 GB

### File Type
H5

### Generated by Product
https://github.com/andrew-saydjari/apMADGICS.jl

### Is a VAC
False

### Data Level
3.3.0

### HDFS List for release DR19
  - [top](#top-level)
  - [flux](#flux)
  - [hdr](#hdr)

---

## Changelog
DR19 is the first release of apMADGICS

---
## Example HDFS List

### Top Level

**Name:** /\
**Parent:**  /\
**Description:** MADGICS spectrum input file\
**Type:** group\
**Number of Members:**  2



### Members


### flux

**Name:** flux{flux_type}\
**Parent:**  /\
**Description:** Independent combinations of flux or fluxerr from APOGEE exposures used as visit input for apMADGICS. Uses a Lanczos interpolation kernel the switches to linear around masked pixels. The inputs are stored as an array that is number of visits by number of wavelength bins.\
**Type:** dataset



**Ndim:** 2\
**Shape:** (2641032, 8700)\
**Size:** 22976978400\
**Dtype:** float64\
**Nbytes:** 183815827200


### hdr

**Name:** hdr\
**Parent:**  /\
**Description:** header dataset used to hold global attributes of the file\
**Type:** dataset

**Attributes**
Key | Value | Comment | Type |
| --- | --- | --- | --- |
| git_branch | b'2024_03_16' | name of the git_branch of apMADGICS that produced these spectra | \|S10 |
| git_commit | b'9035b0626e8eb53a5a06de5be462603ae5574e82' | git commit hash to specify the exact version of the apMADGICS.jl code that produced these spectra | \|S40 |
| pipeline | b'apMADGICS.jl' | name of the codebase that produced these spectra | \|S12 |


**Ndim:** 0\
**Shape:** ()\
**Size:** 1\
**Dtype:** |S21\
**Nbytes:** 21



---
## Notes
None

---
## Regrets
I  have no regrets!