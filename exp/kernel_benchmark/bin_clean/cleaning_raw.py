import os
import sys
import csv


perf_output_format = {
    "laptop" : [16, 3, 7, 10, 14],
    "desktop" : [16, 3, 7, 10, 14],
    "amarel" : [14, 3, 7, 8, 12]
}

def extract_from_perf(src_pathname, filename, dst_pathname, machine, kernel_type):

    data_array = list()
    title = ['cpu_util', 'cycles', 'clkspeed', 'instr', 'instr_rate','time']
    data_array.append(title)

    with open(src_pathname+'/'+filename, 'r') as f:

        txt_block = perf_output_format[machine][0]
        cpu_utilized = perf_output_format[machine][1]
        cycles = perf_output_format[machine][2]
        instructions = perf_output_format[machine][3]
        time = perf_output_format[machine][4]

        i = 0
        for row in f:
            if (row != '' and row != '\n') and i == 0:
                cpu_utilized -= 1
                cycles -= 1
                instructions -= 1
                time -= 1

            tmp_row = row.strip()
            if i % txt_block == 0:
                tmp_list = list()

            if i % txt_block == cpu_utilized:
                pass
                cpu_util = row.strip().split('#')[1].lstrip().split()[0]
                tmp_list.append(float(cpu_util))

            if i % txt_block == cycles:
                cycles_str = tmp_row.split('#')
                total_cycles_commas = cycles_str[0].rstrip().split()[0]
                split_comma = total_cycles_commas.split(',')
                total_cycles = ''.join(split_comma)
                clock_speed = cycles_str[1].lstrip().split()[0]
                tmp_list.append(int(total_cycles))
                tmp_list.append(float(clock_speed))

            if i % txt_block == instructions:
                instr_str = tmp_row.split('#')
                total_instr_comma = instr_str[0].lstrip().split()[0]
                split_comma = total_instr_comma.split(',')
                total_instr = ''.join(split_comma)
                instr_rate = instr_str[1].rstrip().split()[0]
                tmp_list.append(int(total_instr))
                tmp_list.append(float(instr_rate))

            if i % txt_block == time:
                run_time = tmp_row.split()[0]
                tmp_list.append(float(run_time))

            if i % txt_block == (txt_block - 1):
                data_array.append(tmp_list)
            
            i += 1

    if machine == "amarel":
        if kernel_type == "adder" or kernel_type == "matmult":
			num_iterations = filename.split('/')[-1].split('_')[-1]
        elif kernel_type == "synapse":
			num_iterations = filename.split('/')[-2].split('_')[-1]
        else:
            pass
    else:
        num_iterations = filename.split('/')[-1].split('_')[-1]

    out_filename = "timings_" + num_iterations + ".csv"

    with open(dst_pathname+'/'+out_filename, 'w') as f:
        writer = csv.writer(f)
        for row in data_array:
            writer.writerow(row)



dirnames = [
            "adder/laptop/clkspeed_2-6",
            "adder/laptop/clkspeed_3-5",
            "adder/desktop/clkspeed_2-6",
            "adder/desktop/clkspeed_3-5",
            "matmult/laptop/clkspeed_2-6",
            "matmult/laptop/clkspeed_3-5",
            "matmult/desktop/clkspeed_2-6",
            "matmult/desktop/clkspeed_3-5",
            "adder/amarel/compute/exclusive",
            "adder/amarel/compute/shared",
            "adder/amarel/mem/exclusive",
            "adder/amarel/mem/shared",
            "matmult/amarel/compute/exclusive",
            "matmult/amarel/compute/shared",
            "matmult/amarel/mem/exclusive",
            "matmult/amarel/mem/shared"
            ]

adder_filenames = [
					"perfstat_1000000",
					"perfstat_1000000000",
					"perfstat_10000000000",
					"perfstat_100000000000",
					"perfstat_250000000000",
					"perfstat_500000000000",
					"perfstat_750000000000",
					"perfstat_1000000000000"
					]

matmult_filenames = [
						"perfstat_1000",
						"perfstat_2500",
						"perfstat_5000",
						"perfstat_7500",
						"perfstat_10000"
					]

def clean_data(src_path, dst_path):

    for dirname in dirnames:
        if not os.path.isdir(src_path+'/'+dirname):
            print "test"
            continue

        print dirname.split('/')
        dir_keywords = dirname.split('/')
        kernel = dir_keywords[0]
        hostenv = dir_keywords[1]

        if hostenv == "amarel":
            session_dirs = os.listdir(src_path+'/'+dirname)
            for session in session_dirs:
                if kernel == "adder":
                    for perf_file in adder_filenames:
                        extract_from_perf(src_path+'/'+dirname+'/'+session, perf_file, dst_path+'/'+dirname+'/'+session, hostenv, kernel)
                elif kernel == "matmult":
                    for perf_file in matmult_filenames:
                        extract_from_perf(src_path+'/'+dirname+'/'+session, perf_file, dst_path+'/'+dirname+'/'+session, hostenv, kernel)

        elif (hostenv == "laptop") or (hostenv == "desktop"):
            if kernel == "adder":
                for perf_file in adder_filenames:
                    extract_from_perf(src_path+'/'+dirname, perf_file, dst_path+'/'+dirname, hostenv, kernel)
            elif kernel == "matmult":
                for perf_file in matmult_filenames:
                    extract_from_perf(src_path+'/'+dirname, perf_file, dst_path+'/'+dirname, hostenv, kernel)

    


if __name__ == "__main__":
   
    src_path = sys.argv[1]
    dst_path = sys.argv[2]
    clean_data(src_path, dst_path) 
