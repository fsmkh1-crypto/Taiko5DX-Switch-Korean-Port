    .text
    .p2align 2
    .global map_fwd
    .global map_rev
    .extern DELTA_BASE
    .extern FWD_HIT
    .extern FWD_MISS
    .extern REV_RETURN

map_fwd:
    mov     w9, #0xE500
    cmp     w25, w9
    b.lo    .Lf_hangul
    mov     w10, #0xE5C0
    cmp     w25, w10
    b.hs    .Lf_miss
    sub     w9, w25, w9
    add     w9, w9, #2350
    b       .Lf_encode

.Lf_hangul:
    mov     w8, #0xAC00
    cmp     w25, w8
    b.lo    .Lf_miss
    mov     w10, #0xD79D
    cmp     w25, w10
    b.hi    .Lf_miss
    mov     w9, wzr
    cmp     w25, w8
    b.eq    .Lf_encode
    adrp    x10, DELTA_BASE
    add     x10, x10, #0x18
.Lf_loop:
    ldrb    w11, [x10, w9, uxtw]
    add     w8, w8, w11
    add     w9, w9, #1
    cmp     w8, w25
    b.eq    .Lf_encode
    b.lo    .Lf_loop
    b       .Lf_miss

.Lf_encode:
    mov     w10, #188
    udiv    w11, w9, w10
    msub    w12, w11, w10, w9
    add     w11, w11, #0xEB
    add     w12, w12, #0x40
    cmp     w12, #0x7F
    cinc    w12, w12, hs
    orr     w8, w12, w11, lsl #8
    b       FWD_HIT

.Lf_miss:
    mov     w10, #0x81
    mov     w8, #0xA1
    b       FWD_MISS

    nop
map_rev:
    lsr     w8, w25, #8
    and     w9, w25, #0xFF
    sub     w10, w8, #0xEB
    cmp     w10, #13
    b.hi    .Lr_miss
    sub     w11, w9, #0x40
    cmp     w11, #188
    b.hi    .Lr_miss
    cmp     w9, #0x7F
    b.eq    .Lr_miss
    cset    w12, hi
    sub     w11, w11, w12
    mov     w12, #188
    madd    w10, w10, w12, w11
    mov     w11, #2542
    cmp     w10, w11
    b.hs    .Lr_miss
    mov     w11, #2350
    cmp     w10, w11
    b.lo    .Lr_hangul
    sub     w10, w10, w11
    mov     w25, #0xE500
    add     w25, w25, w10
    b       .Lr_return

.Lr_hangul:
    mov     w25, #0xAC00
    cbz     w10, .Lr_return
    adrp    x11, DELTA_BASE
    add     x11, x11, #0x18
    mov     w12, wzr
.Lr_loop:
    ldrb    w13, [x11, w12, uxtw]
    add     w25, w25, w13
    add     w12, w12, #1
    cmp     w12, w10
    b.lo    .Lr_loop
.Lr_return:
    b       REV_RETURN
.Lr_miss:
    mov     w25, #0x25A0
    b       REV_RETURN
