from pymtl3 import *
from pymtl3.stdlib.test_utils import config_model_with_cmdline_opts
from Module.UART.Uart_submodule.UartRx import *

def test_basic( cmdline_opts ):

    # Create the model
    model = UartRxd()

    # Configure the model
    model = config_model_with_cmdline_opts(model, cmdline_opts, duts=[])

    # Create and reset simulator
    model.apply(DefaultPassGroup(linetrace=True))
    model.sim_reset()

    # Helper function
    def t(rxd):
        # Write input value to input port
        model.rxd @= rxd

        # Ensure that all combinational concurrent blocks are called
        model.sim_eval_combinational()

        # If reference output is not '?', verify value read from output port

        # Tick simulator one cycle
        model.sim_tick()
    # data:10110110
    # start bit: low active
    t(0b0)
    t(0b0)

    # data bit 1
    t(0b1)
    t(0b1)

    # data bit 2
    t(0b0)
    t(0b0)


    #data bit 3
    t(0b1)
    t(0b1)


    #data bit 4
    t(0b1)
    t(0b1)


    #data bit 5
    t(0b0)
    t(0b0)


    # data bit 6
    t(0b1)
    t(0b1)


    #data bit 7
    t(0b1)
    t(0b1)


    # data bit 8
    t(0b0)
    t(0b0)


    # stop bit: high active
    t(0b1)
    t(0b1)











