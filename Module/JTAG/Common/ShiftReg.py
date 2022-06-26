# ==========================================================================
# ShiftReg.py
# ==========================================================================

from pymtl3 import *
class ShiftReg( Component ):

  def construct( s, nbits ):

    # Local Parameters
    s.nbits = nbits

    # Interface
    s.in_       = InPort ()
    s.out       = OutPort( s.nbits )
    s.shift_en  = InPort ()
    s.load_en   = InPort ()
    s.load_data = InPort ( s.nbits )

    # Logic

    @update_ff
    def up_shreg():
      if ( s.load_en ):
        s.out <<= s.load_data
      elif ( ~s.load_en & s.shift_en ):
        s.out <<= concat( s.out[0:s.nbits-1], s.in_ )

