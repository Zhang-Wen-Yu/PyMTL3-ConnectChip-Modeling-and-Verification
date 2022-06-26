from pymtl3 import *

class CrossOver( Component ):

    def construct(s, clks_per_bit = 1):

        s.clk_in  = InPort(1)
        s.clk_out = OutPort(1)
        s.cntr    = 0

        @update_ff
        def clk_division():
            if s.reset:
                s.clk_out <<= 1
            if s.cntr == 0:
                s.clk_out <<= ~s.clk_out
                s.cntr <<= s.cntr + 1
            elif s.cntr == clks_per_bit:
                s.clk_out <<= ~s.clk_out
                s.cntr <<= 0
            else:
                s.clk_out <<= s.clk_out
                s.cntr <<= s.cntr + 1
    def line_trace(s):
        return f"clk:{s.clk_out}"

