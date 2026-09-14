# CWTDAT AUXILIARY NAME-ROW HOLD NOTE

Date: 2026-09-14 (KST)
Status: `HOLD_FOR_CWTDAT`

## Purpose

Preserve the current read-only conclusion for anomaly A (garbled small auxiliary person-name/reading row) without creating a separate interim fix. Resume this item as part of Switch-native `CWTDAT_JP.TR5` reconstruction.

## Current conclusion

- Y0 already restored the 2,099 historical main yomi-like fields and disabled the eight known direct visible-yomi enables, but the observed small rows remained. Do not repeat that eight-site-only route.
- The observed protagonist-selection/dialogue auxiliary rows belong to a separate person-name auxiliary path, not the previously tested shared yomi path.
- Current data comparison indicates the PC Korean patch uses Korean SNR person display names while retaining a parallel Japanese person-reading table in `CWTDAT_JP.TR5`, aligned by person index (1,244-person population).
- Therefore anomaly A is currently best treated as a PC-vs-Switch field-selection / semantic-binding issue around SNR display-name data and CWTDAT reading data, not as a standalone font/render defect.
- Exact PC runtime XREF from the CWTDAT reading field to the final draw call remains unclosed; the data-source binding above is a strong working conclusion, not final runtime proof.

## Mandatory CWTDAT checks

When `CWTDAT_JP.TR5` Switch-native reconstruction starts:

1. Identify the Switch counterpart of the 1,244-person reading table and its record/field structure.
2. Preserve original Japanese reading semantics unless PC evidence proves another behavior.
3. Reconstruct on the Switch-native layout; do not wholesale-copy the larger PC CWTDAT file.
4. Include anomaly A in CWTDAT validation: protagonist-selection auxiliary row and dialogue nameplate auxiliary row must both be rechecked after reconstruction.
5. If both rows remain broken after a structurally correct CWTDAT reconstruction, only then reopen the remaining runtime field-selection/binding path as a separate cause family.

## Boundary

No standalone A patch, diagnostic build, or suppression patch is authorized by this note. A remains parked under `HOLD_FOR_CWTDAT` until the CWTDAT scope is explicitly started.
