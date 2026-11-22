source build.tcl
select top cell
extract path extfiles
extract all
ext2spice lvs
ext2spice cthresh 0
ext2spice -p extfiles -o fgfb_pex.spice
ext2spice lvs
ext2spice -p extfiles -o fgfb_lvs.spice
gds write fgfb_cell.gds
quit -noprompt
