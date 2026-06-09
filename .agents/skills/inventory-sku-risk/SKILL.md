---
name: inventory-sku-risk
description: Analyze SKU-level inventory trends, valuation, forecast coverage, and out-of-stock risk at state, warehouse, SKU, brand, and brand-family grain. Use when the user asks to compare inventory against depletion forecast, identify brands or SKUs at risk of going out of stock, quantify replenishment needs, or explain SKU-level inventory movement using seasonality, outliers, and trend context.
---

# Inventory SKU Risk

Analyze inventory risk at the state-warehouse-SKU grain, then roll insights up to brand and brand family. Compare historical/current/projected inventory against the 12-month depletion forecast.

## Required Data

Read `references/inventory-data-guide.md` before analysis. Use the five-source dataset it describes:

1. `inventory_monthly.csv`
2. `sku_brand_pricing.csv`
3. `depletion_forecast.csv`
4. `state_region.csv`
5. `date_dimension.csv`

## Workflow

1. Normalize inventory dates to month end using `date_dimension.csv`.
2. Join SKU brand and pricing attributes from `sku_brand_pricing.csv`.
3. Join depletion forecast at state, warehouse, SKU, and forecast month.
4. Calculate measures:
   - `inventory_units`
   - `inventory_value_usd`
   - `forecast_depletion_units`
   - `planned_receipt_units`
   - `coverage_months = inventory_units / next_3_month_avg_forecast_units`
   - `target_safety_stock_units = next_3_month_avg_forecast_units * target_coverage_months`
   - `recommended_replenishment_units = max(0, target_safety_stock_units - inventory_units)`
   - `recommended_replenishment_value_usd = recommended_replenishment_units * unit_cost_usd`
5. Account for seasonality:
   - Treat `seasonality_index` above `1.15` as elevated seasonal demand.
   - Treat `seasonality_index` below `0.90` as soft seasonal demand.
   - Do not overreact to a one-month outlier unless the forward forecast confirms the trend.
6. Segment risk:
   - Critical: coverage below `1.0` month or potential out-of-stock within 60 days.
   - High: coverage from `1.0` to `1.5` months.
   - Moderate: coverage from `1.5` to `2.0` months.
   - Healthy: coverage from `2.0` to `3.0` months.
   - Excess: coverage above `3.0` months.
7. Recommend replenishment by SKU, state, and warehouse in both units and dollars.

## Output

Lead with the highest-risk brands and SKUs. Include:

- SKU, brand, brand family, state, and warehouse.
- Current inventory units and value.
- Forward depletion forecast.
- Coverage months.
- Out-of-stock risk window.
- Recommended replenishment units and value.
- Notes on seasonality, outliers, and trend direction.
- Assumptions and data quality caveats.
