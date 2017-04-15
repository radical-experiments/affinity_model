import json
import subprocess
import sys
from pprint import pprint

folder = sys.argv[1]


def get_timings(session_json):
    with open(session_json) as j:
        j_file = json.load(j)
    
    try:
        state_history = j_file["pilot"][0]["statehistory"]
    except:
        print "Session: {0}, Something went very wrong with this run".format(session_json)
        return

    pilot_lifetime = dict()

    for state in range(len(state_history)):
        pilot_lifetime[state_history[state]["state"]] = state_history[state]["timestamp"]

    #for state in pilot_lifetime:
    #    if state != "PendingLaunch":
    #        pilot_lifetime[state] -= pilot_lifetime["PendingLaunch"]
    #pilot_lifetime["PendingLaunch"] = 0.0

    #print pilot_lifetime

    if "Active" in pilot_lifetime and "PendingActive" in pilot_lifetime:
        Tq = pilot_lifetime["Active"] - pilot_lifetime["PendingActive"]
    else:
        print "Session: {0}, There was no Tq".format(session_json)
        Tq = -1
        return

    if "Active" in pilot_lifetime:
        if "Canceled" in pilot_lifetime:
            Tx = pilot_lifetime["Canceled"] - pilot_lifetime["Active"]
        elif "Done" in pilot_lifetime:
            Tx = pilot_lifetime["Done"] - pilot_lifetime["Active"]
        else:
            unit_state_history = [j_file["unit"][i]["statehistory"][-1] for i in range(len(j_file["unit"]))]
            #pprint(unit_state_history)
            num_units_finished = j_file["pilot"][0]["description"]["cores"]
            if num_units_finished == len(unit_state_history):
                done_timings = [unit_state_history[i]["timestamp"] for i in range(num_units_finished)]
                #print done_timings
                max_done_timestamp = max(done_timings)
                #print max_done_timestamp
                Tx = max_done_timestamp - pilot_lifetime["Active"]
            else:
                print "Session: {0}, The pilot entered 'Failed' state, or did not reach a final state".format(session_json)
                Tx = -1
    else:
        print "Session: {0}, The pilot entered 'Failed' state before becoming Active".format(session_json)
        Tx = -1

    print "Session: {0}, Tx: {1}, Tq: {2}".format(session_json, Tx, Tq)

def get_unit_timings(session_json):
    pass

proc = subprocess.Popen(['ls ' + folder], stdout=subprocess.PIPE, shell=True)
(session_list, err) = proc.communicate()
session_list = session_list.split('\n')
del session_list[-1]
for session in session_list:
    get_timings(folder+"/"+session)
