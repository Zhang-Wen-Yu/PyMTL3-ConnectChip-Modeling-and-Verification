# =========================================================================
#  JTAG Test Top
# =========================================================================

import pytest
from pymtl3.stdlib.test_utils import mk_test_case_table, run_sim
from pymtl3.stdlib.test_utils.test_srcs import TestSrcRTL
from pymtl3.stdlib.test_utils.test_sinks import TestSinkRTL
from Module.JTAG.jtag_pc.jtag_pc import *
from Module.JTAG.jtag_fpga.jtag_fpga import *

# -------------------------------------------------------------------------
# TestHarness
# -------------------------------------------------------------------------

jtag_resp_type = mk_jtag_resp_msg(1)
jtag_req_type  = mk_jtag_req_msg(1, 1)

# define the class
class TestHarness( Component ):

    def construct(s, flow_control):

       s.master = jtag_pc()
       s.slave  = jtag_fpga()

       # Instantiate models
       s.src  = TestSrcRTL(jtag_req_type)
       s.sink = TestSinkRTL(jtag_resp_type)

       # write the send interface and recv interface and connect
       s.src.send //= s.master.req
       s.master.resp //= s.sink.recv

       # write the port and connect
       s.master.ifc.TDI //= s.slave.ifc.TDI
       s.master.ifc.TDO //= s.slave.ifc.TDO
       s.master.ifc.TCK //= s.slave.ifc.TCK
       s.master.ifc.TMS //= s.slave.ifc.TMS

    # define the founction done and line_trace
    def done(s):
       return s.src.done() and s.sink.done()

    def line_trace(s):
       return s.slave.line_trace()


# -----------------------------------
# Test Case: basic
# -----------------------------------
basic_msgs = [
    # test mode select:
    # ...... means keep, not to change, this mode can hold;
    # don't have ...... means this mode only one clk
    # state =  4: SHIFT DR(tms):   1 0 0 0 ......  or 1 0 1 0 1 0 ......
    # state = 11: SHIFT IR(tms):   1 1 0 0 ......  or 1 1 0 0 1 0 1 0 ......
    # state = 15: UPDATE IR(tms):  1 1 0 0 1 0 1 1 or 1 1 0 0 1 1
    # state =  3: CAPTURE DR(tms): 1 0
    # state =  8: UPDATE DR(tms):  1 0 0 1 1 0 1

    # test case select: (after SHIFT IR, 4 clk)
    # IR = WDATA(tdi):   0 0 1 1   with SHIFT DR
    # IR = RDATA(tdi):   0 1 0 0   with UPDATA DR
    # IR = BYPASS(tdi):  0 0 0 0   with SHIFT DR
    # IR = IDCODE(tdi):  0 0 0 1   With SHIFT DR
    # IR = ADDR(tdi):    0 0 1 0   with SHIFT DR
    #             tdi, tms                 tdo
    # run in SHIFT IR
    jtag_req_type(0b0, 0b1), jtag_resp_type(0), # 1
    jtag_req_type(0b0, 0b1), jtag_resp_type(0), # 2
    jtag_req_type(0b0, 0b0), jtag_resp_type(0), # 3
    jtag_req_type(0b0, 0b0), jtag_resp_type(0), # 4
    # hold in SHIFT IR in 4 clk
    jtag_req_type(0b1, 0b0), jtag_resp_type(0), # 5
    jtag_req_type(0b1, 0b0), jtag_resp_type(0), # 6
    jtag_req_type(0b0, 0b0), jtag_resp_type(0), # 7
    jtag_req_type(0b0, 0b1), jtag_resp_type(0), # 8
    # run in UPDATE IR
    jtag_req_type(0b0, 0b0), jtag_resp_type(0), # 9
    jtag_req_type(0b0, 0b1), jtag_resp_type(0), # 10
    jtag_req_type(0b1, 0b1), jtag_resp_type(0), # 11
    jtag_req_type(0b1, 0b0), jtag_resp_type(0), # 12
    # run in RUN_TEST_IDLE
    jtag_req_type(0b0, 0b0), jtag_resp_type(0), # 13
    # run in SHIFT DR
    jtag_req_type(0b0, 0b1), jtag_resp_type(0), # 14
    jtag_req_type(0b1, 0b0), jtag_resp_type(0), # 15
    jtag_req_type(0b0, 0b0), jtag_resp_type(0), # 16
    # write the data and output the tdo
    jtag_req_type(0b1, 0b0), jtag_resp_type(0), # 17
    jtag_req_type(0b0, 0b0), jtag_resp_type(1), # 18
    jtag_req_type(0b0, 0b0), jtag_resp_type(0), # 19
    jtag_req_type(0b1, 0b0), jtag_resp_type(0), # 20
    jtag_req_type(0b0, 0b0), jtag_resp_type(1), # 21
    jtag_req_type(0b1, 0b0), jtag_resp_type(0), # 22
    jtag_req_type(0b0, 0b0), jtag_resp_type(1), # 23
    jtag_req_type(0b1, 0b0), jtag_resp_type(0), # 24

]

# -------------------------------------------------------------------------
# Test Case
# -------------------------------------------------------------------------
test_case_1 = mk_test_case_table([
     ("msgs       src_delay  sink_delay"),
     ["basic_0x0", basic_msgs, 0, 0, ],
])

# -------------------------------------------------------------------------
# Test cases
# -------------------------------------------------------------------------
@pytest.mark.parametrize(**test_case_1)
def test_stack_1(test_params, cmdline_opts):
    th = TestHarness(0)

    th.set_param("top.src.construct",
                 msgs=test_params.msgs[::2],
                 initial_delay=test_params.src_delay,
                 interval_delay=test_params.src_delay)

    th.set_param("top.sink.construct",
                 msgs=test_params.msgs[1::2],
                 initial_delay=test_params.sink_delay,
                 interval_delay=test_params.sink_delay)

    run_sim(th, cmdline_opts)


