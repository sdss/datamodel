# MOS Target for DR18
# validated
datamodel_generate -f mos_target_allwise -p MOS_TARGET/{v_targ}/mos_allwise-{num}.fits -k v_targ=1.0.2 -k num=01 -r DR19 -c DR18 -h
datamodel_generate -f mos_target_best_brightest -p MOS_TARGET/{v_targ}/mos_best_brightest.fits -k v_targ=1.0.2 -r DR19 -c DR18 -h
datamodel_generate -f mos_target_bhm_csc_v2 -p MOS_TARGET/{v_targ}/mos_bhm_csc_v2.fits -k v_targ=1.0.2 -r DR19 -c DR18 -h
datamodel_generate -f mos_target_bhm_efeds_veto -p MOS_TARGET/{v_targ}/mos_bhm_efeds_veto.fits -k v_targ=1.0.2 -r DR19 -c DR18 -h
datamodel_generate -f mos_target_bhm_rm_v0_2 -p MOS_TARGET/{v_targ}/mos_bhm_rm_v0_2.fits -k v_targ=1.0.2 -r DR19 -c DR18 -h
datamodel_generate -f mos_target_cadence -p MOS_TARGET/{v_targ}/mos_cadence.fits -k v_targ=1.0.2 -r DR19 -c DR18 -h
datamodel_generate -f mos_target_cadence_epoch -p MOS_TARGET/{v_targ}/mos_cadence_epoch.fits -k v_targ=1.0.2 -r DR19 -c DR18 -h
datamodel_generate -f mos_target_carton -p MOS_TARGET/{v_targ}/mos_carton.fits -k v_targ=1.0.2 -r DR19 -c DR18 -h
datamodel_update -f mos_target_carton -r DR19
datamodel_generate -f mos_target_carton_to_target -p MOS_TARGET/{v_targ}/mos_carton_to_target-{num}.fits -k v_targ=1.0.2 -k num=001 -r DR19 -c DR18 -h
datamodel_generate -f mos_target_cataclysmic_variables -p MOS_TARGET/{v_targ}/mos_cataclysmic_variables.fits -k v_targ=1.0.2 -r DR19 -c DR18 -h
datamodel_generate -f mos_target_catalog -p MOS_TARGET/{v_targ}/mos_catalog-{num}.fits -k v_targ=1.0.2 -k num=01 -r DR19 -c DR18 -h
datamodel_generate -f mos_target_catalog_to_allwise -p MOS_TARGET/{v_targ}/mos_catalog_to_allwise-{num}.fits -k v_targ=1.0.2 -k num=01 -r DR19 -c DR18 -h
datamodel_generate -f mos_target_catalog_to_bhm_efeds_veto -p MOS_TARGET/{v_targ}/mos_catalog_to_bhm_efeds_veto.fits -k v_targ=1.0.2 -r DR19 -c DR18 -h
datamodel_generate -f mos_target_catalog_to_bhm_rm_v0_2 -p MOS_TARGET/{v_targ}/mos_catalog_to_bhm_rm_v0_2.fits -k v_targ=1.0.2 -r DR19 -c DR18 -h
datamodel_generate -f mos_target_catalog_to_catwise2020 -p MOS_TARGET/{v_targ}/mos_catalog_to_catwise2020-{num}.fits -k v_targ=1.0.2 -k num=01 -r DR19 -c DR18 -h
datamodel_generate -f mos_target_catalog_to_glimpse -p MOS_TARGET/{v_targ}/mos_catalog_to_glimpse-{num}.fits -k v_targ=1.0.2 -k num=1 -r DR19 -c DR18 -h
datamodel_generate -f mos_target_catalog_to_guvcat -p MOS_TARGET/{v_targ}/mos_catalog_to_guvcat-{num}.fits -k v_targ=1.0.2 -k num=1 -r DR19 -c DR18 -h
datamodel_generate -f mos_target_catalog_to_legacy_survey_dr8 -p MOS_TARGET/{v_targ}/mos_catalog_to_legacy_survey_dr8-{num}.fits -k v_targ=1.0.2 -k num=01 -r DR19 -c DR18 -h
datamodel_generate -f mos_target_catalog_to_panstarrs1 -p MOS_TARGET/{v_targ}/mos_catalog_to_panstarrs1-{num}.fits -k v_targ=1.0.2 -k num=01 -r DR19 -c DR18 -h
datamodel_generate -f mos_target_catalog_to_sdss_dr13_photoobj_primary -p MOS_TARGET/{v_targ}/mos_catalog_to_sdss_dr13_photoobj_primary-{num}.fits -k v_targ=1.0.2 -k num=01 -r DR19 -c DR18 -h
datamodel_generate -f mos_target_catalog_to_sdss_dr16_specobj -p MOS_TARGET/{v_targ}/mos_catalog_to_sdss_dr16_specobj-{num}.fits -k v_targ=1.0.2 -k num=1 -r DR19 -c DR18 -h
datamodel_generate -f mos_target_catalog_to_skies_v2 -p MOS_TARGET/{v_targ}/mos_catalog_to_skies_v2-{num}.fits -k v_targ=1.0.2 -k num=01 -r DR19 -c DR18 -h
datamodel_generate -f mos_target_catalog_to_skymapper_dr2 -p MOS_TARGET/{v_targ}/mos_catalog_to_skymapper_dr2-{num}.fits -k v_targ=1.0.2 -k num=01 -r DR19 -c DR18 -h
datamodel_generate -f mos_target_catalog_to_supercosmos -p MOS_TARGET/{v_targ}/mos_catalog_to_supercosmos-{num}.fits -k v_targ=1.0.2 -k num=01 -r DR19 -c DR18 -h
datamodel_generate -f mos_target_catalog_to_tic_v8 -p MOS_TARGET/{v_targ}/mos_catalog_to_tic_v8-{num}.fits -k v_targ=1.0.2 -k num=01 -r DR19 -c DR18 -h
datamodel_generate -f mos_target_catalog_to_tycho2 -p MOS_TARGET/{v_targ}/mos_catalog_to_tycho2-{num}.fits -k v_targ=1.0.2 -k num=1 -r DR19 -c DR18 -h
datamodel_generate -f mos_target_catalog_to_uvotssc1 -p MOS_TARGET/{v_targ}/mos_catalog_to_uvotssc1.fits -k v_targ=1.0.2 -r DR19 -c DR18 -h
datamodel_generate -f mos_target_catalog_to_xmm_om_suss_4_1 -p MOS_TARGET/{v_targ}/mos_catalog_to_xmm_om_suss_4_1.fits -k v_targ=1.0.2 -r DR19 -c DR18 -h
?? datamodel_generate -f mos_target_catalogdb_version -p MOS_TARGET/{v_targ}/mos_catalogdb_version.fits -k v_targ=1.0.2 -r DR19 -c DR18 -h
datamodel_generate -f mos_target_category -p MOS_TARGET/{v_targ}/mos_category.fits -k v_targ=1.0.2 -r DR19 -c DR18 -h
datamodel_generate -f mos_target_catwise2020 -p MOS_TARGET/{v_targ}/mos_catwise2020-{num}.fits -k v_targ=1.0.2 -k num=01 -r DR19 -c DR18 -h
datamodel_generate -f mos_target_ebosstarget_v5 -p MOS_TARGET/{v_targ}/mos_ebosstarget_v5.fits -k v_targ=1.0.2 -r DR19 -c DR18 -h
datamodel_generate -f mos_target_gaia_dr2_ruwe -p MOS_TARGET/{v_targ}/mos_gaia_dr2_ruwe-{num}.fits -k v_targ=1.0.2 -k num=01 -r DR19 -c DR18 -h
datamodel_generate -f mos_target_gaia_dr2_source -p MOS_TARGET/{v_targ}/mos_gaia_dr2_source-{num}.fits -k v_targ=1.0.2 -k num=01 -r DR19 -c DR18 -h
datamodel_generate -f mos_target_gaia_dr2_wd -p MOS_TARGET/{v_targ}/mos_gaia_dr2_wd.fits -k v_targ=1.0.2 -r DR19 -c DR18 -h
datamodel_generate -f mos_target_gaia_unwise_agn -p MOS_TARGET/{v_targ}/mos_gaia_unwise_agn-{num}.fits -k v_targ=1.0.2 -k num=1 -r DR19 -c DR18 -h
datamodel_generate -f mos_target_gaiadr2_tmass_best_neighbour -p MOS_TARGET/{v_targ}/mos_gaiadr2_tmass_best_neighbour-{num}.fits -k v_targ=1.0.2 -k num=01 -r DR19 -c DR18 -h
datamodel_generate -f mos_target_geometric_distances_gaia_dr2 -p MOS_TARGET/{v_targ}/mos_geometric_distances_gaia_dr2-{num}.fits -k v_targ=1.0.2 -k num=01 -r DR19 -c DR18 -h
datamodel_generate -f mos_target_glimpse -p MOS_TARGET/{v_targ}/mos_glimpse-{num}.fits -k v_targ=1.0.2 -k num=1 -r DR19 -c DR18 -h
datamodel_generate -f mos_target_guvcat -p MOS_TARGET/{v_targ}/mos_guvcat-{num}.fits -k v_targ=1.0.2 -k num=1 -r DR19 -c DR18 -h
datamodel_generate -f mos_target_instrument -p MOS_TARGET/{v_targ}/mos_instrument.fits -k v_targ=1.0.2 -r DR19 -c DR18 -h
datamodel_generate -f mos_target_legacy_survey_dr8 -p MOS_TARGET/{v_targ}/mos_legacy_survey_dr8-{num}.fits -k v_targ=1.0.2 -k num=01 -r DR19 -c DR18 -h
datamodel_generate -f mos_target_magnitude -p MOS_TARGET/{v_targ}/mos_magnitude-{num}.fits -k v_targ=1.0.2 -k num=01 -r DR19 -c DR18 -h
datamodel_generate -f mos_target_mapper -p MOS_TARGET/{v_targ}/mos_mapper.fits -k v_targ=1.0.2 -r DR19 -c DR18 -h
datamodel_generate -f mos_target_panstarrs1 -p MOS_TARGET/{v_targ}/mos_panstarrs1-{num}.fits -k v_targ=1.0.2 -k num=01 -r DR19 -c DR18 -h
datamodel_generate -f mos_target_sagitta -p MOS_TARGET/{v_targ}/mos_sagitta.fits -k v_targ=1.0.2 -r DR19 -c DR18 -h
datamodel_generate -f mos_target_sdss_apogeeallstarmerge_r13 -p MOS_TARGET/{v_targ}/mos_sdss_apogeeallstarmerge_r13.fits -k v_targ=1.0.2 -r DR19 -c DR18 -h
datamodel_generate -f mos_target_sdss_dr13_photoobj_primary -p MOS_TARGET/{v_targ}/mos_sdss_dr13_photoobj_primary-{num}.fits -k v_targ=1.0.2 -k num=1 -r DR19 -c DR18 -h
datamodel_generate -f mos_target_sdss_dr16_qso -p MOS_TARGET/{v_targ}/mos_sdss_dr16_qso.fits -k v_targ=1.0.2 -r DR19 -c DR18 -h
datamodel_update -f mos_target_sdss_dr16_qso -r DR19
datamodel_generate -f mos_target_sdss_dr16_specobj -p MOS_TARGET/{v_targ}/mos_sdss_dr16_specobj-{num}.fits -k v_targ=1.0.2 -k num=1 -r DR19 -c DR18 -h
datamodel_generate -f mos_target_skies_v2 -p MOS_TARGET/{v_targ}/mos_skies_v2-{num}.fits -k v_targ=1.0.2 -k num=01 -r DR19 -c DR18 -h
datamodel_generate -f mos_target_skymapper_dr2 -p MOS_TARGET/{v_targ}/mos_skymapper_dr2-{num}.fits -k v_targ=1.0.2 -k num=01 -r DR19 -c DR18 -h
datamodel_generate -f mos_target_supercosmos -p MOS_TARGET/{v_targ}/mos_supercosmos-{num}.fits -k v_targ=1.0.2 -k num=01 -r DR19 -c DR18 -h
datamodel_generate -f mos_target_target -p MOS_TARGET/{v_targ}/mos_target-{num}.fits -k v_targ=1.0.2 -k num=01 -r DR19 -c DR18 -h
?? datamodel_generate -f mos_target_targetdb_version -p MOS_TARGET/{v_targ}/mos_targetdb_version.fits -k v_targ=1.0.2 -r DR19 -c DR18 -h
?? datamodel_generate -f mos_target_targeting_generation -p MOS_TARGET/{v_targ}/mos_targeting_generation.fits -k v_targ=1.0.2 -r DR19 -c DR18 -h
datamodel_generate -f mos_target_tic_v8 -p MOS_TARGET/{v_targ}/mos_tic_v8-{num}.fits -k v_targ=1.0.2 -k num=01 -r DR19 -c DR18 -h
datamodel_generate -f mos_target_twomass_psc -p MOS_TARGET/{v_targ}/mos_twomass_psc-{num}.fits -k v_targ=1.0.2 -k num=01 -r DR19 -c DR18 -h
datamodel_generate -f mos_target_tycho2 -p MOS_TARGET/{v_targ}/mos_tycho2-{num}.fits -k v_targ=1.0.2 -k num=1 -r DR19 -c DR18 -h
datamodel_update -f mos_target_tycho2 -r DR19
datamodel_generate -f mos_target_uvotssc1 -p MOS_TARGET/{v_targ}/mos_uvotssc1.fits -k v_targ=1.0.2 -r DR19 -c DR18 -h
datamodel_generate -f mos_target_xmm_om_suss_4_1 -p MOS_TARGET/{v_targ}/mos_xmm_om_suss_4_1.fits -k v_targ=1.0.2 -r DR19 -c DR18 -h
datamodel_generate -f mos_target_yso_clustering -p MOS_TARGET/{v_targ}/mos_yso_clustering.fits -k v_targ=1.0.2 -r DR19 -c DR18 -h
datamodel_generate -f mos_target_zari18pms -p MOS_TARGET/{v_targ}/mos_zari18pms.fits -k v_targ=1.0.2 -r DR19 -c DR18 -h


# TBD in minidb_docs (as of 04/05/2022)
