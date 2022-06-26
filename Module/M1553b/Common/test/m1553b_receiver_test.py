#!/usr/bin/env python3

from pymtl3 import *
from pymtl3.stdlib.test_utils import config_model_with_cmdline_opts
from Module.M1553b.Common.m1553b_receiver import m1553b_receiver
def test_basic( cmdline_opts ):

  # Create the model
  model = m1553b_receiver()

  # Configure the model
  model = config_model_with_cmdline_opts( model, cmdline_opts, duts=[] )

  # Create and reset simulator
  model.apply( DefaultPassGroup(linetrace=True) )
  model.sim_reset()

  # Helper function
  def t( idi):

    # Write input value to input port
    model.idi      @= idi
    # Ensure that all combinational concurrent blocks are called
    model.sim_eval_combinational()
    model.sim_tick()

  # idi
  # head
  t(0b00)
  t(0b01)
  t(0b11)
  #data
  t(0b01)
  t(0b10)
  t(0b10)
  t(0b10)
  t(0b01)
  t(0b10)
  t(0b10)
  t(0b10)
  t(0b01)
  t(0b10)
  t(0b10)
  t(0b10)
  t(0b01)
  t(0b10)
  t(0b10)
  t(0b10)
  t(0b10)
  t(0b10)
  t(0b10)







