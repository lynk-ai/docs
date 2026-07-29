"""Paired per-case comparison of two eval runs (McNemar-style).

At ~29 cases the aggregate pass rate has a ±8-9pp standard error — a
single-digit delta between runs is noise. The signal is in the paired
per-case flips: which cases changed verdict, and in which direction.

Usage:
    uv run python compare.py results/<run-A> results/<run-B>
"""

import json
import sys
from pathlib import Path


def load(run_dir: str) -> tuple[dict, dict]:
    meta = json.loads((Path(run_dir) / "meta.json").read_text())
    return meta, meta["verdicts"]


def main() -> int:
    if len(sys.argv) != 3:
        print(__doc__)
        return 2
    (meta_a, va), (meta_b, vb) = load(sys.argv[1]), load(sys.argv[2])
    label_a = f"{meta_a['run']} (arm {meta_a.get('arm', '?')})"
    label_b = f"{meta_b['run']} (arm {meta_b.get('arm', '?')})"
    shared = sorted(set(va) & set(vb))
    if not shared:
        print("no shared case ids between the two runs")
        return 2

    improved = [i for i in shared if va[i] != "PASS" and vb[i] == "PASS"]
    regressed = [i for i in shared if va[i] == "PASS" and vb[i] != "PASS"]
    both_fail = [i for i in shared if va[i] != "PASS" and vb[i] != "PASS"]

    print(f"A: {label_a}  ·  B: {label_b}  ·  {len(shared)} shared cases")
    print(f"pass: A {sum(1 for i in shared if va[i] == 'PASS')}"
          f" → B {sum(1 for i in shared if vb[i] == 'PASS')}")
    print(f"\nimproved (A✗ → B✓): {len(improved)}")
    for i in improved:
        print(f"  {i}: {va[i]} → {vb[i]}")
    print(f"regressed (A✓ → B✗): {len(regressed)}")
    for i in regressed:
        print(f"  {i}: {va[i]} → {vb[i]}")
    print(f"still failing in both: {len(both_fail)}")
    for i in both_fail:
        print(f"  {i}: {va[i]} / {vb[i]}")
    print("\nMcNemar discordant pairs: "
          f"{len(improved)} vs {len(regressed)} — "
          + ("B better" if len(improved) > len(regressed) else
             "A better" if len(regressed) > len(improved) else "tied")
          + "; with counts this small, treat |diff| <= 2 as noise.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
