# FGFB neuron cell, sky130A, Magic
# Units: microns ("um"). Devices from the sky130 generators (gen.tcl).
if {[file exists fgfb_cell.mag]} {file delete fgfb_cell.mag}
load fgfb_cell -force
snap internal

proc B {x1 y1 x2 y2} { box ${x1}um ${y1}um ${x2}um ${y2}um }
proc P {x1 y1 x2 y2 layers} { B $x1 $y1 $x2 $y2; foreach l $layers { paint $l } }
proc place {cell x y} { box ${x}um ${y}um ${x}um ${y}um; getcell $cell child 0 0 }
proc lab {x y layer name} { B $x $y $x $y; label $name c $layer }
# via stack from metal1 up to metal4 on a square centred at x,y
proc sq {x y h layers} { P [expr $x-$h] [expr $y-$h] [expr $x+$h] [expr $y+$h] $layers }
proc stack14 {x y} {
  sq $x $y 0.40 {metal1 metal2 metal3 metal4}
  sq $x $y 0.18 {via1}
  sq $x $y 0.20 {via2}
  sq $x $y 0.20 {via3}
}
proc stack24 {x y} {
  sq $x $y 0.40 {metal2 metal3 metal4}
  sq $x $y 0.20 {via2}
  sq $x $y 0.20 {via3}
}

# ---------------- devices ----------------
place nfgfb 0 0          ;# FGFB nFET (isolated p-well)
place nbulk 9 0          ;# bulk-control nFET (substrate)
place cfix -9 16
place cin   1 11
place cin   6 11
place cmem  16 18

# ------------- isolation: deep n-well + n-well ring -------------
P -3.6 -4.0 3.6 4.0 {dnwell}
# n-well ring overlapping the dnwell edge
P -4.2 -4.6  4.2 -2.6 {nwell}
P -4.2  2.6  4.2  4.6 {nwell}
P -4.2 -4.6 -2.2  4.6 {nwell}
P  2.2 -4.6  4.2  4.6 {nwell}
# HV n-tap in the ring (top segment) with li + mcon + metal1
P -2.1 3.2 2.1 4.0 {mvnsubdiff}
P -1.85 3.45 1.85 3.75 {mvnsubdiffcont}
P -2.0 3.35 2.0 3.85 {locali}
P 0.9 3.48 1.7 3.72 {mcon}
P 0.8 3.35 2.0 3.85 {metal1}
lab 1.4 3.6 metal1 vddh

# ---------------- FG net ----------------
# gate contact (top) metal1 -> up to a via stack at y=6, metal4 to caps
P -0.23 0.66 0.23 2.5 {metal1}
P -0.23 2.5 0.23 6.3 {metal1}
stack14 0 6.3
P -0.25 6.05 0.25 8.5 {metal4}
# metal4 bus at y 9.0..9.5 to Cin A, Cin B top plates and Cfix top plate
P -9.5 8.0 6.5 8.5 {metal4}
P  0.0 8.0 1.2 11.2 {metal4}
P  5.0 8.0 6.2 11.2 {metal4}
P -9.5 8.0 -8.5 16.0 {metal4}
lab 0 7.5 metal4 fg

# --------- body: M1 guard ring (li) -> mcon -> metal1 -> M2 left S/D ---------
P 0.90 -0.85 1.23 -0.35 {metal1}
P 1.23 -0.80 8.62 -0.40 {metal1}
P 0.98 -0.75 1.15 -0.45 {mcon}
lab 4.5 -0.6 metal1 body

# --------- membrane: M1 drain (right S/D) -> via1 -> metal2 -> Cmem top ---------
P 0.28 0.00 0.92 0.50 {metal1}
P 0.48 -0.02 0.94 0.55 {metal2}
P 0.56 0.08 0.86 0.42 {via1}
P 0.50 0.55 0.90 5.0 {metal2}
P 0.50 5.0 14.5 5.4 {metal2}
P 14.1 5.0 14.5 11.6 {metal2}
stack24 14.3 11.6
P 14.05 11.35 14.55 14.0 {metal4}
lab 7 5.2 metal2 vmem

# --------- grounds (separate labelled pieces; tied in the testbench) ---------
# M1 source (left S/D) -> metal1 left
P -0.51 -0.40 -0.28 -0.10 {metal1}
P -3.0 -0.40 -0.51 -0.10 {metal1}
lab -2.5 -0.25 metal1 gnd1
# M2 right S/D = source -> metal1 right
P 9.51 -0.40 11.0 -0.10 {metal1}
lab 10.6 -0.25 metal1 gnd2
# M2 gate (top contact) -> metal1 up, label g2
P 8.77 0.66 9.23 2.0 {metal1}
lab 9 1.6 metal1 g2

# capacitor bottom-plate terminals (metal4 strips on the right of each MIM)
P 2.30 10.5 2.67 11.5 {metal4}
lab 2.485 11 metal4 ina
P 7.30 10.5 7.67 11.5 {metal4}
lab 7.485 11 metal4 inb
P -3.90 15.5 -3.53 16.5 {metal4}
lab -3.715 16 metal4 gnd3
P 21.30 17.5 21.67 18.5 {metal4}
lab 21.485 18 metal4 gnd4
save fgfb_cell
