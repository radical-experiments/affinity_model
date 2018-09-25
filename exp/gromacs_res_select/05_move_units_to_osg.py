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

rev_res_map = {
    'supermic'      : 'xsede.supermic',
    'bridges'       : 'xsede.bridges',
    'comet'         : 'xsede.comet_ssh',
    'osg'           : 'osg.xsede-virt-clust'
}


def avg(input_list):
    if len(input_list) == 0:
        return 0.0
    return sum(input_list) / float(len(input_list))

def samp_std(input_list):
    
    if len(input_list) < 2:
        return 0.0

    samp_std = 0.0
    mean = avg(input_list)
    for elem in input_list:
        samp_std += (elem - mean) * (elem - mean)
    samp_std /= (float(len(input_list)) - 1.0)
    samp_std = sqrt(samp_std)
    return samp_std

def conf_itv(input_list):
    if len(input_list) == 0:
        return 0.0
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


def get_max_timestamp_unit(res_unit_timings, time_comp=None):
    
    if time_comp == 'tq':
        idx = 1
    elif time_comp == 'ttc':
        idx = 3
    else:
        print "specify tq or ttc"

    max_unit_id = ""
    max_timestamp = 0.0
    for unit_id, timings in res_unit_timings.iteritems():
        if timings[idx] > max_timestamp:
            max_timestamp = timings[idx]
            max_unit_id = unit_id
    return max_unit_id


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

    # This is the largest TTC timestamp of all units executed on OSG
    osg_max_ttc_timestamp = get_max_timestamp(unit_timings['osg'], time_comp='ttc')
    osg_max_ttc_unit_id = get_max_timestamp_unit(unit_timings['osg'], time_comp='ttc')
    osg_max_ttc_unit = unit_timings['osg'][osg_max_ttc_unit_id]

    # Check if units move from any HPC to OSG because the TTC of units from 
    #   any HPC was greater than the max TTC of units on OSG
    print "******* IF TTC_TASK,SUPER > MAX(TTC_TASK,OSG) *******"
    print timestamp_fn
    if 'bridges' in unit_timings.keys():
        bridges_to_osg_ttc = get_units_timestamp_larger_than(osg_max_ttc_timestamp,
                                unit_timings['bridges'], time_comp='ttc')
        #print "Bridges"
        #pprint(bridges_to_osg_ttc)
    if 'comet' in unit_timings.keys():
        comet_to_osg_ttc = get_units_timestamp_larger_than(osg_max_ttc_timestamp,
                                unit_timings['comet'], time_comp='ttc')
        #print "Comet"
        #pprint(comet_to_osg_ttc)
    if 'supermic' in unit_timings.keys():
        supermic_to_osg_ttc = get_units_timestamp_larger_than(osg_max_ttc_timestamp,
                                unit_timings['supermic'], time_comp='ttc')
        #print "SuperMIC"
        #pprint(supermic_to_osg_ttc)

    bridges_pct_ttc_reds = list()
    comet_pct_ttc_reds = list()
    supermic_pct_ttc_reds = list()

    osg_max_ttc = osg_max_ttc_unit[3] - osg_max_ttc_unit[0]
    if bridges_to_osg_ttc:
        for unit_id in bridges_to_osg_ttc.keys():
            print "bridges_to_osg"
            unit_ttc = unit_timings['bridges'][unit_id][3] - unit_timings['bridges'][unit_id][0]
            pct_ttc_red = (unit_ttc - osg_max_ttc) / unit_ttc * 100.0
            bridges_pct_ttc_reds.append(pct_ttc_red)
            unit_timings['bridges'][unit_id] = osg_max_ttc_unit
    if comet_to_osg_ttc:
        for unit_id in comet_to_osg_ttc.keys():
            print "comet_to_osg"
            unit_ttc = unit_timings['comet'][unit_id][3] - unit_timings['comet'][unit_id][0]
            pct_ttc_red = (unit_ttc - osg_max_ttc) / unit_ttc * 100.0
            comet_pct_ttc_reds.append(pct_ttc_red)
            unit_timings['comet'][unit_id] = osg_max_ttc_unit
    if supermic_to_osg_ttc:
        for unit_id in comet_to_osg_ttc.keys():
            unit_ttc = unit_timings['supermic'][unit_id][3] - unit_timings['supermic'][unit_id][0]
            pct_ttc_red = (unit_ttc - osg_max_ttc) / unit_ttc * 100.0
            supermic_pct_ttc_reds.append(pct_ttc_red)
            unit_timings['supermic'][unit_id] = osg_max_ttc_unit

    if bridges_pct_ttc_reds or comet_pct_ttc_reds or supermic_pct_ttc_reds:
        session_id = "_".join(timestamp_fn.split('.')[0].split('_')[1:])
        with open(filepath+'/move_to_osg_timestamp_'+session_id+'.csv', 'w') as f:
            writer = csv.writer(f)
            for res, res_timings in unit_timings.iteritems():
                for unit_id, unit_timings in res_timings.iteritems():
                    row_insert = [unit_id]
                    row_insert.extend(unit_timings)
                    row_insert.append(rev_res_map[res])
                    writer.writerow(row_insert)

    pprint(bridges_pct_ttc_reds)
    pprint(comet_pct_ttc_reds)
    pprint(supermic_pct_ttc_reds)
    #pprint(bridges_to_osg_ttc)
    #pprint(comet_to_osg_ttc)
    #pprint(supermic_to_osg_ttc)
    
    if bridges_pct_ttc_reds:
        print "just bridges"
        pprint(bridges_pct_ttc_reds)
    if comet_pct_ttc_reds:
        print "just comet"
        pprint(comet_pct_ttc_reds)

    print "\n\n\n"

    return bridges_pct_ttc_reds, comet_pct_ttc_reds, supermic_pct_ttc_reds



if __name__ == "__main__":

    # Go to directory containing the directory of the profiles, then run this script,
    # where the argument is the name of the directory containing the profiles, but with
    # with no slash at the end

    start_path = os.getcwd()
    if 'baseline' in os.listdir(start_path):
        baseline_dir_ls = os.listdir(start_path+'/baseline')

        avg_bridges_ttc_reds_f = open(start_path+'/baseline/bridges_to_osg_avg_pct_ttc_reds.csv', 'w')
        avg_bridges_reds_writer = csv.writer(avg_bridges_ttc_reds_f)
        avg_comet_ttc_reds_f = open(start_path+'/baseline/comet_to_osg_avg_pct_ttc_reds.csv', 'w')
        avg_comet_reds_writer = csv.writer(avg_comet_ttc_reds_f)
        avg_supermic_ttc_reds_f = open(start_path+'/baseline/supermic_to_osg_avg_pct_ttc_reds.csv', 'w')
        avg_supermic_reds_writer = csv.writer(avg_supermic_ttc_reds_f)

        all_bridges_ttc_reds_f = open(start_path+'/baseline/bridges_to_osg_all_pct_ttc_reds.csv', 'w')
        all_bridges_reds_writer = csv.writer(all_bridges_ttc_reds_f)
        all_comet_ttc_reds_f = open(start_path+'/baseline/comet_to_osg_all_pct_ttc_reds.csv', 'w')
        all_comet_reds_writer = csv.writer(all_comet_ttc_reds_f)
        all_supermic_ttc_reds_f = open(start_path+'/baseline/supermic_to_osg_all_pct_ttc_reds.csv', 'w')
        all_supermic_reds_writer = csv.writer(all_supermic_ttc_reds_f)

        for listing in baseline_dir_ls:
            if listing.endswith('_cus'):

                bridges_all_ttc_reds = list()
                comet_all_ttc_reds = list()
                supermic_all_ttc_reds = list()

                num_cores = listing.split('_cus')[0]

                bridges_ttc_reds_f = open(start_path+'/baseline/'+listing+'/bridges_to_osg_pct_ttc_reds.csv', 'w')
                bridges_ttc_reds_writer = csv.writer(bridges_ttc_reds_f)
                comet_ttc_reds_f = open(start_path+'/baseline/'+listing+'/comet_to_osg_pct_ttc_reds.csv', 'w')
                comet_ttc_reds_writer = csv.writer(comet_ttc_reds_f)
                supermic_ttc_reds_f = open(start_path+'/baseline/'+listing+'/supermic_to_osg_pct_ttc_reds.csv', 'w')
                supermic_ttc_reds_writer = csv.writer(supermic_ttc_reds_f)


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
                            bridges_ttc_red, comet_ttc_red, supermic_ttc_red = check_selection_strategy(datapath, timestamp_listing)

                            if bridges_ttc_red:
                                row_insert_bridges = [session_id]
                                row_insert_bridges.extend(bridges_ttc_red)
                                bridges_ttc_reds_writer.writerow(row_insert_bridges)
                                bridges_all_ttc_reds.extend(bridges_ttc_red)
                            if comet_ttc_red:
                                row_insert_comet = [session_id]
                                row_insert_comet.extend(comet_ttc_red)
                                comet_ttc_reds_writer.writerow(row_insert_comet)
                                comet_all_ttc_reds.extend(comet_ttc_red)
                            if supermic_ttc_red:
                                row_insert_supermic = [session_id]
                                row_insert_supermic.extend(supermic_ttc_red)
                                supermic_ttc_reds_writer.writerow(row_insert_supermic)
                                supermic_all_ttc_reds.extend(comet_ttc_red)

                bridges_ttc_reds_f.close()
                comet_ttc_reds_f.close()
                supermic_ttc_reds_f.close()

                if not bridges_all_ttc_reds:
                    bridges_all_ttc_reds = [0.0, 0.0]
                if not comet_all_ttc_reds:
                    comet_all_ttc_reds = [0.0, 0.0]
                if not bridges_all_ttc_reds:
                    supermic_all_ttc_reds = [0.0, 0.0]

                all_row_insert_bridges = [num_cores]
                all_row_insert_comet = [num_cores]
                all_row_insert_supermic = [num_cores]

                all_row_insert_bridges.extend(bridges_all_ttc_reds)
                all_row_insert_comet.extend(comet_all_ttc_reds)
                all_row_insert_supermic.extend(supermic_all_ttc_reds)

                all_bridges_reds_writer.writerow(all_row_insert_bridges)
                all_comet_reds_writer.writerow(all_row_insert_comet)
                all_supermic_reds_writer.writerow(all_row_insert_supermic)


                avg_row_insert_bridges = [num_cores, avg(bridges_all_ttc_reds), samp_std(bridges_all_ttc_reds), conf_itv(bridges_all_ttc_reds)]
                avg_row_insert_comet = [num_cores, avg(comet_all_ttc_reds), samp_std(comet_all_ttc_reds), conf_itv(comet_all_ttc_reds)]
                avg_row_insert_supermic = [num_cores, avg(supermic_all_ttc_reds), samp_std(supermic_all_ttc_reds), conf_itv(supermic_all_ttc_reds)]

                avg_bridges_reds_writer.writerow(avg_row_insert_bridges)
                avg_comet_reds_writer.writerow(avg_row_insert_comet)
                avg_supermic_reds_writer.writerow(avg_row_insert_supermic)

                os.chdir(start_path)

                # here, insert average pct improvement

        all_bridges_ttc_reds_f.close()
        all_comet_ttc_reds_f.close()
        all_supermic_ttc_reds_f.close()

        avg_bridges_ttc_reds_f.close()
        avg_comet_ttc_reds_f.close()
        avg_supermic_ttc_reds_f.close()

    else:
        print 'Need to be in the directory with the data from random selection that is in \
                the `baseline` directory'
