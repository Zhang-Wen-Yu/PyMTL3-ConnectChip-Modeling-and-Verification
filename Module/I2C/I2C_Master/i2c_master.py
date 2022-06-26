from pymtl3 import *
from pymtl3.stdlib.ifcs.send_recv_ifcs import RecvIfcRTL, SendIfcRTL
from Module.I2C.Common.i2c_msg import *
from pymtl3.stdlib.basic_rtl import RegEn

req_type = mk_i2c_req_msg(8)
resp_type = mk_i2c_resp_msg(8)

class i2c_master( Component ):

    def construct(s):

        s.req  = RecvIfcRTL(req_type)
        s.resp = SendIfcRTL(resp_type)


        # device interface
        s.scl     = OutPort(1)
        s.sda_out = OutPort(1)
        s.sda_in  = InPort(1)

        # register
        s.data_in    = Wire(8)
        s.direction  = Wire(1)
        s.SDA        = Wire(1)
        s.read_write = Wire(1)


        @update
        def sda_logic():
            s.sda_out @= s.SDA

        @update
        def read_write_logic():
            if s.state == s.idle:
                if s.req.msg.type_ == 0:
                    s.read_write @= 0
                else:
                    s.read_write @= 1

        s.state = Wire(4)
        s.addr  = Wire(8)  # address including read/write bit
        s.cntr  = Wire(3)
        s.ack_  = Wire(1)
        s.ack1  = Wire(1)
        s.recv_bit = Wire(1)


        s.idle       = 0
        s.start      = 1
        s.addr_rw    = 2
        s.ack        = 3
        s.data_read  = 4
        s.data_write = 5
        s.rack       = 6
        s.wack       = 7
        s.stop       = 8

        @update
        def req_rdy():
            s.req.rdy @= 1

        @update_ff
        def scl_logic():
            if s.reset:
                s.scl <<= 1
            else:
                if (s.state == s.idle) | (s.state == s.start):
                    s.scl <<= 1
                else:
                    s.scl <<= ~s.scl

        @update
        def resp_data_logic():
            if s.state == s.rack:
                if s.scl == 0:
                    #if s.cntr == 0:
                    s.resp.msg.data @= s.data_in

        s.sda_reg = RegEn(8)
        s.sda_reg.in_ //= s.req.msg.data

        @update
        def sda_reg_en():
            if (s.state == s.idle) & (s.req.en == 1):
                s.sda_reg.en @= 1
            else:
                s.sda_reg.en @= 0

        @update_ff
        def state_trans():
            if s.reset:
                s.state <<= s.idle
                s.direction <<= 1
                s.SDA <<= 1
                s.addr <<= 0b10101111
                s.cntr <<= 0
            else:
                if s.state == s.idle:
                    s.direction <<= 1
                    s.SDA <<= 1
                    s.state <<= s.start
                    s.addr <<= concat(Bits7(87), s.read_write)
                elif s.state == s.start:
                    s.SDA <<= 0
                    s.cntr <<= 7
                    s.state <<= s.addr_rw
                elif s.state == s.addr_rw:
                    if s.scl == 0:
                        s.SDA <<= s.addr[s.cntr-1]
                        if s.cntr == 0:
                            s.state <<= s.ack
                            s.direction <<= 0
                        else:
                            s.cntr <<= s.cntr - 1
                    else:
                        s.state <<= s.addr_rw
                elif s.state == s.ack:
                    s.ack_ <<= s.sda_in
                    if s.ack_ == 0:
                        if s.addr[0]:
                            s.state <<= s.data_write
                            s.cntr <<= 7
                            s.direction <<= 1
                            s.SDA <<= 0
                        else:
                            s.state <<= s.data_read
                            s.cntr <<= 7
                            s.direction <<= 0
                    else:
                        s.state <<= s.idle
                elif s.state == s.data_read:
                    if s.scl == 0:
                        s.recv_bit <<= s.sda_in
                        s.data_in <<= concat(s.data_in[0:7], s.recv_bit)
                        s.cntr <<= s.cntr - 1
                        if s.cntr == 0:
                            s.state <<= s.rack
                            s.direction <<= 1
                            s.SDA <<= 0
                        else:
                            s.state <<= s.data_read
                    else:
                        s.state <<= s.data_read

                elif s.state == s.data_write:
                    if s.scl == 0:
                        s.SDA <<= s.sda_reg.out[s.cntr-1]
                        s.cntr <<= s.cntr - 1
                        if s.cntr == 0:
                            s.state <<= s.wack
                            s.direction <<= 0
                        else:
                            s.state <<= s.data_write
                    else:
                        s.state <<= s.data_write

                elif s.state == s.rack:
                    if s.scl == 0:
                        s.SDA <<= 0
                        s.state <<= s.stop
                    else:
                        s.state <<= s.rack
                elif s.state == s.wack:
                    if s.scl == 0:
                        s.ack1 <<= s.sda_in
                        if s.ack1 == 0:
                            s.state <<= s.stop
                            s.direction <<= 1
                        else:
                            s.state <<= s.idle
                    else:
                        s.state <<= s.wack
                elif s.state == s.stop:
                    s.SDA <<= 1
                    s.state <<= s.idle
                else:
                    s.state <<= s.idle

        s.val_progressing = Wire(1)
        s.msg_from_slave = Wire(1)

        @update
        def valid_resp():
            if s.reset:
                s.val_progressing @= 0
                s.msg_from_slave @= 0
            elif (s.state == s.idle) & (s.req.en == 1):
                s.val_progressing @= 1
                s.msg_from_slave @= 0
            elif (s.state == s.stop) & (s.val_progressing == 1):
                s.msg_from_slave @= 1
            else:
                s.val_progressing @= s.val_progressing

        s.result_read = Wire(1)
        @update
        def result_read():
            if s.reset:
                s.result_read @= 0
            if s.state == s.idle:
                if (s.result_read == 0) & (s.resp.rdy == 0):
                    s.result_read @= 0
                else:
                    s.result_read @= 1
            if (s.state == s.start) | (s.state == s.ack) | (s.state == s.addr_rw):
                s.result_read @= 0
            if (s.state == s.data_read) | (s.state == s.data_write):
                s.result_read @= 0
            if (s.state == s.rack) | (s.state == s.wack):
                s.result_read @= 0
            if s.state == s.stop:
                if (s.resp.rdy == 1) & (s.cntr < 7):
                    s.result_read @= 1

        @update
        def resp_val():
            if (s.state == s.stop) & (s.result_read == 0) & (s.msg_from_slave == 1):
                s.resp.en @= 1
            elif (s.state == s.idle) & (s.result_read == 0) & (s.msg_from_slave == 1):
                s.resp.en @= 1
            else:
                s.resp.en @= 0


    def line_trace(s):
        return f" mode:{s.read_write} state:{s.state} sda_in:{s.sda_in[0]} " \
               f"sda_out:{s.sda_out[0]} scl:{s.scl} s.recv_bit:{s.recv_bit} addr:{s.addr} data_in:{s.data_in} SDA:{s.SDA}"













