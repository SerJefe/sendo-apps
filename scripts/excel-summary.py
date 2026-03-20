#!/usr/bin/env python3
import openpyxl, json, sys
from collections import defaultdict

if len(sys.argv) < 2:
    print("Usage: python3 excel-summary.py file.xlsx [month]", file=sys.stderr)
    sys.exit(1)

file_path = sys.argv[1]
target_month = sys.argv[2] if len(sys.argv) > 2 else "2026-01"

wb = openpyxl.load_workbook(file_path, read_only=True, data_only=True)
ws = wb['PRODUCCION OYMA']

contracts = {}
for row in ws.iter_rows(min_row=2, values_only=True):
    if row[0] and hasattr(row[0], 'strftime') and row[0].strftime('%Y-%m') == target_month:
        cia = str(row[7]) if row[7] else "?"
        contracts[cia] = {
            "prod": float(row[1]) if row[1] else 0,
            "cost": float(row[5]) if row[5] else 0,
            "uai": float(row[6]) if row[6] else 0
        }

# Add calculated fields
for c in contracts.values():
    c["margin"] = (c["uai"]/c["prod"]*100) if c["prod"] else 0

total = {"prod": sum(c["prod"] for c in contracts.values()),
         "cost": sum(c["cost"] for c in contracts.values()),
         "uai": sum(c["uai"] for c in contracts.values())}
total["margin"] = (total["uai"]/total["prod"]*100) if total["prod"] else 0

output = {"month": target_month, "contracts": contracts, "total": total}
print(json.dumps(output, indent=2))
