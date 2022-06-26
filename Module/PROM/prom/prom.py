# ==================================
# PROM
# ==================================

from pymtl3 import *
from Module.PROM.Common.promIfc import *
from Module.PROM.Common.Synchronizer import *

class prom( Component ):

    def construct( s ):

        # prom interface
        s.prom_ifc = promIfc()

        # prom state
        s.mode = Wire(3)

        # mode
        s.idle     = 0
        s.op1      = 1
        s.op2      = 2
        s.serial   = 3
        s.Parallel = 4

        s.data_reg = Wire(8)
        s.data_in  = OutPort()


        s.instruction_reg = Wire(16)
        s.Tck_sync = Synchronizer()
        s.Tck_sync.in_ //= s.prom_ifc.TCK

        s.cntr = Wire(4)
        s.cntr_max = Wire(4)


        # state trans
        @update_ff
        def state_trans():
            if s.reset:
                s.mode <<= s.idle
            if s.mode == s.idle:
                if s.cntr >= s.cntr_max:
                    s.mode <<= s.op1
            if s.mode == s.op1:
                if s.cntr >= s.cntr_max:
                    s.mode <<= s.op2
            if s.mode == s.op2:
                if s.cntr >= s.cntr_max:
                    s.mode <<= s.serial
            if s.mode == s.Parallel:
                if s.cntr >= s.cntr_max:
                    s.mode <<= s.idle

        # Maximum Counter Value
        @update
        def max_counter_values():
            if s.mode == s.idle:
                s.cntr_max @= 2
            if s.mode == s.op1:
                s.cntr_max @= 16
            if s.mode == s.op2:
                s.cntr_max @= 16
            if s.mode == s.serial:
                s.cntr_max @= 8
            if s.mode == s.Parallel:
                s.cntr_max @= 1

        # data reg
        @update_ff
        def instr_reg_logic():
            if s.mode == s.op1:
                if s.Tck_sync.posedge_ == 1:
                    if s.cntr < s.cntr_max:
                        s.data_reg <<= concat(s.data_reg[0:7], s.prom_ifc.TDI)
                        s.cntr <<= s.cntr + 1

                    else:
                        s.cntr <<= 0
            if s.mode == s.op2:
                if s.Tck_sync.posedge_ == 1:
                    if s.cntr < s.cntr_max:
                        s.prom_ifc.TDO <<= s.data_reg[s.cntr]
                        s.cntr <<= s.cntr + 1

                    else:
                        s.cntr <<= 0


        # serial and parallel output logic
        @update_ff
        def serial_logic():
            if s.mode == s.serial:
                for i in range(8):
                    if s.prom_ifc.busy == 0:
                        if s.prom_ifc.CE1 == 0 & s.prom_ifc.OE1 == 1:
                            s.prom_ifc.data <<= concat(s.data_reg[i], 0b0000000)

            if s.mode == s.Parallel:
                if s.prom_ifc.busy == 0:   # when busy is down,can output
                    if s.prom_ifc.CE1 == 0 & s.prom_ifc.OE1 == 1:
                        s.prom_ifc.data <<= s.data_reg




    def line_trace(s):
        return f"D0:{s.prom_ifc.data}"




