import os
import sys
import csv
from math import sqrt
from pprint import pprint
from copy import deepcopy

import radical.utils     as ru
import radical.pilot     as rp
import radical.analytics as ra


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
                

def calc_wkd_timings(filepath, timestamp_fn):

    pilot_queue_times = list()
    unit_exec_times = list()

    with open(filepath+'/'+timestamp_fn) as f:
        reader = csv.reader(f)
        for row in reader:
            pilot_queue_times.append([float(row[1]), float(row[2])])
            unit_exec_times.append([float(row[3]), float(row[4])])

    collapsed_queue_times = ranges(pilot_queue_times)
    collapsed_exec_times = ranges(unit_exec_times)

    print "\ncollapsed queue times"
    print collapsed_queue_times, "\n"
    print "\ncollapsed exec times"
    print collapsed_exec_times, "\n"

    red_queue_range = remove_tx_olap_from_tq(collapsed_exec_times, collapsed_queue_times)
    print red_queue_range, collapsed_exec_times

    red_timings = [sum_all_ranges(red_queue_range), sum_all_ranges(collapsed_exec_times)]
    print "{},{}".format(red_timings[0], red_timings[1])

    return red_timings
    
    
if __name__ == "__main__":

    # Go to directory containing the directory of the profiles, then run this script,
    # where the argument is the name of the directory containing the profiles, but with
    # with no slash at the end

    start_path = os.getcwd()
    if 'baseline' in os.listdir(start_path):
        baseline_dir_ls = os.listdir(start_path+'/baseline')

        avg_ttq_timings = list()
        avg_ttx_timings = list()
        avg_ttc_timings = list()

        for listing in baseline_dir_ls:
            if listing.endswith('_cus'):
                
                num_cores = listing.split('_cus')[0]
                range_timings = list()

                ttc_timings = list()
                ttq_timings = list()
                ttx_timings = list()

                datapath = start_path+'/baseline/'+listing
                os.chdir(datapath)
                for timestamp_listing in os.listdir(datapath):
                    if timestamp_listing.startswith('timestamps'):
                        sid = "_".join(timestamp_listing.split('.')[0].split('_')[-2:])
                        sid_range_timing = [sid]

                        range_timing = calc_wkd_timings(datapath, timestamp_listing)

                        sid_range_timing.extend(range_timing)
                        range_timings.append(sid_range_timing)
                        ttq_timings.append(range_timing[0])
                        ttx_timings.append(range_timing[1])
                        ttc_timings.append(sum(range_timing))

                        print "printing"
                        print range_timings
                        print ttq_timings, ttx_timings, ttc_timings

                ttc_wkd_fn = 'ttc_wkd_'+num_cores+'.csv'
                with open(start_path+'/baseline/'+ttc_wkd_fn, 'w') as f:
                    writer = csv.writer(f)
                    for range_timing in range_timings:
                        writer.writerow(range_timing)

                avg_ttq_timing = [int(num_cores), avg(ttq_timings), samp_std(ttq_timings), conf_itv(ttq_timings)]
                avg_ttx_timing = [int(num_cores), avg(ttx_timings), samp_std(ttx_timings), conf_itv(ttx_timings)]
                avg_ttc_timing = [int(num_cores), avg(ttc_timings), samp_std(ttc_timings), conf_itv(ttc_timings)]

                avg_ttq_timings.append(avg_ttq_timing)
                avg_ttx_timings.append(avg_ttx_timing)
                avg_ttc_timings.append(avg_ttc_timing)

                os.chdir(start_path)

        avg_ttq_timings = sorted(avg_ttq_timings)
        avg_ttx_timings = sorted(avg_ttx_timings)
        avg_ttc_timings = sorted(avg_ttc_timings)

        with open(start_path+'/baseline/'+'avg_ttq_wkd.csv', 'w') as f:
            writer = csv.writer(f)
            for timing in avg_ttq_timings:
                writer.writerow(timing)

        with open(start_path+'/baseline/'+'avg_ttx_wkd.csv', 'w') as f:
            writer = csv.writer(f)
            for timing in avg_ttx_timings:
                writer.writerow(timing)

        with open(start_path+'/baseline/'+'avg_ttc_wkd.csv', 'w') as f:
            writer = csv.writer(f)
            for timing in avg_ttc_timings:
                writer.writerow(timing)

    else:
        print 'Need to be in the directory with the data from random selection that is in \
                the `baseline` directory'
