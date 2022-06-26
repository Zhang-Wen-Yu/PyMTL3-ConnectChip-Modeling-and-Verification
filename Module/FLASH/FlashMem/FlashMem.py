from pymtl3 import *
from Module.FLASH.Common.FlashIfc import *

class FlashMem( Component ):

    def construct(s,num_bits = 8, col_num = 2, page_num = 2, block_num = 2):

        # interface
        #  Port Name          Direction      Description
        #  -----------------------------------------------------------------------
        #  s.I(0~7)              I           Ins,  transferring address, command, and data to the device
        #  s.O(0~7)              O           Outs, transferring address, command, and data from the device
        #  s.ROB                 O           Ready/Busy(Ready = 1,Busy = 0)
        #  s.RE                  I           Read Enable(enable = 0)
        #  s.CE                  I           Chip Enable(enable = 0)
        #  s.CLE                 I           Command Latch Enable
        #  s.ALE                 O           Address Latch Enable
        #  s.WE                  I           Write Enable(rising edge)
        #  s.WP                  I           Write Protect(enable = 0)
        s.ifc = FlashIfc()

        # flash mem array
        s.col = [Wire(num_bits) for i in range(col_num)]
        s.col_next = [Wire(num_bits) for i in range(col_num)]

        # page
        s.page = [s.col for i in range(page_num)]
        s.page_next = [s.col_next for i in range(page_num)]

        # block
        s.Memory = [s.page for i in range(block_num)]
        s.Memory_next = [s.page_next for i in range(block_num)]

        # read data path
        s.dout = Wire(num_bits)
        s.dout_next = Wire(num_bits)

        # adress
        s.col_addr   = Wire(clog2(col_num))
        s.page_addr  = Wire(clog2(page_num))
        s.block_addr = Wire(clog2(block_num))
        s.cntr       = Wire(2)


        @update
        def read_data_logic():
            s.dout_next @= s.Memory[s.block_addr][s.page_addr][s.col_addr] if (~s.ifc.CE & ~s.ifc.RE & ~s.ifc.CLE & s.ifc.WE & s.ifc.WP & ~s.ifc.ALE) else 0

        @update
        def write_addr_logic():
            if s.cntr == 2:
                s.col_addr   @= s.ifc.I[0:col_num-1] if (s.ifc.RE &
                        ~s.ifc.CE & s.ifc.ALE & ~s.ifc.CLE & s.ifc.WE & s.ifc.WP) else s.col_addr
            if s.cntr == 1:
                s.page_addr  @= s.ifc.I[0:page_num-1] if (s.ifc.RE &
                        ~s.ifc.CE & s.ifc.ALE & ~s.ifc.CLE & s.ifc.WE & s.ifc.WP) else s.page_addr
            if s.cntr == 0:
                s.block_addr @= s.ifc.I[0:block_num-1] if (s.ifc.RE &
                        ~s.ifc.CE & s.ifc.ALE & ~s.ifc.CLE & s.ifc.WE & s.ifc.WP) else s.block_addr
        @update_ff
        def addr_cnt_logic():
            if (s.ifc.RE & ~s.ifc.CE & s.ifc.ALE & ~s.ifc.CLE & s.ifc.WE & s.ifc.WP):
                s.cntr <<= s.cntr + 1
            if s.cntr == 3:
                s.cntr <<= 0

        @update
        def write_data_logic():
            for a in range(block_num):
                for b in range(page_num):
                    for c in range(col_num):
                        s.Memory_next[a][b][c] @= s.Memory[a][b][c]
            if (~s.ifc.CE & ~s.ifc.CLE) & (s.ifc.WE & ~s.ifc.ALE) & (s.ifc.RE & s.ifc.WP):
                s.Memory_next[s.block_addr][s.page_addr][s.col_addr] @= s.ifc.I

        @update
        def comb_logic():
            s.ifc.O @= s.dout if (~s.ifc.RE & ~s.ifc.CLE & ~s.ifc.ALE & ~s.ifc.CE & s.ifc.WE) else 0

        @update_ff
        def update_flash():
            s.dout <<= s.dout_next
            for a in range(block_num):
                for b in range(page_num):
                    for c in range(col_num):
                        s.Memory[a][b][c] <<= s.Memory_next[a][b][c]

        @update
        def Ready_or_Busy_logic():
            if s.ifc.RE & s.ifc.WE:
                s.ifc.ROB @= 0
            elif ~s.ifc.WP:
                s.ifc.ROB @= 0
            else:
                s.ifc.ROB @= 1

    def line_trace(s):
        return f"( I:{s.ifc.I} baddr:{s.block_addr} paddr:{s.page_addr} caddr:{s.col_addr} mem: [{s.Memory[s.block_addr][s.page_addr][s.col_addr]}]" \
               f"CE# = {s.ifc.CE} CLE={s.ifc.CLE} ALE={s.ifc.ALE} WE# = {s.ifc.WE}" \
               f"RE# ={s.ifc.RE} WP= {s.ifc.WP} ROB= {s.ifc.ROB} O:{s.ifc.O} dout:{s.dout} "










