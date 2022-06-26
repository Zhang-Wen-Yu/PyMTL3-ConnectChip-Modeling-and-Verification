from pymtl3 import *
from Module.SPI.Common.Synchronizer import *

class DeCoder(Component):
    def construct(s,clks_per_half_bit = 2):
        # Interface
        s.in_   = InPort(1)
        s.out   = OutPort(1)
        s.tmp   = Wire(2)
        s.flag1 = Wire(1) # sign start
        s.flag2 = Wire(1) # sign decode
        s.cntr1 = Wire(2)
        s.cntr2 = Wire(2)
        s.clk1  = Wire(1)
        @update_ff
        def flag_logic():
            if s.reset:
                s.flag1 <<= 0
            if (s.tmp == 0) | (s.tmp == 3):
                s.flag1 <<= 1
        # Generate CLK1
        @update_ff
        def generate_clk():
            s.clk1 <<= ~s.clk1
        s.clk1_sync     = Synchronizer()
        s.clk1_sync.in_ //= s.clk1
        # Generate FLAG2
        @update_ff
        def generate_flag2():
            if s.reset:
                s.flag2 <<= 1
            if s.clk1_sync.posedge_ == 1:
                if s.flag1 == 1:
                    s.flag2 <<= ~s.flag2
            if s.clk1_sync.negedge_ == 1:
                s.tmp <<= concat(s.in_, s.tmp[1])

        @update
        def out_logic():
            if s.flag2 == 0:
                if s.tmp == 2:
                    s.out @= 0

                elif s.tmp == 1:
                    s.out @= 1

                elif (s.tmp == 0) | (s.tmp == 3):
                    s.out @= 0

    def line_trace(s):
        return f"in:{s.in_} out:{s.out} tmp:{s.tmp} flag1:{s.flag1} flag2:{s.flag2} "







