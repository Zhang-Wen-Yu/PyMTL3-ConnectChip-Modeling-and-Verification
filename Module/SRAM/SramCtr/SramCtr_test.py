from pymtl3 import *
from pymtl3.stdlib.test_utils import config_model_with_cmdline_opts
from Module.SRAM.SramCtr.SramCtr import SdramContr
def test_basic( cmdline_opts ):

  # Create the model
  model = SdramContr()

  # Configure the model
  model = config_model_with_cmdline_opts( model, cmdline_opts, duts=[] )

  # Create and reset simulator
  model.apply( DefaultPassGroup(linetrace=True) )
  model.sim_reset()

  # Helper function
  def t( recv_msg, recv_val, send_rdy, O1):

    # Write input value to input port
    model.req.msg         @= recv_msg
    model.req.val         @= recv_val
    model.resp.rdy        @= send_rdy
    model.sdramctr_inter.O1    @= O1

    # Ensure that all combinational concurrent blocks are called
    model.sim_eval_combinational()

    # If reference output is not '?', verify value read from output port

    # Tick simulator one cycle
    model.sim_tick()

    #  Port Name          Direction        Description
    #  -----------------------------------------------------------------------
    #  s.sram_inter.CS1      I           sram select (1 = enabled)
    #  s.sram_inter.WE1      I           transaction type(write enable), 0 = read, 1 = write
    #  s.sram_inter.OE1      I           if nor not output the read data, 0 = output, 1 = not output
    #  s.sram_inter.CE1      I           sram clk in
    #  s.sram_inter.A1       I           sram address
    #  s.sram_inter.I1       I           write data input
    #  s.sram_inter.O1       O           read data output
    #  s.sram_inter.WBM1     I           write bit enable (1 = enabled)


  #   req_msg,         req_val,  resp_rdy,     O1
  t(0x1_0f000000_04,      0b1,     0b1,    0x00000000)
  t(0x0_00000000_00,      0b0,     0b1,    0x0000000f)
  t(0x0_00f00000_00,      0b0,     0b1,    0x00000000)
  t(0x0_00000000_00,      0b0,     0b1,    0x00000000)
  t(0x0_00000000_00,      0b0,     0b1,    0x00000000)
  t(0x0_00000000_00,      0b0,     0b1,    0x00000000)
  t(0x0_00000000_00,      0b0,     0b1,    0x00000000)
  t(0x0_00000000_00,      0b0,     0b1,    0x00000000)
  t(0x0_00000000_00,      0b0,     0b1,    0x00000000)
  t(0x0_00000000_00,      0b0,     0b1,    0x00000000)
  t(0x0_00000000_00,      0b0,     0b1,    0x00000000)
  t(0x0_00000000_00,      0b0,     0b1,    0x00000000)
  t(0x0_00000000_00,      0b0,     0b1,    0x00000000)
  t(0x0_00000000_00,      0b0,     0b1,    0x00000000)
  t(0x0_00000000_00,      0b0,     0b1,    0x00000000)
  t(0x0_00000000_00,      0b0,     0b1,    0x00000000)
  t(0x0_00000000_00,      0b0,     0b1,    0x00000000)
  t(0x0_00000000_00,      0b0,     0b1,    0x00000000)
  t(0x0_00000000_00,      0b0,     0b1,    0x00000000)
  t(0x0_00000000_00,      0b0,     0b1,    0x00000000)
  t(0x0_00000000_00,      0b0,     0b1,    0x00000000)
  t(0x0_00000000_00,      0b0,     0b1,    0x00000000)
  t(0x0_00000000_00,      0b0,     0b1,    0x00000000)
  t(0x0_00000000_00,      0b0,     0b1,    0x00000000)
  t(0x0_00000000_00,      0b0,     0b1,    0x00000000)
  t(0x0_00000000_00,      0b0,     0b1,    0x00000000)
  t(0x0_00000000_00,      0b0,     0b1,    0x00000000)
  t(0x0_00000000_00,      0b0,     0b1,    0x00000000)
  t(0x0_00000000_00,      0b0,     0b1,    0x00000000)
  t(0x0_00000000_00,      0b0,     0b1,    0x00000000)
  t(0x0_00000000_00,      0b0,     0b1,    0x00000000)
  t(0x0_00000000_00,      0b0,     0b1,    0x00000000)
  t(0x0_00000000_00,      0b0,     0b1,    0x00000000)






