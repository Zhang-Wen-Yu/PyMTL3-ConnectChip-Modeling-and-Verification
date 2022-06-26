from pymtl3 import *

class PushOutIfc( Interface ):

  def construct( s, Type ):
    s.en  = OutPort()
    s.msg = OutPort( Type )

    s.trace_len = len( f'{Type}' )

  def __str__( s ):
    if s.en:
      return f'{s.msg}'
    return ' '.ljust( s.trace_len )
