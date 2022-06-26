# ===========================================
# m1553b connect test
# ===========================================

import pytest
import random
from pymtl3.stdlib.test_utils import mk_test_case_table, run_sim
from Module.M1553b.M1553b_bc.m1553b_bus_control import *
from Module.M1553b.M1553b_rt.m1553b_remote_terminal import *
from pymtl3.stdlib.test_utils.test_srcs import TestSrcRTL
from pymtl3.stdlib.test_utils.test_sinks import TestSinkRTL
from Module.M1553b.Common.m1553b_bc_msg import *
from Module.M1553b.Common.m1553b_rt_msg import *

source_type = mk_m1553b_tb2bc_req_msg()
sink_type = mk_m1553b_bc2tb_resp_msg()


class TestHarness( Component ):

  def construct(s, src_msgs, sink_msgs, src_delay, sink_delay):

    s.bc1    = m1553b_bus_controller()
    s.rt1    = m1553b_remote_Terminal()
    #s.rt2    = m1553b_remote_Terminal()
    #s.rt3    = m1553b_remote_Terminal()

    s.src    = TestSrcRTL(source_type, src_msgs, src_delay)
    s.sink   = TestSinkRTL(sink_type, sink_msgs, sink_delay)

    s.src.send  //= s.bc1.tb2bc
    s.sink.recv //= s.bc1.bc2tb

    s.bc1.data_odo  //= s.rt1.data_in
    s.bc1.cmd_odo //= s.rt1.cmd_in
    s.bc1.idi //= s.rt1.data_odo

  def done(s):
    return s.src.done() and s.sink.done()

  def line_trace(s):
    return s.bc1.line_trace()

# -------------------------------------------------------------------------
# make messages
# -------------------------------------------------------------------------

def req( type_,cmd_type_ ,cmd_word, data_word):
  if type_ == 'cmd' : type_ = M1553bMsgType.CMD
  if type_ == 'data': type_ = M1553bMsgType.DATA
  if cmd_type_ == 'wr': cmd_type_ = M1553bCmdMsgType.SEND
  if cmd_type_ == 'rd': cmd_type_ = M1553bCmdMsgType.RECEIVE
  return source_type(type_, cmd_type_, cmd_word, data_word)

def resp( type_,status_word, data_word):
  if type_ == 'cmd' : type_ = M1553bMsgType.CMD
  if type_ == 'data': type_ = M1553bMsgType.DATA
  return sink_type(type_, status_word, data_word )

# ----------------------------------------------------------------------
# Test Case:not random
# ----------------------------------------------------------------------

def read_1word_clean(  ):
  print("-----------start 1word test---------------")
  # 1010 1110 1101 1111 = 1110 0010 0110 0110 1010 01
  return [
    #    type(2)   cmd_type   cmd_word    data_word           type     data_word
    req( 'cmd',     'wr',      0xaedf,     0xabcd),     resp( 'cmd',   0, 0     ),
    req( 'data',    'wr',      0,          0xffff),     resp( 'data',  0, 0xabcd),
  ]

# ----------------------------------------------------------------------
# Test Case: random
# ----------------------------------------------------------------------
"""
def random_test(  ):
  array = []
  test_amount = 100
  cmd = [ i for i in range(test_amount)]
  data = [random.randint(0, 0xffff) for i in range(test_amount)]
  print("-----------start random test---------------")
  for i in range(test_amount):
    #                  type  cmd_type   cmd_word   data_word
    array.append(req(  'cmd',  'wr',    cmd[i], data[i]))
    array.append(resp( 'cmd',   0,      0))
    array.append(req(  'data', 'wr',    0, 0xffff))
    array.append(resp( 'data',  0,      data[i] ))


  return array
"""
# -------------------------------------------------------------------------
# Test table for generic test
# -------------------------------------------------------------------------

test_case_table_generic = mk_test_case_table([
  (                         "msg_func                src sink"),
  [ "read_1word_clean",      read_1word_clean,        0,  0    ],
  #[ "random_test",           random_test,             0,  0    ],
])


@pytest.mark.parametrize( **test_case_table_generic )
def test_generic( test_params, cmdline_opts):
  msgs = test_params.msg_func(  )
  # Instantiate testharness
  th = TestHarness( msgs[::2], msgs[1::2],
                    test_params.src, test_params.sink)
  # Run the test
  run_sim( th, cmdline_opts)
