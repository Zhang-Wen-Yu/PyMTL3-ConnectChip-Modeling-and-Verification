# ================================================
# Sram Controller
# ================================================

from pymtl3 import *
from pymtl3.stdlib.ifcs.send_recv_ifcs import RecvIfcRTL, SendIfcRTL
from Module.SRAM.Common.SramIfc import *
from pymtl3.stdlib.basic_rtl.registers import RegRst
from Module.SRAM.Common.sram_msg import *

resp_type  = mk_mem_resp_msg(32)
req_type = mk_mem_req_msg(8,32,2)

class SramContr( Component ):

    def construct(s, num_bits = 32 , num_words = 256, bank_num = 4):

        # ---------------------------------------------
        # user interface
        # ---------------------------------------------

        s.req = RecvIfcRTL(req_type)
        s.resp = SendIfcRTL(resp_type)

        # ---------------------------------------------
        # sram controller interface
        # ---------------------------------------------
        s.sramctr_ifc = SramContrIfc()
        s.sram_val   = Wire(1)
        s.sram_type  = Wire(1)
        s.sram_idx   = Wire(8)
        s.sram_wdata = Wire(32)
        s.sram_wben  = Wire(32)
        s.sram_rdata = Wire(32)
        s.sram_row  = Wire(2)

        connect(s.sramctr_ifc.CE1,  s.clk       )
        connect(s.sramctr_ifc.CS1,  s.sram_val )
        connect(s.sramctr_ifc.OE1,  0           )
        connect(s.sramctr_ifc.WBM1, s.sram_wben)
        connect(s.sramctr_ifc.WE1,  s.sram_type)
        connect(s.sramctr_ifc.A1,   s.sram_idx )
        connect(s.sramctr_ifc.I1,   s.sram_wdata)
        connect(s.sramctr_ifc.O1,   s.sram_rdata)
        connect(s.sramctr_ifc.BA1,  s.sram_row )


        s.done = Wire(1)

        s.reg_val = RegRst(1)
        s.reg_val.in_ //= s.req.en
        s.reg_val.out //= s.done

        s.reg_type_ = RegRst(2)
        s.reg_type_.in_ //= s.req.msg.type_
        s.reg_type_.out //= s.resp.msg.type_


        @update
        def comb_logic():
            s.req.rdy @= 1
            if s.req.msg.type_ == MemMsgType.WRITE_INIT:
                s.sram_type @= 1       # WRITE ENABLE
                s.sram_wben @= 0xffffffff     # WRITE BIT ENABLE MASK
            else:
                s.sram_type @= 0
                s.sram_wben @= 0

            s.sram_val      @= s.req.en             # CS1
            s.sram_idx      @= s.req.msg.addr        # A1
            s.sram_wdata     @= s.req.msg.data      # WRITE DATA
            s.resp.msg.data @= s.sram_rdata     # READ DATA
            s.sram_row      @= s.req.msg.row
            s.resp.en       @= s.done






    def line_trace(s):
        return f"( WE={s.sramctr_ifc.WE1}  A1={s.sramctr_ifc.A1} " \
               f"I1A={s.sramctr_ifc.I1} O1={s.sramctr_ifc.O1} " \
               f" recv_msg = {s.req.msg} recv_val = {s.req.en} recv_rdy = {s.req.rdy} " \
               f"send_msg = {s.resp.msg} send_val = {s.resp.en} send_rdy = {s.resp.rdy})"




