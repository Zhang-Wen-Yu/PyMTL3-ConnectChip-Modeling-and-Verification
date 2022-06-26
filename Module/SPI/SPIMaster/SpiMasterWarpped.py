# =========================================================================
# SPIMaster
# =========================================================================

from Module.SPI.Common.SPIIfc import *
from pymtl3.stdlib.basic_rtl import RegEn
from pymtl3.stdlib.stream.ifcs import *

class Spi_Master_Warpped(Component):

    def construct(s, pack_size = 8, clks_per_half_bit = 4):
        # ---------------------------------------------
        # SPI Interface
        # ---------------------------------------------
        s.master_ifc = SPIMasterIfc()
        # --------------------------------------------
        # Interfaces
        # --------------------------------------------
        s.req  = RecvIfcRTL(mk_bits(pack_size))
        s.resp = SendIfcRTL(mk_bits(pack_size))
        # ---------------------------------------------
        # State Definitions
        # ---------------------------------------------
        s.user_reset = 0
        s.idle = 1
        s.handshake = 2
        s.transfer = 3
        s.finish = 4
        s.complete = 5


        s.state = Wire(3)
        s.cntr = Wire(7)
        s.cntr_max = Wire(7)
        s.sclk_en = Wire(1)
        s.sclk_cntr = Wire(4)

        # State Transition Logic
        @update_ff
        def state_transitions():
            if s.reset:
                s.state <<= s.user_reset
            if s.state == s.user_reset:
                s.state <<= s.idle
            if s.state == s.idle:
                if s.resp.rdy & s.req.val:
                    s.state <<= s.handshake
            if s.state == s.handshake:
                if s.cntr >= clks_per_half_bit:
                    s.state <<= s.transfer
            if s.state == s.transfer:
                if s.cntr >= (2 * clks_per_half_bit * pack_size) - 1:
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
            if s.state == s.transfer:
                s.cntr_max @= (2 * clks_per_half_bit * pack_size) - 1
            if s.state == s.finish:
                s.cntr_max @= clks_per_half_bit
            if s.state == s.complete:
                s.cntr_max @= clks_per_half_bit

        # CS Logic
        @update
        def cs_logic():
            if s.state == s.user_reset:
                s.master_ifc.cs @= 1
            if s.state == s.idle:
                s.master_ifc.cs @= 1
            if s.state == s.handshake:
                s.master_ifc.cs @= 0
            if s.state == s.transfer:
                s.master_ifc.cs @= 0
            if s.state == s.finish:
                s.master_ifc.cs @= 0
            if s.state == s.complete:
                s.master_ifc.cs @= 1

        # SCLK Logic
        @update
        def sclk_logic():
            if s.state == s.transfer:
                s.sclk_en @= 1
            else:
                s.sclk_en @= 0

        # Counter Logic
        @update_ff
        def counter_logic():
            if s.state == s.idle:
                s.cntr <<= 0
            elif (s.cntr >= s.cntr_max) & (s.state != s.idle):
                s.cntr <<= 0
            else:
                s.cntr <<= s.cntr + 1


        # Generate SCLK
        @update_ff
        def generate_sclk():
            if s.sclk_en:
                if s.sclk_cntr == 0:
                    s.master_ifc.sclk <<= ~s.master_ifc.sclk
                    s.sclk_cntr <<= s.sclk_cntr + 1
                elif s.sclk_cntr == clks_per_half_bit - 1:
                    s.master_ifc.sclk <<= s.master_ifc.sclk
                    s.sclk_cntr <<= 0
                else:
                    s.master_ifc.sclk <<= s.master_ifc.sclk
                    s.sclk_cntr <<= s.sclk_cntr + 1
            else:
                s.master_ifc.sclk <<= 0
                s.sclk_cntr <<= 0

        # MOSI Datapath
        s.mosi_reg = RegEn(pack_size)
        s.mosi_reg_pointer = Wire(4)
        s.mosi_reg.in_ //= s.req.msg
        @update
        def mosi_reg_en():
            if (s.state == s.idle) & (s.req.val == 1) :
                s.mosi_reg.en @= 1
            else:
                s.mosi_reg.en @= 0

        @update
        def mosi_msb():
            s.master_ifc.mosi @= s.mosi_reg.out[s.mosi_reg_pointer]
        @update_ff
        def mosi_shift_reg():
            if s.state == s.idle:
                s.mosi_reg_pointer <<= pack_size - 1
            if s.state == s.transfer:
                if (s.master_ifc.sclk == 1) & (s.sclk_cntr == 0):
                    if s.mosi_reg_pointer == 0:
                        s.mosi_reg_pointer <<= 0
                    else:
                        s.mosi_reg_pointer <<= s.mosi_reg_pointer - 1
        # MISO Datapath
        s.miso_reg = Wire(mk_bits(pack_size))
        s.resp.msg //= s.miso_reg
        @update_ff
        def miso_shift_reg():
            if s.state == s.idle:
                s.miso_reg <<= 0
            if s.state == s.transfer:
                if (s.master_ifc.sclk == 0) & (s.sclk_cntr == 0):
                    # [0:pack_size-1]: 0 means low bit,7 means high bit
                    s.miso_reg <<= concat(s.miso_reg[0:pack_size - 1], s.master_ifc.miso)


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
            if s.state == s.complete:
                if (s.resp.rdy == 1) & (s.cntr > 0):
                    s.result_read @= 1

        s.val_progressing = Wire(1)
        s.msg_from_slave = Wire(1)

        @update
        def valid_resp():
            if s.state == s.user_reset:
                s.val_progressing @= 0
                s.msg_from_slave @= 0
            elif (s.state == s.idle) & (s.req.val == 1):
                s.val_progressing @= 1
                s.msg_from_slave @= 0
            elif (s.state == s.complete) & (s.val_progressing == 1):
                s.msg_from_slave @= 1
            else:
                s.val_progressing @= s.val_progressing

        @update
        def resp_val():
            if (s.state == s.complete) & (s.result_read == 0) & (s.msg_from_slave == 1):
                s.resp.val @= 1
            elif (s.state == s.idle) & (s.result_read == 0) & (s.msg_from_slave == 1):
                s.resp.val @= 1
            else:
                s.resp.val @= 0

    def line_trace(s):
        return f" cs: [{s.master_ifc.cs}]  sclk [{s.master_ifc.sclk}], mosi [{s.master_ifc.mosi}],mosi_reg:{s.mosi_reg} miso [{s.master_ifc.miso}],miso_reg {s.miso_reg}"
