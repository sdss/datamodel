
# validated
datamodel_generate -f mos_target_target -p MOS_TARGET/{v_targ}/mos_target_target-{num}.fits -k v_targ=1.0.1 -k num=01 -t sdss5 --skip-git

# TBD in minidb_docs (as of 09/27/2022)
datamodel_generate -f mos_target_allwise -p MOS_TARGET/{v_targ}/mos_target_allwise-{num}.fits -k v_targ=1.0.1 -k num=01 -t sdss5 --skip-git
