# ===========================================
# i2c link test
# ===========================================

import pytest
import random
from pymtl3.stdlib.test_utils import mk_test_case_table, run_sim
from Module.I2C.I2C_Master.i2c_master import *
from Module.I2C.I2C_Slave.i2c_slave import *
from pymtl3.stdlib.test_utils.test_srcs import TestSrcRTL
from pymtl3.stdlib.test_utils.test_sinks import TestSinkRTL
from Module.I2C.Common.i2c_msg import *

source_type = mk_i2c_req_msg(8)
sink_type = mk_i2c_resp_msg(8)


class TestHarness( Component ):
  def construct(s,src_msgs, sink_msgs, src_delay, sink_delay):
    # Instantiate models
    s.master = i2c_master()
    s.slave  = i2c_slave()

    s.src   = TestSrcRTL(source_type, src_msgs, src_delay)
    s.sink  = TestSinkRTL(sink_type, sink_msgs, sink_delay)

    s.src.send  //= s.master.req
    s.sink.recv //= s.master.resp

    s.master.sda_in //= s.slave.sda_out
    s.master.sda_out //= s.slave.sda_in
    s.master.scl   //= s.slave.scl


  def done(s):
    return s.src.done() and s.sink.done()

  def line_trace(s):
    return s.slave.line_trace()




# -------------------------------------------------------------------------
# make messages
# -------------------------------------------------------------------------

def req( type_, data):

  if   type_ == 'rd': type_ = I2cMsgType.READ
  elif type_ == 'wr': type_ = I2cMsgType.WRITE

  return source_type(type_, data)

def resp(data):
  return sink_type(data)


# ----------------------------------------------------------------------
# Test Case:not random
# ----------------------------------------------------------------------

def read_1word_clean():
  print("-----------start 1word test---------------")
  return [
    # 1 1 0 1 1 1 1 0             0 0 1 1 1 1 1 1
    req('rd', 0xde),     resp(0x7f),
    #req('wr', 0xde),     resp(0xde),
  ]
# 1 1 0 1 1 1 1 0          1 0 1 1 1 1 0 0
# ----------------------------------------------------------------------
# Test Case: random
# ----------------------------------------------------------------------

"""
def random_test(  ):
  print("-----------start random test---------------")
  array = []
  # random.seed(0)
  test_amount = 100
  data = [random.randint(0, 0xff) for i in range(test_amount)]
  for i in range(test_amount):
    #                  type      data   bank
    array.append(req(  'wr',   data[i]))
    array.append(resp( 'wr',     0    ))

  for i in range(test_amount):
    array.append(req(  'rd',     0   ))
    array.append(resp( 'rd',  data[i]))

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
  msgs = test_params.msg_func()
  # Instantiate testharness
  th = TestHarness( msgs[::2], msgs[1::2],
                    test_params.src, test_params.sink)
  # Run the test
  run_sim( th, cmdline_opts)


