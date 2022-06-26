# ===================================
# jtag_fpga model
# ===================================

from pymtl3 import *
from Module.JTAG.Common.jtag_ifc import *
from Module.JTAG.Common.Synchronizer import *


class jtag_fpga( Component ):

    def construct(s, register_size = 32, IR_size = 4):

        # Interface
        s.ifc = jtagIfc_fpga()

        # state
        s.state = Wire(4)

        # ====state define====
        s.TEST_LOGIC_RESET = 0  # test logic reset mode
        s.RUN_TEST_IDLE    = 1  # tap controller scan idle mode
        s.SELECT_DR_SCAN   = 2  # select data register scan mode
        s.CAPTURE_DR       = 3  # capture data register mode
        s.SHIFT_DR         = 4  # shift data register mode
        s.EXIT1_DR         = 5  # exit data register mode 1
        s.PAUSE_DR         = 6  # pause data register mode
        s.EXIT2_DR         = 7  # exit data register mode2
        s.UPDATE_DR        = 8  # update data register mode
        s.SELECT_IR_SCAN   = 9  # select instruction register scan mode
        s.CAPTURE_IR       = 10 # capture instruction register mode
        s.SHIFT_IR         = 11 # shift instruction register mode
        s.EXIT1_IR         = 12 # exit instruction register mode 1
        s.PAUSE_IR         = 13 # pause instruction register mode
        s.EXIT2_IR         = 14 # exit instruction register mode
        s.UPDATE_IR        = 15 # update instruction register mode

        # ======Input Mux======
        s.BYPASS = 0b0000
        s.IDCODE = 0b1000
        s.ADDR   = 0b0100
        s.WDATA  = 0b1100
        s.RDATA  = 0B0010

        # ====registers====
        s.IR = Wire(IR_size)
        s.IR_r = Wire(IR_size)

        @update_ff
        def state_trans():
              # TEST_LOGIC_RESET
              if s.state == s.TEST_LOGIC_RESET:
                if s.ifc.TMS:
                    s.state <<= s.TEST_LOGIC_RESET
                else:
                    s.state <<= s.RUN_TEST_IDLE
              # RUN_TEST_IDLE
              if s.state == s.RUN_TEST_IDLE:
                if s.ifc.TMS:
                    s.state <<= s.SELECT_DR_SCAN
                else:
                    s.state <<= s.RUN_TEST_IDLE
              # SELECT_DR_SCAN
              if s.state == s.SELECT_DR_SCAN:
                if s.ifc.TMS:
                    s.state <<= s.SELECT_IR_SCAN
                else:
                    s.state <<= s.CAPTURE_DR
              # CAPRURE_DR
              if s.state == s.CAPTURE_DR:
                if s.ifc.TMS:
                    s.state <<= s.EXIT1_DR
                else:
                    s.state <<= s.SHIFT_DR
              # SHIFT_DR
              if s.state == s.SHIFT_DR:
                if s.ifc.TMS:
                    s.state <<= s.EXIT1_DR
                else:
                    s.state <<= s.SHIFT_DR
              # EXIT1_DR
              if s.state == s.EXIT1_DR:
                if s.ifc.TMS:
                    s.state <<= s.UPDATE_DR
                else:
                    s.state <<= s.PAUSE_DR
              # PAUSE_DR
              if s.state == s.PAUSE_DR:
                if s.ifc.TMS:
                    s.state <<= s.EXIT2_DR
                else:
                    s.state <<= s.PAUSE_DR
              # EXIT2_DR
              if s.state == s.EXIT2_DR:
                if s.ifc.TMS:
                    s.state <<= s.UPDATE_DR
                else:
                    s.state <<= s.SHIFT_DR
              # UPDATE_DR
              if s.state == s.UPDATE_DR:
                if s.ifc.TMS:
                    s.state <<= s.SELECT_DR_SCAN
                else:
                    s.state <<= s.RUN_TEST_IDLE
              # SELECT_IR_SCAN
              if s.state == s.SELECT_IR_SCAN:
                if s.ifc.TMS:
                    s.state <<= s.TEST_LOGIC_RESET
                else:
                    s.state <<= s.CAPTURE_IR
              # CAPTURE_IR
              if s.state == s.CAPTURE_IR:
                if s.ifc.TMS:
                    s.state <<= s.EXIT1_IR
                else:
                    s.state <<= s.SHIFT_IR
              # SHIFT_IR
              if s.state == s.SHIFT_IR:
                if s.ifc.TMS:
                    s.state <<= s.EXIT1_IR
                else:
                    s.state <<= s.SHIFT_IR
              # EXIT1_DR
              if s.state == s.EXIT1_IR:
                if s.ifc.TMS:
                    s.state <<= s.UPDATE_IR
                else:
                    s.state <<= s.PAUSE_IR
              # PAUSE_IR
              if s.state == s.PAUSE_IR:
                if s.ifc.TMS:
                    s.state <<= s.EXIT2_IR
                else:
                    s.state <<= s.PAUSE_IR
              # EXIT2_IR
              if s.state == s.EXIT2_IR:
                if s.ifc.TMS:
                    s.state <<= s.UPDATE_IR
                else:
                    s.state <<= s.SHIFT_IR
              # UPDATE_IR
              if s.state == s.UPDATE_IR:
                if s.ifc.TMS:
                    s.state <<= s.SELECT_DR_SCAN
                else:
                    s.state <<= s.RUN_TEST_IDLE

        s.instruction_tdo = Wire()
        s.instruction_tdo //= s.IR[0]

        @update
        def IR_register_logic():
            if s.state == s.TEST_LOGIC_RESET:
                s.IR @= 0
            if s.state == s.CAPTURE_IR:
                s.IR @= 0
            if s.state == s.SHIFT_IR:
                s.IR @= concat(s.IR[0:3],s.ifc.TDI)


        # updating IR
        @update
        def IR_update_logic():
            if s.state == s.TEST_LOGIC_RESET:
                s.IR_r @= 0
            if s.state == s.UPDATE_IR:
                s.IR_r @= s.IR

        # =================================
        # BYPASS register
        # =================================
        s.bypass_tdo = Wire()
        s.bypass_reg = Wire()
        s.bypass_tdo //= s.bypass_reg


        @update_ff
        def BYPASS_logic():
            if s.state == s.TEST_LOGIC_RESET:
                s.bypass_reg <<= 0
            if s.state == s.CAPTURE_DR & s.IR_r == s.BYPASS:
                s.bypass_reg <<= 0
            if s.state == s.SHIFT_DR & s.IR_r == s.BYPASS:
                s.bypass_reg <<= s.ifc.TDI

        # =================================
        # ID Code register
        # =================================
        s.DR_IDCODE = Wire(register_size)
        s.idcode_tdo = Wire()
        s.idcode_tdo //= s.DR_IDCODE[0]

        @update_ff
        def IDCODE_logic():
                if s.state == s.TEST_LOGIC_RESET:
                    s.DR_IDCODE <<= 0xf0f0f0f0
                if (s.state == s.CAPTURE_DR) & (s.IR_r == s.IDCODE):
                    s.DR_IDCODE <<= 0Xf0f0f0f0
                if (s.state == s.SHIFT_DR) & (s.IR_r == s.IDCODE):
                    # [1:8] means highest bit can be use,and lowest bit can not be use
                    s.DR_IDCODE <<= concat(s.ifc.TDI, s.DR_IDCODE[1:8])


        # =================================
        # ADDR register
        # =================================
        s.DR_ADDR = Wire(register_size)
        s.addr_tdo = Wire()
        s.addr_tdo //= s.DR_ADDR[0]

        @update_ff
        def ADDR_logic():
                if s.state == s.TEST_LOGIC_RESET:
                    s.DR_ADDR <<= 0
                if (s.state == s.SHIFT_DR) & (s.IR_r == s.ADDR):

                    s.DR_ADDR <<= concat(s.ifc.TDI, s.DR_ADDR[1:8])

        # ====================================
        # READ DATA register
        # ====================================
        s.DR_RDATA = Wire(register_size)
        s.rdata_tdo = Wire()

        s.rdata_tdo //= s.DR_RDATA[0]

        @update_ff
        def RDATA_logic():
                if s.state == s.TEST_LOGIC_RESET:
                    s.DR_RDATA <<= 0
                if (s.state == s.UPDATE_DR) & (s.IR_r == s.RDATA):
                    s.DR_RDATA <<= concat(s.ifc.TDI, s.DR_RDATA[1:8])

        # ===========================
        # WRITE register
        # ===========================
        s.DR_WDATA = Wire(register_size)
        s.wdata_tdo = Wire()
        s.wdata_tdo //= s.DR_WDATA[0]

        @update_ff
        def WDATA_logic():
                if s.state == s.TEST_LOGIC_RESET:
                    s.DR_WDATA <<= 0
                if (s.IR_r == s.WDATA) & (s.state == s.CAPTURE_DR):
                   s.DR_WDATA <<= 0
                if (s.IR_r == s.WDATA) & (s.state == s.SHIFT_DR):
                   s.DR_WDATA <<= concat(s.DR_WDATA[0:31], s.ifc.TDI)

        @update_ff
        # tdo  output select
        def tdo_logic():
            if s.state == s.TEST_LOGIC_RESET:
                s.ifc.TDO <<= 0
            else:
                if s.IR_r == s.RDATA:
                    s.ifc.TDO <<= s.rdata_tdo
                elif s.IR_r == s.WDATA:
                    s.ifc.TDO <<= s.wdata_tdo
                elif s.IR_r == s.IDCODE:
                    s.ifc.TDO <<= s.IDCODE
                elif s.IR_r == s.ADDR:
                    s.ifc.TDO <<= s.addr_tdo
                else:
                    s.ifc.TDO <<= s.bypass_tdo

    def line_trace(s):
        return f"state:{s.state} IR:{s.IR} IR_r:{s.IR_r} tdi: {s.ifc.TDI}, tdo: {s.ifc.TDO} ," \
               f" tms: {s.ifc.TMS} , tck: {s.ifc.TCK} "











