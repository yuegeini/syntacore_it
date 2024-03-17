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
async def test_alu_add1(dut):
    test = ALUTB(dut)
    await test._drive_inputs(0x00000000, 0x00000000, ADD)
    await test._check_outputs(0x00000000, 0)

@cocotb.test()
async def test_alu_add2(dut):
    test = ALUTB(dut)
    await test._drive_inputs(0x00000001, 0xf0000001, ADD)
    await test._check_outputs(0xf0000002, 0)

@cocotb.test()
async def test_alu_add3(dut):
    test = ALUTB(dut)
    await test._drive_inputs(0xffffffff, 0x00000001, ADD)
    await test._check_outputs(0x00000000, 0)


@cocotb.test()
async def test_alu_add4(dut):
    test = ALUTB(dut)
    await test._drive_inputs(0xffffffff, 0x00000000, ADD)
    await test._check_outputs(0xffffffff, 0)


@cocotb.test()
async def test_alu_sub1(dut):
    test = ALUTB(dut)
    await test._drive_inputs(0x00000000, 0x00000002, SUB)
    await test._check_outputs(0xfffffffe, 0)

@cocotb.test()
async def test_alu_sub2(dut):
    test = ALUTB(dut)
    await test._drive_inputs(0x00000002, 0xfffffffe, SUB)
    await test._check_outputs(0x00000004, 0)

@cocotb.test()
async def test_alu_sub3(dut):
    test = ALUTB(dut)
    await test._drive_inputs(0x00000001, 0x00000002, SUB)
    await test._check_outputs(0xffffffff, 0)


@cocotb.test()
async def test_alu_sub4(dut):
    test = ALUTB(dut)
    await test._drive_inputs(0xffffffff, 0x00000001, SUB)
    await test._check_outputs(0xfffffffe, 0)