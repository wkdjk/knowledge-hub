#!/usr/bin/env python3
"""Convert the NZ velvet exports flat CSV (monthly) into the site's export files.

Usage:
    python3 scripts/convert_nz_exports.py "sources/deer_velvet_nz_exports_20192026H1_flat.csv"

Outputs (relative to repo root):
    data/nz-exports-monthly.csv  - source of record: year x month x destination x form, kg
                                   (velvet categories only: dried / frozen / other)
    data/nz-exports.csv          - chart file: year x tonnes, summed across all
                                   destinations, complete years only (all 12 months)

Only the three "velvet, unworked" HS categories (dried / frozen / other) are
counted, to match how Korean quarantine defines dried/frozen velvet. The
generic "antler/velvet unworked" parent code and "powder of horns/velvet" are
excluded. Same input always produces byte-identical output; a summary prints
for eyeball verification.
"""
import csv
import sys
from collections import defaultdict
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
VELVET = {
    "Velvet, unworked, dried": "dried",
    "Velvet, unworked, frozen": "frozen",
    "Velvet, unworked, other": "other",
}


def fail(msg):
    sys.exit(f"ERROR: {msg}")


def main():
    if len(sys.argv) != 2:
        fail(f"usage: {sys.argv[0]} <NZ exports flat CSV>")
    src = Path(sys.argv[1])
    if not src.exists():
        fail(f"input file not found: {src}")

    with open(src, newline="", encoding="utf-8-sig") as f:
        rows = list(csv.DictReader(f))
    need = {"Year", "Month", "Product_EN", "Country", "Quantity_kg"}
    if not need.issubset(rows[0].keys()):
        fail(f"missing expected columns; found {list(rows[0].keys())}")

    records = []          # (year, month, destination, form, kg)
    months_seen = defaultdict(set)
    for r in rows:
        year, month = int(r["Year"]), int(r["Month"])
        months_seen[year].add(month)
        form = VELVET.get(r["Product_EN"])
        if not form:
            continue
        kg = float(r["Quantity_kg"] or 0)
        if kg:
            records.append((year, month, r["Country"], form, kg))

    records.sort(key=lambda x: (x[0], x[1], x[2], x[3]))
    monthly_path = REPO_ROOT / "data" / "nz-exports-monthly.csv"
    with open(monthly_path, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["year", "month", "destination", "form", "kg"])
        for year, month, dest, form, kg in records:
            w.writerow([year, month, dest, form, f"{kg:g}"])

    complete_years = {y for y, ms in months_seen.items() if len(ms) == 12}
    totals = defaultdict(float)
    for year, month, dest, form, kg in records:
        if year in complete_years:
            totals[year] += kg

    exports_path = REPO_ROOT / "data" / "nz-exports.csv"
    with open(exports_path, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["year", "tonnes"])
        for year in sorted(totals):
            w.writerow([year, f"{totals[year] / 1000:.1f}"])

    # ---- verification summary ----
    all_years = sorted(months_seen)
    dests = sorted({d for _, _, d, _, _ in records})
    partial = sorted(y for y in months_seen if y not in complete_years)
    print(f"input : {src}")
    print(f"parsed: {len(records)} monthly velvet rows "
          f"({len(dests)} destinations), years {all_years[0]}-{all_years[-1]}")
    if partial:
        print(f"partial years (excluded from nz-exports.csv): {partial}")
    print(f"wrote : {monthly_path} ({len(records)} rows)")
    print(f"wrote : {exports_path} ({len(totals)} rows)")
    print("\ntotal velvet export tonnes by year (all destinations):")
    for year in sorted(totals):
        print(f"  {year}: {totals[year] / 1000:7.1f}")


if __name__ == "__main__":
    main()
