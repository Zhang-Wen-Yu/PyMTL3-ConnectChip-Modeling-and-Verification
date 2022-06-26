from pymtl3 import *
from pymtl3.stdlib.test_utils import config_model_with_cmdline_opts
from Module.JTAG.jtag_pc.jtag_pc import *
def test_basic( cmdline_opts ):

  # Create the model
  model = jtag_pc()

  # Configure the model
  model = config_model_with_cmdline_opts( model, cmdline_opts, duts=[] )

  # Create and reset simulator
  model.apply( DefaultPassGroup(linetrace=True) )
  model.sim_reset()

  # Helper function
  def t( tdo):
    model.ifc.TDO @= tdo



    # Write input value to input port

    # Ensure that all combinational concurrent blocks are called

    model.sim_eval_combinational()

    # If reference output is not '?', verify value read from output port

    # Tick simulator one cycle
    model.sim_tick()



  # tdi tms
  t(0b1)
  t(0b1)
  t(0b1)
  t(0b1)
