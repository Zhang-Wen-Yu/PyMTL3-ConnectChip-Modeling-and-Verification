# -------------------------------------------------------------------------
# I2cMsgType
# -------------------------------------------------------------------------
# Define the "type" field of I2c messages

class I2cMsgType:
  READ       = 0
  WRITE      = 1

  str = {
    READ       : "rd",
    WRITE      : "wr",
  }