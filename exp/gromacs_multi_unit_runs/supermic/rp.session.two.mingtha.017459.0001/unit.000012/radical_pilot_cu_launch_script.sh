#!/bin/sh


# Environment variables
export RP_SESSION_ID="rp.session.two.mingtha.017459.0001"
export RP_PILOT_ID="pilot.0000"
export RP_AGENT_ID="agent_0"
export RP_SPAWNER_ID="agent.executing.0.child"
export RP_UNIT_ID="unit.000012"
export RP_GTOD="/worka/work/mha/radical.pilot.sandbox/rp.session.two.mingtha.017459.0001/pilot.0000/gtod"
export RP_PROF="/worka/work/mha/radical.pilot.sandbox/rp.session.two.mingtha.017459.0001/pilot.0000/unit.000012/PROF"
export RP_TMP="None"


touch $RP_PROF
echo "`$RP_GTOD`,unit_script,unit.000012,AGENT_EXECUTING,start_script," >> $RP_PROF

# Change to unit sandbox
cd /worka/work/mha/radical.pilot.sandbox/rp.session.two.mingtha.017459.0001/pilot.0000/unit.000012
echo "`$RP_GTOD`,unit_script,unit.000012,AGENT_EXECUTING,after_cd," >> $RP_PROF

# Pre-exec commands
echo "`$RP_GTOD`,unit_script,unit.000012,AGENT_EXECUTING,pre_start," >> $RP_PROF
/bin/true ||  (echo "pre_exec failed"; false) || exit
echo "`$RP_GTOD`,unit_script,unit.000012,AGENT_EXECUTING,pre_stop," >> $RP_PROF

# The command to run
/home/mha/bin/gromacs_pinned.sh
RETVAL=$?
echo "`$RP_GTOD`,unit_script,unit.000012,AGENT_EXECUTING,after_exec," >> $RP_PROF

# Exit the script with the return code from the command
exit $RETVAL
