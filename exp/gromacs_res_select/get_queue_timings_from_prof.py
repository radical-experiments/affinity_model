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

    src = sys.argv[1]
    session = ra.Session(src, 'radical.pilot')

    pilots = session.filter(etype='pilot', inplace=False)
    pilot_info = dict()
    pilot_queue_times = list()
    for pilot in pilots.get():
        try:
            wait_start = pilot.timestamps(rp.PMGR_ACTIVE_PENDING)[0]
            wait_end  = pilot.timestamps(rp.PMGR_ACTIVE)[0]
            pilot_info[pilot.uid] = { 'resource' : pilot.description['resource'], 
                                      'hostid' : pilot.cfg['hostid'],
                                      'wait_period' : [wait_start, wait_end]}
            pilot_queue_times.append([wait_start, wait_end])
        except:
            pilot_info[pilot.uid] = { 'resource' : None, 
                                      'hostid' : pilot.cfg['hostid'],
                                      'wait_period' : [-1, -1]}
    pilot_queue_times = sorted(pilot_queue_times, key=lambda x: x[0])
    pprint(pilot_info)
    pprint(pilot_queue_times)

    session_name = '_'.join(src.split('/')[-1].split('.')[-2:])
    with open('tq_task_'+session_name+'.csv', 'w') as f:
        writer = csv.writer(f)
        for pilot_id, pilot_inf in pilot_info.iteritems():
            print pilot_inf
            if pilot_inf['wait_period'][0] != -1:
                row = [pilot_id, (pilot_inf['wait_period'][1] - pilot_inf['wait_period'][0]), \
                       pilot_inf['resource']]
                writer.writerow(row)
