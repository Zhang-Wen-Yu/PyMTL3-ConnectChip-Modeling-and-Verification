from pymtl3 import *

class PullInIfc( Interface ):

  def construct( s, Type ):
    s.en  = OutPort()
    s.msg = InPort ( Type )

    s.trace_len = len( f'{Type}' )

  def __str__( s ):
    if s.en:
      return f'{s.msg}'
    return ' '.ljust( s.trace_len )

