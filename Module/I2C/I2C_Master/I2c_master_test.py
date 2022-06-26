#!/usr/bin/env python3

from pymtl3 import *
from pymtl3.stdlib.test_utils import config_model_with_cmdline_opts
from Module.I2C.I2C_Master.i2c_master import i2c_master
def test_basic( cmdline_opts ):

  # Create the model
  model = i2c_master()

  # Configure the model
  model = config_model_with_cmdline_opts( model, cmdline_opts, duts=[] )

  # Create and reset simulator
  model.apply( DefaultPassGroup(linetrace=True) )
  model.sim_reset()

  # Helper function
  def t( sda_in ):

    # Write input value to input port
    model.sda_in   @=  sda_in


    # Ensure that all combinational concurrent blocks are called
    model.sim_eval_combinational()

    # Tick simulator one cycle
    model.sim_tick()
  t(0b1)
  t(0b0)
  t(0b1)
  t(0b1)
  t(0b0)
  t(0b1)
  t(0b1)
  t(0b0)
  t(0b1)


