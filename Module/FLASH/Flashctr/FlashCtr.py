from pymtl3 import *
from pymtl3.stdlib.ifcs.send_recv_ifcs import RecvIfcRTL, SendIfcRTL
from Module.FLASH.Common.FlashIfc import *
from pymtl3.stdlib.basic_rtl.registers import RegRst
from Module.FLASH.Common.flash_msg import *

resp_type  = mk_flash_resp_msg(8)
req_type = mk_flash_req_msg(8)

class Flashctr( Component ):

    def construct(s, num_bits = 8, col_num = 2, page_num = 2, block_num = 2):

        # ---------------------------------------------
        # user interface
        # ---------------------------------------------

        s.req = RecvIfcRTL(req_type)
        s.resp = SendIfcRTL(resp_type)

        # ---------------------------------------------
        # flash controller interface
        # ---------------------------------------------

        s.ifc = FlashCtrIfc()
        s.flash_val   = Wire(1)
        s.flash_type  = Wire(1)
        s.flash_aen   = Wire(1)
        s.flash_cen   = Wire(1)
        s.flash_rob   = Wire(1)
        s.flash_wdata = Wire(num_bits)
        s.flash_wen   = Wire(1)
        s.flash_ren   = Wire(1)
        s.flash_rdata = Wire(num_bits)
        s.flash_wp    = Wire(1)

        connect(s.ifc.CE ,  s.flash_val  )
        connect(s.ifc.ALE,  s.flash_aen  )
        connect(s.ifc.CLE,  s.flash_cen  )
        connect(s.ifc.RE ,  s.flash_ren  )
        connect(s.ifc.WE ,  s.flash_wen  )
        connect(s.ifc.ROB,  s.flash_rob  )
        connect(s.ifc.I  ,  s.flash_wdata)
        connect(s.ifc.O  ,  s.flash_rdata)
        connect(s.ifc.WP ,  s.flash_wp )

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
            if s.req.msg.type_ == FlashMsgType.ADDRESS:
                s.flash_cen @= 0
                s.flash_aen @= 1
                s.flash_wen @= 1
                s.flash_ren @= 1
                s.flash_wp  @= 1

            if s.req.msg.type_ == FlashMsgType.WRITE:
                s.flash_cen @= 0
                s.flash_aen @= 0
                s.flash_wen @= 1
                s.flash_ren @= 1
                s.flash_wp  @= 1

            if s.req.msg.type_ == FlashMsgType.READ:
                s.flash_cen @= 0
                s.flash_aen @= 0
                s.flash_wen @= 1
                s.flash_ren @= 0
                s.flash_wp  @= 1

            if s.req.msg.type_ == FlashMsgType.WRITE_PROTECT:
                s.flash_wp  @= 0

            s.flash_val     @= ~s.req.en
            s.flash_wdata   @= s.req.msg.data
            s.resp.msg.data @= s.flash_rdata
            s.resp.en       @= s.done



