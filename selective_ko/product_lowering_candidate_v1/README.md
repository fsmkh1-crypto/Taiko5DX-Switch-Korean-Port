# Product Lowering Candidate Builder v1

This additive offline builder reproduces only the final TAI5MSG and exefs IPS candidates from the frozen product-lowering byte plans.

It intentionally does **not** replace or modify the existing V357/V218 builder path and does not build EVENT, font, install ZIPs, or runtime packages.

Inputs:
- exact Diagnostic218 `TAI5MSG_JP.DAT`
- exact Diagnostic218 BuildID IPS
- this directory's frozen corrected manifest + caller/helper/Buffer8 plans

Expected outputs:
- TAI5MSG SHA-256 `e8738545c3248db23dedbd4dff6ef7dc253b19260b6da613af0aa5186dc8cc28`
- IPS SHA-256 `dadb49f92fd66313145620194b05c108373f780f566bd5ba433f045e8acef7ec`

The builder fails closed on baseline identity, plan identity, caller preimages, helper append order/global IDs, block capacity, final hashes, TAI readback, IPS overlap, and IPS readback.
