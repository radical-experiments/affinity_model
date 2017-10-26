from math import sqrt, pow

def avg(input_list):
    return sum(input_list) / len(input_list)

def samp_std(input_list):
    average = avg(input_list)
    square_diff = [pow((elem - average), 2) for elem in input_list]
    sample_std = sqrt(sum(square_diff) / (len(input_list) - 1))
    return sample_std

def conf_itv(input_list, z=2.576):
    conf_itv_dist = z * samp_std(input_list) / sqrt(len(input_list))
    return conf_itv_dist

def pct_err(input_list, avg):
    pct_error = [(abs(elem - avg) / elem * 100.0)  for elem in input_list]
    return pct_error

def pct_err_list(input_list, avg_list):
    pct_error = [(abs(input_list[i] - avg_list[i]) / input_list[i] * 100.0)  for i in range(len(input_list))]
    return pct_error
