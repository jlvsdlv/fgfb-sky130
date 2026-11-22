proc mkdev {name gen params} {
  load $name -force
  box 0 0 0 0
  set p [dict merge [sky130::${gen}_defaults] $params]
  sky130::${gen}_draw $p
  save $name
}
mkdev nfgfb sky130_fd_pr__nfet_g5v0d10v5 {w 1.0 l 0.5 guard 1 viagb 0 viagt 0}
mkdev nbulk sky130_fd_pr__nfet_g5v0d10v5 {w 1.0 l 0.5 guard 1}
mkdev cin   sky130_fd_pr__cap_mim_m3_1 {w 2.0 l 2.0}
mkdev cmem  sky130_fd_pr__cap_mim_m3_1 {w 4.38 l 4.38}
mkdev cfix2 sky130_fd_pr__cap_mim_m3_2 {w 9.6 l 9.6}
foreach c {nfgfb nbulk cin cmem cfix2} {
  load $c; select top cell; puts "BBOX $c [box values]"
  foreach l {metal3 metal4 metal5 capm cap2m via3 via4 dnwell} {
    select top cell; set r [cif listall? ]; }
}
quit -noprompt
