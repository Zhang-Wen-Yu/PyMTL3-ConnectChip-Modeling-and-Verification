from pymtl3 import *
from pymtl3.stdlib.test_utils import config_model_with_cmdline_opts
from Module.PROM.prom.prom import prom
def test_basic( cmdline_opts ):

  # Create the model
  model = prom()

  # Configure the model
  model = config_model_with_cmdline_opts( model, cmdline_opts, duts=[] )

  # Create and reset simulator
  model.apply( DefaultPassGroup(linetrace=True) )
  model.sim_reset()

  # Helper function
  def t( CE1, OE1,busy,TDI):

    # Write input value to input port

    model.prom_ifc.CE1       @= CE1
    model.prom_ifc.OE1       @= OE1
    model.prom_ifc.busy      @= busy
    model.prom_ifc.TDI       @= TDI
    # Ensure that all combinational concurrent blocks are called

    model.sim_eval_combinational()

    # Tick simulator one cycle
    model.sim_tick()


  # CE1, OE1, busy ,data_out
  t(0b0, 0b1, 0b0,  0b0)
  t(0b0, 0b1, 0b0,  0b1)
  t(0b0, 0b1, 0b0,  0b1)
  t(0b0, 0b1, 0b0,  0b1)
  t(0b0, 0b1, 0b0,  0b0)
  t(0b0, 0b1, 0b0,  0b0)
  t(0b0, 0b1, 0b0,  0b0)
  t(0b0, 0b1, 0b0,  0b1)
  t(0b0, 0b1, 0b0,  0b0)


