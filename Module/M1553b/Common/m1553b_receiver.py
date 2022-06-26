# ================================
# M1553b Recevier
# ================================
from pymtl3 import *
from Module.M1553b.Common.decoder import *

class m1553b_receiver(Component):
    def construct(s):

        # --------------------------
        # 1553b receiver Interface
        # --------------------------
        s.idi   = InPort(2)
        s.odata = OutPort(16)
        s.ocd   = OutPort(1)
        s.odone   = OutPort(1)
        s.oParity_error = OutPort(1)
        #s.decoder  = DeCoder()
        #s.decoder.in_ //= s.idi
        s.manchester = Wire(40)

        # registers
        s.ena_wr      = Wire(1)
        s.in_data          = Wire(1)
        s.reset_length_bit = Wire(1)
        s.true_data_packet = OutPort(1)
        s.data_buf         = Wire(16)
        s.parity_buf       = Wire(1)
        s.cd_buf           = Wire(1)

        @update_ff
        def manchester():
            if s.reset:
                s.manchester <<= 0
            else:
                if ~s.true_data_packet:
                    s.manchester <<= concat(s.manchester[0:38], s.idi)
        @update
        def bit_a():
            for i in range(16):
                s.data_buf[i] @= s.manchester[2*i+3]

        @update_ff
        def output_logic():
            s.odone <<= s.true_data_packet & s.ena_wr
            if s.reset:
                s.odata <<= 0
                s.ocd <<= 0
                s.ena_wr <<= 0
                s.oParity_error <<= 0
            else:
                s.ena_wr <<= 1
                if (s.true_data_packet) & (s.ena_wr):
                    s.ocd <<= s.cd_buf
                    s.odata <<= s.data_buf
                    s.oParity_error <<= ~reduce_xor(concat(s.data_buf, s.parity_buf))

        # comb logic
        @update
        def comb_logic():
            s.true_data_packet @= ((s.manchester[34:40] == 0b000111) | (s.manchester[34:40] == 0b111000)) & ((s.manchester[33] ^ s.manchester[32]) & (s.manchester[31] ^ s.manchester[30]))
            s.parity_buf @= s.manchester[1]
            s.cd_buf @= s.manchester[35]

            
    def line_trace(s):
        return f"manchester: {s.manchester} true_data_packet:{s.true_data_packet} odata:{s.odata} ocd:{s.ocd} odone:{s.odone}"  \
               f"  idi:{s.idi} oParity_error:{s.oParity_error}  "
