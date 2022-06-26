from pymtl3 import *

class i2c_slave( Component ):

    def construct(s):


        s.enable = InPort(1)
        s.sda_in  = InPort(1)
        s.sda_out = OutPort(1)
        s.scl  = InPort(1)
        s.data_recv = OutPort(8)


        # registers
        s.direction = Wire(1)
        s.SDA = Wire(1)

        @update
        def sda_logic():
            s.sda_out @= s.SDA

        s.add_in     = Wire(8)
        s.state      = Wire(4)
        s.addr       = Wire(8)
        s.cntr       = Wire(3)
        s.ack_       = Wire(1)
        s.recv_bit   = Wire(1)
        s.read_value = Wire(8)

        # state define
        s.idle       = 0
        s.start      = 1
        s.add_rw     = 2
        s.ack        = 3
        s.data_read  = 4
        s.data_write = 5
        s.rack       = 6
        s.wack       = 7
        s.stop       = 8

        @update
        def read_value_init():
            s.read_value @= 0xff

        @update_ff
        def seq_logic():
            if s.reset:
                s.state <<= s.idle
                s.cntr <<= 0
            else:
                if s.state == s.idle:
                    s.direction <<= 0

                    s.state <<= s.start
                elif s.state == s.start:
                    if s.sda_in == 0:
                        s.cntr <<= 7
                        s.state <<= s.add_rw
                    else:
                        s.state <<= s.start

                elif s.state == s.add_rw:
                    if s.scl == 0:
                        s.add_in[s.cntr - 1] <<= s.sda_in
                        s.cntr <<= s.cntr - 1
                        if s.cntr == 0:
                            s.state <<= s.ack
                            s.cntr <<= 0
                            s.SDA <<= 0
                            s.direction <<= 1
                        else:
                            s.state <<= s.add_rw
                    else:
                        s.state <<= s.add_rw

                elif s.state == s.ack:
                    if s.add_in[1:8] == s.addr[1:8]:
                        s.SDA <<= 0
                        s.direction <<= 1
                        if s.add_in[0] == 0:
                            s.state <<= s.data_read
                            s.direction <<= 1
                            s.cntr <<= 7
                            s.SDA <<= s.read_value[7]
                        else:
                            s.state <<= s.data_write
                            s.direction <<= 0
                            s.cntr <<= 7
                    else:
                        s.SDA <<= 1
                        s.state <<= s.idle
                elif s.state == s.data_read:
                    if s.scl == 0:
                        s.SDA <<= s.read_value[s.cntr - 1]
                        s.cntr <<= s.cntr - 1
                        if s.cntr == 0:
                            s.state <<= s.rack
                            s.direction <<= 0
                        else:
                            s.state <<= s.data_read
                    else:
                        s.state <<= s.data_read
                elif s.state == s.data_write:
                    if s.scl == 0:
                        s.data_recv[s.cntr -1] <<= s.sda_in
                        s.cntr <<= s.cntr - 1
                        if s.cntr == 0:
                            s.state <<= s.wack
                            s.direction <<= 1
                            s.SDA <<= 0
                        else:
                            s.state <<= s.data_write
                    else:
                        s.state <<= s.data_write
                elif s.state == s.rack:
                    if s.scl == 0:
                        s.ack_ <<= s.sda_in
                        if s.ack_ == 0:
                            s.state <<= s.stop
                        else:
                            s.state <<= s.idle
                    else:
                        s.state <<= s.rack
                elif s.state == s.wack:
                    s.SDA <<= 0
                    s.direction <<= 1
                    s.state <<= s.stop

                elif s.state == s.stop:
                    s.ack_ <<= s.sda_in
                    s.state <<= s.idle
                else:
                    s.state <<= s.idle

    def line_trace(s):
        return f"state:{s.state} sda_i:{s.sda_in} sda_o:{s.sda_out} scl:{s.scl} cntr:{s.cntr}"


















