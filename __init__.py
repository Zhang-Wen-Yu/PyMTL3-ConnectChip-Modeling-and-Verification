#!/usr/bin/env python3

from hypothesis import given,strategies as st
from werkzeug import run_simple

from TestBench.flash_test import TestHarness
@given( nterminals = st.integers(2,16),
        test_pkts  = st.lists(pkt_strat()))
def test_ring_pyh2g( nterminals ,test_pkts ):
    dut = RingNetwork( nterminals )
    th  = TestHarness( dut, test_pkts )
    run_simple( th )





