import os
import sys
import json
import random
from pprint import pprint
import radical.pilot as rp

SAMPLE_SIZE = 1
WALLTIME = 60   #In minutes
OVERHEAD = 5    #Overhead incurred throughout the process
CORES = 20
UTIL = 1        #Percent of Cores Utilized


for run in range(SAMPLE_SIZE):

    with open('resource_handle.json') as j:
        conf = json.load(j)

    cu_per_pilot = [0 for res in conf]
    num_pilots = len(cu_per_pilot)

    random.seed()
    for i in range(CORES):
        pilot_id = random.randint(0, num_pilots - 1)
        cu_per_pilot[pilot_id] += 1

    res = conf.keys()
    try:    
        session = rp.Session()
        session_id = session.uid

        print "Initializing pmgrs, pilots, units\n"
        #pmgr_list = [rp.PilotManager(session=session) for i in range(num_pilots)]
        pmgr = rp.PilotManager(session=session)
        umgr_list = [rp.UnitManager(session=session) for i in range(num_pilots)]
        pilot_list = ["" for i in range(num_pilots)]

        print "Defining pmgrs, pilots, units\n"
        # Creating all pmgr's, pilots, umgr's, and associate each pilot with one pmgr and umgr
        for i in range(num_pilots):

            # Creating list of pilot descriptions (currently only one, general enough to support multiple pilots)
            pdescs = list()

            # Getting configuration for resoure i
            res_conf = conf[res[i]]
    
            pd_init = { 'resource'      :   res_conf['name'],
                        'queue'         :   res_conf['queue'],
                        'access_schema' :   res_conf['access_schema'],
                        'cores'         :   cu_per_pilot[i],
                        'runtime'       :   WALLTIME,
                        'project'       :   'TG-MCB090174'
                      }

            pdescs.append(rp.ComputePilotDescription(pd_init))

            # Associating pilot i with pmgr i
            pilot_list[i] = pmgr.submit_pilots(pdescs)
    
            # Associating pilot i with umgr i
            umgr_list[i].add_pilots(pilot_list[i])
        
        
        print "Creating and submitting CUs\n"
        # Create CUs (number of CUs randomly generated above), and submit to umgr i
        for i in range(num_pilots):    
            cuds = list()
            for task in range(cu_per_pilot[i]):
                cud = rp.ComputeUnitDescription()
                #cud.pre_exec = ['module load python', 'source $HOME/bin/ve.synapse/bin/activate']
                cud.executable = 'module load python; source $HOME/bin/ve.synapse/bin/activate; aimes-skeleton-synapse.py serial flops 1 1715750072310 65536 65536 0 0 0'
                #cud.executable = 'aimes-skeleton-synapse.py'
                #cud.arguments = ['serial', 'flops', '1', '1715750072310', '65536', '65536', '0', '0', '0']
                cuds.append(cud)
            
            umgr_list[i].submit_units(cuds)
       
        print "Waiting for units to finish\n"
        # Wait for units on all pilots to reach finish state. wait_units() is a blocking
        # call which waits for all CUs of a umgr reach a finish state [DONE, CANCELED, FAILED]
        # The loop checks each umgr. If umgr has unfinished pilot, then wait_units() blocks.
        # Otherwise, the function returns.
        for i in range(num_pilots):
            umgr_list[i].wait_units()

        print "Waiting for pilots to return (land) gracefully\n"
        pmgr.wait_pilots()


    except Exception as e:
        print "Caught Exception %s\n" % e

    except(KeyboardInterrupt, SystemExit) as e:
        print "Caught A Keyboard Error"

    finally:
        os.system("radicalpilot-close-session -m export -s {0}".format(session_id))
        os.system("mv {0} results".format(session_id))
        os.system("mv {0}.json results/{0}".format(session_id))
        session.close(cleanup=False)
