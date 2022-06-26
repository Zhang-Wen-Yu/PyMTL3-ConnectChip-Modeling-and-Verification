# ============================================
# SRAM Memory
# ============================================

from pymtl3 import *
from Module.SRAM.Common.SramIfc import *

class Sram( Component ):

    def construct(s, num_bits = 32, num_words = 256 ,row_num = 4):

        # this is 256 x 32 SRAM bank num = 4
        # num_bits  ：data num
        # num_words : address num
        # address width : 8
        # data width : 32

        #  Port Name          Direction        Description
        #  -----------------------------------------------------------------------
        #  s.sdram_inter.CS1      I           sdram select (1 = enabled)
        #  s.sdram_inter.WE1      I           transaction type(write enable), 0 = read, 1 = write
        #  s.sdram_inter.OE1      I           if nor not output the read data, 0 = output, 1 = not output
        #  s.sdram_inter.CE1      I           sdram clk in
        #  s.sdram_inter.A1       I           sdram address
        #  s.sdram_inter.I1       I           write data input
        #  s.sdram_inter.O1       O           read data output
        #  s.sdram_inter.WBM1     I           write bit enable (1 = enabled)
        #  s.sdram_inter.BA1      I           bank select

        s.sram_ifc = SramIfc()

        s.bank = Bits(clog2(row_num))

        # memory array
        # 256 x 32 port

        @update
        def bank_logic():
            s.bank @= s.sram_ifc.BA1

        # create one col ram
        s.ram_l      = [ Wire( num_bits ) for x in range( num_words )]
        s.ram_next_l = [ Wire( num_bits ) for x in range( num_words )]

        # create every row ram
        s.ram      = [s.ram_l for i in range( row_num)]
        s.ram_next = [s.ram_next_l for i in range(row_num)]

        # read path

        s.dout      = Wire( num_bits )
        s.dout_next = Wire( num_bits )

        @update
        def read_logic():
            s.dout_next @= s.ram[s.sram_ifc.BA1][s.sram_ifc.A1] if (s.sram_ifc.CS1
             & ~s.sram_ifc.WE1) else s.dout
        @update
        def comb_logic():
            s.sram_ifc.O1 @= s.dout if ~s.sram_ifc.OE1 else 0



        # write path
        @update
        def write_logic():
           for i in range(num_bits):
               if s.sram_ifc.CS1 & s.sram_ifc.WE1 & s.sram_ifc.WBM1[i]:
                   s.ram_next[s.sram_ifc.BA1][s.sram_ifc.A1][i] @= s.sram_ifc.I1[i]


        @update_ff
        def update_sram():
            s.dout <<= s.dout_next
            for j in range( row_num ):
                for i in range(num_words):
                    s.ram[j][i] <<= s.ram_next[j][i]

    def line_trace(s):
        return f"(CS= {s.sram_ifc.CS1} WE={s.sram_ifc.WE1} OE={s.sram_ifc.OE1} A1={s.sram_ifc.A1} " \
               f"I1={s.sram_ifc.I1} O1={s.sram_ifc.O1} WBM1={s.sram_ifc.WBM1} BA1={s.sram_ifc.BA1} RAM={s.ram[s.sram_ifc.BA1][s.sram_ifc.A1]})"
