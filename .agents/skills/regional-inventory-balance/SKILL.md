---
name: regional-inventory-balance
description: Analyze inventory trends, stock coverage, valuation, and distribution by region across East, West, North, and South. Use when the user asks for region-wise inventory trends, regional stock imbalances, coverage gaps, warehouse transfer recommendations, or replenishment strategy by region.
---

# Regional Inventory Balance

Analyze inventory across region, state, warehouse, brand family, brand, SKU, and month. Use the state-to-region mapping, inventory history/forward projection, SKU pricing attributes, depletion forecast, and date dimension together.

## Required Data

Read `references/inventory-data-guide.md` before analysis. Use the five-source dataset it describes:

1. `inventory_monthly.csv`
2. `sku_brand_pricing.csv`
3. `depletion_forecast.csv`
4. `state_region.csv`
5. `date_dimension.csv`

## Workflow

1. Join state to region using `state_region.csv`.
2. Normalize dates to end-of-month using `date_dimension.csv`.
3. Aggregate inventory volume and inventory value by region, state, warehouse, brand family, brand, SKU, and month.
4. Compare on-hand inventory to the depletion forecast to calculate stock coverage:
   - `coverage_months = inventory_units / next_3_month_avg_forecast_units`
   - `surplus_units = inventory_units - target_safety_stock_units`
   - `shortage_units = max(0, target_safety_stock_units - inventory_units)`
5. Segment each region:
   - Critical: less than 1.0 month of coverage.
   - Watchlist: 1.0 to 1.5 months of coverage.
   - Healthy: 1.5 to 3.0 months of coverage.
   - Excess: more than 3.0 months of coverage.
6. Identify rebalancing opportunities where one region has excess coverage while another has critical or watchlist coverage for the same brand/SKU.
7. Recommend replenishment, warehouse transfer, or allocation changes in units and dollars.

## Output

Lead with region-level risk and recommended action. Include:

- Regions with the highest out-of-stock risk.
- Regions with excess inventory value or slow-moving inventory.
- Brand families driving the largest imbalance.
- SKUs that should be transferred across regions.
- Recommended replenishment or transfer quantity in units and inventory value.
- Assumptions, especially where forecast or pricing coverage is incomplete.
