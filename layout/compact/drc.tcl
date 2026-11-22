load fgfb_c
select top cell
drc catchup
drc check
puts "DRCCOUNT [drc listall count total]"
set w [drc listall why]
foreach {k v} $w { puts "WHY $k :: [llength $v]"; puts "  [lrange $v 0 1]" }
puts "BOX [box values]"
quit -noprompt
