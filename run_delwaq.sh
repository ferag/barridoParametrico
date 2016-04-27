#!/bin/bash
#@ job_name = test_serial
#@ initialdir = .
#@ output = waq_output_%j.out
#@ error = serial_error_%j.err
#@ total_tasks = 1
#@ cpus_per_task = 1
#@ wall_clock_limit = 3:00:00    
#
    # This script is an example for running DELWAQ D-Water Quality
    # Adapt and use it for your own purpose
    #
    # michel.jeuken@deltares.nl
    # 11 Mrt 2013
    # 
    #
    # This script starts 3D DELWAQ D-Water Quality computation on Linux
    #


    #
    # Set the config file here
    # 
export NETCDF_LIBS=<path to NETCDLIB>
export NETCDF_CFLAGS=<path to NETCDFLIB>
module load gcc/4.9.2
echo $PATH
export BASE_PATH=/path/to/origin/path(taken from command line)
export OUTPUT_PATH=/path/to/new/path(automatic)
echo $SLURM_JOBID
export TMPDIR=/scratch/$SLURM_JOBID
mkdir $TMPDIR
cd $TMPDIR

echo "Copying base files"
cp $BASE_PATH/* $TMPDIR
echo "Copying config files"
cp $OUTPUT_PATH/* $TMPDIR

inpfile=wqnew_basic2_t26_2.inp

currentdir=$TMPDIR
echo $currentdir
argfile=$currentdir/$inpfile

    #
    # Set the directory containing delwaq1 and delwaq2 and
    # the directory containing the proc_def and bloom files here
    #
#exedir=$currentdir/../bin/lnx/waq/bin
#export LD_LIBRARY_PATH=$exedir:$LD_LIBRARY_PATH 
#procfile=$currentdir/../bin/lnx/waq/default/proc_def
exedir=<exe_dir>
export LD_LIBRARY_PATH=$exedir:$LD_LIBRARY_PATH
procfile=<proc_def>
    #
    # Run delwaq 1
    #
$exedir/delwaq1 $argfile -eco -p "$procfile"

    #
    # Wait for any key to run delwaq 2
    #
if [ $? == 0 ]
  then
    echo ""
    echo "Delwaq1 did run without errors."

    #
    # Run delwaq 2
    #
    echo ""
    $exedir/delwaq2 $argfile

    if [ $? -eq 0 ]
      then
        echo ""
        echo "Delwaq2 did run without errors."
      else
        echo ""
        echo "Delwaq2 did not run correctly."
    fi
else
    echo ""
    echo "Delwaq1 did not run correctly, ending calculation"
fi

cp $TMPDIR/*.hda $OUTPUT_PATH
cp $TMPDIR/*.hdf $OUTPUT_PATH
cp $TMPDIR/*.ada $OUTPUT_PATH
cp $TMPDIR/*.cco $OUTPUT_PATH
cp $TMPDIR/*.lga $OUTPUT_PATH
cp $TMPDIR/*.lsp $OUTPUT_PATH
cp $TMPDIR/*.lst $OUTPUT_PAT
rm -rf $TMPDIR/*
rm -rf $TMPDIR
echo "FINISHED"
