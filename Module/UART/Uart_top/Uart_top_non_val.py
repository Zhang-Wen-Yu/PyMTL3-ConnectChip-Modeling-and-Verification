# ========================================
# UART receiver and transmitter
# ========================================

from pymtl3 import *
from Module.UART.Uart_submodule.UartRx import *
from Module.UART.Uart_submodule.UartTx import *

class uart_non_val( Component ):

    def construct(s):

        s.tx = UartTxd()  # receiver
        s.rx = UartRxd()  # transmitter

        s.txd = OutPort(1)
        s.rxd = InPort(1)
        connect(s.txd, s.tx.txd)
        connect(s.rxd, s.rx.rxd)
        s.stop = Wire(1)
        connect(s.stop,s.rx.stop_bit_mid)

        @update
        def comb_logic():
            if s.stop == 1:
                s.tx.preload_data @= s.rx.recv_data



