DELTA_BASE = 0x9BF018;
FWD_HIT = 0x430568;
FWD_MISS = 0x43056C;
REV_RETURN = 0x430820;
SECTIONS {
  .text 0x58CE60 : ALIGN(4) { *(.text*) }
  /DISCARD/ : { *(.comment*) *(.note*) *(.eh_frame*) }
}
