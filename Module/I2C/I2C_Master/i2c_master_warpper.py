# ================================
# I2C Master
# ================================
from pymtl3 import *
from pymtl3.stdlib.ifcs.send_recv_ifcs import RecvIfcRTL, SendIfcRTL
from Module.I2C.Common.i2c_msg import *
from pymtl3.stdlib.basic_rtl import RegEn
from pymtl3.stdlib.basic_rtl.registers import RegRst

req_type  = mk_i2c_req_msg(8)
resp_type = mk_i2c_resp_msg(8)

class i2c_master(Component):
    def construct(s, clk_per_half_bit= 4, pack_size = 8):

        # --------------------------
        # I2C Master Interface
        # --------------------------
        s.SDA_i = InPort()
        s.SDA_o = OutPort()
        s.SCL = OutPort()
        s.dir = Wire()
        s.rw = Wire()

        s.req  = RecvIfcRTL(req_type)
        s.resp = SendIfcRTL(resp_type)
        # --------------------------
        # state define
        # --------------------------

        s.user_reset = 0
        s.idle = 1
        s.handshake = 2
        s.transfer = 3
        s.finish = 4
        s.ack = 5

        s.state = Wire(3)
        s.cntr = Wire(8)
        s.cntr_max = Wire(8)
        s.scl_en = Wire(1)
        s.scl_cntr = Wire(4)

        # State Transition Logic
        @update_ff
        def state_transitions():
            if s.reset:
                s.state <<= s.user_reset
            if s.state == s.user_reset:
                s.state <<= s.idle
            if s.state == s.idle:
                if s.resp.rdy & s.req.en:
                    s.state <<= s.handshake
            if s.state == s.handshake:
                if s.cntr >= clk_per_half_bit:
                    s.state <<= s.transfer
            if s.state == s.transfer:
                if s.cntr >= (2 * clk_per_half_bit * pack_size) - 1:
                    s.state <<= s.finish
            if s.state == s.finish:
                if s.cntr >= clk_per_half_bit:
                    s.state <<= s.ack
            if s.state == s.ack:
                if s.cntr >= clk_per_half_bit:
                    s.state <<= s.idle

        # Maximum Counter Value
        @update
        def max_counter_values():
            if s.state == s.user_reset:
                s.cntr_max @= clk_per_half_bit
            if s.state == s.idle:
                s.cntr_max @= clk_per_half_bit
            if s.state == s.handshake:
                s.cntr_max @= clk_per_half_bit
            if s.state == s.transfer:
                s.cntr_max @= (2 * clk_per_half_bit * pack_size) - 1
            if s.state == s.finish:
                s.cntr_max @= clk_per_half_bit
            if s.state == s.ack:
                s.cntr_max @= clk_per_half_bit

        # SCL Logic
        @update
        def sclk_logic():
            if s.state == s.transfer:
                s.scl_en @= 1
            else:
                s.scl_en @= 0

        # Counter Logic
        @update_ff
        def counter_logic():
            if s.state == s.idle:
                s.cntr <<= 0
            elif (s.cntr >= s.cntr_max) & (s.state != s.idle):
                s.cntr <<= 0
            else:
                s.cntr <<= s.cntr + 1

        # Generate SCL
        @update_ff
        def generate_scl():
            if s.scl_en:
                if s.scl_cntr == 0:
                    s.SCL <<= ~s.SCL
                    s.scl_cntr <<= s.scl_cntr + 1
                elif s.scl_cntr == clk_per_half_bit - 1:
                    s.SCL <<= s.SCL
                    s.scl_cntr <<= 0
                else:
                    s.SCL <<= s.SCL
                    s.scl_cntr <<= s.scl_cntr + 1
            else:
                 # when SCL high，it’s control command
                s.SCL <<= 1
                s.scl_cntr <<= 0

        # SDA_o Datapath
        s.sda_o_reg = RegEn(pack_size)
        s.sda_o_reg_pointer = Wire(4)
        s.sda_o_reg.in_ //= s.req.msg.data

        @update
        def comb_logic():
            if s.req.msg.type_ == I2cMsgType.WRITE:
                s.rw @= 1  # WRITE ENABLE
            else:
                s.rw @= 0

        @update
        def sda_o_reg_en():
            if (s.state == s.idle) & (s.req.en == 1) & (s.rw == 1):
                s.sda_o_reg.en @= 1
            else:
                s.sda_o_reg.en @= 0

        @update
        def sda_o_msb():
            s.SDA_o @= s.sda_o_reg.out[s.sda_o_reg_pointer]

        @update_ff
        def sda_o_shift_reg():
            if s.state == s.idle:
                s.sda_o_reg_pointer <<= pack_size - 1
            if s.state == s.transfer:
                if (s.SCL == 0) & (s.scl_cntr == 0):
                    if s.sda_o_reg_pointer == 0:
                        s.sda_o_reg_pointer <<= 0
                    else:
                        s.sda_o_reg_pointer <<= s.sda_o_reg_pointer - 1

        # SDA_i Datapath
        s.sda_i_reg = Wire(mk_bits(pack_size))
        s.resp.msg.data //= s.sda_i_reg

        @update_ff
        def sda_i_shift_reg():
            if s.state == s.idle:
                s.sda_i_reg <<= 0
            if (s.state == s.transfer) & (s.rw == 0):
                if (s.SCL == 1) & (s.scl_cntr == 0):
                    # [0:pack_size-1]: 0 means low bit,7 means high bit
                    s.sda_i_reg <<= concat(s.sda_i_reg[0:pack_size - 1], s.SDA_i)

        # val rdy interface
        @update
        def req_rdy():
            s.req.rdy @= s.resp.rdy & (s.state == s.idle)
        s.result_read = Wire(1)

        @update
        def result_read():
            if s.state == s.user_reset:
                s.result_read @= 0
            if s.state == s.idle:
                if (s.result_read == 0) & (s.resp.rdy == 0):
                    s.result_read @= 0
                else:
                    s.result_read @= 1
            if s.state == s.handshake:
                s.result_read @= 0
            if s.state == s.transfer:
                s.result_read @= 0
            if s.state == s.finish:
                s.result_read @= 0
            if s.state == s.ack:
                if (s.resp.rdy == 1) & (s.cntr > 0):
                    s.result_read @= 1

        s.val_progressing = Wire(1)
        s.msg_from_slave = Wire(1)

        @update
        def valid_resp():
            if s.state == s.user_reset:
                s.val_progressing @= 0
                s.msg_from_slave @= 0
            elif (s.state == s.idle) & (s.req.en == 1):
                s.val_progressing @= 1
                s.msg_from_slave @= 0
            elif (s.state == s.ack) & (s.val_progressing == 1):
                s.msg_from_slave @= 1
            else:
                s.val_progressing @= s.val_progressing

        @update
        def resp_val():
            if (s.state == s.ack) & (s.result_read == 0) & (s.msg_from_slave == 1):
                s.resp.en @= 1
            elif (s.state == s.idle) & (s.result_read == 0) & (s.msg_from_slave == 1):
                s.resp.en @= 1
            else:
                s.resp.en @= 0

    def line_trace(s):
        return f"req_en:{s.req.en} req_rdy:{s.req.rdy} state:{s.state} SDA_i:{s.SDA_i} SDA_O:{s.SDA_o} SCL:{s.SCL}"
