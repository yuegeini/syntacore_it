TOPLEVEL_LANG = verilog
VERILOG_SOURCES = scr1_pipe_ialu.sv
TOPLEVEL = scr1_pipe_ialu
MODULE := test_scr1_pipe_ialu
SIM ?= verilator
VERILATOR_ROOT ?= /home/yuegeini/ver/verilator
VERILATOR = $(VERILATOR_ROOT)/bin/verilator
VERILATOR_COVERAGE = $(VERILATOR_ROOT)/bin/verilator_coverage
 
COMPILE_ARGS = --coverage --trace
VERILATOR_INPUT = -f input.vc scr1_pipe_ialu.sv scr1_arch_description.svh scr1_riscv_isa_decoding.svh scr1_search_ms1.svh 
 
VERILATOR_COV_FLAGS += --annotate logs/annotated
# A single coverage hit is considered good enough
VERILATOR_COV_FLAGS += --annotate-min 1
# Create LCOV info
VERILATOR_COV_FLAGS += --write-info logs/coverage.info
# Input file from Verilator
VERILATOR_COV_FLAGS += coverage.dat

include $(shell cocotb-config --makefiles)/Makefile.sim
 
all: run waves
 
run:
	@rm -rf logs
	@mkdir -p logs
	@rm -rf logs/annotated
	$(VERILATOR_COVERAGE) $(VERILATOR_COV_FLAGS)
	genhtml logs/coverage.info --output-directory logs/html
waves:
	gtkwave dump.vcd