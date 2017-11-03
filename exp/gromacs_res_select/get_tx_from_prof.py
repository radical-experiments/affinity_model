import sys
from pprint import pprint
from copy import deepcopy

import radical.utils     as ru
import radical.pilot     as rp
import radical.analytics as ra


def ranges(range_list):

    if len(range_list) < 2:
        return range_list

    sorted_ranges = sorted(range_list, key=lambda x: x[0])

    collapsed_list = [sorted_ranges[0]]
    for i in range(1, len(sorted_ranges)):
        if sorted_ranges[i][0] > collapsed_list[-1][1]:
            collapsed_list.append(sorted_ranges[i])
        else:
            if sorted_ranges[i][1] > collapsed_list[-1][1]:
                collapsed_list[-1][1] = sorted_ranges[i][1]
    
    #pprint(collapsed_list)
    return collapsed_list


if __name__ == "__main__":

    src = sys.argv[1]
    session = ra.Session(src, 'radical.pilot')

    units = session.filter(etype='unit', inplace=False)
    unit_info = dict()
    unit_exec_timestamps = list()
    unit_exec_durations = list()
    for unit in units.get():
        try:
            exec_start = unit.timestamps(rp.AGENT_EXECUTING)[0]
            exec_end  = unit.timestamps(rp.AGENT_STAGING_OUTPUT_PENDING)[0]
            duration_exec = unit.duration([rp.AGENT_EXECUTING, rp.AGENT_STAGING_OUTPUT_PENDING])
            unit_info[unit.uid] = { 'exec_period' : [exec_start, exec_end]}
            if (exec_end - exec_start) > 600.0:
                unit_exec_timestamps.append([exec_start, exec_end])
                unit_exec_durations.append(duration_exec)
        except:
            unit_info[unit.uid] = { 'exec_period' : [-1, -1]}
    
    #unit_exec_timestamps = sorted(unit_exec_timestamps, key=lambda x: x[0])
    print
    #pprint(unit_info)
    pprint(unit_exec_timestamps)
    pprint(unit_exec_durations)
    avg_exec_durations = sum(unit_exec_durations) / len(unit_exec_durations)
    pprint(avg_exec_durations)
