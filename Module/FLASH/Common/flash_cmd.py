# -------------------------------------------------------------------------
# FlashMsgType
# -------------------------------------------------------------------------
# Define the "type" field of flash messages

class FlashMsgType:
  ADDRESS        = 0
  WRITE          = 1
  READ           = 2
  WRITE_PROTECT  = 3

  str = {
    ADDRESS       : "ad",
    READ          : "rd",
    WRITE         : "wr",
    WRITE_PROTECT : "wp",
  }