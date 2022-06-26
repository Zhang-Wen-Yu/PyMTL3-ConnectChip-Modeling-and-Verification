import os

directory = os.path.dirname(os.getcwd())
print(directory)
# os.startfile(directory+'\gtkwave\gtkwave\\bin\gtkwave.exe')
# check any vcd file only to change the name
os.system('gtkwave ' + directory + "\Vcdwavedir" + "\sim__test_stack_8bit_basic_0x0.vcd")
print('gtkwave ' +directory + '\\Vcdwavedir' + '\\sim__test_stack_8bit_basic_0x0.vcd')
