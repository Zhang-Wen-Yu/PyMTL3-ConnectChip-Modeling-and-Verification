#!/usr/bin/env python3
import sys
import os
curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)
from pymtl3 import *
from pymtl3.stdlib.test_utils import config_model_with_cmdline_opts
from Module.SPI.SPISlave.SpiSlaveWarpped import Spi_Slave_Warpped
def test_basic( cmdline_opts ):
  # Create the model
  model = Spi_Slave_Warpped()
  # Configure the model
  model = config_model_with_cmdline_opts( model, cmdline_opts, duts=[] )
  # Create and reset simulator
  model.apply( DefaultPassGroup(linetrace=True) )
  model.slave_inter.cs          @= 1
  model.slave_inter.sclk        @= 0
  model.slave_inter.mosi        @= 0
  model.pull.msg    @= 0
  model.sim_reset()
  # Helper function
  def t(cs_n,sclk,mosi,miso,pull_msg):
    # Write input value to input port
    model.slave_inter.cs     @= cs_n
    model.slave_inter.mosi     @= mosi
    model.slave_inter.sclk      @= sclk
    model.pull.msg @= pull_msg
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
  # cs_n,  sclk,   ,mosi,    miso,     pull_msg)
  t(0b1,    0b0,    0b0,      0b0,      0b0 )
  t(0b0,    0b0,    0b0,      0b0,      0b0 )
  t(0b0,    0b1,    0b1,      0b0,      0xaa )
  t(0b0,    0b0,    0b1,      0b0,      0b0 )      # sclk negedge 1
  t(0b0,    0b1,    0b1,      0b0,      0b0 )
  t(0b0,    0b0,    0b1,      0b1,      0b0 )      # sclk negedge 2
  t(0b0,    0b1,    0b1,      0b1,      0b0 )
  t(0b0,    0b0,    0b1,      0b0,      0b0 )      # sclk negegde 3
  t(0b0,    0b1,    0b1,      0b0,      0b0 )
  t(0b0,    0b0,    0b0,      0b1,      0b0 )      # sclk negedge 4
  t(0b0,    0b1,    0b1,      0b1,      0b0 )
  t(0b0,    0b0,    0b0,      0b0,      0b0 )      # sclk negedge 5
  t(0b0,    0b1,    0b1,      0b0,      0b0 )
  t(0b0,    0b0,    0b0,      0b1,      0b0 )      # sclk negedge 6
  t(0b0,    0b1,    0b1,      0b1,      0b0 )
  t(0b0,    0b0,    0b0,      0b0,      0b0 )      # sclk negedge 7
  t(0b0,    0b1,    0b1,      0b0,      0b0 )
  t(0b0,    0b0,    0b0,      0b1,      0b0 )      # sclk negedge 8
  t(0b0,    0b0,    0b0,      0b1,      0b0 )
  t(0b0,    0b0,    0b0,      0b0,      0b0 )



