# Final product v1

Canonical reproducible product path for Taiko Risshiden V DX Switch v1.1.3.

This directory freezes the plans consumed by `builder/final_product_candidate.py`.
The builder starts from the Diagnostic218 TAI5MSG + inherited 5-record IPS + exact Switch v1.1.3 `main`; it does not use the final TAI5MSG as an input.

Expected outputs:

- RootCause223 intermediate TAI5MSG: `8c9a70575258fad362c0197c8b59190fd332843195f35e185894ee34fe6547b1`
- final B23-reflow TAI5MSG: `1b44170a817e047ba942ba10e46571049ff7405c7fac4278c3e1598089efd61e`
- corrected 18-record IPS: `28c423a0a8e805308f8e935f2a3f5304fe12e3f948ca6468c46dd72a96cdcfae`

Required Python dependency for the tested NSO decompression path is pinned in `/requirements-final-product.txt`.

The historical IPS `dadb49f92fd66313145620194b05c108373f780f566bd5ba433f045e8acef7ec` is defective and must never be accepted as a successful output.

Runtime-pass reference package is kept outside Git as a large artifact:

- SHA-256 `cfd14031bab300929a9926bae9bb82bf28f21a9d417aee50ca527b88df873c91`
- Google Drive ID `1yCgjdWKQUTpwEfLll_Y29ztKG96EkXv2`

Its game payloads are authoritative runtime-reference bytes. Its internal `SELECTIVE_PACKAGE_INFO.json` is intentionally stale pre-B23 metadata because the known-working package was preserved byte-for-byte apart from the TAI5MSG payload during runtime diagnosis. Do not silently rewrite that reference artifact.
