import math
import sys


def average(input_list):
    return float(sum(input_list)) / len(input_list)

def samp_std_dev(input_list):
    mean = average(input_list)

    sum_dist_from_mean = 0.0
    for point in input_list:
        sum_dist_from_mean += math.pow((point - mean), 2)

    samp_stdev = math.sqrt(sum_dist_from_mean / (len(input_list) - 1))
    return samp_stdev

def conf_interval(input_list, z=2.576):
   samp_stdev = samp_std_dev(input_list)
   conf_interval = z * samp_stdev / math.sqrt(len(input_list))
   return conf_interval


if __name__ == "__main__":
    sys.exit()
