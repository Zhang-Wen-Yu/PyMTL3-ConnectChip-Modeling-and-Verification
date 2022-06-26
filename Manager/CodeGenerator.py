# ============================
# generate the top connect module
# ============================
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


# write in top test file
with open(directory+'\\TestBench\\'+file_tb1+'.py','a') as file_obj1:
 print(directory)
 print(file_obj1)
 file_obj1.seek(0)
 file_obj1.truncate()


 file_obj1.write("# ========================================================================="'\n'
                 "#  Test Top"'\n'
                 "# ========================================================================="'\n')

 file_obj1.write('\n'"# import the Module and DUT1&2"'\n')

 file_obj1.write('import pytest' + '\n'
                 'import random' + '\n'
                 'from pymtl3.stdlib.test_utils import mk_test_case_table, run_sim''\n'
                 'from pymtl3.stdlib import stream''\n'
                 'from '+ file_name +'.'+ master_file_name+ '.' + master_module_name+' import *''\n'
                 'from '+ file_name +'.'+ slave_file_name + '.' + slave_module_name + ' import *''\n''\n')

 # comment
 file_obj1.write("# -------------------------------------------------------------------------"'\n'
                 "# TestHarness"'\n'
                 "# -------------------------------------------------------------------------"'\n')


 file_obj1.write('\n'"# define the class and import the DUT1 and DUT2"'\n')
 file_obj1.write('class '+ class_name +'(Component):''\n''\n'
                 '    def construct(s,'+control_param+',flow_control):''\n''\n'
                 '       s.master = '+master_class_name+'('+control_param+')''\n'
                 '       s.slave  = '+slave_class_name+'('+control_param+')''\n''\n'
                 "       # Instantiate models"'\n'
                 '       s.src = stream.SourceRTL(mk_bits('+test_src_param+'))''\n'
                 '       s.sink = stream.SinkRTL(mk_bits('+test_sink_param+'))''\n''\n'
 )


 file_obj1.write('\n'"       # write the send interface and recv interface and connect"'\n')
 file_obj1.write('       s.src.send //= s.master.req''\n''\n'
                 '       s.master.resp //= s.sink.recv''\n''\n')

 file_obj1.write('\n'"       # write the DUT1 and DUT2 port and connect"'\n')


 # read the json of DUT's port and write in the top test
 for i in range(port_num):
     if (con_state[i] == 1):
         file_obj1.write('       s.master.'+master_port[i]+ ' //= '+ 's.slave.'+slave_port[i]+'\n')
         file_obj1.write('\n')


 file_obj1.write('\n'"    # define the founction done and line_trace "'\n')
 file_obj1.write('    def done(s):''\n'
                 '       return s.src.done() and s.sink.done()''\n''\n'
                 '    def line_trace(s):''\n'
                 '       return s.src.line_trace() + " > " +s.master.line_trace()+ " > " + s.sink.line_trace()''\n''\n')

 # define the test case basic
 file_obj1.write("# -------------------------------------------------------------------------"'\n'
                 "# Test Case: basic"'\n'
                 "# -------------------------------------------------------------------------"'\n'
                 'basic_msgs = [''\n''    5, 0,  ''\n'
                 '    1, 5,  ''\n'
                 '    4, 1,  ''\n'
                 '    8, 4,  ''\n'
                 '    0, 8, ''\n'']''\n')

 # define the test case large
 file_obj1.write("# -------------------------------------------------------------------------"'\n'
                 "# Test Case: larger"'\n'
                 "# -------------------------------------------------------------------------"'\n'
                 'larger_msgs = [''\n'
                 '    125, 0,''\n'
                 '    420, 125,''\n'
                 '    18, 420,''\n'
                 '    88, 18,''\n'
                 '    0, 88,''\n'
                 ']''\n\n')


 # use the test case basic to construct test case small
 file_obj1.write("# -------------------------------------------------------------------------"'\n'
                 "# Test Case small"'\n'
                 "# -------------------------------------------------------------------------"'\n'
                 'test_case_8bits = mk_test_case_table([''\n'
                 '     ("msgs        src_delay  sink_delay"),''\n'
                 '     ["basic_0x0", basic_msgs, 0, 0, ],''\n'
                 '     ["basic_1x5", basic_msgs, 1, 5, ],''\n'
                 '     ["basic_3x1", basic_msgs, 3, 1, ],''\n'
                 '     ["basic_8x8", basic_msgs, 8, 8, ],''\n'
                 '     ["basic_7x7", basic_msgs, 7, 7, ],''\n'
                 '])''\n''\n''\n')


 # use the test case large
 file_obj1.write("# -------------------------------------------------------------------------"'\n'
                 "# Test Case large"'\n'
                 "# -------------------------------------------------------------------------"'\n'
                 'test_case_12bits = mk_test_case_table([''\n'
                 '      ("msgs          src_delay  sink_delay"),''\n'
                 '      ["larger_0x0", larger_msgs, 0, 0, ],''\n'
                 '      ["larger_1x5", larger_msgs, 1, 5, ],''\n'
                 '      ["larger_3x1", larger_msgs, 3, 1, ],''\n'
                 '      ["larger_8x8", larger_msgs, 8, 8, ],''\n'
                 '      ["larger_7x7", larger_msgs, 7, 7, ],''\n'
                 '])''\n''\n')


 file_obj1.write("# -------------------------------------------------------------------------"'\n'
                 "# Test cases"'\n'
                 "# -------------------------------------------------------------------------"'\n')

 # generate the small case
 file_obj1.write(
 "@pytest.mark.parametrize(**test_case_8bits)"'\n'
 'def test_stack_8bit(test_params, cmdline_opts):''\n'
 '    th = TestHarness(8, 0)''\n''\n'
 '    th.set_param("top.src.construct",''\n'
 '                 msgs=test_params.msgs[::2],''\n'
 '                 initial_delay=test_params.src_delay,''\n'
 '                 interval_delay=test_params.src_delay)''\n''\n'
 '    th.set_param("top.sink.construct",''\n'
 '                msgs=test_params.msgs[1::2],''\n'
 '                 initial_delay=test_params.sink_delay,''\n'
 '                 interval_delay=test_params.sink_delay)''\n''\n'
 '    run_sim(th, cmdline_opts)''\n\n')

 # generate the large case
 file_obj1.write(
 "@pytest.mark.parametrize(**test_case_12bits)"'\n'
 'def test_stack_12bit(test_params, cmdline_opts):''\n'
 '   th = TestHarness(12, 0)''\n''\n'
 '   th.set_param("top.src.construct",''\n'
 '                msgs=test_params.msgs[::2],''\n'
 '                initial_delay=test_params.src_delay,''\n'
 '                interval_delay=test_params.src_delay)''\n''\n'
 '   th.set_param("top.sink.construct",''\n'
 '                msgs=test_params.msgs[1::2],''\n'
 '                initial_delay=test_params.sink_delay,''\n'
 '                interval_delay=test_params.sink_delay)''\n''\n'
 '   run_sim(th, cmdline_opts)''\n\n')




