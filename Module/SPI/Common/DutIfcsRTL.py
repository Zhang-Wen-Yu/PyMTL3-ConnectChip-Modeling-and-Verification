# =========================
# TX_Buffer
# =========================
from pymtl3 import *
class TxBuffer(Interface):
    def construct(s,nbits):
        s.Byte = InPort(nbits)


# =========================
# RX_Buffer
# =========================
class RxBuffer(Interface):
    def construct(s,nbits):
        s.Byte = OutPort(nbits)