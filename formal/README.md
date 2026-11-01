## Formal verification

NFOT includes a Lean 4 / Mathlib component in [`formal/NFOT/`](formal/NFOT/)
for checking selected mathematical definitions and propositions associated
with the Write-Back Gap and finite-sample distributional properties. The
formal component makes assumptions explicit and checks that stated theorems
follow from them. It does not establish biological validity, causal effects,
physical display timing, or empirical performance. See
[`docs/FORMAL_VERIFICATION.md`](docs/FORMAL_VERIFICATION.md) for scope and
[`formal/NFOT/README.md`](formal/NFOT/README.md) for build instructions.
