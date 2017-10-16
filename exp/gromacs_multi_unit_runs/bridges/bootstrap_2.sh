#!/bin/sh

# some inspection for logging
hostname

# disable user site packages as those can conflict with our virtualenv
export PYTHONNOUSERSITE=True

# make sure we use the correct sandbox
cd /home/mha/radical.pilot.sandbox/rp.session.two.mingtha.017452.0001/pilot.0000

# apply some env settings as stored after running pre_bootstrap_1 commands
export PATH="/opt/packages/python/2_7_11_gcc/bin:/opt/packages/slurm/17.02.5/bin:/usr/mpi/gcc/openmpi-1.10.4-hfi/bin:/opt/packages/gcc/5.3.0/bin:/usr/lib64/qt-3.3/bin:/usr/lib64/ccache:/usr/local/bin:/bin:/usr/bin:/usr/bin:/usr/local/sbin:/usr/sbin:/opt/puppetlabs/puppet/bin:/opt/packages/slash2/psc/sbin:/opt/puppetlabs/bin:/home/mha/.local/bin:/home/mha/bin:/opt/puppetlabs/puppet/bin:/opt/packages/slash2/psc/sbin:/home/mha/.local/bin:/home/mha/bin"
export LD_LIBRARY_PATH="/opt/packages/python/2_7_11_gcc/lib:/usr/mpi/gcc/openmpi-1.10.4-hfi/lib64:/opt/packages/gcc/5.3.0/lib64:/opt/packages/gcc/5.3.0/lib"

# activate virtenv
if test "default" = "anaconda"
then
    source activate /home/mha/radical.pilot.sandbox/ve.xsede.bridges.0.47/
else
    . /home/mha/radical.pilot.sandbox/ve.xsede.bridges.0.47/bin/activate
fi

# make sure rp_install is used
export PYTHONPATH=/home/mha/radical.pilot.sandbox/rp.session.two.mingtha.017452.0001/pilot.0000/rp_install/lib/python2.7/site-packages::

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
exec /home/mha/radical.pilot.sandbox/ve.xsede.bridges.0.47/bin/python /home/mha/radical.pilot.sandbox/rp.session.two.mingtha.017452.0001/pilot.0000/rp_install/bin/radical-pilot-agent "$1" 1>"$1.out" 2>"$1.err"

