from pymtl3 import *

class FlashIfc( Interface ):
    def construct(s):

        #  Port Name          Direction      Description
        #  -----------------------------------------------------------------------
        #  s.I(0~7)              I           Ins,  transferring address, command, and data to the device
        #  s.O(0~7)              O           Outs, transferring address, command, and data from the device
        #  s.ROB                 I           Ready/Busy(Ready = 1,Busy = 0)
        #  s.RE                  I           Read Enable(enable = 0)
        #  s.CE                  I           Chip Enable(enable = 0)
        #  s.CLE                 I           Command Latch Enable
        #  s.ALE                 O           read data output
        #  s.WE                  I           Write Enable(rising edge)
        #  s.WP                  I           Write Protect(enable = 0)

        s.I   = InPort(8)
        s.O   = OutPort(8)
        s.ROB = OutPort(1)
        s.RE  = InPort(1)
        s.CE  = InPort(1)
        s.CLE = InPort(1)
        s.ALE = InPort(1)
        s.WE  = InPort(1)
        s.WP  = InPort(1)

class FlashCtrIfc( Interface ):
    def construct(s):

        s.I   = OutPort(8)
        s.O   = InPort(8)
        s.ROB = InPort(1)
        s.RE  = OutPort(1)
        s.CE  = OutPort(1)
        s.CLE = OutPort(1)
        s.ALE = OutPort(1)
        s.WE  = OutPort(1)
        s.WP  = OutPort(1)


