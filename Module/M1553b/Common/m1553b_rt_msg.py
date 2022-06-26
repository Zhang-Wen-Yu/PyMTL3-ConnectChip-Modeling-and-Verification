from pymtl3 import *
from Module.M1553b.Common.m1553b_cmd import *

# ===================================================
# RT_resp_cmd_msg
# ===================================================

def mk_m1553b_rt_resp_msg():
    @bitstruct
    class M1553bReqMsg:
        type_: Bits1
        cmd_type_ : Bits1
        # [1:3]: head
        # [4:8]: remote addr
        # [9]  : send or receive(0: BC->RT, 1: RT->BC)
        # [20] : parity
        data_word : Bits20
        # [1:3] : head
        # [4:19]: data
        # [20]  : parity
        def __str__(self):
            return "{}:{}:{}".format(
                M1553bMsgType.str[int(self.type_)],
                M1553bCmdMsgType.str[int(self.cmd_type_)],
                self.cmd_word,
                self.data_word,
            )
    return M1553bReqMsg

# ==================================================
# RT_req_msg
# ==================================================

def mk_m1553b_rt_req_msg():
    @bitstruct
    class M1553bRespMsg:
        type_: Bits1
        status_word: Bits40
        data_word:   Bits40
        cmd_word: Bits40

        def __str__(self):
            return "{}:{}:{}".format(
                M1553bMsgType.str[int(self.type_)],
                self.status_word,
                self.data_word,
            )

    return M1553bRespMsg

