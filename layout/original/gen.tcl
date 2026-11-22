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
mkdev cfix  sky130_fd_pr__cap_mim_m3_1 {w 9.6 l 9.6}
mkdev cmem  sky130_fd_pr__cap_mim_m3_1 {w 10.0 l 10.0}
quit -noprompt
