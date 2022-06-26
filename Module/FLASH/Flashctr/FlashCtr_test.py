from pymtl3 import *
from pymtl3.stdlib.test_utils import config_model_with_cmdline_opts
from Module.FLASH.Flashctr.FlashCtr import *
def test_basic( cmdline_opts ):

  # Create the model
  model = Flashctr()

  # Configure the model
  model = config_model_with_cmdline_opts( model, cmdline_opts, duts=[] )

  # Create and reset simulator
  model.apply( DefaultPassGroup(linetrace=True) )
  model.sim_reset()

  # Helper function
  def t( type, data, send_rdy, O ,ROB):

    # Write input value to input port
    model.req.msg.type_ @= type
    model.req.msg.data  @= data
    model.resp.rdy     @= send_rdy
    model.ifc.O       @= O
    model.ifc.ROB      @= ROB

    # Ensure that all combinational concurrent blocks are called
    model.sim_eval_combinational()


    # Tick simulator one cycle
    model.sim_tick()
    #recv_msg,  recv_val, send_rdy,  O     ROB
  t(0b00,  0x00,        0b1,     0x00, 0b0)

