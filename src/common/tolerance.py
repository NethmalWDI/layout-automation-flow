"""The one tolerance for "use within the allowed use" checks (Plan v3 Phase A, Q3; PREREG amendment 2026-11-01).

TOL_USE is a fraction of the allowed use, eta x margin. Its users:
  - S2's verification (G2.5) and `baselines.outcome()` (step 6 of the plan);
  - S3, as TOL_USE x eta of the margin (step 6);
  - S3's do-no-harm check for a device already below vdsat in the schematic (step 4): an option may lower its
    vds - vdsat by at most TOL_USE x |schematic value|. That tolerance is an ASSUMPTION (no upstream source).
"""
TOL_USE = 0.02
