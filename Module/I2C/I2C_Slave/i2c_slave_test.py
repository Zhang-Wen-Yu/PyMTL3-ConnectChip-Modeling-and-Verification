#!/usr/bin/env python3
import sys
import os
curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)
from pymtl3 import *
from pymtl3.stdlib.test_utils import config_model_with_cmdline_opts
from Module.I2C.I2C_Slave.i2c_slave_warpper import i2c_slave
def test_basic( cmdline_opts ):
  # Create the model
  model = i2c_slave()
  # Configure the model
  model = config_model_with_cmdline_opts( model, cmdline_opts, duts=[] )
  # Create and reset simulator
  model.apply( DefaultPassGroup(linetrace=True) )
  model.sim_reset()
  # Helper function
  def t(sda_i,scl):
    # Write input value to input port
    model.SDA_i     @= sda_i
    model.SCL       @= scl

    # Ensure that all combinational concurrent blocks are called
    model.sim_eval_combinational()
    # If reference output is not '?', verify value read from output port
   # if miso != '?':
   #   assert model.o_SPI_MISO  == miso
   # if rx_dv != '?':
   #   assert model.RX.o_DV == rx_dv
   # if rx_byte != '?':
   #   assert model.RX.o_Byte == rx_byte
    # Tick simulator one cycle
    model.sim_tick()
  # sda_i scl
  t(0b1, 0b0 )
  t(0b1, 0b0 )
  t(0b1, 0b0 )



