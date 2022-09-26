# MOS Target for DR18
# validated
datamodel_generate -f mos_target_target -p MOS_TARGET/{v_targ}/mos_target_target-{num}.fits -k v_targ=1.0.1 -k num=01 -t sdss5 --skip-git

# TBD in minidb_docs (as of 09/27/2022)
datamodel_generate -f mos_target_allwise -p MOS_TARGET/{v_targ}/mos_target_allwise-{num}.fits -k v_targ=1.0.1 -k num=01 -t sdss5 --skip-git
# MOS Target paths

datamodel_generate -f mos_target_carton_to_target -p MOS_TARGET/{v_targ}/mos_target_carton_to_target-{num}.fits -k v_targ=1.0.1 -k num=01 -t sdss5 --skip-git
datamodel_generate -f mos_target_catwise2020 -p MOS_TARGET/{v_targ}/mos_target_catwise2020-{num}.fits -k v_targ=1.0.1 -k num=01 -t sdss5 --skip-git
datamodel_generate -f mos_target_magnitude -p MOS_TARGET/{v_targ}/mos_target_magnitude-{num}.fits -k v_targ=1.0.1 -k num=01 -t sdss5 --skip-git
datamodel_generate -f mos_target_bhm_rm_v0_2_1 -p MOS_TARGET/{v_targ}/mos_target_bhm_rm_v0_2_1.fits -k v_targ=1.0.1 -t sdss5 --skip-git
datamodel_generate -f mos_target_cadence_epoch -p MOS_TARGET/{v_targ}/mos_target_cadence_epoch.fits -k v_targ=1.0.1 -t sdss5 --skip-git
datamodel_generate -f mos_target_cadence -p MOS_TARGET/{v_targ}/mos_target_cadence.fits -k v_targ=1.0.1 -t sdss5 --skip-git
datamodel_generate -f mos_target_carton -p MOS_TARGET/{v_targ}/mos_target_carton.fits -k v_targ=1.0.1 -t sdss5 --skip-git
datamodel_generate -f mos_target_catalogdb_version -p MOS_TARGET/{v_targ}/mos_target_catalogdb_version.fits -k v_targ=1.0.1 -t sdss5 --skip-git
datamodel_generate -f mos_target_category -p MOS_TARGET/{v_targ}/mos_target_category.fits -k v_targ=1.0.1 -t sdss5 --skip-git
datamodel_generate -f mos_target_instrument -p MOS_TARGET/{v_targ}/mos_target_instrument.fits -k v_targ=1.0.1 -t sdss5 --skip-git
datamodel_generate -f mos_target_mapper -p MOS_TARGET/{v_targ}/mos_target_mapper.fits -k v_targ=1.0.1 -t sdss5 --skip-git
datamodel_generate -f mos_target_targetdb_version -p MOS_TARGET/{v_targ}/mos_target_targetdb_version.fits -k v_targ=1.0.1 -t sdss5 --skip-git

	modified:   mos_target_bhm_efeds_veto.yaml
	modified:   mos_target_cadence.yaml
	modified:   mos_target_cadence_epoch.yaml
	modified:   mos_target_carton.yaml
	modified:   mos_target_carton_to_target.yaml
	modified:   mos_target_category.yaml
	modified:   mos_target_catwise2020.yaml
	modified:   mos_target_instrument.yaml
	modified:   mos_target_magnitude.yaml
	modified:   mos_target_mapper.yaml
