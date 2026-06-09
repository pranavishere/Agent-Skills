import csv
import sys
import tomllib
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "outputs" / "supply-chain-manager" / "data"

skills = [
    ROOT / ".agents" / "skills" / "inventory-sku-risk" / "SKILL.md",
    ROOT / ".agents" / "skills" / "regional-inventory-balance" / "SKILL.md",
    ROOT / ".agents" / "skills" / "supply-chain-optimization-insights" / "SKILL.md",
]

required_csv_columns = {
    "inventory_monthly.csv": {
        "snapshot_month", "month_end_date", "month_type", "state", "warehouse",
        "sku", "brand", "brand_family", "inventory_units", "inventory_value_usd",
        "seasonality_index", "outlier_flag", "trend_signal",
    },
    "sku_brand_pricing.csv": {
        "sku", "sku_description", "brand", "brand_family", "state", "warehouse",
        "list_price_usd", "wholesale_price_usd", "unit_cost_usd",
        "case_pack_units", "pallet_units", "safety_stock_days",
        "target_coverage_months", "lead_time_days",
    },
    "depletion_forecast.csv": {
        "forecast_month", "month_end_date", "state", "warehouse", "sku",
        "brand", "brand_family", "forecast_depletion_units",
        "planned_receipt_units", "projected_inventory_units",
        "expected_stock_coverage_months", "target_safety_stock_units",
        "recommended_replenishment_units", "recommended_replenishment_value_usd",
        "potential_oos_flag", "risk_level", "lead_time_days",
    },
    "state_region.csv": {"state", "region", "region_manager", "region_priority_score"},
    "date_dimension.csv": {
        "calendar_month", "month_end_date", "fiscal_year", "fiscal_quarter",
        "month_number", "relative_month", "month_type",
    },
}


def fail(message):
    print(f"FAIL: {message}")
    sys.exit(1)


agent_path = ROOT / ".codex" / "agents" / "supply-chain-manager.toml"
with agent_path.open("rb") as handle:
    agent = tomllib.load(handle)
for key in ("name", "description", "developer_instructions"):
    if not agent.get(key):
        fail(f"agent missing {key}")

for skill_path in skills:
    text = skill_path.read_text(encoding="utf-8")
    if "[TODO" in text or "TODO:" in text:
        fail(f"{skill_path} contains TODO text")
    if not text.startswith("---\n"):
        fail(f"{skill_path} missing YAML frontmatter")
    frontmatter = text.split("---\n", 2)[1]
    if "name:" not in frontmatter or "description:" not in frontmatter:
        fail(f"{skill_path} missing name or description")

for filename, required in required_csv_columns.items():
    path = DATA_DIR / filename
    with path.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        columns = set(reader.fieldnames or [])
        missing = required - columns
        if missing:
            fail(f"{filename} missing columns: {sorted(missing)}")
        rows = list(reader)
        if not rows:
            fail(f"{filename} has no rows")
        print(f"OK: {filename}: {len(rows)} rows")

print("OK: supply-chain-manager package structure validated")
