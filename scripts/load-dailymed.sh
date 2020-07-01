#!/bin/bash

set -x

export LUIGI_CONFIG_PATH=./config/luigi.cfg
export PYTHON=./_python-env/bin/python
export LOGDIR=./logs

echo $PYTHON

mkdir -p $LOGDIR

# This will download, extract and flatten all the DailyMed data, including OTC
# If you only want human prescription drugs, kill the script after all those 
# files are downloaded, delete any OTC or unneeded zips in the data folder, then
# re-run this script.
$PYTHON openfda/spl/pipeline.py FlattenDailyMedSPL | tee -a $LOGDIR/dailymed.log 2>&1


