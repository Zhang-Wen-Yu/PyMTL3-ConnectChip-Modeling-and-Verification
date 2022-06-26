from pymtl3 import *

# ==================================================
# jtag_resp_msg
# ==================================================

def mk_jtag_resp_msg( do ):

  @bitstruct
  class JtagRespMsg:
    tdo   : mk_bits( do )         # 32

    def __str__( self ):
      return "{}".format(self.tdo,)
  return JtagRespMsg

# ==================================================
# jtag_req_msg
# ==================================================

def mk_jtag_req_msg( di,ms ):

  @bitstruct
  class JtagReqMsg:
    tdi    : mk_bits( di )
    tms    : mk_bits( ms)

    def __str__( self ):
      return "{}:{}".format(self.tdi, self.tms,)
  return JtagReqMsg


