from pymtl3 import *

class promIfc( Interface ):

    def construct(s):

        s.data  = OutPort(8)   # serial output
        s.CE1   = InPort()     # chip select
        s.busy  = InPort()
        s.OE1   = InPort()
        s.CLK   = InPort()
        # JTAG
        s.TDO   = OutPort()
        s.TCK   = InPort()  # test clk input
        s.TDI   = InPort()  # test data input
        s.TMS   = InPort()  # test mode select



