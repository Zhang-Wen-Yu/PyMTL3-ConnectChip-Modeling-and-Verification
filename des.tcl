set nfacs [ gtkwave::getNumFacs ]
set dumpname [ gtkwave::getDumpFileName ]
set dmt [ gtkwave::getDumpType ]

puts "number of signals in dumpfile '$dumpname' of type $dmt: $nfacs"

set clk48 [list]
set clk78 [list]

for {set i 0} {$i < $nfacs } {incr i} {
    set facname [ gtkwave::getFacName $i ]
    #puts "$facname"
    lappend clk48 "$facname"
}

set indx [lsearch $clk48 top.master.mosi]
puts "$indx"
set k1 [lindex $clk48 $indx]
puts $clk78
set indx [lsearch $clk48 top.master.miso]
puts $indx
set k2 [lindex $clk48 $indx]
set indx [lsearch $clk48 top.master.cs]
puts $indx
set k3 [lindex $clk48 $indx]
set indx [lsearch $clk48 top.master.sclk]
puts $indx
set k4 [lindex $clk48 $indx]
set indx [lsearch $clk48 top.slave.mosi]
puts $indx
set k5 [lindex $clk48 $indx]
set indx [lsearch $clk48 top.slave.miso]
puts $indx
set k6 [lindex $clk48 $indx]
set indx [lsearch $clk48 top.slave.cs]
puts $indx
set k7 [lindex $clk48 $indx]
set indx [lsearch $clk48 top.slave.sclk]
puts $indx
set k8 [lindex $clk48 $indx]
lappend clk78 "$k1"
lappend clk78 "$k2"
lappend clk78 "$k3"
lappend clk78 "$k4"
lappend clk78 "$k5"
lappend clk78 "$k6"
lappend clk78 "$k7"
lappend clk78 "$k8"

puts #clk78
set ll [ llength $clk78 ]
puts "number of signals found matching: $ll"

set num_added [ gtkwave::addSignalsFromList $clk78 ]
puts "num signals added: $num_added"


gtkwave::/Edit/Set_Trace_Max_Hier 0
gtkwave::/Time/Zoom/Zoom_Full

gtkwave::setMarker 128
gtkwave::setNamedMarker A 400 "Example Named Marker"

gtkwave::/File/Print_To_File PS {Letter (8.5" x 11")} Full $dumpname.ps
#gtkwave::/File/Quit
