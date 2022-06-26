# ================================================
# Uart_submodule Transmitter
# ================================================

from pymtl3 import *
from Module.UART.Common.UARTIfc import *

class UartTxd( Component ):

    def construct(s, pack_size = 8, bit_rate = 100, clk_freq = 100, msg=100):

        s.txd = OutPort(1)

        # tx_trig set 1 for 1 cycle to trigger a transmission
        # tx_busy set 1 when transmitting
        # tx_done set 1 for 1 cycle when all bits are transmitted
        # preload datad to transmit

        s.preload_data = InPort(mk_bits(pack_size))
        s.din = Wire(mk_bits(pack_size))

        s.tx_busy = Wire(1)
        s.tx_done = Wire(1)

        s.clks_per_bit = (clk_freq / bit_rate)      # clks per bit
        s.clk_cntr_bw  = clog2(s.clks_per_bit) + 1   # bit width for clk counter
        s.bit_cntr_bw  = clog2(pack_size) + 1        # bit width for bit counter

        # FSM states
        s.idle      = 0
        s.start_bit = 1
        s.data_bits = 2
        s.stop_bit  = 3

        s.clk_cntr = Wire(s.clk_cntr_bw)  # counting clk edges
        s.bit_cntr = Wire(s.bit_cntr_bw) # counting bits transmitted

        s.start_bit_init = OutPort(1)
        s.data_bit_init = Wire(1)
        s.stop_bit_init = Wire(1)
        s.stop_bit_end = OutPort(1)

        s.state = OutPort(2)
        s.next_state = Wire(2)

        @update
        def next_state_logic():
            s.next_state @= s.idle

            # trigger signal set 1,start a transmission
            if s.state == s.idle:
                s.next_state @= s.start_bit

            # transmit the first data bit, go to data_bits
            if s.state == s.start_bit:
                if s.data_bit_init == 1:
                    s.next_state @= s.data_bits
                else:
                    s.next_state @= s.start_bit

            # transmit the stop data bit, go to stop_bit
            if s.state == s.data_bits:
                if s.stop_bit_init == 1:
                    s.next_state @= s.stop_bit
                else:
                    s.next_state @= s.data_bits

            # stop bit transmitted, go back to idle
            if s.state == s.stop_bit:
                if s.stop_bit_end == 1:
                    s.next_state @= s.idle
                else:
                    s.next_state @= s.stop_bit

        @update
        def output_logic():
            s.start_bit_init @= 0
            s.data_bit_init @= 0
            s.stop_bit_init @= 0
            s.stop_bit_end @= 0
            s.tx_busy @= 1

            # transmit start bit when trigger signal set 1
            if s.state == s.idle:
                s.start_bit_init @= 1
                s.tx_busy @= 0

            # start bit lasts for 1 clks_per_bit
            if s.state == s.start_bit:
                s.data_bit_init @= (s.clk_cntr == s.clks_per_bit)

            if s.state == s.data_bits:
                if s.bit_cntr < pack_size:
                    s.data_bit_init @= (s.clk_cntr == s.clks_per_bit)

                else:
                    # all data bits transmitted , transmit stop bit
                    s.stop_bit_init @= (s.clk_cntr == s.clks_per_bit)

            # stop bit lasts for 1 clks_per_bit
            if s.state == s.stop_bit:
                s.stop_bit_end @= (s.clk_cntr == s.clks_per_bit)

        @update_ff
        def fsm_stations():
            if s.reset:
                s.state <<= s.idle
            else:
                s.state <<= s.next_state

        s.data_reg = Wire(pack_size)

        @update_ff
        def data_reg_pre():
            if s.reset:
                s.data_reg <<= 0
            if s.start_bit_init == 1:
                s.data_reg <<= s.preload_data

        # update data bit when necessary
        @update_ff
        def update_data():
            if s.reset:
                s.txd <<= 1
            else:
                if s.start_bit_init == 1:  # start bit
                    s.txd <<= 0

                if s.data_bit_init == 1:  # data bit
                    s.txd <<= s.data_reg[s.bit_cntr]

                if s.stop_bit_init == 1:  # stop bit
                    s.txd <<= 1

        # clk_cntr and bit_cntr control
        @update_ff
        def cntr_logic():
            if s.reset:
                s.clk_cntr <<= 0
                s.bit_cntr <<= 0
            else:
                if s.state == s.idle:
                    s.clk_cntr <<= 0
                    s.bit_cntr <<= 0

                # clk cntr counting from 0 to clks_per_bit
                if s.state == s.start_bit:
                    if s.clk_cntr < s.clks_per_bit:
                        s.clk_cntr <<= s.clk_cntr + 1
                    else:
                        s.clk_cntr <<= 0
                    # at the head of the first data bit ,bit_cntr adds 1
                    if s.data_bit_init == 1:
                        s.bit_cntr <<= s.bit_cntr + 1

                    # clk_cntr counting from 0 to clks_per_bit
                if s.state == s.data_bits:
                    if s.clk_cntr < s.clks_per_bit:
                        s.clk_cntr <<= s.clk_cntr + 1
                    else:
                        s.clk_cntr <<= 0
                    # at the head of each data bit ,bit_cntr adds 1
                    if s.data_bit_init == 1:
                        s.bit_cntr <<= s.bit_cntr + 1
                    elif s.stop_bit_init == 1:
                        s.bit_cntr <<= 0    # reset bit cntr when at the head of stop bit

                    # clk_cntr counting from 0 to clks_per_bit
                if s.state == s.stop_bit:
                    if s.clk_cntr < s.clks_per_bit:
                        s.clk_cntr <<= s.clk_cntr + 1
                    else:
                        s.clk_cntr <<= 0

        @update_ff
        def done_logic():
            if s.reset:
                s.tx_done <<= 0
            else:
                s.tx_done <<= s.stop_bit_end # tx done at the tail of stop bit
    def line_trace(s):
        return f" reg: {s.data_reg } state: { s.state } txd: [{s.txd}] data:{s.data_reg}" \
               f"  start_bit_init:{s.start_bit_init} " \
               f"data_bit_init:{s.data_bit_init} stop_bit_init:{s.stop_bit_init} stop_bit_end: {s.stop_bit_end}"











        

