import cocotb
from cocotb.triggers import Timer
from cocotb.result import TestSuccess, TestFailure
from cocotb.result import TestFailure, TestSuccess
import cocotb.regression
ADD     = 0b0100
SUB     = 0b0101
SUB_LT  = 0b0110
SUB_LTU = 0b0111
SUB_EQ  = 0b1000
SUB_NE  = 0b1001
SUB_GE  = 0b1010
SUB_GE  = 0b1011
SUB_GEU = 0b1100
# Define the testbench class
class ALUTB(object):
    def __init__(self, dut):
        super().__init__()
        self.dut = dut

        # Create drivers for input signals
        self.exu2ialu_main_op1_i = dut.exu2ialu_main_op1_i
        self.exu2ialu_main_op2_i = dut.exu2ialu_main_op2_i
        self.exu2ialu_cmd_i = dut.exu2ialu_cmd_i
        self.ialu2exu_main_res_o = dut.ialu2exu_main_res_o
        self.ialu2exu_cmp_res_o = dut.ialu2exu_cmp_res_o


    @cocotb.coroutine
    def _drive_inputs(self, op1, op2, cmd):
        self.exu2ialu_main_op1_i.value = op1
        self.exu2ialu_main_op2_i.value = op2
        self.exu2ialu_cmd_i.value = cmd
        yield Timer(1, units="ns")
        

    @cocotb.coroutine
    def _check_outputs(self, expected_result, expected_cmp_res):
        yield Timer(10, units='ns')
        if self.ialu2exu_main_res_o.value != expected_result:
            raise TestFailure(f"Unexpected main result: {self.ialu2exu_main_res_o.value} (expected: {expected_result})")
        if self.ialu2exu_cmp_res_o.value != expected_cmp_res:
            raise TestFailure(f"Unexpected comparison result: {self.ialu2exu_cmp_res_o.value} (expected: {expected_cmp_res})")
        raise TestSuccess("Test passed")

    
@cocotb.test()
async def test_alu_sub(dut):
    test = ALUTB(dut)
    await test._drive_inputs(0x00000001, 0x00000001, SUB)
    await test._check_outputs(0x00000000, False)
@cocotb.test()
async def test_alu_add1(dut):
    test = ALUTB(dut)
    await test._drive_inputs(0x00000000, 0x00000000, ADD)
    await test._check_outputs(0x00000000, False)

@cocotb.test()
async def test_alu_add2(dut):
    test = ALUTB(dut)
    await test._drive_inputs(0x00000001, 0x00000001, ADD)
    await test._check_outputs(0x00000002, False)

@cocotb.test()
async def test_alu_add_carry(dut):
    test = ALUTB(dut)
    await test._drive_inputs(0x7fffffff, 0x00000001, ADD)
    await test._check_outputs(0x80000000, True)

@cocotb.test()
async def test_alu_sub(dut):
    test = ALUTB(dut)
    await test._drive_inputs(0x00000001, 0x00000001, SUB)
    await test._check_outputs(0x00000000, False)

@cocotb.test()
async def test_alu_sub_borrow(dut):
    test = ALUTB(dut)
    await test._drive_inputs(0x00000001, 0x00000002, SUB)
    await test._check_outputs(0xfffffffe, True)

@cocotb.test()
async def test_alu_slt(dut):
    test = ALUTB(dut)
    await test._drive_inputs(0x00000001, 0x00000002, SUB_LT)
    await test._check_outputs(1, False)

@cocotb.test()
async def test_alu_sltu(dut):
    test = ALUTB(dut)
    await test._drive_inputs(0x00000001, 0x00000002, SUB_LTU)
    await test._check_outputs(0, True)

@cocotb.test()
async def test_alu_slt_eq(dut):
    test = ALUTB(dut)
    await test._drive_inputs(0x00000001, 0x00000001, SUB_EQ)
    await test._check_outputs(1, True)

@cocotb.test()
async def test_alu_slt_ne(dut):
    test = ALUTB(dut)
    await test._drive_inputs(0x00000001, 0x00000002, SUB_NE)
    await test._check_outputs(1, False)

@cocotb.test()
async def test_alu_slt_ge(dut):
    test = ALUTB(dut)
    await test._drive_inputs(0x00000002, 0x00000001, SUB_GE)
    await test._check_outputs(0, True)

@cocotb.test()
async def test_alu_slt_geu(dut):
    test = ALUTB(dut)
    await test._drive_inputs(0x00000002, 0x00000001, SUB_GEU)
    await test._check_outputs(0, True)
