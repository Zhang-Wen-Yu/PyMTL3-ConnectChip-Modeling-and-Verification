from pymtl3 import *
from pymtl3.stdlib.test_utils import config_model_with_cmdline_opts
from Module.SRAM.SRAM.Sram import Sdram
def test_basic( cmdline_opts ):

  # Create the model
  model = Sdram()

  # Configure the model
  model = config_model_with_cmdline_opts( model, cmdline_opts, duts=[] )

  # Create and reset simulator
  model.apply( DefaultPassGroup(linetrace=True) )
  model.sim_reset()

  # Helper function
  def t( CS1, WE1, OE1,  A1, I1, BA1, WBM1):

    # Write input value to input port
    model.sdram_inter.CS1   @= CS1
    model.sdram_inter.WE1   @= WE1
    model.sdram_inter.OE1   @= OE1
    model.sdram_inter.A1    @= A1
    model.sdram_inter.I1    @= I1
    model.sdram_inter.WBM1  @= WBM1
    model.sdram_inter.CE1   @= model.clk
    model.sdram_inter.BA1   @= BA1
    # Ensure that all combinational concurrent blocks are called

    model.sim_eval_combinational()

    # If reference output is not '?', verify value read from output port

    # Tick simulator one cycle
    model.sim_tick()

    #  Port Name          Direction        Description
    #  -----------------------------------------------------------------------
    #  s.sram_inter.CS1      I           sdram select (1 = enabled)
    #  s.sram_inter.WE1      I           transaction type(write enable), 0 = read, 1 = write
    #  s.sram_inter.OE1      I           if nor not output the read data, 0 = output, 1 = not output
    #  s.sram_inter.CE1      I           sdram clk in
    #  s.sram_inter.A1       I           sdram address
    #  s.sram_inter.I1       I           write data input
    #  s.sram_inter.O1       O           read data output
    #  s.sram_inter.WBM1     I           write bit enable (1 = enabled)


  # CS1, WE1, OE1,   A1,      I1,     BA1,     WBM1
  t(0b1, 0b1, 0b0,  0x00, 0x10000000, 0b1, 0xffffffff)    # write to  sdram
  t(0b1, 0b0, 0b0,  0x00, 0x00000000, 0b1, 0xffffffff)    # read from sdram
  t(0b1, 0b0, 0b0,  0x00, 0x00000000, 0b1, 0xffffffff)
  t(0b1, 0b0, 0b0,  0x00, 0x00000000, 0b1, 0xffffffff)
  t(0b1, 0b0, 0b0,  0x00, 0x00000000, 0b1, 0xffffffff)
  t(0b1, 0b1, 0b0,  0xff, 0xaaa00000, 0b1, 0xffffffff)    # write to sdram
  t(0b1, 0b0, 0b0,  0xff, 0x00000000, 0b1, 0xffffffff)    # read from sdram
  t(0b1, 0b0, 0b0,  0x00, 0x00000000, 0b1, 0xffffffff)
  t(0b1, 0b0, 0b0,  0x00, 0x00000000, 0b1, 0xffffffff)
  t(0b1, 0b1, 0b0,  0x00, 0x0f000000, 0b1, 0xffffffff)
  t(0b1, 0b0, 0b0,  0x00, 0x00000000, 0b1, 0xffffffff)
  t(0b1, 0b0, 0b0,  0x00, 0x00000000, 0b1, 0xffffffff)


