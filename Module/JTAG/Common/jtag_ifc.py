from pymtl3 import *

class jtagIfc_fpga( Interface ):

    def construct(s):

        s.TDI = InPort()
        s.TDO = OutPort()
        s.TMS = InPort()
        s.TCK = InPort()

class jtagIfc_pc( Interface ):

    def construct(s):

        s.TDI = OutPort()
        s.TDO = InPort()
        s.TMS = OutPort()
        s.TCK = OutPort()
