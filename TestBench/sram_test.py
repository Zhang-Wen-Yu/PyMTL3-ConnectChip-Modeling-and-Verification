# ===========================================
# sram connect test
# ===========================================

import pytest
import random
from pymtl3.stdlib.test_utils import mk_test_case_table, run_sim
from Module.SRAM.SRAM.Sram import *
from Module.SRAM.SramCtr.SramCtr import *
from Module.SRAM.Common.sram_msg import *
from pymtl3.stdlib.test_utils.test_srcs import TestSrcRTL
from pymtl3.stdlib.test_utils.test_sinks import TestSinkRTL

source_type = mk_mem_req_msg(8,32,2)
sink_type = mk_mem_resp_msg(32)

class TestHarness( Component ):

  def construct(s, src_msgs, sink_msgs, src_delay, sink_delay):
    # Instantiate models
    s.memctr = SramContr(32,256)
    s.mem    = Sram(32,256)
    s.src = TestSrcRTL(source_type, src_msgs, src_delay)
    s.sink = TestSinkRTL(sink_type, sink_msgs, sink_delay)
    #connect(s.src.send, s.memctr.req)
    #connect(s.memctr.resp, s.sink.recv)

    s.src.send //= s.memctr.req
    s.sink.recv //= s.memctr.resp

    s.memctr.sramctr_ifc.CE1  //= s.mem.sram_ifc.CE1
    s.memctr.sramctr_ifc.WE1  //= s.mem.sram_ifc.WE1
    s.memctr.sramctr_ifc.OE1  //= s.mem.sram_ifc.OE1
    s.memctr.sramctr_ifc.CS1  //= s.mem.sram_ifc.CS1
    s.memctr.sramctr_ifc.A1   //= s.mem.sram_ifc.A1
    s.memctr.sramctr_ifc.I1   //= s.mem.sram_ifc.I1
    s.memctr.sramctr_ifc.O1   //= s.mem.sram_ifc.O1
    s.memctr.sramctr_ifc.WBM1 //= s.mem.sram_ifc.WBM1
    s.memctr.sramctr_ifc.BA1  //= s.mem.sram_ifc.BA1


  def done(s):
    return s.src.done() and s.sink.done()

  def line_trace(s):
    #return s.mem.line_trace()
    #return f"{s.memctr.req.msg.type_} {s.memctr.resp.msg.type_}"
     return f"req.en:{s.memctr.resp.en}"

# -------------------------------------------------------------------------
# make messages
# -------------------------------------------------------------------------

def req( type_, addr, data, bank):

  if   type_ == 'rd': type_ = MemMsgType.READ
  elif type_ == 'wr': type_ = MemMsgType.WRITE
  elif type_ == 'in': type_ = MemMsgType.WRITE_INIT
  return source_type(type_, addr, data, bank)

def resp( type_, data):
  if   type_ == 'rd': type_ = MemMsgType.READ
  elif type_ == 'wr': type_ = MemMsgType.WRITE
  elif type_ == 'in': type_ = MemMsgType.WRITE_INIT
  return sink_type(type_, data )


# ----------------------------------------------------------------------
# Test Case:not random
# ----------------------------------------------------------------------

def read_1word_clean(  ):
  print("-----------start 1word test---------------")
  return [
    #    type(2)   addr(8)     data(32)   bank(2)              type  data
    req( 'in',     0x01,       0xdeadbfef,    0),       resp( 'in',  0          ),
    req( 'rd',     0x01,       0         ,    0),       resp( 'rd',  0xdeadbfef ),
  ]

# ----------------------------------------------------------------------
# Test Case: random
# ----------------------------------------------------------------------


def random_test(  ):
  array = []
  test_amount = 100
  addr = [ i for i in range(test_amount)]
  data = [random.randint(0, 0xffff) for i in range(test_amount)]
  print("-----------start random test---------------")
  for i in range(test_amount):

    #                  type    addr    data   bank
    array.append(req(  'in',  addr[i], data[i], 0))
    array.append(resp( 'in',       0       ))

  for i in range(test_amount):
    array.append(req(  'rd',  addr[i], 0, 0))
    array.append(resp( 'rd',  data[i] ))


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
def test_generic( test_params, cmdline_opts):
  msgs = test_params.msg_func(  )
  # Instantiate testharness
  th = TestHarness( msgs[::2], msgs[1::2],
                    test_params.src, test_params.sink)
  # Run the test
  run_sim( th, cmdline_opts)


