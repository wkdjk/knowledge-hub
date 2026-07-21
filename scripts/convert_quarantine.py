#!/usr/bin/env python3
"""Convert the QIA quarantine flat CSV (monthly) into the site's import files.

Usage:
    python3 scripts/convert_quarantine.py "sources/deer_velvet_quarantine_20192026_flat.csv"

Outputs (relative to repo root):
    data/imports-monthly.csv  - source of record: year x month x country x form, kg
                                (Import rows only; dried and frozen velvet)
    data/imports.csv          - chart file: year x country, dried-equivalent tonnes
                                For years the monthly file covers completely
                                (all 12 months) the totals come from this monthly
                                data; earlier years (< first complete monthly year)
                                are preserved from data/imports-annual.csv so the
                                chart keeps its long history.

Deer velvet extract rows and Export rows are excluded from import volume.
Same input always produces byte-identical output. A summary is printed for
eyeball verification.
"""
import csv
import sys
from collections import defaultdict
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
FROZEN_TO_DRIED = 0.33
FORM = {"Dried deer velvet": "dried", "Frozen deer velvet": "frozen"}


def fail(msg):
    sys.exit(f"ERROR: {msg}")


def main():
    if len(sys.argv) != 2:
        fail(f"usage: {sys.argv[0]} <quarantine flat CSV>")
    src = Path(sys.argv[1])
    if not src.exists():
        fail(f"input file not found: {src}")

    with open(src, newline="", encoding="utf-8-sig") as f:
        rows = list(csv.DictReader(f))
    need = {"Year", "Month", "Trade", "Product", "Country", "Quantity_kg"}
    if not need.issubset(rows[0].keys()):
        fail(f"missing expected columns; found {list(rows[0].keys())}")

    # Monthly import record: dried/frozen only.
    records = []          # (year, month, country, form, kg)
    months_seen = defaultdict(set)
    for r in rows:
        year, month = int(r["Year"]), int(r["Month"])
        months_seen[year].add(month)
        if r["Trade"] != "Import":
            continue
        form = FORM.get(r["Product"])
        if not form:
            continue          # skip extract
        kg = float(r["Quantity_kg"])
        records.append((year, month, r["Country"], form, kg))

    records.sort(key=lambda x: (x[0], x[1], x[2], x[3]))
    monthly_path = REPO_ROOT / "data" / "imports-monthly.csv"
    with open(monthly_path, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["year", "month", "country", "form", "kg"])
        for year, month, country, form, kg in records:
            w.writerow([year, month, country, form, f"{kg:g}"])

    complete_years = {y for y, ms in months_seen.items() if len(ms) == 12}

    # Dried-equivalent tonnes per year x country from the monthly data.
    eq = defaultdict(float)
    for year, month, country, form, kg in records:
        if year not in complete_years:
            continue
        eq[(year, country)] += kg * (1.0 if form == "dried" else FROZEN_TO_DRIED)

    monthly_years = sorted(complete_years)
    first_monthly = monthly_years[0] if monthly_years else None

    # Preserve earlier years from the annual workbook output, if present.
    annual_path = REPO_ROOT / "data" / "imports-annual.csv"
    preserved = defaultdict(float)
    if annual_path.exists() and first_monthly is not None:
        for r in csv.DictReader(open(annual_path, encoding="utf-8-sig")):
            y = int(r["year"])
            if y >= first_monthly or r.get("coverage") == "partial":
                continue
            factor = 1.0 if r["form"] == "dried" else FROZEN_TO_DRIED
            preserved[(y, r["country"])] += float(r["kg"]) * factor

    combined = dict(preserved)
    for k, v in eq.items():
        combined[k] = v

    imports_path = REPO_ROOT / "data" / "imports.csv"
    with open(imports_path, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["year", "country", "tonnes"])
        for (year, country) in sorted(combined):
            w.writerow([year, country, f"{combined[(year, country)] / 1000:.1f}"])

    # ---- verification summary ----
    all_years = sorted(months_seen)
    partial = sorted(y for y in months_seen if y not in complete_years)
    print(f"input : {src}")
    print(f"parsed: {len(records)} monthly import rows, years {all_years[0]}-{all_years[-1]}")
    if partial:
        print(f"partial years (excluded from imports.csv): {partial}")
    if preserved:
        pre_years = sorted({y for (y, _) in preserved})
        print(f"preserved from annual workbook: {pre_years[0]}-{pre_years[-1]}")
    print(f"wrote : {monthly_path} ({len(records)} rows)")
    print(f"wrote : {imports_path} ({len(combined)} rows)")
    print("\ndried-equivalent import totals by year (tonnes):")
    totals = defaultdict(float)
    for (year, _), v in combined.items():
        totals[year] += v
    for year in sorted(totals):
        tag = "" if year in complete_years or year < (first_monthly or 0) else " (partial)"
        print(f"  {year}: {totals[year] / 1000:6.1f}{tag}")


if __name__ == "__main__":
    main()
