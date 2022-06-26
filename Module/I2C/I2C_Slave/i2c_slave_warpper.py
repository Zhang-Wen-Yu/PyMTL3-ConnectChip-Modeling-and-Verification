# ================================
# I2C Slave
# ================================
from pymtl3 import *
from Module.I2C.Common.Synchronizer import *
from Module.SPI.Common.ShiftReg import ShiftReg
from Module.SPI.Common.PullInIfc import PullInIfc
from Module.SPI.Common.PushOutIfc import PushOutIfc

class i2c_slave(Component):
    def construct(s):
        s.nbits = 8

        # --------------------------
        # I2C Slave Interface
        # --------------------------
        s.SDA_i = InPort(1)
        s.SDA_o = OutPort(1)
        s.SCL = InPort(1)
        s.dir = Wire(1)

        s.push = PushOutIfc(s.nbits)
        s.pull = PullInIfc(s.nbits)

        # Components & Logic
        s.sclk_sync = Synchronizer()
        s.sclk_sync.in_ //= s.SCL
        s.sdai_sync = Synchronizer()
        s.sdai_sync.in_ //= s.SDA_i

        s.shreg_in = m = ShiftReg(s.nbits)
        m.in_ //= s.sdai_sync.out
        m.shift_en //= lambda: s.sclk_sync.negedge_
        m.load_en //= 0
        m.load_data //= 0

        s.shreg_out = m = ShiftReg(s.nbits)
        m.in_ //= 0
        m.shift_en //= lambda: s.sclk_sync.posedge_
        m.load_en //= s.pull.en
        m.load_data //= s.push.msg

        s.SDA_o //= s.shreg_out.out[s.nbits - 1]
        s.pull.en //= s.sdai_sync.negedge_
        s.push.en //= s.sdai_sync.posedge_
        s.push.msg //= s.shreg_in.out


    def line_trace(s):
        return f""
