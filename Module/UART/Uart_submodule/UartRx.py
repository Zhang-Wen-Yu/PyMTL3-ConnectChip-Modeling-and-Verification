# =============================================
# Uart_submodule Receiver
# =============================================

from pymtl3 import *
from Module.UART.Common.UARTIfc import *

class UartRxd( Component ):

    def construct(s, pack_size = 8, bit_rate = 100, clk_freq = 100 ):

        # interface
        s.rxd = InPort(1)  # input serial data
        s.serial_data = Wire(1)
        s.rx_done   = Wire(1)    # when all bits received rx_done set1 for 1 cycle
        s.recv_data = OutPort(mk_bits(pack_size))    # received data

        s.clks_per_bit = (clk_freq / bit_rate)      # clks per bit
        s.clk_cntr_bw  = clog2(s.clks_per_bit) + 1   # bit width for clk counter
        s.bit_cntr_bw  = clog2(pack_size) + 1        # bit width for bit counter

        # FSM states
        s.idle      = 0
        s.start_bit = 1
        s.data_bits = 2
        s.stop_bit  = 3

        s.clk_cntr = Wire(mk_bits(s.clk_cntr_bw))  # counting clk edges
        s.bit_cntr = Wire(mk_bits(s.bit_cntr_bw))  # counting bits transmitted

        s.start_bit_mid = Wire(1)
        s.data_bit_mid  = Wire(1)
        s.stop_bit_mid  = OutPort(1)

        s.state = OutPort(2)
        s.next_state = Wire(2)

        @update
        def next_state_logic():
            s.next_state @= s.idle
            if s.state == s.idle:
                s.next_state @= s.start_bit
            if s.state == s.start_bit:
                if s.start_bit_mid == 1:
                    # check if serial data is still 0,if not,treat as noise and return to idle
                    if s.rxd == 0:
                        s.next_state @= s.data_bits
                    else:
                        s.next_state @= s.idle
                else:
                    s.next_state @= s.start_bit
            if s.state == s.data_bits:
                if s.bit_cntr == pack_size:
                    s.next_state @= s.stop_bit # all bits are transmitted, go to stop bit
                else:
                    s.next_state @= s.data_bits
            if s.state == s.stop_bit:
                if s.stop_bit_mid == 1:
                    s.next_state @= s.idle  # at the middle of stop bit,transmission completed
                else:
                    s.next_state @= s.stop_bit

        @update
        def output_logic():
            s.start_bit_mid @= 0
            s.data_bit_mid @= 0
            s.stop_bit_mid @= 0
            if s.state == s.start_bit:
                s.start_bit_mid @= (s.clk_cntr == s.clks_per_bit / 2)
            if s.state == s.data_bits:
                s.data_bit_mid @= (s.clk_cntr == s.clks_per_bit)
            if s.state == s.stop_bit:
                s.stop_bit_mid @= (s.clk_cntr == s.clks_per_bit)

        @update_ff
        def fsm_stations():
            if s.reset:
                s.state <<= s.idle
            else:
                s.state <<= s.next_state

        # grab data bit when in middle of data bit
        @update_ff
        def grab_data_mid():
            if s.reset:
                s.recv_data <<= 0
            if s.data_bit_mid == 1:
                s.recv_data <<= concat(s.recv_data[0:pack_size-1], s.rxd)
            if s.stop_bit_mid == 1:
                s.recv_data <<= 0


        # control clk_cntr and bit cntr
        @update_ff
        def cntr_logic():
            if s.reset:
                s.clk_cntr <<= 0
                s.bit_cntr <<= 0
            else:
                if s.state == s.idle:
                    # disable counters when in idle
                    s.clk_cntr <<= 0
                    s.bit_cntr <<= 0
                # clk_cntr counting from 0 to clks_per_bit/2
                if s.state == s.start_bit:
                    if s.clk_cntr < (s.clks_per_bit/2):
                        s.clk_cntr <<= s.clk_cntr + 1
                    else:
                        s.clk_cntr <<= 0
                if s.state == s.data_bits:
                    # clk_cntr counting from 0 to clks_per_bit
                    if s.clk_cntr < s.clks_per_bit:
                        s.clk_cntr <<= s.clk_cntr + 1
                    else:
                        s.clk_cntr <<= 0
                    # at the middle of each data bit,bit_cntr adds 1,until pack_size
                    if s.data_bit_mid == 1:
                        if s.bit_cntr < pack_size:
                            s.bit_cntr <<= s.bit_cntr + 1
                        else:
                            s.bit_cntr <<= 0
                # clk_cntr counting from 0 to clks_per_bit
                if s.state == s.stop_bit:
                    if s.clk_cntr < s.clks_per_bit:
                        s.clk_cntr <<= s.clk_cntr + 1
                    else:
                        s.clk_cntr <<= 0

        # when at the middle of stop bit, rx done
        @update_ff
        def rx_done_logic():
            if s.reset:
                s.rx_done <<= 0
            else:
                s.rx_done <<= s.stop_bit_mid

    def line_trace(s):
        return f" state: { s.state } rxd: [{s.rxd}] rx_done: [{s.rx_done}], recv_data: [{s.recv_data} ]" \
               f" clk_cntr: {s.clk_cntr } bit_cntr: {s.bit_cntr} start_bit_mid:{s.start_bit_mid} data_bit_mid:{s.data_bit_mid} stop_bit_mid:{s.stop_bit_mid}"




















