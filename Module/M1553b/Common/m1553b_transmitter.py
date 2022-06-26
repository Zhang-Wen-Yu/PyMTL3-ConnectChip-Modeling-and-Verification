# ================================
# M1553b Transmitter
# ================================
from pymtl3 import *

class m1553b_transmitter(Component):
    def construct(s, data_manchester= 32, word_manchester = 40):

        # --------------------------
        # 1553b Transmitter Interface
        # --------------------------
        s.icd   = InPort(1)
        s.ien   = InPort(1)
        s.idata = InPort(16)
        s.odo   = OutPort(2)
        s.obusy = OutPort(1)

        # registers
        s.data_buf   = Wire(16)
        s.cd_buf     = Wire(1)
        s.length_bit = Wire(3)
        s.cntr_bit   = Wire(6)

        s.DATA_MANCHESTER = Wire(data_manchester)
        s.WORD_MANCHESTER = Wire(word_manchester)
        s.Parity  = Wire(1)

        @update_ff
        def length_bit_cntr():
            if s.reset:
                s.length_bit <<= 0
            else:
                if s.ien:
                    s.length_bit <<= 0
                else:
                    s.length_bit <<= s.length_bit + 1


        @update_ff
        def buffer_logic():
            if s.reset:
                s.data_buf <<= 0
                s.cd_buf <<= 0
            else:
                if s.ien:
                    s.data_buf <<= s.idata
                    s.cd_buf <<= s.icd

        @update_ff
        def cntr_logic():
            if s.reset:
                s.cntr_bit <<= 19
            else:
                if s.ien:
                    s.cntr_bit <<= 19
                elif (s.cntr_bit != 0) :
                    s.cntr_bit <<= s.cntr_bit - 1
                elif s.cntr_bit == 0:
                    s.cntr_bit <<= 19

        @update_ff
        def obusy_logic():
            if s.reset:
                s.obusy <<= 0
            else:
                if s.ien:
                    s.obusy <<= 1
                elif (s.cntr_bit == 0):
                    s.obusy <<= 0

        @update_ff
        def output_logic():
            if s.obusy:
                s.odo <<= concat(s.WORD_MANCHESTER[2*s.cntr_bit+1], s.WORD_MANCHESTER[2*s.cntr_bit])
            else:
                s.odo <<= 0

        @update
        def gen_manchester():
            for i in range(16):
                s.DATA_MANCHESTER[2*i]   @= ~s.data_buf[i]
                s.DATA_MANCHESTER[2*i+1] @= s.data_buf[i]

            s.WORD_MANCHESTER[34:40] @= 0b000111 if s.cd_buf else 0b111000
            s.WORD_MANCHESTER[2:34]  @= s.DATA_MANCHESTER
            s.WORD_MANCHESTER[0:2]   @= 0b10 if s.Parity else 0b01
            s.Parity @= ~reduce_xor(s.data_buf)

    def line_trace(s):
        return f"WORD_MANCHESTER:{s.WORD_MANCHESTER} DATA_MANCHESTER:{s.DATA_MANCHESTER} " \
               f" ien:{s.ien} idata:{s.idata} odo:{s.odo} cntr_bit:{s.cntr_bit} obusy:{s.obusy} parity:{s.Parity}"













