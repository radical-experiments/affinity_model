#!/bin/sh

# some inspection for logging
hostname

# disable user site packages as those can conflict with our virtualenv
export PYTHONNOUSERSITE=True

# make sure we use the correct sandbox
cd /home/mingtha/radical.pilot.sandbox/rp.session.two.mingtha.017452.0001/pilot.0238

# apply some env settings as stored after running pre_bootstrap_1 commands
export PATH="/opt/python/bin:/opt/gnu/gcc/bin:/opt/gnu/bin:/opt/mvapich2/intel/ib/bin:/opt/intel/composer_xe_2013_sp1.2.144/bin/intel64:/opt/intel/composer_xe_2013_sp1.2.144/mpirt/bin/intel64:/opt/intel/composer_xe_2013_sp1.2.144/debugger/gdb/intel64_mic/bin:/usr/lib64/qt-3.3/bin:/usr/local/bin:/bin:/usr/bin:/usr/local/sbin:/usr/sbin:/sbin:/opt/ibutils/bin:/usr/java/latest/bin:/opt/pdsh/bin:/opt/rocks/bin:/opt/rocks/sbin:/opt/sdsc/bin:/opt/sdsc/sbin:/home/mingtha/bin:/home/mingtha/bin"
export LD_LIBRARY_PATH="/opt/python/lib:/opt/gnu/gcc/lib64:/opt/gnu/gmp/lib:/opt/gnu/mpfr/lib:/opt/gnu/mpc/lib:/opt/gnu/lib:/opt/gnu/lib64:/opt/mvapich2/intel/ib/lib:/opt/intel/composer_xe_2013_sp1.2.144/compiler/lib/intel64:/opt/intel/composer_xe_2013_sp1.2.144/mpirt/lib/intel64:/opt/intel/composer_xe_2013_sp1.2.144/ipp/../compiler/lib/intel64:/opt/intel/composer_xe_2013_sp1.2.144/ipp/lib/intel64:/opt/intel/composer_xe_2013_sp1.2.144/compiler/lib/intel64:/opt/intel/composer_xe_2013_sp1.2.144/mkl/lib/intel64:/opt/intel/composer_xe_2013_sp1.2.144/tbb/lib/intel64/gcc4.4:/opt/sdsc/lib"

# activate virtenv
if test "default" = "anaconda"
then
    source activate /home/mingtha/radical.pilot.sandbox/ve.xsede.comet_ssh.0.47/
else
    . /home/mingtha/radical.pilot.sandbox/ve.xsede.comet_ssh.0.47/bin/activate
fi

# make sure rp_install is used
export PYTHONPATH=/home/mingtha/radical.pilot.sandbox/rp.session.two.mingtha.017452.0001/pilot.0238/rp_install/lib/python2.7/site-packages::/opt/sdsc/lib:/opt/sdsc/lib/python2.6/site-packages

# run agent in debug mode
# FIXME: make option again?
export SAGA_VERBOSE=DEBUG
export RADICAL_VERBOSE=DEBUG
export RADICAL_UTIL_VERBOSE=DEBUG
export RADICAL_PILOT_VERBOSE=DEBUG

# the agent will *always* use the dburl from the config file, not from the env
# FIXME: can we better define preference in the session ctor?
unset RADICAL_PILOT_DBURL

# avoid ntphost lookups on compute nodes
export RADICAL_PILOT_NTPHOST=46.101.140.169

# pass environment variables down so that module load becomes effective at
# the other side too (e.g. sub-agents).


# start agent, forward arguments
# NOTE: exec only makes sense in the last line of the script
exec /home/mingtha/radical.pilot.sandbox/ve.xsede.comet_ssh.0.47/bin/python /home/mingtha/radical.pilot.sandbox/rp.session.two.mingtha.017452.0001/pilot.0238/rp_install/bin/radical-pilot-agent "$1" 1>"$1.out" 2>"$1.err"

