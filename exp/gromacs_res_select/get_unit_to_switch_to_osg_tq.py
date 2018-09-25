from pprint import pprint
import os
import sys
import csv

res_map = {
    'xsede.supermic'        : 'supermic',
    'xsede.bridges'         : 'bridges',
    'xsede.comet_ssh'       : 'comet',
    'osg.xsede-virt-clust'  : 'osg'
}

def get_max_tx_timestamp(res_unit_timings):
    max_timestamp = 0.0
    for unit_id, timings in res_unit_timings.iteritems():
        if timings[3] > max_timestamp:
            max_timestamp = timings[3]
    return max_timestamp

def cmp_tq_timestamp_tx_timestamp(max_timestamp, res_unit_timings):
    unit_wait_move_new_res = dict()
    for unit_id, timings in res_unit_timings.iteritems():
        if timings[1] > max_timestamp:
            unit_wait_move_new_res[unit_id] = timings
    return unit_wait_move_new_res

def cmp_tq_increase(max_timestamp, unit_wait_move_new_res):
    
    tq_perf_pct = list()
    for unit_id, timings in unit_wait_move_new_res.iteritems():
        tq_move_red = 100.0 * abs(timings[1] - max_timestamp) / timings[1]
        tq_perf_pct.append(tq_move_red)
    return tq_perf_pct


if __name__ == "__main__":

    src_file = sys.argv[1]
    unit_timings = dict()

    with open(src_file) as f:
        reader = csv.reader(f)

        for row in reader:
            if res_map[row[-1]] not in unit_timings:
                unit_timings[res_map[row[-1]]] = dict()
            unit_timings[res_map[row[-1]]][row[0]] = map(float, row[1:5])
    pprint(unit_timings)

    osg_max_tx_timestamp = get_max_tx_timestamp(unit_timings['osg'])
    pprint(osg_max_tx_timestamp)
    print "****************"
    try:
        bridges_move_units = cmp_tq_timestamp_tx_timestamp(osg_max_tx_timestamp, unit_timings['bridges']) 
        print "Bridges"
        pprint(bridges_move_units)
    except:
        pass

    try:
        comet_move_units = cmp_tq_timestamp_tx_timestamp(osg_max_tx_timestamp, unit_timings['comet']) 
        print "Comet"
        pprint(comet_move_units)
    except:
        pass

    print "&&&&&&&&&&&&&&&&"
    try:
        bridges_perf_inc = cmp_tq_increase(osg_max_tx_timestamp, bridges_move_units)
        print "Bridges"
        pprint(bridges_perf_inc)
    except:
        pass

    try:
        comet_perf_inc = cmp_tq_increase(osg_max_tx_timestamp, comet_move_units) 
        print "Comet"
        pprint(comet_perf_inc)
    except:
        pass

    print "========="
