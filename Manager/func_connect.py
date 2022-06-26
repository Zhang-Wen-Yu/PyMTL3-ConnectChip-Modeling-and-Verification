import os
import sys
from readjson import *
directory = os.getcwd()
directory= os.path.dirname(directory)
curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)

config1= read_config()
# print(config1)
globals().update(config1)
file_tb1 = target_name

# read the json of DUT's port and write in the top test
for i in range(port_num):
    if (con_state[i] == 1):
        file_obj1.write('       s.master.' + master_port[i] + ' //= ' + 's.slave.' + slave_port[i] + '\n')
        file_obj1.write('\n')