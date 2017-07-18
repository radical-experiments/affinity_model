INSTRUCTIONS_ADDER = 8.
CYCLES_ADDER = 8.
CPI_ADDER = CYCLES_ADDER / INSTRUCTIONS_ADDER
INSTR_RATE_ADDER = INSTRUCTIONS_ADDER / CYCLES_ADDER

INSTRUCTIONS_MATMULT = 35.
CYCLES_MATMULT = 40.
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
                    "cycles",
                    "cycles_pred",
                    "cycles_prederr",
                    "instr",
                    "instr_pred",
                    "instr_prederr",
                    "instr_rate",
                    "instr_rate_prederr",
                    "p2a_cycles",
                    "p2a_cycles_prederr",
                    "cycles_speedup_cpi_adj",
                    "p2a_cycles_speedup_prederr_cpi_adj",
                    "time"
                    ]
