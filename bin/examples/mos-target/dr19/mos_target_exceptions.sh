?? datamodel_generate -f mos_target_carton -p MOS_TARGET/{v_targ}/mos_carton.fits -k v_targ=1.0.2 -r DR19 -c DR18 -h
?? datamodel_generate -f mos_target_legacy_survey_dr8 -p MOS_TARGET/{v_targ}/mos_legacy_survey_dr8-{num}.fits -k v_targ=1.0.2 -k num=1 -r DR19 -c DR18 -h
needs a dr18 datamodel?
? datamodel_generate -f mos_target_sdss_dr16_qso -p MOS_TARGET/{v_targ}/mos_sdss_dr16_qso.fits -k v_targ=1.0.2 -r DR19 -c DR18 -h

?? datamodel_generate -f mos_target_targetdb_version -p MOS_TARGET/{v_targ}/mos_targetdb_version.fits -k v_targ=1.0.2 -r DR19 -c DR18 -h
needs a DR18 datamodel
?? datamodel_generate -f mos_target_targeting_generation -p MOS_TARGET/{v_targ}/mos_targeting_generation.fits -k v_targ=1.0.2 -r DR19 -c DR18 -h

?? datamodel_generate -f mos_target_tycho2 -p MOS_TARGET/{v_targ}/mos_tycho2-{num}.fits -k v_targ=1.0.2 -k num=1 -r DR19 -c DR18 -h

