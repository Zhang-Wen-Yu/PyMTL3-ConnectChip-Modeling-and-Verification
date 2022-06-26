#!/usr/bin/env python3

from pymtl3 import *
from pymtl3.stdlib.test_utils import config_model_with_cmdline_opts
from Module.SPI.SPIMaster.SpiMasterWarpped import Spi_Master_Warpped
def test_basic( cmdline_opts ):

  # Create the model
  model = Spi_Master_Warpped()

  # Configure the model
  model = config_model_with_cmdline_opts( model, cmdline_opts, duts=[] )

  # Create and reset simulator
  model.apply( DefaultPassGroup(linetrace=True) )
  model.sim_reset()

  # Helper function
  def t( cs_n, MISO, MOSI, sclk, recv_val, recv_msg, recv_rdy, req_val, req_msg ,req_rdy):

    # Write input value to input port
    model.master_infer.miso   @= MISO
    model.req.msg      @= recv_msg
    model.req.val    @= recv_val
    model.resp.rdy @= req_rdy

    # Ensure that all combinational concurrent blocks are called
    model.sim_eval_combinational()

    # If reference output is not '?', verify value read from output port
  #  if MOSI != '?':
  #    assert model.o_SPI_MOSI == MOSI
  #  if sclk != '?':
  #    assert model.o_SPI_Clk  == sclk
  #  if tx_ready != '?':
  #    assert model.o_TX_Ready == tx_ready
  #  if cs_n != '?':
  #    assert model.o_SPI_CS_n == cs_n
  #  if rx_dv != '?':
  #    assert model.RX.o_DV == rx_dv
  #  if rx_byte != '?':
  #    assert model.RX.o_Byte == rx_byte
    # Tick simulator one cycle
    model.sim_tick()
  # cs_n ,   MISO,     MOSI,     sclk,    recv_val,  recv_msg,  recv_rdy,  req_val,  req_msg  , req_rdy
  t(0b1,     0b0,      0b0,      0b0,       0b0,      0b0,       0b1,       0b0,     0b0,        0b0)
  t(0b1,     0b0,      0b0,      0b0,       0b1,      0xAA,      0b0,       0b0,     0b0,        0b1)
  t(0b0,     0b0,      0b0,      0b0,       0b0,      0b0,       0b0,       0b0,     0b0,        0b0)
  t(0b0,     0b1,      0b1,      0b1,       0b0,      0b0,       0b0,       0b0,     0b0,        0b0)
  t(0b0,     0b0,      0b1,      0b0,       0b0,      0b0,       0b0,       0b0,     0x01,        0b0) # sclk posedge  1
  t(0b0,     0b1,      0b0,      0b1,       0b0,      0b0,       0b0,       0b0,     0x01,        0b0)
  t(0b0,     0b0,      0b0,      0b0,       0b0,      0b0,       0b0,       0b0,     0x03,        0b0) # sclk posedage 2
  t(0b0,     0b1,      0b1,      0b1,       0b0,      0b0,       0b0,       0b0,     0x03,        0b0)
  t(0b0,     0b0,      0b1,      0b0,       0b0,      0b0,       0b0,       0b0,     0x07,        0b0) # sclk posedage 3
  t(0b0,     0b1,      0b0,      0b1,       0b0,      0b0,       0b0,       0b0,     0x07,        0b0)
  t(0b0,     0b0,      0b0,      0b0,       0b0,      0b1,       0b0,       0b0,     0x0f,        0b0) # sclk posedage 4
  t(0b0,     0b1,      0b1,      0b1,       0b0,      0b0,       0b0,       0b0,     0x0f,        0b0)
  t(0b0,     0b0,      0b1,      0b0,       0b0,      0b1,       0b0,       0b0,     0x1f,        0b0) # sclk posedage 5
  t(0b0,     0b1,      0b0,      0b1,       0b0,      0b0,       0b0,       0b0,     0x1f,        0b0)
  t(0b0,     0b0,      0b0,      0b0,       0b0,      0b1,       0b0,       0b0,     0x3f,        0b0) # sclk posedage 6
  t(0b0,     0b1,      0b1,      0b1,       0b0,      0b0,       0b0,       0b0,     0x3f,        0b0)
  t(0b0,     0b0,      0b1,      0b0,       0b0,      0b1,       0b0,       0b0,     0x7f,        0b0) # sclk posedage 7
  t(0b0,     0b0,      0b0,      0b1,       0b0,      0b0,       0b0,       0b0,     0x7f,        0b0)
  t(0b0,     0b0,      0b0,      0b0,       0b0,      0b1,       0b0,       0b1,     0xfe,        0b0) # sclk posedage 8   recv successful
  t(0b0,     0b0,      0b1,      0b0,       0b0,      0b0,       0b1,       0b0,     0xfe,        0b0)
  t(0b0,     0b0,      0b1,      0b0,       0b1,      0x01,      0b0,       0b0,     0xfe,        0b0)
  t(0b0,     0b0,      0b1,      0b0,       0b0,      0b0,       0b0,       0b0,     0xfe,        0b0)
  t(0b0,     0b0,      0b0,      0b1,       0b0,      0b0,       0b0,       0b0,     0xfe,        0b0)
  t(0b0,     0b1,      0b0,      0b0,       0b0,      0b0,       0b0,       0b0,     0xfc,        0b0)  #sclk posedge 1
  t(0b0,     0b0,      0b0,      0b1,       0b0,      0b0,       0b0,       0b0,     0xfc,        0b0)
  t(0b0,     0b1,      0b0,      0b0,       0b0,      0b0,       0b0,       0b0,     0xf8,        0b0)  #sclk posedge 2
  t(0b0,     0b0,      0b0,      0b1,       0b0,      0b0,       0b0,       0b0,     0xf8,        0b0)
  t(0b0,     0b1,      0b0,      0b0,       0b0,      0b0,       0b0,       0b0,     0xf0,        0b0)  #sclk posedge 3
  t(0b0,     0b1,      0b0,      0b1,       0b0,      0b0,       0b0,       0b0,     0xf0,        0b0)
  t(0b0,     0b1,      0b0,      0b0,       0b0,      0b0,       0b0,       0b0,     0xe1,        0b0)  #sclk posedge 4
  t(0b0,     0b1,      0b0,      0b1,       0b0,      0b0,       0b0,       0b0,     0xe1,        0b0)
  t(0b0,     0b0,      0b0,      0b0,       0b0,      0b0,       0b0,       0b0,     0xc3,        0b0)  #sclk posedge 5
  t(0b0,     0b0,      0b0,      0b1,       0b0,      0b0,       0b0,       0b0,     0xc3,        0b0)
  t(0b0,     0b0,      0b0,      0b0,       0b0,      0b0,       0b0,       0b0,     0x86,        0b0)  #sclk posedge 6
  t(0b0,     0b0,      0b0,      0b1,       0b0,      0b0,       0b0,       0b0,     0x86,        0b0)
  t(0b0,     0b0,      0b0,      0b0,       0b0,      0b0,       0b0,       0b0,     0x0c,        0b0)  #sclk posedge 7
  t(0b0,     0b0,      0b1,      0b1,       0b0,      0b0,       0b0,       0b0,     0x0c,        0b0)
  t(0b0,     0b1,      0b1,      0b0,       0b0,      0b0,       0b0,       0b1,     0x18,        0b0)  #sclk posedge 8  recv successful
  t(0b0,     0b0,      0b0,      0b0,       0b0,      0b0,       0b0,       0b0,     0x18,        0b0)
  t(0b1,     0b0,      0b0,      0b0,       0b0,      0b0,       0b0,       0b0,     0x18,        0b0)
  t(0b1,     0b0,      0b0,      0b0,       0b0,      0b0,       0b0,       0b0,     0x18,        0b0)
  t(0b1,     0b0,      0b0,      0b0,       0b0,      0b0,       0b1,       0b0,     0x18,        0b0)
  t(0b1,     0b0,      0b0,      0b0,       0b0,      0b0,       0b1,       0b0,     0x18,        0b0)
  t(0b1,     0b0,      0b0,      0b0,       0b0,      0b0,       0b1,       0b0,     0x18,        0b0)

