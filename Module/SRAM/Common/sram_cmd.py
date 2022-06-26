# -------------------------------------------------------------------------
# MemMsgType
# -------------------------------------------------------------------------
# Define the "type" field of memory messages

class MemMsgType:
  READ       = 0
  WRITE      = 1
  WRITE_INIT = 2

  str = {
    READ       : "rd",
    WRITE      : "wr",
    WRITE_INIT : "in",
  }