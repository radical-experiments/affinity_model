import sys
import csv
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

def sum_all_ranges(range_list):

    if range_list:
        total = 0
        for rng in range_list:
            total += rng[1] - rng[0]
        return total

def is_overlapping(range1, range2):

    range_len1 = range1[1] - range1[0]
    range_len2 = range2[1] - range2[0]
    combined_len = max(range1[1], range2[1]) - min(range1[0], range2[0])
    if combined_len < (range_len1 + range_len2):
        return True
    else:
        return False


def remove_tx_olap_from_tq(tx_ranges, tq_ranges):

    totally_idle_tq_ranges = list()

    queue_ranges = deepcopy(tq_ranges)
    #pprint(queue_ranges)

    for tx_range in tx_ranges:
        for i in range(len(queue_ranges)):
            queue_range = queue_ranges[i]
            if queue_range[0] == -1:
                pass
            if is_overlapping(queue_range, tx_range):
                if queue_range[0] > tx_range[0] and queue_range[1] < tx_range[1]:
                    # tq is contained in a tx range, set tq_range to [-1, -1] as null
                    queue_range = [-1, -1]
                elif queue_range[0] < tx_range[0] and queue_range[1] < tx_range[1]:
                    # tq starts before tx starts and ends before tx ends
                    queue_range[1] = tx_range[0]
                elif queue_range[0] > tx_range[0] and queue_range[1] > tx_range[1]:
                    # tq starts after tx starts and ends after tx ends
                    queue_range[0] = tx_range[1]
                else:
                    # tq starts before tx starts and ends after tx_ends
                    before_part = [queue_range[0], tx_range[0]]
                    after_part = [tx_range[1], queue_range[1]]
                    queue_ranges[i] = before_part
                    queue_ranges.insert(i+1, after_part)

    print "removing tx from tq"
    #pprint(queue_ranges)
    return queue_ranges
                

if __name__ == "__main__":

    # Go to directory containing the directory of the profiles, then run this script,
    # where the argument is the name of the directory containing the profiles, but with
    # with no slash at the end

    src = sys.argv[1]
    session = ra.Session(src, 'radical.pilot')

    relationships = session.describe('relations', ['pilot', 'unit'])
    pprint(relationships)

    rev_relationships = dict()
    for pilot_id, unit_list in relationships.iteritems():
        for unit_id in unit_list:
            rev_relationships[unit_id] = pilot_id
    pprint(rev_relationships)

    pilots = session.filter(etype='pilot', inplace=False)
    pilot_info = dict()
    pilot_queue_times = list()
    for pilot in pilots.get():
        try:
            wait_start = pilot.timestamps(rp.PMGR_ACTIVE_PENDING)[0]
            wait_end  = pilot.timestamps(rp.PMGR_ACTIVE)[0]
            pilot_info[pilot.uid] = { 'resource' : pilot.description['resource'], 
                                      'hostid' : pilot.cfg['hostid'],
                                      'wait_period' : [wait_start, wait_end],
                                      'units' : relationships[pilot.uid]}
            pilot_queue_times.append([wait_start, wait_end])
        except:
            pilot_info[pilot.uid] = { 'resource' : None, 
                                      'hostid' : pilot.cfg['hostid'],
                                      'wait_period' : [-1, -1]}
    pilot_queue_times = sorted(pilot_queue_times, key=lambda x: x[0])
    pprint(pilot_info)
    #pprint(pilot_queue_times)
    collapsed_queue_times = ranges(pilot_queue_times)

    units = session.filter(etype='unit', inplace=False)
    unit_info = dict()
    unit_exec_times = list()
    for unit in units.get():
        try:
            exec_start = unit.timestamps(rp.AGENT_EXECUTING)[0]
            exec_end  = unit.timestamps(rp.AGENT_STAGING_OUTPUT_PENDING)[0]
            #duration_exec = unit.duration([rp.AGENT_EXECUTING, rp.AGENT_STAGING_OUTPUT_PENDING])
            if (exec_end - exec_start) > 600.0:
                unit_info[unit.uid] = { 'exec_period' : [exec_start, exec_end],
                                        'pilot_id' : rev_relationships[unit.uid],
                                        'resource' : pilot_info[rev_relationships[unit.uid]]['resource'],
                                        'wait_period' : pilot_info[rev_relationships[unit.uid]]['wait_period']}
                unit_exec_times.append([exec_start, exec_end])
        except:
            unit_info[unit.uid] = { 'exec_period' : [-1, -1]}
    
    #unit_exec_times = sorted(unit_exec_times, key=lambda x: x[0])
    print

    pprint(unit_info)
    #pprint(unit_exec_times)
    collapsed_exec_times = ranges(unit_exec_times)

    # Some pilots may wait hang, and never execute a unit. This doesn't happen often, but
    #   can happen on OSG when pilots don't terminate correctly. Need to make sure we don't
    #   count pilots that wait but don't execute a unit by bounding the amount of time that
    #   we consider waiting with the timestamps of the last unit that finishes execution
    max_exec_timestamp = max([subrange[-1] for subrange in collapsed_exec_times])
    for subrange in collapsed_queue_times:
        subrange[1] = min(max_exec_timestamp, subrange[1])

    print "\ncollapsed queue times"
    print collapsed_queue_times, "\n"
    print "\ncollapsed exec times"
    print collapsed_exec_times, "\n"

    red_queue_range = remove_tx_olap_from_tq(collapsed_exec_times, collapsed_queue_times)
    print red_queue_range, collapsed_exec_times
    print "{},{}".format(sum_all_ranges(red_queue_range), sum_all_ranges(collapsed_exec_times))
    
    session_name = "_".join(src.split('/')[-1].split('.')[-2:])

    with open('timestamps_task_'+session_name+'.csv', 'w') as f:
        writer = csv.writer(f)
        for unit_id, unit_inf in unit_info.iteritems():
            if unit_inf['exec_period'][0] != -1:
                row = [unit_id, unit_inf['wait_period'][0], unit_inf['wait_period'][1], \
                       unit_inf['exec_period'][0], unit_inf['exec_period'][1], \
                       unit_inf['resource']]
                writer.writerow(row)

    with open('ttc_task_'+session_name+'.csv', 'w') as f:
        writer = csv.writer(f)
        for unit_id, unit_inf in unit_info.iteritems():
            print unit_inf
            if unit_inf['exec_period'][0] != -1:
                row = [unit_id, (unit_inf['wait_period'][1] - unit_inf['wait_period'][0]), \
                       (unit_inf['exec_period'][1] - unit_inf['exec_period'][0]), \
                       unit_inf['resource']]
                writer.writerow(row)
