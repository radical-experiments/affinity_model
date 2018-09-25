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

def get_min_tq_timestamp(res_unit_timings):
    min_timestamp = 10000000000.0
    for unit_id, timings in res_unit_timings.iteritems():
        if timings[1] < min_timestamp:
            min_timestamp = timings[1]
    return min_timestamp

def get_max_ttc_timestamp(res_unit_timings):
    max_timestamp = 0.0
    for unit_id, timings in res_unit_timings.iteritems():
        if timings[3] > max_timestamp:
            max_timestamp = timings[3]
    return max_timestamp

def get_units_larger_ttc(max_timestamp, res_unit_timings):
    unit_wait_move_new_res = dict()
    for unit_id, timings in res_unit_timings.iteritems():
        if timings[3] > max_timestamp:
            unit_wait_move_new_res[unit_id] = timings
    return unit_wait_move_new_res

def get_units_smaller_tq(min_timestamp, res_unit_timings):
    unit_wait_move_new_res = dict()
    for unit_id, timings in res_unit_timings.iteritems():
        if timings[1] < min_timestamp:
            unit_wait_move_new_res[unit_id] = timings
    return unit_wait_move_new_res

def cmp_ttc_increase(max_timestamp, unit_wait_move_new_res):
    
    ttc_perf_pct = list()
    for unit_id, timings in unit_wait_move_new_res.iteritems():
        ttc_move_red = 100.0 * abs(timings[3] - max_timestamp) / timings[3]
        ttc_perf_pct.append(ttc_move_red)
    return ttc_perf_pct


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


    bridges_max_ttc_timestamp = get_max_ttc_timestamp(unit_timings['bridges'])
    bridges_min_tq_timestamp = get_min_tq_timestamp(unit_timings['bridges'])
    comet_max_ttc_timestamp = get_max_ttc_timestamp(unit_timings['comet'])
    comet_min_tq_timestamp = get_min_tq_timestamp(unit_timings['comet'])

    print "Bridges: {}, {}".format(bridges_max_ttc_timestamp, bridges_min_tq_timestamp)
    print "Comet: {}, {}".format(comet_max_ttc_timestamp, comet_min_tq_timestamp)

    print "****************"
    print "units on OSG with longer TTC than on Bridges or Comet, but shorter Tq than on Bridges or Comet"
    try:
        osg_units_ttc_greater_bridges = get_units_larger_ttc(bridges_max_ttc_timestamp, unit_timings['osg'])
        osg_bridges_move_units = get_units_smaller_tq(bridges_min_tq_timestamp, osg_units_ttc_greater_bridges)
        print "Bridges"
        pprint(osg_bridges_move_units)
    except:
        pass

    try:
        osg_units_ttc_greater_comet = get_units_larger_ttc(comet_max_ttc_timestamp, unit_timings['osg'])
        osg_comet_move_units = get_units_smaller_tq(comet_min_tq_timestamp, osg_units_ttc_greater_comet)
        print "Comet"
        pprint(osg_comet_move_units)
    except:
        pass

    print "&&&&&&&&&&&&&&&&"
    try:
        bridges_perf_inc = cmp_ttc_increase(bridges_max_ttc_timestamp, osg_bridges_move_units)
        print "Bridges"
        pprint(bridges_perf_inc)
    except:
        pass

    try:
        comet_perf_inc = cmp_ttc_increase(comet_max_ttc_timestamp, osg_comet_move_units) 
        print "Comet"
        pprint(comet_perf_inc)
    except:
        pass

    print "================"
