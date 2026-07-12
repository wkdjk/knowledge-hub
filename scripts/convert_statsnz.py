#!/usr/bin/env python3
"""Convert a Stats NZ "Harmonised Trade - Exports (Monthly)" CSV export into
the site's NZ velvet export CSV files.

Usage:
    python3 scripts/convert_statsnz.py "sources/NZ Stats - HarmonisedTradeExports_20260629.csv"

Outputs (always written relative to the repo root):
    data/nz-exports-monthly.csv  - source of record: month x destination country, kg
                                    (velvet categories only: frozen / dried / other)
    data/nz-exports.csv          - chart file: year x tonnes, summed across all
                                    destination countries in the export

The same input always produces byte-identical output (fixed sort order, no
timestamps). After running, a summary is printed for eyeball verification.

Note: only the "velvet" HS categories are counted (frozen / dried / other-than-
frozen-or-dried). The separate "horns and antlers, unworked" and "powder of
horns and velvet" categories in the Stats NZ export are excluded, to match
what QIA calls dried/frozen velvet (녹용/생녹용) on the Korean side.
"""
import csv
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
VELVET_CATEGORIES = {
    "Animal products; velvet and waste products (excluding powder), of deer, unworked, frozen": "frozen",
    "Animal products; velvet and waste products (excluding powder), of deer, unworked, dried": "dried",
    "Animal products; velvet and waste products (excluding powder) of deer, unworked, other than frozen or dried": "other",
}
MONTH_RE = re.compile(r"^(\d{4})M(\d{2})$")


def fail(msg):
    sys.exit(f"ERROR: {msg}")


def main():
    if len(sys.argv) != 2:
        fail(f"usage: {sys.argv[0]} <Stats NZ export CSV>")
    src = Path(sys.argv[1])
    if not src.exists():
        fail(f"input file not found: {src}")

    with open(src, newline="", encoding="utf-8-sig") as f:
        rows = list(csv.reader(f))
    if len(rows) < 4:
        fail("file too short to contain the expected header block")

    width = max(len(r) for r in rows[:4])
    header_rows = [r + [""] * (width - len(r)) for r in rows[:4]]
    country_row, category_row, measure_row = header_rows[1], header_rows[2], header_rows[3]

    # Forward-fill the sparse country/category header cells.
    countries = []
    last = None
    for v in country_row:
        if v.strip():
            last = v.strip()
        countries.append(last)
    categories = []
    last = None
    for v in category_row:
        if v.strip():
            last = v.strip()
        categories.append(last)

    columns = []  # (col_index, country, form)
    for i in range(1, width):
        if measure_row[i].strip() != "Quantity":
            continue
        cat = categories[i]
        if cat not in VELVET_CATEGORIES:
            continue
        country = countries[i]
        if not country:
            continue
        columns.append((i, country, VELVET_CATEGORIES[cat]))
    if not columns:
        fail("no velvet quantity columns found - has the export layout changed?")

    records = []  # (year, month, country, form, kg)
    months_seen = {}  # year -> set(month), regardless of value, for completeness checks
    for row in rows[4:]:
        if not row or not row[0]:
            continue
        m = MONTH_RE.match(row[0].strip().strip('"'))
        if not m:
            break  # reached the trailing "Table information:" footer block
        year, month = int(m.group(1)), int(m.group(2))
        months_seen.setdefault(year, set()).add(month)
        for col, country, form in columns:
            if col >= len(row):
                continue
            raw = row[col].strip()
            if raw == "":
                continue
            try:
                kg = float(raw)
            except ValueError:
                fail(f"non-numeric quantity {raw!r} for {row[0]} col {col}")
            if kg:
                records.append((year, month, country, form, kg))

    if not records:
        fail("no monthly data rows parsed")

    records.sort(key=lambda x: (x[0], x[1], x[2], x[3]))

    monthly_path = REPO_ROOT / "data" / "nz-exports-monthly.csv"
    with open(monthly_path, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["year", "month", "destination", "form", "kg"])
        for year, month, country, form, kg in records:
            w.writerow([year, month, country, form, f"{kg:g}"])

    # Chart file: total tonnes per year across all destinations, complete years only.
    by_year_month = months_seen
    complete_years = {y for y, months in by_year_month.items() if len(months) == 12}

    totals = {}
    for year, month, country, form, kg in records:
        if year not in complete_years:
            continue
        totals[year] = totals.get(year, 0.0) + kg

    exports_path = REPO_ROOT / "data" / "nz-exports.csv"
    with open(exports_path, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["year", "tonnes"])
        for year in sorted(totals):
            w.writerow([year, f"{totals[year] / 1000:.1f}"])

    # ---- verification summary ----
    years = sorted({y for y, *_ in records})
    dest_countries = sorted({c for _, _, c, _, _ in records})
    print(f"input : {src}")
    print(f"parsed: {len(records)} monthly data cells "
          f"({len(dest_countries)} destinations: {', '.join(dest_countries)})")
    print(f"period: {years[0]}-{min(by_year_month[years[0]])} "
          f"to {years[-1]}-{max(by_year_month[years[-1]]):02d}")
    incomplete = sorted(set(years) - complete_years)
    if incomplete:
        print(f"partial years excluded from {exports_path.name}: {incomplete}")
    print(f"wrote : {monthly_path} ({len(records)} rows)")
    print(f"wrote : {exports_path} ({len(totals)} rows)")
    print("\ntotal velvet export tonnes by year (all destinations):")
    for year in sorted(totals):
        print(f"  {year}: {totals[year] / 1000:,.1f}")


if __name__ == "__main__":
    main()
