#!/bin/sh


# Environment variables
export RP_SESSION_ID="rp.session.two.mingtha.017452.0001"
export RP_PILOT_ID="pilot.0238"
export RP_AGENT_ID="agent_0"
export RP_SPAWNER_ID="agent.executing.0.child"
export RP_UNIT_ID="unit.000270"
export RP_GTOD="/home/mingtha/radical.pilot.sandbox/rp.session.two.mingtha.017452.0001/pilot.0238/gtod"
export RP_PROF="/home/mingtha/radical.pilot.sandbox/rp.session.two.mingtha.017452.0001/pilot.0238/unit.000270/PROF"
export RP_TMP="/scratch/$USER/$SLURM_JOBID"


touch $RP_PROF
echo "`$RP_GTOD`,unit_script,unit.000270,AGENT_EXECUTING,start_script," >> $RP_PROF

# Change to unit sandbox
cd /home/mingtha/radical.pilot.sandbox/rp.session.two.mingtha.017452.0001/pilot.0238/unit.000270
echo "`$RP_GTOD`,unit_script,unit.000270,AGENT_EXECUTING,after_cd," >> $RP_PROF

# Pre-exec commands
echo "`$RP_GTOD`,unit_script,unit.000270,AGENT_EXECUTING,pre_start," >> $RP_PROF
module purge ||  (echo "pre_exec failed"; false) || exit
module load gromacs/5.1.2 ||  (echo "pre_exec failed"; false) || exit
echo "`$RP_GTOD`,unit_script,unit.000270,AGENT_EXECUTING,pre_stop," >> $RP_PROF

# The command to run
/home/mingtha/bin/gromacs_pinned.sh
RETVAL=$?
echo "`$RP_GTOD`,unit_script,unit.000270,AGENT_EXECUTING,after_exec," >> $RP_PROF

# Exit the script with the return code from the command
exit $RETVAL
