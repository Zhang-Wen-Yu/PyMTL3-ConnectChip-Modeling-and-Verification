from pymtl3 import *
from pymtl3.passes.backends.verilog import *
from Module.SPI.SPIMaster.SpiMasterWarpped import Spi_Master_Warpped
model = Spi_Master_Warpped()
model.set_metadata( VerilogTranslationPass.enable, True )
model.apply( VerilogTranslationPass() )
