INSTRUCTIONS_ADDER = 8.
CYCLES_ADDER = 8.
CPI_ADDER = CYCLES_ADDER / INSTRUCTIONS_ADDER
INSTR_RATE_ADDER = INSTRUCTIONS_ADDER / CYCLES_ADDER

INSTRUCTIONS_MATMULT = 35.
CYCLES_MATMULT = 36.
CPI_MATMULT = CYCLES_MATMULT / INSTRUCTIONS_MATMULT
INSTR_RATE_MATMULT = INSTRUCTIONS_MATMULT / CYCLES_MATMULT

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
            "matmult/amarel/mem/shared",
            "gromacs/amarel/compute/run_1",
            "gromacs/amarel/compute/run_2",
            "gromacs/amarel/compute/run_3",
            "gromacs/amarel/compute/run_4",
            "gromacs/amarel/compute/run_5",
            "gromacs/amarel/compute/run_6",
            "gromacs/amarel/compute/run_7",
            "gromacs/amarel/compute/run_8",
            "gromacs/amarel/mem/run_1",
            "gromacs/amarel/mem/run_2",
            "gromacs/amarel/mem/run_3",
            "gromacs/amarel/mem/run_4",
            "gromacs/comet/run_1",
            "gromacs/comet/run_2",
            "gromacs/comet/run_3",
            "gromacs/comet/run_4",
            "gromacs/bridges/run_1",
            "gromacs/bridges/run_2",
            "gromacs/bridges/run_3",
            "gromacs/bridges/run_4"
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

cleaned_adder_filenames = [
					"timings_1000000",
					"timings_1000000000",
					"timings_10000000000",
					"timings_100000000000",
					"timings_250000000000",
					"timings_500000000000",
					"timings_750000000000",
					"timings_1000000000000"
					]

cleaned_matmult_filenames = [
						"timings_1000",
						"timings_2500",
						"timings_5000",
						"timings_7500",
						"timings_10000"
					]

measurements = [
                    "clkspeed",
                    "cpu_util",
                    "cycles_act",
                    "cycles_pred",
                    "cycles_prederr",
                    "cycles_speedup_cpi_adj",
                    "instr_act",
                    "instr_pred",
                    "instr_prederr",
                    "instr_rate",
                    "instr_rate_prederr",
                    "p2a_cycles",
                    "p2a_cycles_prederr",
                    "p2a_cycles_speedup_prederr_cpi_adj",
                    "time"
                    ]

set1_adder_dirs = [
            "adder/laptop/clkspeed_2-6",
            "adder/laptop/clkspeed_3-5",
            "adder/desktop/clkspeed_2-6",
            "adder/desktop/clkspeed_3-5"
				]

set1_matmult_dirs = [
					"matmult/laptop/clkspeed_2-6",
					"matmult/laptop/clkspeed_3-5",
					"matmult/desktop/clkspeed_2-6",
					"matmult/desktop/clkspeed_3-5"
					]

set2_adder_dirs = [
            "adder/amarel/compute/exclusive",
            "adder/amarel/compute/shared",
            "adder/amarel/mem/exclusive",
            "adder/amarel/mem/shared"
				]

set2_matmult_dirs = [
            "matmult/amarel/compute/exclusive",
            "matmult/amarel/compute/shared",
            "matmult/amarel/mem/exclusive",
            "matmult/amarel/mem/shared"
				]

plot_filenames = [
            "clkspeed.csv",
            "cycles_prederr.csv",
            "cycles.csv",
            "instr.csv",
            "instr_prederr.csv",
            "instr_rate.csv",
            "p2a_cycles.csv",
            "p2a_cycles_prederr.csv",
            "time.csv"
            ]

amarel_aggr_measurements = [
            "instr_rate",
            "p2a_cycles",
            "time"
            ]

gromacs_files = [
            "cycles",
            "instructions",
            "task_clock",
            "time"
            ]

gromacs_dirs = [
            "gromacs/amarel/compute/run_1",
            "gromacs/amarel/compute/run_2",
            "gromacs/amarel/compute/run_3",
            "gromacs/amarel/compute/run_4",
            "gromacs/amarel/compute/run_5",
            "gromacs/amarel/compute/run_6",
            "gromacs/amarel/compute/run_7",
            "gromacs/amarel/compute/run_8",
            "gromacs/amarel/mem/run_1",
            "gromacs/amarel/mem/run_2",
            "gromacs/amarel/mem/run_3",
            "gromacs/amarel/mem/run_4",
            "gromacs/comet/run_1",
            "gromacs/comet/run_2",
            "gromacs/comet/run_3",
            "gromacs/comet/run_4",
            "gromacs/bridges/run_1",
            "gromacs/bridges/run_2",
            "gromacs/bridges/run_3",
            "gromacs/bridges/run_4"
            ]

set3_dirs = [
            "gromacs/amarel/compute",
            "gromacs/amarel/mem",
            "gromacs/comet",
            "gromacs/bridges"
            ]
