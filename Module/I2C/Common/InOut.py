from pymtl3 import *

class InOutPort(Component):
    def construct(s):
        s.in_ = InPort(1)
        s.out = OutPort(1)
        s.en  = Wire(1)
        s.data = Wire(1)
        @update
        def tri_logic():
            if s.en:
                s.data @= s.out
            else:
                s.in_ @= s.data


