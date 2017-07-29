import os
import sys
import json
import csv
from pprint import pprint

from files_dir_mod import *

def id_machine_map(src_path):

    run_machine_map = dict()
    usage = ""
    for dirname in dirnames:
        if not os.path.isdir(src_path+'/'+dirname):
            #print "{} not a real dir".format(dirname)
            continue
            
        dir_keywords = dirname.split('/')
        pprint(dir_keywords)
        usage = dir_keywords[-1]
        if dir_keywords[1] == "amarel":
            sessions = os.listdir(src_path+'/'+dirname)

            for session in sessions:
                hostinfo = ""
                with open(src_path+'/'+dirname+'/'+session+'/'+"hostname") as f:
                    hostinfo = f.readline()
                hostname = hostinfo.split('.')[0]
                run_machine_map[session] = hostname

    #pprint(run_machine_map)

    with open("../machine_info/amarel_config.json") as j:
        amarel_conf = json.load(j)
    #pprint(amarel_conf)

    run_machine_spec = dict()
    for run_id, machine in run_machine_map.iteritems():
        machine_class = ""
        for mc in amarel_conf.keys():
            if machine[:len(mc)] == mc:
                machine_class = mc
        node_number = int(machine[len(machine_class):])
        mc_spec = amarel_conf[machine_class]
        for subclass, subclass_spec in mc_spec.iteritems():
            for nr in subclass_spec["node_num"]:
                node_range = map(int, nr.split('-'))
                if node_number >= node_range[0] and node_number <= node_range[1]:
                    run_machine_spec[run_id] = subclass_spec
                    run_machine_spec[run_id]['usage'] = usage
                    """
                    pprint(machine)
                    pprint(subclass)
                    pprint(subclass_spec)
                    pprint(node_range)
                    print
                    """
            #pprint(subclass_spec)
    pprint(run_machine_spec)

    with open("run_machine_map.json", "w") as j:
        json.dump(run_machine_spec, j, sort_keys=True, indent=4)


if __name__ == "__main__":
    
    src_path = sys.argv[1]
    id_machine_map(src_path)
