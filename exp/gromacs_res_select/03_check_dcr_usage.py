import os
import sys
import csv
from pprint import pprint
from copy import deepcopy

import radical.utils     as ru
import radical.pilot     as rp
import radical.analytics as ra



def if_all_dcrs_used(datapath, timestamps_fn):

    dcrs_used = list()
    with open(datapath+'/'+timestamps_fn) as f:
        reader = csv.reader(f)
        for row in reader:
            if row[-1] not in dcrs_used:
                dcrs_used.append(row[-1])
            if len(dcrs_used) == 4:
                return True
    return False

if __name__ == "__main__":

    # Go to directory containing the directory of the profiles, then run this script,
    # where the argument is the name of the directory containing the profiles, but with
    # with no slash at the end

    start_path = os.getcwd()
    if 'baseline' in os.listdir(start_path):
        baseline_dir_ls = os.listdir(start_path+'/baseline')
        for listing in baseline_dir_ls:
            if listing.endswith('_cus'):

                sessions_all_dcrs_used = list()
                datapath = start_path+'/baseline/'+listing
                os.chdir(datapath)
                for timestamp_listing in os.listdir(datapath):
                    if timestamp_listing.startswith('timestamp'):
                        print datapath+"/"+timestamp_listing
                        if if_all_dcrs_used(datapath, timestamp_listing):
                            session_name = '_'.join(timestamp_listing.split('.')[0].split('_')[-2:])
                            sessions_all_dcrs_used.append(session_name)
                
                with open(datapath+'/session_all_dcrs_used.csv', 'w') as f:
                    writer = csv.writer(f)
                    writer.writerow(sessions_all_dcrs_used)

                os.chdir(start_path)

    else:
        print 'Need to be in the directory with the data from random selection that is in \
                the `baseline` directory'
