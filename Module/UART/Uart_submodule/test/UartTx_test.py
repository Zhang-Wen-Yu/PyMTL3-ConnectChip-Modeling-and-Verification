from pymtl3 import *
from pymtl3.stdlib.test_utils import config_model_with_cmdline_opts
from Module.UART.Uart_submodule.UartTx import *

def test_basic( cmdline_opts ):

    # Create the model
    model = UartTxd()

    # Configure the model
    model = config_model_with_cmdline_opts(model, cmdline_opts, duts=[])

    # Create and reset simulator
    model.apply(DefaultPassGroup(linetrace=True))
    model.sim_reset()

    # Helper function
    def t(trig, pre_data):

        # Write input value to input port
        model.tx_trig           @= trig
        model.preload_data      @= pre_data

        # Ensure that all combinational concurrent blocks are called
        model.sim_eval_combinational()

        # If reference output is not '?', verify value read from output port

        # Tick simulator one cycle
        model.sim_tick()
    # data:0 11101110 1
    t(0b1,0xee)

    t(0b0,0x00)
    t(0b0,0x00)
    t(0b0,0x00)
    t(0b0,0x00)
    t(0b0,0x00)
    t(0b0,0x00)
    t(0b0,0x00)
    t(0b0,0x00)
    t(0b0,0x00)
    t(0b0,0x00)
    t(0b0,0x00)
    t(0b0,0x00)
    t(0b0,0x00)
    t(0b0,0x00)
    t(0b0,0x00)
    t(0b0,0x00)
    t(0b0,0x00)
    t(0b0,0x00)

    t(0b0,0x00)




