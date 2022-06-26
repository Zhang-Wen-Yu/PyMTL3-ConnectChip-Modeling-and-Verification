from pymtl3 import *
from pymtl3.stdlib.test_utils import config_model_with_cmdline_opts
from Module.M1553b.Common.decoder import DeCoder
def test_basic( cmdline_opts ):
  # Create the model
  model = DeCoder()
  # Configure the model
  model = config_model_with_cmdline_opts( model, cmdline_opts, duts=[] )
  # Create and reset simulator
  model.apply( DefaultPassGroup(linetrace=True) )
  model.sim_reset()
  # Helper function
  def t(in_):
    # Write input value to input port
    model.in_     @= in_

    # Ensure that all combinational concurrent blocks are called
    model.sim_eval_combinational()
    # If reference output is not '?', verify value read from output port
    # Tick simulator one cycle
    model.sim_tick()
  # sda_i scl
  t(0b1)

  t(0b1) #1   1
  t(0b1)
  t(0b0)
  t(0b0)

  t(0b0) #2   0
  t(0b0)
  t(0b1)
  t(0b1)

  t(0b1) #3   1
  t(0b1)
  t(0b0)
  t(0b0)

  t(0b0) #4   0
  t(0b0)
  t(0b1)
  t(0b1)

  t(0b1) #5   1
  t(0b1)
  t(0b0)
  t(0b0)

  t(0b0) #6
  t(0b0)





