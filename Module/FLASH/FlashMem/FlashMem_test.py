from pymtl3 import *
from pymtl3.stdlib.test_utils import config_model_with_cmdline_opts
from Module.FLASH.FlashMem.FlashMem import FlashMem

def test_basic( cmdline_opts ):

  # Create the model
  model = FlashMem()

  # Configure the model
  model = config_model_with_cmdline_opts( model, cmdline_opts, duts=[] )

  # Create and reset simulator
  model.apply( DefaultPassGroup(linetrace=True) )
  model.sim_reset()

  # Helper function
  def t( I, RE, CE,  CLE, ALE, WE, WP):

    # Write input value to input port
    model.ifc.I     @= I
    model.ifc.RE    @= RE
    model.ifc.CE    @= CE
    model.ifc.CLE   @= CLE
    model.ifc.ALE   @= ALE
    model.ifc.WE    @= WE
    model.ifc.WP    @= WP
    # Ensure that all combinational concurrent blocks are called
    model.sim_eval_combinational()

    #  Port Name          Direction      Description
    #  -----------------------------------------------------------------------
    #  s.I(0~7)              I           Ins,  transferring address, command, and data to the device
    #  s.O(0~7)              O           Outs, transferring address, command, and data from the device
    #  s.ROB                 O           Ready/Busy(Ready = 1,Busy = 0)
    #  s.RE                  I           Read Enable(enable = 0)
    #  s.CE                  I           Chip Enable(enable = 0)
    #  s.CLE                 I           Command Latch Enable
    #  s.ALE                 I           Address Latch Enable
    #  s.WE                  I           Write Enable(rising edge)
    #  s.WP                  I           Write Protect(enable = 0)

    # Tick simulator one cycle
    model.sim_tick()

  #  I,   RE,  CE,   CLE,   ALE,  WE,   WP
  t(0b0,  0b0, 0b1,  0b0,   0b0,  0b0, 0b1)
  t(0b0,  0b0, 0b1,  0b0,   0b0,  0b0, 0b1)
  t(0xff, 0b1, 0b0,  0b0,   0b1,  0b1, 0b1)  #
  t(0xff, 0b1, 0b0,  0b0,   0b1,  0b1, 0b1)  #
  t(0xff, 0b1, 0b0,  0b0,   0b1,  0b1, 0b1)  #
  t(0xff, 0b1, 0b0,  0b0,   0b0,  0b1, 0b1)
  t(0xff, 0b1, 0b0,  0b0,   0b0,  0b1, 0b1)
  t(0xff, 0b0, 0b0,  0b0,   0b0,  0b1, 0b1)
  t(0xff, 0b0, 0b0,  0b0,   0b0,  0b1, 0b1)





