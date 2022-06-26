from pymtl3 import *

class EnCoder(Component):
    def construct(s):
        # Interface
        s.in_  = InPort(1)
        s.out  = OutPort(1)
        s.tmp  = Wire(2)
        s.flag = Wire(1) # sign start and end

        @update_ff
        def decode_logic():
            if s.flag == 1:
                if s.in_ == 0:
                    s.tmp <<= 1
                else:
                    s.tmp <<= 2
        @update_ff
        def flag_logic():
            s.flag <<= ~s.flag

        @update
        def out_logic():
            if s.flag == 0:
                s.out @= s.tmp[1]
            else:
                s.out @= s.tmp[0]


    def line_trace(s):
        return f"in:{s.in_} out:{s.out} tmp:{s.tmp} flag:{s.flag} "


