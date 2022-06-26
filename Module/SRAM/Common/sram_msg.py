from pymtl3 import *
from Module.SRAM.Common.sram_cmd import MemMsgType

# ===================================================
# mem_req_msg
# ===================================================

def mk_mem_req_msg(  a, d, b ):
  
  @bitstruct
  class MemReqMsg:        
    type_  : Bits2                  
    addr   : mk_bits( a           )  
    data   : mk_bits( d           )  
    row   : mk_bits( b           )             

    def __str__( self ):
      return "{}:{}:{}:{}".format(
        MemMsgType.str[ int( self.type_ ) ],
        self.addr,
        self.data if self.type_ != MemMsgType.READ else " " * ( d//4 ),
        self.row,
      )
      
  return MemReqMsg



# ==================================================
# mem_resp_msg
# ==================================================

def mk_mem_resp_msg( d ):

  @bitstruct
  class MemRespMsg:           
    type_  : Bits2                         
    data   : mk_bits( d )        

    def __str__( self ):
      return "{}:{}".format(
        MemMsgType.str[ int( self.type_ ) ],
        self.data if self.type_ != MemMsgType.WRITE else " " * ( d//4 ),
      )
  return MemRespMsg

