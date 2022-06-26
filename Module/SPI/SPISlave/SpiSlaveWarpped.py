# ==========================================================================
# SpiSlaveWarpped.py
# ==========================================================================

from pymtl3 import *
from Module.SPI.Common.Synchronizer import Synchronizer
from Module.SPI.Common.ShiftReg import ShiftReg
from Module.SPI.Common.PullInIfc import PullInIfc
from Module.SPI.Common.PushOutIfc import PushOutIfc
from Module.SPI.Common.SPIIfc import *

class Spi_Slave_Warpped(Component):

  def construct( s, nbits=8  ):

    # Local parameters
    s.nbits = nbits

    # Interface
    s.slave_ifc = SPISlaveIfc()

    s.push = PushOutIfc( s.nbits )
    s.pull = PullInIfc ( s.nbits )

    # Components & Logic
    s.cs_sync = Synchronizer()
    s.sclk_sync = Synchronizer()
    s.sclk_sync.in_ //= s.slave_ifc.sclk
    s.mosi_sync = Synchronizer()
    s.mosi_sync.in_ //= s.slave_ifc.mosi

    s.shreg_in = m = ShiftReg( s.nbits )
    m.in_       //= s.mosi_sync.out
    m.shift_en  //= lambda: ~s.cs_sync.out & s.sclk_sync.posedge_
    m.load_en   //= 0
    m.load_data //= 0

    s.shreg_out = m = ShiftReg( s.nbits )
    m.in_       //= 0
    m.shift_en  //= lambda: ~s.cs_sync.out & s.sclk_sync.negedge_
    m.load_en   //= s.pull.en
    m.load_data //= s.push.msg

    s.slave_ifc.miso     //= s.shreg_out.out[s.nbits-1]
    s.pull.en  //= s.cs_sync.negedge_
    s.push.en  //= s.cs_sync.posedge_
    s.push.msg //= s.shreg_in.out

    @update
    def cs():
      s.cs_sync.in_ @= s.slave_ifc.cs

  def line_trace( s ):
    return f'cs {s.slave_ifc.cs} sclk {s.slave_ifc.sclk}  mosi {s.slave_ifc.mosi}  miso{s.slave_ifc.miso}  ' \
           f'pull_msg {s.pull.msg} push_msg {s.push.msg}'
