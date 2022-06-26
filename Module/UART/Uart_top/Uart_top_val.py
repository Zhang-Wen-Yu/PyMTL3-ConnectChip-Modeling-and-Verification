# ========================================
# UART receiver and transmitter
# ========================================

from pymtl3 import *
from Module.UART.Uart_submodule.UartRx import *
from Module.UART.Uart_submodule.UartTx import *
from pymtl3.stdlib.ifcs.send_recv_ifcs import RecvIfcRTL, SendIfcRTL
from pymtl3.stdlib.basic_rtl.registers import RegRst

class uart_val( Component ):

    def construct(s,pack_size = 8):

        s.tx = UartTxd()  # receiver
        s.rx = UartRxd()  # transmitter

        s.txd   = OutPort(1)
        s.rxd   = InPort(1)
        s.stop  = Wire(1)
        s.state = Wire(2)

        s.stop_end = Wire(1)


        connect(s.txd, s.tx.txd)
        connect(s.rxd, s.rx.rxd)
        connect(s.stop, s.rx.stop_bit_mid)
        connect(s.stop_end, s.tx.stop_bit_end)
        connect(s.state,s.tx.state)


        s.req  = RecvIfcRTL(mk_bits(pack_size))
        s.resp = SendIfcRTL(mk_bits(pack_size))

        @update
        def val_rdy_logic():
            s.req.rdy @= s.resp.rdy & (s.state == s.tx.idle)

        @update
        def resp_logic():
            if (s.stop == 1) & (s.stop_end == 1):
                s.resp.en @= 1
            else:
                s.resp.en @= 0

        @update
        def preload():
            if s.state == s.tx.idle:
                s.tx.preload_data @= s.req.msg
        s.rx.recv_data //= s.resp.msg










