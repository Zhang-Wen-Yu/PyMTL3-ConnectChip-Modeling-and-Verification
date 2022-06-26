from pymtl3 import *
from Module.I2C.Common.i2c_cmd import *

# ==================================================
# i2c_resp_msg
# ==================================================

def mk_i2c_resp_msg( D ):

  @bitstruct
  class I2cRespMsg:
    data: mk_bits(D)
    def __str__( self ):
      return "{}:".format(self.data)
  return I2cRespMsg


# ==================================================
# i2c_req_msg
# ==================================================
def mk_i2c_req_msg(Data ):

  @bitstruct
  class I2cReqMsg:
    type_:   Bits1
    data: mk_bits(Data)
    def __str__( self ):
      return "{}:{}:".format(I2cMsgType.str[int(self.type_)],
                            self.data,)
  return I2cReqMsg


