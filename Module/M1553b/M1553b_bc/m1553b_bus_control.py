# ================================
# M1553b Bus Controller
# ================================

from pymtl3.stdlib.ifcs.send_recv_ifcs import SendIfcRTL
from pymtl3.stdlib.ifcs.send_recv_ifcs import RecvIfcRTL
from Module.M1553b.Common.m1553b_bc_msg import *
from Module.M1553b.Common.m1553b_transmitter import *
from Module.M1553b.Common.m1553b_receiver import *
from Module.M1553b.Common.m1553b_cmd import *
from pymtl3.stdlib.basic_rtl.registers import RegEn

mk_m1553b_tb2bc_req_type  = mk_m1553b_tb2bc_req_msg()
mk_m1553b_bc2tb_resp_type = mk_m1553b_bc2tb_resp_msg()
mk_m1553b_rt2bc_req_type  = mk_m1553b_rt2bc_req_msg()
mk_m1553b_bc2rt_resp_type = mk_m1553b_bc2rt_resp_msg()

class m1553b_bus_controller( Component ):

    def construct(s, pack_size = 20, clks_per_half_bit = 1):

        # 1553b BC Interface
        s.tb2bc = RecvIfcRTL(mk_m1553b_tb2bc_req_type)
        s.bc2tb = SendIfcRTL(mk_m1553b_bc2tb_resp_type)
        s.cmd_odo   = OutPort(2)
        s.data_odo  = OutPort(2)
        s.idi       = InPort(2)
        s.tran_cmd  = m1553b_transmitter()
        s.tran_data = m1553b_transmitter()
        s.recv_data = m1553b_receiver()

        connect(s.cmd_odo, s.tran_cmd.odo)
        connect(s.data_odo, s.tran_data.odo)
        connect(s.idi, s.recv_data.idi)

        # interface
        s.SELECT_n  = OutPort(1)
        s.STRBD_n   = OutPort(1)
        s.MEM_REG   = OutPort(1)
        s.RD_WR     = OutPort(1)
        s.IOEN_n    = OutPort(1)
        s.addr_in   = OutPort(12)
        s.data_in   = OutPort(16)
        #s.addr_out  = OutPort(12)
        #s.data_out  = OutPort(16)

        s.select_n = Wire(1)
        s.strbd_n  = Wire(1)
        s.mem_reg  = Wire(1)
        s.rd_wr    = Wire(1)
        s.ioen_n   = Wire(1)
        s.addr_i  = Wire(12)
        #s.data_i  = Wire(16)
        s.addr_o  = Wire(12)
        s.data_o  = Wire(16)

        connect(s.SELECT_n, s.select_n)
        connect(s.STRBD_n , s.strbd_n )
        connect(s.MEM_REG , s.mem_reg )
        connect(s.RD_WR   , s.rd_wr   )
        connect(s.IOEN_n  , s.ioen_n  )
        connect(s.addr_in , s.addr_i  )
        #connect(s.addr_out, s.addr_o )
        #connect(s.data_in , s.data_i  )
        #connect(s.data_out, s.data_o )

        s.reg_type_ = RegEn(1)
        s.reg_type_.in_ //= s.tb2bc.msg.type_
        s.reg_type_.out //= s.bc2tb.msg.type_


        @update
        def comb_logic():
            s.strbd_n @= 0
            s.mem_reg @= 0
            s.rd_wr   @= 1
            s.addr_i  @= 0x111
            s.reg_type_.en @= (s.bc2tb.rdy & s.tb2bc.en)

        s.ram = [Wire(16) for i in range(4096)]
        s.config_reg  = Wire(16)


        s.ram[0] //= s.tb2bc.msg.cmd_word
        s.ram[1] //= s.tb2bc.msg.data_word

        @update_ff
        def start_logic():
            if (s.SELECT_n == 0) & (s.STRBD_n == 0):
                s.ioen_n <<= 0

        @update_ff
        def ifc_logic():
            if s.IOEN_n == 0:
                s.select_n <<= 1

        # State Definitions
        s.state = Wire(3)
        s.user_reset = 0
        s.idle       = 1
        s.handshake  = 2
        s.transfer_msg = 3
        s.receive_msg  = 4
        s.finish     = 4
        s.complete   = 5

        s.cntr     = Wire(8)
        s.cntr_max = Wire(8)


        # State Transition Logic
        @update_ff
        def state_transitions():
            if s.reset:
                s.state <<= s.user_reset
            if s.state == s.user_reset:
                s.state <<= s.idle
            if s.state == s.idle:
                if s.bc2tb.rdy & s.tb2bc.en:
                    s.state <<= s.handshake
            if s.state == s.handshake:
                s.state <<= s.transfer_msg
            if s.state == s.transfer_msg:
                if s.cntr >= pack_size:
                    s.state <<= s.receive_msg
            if s.state == s.receive_msg:
                if s.cntr >= pack_size:
                    s.state <<= s.finish
            if s.state == s.finish:
                if s.cntr >= clks_per_half_bit:
                    s.state <<= s.complete
            if s.state == s.complete:
                if s.cntr >= clks_per_half_bit:
                    s.state <<= s.idle

        # Maximum Counter Value
        @update
        def max_counter_values():
            if s.state == s.user_reset:
                s.cntr_max @= clks_per_half_bit
            if s.state == s.idle:
                s.cntr_max @= clks_per_half_bit
            if s.state == s.handshake:
                s.cntr_max @= clks_per_half_bit
            if s.state == s.transfer_msg:
                s.cntr_max @= pack_size
            if s.state == s.receive_msg:
                s.cntr_max @= pack_size
            if s.state == s.finish:
                s.cntr_max @= clks_per_half_bit
            if s.state == s.complete:
                s.cntr_max @= clks_per_half_bit

        # Counter Logic
        @update_ff
        def counter_logic():
            if s.state == s.idle:
                s.cntr <<= 0
            elif (s.cntr >= s.cntr_max) & (s.state != s.idle):
                s.cntr <<= 0
            else:
                s.cntr <<= s.cntr + 1

        s.data_ien = Wire(1)
        s.cmd_ien  = Wire(1)
        connect(s.data_ien,s.tran_data.ien)
        connect(s.cmd_ien,s.tran_cmd.ien)

        @update
        def ien_logic():
            if (s.state == s.idle):
                s.cmd_ien @= 1
                s.data_ien @= 1
            else:
                s.cmd_ien @= 0
                s.data_ien @= 0

        @update
        def cmd_or_data():
            if (s.state == s.idle):
                s.tran_cmd.idata  @= s.ram[0]
                s.tran_data.idata @= s.ram[1]

        s.bc2tb.msg.data_word //= s.recv_data.odata



        @update_ff
        def recv_rt_logic():
            pass


        # val rdy interface(tb 2 bc)
        @update
        def req_rdy_tb_and_bc():
            s.tb2bc.rdy @= s.bc2tb.rdy & (s.state == s.idle)
        s.result_read = Wire(1)

        @update
        def result_read():
            if s.state == s.user_reset:
                s.result_read @= 0
            if s.state == s.idle:
                if (s.result_read == 0) & (s.bc2tb.rdy == 0):
                    s.result_read @= 0
                else:
                    s.result_read @= 1
            if s.state == s.handshake:
                s.result_read @= 0
            if s.state == s.transfer_msg:
                s.result_read @= 0
            if s.state == s.finish:
                s.result_read @= 0
            if s.state == s.complete:
                if (s.bc2tb.rdy == 1) & (s.cntr > 0):
                    s.result_read @= 1

        s.val_progressing = Wire(1)
        s.msg_from_rt = Wire(1)

        @update
        def valid_resp_tb_and_bc():
            if s.state == s.user_reset:
                s.val_progressing @= 0
                s.msg_from_rt @= 0
            elif (s.state == s.idle) & (s.tb2bc.en == 1):
                s.val_progressing @= 1
                s.msg_from_rt @= 0
            elif (s.state == s.complete) & (s.val_progressing == 1):
                s.msg_from_rt @= 1
            else:
                s.val_progressing @= s.val_progressing


        @update
        def resp_val_tb_and_bc():
            if (s.state == s.complete) & (s.result_read == 0) & (s.msg_from_rt == 1):
                s.bc2tb.en @= 1
            elif (s.state == s.idle) & (s.result_read == 0) & (s.msg_from_rt == 1):
                s.bc2tb.en @= 1
            else:
                s.bc2tb.en @= 0

    def line_trace(s):
        return f"cmd:{s.tran_cmd.idata} data:{s.tran_data.idata} do:{s.cmd_odo} co:{s.data_odo} s:{s.state}r0:{s.ram[0]} r1:{s.ram[1]} "
        #return f"data_i:{s.data_i} msg:{s.tb2bc.msg.cmd_word} data_or_cmd：{s.data_or_cmd} state:{s.state} "







