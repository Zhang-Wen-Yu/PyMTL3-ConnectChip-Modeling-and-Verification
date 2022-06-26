# -------------------------------------------------------------------------
# M1553bMsgType
# -------------------------------------------------------------------------

class M1553bCmdMsgType:
  SEND       = 0
  RECEIVE    = 1

  str = {
    SEND       : "rd",
    RECEIVE    : "wr",
  }

class M1553bMsgType:
  CMD       = 0
  DATA      = 1

  str = {
    CMD       : "cmd",
    DATA      : "data",
  }


