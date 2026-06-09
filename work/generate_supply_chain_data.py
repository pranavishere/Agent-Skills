import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "outputs" / "supply-chain-manager" / "data"

BASE_DEMAND = {
    "SKU-1001": 540,
    "SKU-1002": 470,
    "SKU-2001": 390,
    "SKU-2002": 310,
    "SKU-3001": 620,
    "SKU-3002": 420,
    "SKU-4001": 360,
}

STATE_FACTOR = {
    "CA": 1.18,
    "WA": 0.82,
    "NY": 1.22,
    "FL": 0.95,
    "TX": 1.10,
    "IL": 0.88,
}

SEASONALITY = {
    1: 0.86,
    2: 0.90,
    3: 0.98,
    4: 1.05,
    5: 1.12,
    6: 1.18,
    7: 1.24,
    8: 1.20,
    9: 1.08,
    10: 1.00,
    11: 0.96,
    12: 1.15,
}


def read_csv(path):
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def write_csv(path, rows, fieldnames):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


pricing = read_csv(DATA_DIR / "sku_brand_pricing.csv")
dates = read_csv(DATA_DIR / "date_dimension.csv")
future_dates = [row for row in dates if row["month_type"] == "Forward"]

inventory_rows = []
forecast_rows = []

for item_idx, item in enumerate(pricing):
    sku = item["sku"]
    state = item["state"]
    warehouse = item["warehouse"]
    unit_cost = float(item["unit_cost_usd"])
    target_coverage = float(item["target_coverage_months"])
    lead_time_days = int(item["lead_time_days"])
    base = BASE_DEMAND[sku] * STATE_FACTOR[state]

    current_units = None
    for date_row in dates:
        rel = int(date_row["relative_month"])
        month_num = int(date_row["month_number"])
        seasonality = SEASONALITY[month_num]
        trend = 1 + (rel * 0.012)
        outlier_flag = "N"

        if sku == "SKU-1001" and state == "NY" and date_row["calendar_month"] == "2026-05":
            outlier_flag = "Y"
            trend_signal = "Promo spike depleted inventory faster than normal"
            demand_pressure = 1.42
        elif sku == "SKU-4001" and state == "NY" and date_row["calendar_month"] == "2026-06":
            outlier_flag = "Y"
            trend_signal = "Supplier delay caused unusually low stock"
            demand_pressure = 1.25
        elif sku in {"SKU-2001", "SKU-2002"} and month_num in {6, 7, 8}:
            trend_signal = "Summer seasonal build"
            demand_pressure = 1.15
        elif rel > 0:
            trend_signal = "Forward projected inventory"
            demand_pressure = 1.04
        elif rel < -3:
            trend_signal = "Historical baseline"
            demand_pressure = 1.00
        else:
            trend_signal = "Recent trend"
            demand_pressure = 1.06

        demand_units = base * seasonality * trend * demand_pressure
        if rel < 0:
            inventory_units = max(90, int(demand_units * (2.2 - (rel / 48)) + (item_idx % 4) * 45))
        elif rel == 0:
            inventory_units = max(75, int(demand_units * (1.55 - (item_idx % 3) * 0.18)))
            current_units = inventory_units
        else:
            replenishment = 0
            if sku in {"SKU-1001", "SKU-4001"} and rel in {2, 5, 8}:
                replenishment = int(base * 1.1)
            if sku in {"SKU-2001", "SKU-2002"} and rel in {1, 4, 7}:
                replenishment = int(base * 1.35)
            current_units = max(25, int(current_units - demand_units + replenishment))
            inventory_units = current_units

        inventory_rows.append({
            "snapshot_month": date_row["calendar_month"],
            "month_end_date": date_row["month_end_date"],
            "month_type": date_row["month_type"],
            "state": state,
            "warehouse": warehouse,
            "sku": sku,
            "brand": item["brand"],
            "brand_family": item["brand_family"],
            "inventory_units": inventory_units,
            "inventory_value_usd": f"{inventory_units * unit_cost:.2f}",
            "seasonality_index": f"{seasonality:.2f}",
            "outlier_flag": outlier_flag,
            "trend_signal": trend_signal,
        })

    starting_inventory = next(
        int(row["inventory_units"])
        for row in inventory_rows
        if row["sku"] == sku
        and row["state"] == state
        and row["warehouse"] == warehouse
        and row["snapshot_month"] == "2026-06"
    )

    projected_units = starting_inventory
    for forecast_idx, date_row in enumerate(future_dates, start=1):
        month_num = int(date_row["month_number"])
        seasonality = SEASONALITY[month_num]
        forecast_units = int(base * seasonality * (1 + forecast_idx * 0.015))
        next_3_avg = int(forecast_units * 1.04)
        target_safety_stock = int(next_3_avg * target_coverage)
        is_delayed_risk_case = (sku == "SKU-1001" and state == "NY") or (sku == "SKU-4001" and state == "NY")
        if sku == "SKU-1001" and state == "NY":
            planned_receipt_units = int(base * 2.2) if forecast_idx in {3, 7, 11} else 0
        elif sku == "SKU-4001" and state == "NY":
            planned_receipt_units = int(base * 1.9) if forecast_idx in {5, 9} else 0
        elif sku in {"SKU-2001", "SKU-2002"}:
            planned_receipt_units = int(base * 2.6) if forecast_idx in {1, 4, 7, 10} else 0
        elif sku == "SKU-3001" and state == "TX":
            planned_receipt_units = int(base * 1.4) if forecast_idx in {2, 6, 10} else 0
        else:
            planned_receipt_units = int(base * 2.0) if forecast_idx in {1, 5, 9} else 0

        projected_after_receipts = projected_units + planned_receipt_units - forecast_units
        if not is_delayed_risk_case and projected_after_receipts < target_safety_stock:
            planned_receipt_units += int((target_safety_stock - projected_after_receipts) * 1.15)

        projected_units = max(0, projected_units + planned_receipt_units - forecast_units)
        coverage_months = projected_units / next_3_avg if next_3_avg else 0
        recommended_replenishment = max(0, target_safety_stock - projected_units)
        potential_oos = "Y" if coverage_months < 1.0 or projected_units == 0 else "N"
        risk_level = (
            "Critical" if coverage_months < 1.0 else
            "High" if coverage_months < 1.5 else
            "Moderate" if coverage_months < 2.0 else
            "Healthy" if coverage_months <= 3.0 else
            "Excess"
        )

        forecast_rows.append({
            "forecast_month": date_row["calendar_month"],
            "month_end_date": date_row["month_end_date"],
            "state": state,
            "warehouse": warehouse,
            "sku": sku,
            "brand": item["brand"],
            "brand_family": item["brand_family"],
            "forecast_depletion_units": forecast_units,
            "planned_receipt_units": planned_receipt_units,
            "projected_inventory_units": projected_units,
            "expected_stock_coverage_months": f"{coverage_months:.2f}",
            "target_safety_stock_units": target_safety_stock,
            "recommended_replenishment_units": recommended_replenishment,
            "recommended_replenishment_value_usd": f"{recommended_replenishment * unit_cost:.2f}",
            "potential_oos_flag": potential_oos,
            "risk_level": risk_level,
            "lead_time_days": lead_time_days,
        })

write_csv(
    DATA_DIR / "inventory_monthly.csv",
    inventory_rows,
    [
        "snapshot_month",
        "month_end_date",
        "month_type",
        "state",
        "warehouse",
        "sku",
        "brand",
        "brand_family",
        "inventory_units",
        "inventory_value_usd",
        "seasonality_index",
        "outlier_flag",
        "trend_signal",
    ],
)

write_csv(
    DATA_DIR / "depletion_forecast.csv",
    forecast_rows,
    [
        "forecast_month",
        "month_end_date",
        "state",
        "warehouse",
        "sku",
        "brand",
        "brand_family",
        "forecast_depletion_units",
        "planned_receipt_units",
        "projected_inventory_units",
        "expected_stock_coverage_months",
        "target_safety_stock_units",
        "recommended_replenishment_units",
        "recommended_replenishment_value_usd",
        "potential_oos_flag",
        "risk_level",
        "lead_time_days",
    ],
)

print(f"Wrote {len(inventory_rows)} inventory rows")
print(f"Wrote {len(forecast_rows)} forecast rows")
