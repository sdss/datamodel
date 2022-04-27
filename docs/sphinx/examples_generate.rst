
.. _examples:

Examples
========

Here are examples of generating datamodels for different supported filetypes.

.. tab:: FITS

    the common FITS standard astronomy file format

    **File Info**

    A MaNGA RSS FITS file

    - **Example**: $MANGA_SPECTRO_REDUX/v2_4_3/8485/stack/manga-8485-1901-LOGRSS.fits.gz
    - **File Species**: mangaRss
    - **Abstract Path**: MANGA_SPECTRO_REDUX/{drpver}/{plate}/stack/manga-{plate}-{ifu}-{wave}RSS.fits.gz
    - **Example Keys**: plate=8485; ifu=1901; drpver=v2_4_3; wave=LOG

    **Generate Commands**

    Command-line and Python commands to generate a datamodel

    .. tab:: CLI

        .. code-block:: console

            $ datamodel generate -f mangaRss \
            -p MANGA_SPECTRO_REDUX/{drpver}/{plate}/stack/manga-{plate}-{ifu}-{wave}RSS.fits.gz \
            -k plate=8485 -k ifu=1901 -k drpver=v2_4_3 -k wave=LOG -r DR15

    .. tab:: Python

        .. code-block:: python

            # define the inputs 
            file_species = "mangaRss"
            path = "MANGA_SPECTRO_REDUX/{drpver}/{plate}/stack/manga-{plate}-{ifu}-{wave}RSS.fits.gz"
            keys = ['plate=8485', 'ifu=1901', 'drpver=v2_4_3', 'wave=LOG']

            # generate a datamodel for Data Release 15 (DR15)
            dm = DataModel(file_spec=file_species, path=path, keywords=keys, release='DR15')
            dm.write_stubs()

    **Yaml Output**

    The generated output yaml datamodel stub

    .. code-block:: yaml

        general:
          name: mangaRss
          short: this is a manga rss
          description: longer description
          datatype: FITS
          filesize: 14 MB
          releases:
          - DR15
          environments:
          - MANGA_SPECTRO_REDUX
          naming_convention: $MANGA_SPECTRO_REDUX/[DRPVER]/[PLATE]/stack/manga-[PLATE]-[IFU]-[WAVE]RSS.fits.gz
          generated_by: mangadrp
        changelog:
          description: this changelog describes changes to the datamodel product and/or file
            structure
          releases: {}
        releases:
          DR15:
            template: $MANGA_SPECTRO_REDUX/[DRPVER]/[PLATE]/stack/manga-[PLATE]-[IFU]-[WAVE]RSS.fits.gz
            example: v2_4_3/8485/stack/manga-8485-1901-LOGRSS.fits.gz
            location: '{drpver}/{plate}/stack/manga-{plate}-{ifu}-{wave}RSS.fits.gz'
            environment: MANGA_SPECTRO_REDUX
            access:
              in_sdss_access: true
              path_name: mangarss
              path_template: $MANGA_SPECTRO_REDUX/{drpver}/{plate}/stack/manga-{plate}-{ifu}-{wave}RSS.fits.gz
              path_kwargs:
              - plate
              - drpver
              - wave
              - ifu
              access_string: mangaRss = $MANGA_SPECTRO_REDUX/{drpver}/{plate}/stack/manga-{plate}-{ifu}-{wave}RSS.fits.gz
            hdus:
              hdu0:
                name: PRIMARY
                description: description of the HDU extension
                is_image: true
                size: 0 bytes
                header:
                - key: SIMPLE
                  value: true
                  comment: ''
                - key: BITPIX
                  value: 8
                  comment: ''
                - key: NAXIS
                  value: 0
                  comment: ''
                - key: EXTEND
                  value: true
                  comment: ''
                - key: AUTHOR
                  value: Brian Cherinka & David Law <bcherin1@jhu.edu, dlaw@stsci.edu>
                  comment: ''
                - key: VERSDRP2
                  value: v2_4_3
                  comment: MaNGA DRP version (2d processing)
                - key: VERSDRP3
                  value: v2_4_3
                  comment: MaNGA DRP Version (3d processing)
                - key: VERSPLDS
                  value: v2_52
                  comment: Platedesign Version
                - key: VERSFLAT
                  value: v1_31
                  comment: Specflat Version
                - key: VERSCORE
                  value: v1_6_2
                  comment: MaNGAcore Version
                - key: VERSPRIM
                  value: v2_5
                  comment: MaNGA Preimaging Version
                - key: VERSUTIL
                  value: v5_5_32
                  comment: Version of idlutils
                - key: VERSIDL
                  value: x86_64 linux unix linux 7.1.1 Aug 21 2009 64 64
                  comment: Version of IDL
                - key: BSCALE
                  value: 1.0
                  comment: Intensity unit scaling
                - key: BZERO
                  value: 0.0
                  comment: Intensity zeropoint
                - key: BUNIT
                  value: 1E-17 erg/s/cm^2/Ang/fiber
                  comment: Specific intensity (per fiber-area)
                - key: MASKNAME
                  value: MANGA_DRP2PIXMASK
                  comment: Bits in sdssMaskbits.par used by mask extension
                - key: TELESCOP
                  value: SDSS 2.5-M
                  comment: Sloan Digital Sky Survey
                - key: INSTRUME
                  value: MaNGA
                  comment: SDSS-IV MaNGA IFU
                - key: SRVYMODE
                  value: MaNGA dither
                  comment: Survey leading this observation and its mode
                - key: PLATETYP
                  value: APOGEE-2&MaNGA
                  comment: Type of plate (e.g. MANGA, APOGEE-2&MANGA)
                - key: OBJSYS
                  value: ICRS
                  comment: The TCC objSys
                - key: EQUINOX
                  value: 2000.0
                  comment: ''
                - key: RADESYS
                  value: FK5
                  comment: ''
                - key: LAMPLIST
                  value: lamphgcdne.dat
                  comment: ''
                - key: TPLDATA
                  value: BOSZ_3000-11000A.fits
                  comment: ''
                - key: NEXP
                  value: 9
                  comment: Total number of exposures
                - key: EXPTIME
                  value: 8100.87
                  comment: Total exposure time (seconds)
                - key: BLUESN2
                  value: 19.9834
                  comment: Total SN2 in blue channel
                - key: REDSN2
                  value: 42.7417
                  comment: Total SN2 in red channel
                - key: AIRMSMIN
                  value: 1.03987
                  comment: Minimum airmass
                - key: AIRMSMED
                  value: 1.04708
                  comment: Median airmass
                - key: AIRMSMAX
                  value: 1.08221
                  comment: Maximum airmass
                - key: SEEMIN
                  value: 1.1779
                  comment: Best guider seeing
                - key: SEEMED
                  value: 1.30425
                  comment: Median guider seeing
                - key: SEEMAX
                  value: 1.42179
                  comment: Worst guider seeing
                - key: TRANSMIN
                  value: 0.802254
                  comment: Worst guider transparency
                - key: TRANSMED
                  value: 0.831209
                  comment: Median guider transparency
                - key: TRANSMAX
                  value: 0.839501
                  comment: Best guider transparency
                - key: MJDMIN
                  value: 57132
                  comment: MJD of first exposure
                - key: MJDMED
                  value: 57132
                  comment: MJD of median exposure
                - key: MJDMAX
                  value: 57132
                  comment: MJD of last exposure
                - key: DATE-OBS
                  value: '2015-04-20'
                  comment: Date of median exposure
                - key: MJDRED
                  value: 58198
                  comment: MJD of the reduction
                - key: DATERED
                  value: '2018-03-21'
                  comment: Date of the reduction
                - key: MNGTARG1
                  value: 2336
                  comment: manga_target1 maskbit
                - key: MNGTARG2
                  value: 0
                  comment: manga_target2 maskbit
                - key: MNGTARG3
                  value: 0
                  comment: manga_target3 maskbit
                - key: IFURA
                  value: 232.5447
                  comment: IFU R.A. (J2000 deg.)
                - key: IFUDEC
                  value: 48.690201
                  comment: IFU Dec. (J2000 deg.)
                - key: OBJRA
                  value: 232.544703894
                  comment: Object R.A. (J2000 deg.)
                - key: OBJDEC
                  value: 48.6902009334
                  comment: Object Dec. (J2000 deg.)
                - key: CENRA
                  value: 234.06426
                  comment: Plate center R.A. (J2000 deg.)
                - key: CENDEC
                  value: 48.589874
                  comment: Plate center Dec. (J2000 deg.)
                - key: PLATEID
                  value: 8485
                  comment: Current plate
                - key: DESIGNID
                  value: 8980
                  comment: Current design
                - key: IFUDSGN
                  value: 1901
                  comment: ifuDesign
                - key: FRLPLUG
                  value: 29
                  comment: Plugged ferrule
                - key: PLATEIFU
                  value: 8485-1901
                  comment: PLATEID-ifuDesign
                - key: CARTID
                  value: '3'
                  comment: Cart(s) used
                - key: HARNAME
                  value: ma060
                  comment: Harness name(s)
                - key: METFILE
                  value: ma060-56887-1.par
                  comment: IFU metrology file(s)
                - key: MANGAID
                  value: 1-209232
                  comment: MaNGA ID number
                - key: CATIDNUM
                  value: '1'
                  comment: Primary target input catalog
                - key: PLTTARG
                  value: plateTargets-1.par
                  comment: plateTarget reference file
                - key: DRP3QUAL
                  value: 0
                  comment: DRP-3d quality bitmask
                - key: IFUGLON
                  value: 78.9550411299
                  comment: IFU Galactic longitude (deg)
                - key: IFUGLAT
                  value: 52.6212190954
                  comment: IFU Galactic latitude (deg)
                - key: EBVGAL
                  value: 0.0144335
                  comment: Galactic reddening E(B-V)
                - key: DATASUM
                  value: '0'
                  comment: data unit checksum updated 2018-03-21T06:08:46
                - key: CHECKSUM
                  value: YG5FZ949YE4EY949
                  comment: HDU checksum updated 2018-03-21T06:08:46
              hdu1:
                name: FLUX
                description: description of the HDU extension
                is_image: true
                size: 2 MB
                header:
                - key: XTENSION
                  value: IMAGE
                  comment: IMAGE extension
                - key: BITPIX
                  value: -32
                  comment: Number of bits per data pixel
                - key: NAXIS
                  value: 2
                  comment: Number of data axes
                - key: NAXIS1
                  value: 4563
                  comment: ''
                - key: NAXIS2
                  value: 171
                  comment: ''
                - key: PCOUNT
                  value: 0
                  comment: No Group Parameters
                - key: GCOUNT
                  value: 1
                  comment: One Data Group
                - key: AUTHOR
                  value: Brian Cherinka & David Law <bcherin1@jhu.edu, dlaw@stsci.edu>
                  comment: ''
                - key: VERSDRP2
                  value: v2_4_3
                  comment: MaNGA DRP version (2d processing)
                - key: VERSDRP3
                  value: v2_4_3
                  comment: MaNGA DRP Version (3d processing)
                - key: VERSPLDS
                  value: v2_52
                  comment: Platedesign Version
                - key: VERSFLAT
                  value: v1_31
                  comment: Specflat Version
                - key: VERSCORE
                  value: v1_6_2
                  comment: MaNGAcore Version
                - key: VERSPRIM
                  value: v2_5
                  comment: MaNGA Preimaging Version
                - key: VERSUTIL
                  value: v5_5_32
                  comment: Version of idlutils
                - key: VERSIDL
                  value: x86_64 linux unix linux 7.1.1 Aug 21 2009 64 64
                  comment: Version of IDL
                - key: BSCALE
                  value: 1.0
                  comment: Intensity unit scaling
                - key: BZERO
                  value: 0.0
                  comment: Intensity zeropoint
                - key: BUNIT
                  value: 1E-17 erg/s/cm^2/Ang/fiber
                  comment: Specific intensity (per fiber-area)
                - key: MASKNAME
                  value: MANGA_DRP2PIXMASK
                  comment: Bits in sdssMaskbits.par used by mask extension
                - key: TELESCOP
                  value: SDSS 2.5-M
                  comment: Sloan Digital Sky Survey
                - key: INSTRUME
                  value: MaNGA
                  comment: SDSS-IV MaNGA IFU
                - key: SRVYMODE
                  value: MaNGA dither
                  comment: Survey leading this observation and its mode
                - key: PLATETYP
                  value: APOGEE-2&MaNGA
                  comment: Type of plate (e.g. MANGA, APOGEE-2&MANGA)
                - key: OBJSYS
                  value: ICRS
                  comment: The TCC objSys
                - key: EQUINOX
                  value: 2000.0
                  comment: ''
                - key: RADESYS
                  value: FK5
                  comment: ''
                - key: LAMPLIST
                  value: lamphgcdne.dat
                  comment: ''
                - key: TPLDATA
                  value: BOSZ_3000-11000A.fits
                  comment: ''
                - key: NEXP
                  value: 9
                  comment: Total number of exposures
                - key: EXPTIME
                  value: 8100.87
                  comment: Total exposure time (seconds)
                - key: BLUESN2
                  value: 19.9834
                  comment: Total SN2 in blue channel
                - key: REDSN2
                  value: 42.7417
                  comment: Total SN2 in red channel
                - key: AIRMSMIN
                  value: 1.03987
                  comment: Minimum airmass
                - key: AIRMSMED
                  value: 1.04708
                  comment: Median airmass
                - key: AIRMSMAX
                  value: 1.08221
                  comment: Maximum airmass
                - key: SEEMIN
                  value: 1.1779
                  comment: Best guider seeing
                - key: SEEMED
                  value: 1.30425
                  comment: Median guider seeing
                - key: SEEMAX
                  value: 1.42179
                  comment: Worst guider seeing
                - key: TRANSMIN
                  value: 0.802254
                  comment: Worst guider transparency
                - key: TRANSMED
                  value: 0.831209
                  comment: Median guider transparency
                - key: TRANSMAX
                  value: 0.839501
                  comment: Best guider transparency
                - key: MJDMIN
                  value: 57132
                  comment: MJD of first exposure
                - key: MJDMED
                  value: 57132
                  comment: MJD of median exposure
                - key: MJDMAX
                  value: 57132
                  comment: MJD of last exposure
                - key: DATE-OBS
                  value: '2015-04-20'
                  comment: Date of median exposure
                - key: MJDRED
                  value: 58198
                  comment: MJD of the reduction
                - key: DATERED
                  value: '2018-03-21'
                  comment: Date of the reduction
                - key: MNGTARG1
                  value: 2336
                  comment: manga_target1 maskbit
                - key: MNGTARG2
                  value: 0
                  comment: manga_target2 maskbit
                - key: MNGTARG3
                  value: 0
                  comment: manga_target3 maskbit
                - key: IFURA
                  value: 232.5447
                  comment: IFU R.A. (J2000 deg.)
                - key: IFUDEC
                  value: 48.690201
                  comment: IFU Dec. (J2000 deg.)
                - key: OBJRA
                  value: 232.544703894
                  comment: Object R.A. (J2000 deg.)
                - key: OBJDEC
                  value: 48.6902009334
                  comment: Object Dec. (J2000 deg.)
                - key: CENRA
                  value: 234.06426
                  comment: Plate center R.A. (J2000 deg.)
                - key: CENDEC
                  value: 48.589874
                  comment: Plate center Dec. (J2000 deg.)
                - key: PLATEID
                  value: 8485
                  comment: Current plate
                - key: DESIGNID
                  value: 8980
                  comment: Current design
                - key: IFUDSGN
                  value: 1901
                  comment: ifuDesign
                - key: FRLPLUG
                  value: 29
                  comment: Plugged ferrule
                - key: PLATEIFU
                  value: 8485-1901
                  comment: PLATEID-ifuDesign
                - key: CARTID
                  value: '3'
                  comment: Cart(s) used
                - key: HARNAME
                  value: ma060
                  comment: Harness name(s)
                - key: METFILE
                  value: ma060-56887-1.par
                  comment: IFU metrology file(s)
                - key: MANGAID
                  value: 1-209232
                  comment: MaNGA ID number
                - key: CATIDNUM
                  value: '1'
                  comment: Primary target input catalog
                - key: PLTTARG
                  value: plateTargets-1.par
                  comment: plateTarget reference file
                - key: DRP3QUAL
                  value: 0
                  comment: DRP-3d quality bitmask
                - key: IFUGLON
                  value: 78.9550411299
                  comment: IFU Galactic longitude (deg)
                - key: IFUGLAT
                  value: 52.6212190954
                  comment: IFU Galactic latitude (deg)
                - key: EBVGAL
                  value: 0.0144335
                  comment: Galactic reddening E(B-V)
                - key: CTYPE1
                  value: WAVE-LOG
                  comment: ''
                - key: CRPIX1
                  value: 1
                  comment: Starting pixel (1-indexed)
                - key: CRVAL1
                  value: 3621.59598486
                  comment: Central wavelength of first pixel
                - key: CD1_1
                  value: 0.833903304339
                  comment: Initial dispersion per pixel
                - key: CUNIT1
                  value: Angstrom
                  comment: ''
                - key: HDUCLASS
                  value: SDSS
                  comment: SDSS format class
                - key: HDUCLAS1
                  value: IMAGE
                  comment: ''
                - key: HDUCLAS2
                  value: DATA
                  comment: ''
                - key: ERRDATA
                  value: IVAR
                  comment: Error extension name
                - key: QUALDATA
                  value: MASK
                  comment: Mask extension name
                - key: EXTNAME
                  value: FLUX
                  comment: ''
                - key: DATASUM
                  value: '404143304'
                  comment: data unit checksum updated 2018-03-21T06:08:46
                - key: CHECKSUM
                  value: MZISMYFQMYFQMYFQ
                  comment: HDU checksum updated 2018-03-21T06:08:46
              hdu2:
                name: IVAR
                description: description of the HDU extension
                is_image: true
                size: 2 MB
                header:
                - key: XTENSION
                  value: IMAGE
                  comment: IMAGE extension
                - key: BITPIX
                  value: -32
                  comment: Number of bits per data pixel
                - key: NAXIS
                  value: 2
                  comment: Number of data axes
                - key: NAXIS1
                  value: 4563
                  comment: ''
                - key: NAXIS2
                  value: 171
                  comment: ''
                - key: PCOUNT
                  value: 0
                  comment: No Group Parameters
                - key: GCOUNT
                  value: 1
                  comment: One Data Group
                - key: HDUCLASS
                  value: SDSS
                  comment: SDSS format class
                - key: HDUCLAS1
                  value: IMAGE
                  comment: ''
                - key: HDUCLAS2
                  value: ERROR
                  comment: ''
                - key: HDUCLAS3
                  value: INVMSE
                  comment: Inverse variance
                - key: SCIDATA
                  value: FLUX
                  comment: Science extension name
                - key: QUALDATA
                  value: MASK
                  comment: Mask extension name
                - key: EXTNAME
                  value: IVAR
                  comment: ''
                - key: DATASUM
                  value: '1140307641'
                  comment: data unit checksum updated 2018-03-21T06:08:46
                - key: CHECKSUM
                  value: 6K5C9K396K3C6K39
                  comment: HDU checksum updated 2018-03-21T06:08:46
              hdu3:
                name: MASK
                description: description of the HDU extension
                is_image: true
                size: 2 MB
                header:
                - key: XTENSION
                  value: IMAGE
                  comment: IMAGE extension
                - key: BITPIX
                  value: 32
                  comment: Number of bits per data pixel
                - key: NAXIS
                  value: 2
                  comment: Number of data axes
                - key: NAXIS1
                  value: 4563
                  comment: ''
                - key: NAXIS2
                  value: 171
                  comment: ''
                - key: PCOUNT
                  value: 0
                  comment: No Group Parameters
                - key: GCOUNT
                  value: 1
                  comment: One Data Group
                - key: HDUCLASS
                  value: SDSS
                  comment: SDSS format class
                - key: HDUCLAS1
                  value: IMAGE
                  comment: ''
                - key: HDUCLAS2
                  value: QUALITY
                  comment: ''
                - key: HDUCLAS3
                  value: FLAG64BIT
                  comment: ''
                - key: SCIDATA
                  value: FLUX
                  comment: Science extension name
                - key: ERRDATA
                  value: IVAR
                  comment: Error extension name
                - key: EXTNAME
                  value: MASK
                  comment: ''
                - key: DATASUM
                  value: '2359936278'
                  comment: data unit checksum updated 2018-03-21T06:08:46
                - key: CHECKSUM
                  value: cbdRdabOcabOcabO
                  comment: HDU checksum updated 2018-03-21T06:08:46
              hdu4:
                name: DISP
                description: description of the HDU extension
                is_image: true
                size: 2 MB
                header:
                - key: XTENSION
                  value: IMAGE
                  comment: IMAGE extension
                - key: BITPIX
                  value: -32
                  comment: Number of bits per data pixel
                - key: NAXIS
                  value: 2
                  comment: Number of data axes
                - key: NAXIS1
                  value: 4563
                  comment: ''
                - key: NAXIS2
                  value: 171
                  comment: ''
                - key: PCOUNT
                  value: 0
                  comment: No Group Parameters
                - key: GCOUNT
                  value: 1
                  comment: One Data Group
                - key: EXTNAME
                  value: DISP
                  comment: ''
                - key: DATASUM
                  value: '2453379726'
                  comment: data unit checksum updated 2018-03-21T06:08:46
                - key: CHECKSUM
                  value: RAH2S3G2R9G2R9G2
                  comment: HDU checksum updated 2018-03-21T06:08:46
              hdu5:
                name: PREDISP
                description: description of the HDU extension
                is_image: true
                size: 2 MB
                header:
                - key: XTENSION
                  value: IMAGE
                  comment: IMAGE extension
                - key: BITPIX
                  value: -32
                  comment: Number of bits per data pixel
                - key: NAXIS
                  value: 2
                  comment: Number of data axes
                - key: NAXIS1
                  value: 4563
                  comment: ''
                - key: NAXIS2
                  value: 171
                  comment: ''
                - key: PCOUNT
                  value: 0
                  comment: No Group Parameters
                - key: GCOUNT
                  value: 1
                  comment: One Data Group
                - key: EXTNAME
                  value: PREDISP
                  comment: ''
                - key: DATASUM
                  value: '1425839999'
                  comment: data unit checksum updated 2018-03-21T06:08:46
                - key: CHECKSUM
                  value: FAP7F3O4FAO4F3O4
                  comment: HDU checksum updated 2018-03-21T06:08:46
              hdu6:
                name: WAVE
                description: description of the HDU extension
                is_image: true
                size: 35 KB
                header:
                - key: XTENSION
                  value: IMAGE
                  comment: IMAGE extension
                - key: BITPIX
                  value: -64
                  comment: Number of bits per data pixel
                - key: NAXIS
                  value: 1
                  comment: Number of data axes
                - key: NAXIS1
                  value: 4563
                  comment: ''
                - key: PCOUNT
                  value: 0
                  comment: No Group Parameters
                - key: GCOUNT
                  value: 1
                  comment: One Data Group
                - key: EXTNAME
                  value: WAVE
                  comment: ''
                - key: DATASUM
                  value: '3938867060'
                  comment: data unit checksum updated 2018-03-21T06:08:46
                - key: CHECKSUM
                  value: cL7TfJ5TcJ5TcJ5T
                  comment: HDU checksum updated 2018-03-21T06:08:46
              hdu7:
                name: SPECRES
                description: description of the HDU extension
                is_image: true
                size: 35 KB
                header:
                - key: XTENSION
                  value: IMAGE
                  comment: IMAGE extension
                - key: BITPIX
                  value: -64
                  comment: Number of bits per data pixel
                - key: NAXIS
                  value: 1
                  comment: Number of data axes
                - key: NAXIS1
                  value: 4563
                  comment: ''
                - key: PCOUNT
                  value: 0
                  comment: No Group Parameters
                - key: GCOUNT
                  value: 1
                  comment: One Data Group
                - key: EXTNAME
                  value: SPECRES
                  comment: ''
                - key: DATASUM
                  value: '1547448224'
                  comment: data unit checksum updated 2018-03-21T06:08:46
                - key: CHECKSUM
                  value: OcOcRaOZOaObOaOZ
                  comment: HDU checksum updated 2018-03-21T06:08:46
              hdu8:
                name: SPECRESD
                description: description of the HDU extension
                is_image: true
                size: 35 KB
                header:
                - key: XTENSION
                  value: IMAGE
                  comment: IMAGE extension
                - key: BITPIX
                  value: -64
                  comment: Number of bits per data pixel
                - key: NAXIS
                  value: 1
                  comment: Number of data axes
                - key: NAXIS1
                  value: 4563
                  comment: ''
                - key: PCOUNT
                  value: 0
                  comment: No Group Parameters
                - key: GCOUNT
                  value: 1
                  comment: One Data Group
                - key: EXTNAME
                  value: SPECRESD
                  comment: ''
                - key: DATASUM
                  value: '706612906'
                  comment: data unit checksum updated 2018-03-21T06:08:46
                - key: CHECKSUM
                  value: K3YcN3WZK3WbK3WZ
                  comment: HDU checksum updated 2018-03-21T06:08:46
              hdu9:
                name: PRESPECRES
                description: description of the HDU extension
                is_image: true
                size: 35 KB
                header:
                - key: XTENSION
                  value: IMAGE
                  comment: IMAGE extension
                - key: BITPIX
                  value: -64
                  comment: Number of bits per data pixel
                - key: NAXIS
                  value: 1
                  comment: Number of data axes
                - key: NAXIS1
                  value: 4563
                  comment: ''
                - key: PCOUNT
                  value: 0
                  comment: No Group Parameters
                - key: GCOUNT
                  value: 1
                  comment: One Data Group
                - key: EXTNAME
                  value: PRESPECRES
                  comment: ''
                - key: DATASUM
                  value: '2694726452'
                  comment: data unit checksum updated 2018-03-21T06:08:46
                - key: CHECKSUM
                  value: bD8IeD8IbD8IbD8I
                  comment: HDU checksum updated 2018-03-21T06:08:46
              hdu10:
                name: PRESPECRESD
                description: description of the HDU extension
                is_image: true
                size: 35 KB
                header:
                - key: XTENSION
                  value: IMAGE
                  comment: IMAGE extension
                - key: BITPIX
                  value: -64
                  comment: Number of bits per data pixel
                - key: NAXIS
                  value: 1
                  comment: Number of data axes
                - key: NAXIS1
                  value: 4563
                  comment: ''
                - key: PCOUNT
                  value: 0
                  comment: No Group Parameters
                - key: GCOUNT
                  value: 1
                  comment: One Data Group
                - key: EXTNAME
                  value: PRESPECRESD
                  comment: ''
                - key: DATASUM
                  value: '2908884265'
                  comment: data unit checksum updated 2018-03-21T06:08:46
                - key: CHECKSUM
                  value: eDDUe9BTeABTe9BT
                  comment: HDU checksum updated 2018-03-21T06:08:46
              hdu11:
                name: OBSINFO
                description: description of the HDU extension
                is_image: false
                size: 2 KB
                columns:
                  SLITFILE:
                    name: SLITFILE
                    type: char[25]
                    unit: this is the unit and description text
                    description: this is the unit and description text
                  METFILE:
                    name: METFILE
                    type: char[17]
                    unit: this is the unit and description text
                    description: this is the unit and description text
                  HARNAME:
                    name: HARNAME
                    type: char[5]
                    unit: this is the unit and description text
                    description: this is the unit and description text
                  IFUDESIGN:
                    name: IFUDESIGN
                    type: int32
                    unit: this is the unit and description text
                    description: this is the unit and description text
                  FRLPLUG:
                    name: FRLPLUG
                    type: int16
                    unit: this is the unit and description text
                    description: this is the unit and description text
                  MANGAID:
                    name: MANGAID
                    type: char[8]
                    unit: this is the unit and description text
                    description: this is the unit and description text
                  AIRTEMP:
                    name: AIRTEMP
                    type: float32
                    unit: this is the unit and description text
                    description: this is the unit and description text
                  HUMIDITY:
                    name: HUMIDITY
                    type: float32
                    unit: this is the unit and description text
                    description: this is the unit and description text
                  PRESSURE:
                    name: PRESSURE
                    type: float32
                    unit: this is the unit and description text
                    description: this is the unit and description text
                  SEEING:
                    name: SEEING
                    type: float32
                    unit: this is the unit and description text
                    description: this is the unit and description text
                  PSFFAC:
                    name: PSFFAC
                    type: float32
                    unit: this is the unit and description text
                    description: this is the unit and description text
                  TRANSPAR:
                    name: TRANSPAR
                    type: float32
                    unit: this is the unit and description text
                    description: this is the unit and description text
                  PLATEID:
                    name: PLATEID
                    type: int32
                    unit: this is the unit and description text
                    description: this is the unit and description text
                  DESIGNID:
                    name: DESIGNID
                    type: int32
                    unit: this is the unit and description text
                    description: this is the unit and description text
                  CARTID:
                    name: CARTID
                    type: int16
                    unit: this is the unit and description text
                    description: this is the unit and description text
                  MJD:
                    name: MJD
                    type: int32
                    unit: this is the unit and description text
                    description: this is the unit and description text
                  EXPTIME:
                    name: EXPTIME
                    type: float32
                    unit: this is the unit and description text
                    description: this is the unit and description text
                  EXPNUM:
                    name: EXPNUM
                    type: char[12]
                    unit: this is the unit and description text
                    description: this is the unit and description text
                  SET:
                    name: SET
                    type: int32
                    unit: this is the unit and description text
                    description: this is the unit and description text
                  MGDPOS:
                    name: MGDPOS
                    type: char[8]
                    unit: this is the unit and description text
                    description: this is the unit and description text
                  MGDRA:
                    name: MGDRA
                    type: float32
                    unit: this is the unit and description text
                    description: this is the unit and description text
                  MGDDEC:
                    name: MGDDEC
                    type: float32
                    unit: this is the unit and description text
                    description: this is the unit and description text
                  OMEGASET_U:
                    name: OMEGASET_U
                    type: float32
                    unit: this is the unit and description text
                    description: this is the unit and description text
                  OMEGASET_G:
                    name: OMEGASET_G
                    type: float32
                    unit: this is the unit and description text
                    description: this is the unit and description text
                  OMEGASET_R:
                    name: OMEGASET_R
                    type: float32
                    unit: this is the unit and description text
                    description: this is the unit and description text
                  OMEGASET_I:
                    name: OMEGASET_I
                    type: float32
                    unit: this is the unit and description text
                    description: this is the unit and description text
                  OMEGASET_Z:
                    name: OMEGASET_Z
                    type: float32
                    unit: this is the unit and description text
                    description: this is the unit and description text
                  EAMFIT_RA:
                    name: EAMFIT_RA
                    type: float32
                    unit: this is the unit and description text
                    description: this is the unit and description text
                  EAMFIT_DEC:
                    name: EAMFIT_DEC
                    type: float32
                    unit: this is the unit and description text
                    description: this is the unit and description text
                  EAMFIT_THETA:
                    name: EAMFIT_THETA
                    type: float32
                    unit: this is the unit and description text
                    description: this is the unit and description text
                  EAMFIT_THETA0:
                    name: EAMFIT_THETA0
                    type: float32
                    unit: this is the unit and description text
                    description: this is the unit and description text
                  EAMFIT_A:
                    name: EAMFIT_A
                    type: float32
                    unit: this is the unit and description text
                    description: this is the unit and description text
                  EAMFIT_B:
                    name: EAMFIT_B
                    type: float32
                    unit: this is the unit and description text
                    description: this is the unit and description text
                  EAMFIT_RAERR:
                    name: EAMFIT_RAERR
                    type: float32
                    unit: this is the unit and description text
                    description: this is the unit and description text
                  EAMFIT_DECERR:
                    name: EAMFIT_DECERR
                    type: float32
                    unit: this is the unit and description text
                    description: this is the unit and description text
                  EAMFIT_THETAERR:
                    name: EAMFIT_THETAERR
                    type: float32
                    unit: this is the unit and description text
                    description: this is the unit and description text
                  EAMFIT_THETA0ERR:
                    name: EAMFIT_THETA0ERR
                    type: float32
                    unit: this is the unit and description text
                    description: this is the unit and description text
                  EAMFIT_AERR:
                    name: EAMFIT_AERR
                    type: float32
                    unit: this is the unit and description text
                    description: this is the unit and description text
                  EAMFIT_BERR:
                    name: EAMFIT_BERR
                    type: float32
                    unit: this is the unit and description text
                    description: this is the unit and description text
                  TAIBEG:
                    name: TAIBEG
                    type: char[13]
                    unit: this is the unit and description text
                    description: this is the unit and description text
                  HADRILL:
                    name: HADRILL
                    type: float32
                    unit: this is the unit and description text
                    description: this is the unit and description text
                  LSTMID:
                    name: LSTMID
                    type: float32
                    unit: this is the unit and description text
                    description: this is the unit and description text
                  HAMID:
                    name: HAMID
                    type: float32
                    unit: this is the unit and description text
                    description: this is the unit and description text
                  AIRMASS:
                    name: AIRMASS
                    type: float32
                    unit: this is the unit and description text
                    description: this is the unit and description text
                  IFURA:
                    name: IFURA
                    type: float64
                    unit: this is the unit and description text
                    description: this is the unit and description text
                  IFUDEC:
                    name: IFUDEC
                    type: float64
                    unit: this is the unit and description text
                    description: this is the unit and description text
                  CENRA:
                    name: CENRA
                    type: float64
                    unit: this is the unit and description text
                    description: this is the unit and description text
                  CENDEC:
                    name: CENDEC
                    type: float64
                    unit: this is the unit and description text
                    description: this is the unit and description text
                  XFOCAL:
                    name: XFOCAL
                    type: float32
                    unit: this is the unit and description text
                    description: this is the unit and description text
                  YFOCAL:
                    name: YFOCAL
                    type: float32
                    unit: this is the unit and description text
                    description: this is the unit and description text
                  MNGTARG1:
                    name: MNGTARG1
                    type: int32
                    unit: this is the unit and description text
                    description: this is the unit and description text
                  MNGTARG2:
                    name: MNGTARG2
                    type: int32
                    unit: this is the unit and description text
                    description: this is the unit and description text
                  MNGTARG3:
                    name: MNGTARG3
                    type: int32
                    unit: this is the unit and description text
                    description: this is the unit and description text
                  BLUESN2:
                    name: BLUESN2
                    type: float32
                    unit: this is the unit and description text
                    description: this is the unit and description text
                  REDSN2:
                    name: REDSN2
                    type: float32
                    unit: this is the unit and description text
                    description: this is the unit and description text
                  BLUETHRUPT:
                    name: BLUETHRUPT
                    type: float32
                    unit: this is the unit and description text
                    description: this is the unit and description text
                  REDTHRUPT:
                    name: REDTHRUPT
                    type: float32
                    unit: this is the unit and description text
                    description: this is the unit and description text
                  BLUEPSTAT:
                    name: BLUEPSTAT
                    type: float32
                    unit: this is the unit and description text
                    description: this is the unit and description text
                  REDPSTAT:
                    name: REDPSTAT
                    type: float32
                    unit: this is the unit and description text
                    description: this is the unit and description text
                  DRP2QUAL:
                    name: DRP2QUAL
                    type: int32
                    unit: this is the unit and description text
                    description: this is the unit and description text
                  THISBADIFU:
                    name: THISBADIFU
                    type: int32
                    unit: this is the unit and description text
                    description: this is the unit and description text
                  PF_FWHM_G:
                    name: PF_FWHM_G
                    type: float32
                    unit: this is the unit and description text
                    description: this is the unit and description text
                  PF_FWHM_R:
                    name: PF_FWHM_R
                    type: float32
                    unit: this is the unit and description text
                    description: this is the unit and description text
                  PF_FWHM_I:
                    name: PF_FWHM_I
                    type: float32
                    unit: this is the unit and description text
                    description: this is the unit and description text
                  PF_FWHM_Z:
                    name: PF_FWHM_Z
                    type: float32
                    unit: this is the unit and description text
                    description: this is the unit and description text
              hdu12:
                name: XPOS
                description: description of the HDU extension
                is_image: true
                size: 2 MB
                header:
                - key: XTENSION
                  value: IMAGE
                  comment: IMAGE extension
                - key: BITPIX
                  value: -32
                  comment: Number of bits per data pixel
                - key: NAXIS
                  value: 2
                  comment: Number of data axes
                - key: NAXIS1
                  value: 4563
                  comment: ''
                - key: NAXIS2
                  value: 171
                  comment: ''
                - key: PCOUNT
                  value: 0
                  comment: No Group Parameters
                - key: GCOUNT
                  value: 1
                  comment: One Data Group
                - key: EXTNAME
                  value: XPOS
                  comment: ''
                - key: DATASUM
                  value: '3023661791'
                  comment: data unit checksum updated 2018-03-21T06:08:46
                - key: CHECKSUM
                  value: 64MB71K961KA61K9
                  comment: HDU checksum updated 2018-03-21T06:08:46
              hdu13:
                name: YPOS
                description: description of the HDU extension
                is_image: true
                size: 2 MB
                header:
                - key: XTENSION
                  value: IMAGE
                  comment: IMAGE extension
                - key: BITPIX
                  value: -32
                  comment: Number of bits per data pixel
                - key: NAXIS
                  value: 2
                  comment: Number of data axes
                - key: NAXIS1
                  value: 4563
                  comment: ''
                - key: NAXIS2
                  value: 171
                  comment: ''
                - key: PCOUNT
                  value: 0
                  comment: No Group Parameters
                - key: GCOUNT
                  value: 1
                  comment: One Data Group
                - key: EXTNAME
                  value: YPOS
                  comment: ''
                - key: DATASUM
                  value: '2342972923'
                  comment: data unit checksum updated 2018-03-21T06:08:46
                - key: CHECKSUM
                  value: 0Apa14oX0Aoa03oW
                  comment: HDU checksum updated 2018-03-21T06:08:46


.. tab:: Par

    the "Yanny" acsii parameter file format, i.e. ".par"

    **File Info**

    An SDSS platePlans Yanny parameter file

    - **Example**: $PLATELIST_DIR/platePlans.par
    - **File Species**: platePlans
    - **Abstract Path**: PLATELIST_DIR/platePlans.par
    - **Example Keys**: None

    **Generate Commands**

    Command-line and Python commands to generate a datamodel

    .. tab:: CLI

        .. code-block:: console

            $ datamodel generate -f platePlans \
            -p PLATELIST_DIR/platePlans.par -r WORK

    .. tab:: Python

        .. code-block:: python

            # generate a datamodel for the "WORK" release
            dm = DataModel(file_spec='platePlans', path='PLATELIST_DIR/platePlans.par', keywords=[], release="WORK")
            dm.write_stubs()

    **Yaml Output**

    The generated output yaml datamodel stub

    .. code-block:: yaml

        general:
          name: platePlans
          short: replace me - with a short one sentence summary of file
          description: replace me - with a longer description of the data product
          datatype: PAR
          filesize: 1 MB
          releases:
          - WORK
          environments:
          - PLATELIST_DIR
          naming_convention: replace me - with $PLATELIST_DIR/platePlans.par or platePlans.par
            but with regex pattern matches
          generated_by: replace me - with the name(s) of any git or svn product(s) that produces
            this product.
          design: false
        changelog:
          description: Describes changes to the datamodel product and/or file structure from
            one release to another
          releases: {}
        releases:
          WORK:
            template: $PLATELIST_DIR/platePlans.par
            example: platePlans.par
            location: platePlans.par
            environment: PLATELIST_DIR
            access:
            in_sdss_access: true
            path_name: platePlans
            path_template: $PLATELIST_DIR/platePlans.par
            path_kwargs: []
            access_string: platePlans = $PLATELIST_DIR/platePlans.par
            par:
              comments: |-
                # platePlans.par
                #
                # Global plate planning file for SDSS-III
                #
                # Every plate number (plateid) has one and only one entry here.
                #
                # Numbering of plates starts after last plates of SDSS-II, which
                # were the MARVELS June 2008 pre-selection plates (3000-3014).
                # Note that SDSS-II also used plate numbers 8000-8033, which should
                # therefore be avoided
                #
                # Meaning of columns:
                #  plateid - unique ID of plate
                #  designid - ID of "design"; two plates can have the same design
                #             but be drilled for different HA, TEMP, EPOCH
                #  locationid - ID indicating a notional "location", usually meaning
                #               a group of plates at least roughly co-centered and
                #               which should be thought of as related to each other
                #  tileid - SDSS-I, -II tileId value (-1 for SDSS-III plates, for
                #           backwards compatibility ONLY)
                #  plateDesignVersion - indicates which version of the defaults
                #                       file (specified in the definition
                #                       file) to use
                #  ha - hour angle to drill plate for (one for each pointing)
                #       should be given in degrees
                #       Sign convention is such that HA = LST - RA
                #  temp - temperature to drill plate for
                #  epoch - epoch to drill plate for
                #  raCen, decCen - center of plate; note that we are breaking normal
                #                  form here, since this should be defined in the
                #                  plateDefinition file; if the two disagree,
                #                  plate_design will bail
                #  survey - what survey is the plate associated with?
                #  programname - what program within the survey is the plate associated with?
                #  drillstyle - what instrument
                #  rerun - for SDSS data, what rerun(s) should we be search for data in?
                #          (e.g. "137 161")
                #  platerun - name for platerun (used to gather plates for output to drillers)
                #  chunk - name of associated targeting "chunk", if any (for SEGUE-2 and
                #          MARVELS, this is the same as platerun; in SDSS-I, -II and BOSS,
                #          it will vary)
                #  name - a name for the plate
                #  comments - any comments about the plate
                #
                # plate_design reads the line in this file for a given plate and
                # uses it to set the appropriate parameters for drilling. If the
                # designs have been created for a given designid, then it does not
                # remake, but just makes the new plateid (unless /clobber is set).
                #
                # Note that a limit is imposed here on the number of pointings per
                # plate; there is one HA value per pointing, and this file only allows
                # six entries.
                #
                # There are a number of different fields to indicate what "type"
                # of plate it is: survey, programname, chunk, and platerun.
                #    platerun - just the drilling run that was used
                #    chunk - the "chunk" name, usually specifying that
                #            which tiling section this plate is part of
                #            (for SDSS Legacy and BOSS)
                #    programname - the name of the program, e.g. SDSS-I,-II had
                #                  a large # of plates in the legacy program
                #                  but had other programs (lowz, photoz, etc)
                #    survey - generic survey (segue1, segue2, sdss_special, etc)
                #
                # MRB 2008-06-10
                #
              header: []
              tables:
                PLATEPLANS:
                name: PLATEPLANS
                description: replace me - with a description of this table
                n_rows: 7551
                structure:
                - name: plateid
                    type: int
                    description: replace me - with a description of this column
                    unit: replace me - with a unit of this column
                    is_array: false
                    is_enum: false
                    example: 186
                - name: designid
                    type: int
                    description: replace me - with a description of this column
                    unit: replace me - with a unit of this column
                    is_array: false
                    is_enum: false
                    example: -1
                - name: locationid
                    type: int
                    description: replace me - with a description of this column
                    unit: replace me - with a unit of this column
                    is_array: false
                    is_enum: false
                    example: -1
                - name: tileid
                    type: int
                    description: replace me - with a description of this column
                    unit: replace me - with a unit of this column
                    is_array: false
                    is_enum: false
                    example: 25
                - name: plateDesignVersion
                    type: char[20]
                    description: replace me - with a description of this column
                    unit: replace me - with a unit of this column
                    is_array: false
                    is_enum: false
                    example: ' '
                - name: ha
                    type: float[6]
                    description: replace me - with a description of this column
                    unit: replace me - with a unit of this column
                    is_array: true
                    is_enum: false
                    example:
                    - -45.0
                    - 0.0
                    - 0.0
                    - 0.0
                    - 0.0
                    - 0.0
                - name: temp
                    type: float
                    description: replace me - with a description of this column
                    unit: replace me - with a unit of this column
                    is_array: false
                    is_enum: false
                    example: 0.0
                - name: epoch
                    type: float
                    description: replace me - with a description of this column
                    unit: replace me - with a unit of this column
                    is_array: false
                    is_enum: false
                    example: 1999.719970703125
                - name: raCen
                    type: double
                    description: replace me - with a description of this column
                    unit: replace me - with a unit of this column
                    is_array: false
                    is_enum: false
                    example: 354.36291
                - name: decCen
                    type: double
                    description: replace me - with a description of this column
                    unit: replace me - with a unit of this column
                    is_array: false
                    is_enum: false
                    example: 0.061307
                - name: survey
                    type: char[20]
                    description: replace me - with a description of this column
                    unit: replace me - with a unit of this column
                    is_array: false
                    is_enum: false
                    example: sdss
                - name: programname
                    type: char[40]
                    description: replace me - with a description of this column
                    unit: replace me - with a unit of this column
                    is_array: false
                    is_enum: false
                    example: commissioning
                - name: drillstyle
                    type: char[20]
                    description: replace me - with a description of this column
                    unit: replace me - with a unit of this column
                    is_array: false
                    is_enum: false
                    example: sdss
                - name: rerun
                    type: char[50]
                    description: replace me - with a description of this column
                    unit: replace me - with a unit of this column
                    is_array: false
                    is_enum: false
                    example: ' '
                - name: platerun
                    type: char[200]
                    description: replace me - with a description of this column
                    unit: replace me - with a unit of this column
                    is_array: false
                    is_enum: false
                    example: chunk2
                - name: chunk
                    type: char[200]
                    description: replace me - with a description of this column
                    unit: replace me - with a unit of this column
                    is_array: false
                    is_enum: false
                    example: chunk2
                - name: name
                    type: char[200]
                    description: replace me - with a description of this column
                    unit: replace me - with a unit of this column
                    is_array: false
                    is_enum: false
                    example: ''
                - name: comments
                    type: char[200]
                    description: replace me - with a description of this column
                    unit: replace me - with a unit of this column
                    is_array: false
                    is_enum: false
                    example: SDSS-I, -II; ctile=v1_0; v1_11


