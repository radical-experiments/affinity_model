import os
import sys
import json
import random
import radical.pilot as rp
import saga.url as surl
import saga.utils.pty_shell as sups

SAMPLE_SIZE = 10
WALLTIME = 60   #In minutes
OVERHEAD = 5    #Overhead incurred throughout the process
CORES = 16
UTIL = 1        #Percent of Cores Utilized

def job_select():
    pass    

if sys.argv[1] == "stampede" or sys.argv[1] == "gordon" or sys.argv[1] == "comet" or sys.argv[1] == "supermic":
    res = sys.argv[1]
    random.seed()
else:
    sys.exit()


for run in range(SAMPLE_SIZE):

    with open('resource_handle.json') as j:
        conf = json.load(j)

    res_conf = conf[res]

    try:    
        session = rp.Session()
        session_id = session.uid
        pmgr = rp.PilotManager(session=session)
        pdescs = list()
    
        pd_init = { 'resource'      :   res_conf['name'],
                    'queue'         :   res_conf['queue'],
                    'access_schema' :   res_conf['access_schema'],
                    'cores'         :   CORES,
                    'runtime'       :   WALLTIME,
                    'project'       :   'TG-MCB090174'
                  }

        if res == 'gordon':
            pd_init['project'] = 'TG-DPP160003'

        pdescs.append(rp.ComputePilotDescription(pd_init))
        pilots = pmgr.submit_pilots(pdescs)
    
        umgr = rp.UnitManager(session=session)
        umgr.add_pilots(pilots)
    
        cuds = list()
        
        for task in range(CORES * UTIL):
            cud = rp.ComputeUnitDescription()
            #cud.pre_exec = ['module load python', 'source $HOME/bin/ve.synapse/bin/activate']
            #cud.executable = 'module load python; source $HOME/bin/ve.synapse/bin/activate; aimes-skeleton-synapse.py serial flops 1 1715750072310 65536 65536 0 0 0'
            cud.executable = 'module load python; source $HOME/bin/ve.synapse/bin/activate; aimes-skeleton-synapse.py serial flops 1 0 65536 65536 0 0 0'
            #cud.executable = 'aimes-skeleton-synapse.py'
            #cud.arguments = ['serial', 'flops', '1', '1715750072310', '65536', '65536', '0', '0', '0']
            cuds.append(cud)
    
        umgr.submit_units(cuds)
        umgr.wait_units()

    except Exception as e:
        print "Caught Exception %s\n" % e

    except(KeyboardInterrupt, SystemExit) as e:
        print "Caught A Keyboard Error"

    finally:
        os.system("radicalpilot-close-session -m export -s {0}".format(session_id))
        os.system("mv {0} {1}".format(session_id, res))
        os.system("mv {0}.json {1}/{0}".format(session_id, res))
        session.close(cleanup=False)
