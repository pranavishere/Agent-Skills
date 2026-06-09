# Hypothetical Inventory Data Guide

Default sample dataset path: `outputs/supply-chain-manager/data`.

## Data Sources

1. `inventory_monthly.csv`: monthly inventory across historical, current, and forward months at state, warehouse, SKU grain. Includes brand hierarchy, inventory volume, inventory value, seasonality, outlier, and trend fields.
2. `sku_brand_pricing.csv`: SKU-to-brand mapping plus state/warehouse-specific pricing, cost, case pack, pallet quantity, safety stock, target coverage, and lead time measures.
3. `depletion_forecast.csv`: 12-month forward depletion forecast by state, warehouse, SKU, and month. Includes forecast units, planned receipts, expected stock coverage, out-of-stock risk, and recommended replenishment units.
4. `state_region.csv`: state-to-region mapping for East, West, North, and South.
5. `date_dimension.csv`: month-end normalization and fiscal calendar attributes.

## Grain

Use state, warehouse, SKU, and month as the base grain. Roll up only after calculating SKU-level measures.

## Core Measures

- `inventory_units`: units on hand or projected on hand.
- `inventory_value_usd`: inventory dollar valuation.
- `unit_cost_usd`: cost basis for replenishment and inventory valuation.
- `list_price_usd`: retail/list price.
- `wholesale_price_usd`: sell-in or wholesale price.
- `forecast_depletion_units`: expected units depleted in a forecast month.
- `planned_receipt_units`: expected replenishment receipts already planned for a forecast month.
- `coverage_months`: estimated months of stock coverage.
- `target_safety_stock_units`: target buffer inventory.
- `recommended_replenishment_units`: units needed to restore target coverage.
- `recommended_replenishment_value_usd`: replenishment value at unit cost.

## Risk Thresholds

- Critical: less than 1.0 month of coverage.
- High: 1.0 to 1.5 months.
- Moderate: 1.5 to 2.0 months.
- Healthy: 2.0 to 3.0 months.
- Excess: more than 3.0 months.

## Analysis Rules

- Do not compare raw inventory without accounting for forecast depletion.
- Use unit and dollar measures together; a low-unit SKU can still be material if high value.
- Treat seasonality and outliers as explanations to test, not automatic conclusions.
- Prefer replenishment recommendations that reach target coverage without creating excess inventory.
- Where one warehouse has excess and another has shortage for the same SKU, recommend transfer before new purchase.
