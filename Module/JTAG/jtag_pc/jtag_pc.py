# ===================================
# jtag model
# ===================================

from pymtl3 import *
from Module.JTAG.Common.jtag_ifc import *
from pymtl3.stdlib.ifcs.send_recv_ifcs import RecvIfcRTL, SendIfcRTL
from Module.JTAG.Common.jtag_msg import *
from pymtl3.stdlib.basic_rtl.registers import RegRst
from Module.JTAG.Common.CrossOver import *

jtag_req_type  = mk_jtag_req_msg(1,1)
jtag_resp_type = mk_jtag_resp_msg(1)

class jtag_pc( Component ):

    def construct(s, tck_per_bit = 2):

        # Interface
        s.ifc = jtagIfc_pc()

        s.req  = RecvIfcRTL(jtag_req_type)
        s.resp = SendIfcRTL(jtag_resp_type)

        s.jtag_tdi = Wire(1)
        s.jtag_tdo = Wire(1)
        s.jtag_tms = Wire(1)
        s.jtag_tck = Wire(1)

        s.tck_clk = CrossOver()



        connect(s.ifc.TDI, s.jtag_tdi)
        connect(s.ifc.TDO, s.jtag_tdo)
        connect(s.ifc.TMS, s.jtag_tms)
        connect(s.ifc.TCK, s.tck_clk.clk_out)

        s.done = Wire(1)
        s.reg_val = RegRst(1)
        s.reg_val.in_ //= s.req.en
        s.reg_val.out //= s.done

        @update
        def comb_logic():
            s.req.rdy       @= 1
            s.jtag_tdi      @= s.req.msg.tdi
            s.jtag_tms      @= s.req.msg.tms
            s.resp.msg.tdo  @= s.jtag_tdo
            s.resp.en       @= s.done

    def line_trace(s):
        return f"TDI: {s.ifc.TDI},TDO: {s.ifc.TDO}," \
               f"TMS: {s.ifc.TMS},TCK: {s.ifc.TCK} clk:{s.clk}"











