# =========================================================================
#  UART Test
# =========================================================================

import pytest
from pymtl3.stdlib.test_utils import mk_test_case_table, run_sim
from Module.UART.Uart_top.Uart_top_val import *
from Module.UART.Uart_top.Uart_top_non_val import *
from pymtl3.stdlib.test_utils.test_srcs import TestSrcRTL
from pymtl3.stdlib.test_utils.test_sinks import TestSinkRTL

# -------------------------------------------------------------------------
# TestHarness
# -------------------------------------------------------------------------


class TestHarness( Component ):

    def construct(s, pack_size = 8):

        s.u1 = uart_val()
        s.u2 = uart_non_val()
        s.src   = TestSrcRTL(mk_bits(pack_size))
        s.sink  = TestSinkRTL(mk_bits(pack_size))

        s.src.send //= s.u1.req
        s.sink.recv //= s.u1.resp

        s.u1.txd //= s.u2.rxd
        s.u1.rxd //= s.u2.txd

    def done(s):
        return s.src.done() and s.sink.done()

    def line_trace(s):
        return f" txd:{s.u2.tx.txd} rxd:{s.u1.rx.rxd} req.rdy:{s.u1.req.rdy} " \
               f"req.en:{s.u1.req.en} resp.en:{s.u1.resp.en} resp.rdy:{s.u1.resp.rdy} " \
               f"u1_data:{s.u1.tx.preload_data} u1_rdata:{s.u1.rx.recv_data}" \
               f" state:{s.u1.tx.state} state1:{s.u2.rx.state} "


# -------------------------------------------------------------------------
# Test Case small
# -------------------------------------------------------------------------
basic_msgs = [
    127,  127,
    69, 69,
]
test_case_8bits = mk_test_case_table([
    ("msgs        src_delay  sink_delay"),
    ["basic_0x0", basic_msgs, 0, 0, ],
])


# -------------------------------------------------------------------------
# Test cases
# -------------------------------------------------------------------------
@pytest.mark.parametrize(**test_case_8bits)
def test_stack_8bit(test_params, cmdline_opts):
    th = TestHarness(8)

    th.set_param("top.src.construct",
                 msgs=test_params.msgs[::2],
                 initial_delay=test_params.src_delay,
                 interval_delay=test_params.src_delay, )

    th.set_param("top.sink.construct",
                 msgs=test_params.msgs[1::2],
                 initial_delay=test_params.sink_delay,
                 interval_delay=test_params.sink_delay)

    run_sim(th, cmdline_opts)
