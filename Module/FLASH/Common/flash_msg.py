from pymtl3 import *
from Module.FLASH.Common.flash_cmd import *

# ===================================================
# flash_req_msg
# ===================================================


def mk_flash_req_msg( d):
  @bitstruct
  class FlashReqMsg:
    type_  : Bits2
    data   : mk_bits( d )

    data_nbits = d

    def __str__( self ):
      return "{}:{}".format(
        FlashMsgType.str[ int( self.type_ ) ],
        self.data if self.type_ != FlashMsgType.READ else " " * ( d//4 ),
      )

  return FlashReqMsg

# ==================================================
# flash_resp_msg
# ==================================================

def mk_flash_resp_msg( d ):
  @bitstruct
  class FlashRespMsg:
    type_  : Bits2
    data   : mk_bits( d )
    data_nbits = d

    def __str__( self ):
      return "{}:{}".format(
        FlashMsgType.str[ int( self.type_ ) ],
        self.data if self.type_ != FlashMsgType.WRITE else " " * ( d//4 ),
      )
  return FlashRespMsg
