# =========================================================================
#  Test Top
# =========================================================================

# import the Module and DUT1&2
import pytest
from pymtl3.stdlib.test_utils import mk_test_case_table, run_sim
from pymtl3.stdlib.stream import *
from Module.SPI.SPIMaster.SpiMasterWarpped import *
from Module.SPI.SPISlave.SpiSlaveWarpped import *

# -------------------------------------------------------------------------
# TestHarness
# -------------------------------------------------------------------------

# define the class and import the DUT1 and DUT2
class TestHarness( Component ):

    def construct(s, pack_size, flow_control):

        s.master = Spi_Master_Warpped(pack_size)
        s.slave  = Spi_Slave_Warpped(pack_size)
        s.src    = SourceRTL(mk_bits(pack_size))
        s.sink   = SinkRTL(mk_bits(pack_size))

        s.src.send //= s.master.req
        s.master.resp //= s.sink.recv

        s.master.master_ifc.miso //= s.slave.slave_ifc.miso
        s.master.master_ifc.cs   //= s.slave.slave_ifc.cs
        s.master.master_ifc.mosi //= s.slave.slave_ifc.mosi
        s.master.master_ifc.sclk //= s.slave.slave_ifc.sclk

    def done(s):
        return s.src.done() and s.sink.done()

    def line_trace(s):
        return s.master.line_trace()




# -------------------------------------------------------------------------
# Test Case: larger
# -------------------------------------------------------------------------
larger_msgs = [
    333, 0,
    222, 333,
    555, 222,
    880, 555,
    700, 880,
]
# -------------------------------------------------------------------------
# Test Case: more larger
# -------------------------------------------------------------------------
more_larger_msgs = [
    2480, 0,
    4275, 2480,
    1875, 4275,
    8500, 1875,
    7007, 8500,
]
# -------------------------------------------------------------------------
# Test Case small
# -------------------------------------------------------------------------
basic_msgs = [
    4, 0,   
    7, 4,    
    6, 7,    
    8, 6,    
    1, 8
]
test_case_8bits = mk_test_case_table([
    ("msgs        src_delay  sink_delay"),  
    ["basic_0x0", basic_msgs, 0, 0, ],     
    ["basic_1x5", basic_msgs, 1, 5, ],
    ["basic_3x1", basic_msgs, 3, 1, ],
    ["basic_8x8", basic_msgs, 8, 8, ],
    ["basic_7x7", basic_msgs, 7, 7, ],
])

# -------------------------------------------------------------------------
# Test Case large
# -------------------------------------------------------------------------
test_case_12bits = mk_test_case_table([
    ("msgs          src_delay  sink_delay"),
    ["larger_0x0", larger_msgs, 0, 0, ],
    ["larger_1x5", larger_msgs, 1, 5, ],
    ["larger_3x1", larger_msgs, 3, 1, ],
    ["larger_8x8", larger_msgs, 8, 8, ],
    ["larger_7x7", larger_msgs, 7, 7, ],
])

# -------------------------------------------------------------------------
# Test Case more_larger
# -------------------------------------------------------------------------
test_case_16bits = mk_test_case_table([
    ("msgs          src_delay  sink_delay"),
    ["more_larger_0x0", more_larger_msgs, 0, 0, ],
    ["more_larger_1x5", more_larger_msgs, 1, 5, ],
    ["more_larger_3x1", more_larger_msgs, 3, 1, ],
    ["more_larger_8x8", more_larger_msgs, 8, 8, ],
    ["more_larger_7x7", more_larger_msgs, 7, 7, ],
])


# -------------------------------------------------------------------------
# Test cases
# -------------------------------------------------------------------------
@pytest.mark.parametrize(**test_case_8bits)
def test_stack_8bit(test_params, cmdline_opts):
    th = TestHarness(8, 0)

    th.set_param("top.src.construct",
                 msgs=test_params.msgs[::2],
                 initial_delay=test_params.src_delay,
                 interval_delay=test_params.src_delay, )

    th.set_param("top.sink.construct",
                 msgs=test_params.msgs[1::2],
                 initial_delay=test_params.sink_delay,
                 interval_delay=test_params.sink_delay)

    run_sim(th, cmdline_opts)


@pytest.mark.parametrize(**test_case_12bits)
def test_stack_12bit(test_params, cmdline_opts):
    th = TestHarness(12, 0)

    th.set_param("top.src.construct",
                 msgs=test_params.msgs[::2],
                 initial_delay=test_params.src_delay,
                 interval_delay=test_params.src_delay)

    th.set_param("top.sink.construct",
                 msgs=test_params.msgs[1::2],
                 initial_delay=test_params.sink_delay,
                 interval_delay=test_params.sink_delay)

    run_sim(th, cmdline_opts)


@pytest.mark.parametrize(**test_case_16bits)
def test_stack_16bit(test_params, cmdline_opts):
    th = TestHarness(16, 0)

    th.set_param("top.src.construct",
                 msgs=test_params.msgs[::2],
                 initial_delay=test_params.src_delay,
                 interval_delay=test_params.src_delay)

    th.set_param("top.sink.construct",
                 msgs=test_params.msgs[1::2],
                 initial_delay=test_params.sink_delay,
                 interval_delay=test_params.sink_delay)

    run_sim(th, cmdline_opts)
