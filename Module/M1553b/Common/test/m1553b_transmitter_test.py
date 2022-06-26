#!/usr/bin/env python3

from pymtl3 import *
from pymtl3.stdlib.test_utils import config_model_with_cmdline_opts
from Module.M1553b.Common.m1553b_transmitter import m1553b_transmitter
def test_basic( cmdline_opts ):

  # Create the model
  model = m1553b_transmitter()

  # Configure the model
  model = config_model_with_cmdline_opts( model, cmdline_opts, duts=[] )

  # Create and reset simulator
  model.apply( DefaultPassGroup(linetrace=True) )
  model.sim_reset()

  # Helper function
  def t( icd,ien,idata):

    # Write input value to input port
    model.icd      @= icd
    model.ien      @= ien
    model.idata    @= idata

    # Ensure that all combinational concurrent blocks are called
    model.sim_eval_combinational()

    model.sim_tick()
  # icd      ien      idata                     1   2  3  4  5  6  7  8  9  10 11 12 13 14 15 16
  t(0b1,     0b1,      0xffff) # (0 0 0 1 1 1)[10   10 10 10 10 10 10 10 10 10 10 10 10 10 10 10] (10) = 1eaaaaaaaaa
  t(0b0,     0b0,      0b0)
  t(0b0,     0b0,      0b0)
