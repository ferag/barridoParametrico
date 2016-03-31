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
export NETCDF_LIBS=-I/gpfs/csic_users/aguilarf/lib
export NETCDF_CFLAGS=-I/gpfs/csic_users/aguilarf/include/
module load gcc/4.9.2
echo $PATH

inpfile=wqnew_basic2_t26.inp

currentdir=`pwd`
echo $currentdir
argfile=$currentdir/$inpfile

    #
    # Set the directory containing delwaq1 and delwaq2 and
    # the directory containing the proc_def and bloom files here
    #
#exedir=$currentdir/../bin/lnx/waq/bin
#export LD_LIBRARY_PATH=$exedir:$LD_LIBRARY_PATH 
#procfile=$currentdir/../bin/lnx/waq/default/proc_def
exedir=/gpfs/csic_users/aguilarf/delft3d_v2/bin/lnx64/waq/bin
export LD_LIBRARY_PATH=$exedir:$LD_LIBRARY_PATH
procfile=/gpfs/csic_users/aguilarf/delft3d_v2/bin/lnx64/waq/default/proc_def
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
