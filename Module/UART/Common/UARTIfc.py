from pymtl3 import *

class UartRx( Interface ):

    def construct( s):

        s.rxd  = InPort( )



class UartTx( Interface ):
    def construct( s ):

        s.txd = OutPort( )

