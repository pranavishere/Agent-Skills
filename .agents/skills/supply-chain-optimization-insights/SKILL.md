---
name: supply-chain-optimization-insights
description: Generate broader supply-chain insights from inventory, SKU, pricing, depletion forecast, region, and date data. Use when the user asks for additional insights, lean inventory recommendations, safety stock optimization, forecast quality checks, outlier detection, working-capital reduction, or ways to prevent out-of-stocks while avoiding excess stock.
---

# Supply Chain Optimization Insights

Use this skill for insights beyond direct SKU-level and region-level inventory trend analysis. The goal is a lean, stable supply chain with no avoidable out-of-stocks and appropriate safety stock.

## Required Data

Read `references/inventory-data-guide.md` before analysis. Use:

1. `inventory_monthly.csv`
2. `sku_brand_pricing.csv`
3. `depletion_forecast.csv`
4. `state_region.csv`
5. `date_dimension.csv`

## Insight Areas

Evaluate these angles when relevant:

1. Forecast quality and volatility:
   - Compare historical inventory movement against forward depletion forecast.
   - Flag SKUs where forecasted depletion sharply diverges from recent trend.
   - Identify seasonality-sensitive SKUs that need higher temporary safety stock.
2. Working capital:
   - Rank excess inventory by dollar value.
   - Identify slow-moving high-value SKUs.
   - Separate strategic safety stock from avoidable overstock.
3. Service-level risk:
   - Identify SKUs with repeated low coverage across multiple states or warehouses.
   - Prioritize stockout prevention by brand family, SKU criticality, and forecast demand.
4. Network balance:
   - Identify warehouses with persistent excess or shortage patterns.
   - Recommend transfer, allocation, or reorder policy changes.
5. Data quality:
   - Check missing brand mappings, missing prices, negative inventory, zero forecast, impossible values, and month gaps.
   - Call out outliers before drawing conclusions from them.

## Measures

Quantify every recommendation when data allows:

- Inventory units.
- Inventory value.
- Forecast depletion units.
- Planned receipt units.
- Coverage months.
- Safety stock units.
- Replenishment units.
- Transfer units.
- Overstock units.
- Dollar value at risk.

## Output

Provide a concise executive summary followed by prioritized recommendations. For each recommendation, include:

- Problem.
- Evidence.
- Financial or service-level impact.
- Recommended action.
- Expected unit impact.
- Expected dollar impact.
- Confidence and assumptions.
