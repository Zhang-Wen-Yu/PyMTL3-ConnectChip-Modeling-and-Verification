# ================================
# M1553b remote terminal
# ================================


# from pymtl3.stdlib.ifcs.send_recv_ifcs import SendIfcRTL
# from pymtl3.stdlib.ifcs.send_recv_ifcs import RecvIfcRTL
from Module.M1553b.Common.m1553b_rt_msg import *
from Module.M1553b.Common.m1553b_transmitter import *
from Module.M1553b.Common.m1553b_receiver import *
from Module.SPI.Common.PullInIfc import PullInIfc
from Module.SPI.Common.PushOutIfc import PushOutIfc

mk_m1553b_rt_req_type  = mk_m1553b_rt_req_msg()
mk_m1553b_rt_resp_type = mk_m1553b_rt_resp_msg()

class m1553b_remote_Terminal( Component ):

    def construct(s):

        # 1553b RT Interface
        #s.bc2rt   = RecvIfcRTL(mk_m1553b_rt_req_type)
        #s.rt2bc   = SendIfcRTL(mk_m1553b_rt_resp_type)
        #s.RT2rt   = RecvIfcRTL(mk_m1553b_rt_req_type)
        #s.rt2RT   = SendIfcRTL(mk_m1553b_rt_resp_type)
        s.trans_data = m1553b_transmitter()
        s.recv_cmd   = m1553b_receiver()
        s.recv_data  = m1553b_receiver()
        s.cmd_in    = InPort(2)
        s.data_in   = InPort(2)
        s.data_odo  = OutPort(2)
        s.cmd_odata = Wire(16)

        s.push = PushOutIfc(40)
        s.pull = PullInIfc(40)
        s.cmd_odata //= s.recv_cmd.odata

        s.cmd_true_data_packet = Wire(1)
        s.cmd_true_data_packet  //= s.recv_cmd.true_data_packet
        s.data_true_data_packet = Wire(1)
        s.data_true_data_packet //= s.recv_data.true_data_packet
        s.ien = Wire(1)
        s.ien //= s.trans_data.ien
        connect(s.data_odo,  s.trans_data.odo)
        connect(s.data_in,   s.recv_data.idi)
        connect(s.cmd_in,    s.recv_cmd.idi)


        s.data_num = Wire(5)
        s.trans_or_recv = Wire(1)
        s.sub_addr  = Wire(5)
        s.word_cntr = Wire(5)

        @update
        def cmd_load_logic():
            if s.cmd_true_data_packet:
                s.data_num @= s.cmd_odata[0:5]
                s.trans_or_recv @= s.cmd_odata[5]
                s.word_cntr @= s.cmd_odata[11:16]
                s.sub_addr @= s.cmd_odata[6:11]

        """
        @update
        def rt_and_bc_val_rdy_logic():
            if s.data_en == 1:
                s.rt2bc.en @= 1
            else:
                s.rt2bc.en @= 0
            s.bc2rt.rdy @= 1

        s.trans_data.idata //= s.rt2bc.msg.data_word[3:19]
        @update_ff
        def recv_manchester():
            if s.bc2rt.en == 1:
                for i in range(20):
                    s.cmd_in <<= concat(s.bc2rt.msg.cmd_word[2*i+1], s.bc2rt.msg.cmd_word[2*i])
        """
        s.ram = [Wire(16) for i in range(4096)]
        s.ram_next = [Wire(16) for i in range(4096)]

        s.dout = Wire(16)
        s.dout_next = Wire(16)

        @update
        def ram_load_logic():
            if s.data_true_data_packet:
                s.ram_next[0] @= s.recv_data.odata
            else:
                s.ram_next[0] @= 0
            if s.cmd_true_data_packet:
                s.ram_next[1] @= s.recv_cmd.odata
            else:
                s.ram_next[1] @= 0


        @update_ff
        def ien_logic():
            if (s.data_true_data_packet == 1) & (s.recv_data.odone == 0):
                s.ien <<= 1
            else:
                s.ien <<= 0

        @update
        def ram_read_logic():
            if s.ien:
                s.trans_data.idata @= 0xabcd

        @update_ff
        def update_ram():
            s.dout <<= s.dout_next
            for i in range(4096):
                s.ram[i] <<= s.ram_next[i]


    def line_trace(s):
        return s.trans_data.line_trace()










