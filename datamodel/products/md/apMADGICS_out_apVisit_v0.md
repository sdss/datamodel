# Data Model: apMADGICS_out_apVisit_v0


Output spectrum from apMADGICS most analogous to classical apVisit spectra


## Contents
- [Basic Information](#basic-information)
- [Changelog](#changelog)
- [Example HDFS List](#example-hdfs-list)
- [Notes](#notes)
- [Regrets](#regrets)
---

## Basic Information
Output spectrum from apMADGICS in the observational restframe, on a common log-spaced wavelength grid, having done sky subtraction, telluric absorption division, and transfer function correction (using the maximum likelihood value from a full posterior).

### Naming Convention
APMADGICS/[VERS]/outdir_wu_[STAR_PRIOR_TYPE]/apMADGICS_out_apVisit_v0.h5 where VERS = "v2024_03_16" for DR19 and STAR_PRIOR_TYPE has one of the values ["th", "dd"]

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
  - [apVisit_v0](#apVisit_v0)
  - [hdr](#hdr)

---

## Changelog
DR19 is the first release of apMADGICS

---
## Example HDFS List

### Top Level

**Name:** /\
**Parent:**  /\
**Description:** MADGICS spectrum output file\
**Type:** group\
**Number of Members:**  2



### Members


### apVisit_v0

**Name:** apVisit_v0\
**Parent:**  /\
**Description:** Output spectrum from apMADGICS (most analogous to classical apVisit spectra) in the observational restframe, on a common log-spaced wavelength grid, having done sky subtraction, telluric absorption division, and transfer function correction (using the maximum likelihood value from a full posterior).\
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
| git_branch | b'2024_03_16' | name of the git_branch of apMADGICS that produced these set of component spectra | \|S10 |
| git_commit | b'9035b0626e8eb53a5a06de5be462603ae5574e82' | git commit hash to specify the exact version of the apMADGICS.jl code that produced these set of component spectra | \|S40 |
| pipeline | b'apMADGICS.jl' | name of the codebase that produced these component spectra | \|S12 |


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