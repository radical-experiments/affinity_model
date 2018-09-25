import os
import sys
import csv
from math import sqrt
from pprint import pprint
from copy import deepcopy

import radical.utils     as ru
import radical.pilot     as rp
import radical.analytics as ra


res_map = {
    'xsede.supermic'        : 'supermic',
    'xsede.bridges'         : 'bridges',
    'xsede.comet_ssh'       : 'comet',
    'osg.xsede-virt-clust'  : 'osg'
}


def avg(input_list):
    return sum(input_list) / float(len(input_list))

def samp_std(input_list):
    
    samp_std = 0.0
    mean = avg(input_list)
    for elem in input_list:
        samp_std += (elem - mean) * (elem - mean)
    samp_std /= (float(len(input_list)) - 1.0)
    samp_std = sqrt(samp_std)
    return samp_std

def conf_itv(input_list):
    return 2.576 * samp_std(input_list) / sqrt(len(input_list))



def get_min_timestamp(res_unit_timings, time_comp=None):

    if time_comp == 'tq':
        idx = 1
    elif time_comp == 'ttc':
        idx = 3
    else:
        print "specify tq or ttc"

    min_timestamp = 100000000.0
    for unit_id, timings in res_unit_timings.iteritems():
        if timings[idx] < min_timestamp:
            min_timestamp = timings[idx]
    return min_timestamp


def get_max_timestamp(res_unit_timings, time_comp=None):

    if time_comp == 'tq':
        idx = 1
    elif time_comp == 'ttc':
        idx = 3
    else:
        print "specify tq or ttc"

    max_timestamp = 0.0
    for unit_id, timings in res_unit_timings.iteritems():
        if timings[idx] > max_timestamp:
            max_timestamp = timings[idx]
    return max_timestamp


def get_units_timestamp_larger_than(max_timestamp, res_unit_timings, time_comp=None):

    if time_comp == 'tq':
        idx = 1
    elif time_comp == 'ttc':
        idx = 3
    else:
        print "specify tq or ttc"

    unit_move_new_res = dict()
    for unit_id, timings in res_unit_timings.iteritems():
        if timings[idx] > max_timestamp:
            unit_move_new_res[unit_id] = timings
    return unit_move_new_res


def get_units_timestamp_smaller_than(min_timestamp, res_unit_timings, time_comp=None):

    if time_comp == 'tq':
        idx = 1
    elif time_comp == 'ttc':
        idx = 3
    else:
        print "specify tq or ttc"

    unit_move_new_res = dict()
    for unit_id, timings in res_unit_timings.iteritems():
        if timings[idx] < min_timestamp:
            unit_move_new_res[unit_id] = timings
    return unit_move_new_res


def cmp_ttc_increase(max_timestamp, unit_wait_move_new_res):
    
    ttc_perf_pct = list()
    for unit_id, timings in unit_wait_move_new_res.iteritems():
        ttc_move_red = 100.0 * abs(timings[3] - max_timestamp) / timings[3]
        ttc_perf_pct.append(ttc_move_red)
    return ttc_perf_pct



def check_selection_strategy(filepath, timestamp_fn):

    unit_timings = dict()
    with open(filepath+'/'+timestamp_fn) as f:
        reader = csv.reader(f)
        for row in reader:
            if res_map[row[-1]] not in unit_timings:
                unit_timings[res_map[row[-1]]] = dict()
            unit_timings[res_map[row[-1]]][row[0]] = map(float, row[1:5])
    #pprint(unit_timings)

    unit_movement = {   '01_ttc_super_gt_max_ttc_osg': list(),
                        '02_tq_super_gt_max_ttc_osg' : list(),
                        '03_tq_super_lt_max_ttc_osg' : list(),
                        '04_ttc_osg_gt_max_ttc_super': list(),
                        '05_tq_osg_gt_max_tq_super'  : list(),
                        '06_tq_osg_lt_max_tq_super'  : list()}

    # This is the largest TTC timestamp of all units executed on OSG
    osg_max_ttc_timestamp = get_max_timestamp(unit_timings['osg'], time_comp='ttc')

    # Check if units move from any HPC to OSG because the TTC of units from 
    #   any HPC was greater than the max TTC of units on OSG
    print "******* IF TTC_TASK,SUPER > MAX(TTC_TASK,OSG) *******"
    print timestamp_fn
    if 'bridges' in unit_timings.keys():
        bridges_to_osg_ttc = get_units_timestamp_larger_than(osg_max_ttc_timestamp,
                                unit_timings['bridges'], time_comp='ttc')
        if bridges_to_osg_ttc:
            unit_movement['01_ttc_super_gt_max_ttc_osg'].append('bridges')
        #print "Bridges"
        #pprint(bridges_to_osg_ttc)
    if 'comet' in unit_timings.keys():
        comet_to_osg_ttc = get_units_timestamp_larger_than(osg_max_ttc_timestamp,
                                unit_timings['comet'], time_comp='ttc')
        if comet_to_osg_ttc:
            unit_movement['01_ttc_super_gt_max_ttc_osg'].append('comet')
        #print "Comet"
        #pprint(comet_to_osg_ttc)
    if 'supermic' in unit_timings.keys():
        supermic_to_osg_ttc = get_units_timestamp_larger_than(osg_max_ttc_timestamp,
                                unit_timings['supermic'], time_comp='ttc')
        if supermic_to_osg_ttc:
            unit_movement['01_ttc_super_gt_max_ttc_osg'].append('supermic')
        #print "SuperMIC"
        #pprint(supermic_to_osg_ttc)


    # Check if units move from any HPC to OSG because the Tq of units from 
    #   any HPC was greater than the max TTC of units on OSG
    print "******* IF Tq_TASK,SUPER > MAX(TTC_TASK,OSG) *******"
    print timestamp_fn
    if 'bridges' in unit_timings.keys():
        bridges_to_osg_tq = get_units_timestamp_larger_than(osg_max_ttc_timestamp,
                                unit_timings['bridges'], time_comp='tq')
        if bridges_to_osg_tq:
            unit_movement['02_tq_super_gt_max_ttc_osg'].append('bridges')
        #print "Bridges"
        #pprint(bridges_to_osg_tq)
    if 'comet' in unit_timings.keys():
        comet_to_osg_tq = get_units_timestamp_larger_than(osg_max_ttc_timestamp,
                                unit_timings['comet'], time_comp='tq')
        if comet_to_osg_tq:
            unit_movement['02_tq_super_gt_max_ttc_osg'].append('comet')
        #print "Comet"
        #pprint(comet_to_osg_tq)
    if 'supermic' in unit_timings.keys():
        supermic_to_osg_tq = get_units_timestamp_larger_than(osg_max_ttc_timestamp,
                                unit_timings['supermic'], time_comp='tq')
        if supermic_to_osg_tq:
            unit_movement['02_tq_super_gt_max_ttc_osg'].append('supermic')
        #print "SuperMIC"
        #pprint(supermic_to_osg_tq)


    # Check if units move from HPC to OSG because TTC of units from any HPC
    #   was greater than the max TTC of units on OSG, but not the max Tq of
    #   units on OSG
    print "******* IF TTC_TASK,SUPER > MAX(TTC_TASK,OSG) AND Tq_TASK,SUPER < MAX(TTC_TASK,OSG) *******"
    print timestamp_fn
    if 'bridges' in unit_timings.keys():
        if bridges_to_osg_ttc and not bridges_to_osg_tq:
            bridges_to_osg_ttc_not_tq = bridges_to_osg_ttc
            unit_movement['03_tq_super_lt_max_ttc_osg'].append('bridges')
            #print "Bridges"
            #pprint(bridges_to_osg_ttc_not_tq)
    if 'comet' in unit_timings.keys():
        if comet_to_osg_ttc and not comet_to_osg_tq:
            comet_to_osg_ttc_not_tq = comet_to_osg_ttc
            unit_movement['03_tq_super_lt_max_ttc_osg'].append('comet')
            #print "Comet"
            #pprint(comet_to_osg_ttc_not_tq)
    if 'supermic' in unit_timings.keys():
        if supermic_to_osg_ttc and not supermic_to_osg_tq:
            supermic_to_osg_ttc_not_tq = supermic_to_osg_ttc
            unit_movement['03_tq_super_lt_max_ttc_osg'].append('supermic')
            #print "SuperMIC"
            #pprint(supermic_to_osg_ttc_not_tq)


    # These are the largest TTC timestamps of all units executed on the HPCs
    bridges_max_ttc_timestamp = get_max_timestamp(unit_timings['bridges'], time_comp='ttc')
    comet_max_ttc_timestamp = get_max_timestamp(unit_timings['comet'], time_comp='ttc')
    supermic_max_ttc_timestamp = get_max_timestamp(unit_timings['supermic'], time_comp='ttc')

    # Check if any units move from any HPC to OSG because the TTC of units from 
    #   OSG was greater than the max TTC of units from any HPC
    print "******* IF TTC_TASK,OSG > MAX(TTC_TASK,SUPER) *******"
    print timestamp_fn
    if 'bridges' in unit_timings.keys():
        osg_to_bridges_ttc = get_units_timestamp_larger_than(bridges_max_ttc_timestamp,
                                unit_timings['osg'], time_comp='ttc')
        if osg_to_bridges_ttc:
            unit_movement['04_ttc_osg_gt_max_ttc_super'].append('bridges')
        #print "Bridges"
        #pprint(osg_to_bridges_ttc)
    if 'comet' in unit_timings.keys():
        osg_to_comet_ttc = get_units_timestamp_larger_than(comet_max_ttc_timestamp,
                                unit_timings['osg'], time_comp='ttc')
        if osg_to_comet_ttc:
            unit_movement['04_ttc_osg_gt_max_ttc_super'].append('comet')
        #print "Comet"
        #pprint(osg_to_comet_ttc)
    if 'supermic' in unit_timings.keys():
        osg_to_supermic_ttc = get_units_timestamp_larger_than(supermic_max_ttc_timestamp,
                                unit_timings['osg'], time_comp='ttc')
        if osg_to_supermic_ttc:
            unit_movement['04_ttc_osg_gt_max_ttc_super'].append('supermic')
        #print "SuperMIC"
        #pprint(osg_to_supermic_ttc)


    # There are the smallest and largest Tq timestamps of all units executed
    #   on HPCs
    bridges_min_tq_timestamp = get_min_timestamp(unit_timings['bridges'], time_comp='tq')
    comet_min_tq_timestamp = get_min_timestamp(unit_timings['comet'], time_comp='tq')
    supermic_min_tq_timestamp = get_min_timestamp(unit_timings['supermic'], time_comp='tq')
    bridges_max_tq_timestamp = get_max_timestamp(unit_timings['bridges'], time_comp='tq')
    comet_max_tq_timestamp = get_max_timestamp(unit_timings['comet'], time_comp='tq')
    supermic_max_tq_timestamp = get_max_timestamp(unit_timings['supermic'], time_comp='tq')

    print "Bridges:\t{}".format(bridges_max_tq_timestamp - bridges_min_tq_timestamp)
    print "Comet:\t\t{}".format(comet_max_tq_timestamp - comet_min_tq_timestamp)
    print "SuperMIC:\t{}".format(supermic_max_tq_timestamp - supermic_min_tq_timestamp)
    # Check if any units move from any HPC to OSG because the TTC of units from 
    #   OSG was greater than the max TTC of units from any HPC, and because the 
    #   units Tq of units from OSG was greater than the max Tq of units from any
    #   any HPC
    print "******* IF TTC_TASK,OSG > MAX(TTC_TASK,SUPER) AND Tq_TASK,OSG > MAX(Tq,SUPER) *******"
    print timestamp_fn
    if 'bridges' in unit_timings.keys():
        osg_to_bridges_ttc = get_units_timestamp_larger_than(bridges_max_ttc_timestamp,
                                unit_timings['osg'], time_comp='ttc')
        osg_to_bridges_ttc_and_tq = get_units_timestamp_larger_than(bridges_max_tq_timestamp,
                                osg_to_bridges_ttc, time_comp='tq')
        if osg_to_bridges_ttc_and_tq:
            unit_movement['05_tq_osg_gt_max_tq_super'].append('bridges')
        #print "Bridges"
        #pprint(osg_to_bridges_ttc_and_tq)
    if 'comet' in unit_timings.keys():
        osg_to_comet_ttc = get_units_timestamp_larger_than(comet_max_ttc_timestamp,
                                unit_timings['osg'], time_comp='ttc')
        osg_to_comet_ttc_and_tq = get_units_timestamp_larger_than(comet_max_tq_timestamp,
                                osg_to_comet_ttc, time_comp='tq')
        if osg_to_comet_ttc_and_tq:
            unit_movement['05_tq_osg_gt_max_tq_super'].append('comet')
        #print "Comet"
        #pprint(osg_to_comet_ttc_and_tq)
    if 'supermic' in unit_timings.keys():
        osg_to_supermic_ttc = get_units_timestamp_larger_than(supermic_max_ttc_timestamp,
                                unit_timings['osg'], time_comp='ttc')
        osg_to_supermic_ttc_and_tq = get_units_timestamp_larger_than(supermic_max_tq_timestamp,
                                osg_to_supermic_ttc, time_comp='tq')
        if osg_to_supermic_ttc_and_tq:
            unit_movement['05_tq_osg_gt_max_tq_super'].append('supermic')
        #print "SuperMIC"
        #pprint(osg_to_supermic_ttc_and_tq)


    # Check if any units move from any HPC to OSG because the TTC of units from 
    #   OSG was greater than the max TTC of units from any HPC, but because the 
    #   units Tq of units from OSG was smaller than the max Tq of units from any
    #   any HPC
    print "******* IF TTC_TASK,OSG > MAX(TTC_TASK,SUPER) AND Tq_TASK,OSG < MAX(Tq,SUPER) *******"
    print timestamp_fn
    # TODO: Need to implement correct semantics
    if 'bridges' in unit_timings.keys():
        osg_to_bridges_ttc = get_units_timestamp_larger_than(bridges_max_ttc_timestamp,
                                unit_timings['osg'], time_comp='ttc')
        osg_to_bridges_ttc_not_tq = get_units_timestamp_smaller_than(bridges_max_tq_timestamp,
                                osg_to_bridges_ttc, time_comp='tq')
        if osg_to_bridges_ttc_not_tq:
            unit_movement['06_tq_osg_lt_max_tq_super'].append('bridges')
        #print "Bridges"
        #pprint(osg_to_bridges_ttc_not_tq)
    if 'comet' in unit_timings.keys():
        osg_to_comet_ttc = get_units_timestamp_larger_than(comet_max_ttc_timestamp,
                                unit_timings['osg'], time_comp='ttc')
        osg_to_comet_ttc_not_tq = get_units_timestamp_smaller_than(comet_max_tq_timestamp,
                                osg_to_comet_ttc, time_comp='tq')
        if osg_to_comet_ttc_not_tq:
            unit_movement['06_tq_osg_lt_max_tq_super'].append('comet')
        #print "Comet"
        #pprint(osg_to_comet_ttc_not_tq)
    if 'supermic' in unit_timings.keys():
        osg_to_supermic_ttc = get_units_timestamp_larger_than(supermic_max_ttc_timestamp,
                                unit_timings['osg'], time_comp='ttc')
        osg_to_supermic_ttc_not_tq = get_units_timestamp_smaller_than(supermic_max_tq_timestamp,
                                osg_to_supermic_ttc, time_comp='tq')
        if osg_to_supermic_ttc_not_tq:
            unit_movement['06_tq_osg_lt_max_tq_super'].append('supermic')
        #print "SuperMIC"
        #pprint(osg_to_supermic_ttc_not_tq)

    pprint(unit_movement)

    print "\n\n\n"

    bridges_movement = [0 for key in unit_movement.keys()]
    comet_movement = [0 for key in unit_movement.keys()]
    supermic_movement = [0 for key in unit_movement.keys()]
    total_movement = [0 for key in unit_movement.keys()]

    strat_counter = 0
    for strat in sorted(unit_movement.keys()):
        if 'bridges' in unit_movement[strat]:
            bridges_movement[strat_counter] = 1
            total_movement[strat_counter] += 1
        if 'comet' in unit_movement[strat]:
            comet_movement[strat_counter] = 1
            total_movement[strat_counter] += 1
        if 'supermic' in unit_movement[strat]:
            supermic_movement[strat_counter] = 1
            total_movement[strat_counter] += 1
        strat_counter += 1
    
    return bridges_movement, comet_movement, supermic_movement, total_movement


if __name__ == "__main__":

    # Go to directory containing the directory of the profiles, then run this script,
    # where the argument is the name of the directory containing the profiles, but with
    # with no slash at the end

    start_path = os.getcwd()
    if 'baseline' in os.listdir(start_path):
        baseline_dir_ls = os.listdir(start_path+'/baseline')

        bridges_movement_f = open(start_path+'/baseline/unit_movement_bridges.csv', 'w')
        comet_movement_f = open(start_path+'/baseline/unit_movement_comet.csv', 'w')
        supermic_movement_f = open(start_path+'/baseline/unit_movement_supermic.csv', 'w')
        total_movement_f = open(start_path+'/baseline/unit_movement_total.csv', 'w')

        b_movement_writer = csv.writer(bridges_movement_f)
        c_movement_writer = csv.writer(comet_movement_f)
        s_movement_writer = csv.writer(supermic_movement_f)
        t_movement_writer = csv.writer(total_movement_f)
	
        movement_row_header = ['session_id',
							   'ttc_super_gt_max_ttc_osg',
							   'tq_super_gt_max_ttc_osg',
							   'tq_super_lt_max_ttc_osg',
							   'ttc_osg_gt_max_ttc_super',
							   'tq_osg_gt_max_tq_super',
							   'tq_osg_lt_max_tq_super']
        b_movement_writer.writerow(movement_row_header)
        c_movement_writer.writerow(movement_row_header)
        s_movement_writer.writerow(movement_row_header)
        t_movement_writer.writerow(movement_row_header)


        for listing in baseline_dir_ls:
            if listing.endswith('_cus'):
                datapath = start_path+'/baseline/'+listing
                os.chdir(datapath)

                session_ids_used_all_dcrs = None
                with open(datapath+'/session_all_dcrs_used.csv') as f:
                    reader = csv.reader(f)
                    for row in reader:
                        session_ids_used_all_dcrs = row

                for timestamp_listing in os.listdir(datapath):
                    if timestamp_listing.startswith('timestamps'):
                        session_id = "_".join(timestamp_listing.split('.')[0].split('_')[1:])
                        if session_id in session_ids_used_all_dcrs:
                            b_movement, c_movement, s_movement, t_movement = check_selection_strategy(datapath, timestamp_listing)
                            b_movement.insert(0, session_id)
                            c_movement.insert(0, session_id)
                            s_movement.insert(0, session_id)
                            t_movement.insert(0, session_id)

                            b_movement_writer.writerow(b_movement)
                            c_movement_writer.writerow(c_movement)
                            s_movement_writer.writerow(s_movement)
                            t_movement_writer.writerow(t_movement)
                os.chdir(start_path)

        bridges_movement_f.close()
        comet_movement_f.close()
        supermic_movement_f.close()
        total_movement_f.close()

    else:
        print 'Need to be in the directory with the data from random selection that is in \
                the `baseline` directory'
