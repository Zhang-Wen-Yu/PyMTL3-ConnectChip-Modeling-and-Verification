from pymtl3 import *
from pymtl3.stdlib.test_utils import config_model_with_cmdline_opts
from Module.M1553b.M1553b_bc.m1553b_bus_control import *
def test_basic( cmdline_opts ):

  # Create the model
  model = m1553b_bus_controller()

  # Configure the model
  model = config_model_with_cmdline_opts( model, cmdline_opts, duts=[] )

  # Create and reset simulator
  model.apply( DefaultPassGroup(linetrace=True) )
  model.sim_reset()

  # Helper function
  def t( cmd_word, data_word, send_rdy):

    # Write input value to input port
    model.tb2bc.msg.type_        @= 0
    model.tb2bc.msg.cmd_type_    @= 0
    model.tb2bc.msg.cmd_word     @= cmd_word
    model.tb2bc.msg.data_word    @= data_word
    model.bc2tb.rdy              @= send_rdy

    # Ensure that all combinational concurrent blocks are called
    model.sim_eval_combinational()

    # Tick simulator one cycle
    model.sim_tick()

  # cmd_word,data_word,send_rdy
  t(0xfffff, 0xfffff, 0b1)
  t(0xfffff, 0xfffff, 0b1)
  t(0xfffff, 0xfffff, 0b1)
  t(0xfffff, 0xfffff, 0b1)
  t(0xfffff, 0xfffff, 0b1)
  t(0xfffff, 0xfffff, 0b1)
  t(0xfffff, 0xfffff, 0b1)
  t(0xfffff, 0xfffff, 0b1)
  t(0xfffff, 0xfffff, 0b1)
  t(0xfffff, 0xfffff, 0b1)
  t(0xfffff, 0xfffff, 0b1)
  t(0xfffff, 0xfffff, 0b1)
  t(0xfffff, 0xfffff, 0b1)
  t(0xfffff, 0xfffff, 0b1)
  t(0xfffff, 0xfffff, 0b1)
  t(0xfffff, 0xfffff, 0b1)
  t(0xfffff, 0xfffff, 0b1)
  t(0xfffff, 0xfffff, 0b1)
  t(0xfffff, 0xfffff, 0b1)
  t(0xfffff, 0xfffff, 0b1)
  t(0xfffff, 0xfffff, 0b1)
  t(0xfffff, 0xfffff, 0b1)
  t(0xfffff, 0xfffff, 0b1)
  t(0xfffff, 0xfffff, 0b1)







