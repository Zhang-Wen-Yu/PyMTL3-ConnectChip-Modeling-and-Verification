# ===========================================
# flash test
# ===========================================

import pytest
import random
from pymtl3.stdlib.test_utils import mk_test_case_table, run_sim
from Module.FLASH.FlashMem.FlashMem import *
from Module.FLASH.Flashctr.FlashCtr import *
from Module.FLASH.Common.flash_msg import *
from pymtl3.stdlib.test_utils.test_srcs import TestSrcRTL
from pymtl3.stdlib.test_utils.test_sinks import TestSinkRTL

source_type = mk_flash_req_msg(8)
sink_type = mk_flash_resp_msg(8)

class TestHarness( Component ):

  def construct(s, src_msgs, sink_msgs, src_delay, sink_delay):
    # Instantiate models

    s.memctr = Flashctr()
    s.mem    = FlashMem()

    s.src = TestSrcRTL(source_type, src_msgs, src_delay)
    s.sink = TestSinkRTL(sink_type, sink_msgs, sink_delay)

    s.src.send  //= s.memctr.req
    s.sink.recv //= s.memctr.resp

    connect(s.memctr.ifc,s.mem.ifc)


  def done(s):
    return s.src.done() and s.sink.done()

  def line_trace(s):
    return s.mem.line_trace()


# -------------------------------------------------------------------------
# make messages
# -------------------------------------------------------------------------

def req( type_, data):

  if   type_ == 'rd': type_ = FlashMsgType.READ
  elif type_ == 'wr': type_ = FlashMsgType.WRITE
  elif type_ == 'wp': type_ = FlashMsgType.WRITE_PROTECT
  elif type_ == 'ad': type_ = FlashMsgType.ADDRESS
  return source_type(type_, data)

def resp( type_, data):
  if   type_ == 'rd': type_ = FlashMsgType.READ
  elif type_ == 'wr': type_ = FlashMsgType.WRITE
  elif type_ == 'wp': type_ = FlashMsgType.WRITE_PROTECT
  elif type_ == 'ad': type_ = FlashMsgType.ADDRESS
  return sink_type(type_, data)


# ----------------------------------------------------------------------
# Test Case:not random
# ----------------------------------------------------------------------

def read_1word_clean(  ):
  print("-----------start 1word test---------------")
  return [
    #    type(2)   data(8)           type(2)  data(8)
    req( 'ad',     0xff  ),    resp( 'ad',  0    ),
    req( 'ad',     0xff  ),    resp( 'ad',  0    ),
    req( 'ad',     0xff  ),    resp( 'ad',  0    ),
    req( 'wr',     0xab  ),    resp( 'wr',  0    ),
    req( 'rd',     0     ),    resp( 'rd',  0xab ),
    req( 'rd',     0     ),    resp( 'rd',  0    ),
  ]

# ----------------------------------------------------------------------
# Test Case: random
# ----------------------------------------------------------------------


def random_test(  ):
  print("-----------start random test---------------")
  array = []
  # random.seed(0)
  test_amount = 50
  addr = [i for i in range(test_amount)]
  data = [random.randint(0, 0xff) for i in range(test_amount)]

  for i in range(test_amount):
    #                  type   data
    array.append(req(  'ad',  addr[i]))
    array.append(resp( 'ad',  0      ))
    array.append(req(  'ad',  addr[i]))
    array.append(resp( 'ad',  0))
    array.append(req(  'ad',  addr[i]))
    array.append(resp( 'ad',  0))
    array.append(req(  'wr',  data[i]))
    array.append(resp( 'wr',  0      ))
    array.append(req(  'rd',  0      ))
    array.append(resp( 'rd',  data[i]))
    array.append(req(  'rd',  0      ))
    array.append(resp( 'rd',  0))

  return array

# -------------------------------------------------------------------------
# Test table for generic test
# -------------------------------------------------------------------------

test_case_table_generic = mk_test_case_table([
  (                         "msg_func                src sink"),
  [ "read_1word_clean",      read_1word_clean,        0,  0    ],
  [ "random_test",           random_test,             0,  0    ],
])

@pytest.mark.parametrize( **test_case_table_generic )
def test_generic( test_params,cmdline_opts):
  msgs = test_params.msg_func(  )
  # Instantiate testharness
  th = TestHarness( msgs[::2], msgs[1::2],
                    test_params.src, test_params.sink)
  # Run the test
  run_sim( th,cmdline_opts)
