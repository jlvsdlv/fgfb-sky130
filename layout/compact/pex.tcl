load fgfb_c
select top cell
extract path extfiles
extract all
ext2spice lvs
ext2spice cthresh 0
ext2spice -p extfiles -o fgfbc_pex.spice
ext2spice lvs
ext2spice -p extfiles -o fgfbc_lvs.spice
gds write fgfb_c.gds
quit -noprompt
