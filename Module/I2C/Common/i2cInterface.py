from pymtl3 import *

class i2c_master_ifc( Interface ):

    def construct(s):
        s.sda_in  = InPort()
        s.sda_out = OutPort()
        s.sda_oen = OutPort()


        s.scl_out = OutPort()
        s.scl_oen = OutPort()
        s.scl_in  = InPort()


class i2c_slave_ifc( Interface ):

    def construct(s):
        s.sda_in  = InPort()
        s.sda_out = OutPort()
        s.sda_oen = OutPort()

        s.scl_in  = InPort()
        s.scl_oen = OutPort()
        s.scl_out = OutPort()









