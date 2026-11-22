# Compact FGFB cell: MIMs stacked over the transistors. Cmem 4.38x4.38 (MIM1),
# Cin A/B 2x2 (MIM1, under the FG sheet), Cfix 9.6x9.6 on MIM2 whose metal4 bottom plate is the FG.
if {[file exists fgfb_c.mag]} {file delete fgfb_c.mag}
load fgfb_c -force
snap internal
proc B {x1 y1 x2 y2} { box ${x1}um ${y1}um ${x2}um ${y2}um }
proc P {x1 y1 x2 y2 layers} { B $x1 $y1 $x2 $y2; foreach l $layers { paint $l } }
proc place {cell x y {o 0}} { box ${x}um ${y}um ${x}um ${y}um; if {$o==0} {getcell $cell child 0 0} else {getcell $cell $o child 0 0} }
proc lab {x y layer name} { B $x $y $x $y; label $name c $layer }
proc sq {x y h layers} { P [expr $x-$h] [expr $y-$h] [expr $x+$h] [expr $y+$h] $layers }
proc stack14 {x y} { sq $x $y 0.40 {metal1 metal2 metal3 metal4}; sq $x $y 0.18 {via1}; sq $x $y 0.20 {via2}; sq $x $y 0.20 {via3} }
proc stack24 {x y} { sq $x $y 0.40 {metal2 metal3 metal4}; sq $x $y 0.20 {via2}; sq $x $y 0.20 {via3} }

place nfgfb 0 0
place nbulk 9 0
place cfix2 -1.5 0
place cin -3.5 -6.2 90
place cin 0.5 -6.2 90
place cmem 9.6 0

# isolation (as in the original cell)
P -3.6 -4.0 3.6 4.0 {dnwell}
P -4.2 -4.6  4.2 -2.6 {nwell}
P -4.2  2.6  4.2  4.6 {nwell}
P -4.2 -4.6 -2.2  4.6 {nwell}
P  2.2 -4.6  4.2  4.6 {nwell}
P -2.1 3.2 2.1 4.0 {mvnsubdiff}
P -1.85 3.45 1.85 3.75 {mvnsubdiffcont}
P -2.0 3.35 2.0 3.85 {locali}
P 0.9 3.48 1.7 3.72 {mcon}
P 0.8 3.35 2.0 3.85 {metal1}
lab 1.4 3.6 metal1 vddh

# FG: gate metal1 -> stack to metal4 (merges with the MIM2 bottom plate)
P -0.23 0.66 0.23 2.5 {metal1}
P -0.23 2.1 2.9 2.5 {metal1}
stack14 2.9 2.3
lab 2.9 2.3 metal4 fg

# body
P 0.90 -0.85 1.23 -0.35 {metal1}
P 1.23 -0.80 8.62 -0.40 {metal1}
P 0.98 -0.75 1.15 -0.45 {mcon}
lab 4.5 -0.6 metal1 body

# membrane: drain -> metal2 down to y=-3.6 -> right -> stack -> metal4 tab into Cmem top plate
P 0.28 0.00 0.92 0.50 {metal1}
P 0.48 -0.02 0.94 0.55 {metal2}
P 0.56 0.08 0.86 0.42 {via1}
P 0.50 -3.80 0.90 0.0 {metal2}
P 0.50 -3.80 9.6 -3.40 {metal2}
stack24 9.6 -3.6
P 9.35 -3.6 9.85 -1.0 {metal4}
lab 5 -3.6 metal2 vmem

# grounds / gate of M2
P -0.51 -0.40 -0.28 -0.10 {metal1}
P -3.0 -0.40 -0.51 -0.10 {metal1}
lab -2.5 -0.25 metal1 gnd1
P 9.51 -0.40 11.0 -0.10 {metal1}
lab 10.6 -0.25 metal1 gnd2
P 8.77 0.66 9.23 2.0 {metal1}
lab 9 1.6 metal1 g2

# capacitor terminals
P -1.8 -0.3 -1.2 0.3 {metal5}
lab -1.5 0 metal5 gnd3
P 12.1 -0.3 12.45 0.3 {metal4}
lab 12.275 0 metal4 gnd4
P -3.7 -7.885 -3.3 -7.485 {metal4}
lab -3.5 -7.685 metal4 ina
P 0.3 -7.885 0.7 -7.485 {metal4}
lab 0.5 -7.685 metal4 inb
save fgfb_c
quit -noprompt
