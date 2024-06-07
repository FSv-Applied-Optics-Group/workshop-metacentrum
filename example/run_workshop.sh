#!/bin/bash
#PBS -q default@pbs-m1.metacentrum.cz
#PBS -l select=1:ncpus=1:ngpus=2:mem=500mb:scratch_local=500mb
#PBS -l walltime=0:05:00
#PBS -N workshop_test
#PBS -m abe
# initialize the required application (e.g. Python, version 3.4.1, compiled by gcc)

trap 'clean_scratch' TERM EXIT
DATADIR=/storage/projects/CVUT_Fsv_AO/workshop/workshop_test
DATADIR_text=/storage/projects/CVUT_Fsv_AO/workshop/data.txt

echo "$PBS_JOBID is running on node `hostname -f` in a scratch directory $SCRATCHDIR" >> $DATADIR/jobs_info.txt
test -n "$SCRATCHDIR" || { echo >&2 "Variable SCRATCHDIR is not set!"; exit 1; }

cp $DATADIR/test.py $SCRATCHDIR
cp $DATADIR_text $SCRATCHDIR
cd $SCRATCHDIR

mkdir output

module add python/3.6.2-gcc

python3 test.py

cp -r $SCRATCHDIR/output $DATADIR
clean_scratch
exit