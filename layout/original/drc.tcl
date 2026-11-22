source build.tcl
select top cell
drc style drc(full)
drc check
drc catchup
set n [drc listall count total]
puts "DRC total: $n"
set why [drc listall why]
foreach {msg boxes} $why { puts "DRC: $msg  ([llength $boxes] x)  first: [lindex $boxes 0]" }
quit -noprompt
