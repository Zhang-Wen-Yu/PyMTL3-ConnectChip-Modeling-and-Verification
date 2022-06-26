from pymtl3 import *

class SPIMasterIfc( Interface ):

  def construct( s ):
    s.cs   = OutPort(1)
    s.sclk = OutPort(1)
    s.miso = InPort(1)
    s.mosi = OutPort(1)

class SPISlaveIfc(Interface):

    def construct(s):
        s.cs = InPort(1)
        s.sclk = InPort(1)
        s.miso = OutPort(1)
        s.mosi = InPort(1)
