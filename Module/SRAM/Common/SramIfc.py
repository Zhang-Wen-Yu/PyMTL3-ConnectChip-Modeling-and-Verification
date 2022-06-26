from pymtl3 import *

class SramIfc(Interface):

    def construct(s, num_bits = 32, num_words = 256,bank_num = 4):

        s.addr_width = clog2( num_words )           # address width

        s.CE1  = InPort()                           # clk
        s.WE1 = InPort()                            # write enable
        s.OE1 = InPort()                            # out enable
        s.CS1 = InPort()                            # sdram select
        s.A1   = InPort( mk_bits(s.addr_width) )    # address
        s.I1   = InPort( mk_bits( num_bits ) )      # write data
        s.O1   = OutPort(mk_bits( num_bits ) )      # read data
        s.WBM1 = InPort( mk_bits( num_bits ) )      # bit-level write mask
        s.BA1   = InPort( mk_bits( clog2(bank_num) ))

class SramContrIfc(Interface):

    def construct(s, num_bits=32, num_words=256, bank_num =4):

        s.addr_width = clog2(num_words)       # address width

        s.CE1  = OutPort()                      # clk
        s.WE1  = OutPort()                      # write enable
        s.OE1  = OutPort()                      # out enable
        s.CS1  = OutPort()                      # sdram select
        s.A1   = OutPort(mk_bits(s.addr_width))  # address
        s.I1   = OutPort(mk_bits(num_bits))      # write data
        s.O1   = InPort(mk_bits(num_bits))     # read data
        s.WBM1 = OutPort(mk_bits(num_bits))    # bit-level write mask
        s.BA1  = OutPort( mk_bits( clog2(bank_num) ))
